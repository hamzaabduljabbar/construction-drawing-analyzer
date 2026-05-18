---
name: drawing-analyzer
description: Pre-process construction drawing PDF sets into structured text indexes so Claude can answer questions faster, cheaper, and more accurately. Use this skill whenever a user mentions construction drawings, PDF drawings, takeoffs, drawing sets, plans, or wants to extract information from construction documents. Trigger on phrases like "analyze my drawings", "run drawing analyzer", "process these drawings", "how many footings", "what is the slab area", or any question about quantities, elements, or scope from a set of construction drawings. This skill runs once on a drawing set and creates lightweight text indexes that replace the need to re-process large PDFs on every query — reducing token usage by ~90% and significantly improving accuracy.
---

# Drawing Analyzer Skill

Pre-processes a set of construction drawing PDFs into structured, lightweight text indexes. Run this once on any new drawing set. After it completes, answer questions by reading the indexes first, then targeting only the specific drawing needed.

## When to run this skill

- User uploads or points to a folder containing construction drawing PDFs
- User asks any question about quantities, elements, areas, or scope from drawings
- User says "run drawing analyzer", "process my drawings", or "analyze these drawings"
- Any takeoff, footing count, slab area, or element count request

---

## Phase 1: Split and extract

**Goal:** Break the merged PDF into individual sheets. Extract text and create an image of each.

Run the PDF splitter script first:

```
scripts/split_drawings.py
```

For each sheet produced:
1. Save as an individual PDF: `sheets/SHEET-001.pdf`, `sheets/SHEET-002.pdf`, etc.
2. Extract all vector/text layer content → save as `sheets/SHEET-001.txt`
3. Render the sheet as an image at maximum resolution → save as `sheets/SHEET-001.png`

**Important:** Do NOT use pattern matching scripts to classify drawings. Use Claude vision to read each sheet image and determine its type. Scripts cannot reliably handle the variation in construction drawing formats.

---

## Phase 2: Build the sheet classification index

Read each sheet image (`.png`) and text file (`.txt`) and classify every sheet.

Output file: `indexes/sheet-classification.md`

For each sheet, record:

```
| Sheet No | File | Drawing Type | Title | Scale | Key Elements | Notes |
```

Drawing types to classify into:
- General Notes / Legend / Cover Sheet
- Site Plan / Survey
- Floor Plan / Layout
- Foundation Plan
- Structural Layout
- Section / Detail
- Elevation
- Roof Plan
- Mechanical / Hydraulic / Plumbing
- Electrical / Single Line Diagram
- Fire Services
- Schedule (door, window, finish, equipment, footing)
- Specification Sheet

For schedules and legends: extract the full symbol or item list into the notes column. This is critical — it allows later queries to understand what symbols mean without re-reading the image.

**Read the drawing type reference guide if uncertain:**
→ `references/drawing-types.md`

---

## Phase 3: Build the cross-reference matrix

Read all sheets. Map which drawings reference which other drawings.

Output file: `indexes/cross-reference.md`

```
| Source Sheet | Element / Note | References | Purpose |
```

Examples:
- Foundation plan says "See S-03 for footing schedule" → log this
- Detail on A-07 refers to section cut shown on A-04 → log this
- Hydraulic drawing uses symbol TD7 → refers to trench drain schedule on H-02 → log this

This index allows Claude to follow cross-references without manually hunting through sheets.

---

## Phase 4: Build the symbol library

For each sheet that contains a legend, symbol key, or abbreviation list:
- Extract every symbol, line type, and abbreviation
- Record: Symbol description, what it represents, which sheet it appears on

Output file: `indexes/symbol-library.md`

```
| Symbol / Line Type | Meaning | Sheet(s) |
```

Examples:
- Dashed line = cold water pipe (H-02)
- Double-dashed line = hot water pipe (H-02)
- F6 = 600x600 pad footing with 4xN20 bars (see S-04 footing schedule)
- TD7 = 300mm wide ACO drain, stainless grate (H-01 legend)

---

## Phase 5: Build the master drawings register

Output file: `indexes/drawings.md`

This file is loaded at the start of every subsequent query. Keep it concise.

Include:
1. **Project overview** — project name, address, drawing package date, number of sheets
2. **Sheet list** — one row per sheet with type, title, file reference
3. **How to query this drawing set** — brief instructions for Claude on how to use the indexes
4. **Key notes** — any general notes or spec requirements that affect multiple trades

Target size: under 10KB. This file is read on every query. Keep it lean.

---

## Phase 6: Confirm completion

Report to the user:
- Number of sheets processed
- Index files created and their sizes
- Any sheets that could not be classified (need manual review)
- Any cross-references that appear broken or unclear
- Estimated token savings vs querying raw PDFs

---

## How to answer questions after the analyzer runs

When a user asks a question about the drawings after this skill has run:

1. **Read `indexes/drawings.md` first** — understand the drawing set structure
2. **Read `indexes/sheet-classification.md`** — identify which sheet(s) contain the answer
3. **Read `indexes/cross-reference.md`** — check if the answer requires following references to other sheets
4. **Read `indexes/symbol-library.md`** — confirm you understand all symbols on relevant sheets
5. **Read the target sheet `.txt` file** — get the vector/text data
6. **View the target sheet `.png` image** — visual confirmation
7. **Only open the raw `.pdf` if the text and image are insufficient**

For quantity takeoffs: run the polygon extraction script on the specific sheet only.

```
scripts/extract_polygons.py --sheet SHEET-XXX
```

Cross-check polygon extraction against dimension annotations for high-value items.

---

## Reference files

- `references/drawing-types.md` — Construction drawing type descriptions and what to extract from each
- `references/takeoff-guide.md` — How to run accurate quantity takeoffs using the processed indexes

---

## Token efficiency notes

- Raw 11MB PDF set: ~70,000 tokens per query
- After processing: `drawings.md` ~500 tokens, target sheet text ~2,000 tokens, image ~4,000 tokens
- Estimated saving: 85 to 90% fewer tokens per query
- Accuracy improvement: cross-referencing, symbol library, and individual sheet processing all address the known AI limitations on spatial reasoning and element identification in construction drawings
