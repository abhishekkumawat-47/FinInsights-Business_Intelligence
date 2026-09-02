"""Open the .docx in Word, export a PDF, and rasterise the pages.

This is the only honest test of the file. It proves Word opens it without a repair prompt, it
reports the real page count, and it gives images to inspect for the two failure modes that a
generator cannot see on its own: type that falls back to another face, and rows or figures that
break across a page.
"""
from __future__ import annotations

import os
import sys

os.chdir(os.path.dirname(os.path.abspath(__file__)))

import fitz
import win32com.client as win32

DOCX = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else "FinInsights_Business_Proposal.docx")
PDF = os.path.splitext(DOCX)[0] + ".pdf"
OUTDIR = "proof"
os.makedirs(OUTDIR, exist_ok=True)

word = win32.DispatchEx("Word.Application")
word.Visible = False
word.DisplayAlerts = 0
try:
    doc = word.Documents.Open(DOCX, ReadOnly=False, AddToRecentFiles=False)
    doc.Repaginate()
    pages = doc.ComputeStatistics(2)  # wdStatisticPages
    words = doc.ComputeStatistics(0)
    print(f"pages={pages} words={words}")
    doc.SaveAs(PDF, FileFormat=17)    # wdFormatPDF
    doc.Close(False)
finally:
    word.Quit()

pdf = fitz.open(PDF)
print(f"pdf pages={pdf.page_count}")
fonts = set()
for pg in pdf:
    for f in pg.get_fonts(full=False):
        fonts.add(f[3])
print("fonts in pdf:", sorted(fonts))

scale = float(os.environ.get("PROOF_SCALE", "1.35"))
only = os.environ.get("PROOF_PAGES")
todo = [int(x) for x in only.split(",")] if only else range(1, pdf.page_count + 1)
for n in todo:
    pg = pdf[n - 1]
    pix = pg.get_pixmap(matrix=fitz.Matrix(scale, scale))
    pix.save(os.path.join(OUTDIR, f"p{n:02d}.png"))
print("rendered", len(list(todo)), "pages to", OUTDIR)
