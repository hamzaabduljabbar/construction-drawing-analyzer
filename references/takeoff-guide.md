# Takeoff Guide

How to run accurate quantity takeoffs using the processed drawing indexes. Read this when answering any quantity question after the Drawing Analyzer has run.

---

## General approach

Always use a two-method cross-check for any quantity with significant cost impact.

**Method 1: Polygon extraction (precise)**
Run `scripts/extract_polygons.py --sheet SHEET-XXX` on the specific drawing.
This extracts closed polygon areas from the vector layer.
Result is mathematically precise for CAD-exported drawings.

**Method 2: Dimension annotation (sanity check)**
Read the text layer file (`.txt`) for the sheet.
Find overall building dimensions or room dimensions.
Calculate area from length × width.
This gives an order-of-magnitude check on Method 1.

If both methods agree within 5%: report the average with high confidence.
If they differ by more than 5%: report both results, state the discrepancy, and flag for manual verification.

---

## Counting elements (footings, columns, doors, windows)

**Do not count from images.** Image-based counting is unreliable for construction drawings (confirmed limitation of Claude's spatial reasoning on dense drawings).

**Use this order:**

1. Check if a schedule exists — read the `indexes/sheet-classification.md` to find it
2. If a schedule exists: count rows in the schedule (text file). This is the authoritative count.
3. If no schedule: read the foundation/structural plan text layer for reference codes
4. Cross-check: count unique reference codes in text layer against the schedule
5. Report: "X footings per schedule on Sheet S-04. Types: F1 (N), F2 (N), F6 (N)."

**Always report by type**, not just total count. "141 footings" is less useful than "F1: 22, F2: 18, F3: 14, F6: 8 per footing schedule on S-04."

---

## Slab areas

1. Identify which sheet shows the slab outline — check `indexes/sheet-classification.md`
2. Run polygon extraction on that sheet
3. Read text layer for overall building dimensions
4. If the polygon extraction returns a gross area, subtract any voids, courtyards, or openings visible in the drawing notes or text layer
5. Check `indexes/symbol-library.md` for any hatch patterns that define slab vs non-slab areas
6. Report gross area and net area separately

---

## Linear elements (pipes, cables, beams, walls)

1. Check if a schedule or length annotation exists in the text layer
2. If the element is shown in plan: use dimension annotations from text layer to calculate run length
3. For complex routes: polygon extraction will give perimeter of enclosed areas — use perimeter for linear elements that follow room boundaries
4. Always apply the drawing scale confirmed from the title block or `indexes/sheet-classification.md`

---

## Understanding symbols before counting

Before counting ANY element:
1. Read `indexes/symbol-library.md` to confirm what the symbol for that element looks like
2. Check the cross-reference matrix (`indexes/cross-reference.md`) to see if the element type is defined on another sheet
3. If the symbol is a line type (especially hydraulic/plumbing): never assume — always read the legend first

---

## Confidence reporting

Always state confidence level with quantities:

- **High confidence:** Extracted from a schedule or text layer annotation. No visual interpretation required.
- **Medium confidence:** Calculated from polygon extraction on CAD-exported drawing with confirmed scale.
- **Low confidence:** Estimated from image visual analysis or from a scanned drawing with no text layer.

Example output format:
```
Quantity: 34 F6 footings
Source: Footing schedule, Sheet S-04 (text layer extraction)
Confidence: High
Cross-reference: F6 detail on Sheet S-07
```

---

## When the drawing is scanned (no text layer)

Scanned drawings have no vector data. This is noted in `indexes/sheet-classification.md`.

For scanned drawings:
1. Use the image (`.png`) only
2. Estimate dimensions from scale bar if shown (look for a graphic scale bar on the drawing)
3. Count elements visually from the image
4. Always flag as Low confidence
5. Recommend the client provide CAD or BIM files if quantities are cost-critical
