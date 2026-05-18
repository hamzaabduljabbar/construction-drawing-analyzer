#!/usr/bin/env python3
"""
split_drawings.py

Splits a merged construction drawing PDF into individual sheet files.
Creates a PNG image and extracts text layer for each sheet.

Usage:
    python scripts/split_drawings.py <input_pdf> [output_dir]

Output structure:
    sheets/
        SHEET-001.pdf
        SHEET-001.txt   (extracted text/vector layer)
        SHEET-001.png   (rendered image at max Claude resolution)
        SHEET-002.pdf
        ...
"""

import sys
import os
from pathlib import Path


def split_drawings(input_pdf: str, output_dir: str = "sheets"):
    """Split a merged PDF into individual drawing sheets."""
    try:
        from pypdf import PdfReader, PdfWriter
    except ImportError:
        print("Installing pypdf...")
        os.system("pip install pypdf --break-system-packages -q")
        from pypdf import PdfReader, PdfWriter

    try:
        import fitz  # PyMuPDF for rendering
    except ImportError:
        print("Installing PyMuPDF for image rendering...")
        os.system("pip install PyMuPDF --break-system-packages -q")
        import fitz

    input_path = Path(input_pdf)
    if not input_path.exists():
        print(f"Error: File not found: {input_pdf}")
        sys.exit(1)

    out_path = Path(output_dir)
    out_path.mkdir(exist_ok=True)

    reader = PdfReader(str(input_path))
    doc = fitz.open(str(input_path))

    total_sheets = len(reader.pages)
    print(f"Found {total_sheets} sheets in {input_path.name}")

    results = []

    for i, page in enumerate(reader.pages):
        sheet_num = f"SHEET-{i+1:03d}"
        print(f"Processing {sheet_num} ({i+1}/{total_sheets})...")

        # 1. Save individual PDF
        writer = PdfWriter()
        writer.add_page(page)
        pdf_out = out_path / f"{sheet_num}.pdf"
        with open(pdf_out, "wb") as f:
            writer.write(f)

        # 2. Extract text layer (vector data)
        txt_out = out_path / f"{sheet_num}.txt"
        text = page.extract_text() or ""
        with open(txt_out, "w", encoding="utf-8") as f:
            f.write(f"=== {sheet_num} — Extracted Text Layer ===\n\n")
            f.write(text if text.strip() else "[No extractable text layer — scanned or image-only drawing]\n")

        # 3. Render as image at maximum resolution Claude can process
        # Claude's max image processing is ~1568px on longest side for high detail
        fitz_page = doc[i]
        # Use matrix for ~150 DPI rendering (good balance of quality and token cost)
        mat = fitz.Matrix(2.0, 2.0)
        pix = fitz_page.get_pixmap(matrix=mat, alpha=False)
        png_out = out_path / f"{sheet_num}.png"
        pix.save(str(png_out))

        results.append({
            "sheet": sheet_num,
            "pdf": str(pdf_out),
            "txt": str(txt_out),
            "png": str(png_out),
            "has_text": bool(text.strip()),
            "page_size": f"{page.mediabox.width:.0f}x{page.mediabox.height:.0f}pt",
        })

        print(f"  PDF: {pdf_out.stat().st_size / 1024:.1f}KB | "
              f"TXT: {txt_out.stat().st_size / 1024:.1f}KB | "
              f"PNG: {png_out.stat().st_size / 1024:.1f}KB | "
              f"Text layer: {'Yes' if text.strip() else 'No (scanned)'}")

    doc.close()

    print(f"\nDone. {total_sheets} sheets processed → {output_dir}/")
    print(f"Sheets with text layer: {sum(1 for r in results if r['has_text'])}/{total_sheets}")
    print(f"Scanned/image-only sheets: {sum(1 for r in results if not r['has_text'])}/{total_sheets}")

    return results


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python scripts/split_drawings.py <input_pdf> [output_dir]")
        sys.exit(1)

    input_pdf = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else "sheets"
    split_drawings(input_pdf, output_dir)
