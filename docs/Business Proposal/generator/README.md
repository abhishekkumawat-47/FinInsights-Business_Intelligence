# Rebuilding the business proposal

`FinInsights_Business_Proposal.docx` is generated, not hand-edited. Edit the source here and
rebuild , editing the `.docx` directly means the next rebuild silently discards your change.

## Where things live

| File | What it owns |
|---|---|
| `theme.py` | The palette, copied hex for hex from `dashboard/src/app/globals.css`, and the font paths |
| `charts.py` | Every figure, authored at exactly the 15 cm text column so nothing rescales on the page |
| `cover.py` | The full-bleed A4 cover, drawn rather than laid out in Word |
| `docx_kit.py` | The typographic system: page setup, headings, tables, panels, stat bands, figures |
| `embed_fonts.py` | Embeds Archivo into the package so the file typesets identically on any machine |
| `sources.py` | Every external claim: publisher, title, date, URL, tier, caveat. Inline citations and the reference list are both generated from it, so they cannot drift apart |
| `content_a/b/c.py` | The document text, in reading order |
| `make.py` | Renders the figures, builds the document, embeds the fonts |
| `proof.py` | Opens the result in Word, exports a PDF, rasterises the pages |
| `audit.py` | Flags pages whose trailing whitespace reads as a layout accident |

## Build

```bash
python -m venv .venv && .venv/Scripts/python -m pip install python-docx matplotlib pywin32 pymupdf
.venv/Scripts/python make.py          # -> FinInsights_Business_Proposal.docx
.venv/Scripts/python proof.py         # -> .pdf + proof/p01.png ... (needs Word on Windows)
.venv/Scripts/python audit.py         # any page over ~4.5 cm of trailing white needs reflowing
```

`proof.py` is the only honest test of the file: it proves Word opens it without a repair prompt,
reports the real page count, and gives you images to check for type falling back to another face.

## House rules this document holds itself to

**No em dashes, anywhere.** `make.py` fails nothing on its own, so check after every build:

```bash
python -c "import zipfile;z=zipfile.ZipFile('FinInsights_Business_Proposal.docx');print(sum(z.read(n).decode('utf8','ignore').count(chr(8212)) for n in z.namelist() if n.endswith('.xml')))"
```

It must print 0. The count includes headers, footers and `docProps/core.xml`, which is where a
document title quietly reintroduces one.

**Every chart says what kind of thing it is.** `charts._tag()` prints a provenance label on the
figure itself: FROM THE BUILD, MODELLED, ILLUSTRATIVE or OUR ASSESSMENT. A chart of invented
numbers that looks like a chart of measured numbers is the exact failure this product exists to
prevent, so it must never be possible to screenshot one out of context.

**A claim not in `sources.py` cannot be cited.** If a figure cannot be traced to a primary source,
it gets removed, qualified, or listed in the "claims we could not verify" panel in Appendix B.

## Typographic decisions, and why

Body is 10.5 pt on 130% leading in a 15 cm measure, inside Butterick's bands of 10 to 12 pt,
120 to 145% leading and 45 to 90 characters. Paragraphs are separated by space and never also by an indent. Body ink is
`#342F49` on white (about 11:1) and the lightest text at body size is `#6C6581` (about 6:1), both
clear of the WCAG 2.2 SC 1.4.3 minimum of 4.5:1; the 3:1 large-text allowance is used only for
display figures at 18 pt and above. Tables carry no vertical rules: a header band, hairline row
separators, and numerals right-aligned and tabular.

Sections flow rather than each claiming a fresh page. A forced break before every section leaves a
stub page whenever a section overruns by a line, so instead each opener carries a rule above it and
its kicker, title, standfirst and first paragraph are bound together.

## Fonts

`fonts/static/` holds four static instances of Archivo (400 and 700, roman and italic), generated
from the variable font in `google/fonts` with `fontTools.varLib.instancer`. They are embedded in
the `.docx`, so a reader without Archivo installed still sees the document as designed. Without
embedding, Word falls back to Cambria and the page count changes.
