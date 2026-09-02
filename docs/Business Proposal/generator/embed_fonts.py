"""Embed Archivo into the .docx so the document is typeset the same on a machine that does not
have the font installed.

A proposal that silently falls back to Calibri on the reader's machine is a different document
from the one that was designed — different measure, different rhythm, different page count. Word
supports embedding, but python-docx does not write it, so the package is edited afterwards.

The obfuscation is the one defined in ECMA-376 §17.8.1: the first 32 bytes of the font file are
XORed with the 16-byte key formed by reading the font-key GUID's hex digits in reverse pairs, and
the file is stored with an .odttf extension.
"""
from __future__ import annotations

import os
import re
import shutil
import uuid
import zipfile

FONT_REL = "http://schemas.openxmlformats.org/officeDocument/2006/relationships/font"
ODTTF_CT = "application/vnd.openxmlformats-officedocument.obfuscatedFont"
NS_W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
NS_R = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"


def obfuscate(data: bytes, guid: str) -> bytes:
    key = bytes.fromhex(guid.strip("{}").replace("-", ""))[::-1]
    out = bytearray(data)
    for i in range(min(32, len(out))):
        out[i] ^= key[i % 16]
    return bytes(out)


def embed(docx_path: str, family: str, faces: dict[str, str]) -> None:
    """faces: {'embedRegular'|'embedBold'|'embedItalic'|'embedBoldItalic': ttf path}."""
    tmp = docx_path + ".tmp"
    zin = zipfile.ZipFile(docx_path)
    names = set(zin.namelist())

    font_parts = {}
    font_rels = []
    for idx, (slot, path) in enumerate(faces.items(), start=1):
        guid = "{" + str(uuid.uuid4()).upper() + "}"
        with open(path, "rb") as fh:
            blob = obfuscate(fh.read(), guid)
        part = f"word/fonts/font{idx}.odttf"
        rid = f"rIdFont{idx}"
        font_parts[part] = blob
        font_rels.append((rid, part, slot, guid))

    # 1. content types — declare the odttf default
    ct = zin.read("[Content_Types].xml").decode("utf8")
    if "obfuscatedFont" not in ct:
        ct = ct.replace("<Types ", "<Types ", 1)
        ct = re.sub(r"(<Types[^>]*>)",
                    r'\1<Default Extension="odttf" ContentType="%s"/>' % ODTTF_CT, ct, count=1)

    # 2. settings — turn embedding on, in its schema position (before defaultTabStop)
    st = zin.read("word/settings.xml").decode("utf8")
    if "embedTrueTypeFonts" not in st:
        flags = "<w:embedTrueTypeFonts/><w:saveSubsetFonts w:val=\"false\"/>"
        if "<w:defaultTabStop" in st:
            st = st.replace("<w:defaultTabStop", flags + "<w:defaultTabStop", 1)
        else:
            st = re.sub(r"(<w:settings[^>]*>)", r"\1" + flags, st, count=1)

    # 3. fontTable — one w:font carrying the four embed references
    ft = zin.read("word/fontTable.xml").decode("utf8")
    ft = re.sub(r"<w:font w:name=\"%s\">.*?</w:font>" % re.escape(family), "", ft, flags=re.S)
    embeds = "".join(
        '<w:%s r:id="%s" w:fontKey="%s" w:subsetted="0"/>' % (slot, rid, guid)
        for rid, _part, slot, guid in font_rels)
    entry = ('<w:font w:name="%s"><w:panose1 w:val="00000000000000000000"/>'
             '<w:charset w:val="00"/><w:family w:val="swiss"/><w:pitch w:val="variable"/>'
             '%s</w:font>' % (family, embeds))
    ft = re.sub(r"(</w:fonts>)", entry + r"\1", ft, count=1)
    root_open = ft[ft.index("<w:fonts"):ft.index(">", ft.index("<w:fonts")) + 1]
    if "xmlns:r=" not in root_open:
        ft = ft.replace("<w:fonts", '<w:fonts xmlns:r="%s"' % NS_R, 1)

    # 4. fontTable rels
    rels_part = "word/_rels/fontTable.xml.rels"
    if rels_part in names:
        rels = zin.read(rels_part).decode("utf8")
    else:
        rels = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
                '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/'
                'relationships"></Relationships>')
    add = "".join('<Relationship Id="%s" Type="%s" Target="fonts/font%d.odttf"/>'
                  % (rid, FONT_REL, i)
                  for i, (rid, _p, _s, _g) in enumerate(font_rels, start=1))
    rels = rels.replace("</Relationships>", add + "</Relationships>")

    replaced = {
        "[Content_Types].xml": ct.encode("utf8"),
        "word/settings.xml": st.encode("utf8"),
        "word/fontTable.xml": ft.encode("utf8"),
        rels_part: rels.encode("utf8"),
    }

    with zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as zout:
        for item in zin.infolist():
            data = replaced.pop(item.filename, None)
            zout.writestr(item, data if data is not None else zin.read(item.filename))
        for name, data in replaced.items():
            zout.writestr(name, data)
        for part, blob in font_parts.items():
            zout.writestr(part, blob)
    zin.close()
    shutil.move(tmp, docx_path)
    return len(font_parts)
