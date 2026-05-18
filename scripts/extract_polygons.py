#!/usr/bin/env python3
"""
extract_polygons.py

Extracts polygon geometry and area calculations from construction drawing PDFs.
Used for quantity takeoffs — runs on specific sheets, not the whole set.

Usage:
    python scripts/extract_polygons.py --sheet SHEET-001
    python scripts/extract_polygons.py --sheet SHEET-001 --sheets-dir sheets
    python scripts/extract_polygons.py --all   (runs on all sheets, use sparingly)

Output:
    Prints a structured report of detected polygons, areas, and dimensions.
    For each polygon: coordinates, calculated area (m²), perimeter (m).
    Includes a summary table of all detected enclosed areas.
"""

import sys
import os
import argparse
from pathlib import Path


def extract_polygons_from_sheet(sheet_pdf: Path, scale_factor: float = None) -> dict:
    """
    Extract polygon data from a single drawing sheet PDF.
    
    Returns dict with:
        - polygons: list of detected closed polygons with vertices and area
        - dimensions: annotated dimension strings found in text layer
        - scale: detected drawing scale (if found in title block)
        - areas: calculated areas in m²
    """
    try:
        import fitz
    except ImportError:
        os.system("pip install PyMuPDF --break-system-packages -q")
        import fitz

    if not sheet_pdf.exists():
        print(f"Error: Sheet not found: {sheet_pdf}")
        return {}

    doc = fitz.open(str(sheet_pdf))
    page = doc[0]

    results = {
        "sheet": sheet_pdf.stem,
        "polygons": [],
        "dimensions": [],
        "scale": None,
        "areas_m2": [],
        "summary": "",
    }

    # Extract drawing scale from text layer
    text_blocks = page.get_text("blocks")
    full_text = " ".join([b[4] for b in text_blocks if isinstance(b[4], str)])

    # Look for scale annotations (common formats: 1:100, 1:200, 1:50)
    import re
    scale_match = re.search(r'1\s*:\s*(\d+)', full_text)
    if scale_match:
        results["scale"] = f"1:{scale_match.group(1)}"
        scale_denominator = int(scale_match.group(1))
    else:
        scale_denominator = 100  # Default assumption: 1:100
        results["scale"] = "1:100 (assumed — not found in text layer)"

    # Extract vector paths (polygon geometry)
    paths = page.get_drawings()
    closed_polygons = []

    for path in paths:
        items = path.get("items", [])
        rect = path.get("rect")

        # Only process closed paths with meaningful area
        if not path.get("closePath") and not path.get("fill"):
            continue

        if rect is None:
            continue

        width_pt = rect.width
        height_pt = rect.height

        # Convert from PDF points to metres using scale
        # 1 PDF point = 1/72 inch = 25.4/72 mm
        pt_to_mm = 25.4 / 72
        width_mm_drawing = width_pt * pt_to_mm
        height_mm_drawing = height_pt * pt_to_mm

        # Apply drawing scale to get real-world dimensions
        width_m_real = (width_mm_drawing * scale_denominator) / 1000
        height_m_real = (height_mm_drawing * scale_denominator) / 1000

        area_m2 = width_m_real * height_m_real

        # Filter: only include polygons with area > 0.1 m² (ignore tiny annotation elements)
        if area_m2 > 0.1:
            closed_polygons.append({
                "rect_pt": [rect.x0, rect.y0, rect.x1, rect.y1],
                "width_m": round(width_m_real, 3),
                "height_m": round(height_m_real, 3),
                "area_m2": round(area_m2, 2),
            })

    # Sort by area descending
    closed_polygons.sort(key=lambda x: x["area_m2"], reverse=True)
    results["polygons"] = closed_polygons

    # Extract dimension annotations from text layer
    dim_pattern = re.compile(r'\d+[\.,]\d+\s*(?:m|mm|M|MM)?|\d{3,5}\s*(?:mm|MM)')
    dimensions_found = dim_pattern.findall(full_text)
    results["dimensions"] = list(set(dimensions_found))[:20]  # Top 20 unique values

    # Build summary
    if closed_polygons:
        total_area = sum(p["area_m2"] for p in closed_polygons)
        largest = closed_polygons[0]
        results["areas_m2"] = [p["area_m2"] for p in closed_polygons]
        results["summary"] = (
            f"Sheet: {sheet_pdf.stem} | Scale: {results['scale']}\n"
            f"Polygons detected: {len(closed_polygons)}\n"
            f"Largest element: {largest['width_m']}m x {largest['height_m']}m = {largest['area_m2']} m²\n"
            f"Total polygon area: {round(total_area, 2)} m²\n"
            f"(Note: overlapping elements may cause double-counting — review largest polygons first)"
        )
    else:
        results["summary"] = (
            f"Sheet: {sheet_pdf.stem} | Scale: {results['scale']}\n"
            "No significant closed polygons detected in vector layer.\n"
            "This may be a scanned drawing — use image analysis and dimension annotations instead."
        )

    doc.close()
    return results


def print_report(results: dict):
    """Print a structured takeoff report."""
    print("\n" + "="*60)
    print(f"POLYGON EXTRACTION REPORT")
    print("="*60)
    print(results.get("summary", "No summary available"))

    polygons = results.get("polygons", [])
    if polygons:
        print(f"\nTop {min(10, len(polygons))} polygons by area:")
        print(f"{'#':<4} {'Width (m)':<12} {'Height (m)':<12} {'Area (m²)':<12}")
        print("-" * 44)
        for i, p in enumerate(polygons[:10], 1):
            print(f"{i:<4} {p['width_m']:<12} {p['height_m']:<12} {p['area_m2']:<12}")

    dims = results.get("dimensions", [])
    if dims:
        print(f"\nDimension annotations found in text layer:")
        print(", ".join(dims))

    print("\nRecommendation: Cross-check the largest polygon area against annotated dimensions.")
    print("="*60 + "\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract polygon data from construction drawing sheets")
    parser.add_argument("--sheet", help="Sheet name e.g. SHEET-001")
    parser.add_argument("--sheets-dir", default="sheets", help="Directory containing split sheets")
    parser.add_argument("--all", action="store_true", help="Process all sheets")
    args = parser.parse_args()

    sheets_dir = Path(args.sheets_dir)

    if args.all:
        pdfs = sorted(sheets_dir.glob("SHEET-*.pdf"))
        print(f"Processing {len(pdfs)} sheets...")
        for pdf in pdfs:
            results = extract_polygons_from_sheet(pdf)
            print_report(results)
    elif args.sheet:
        pdf = sheets_dir / f"{args.sheet}.pdf"
        results = extract_polygons_from_sheet(pdf)
        print_report(results)
    else:
        parser.print_help()
