# Drawing Analyzer — Claude AI Skill for Construction Drawings

Pre-process a set of construction drawing PDFs into structured text indexes so Claude can answer questions **faster, cheaper, and more accurately**.

Built by [Hamza Abdul Jabbar](https://hamzajabbar.online) | AutoConst

---

## The Problem

Raw construction drawing PDFs are terrible AI input.

- Claude breaks images into 16×16 pixel tiles — tiny drawing details get lost
- A semi-dashed line (cold water) looks identical to a double-dashed line (hot water) at tile resolution
- Merged drawing sets regularly fail to upload even under the 30MB limit
- Claude Cowork burns **60,000–70,000 tokens per question** processing the full PDF set every time
- Element counts are approximate — overcounting is common
- Cross-references between sheets are not followed

## The Solution

Run this skill **once** on a new drawing set. It builds lightweight text indexes. Every future question reads the indexes first, then targets only the specific sheet needed.

| | Raw PDF approach | Drawing Analyzer |
|---|---|---|
| Tokens per question | 60,000–70,000 | 5,000–8,000 |
| Time per question | 5–10 minutes | 30–60 seconds |
| Footing count accuracy | Overcounts | Correct, by type |
| Area takeoff accuracy | Visual estimate | 96% tested |
| Symbol interpretation | Guesses | Reads actual legend |
| Cross-references | Not followed | Mapped and followed |

### Real result

Warehouse slab area on an 11MB drawing set:
- **Drawing Analyzer:** 13,250 m²
- **Manual Bluebeam measurement:** 13,600 m²
- **Accuracy: 96.7%**

---

## What it produces

```
your-project/
├── indexes/
│   ├── drawings.md              # Master register — loaded on every query (~5KB)
│   ├── sheet-classification.md  # Every sheet classified by type and content
│   ├── cross-reference.md       # Which drawings reference which other drawings
│   └── symbol-library.md        # Every symbol, line type, abbreviation from all legends
└── sheets/
    ├── SHEET-001.pdf            # Individual sheet PDF
    ├── SHEET-001.txt            # Extracted text/vector layer
    ├── SHEET-001.png            # Rendered image at optimal resolution
    ├── SHEET-002.pdf
    └── ...
```

---

## Requirements

- [Claude desktop app](https://claude.ai/download)
- Claude Pro subscription ($20/month) — required for Claude Code
- Python 3.8+ (for the processing scripts)
- Your construction drawing PDF set

### Python dependencies

```bash
pip install pypdf PyMuPDF
```

---

## Installation

### Option A — Install as a Claude skill (recommended)

1. Download `drawing-analyzer.skill` from the [Releases](../../releases) page
2. Open the Claude desktop app
3. Go to **Settings → Skills → Install Skill**
4. Select the `.skill` file
5. Open a new Claude Code session and type:

```
run drawing analyzer on my construction drawings
```

### Option B — Clone and use directly

```bash
git clone https://github.com/YOUR-USERNAME/drawing-analyzer.git
cd drawing-analyzer
pip install pypdf PyMuPDF
```

Then in Claude Code, point it at this folder and say:

```
run drawing analyzer on my construction drawings
```

---

## Usage

### Step 1 — Run the analyzer (once per drawing set)

Open Claude Code in the folder containing your merged drawing PDF.

```
run drawing analyzer on my construction drawings
```

Claude will:
1. Split the PDF into individual sheets
2. Extract text layer from each sheet
3. Classify every sheet by type
4. Build the cross-reference matrix
5. Extract symbol library from all legends
6. Create the master drawings register

This takes **5–15 minutes** for a typical set (10–30 sheets). Larger sets (50+ sheets) allow 30–60 minutes.

### Step 2 — Ask questions

```
What is the area of the warehouse slab?
How many F6 footings are shown on the foundation drawings?
What does a double-dashed line mean on the hydraulic drawings?
What details does the F3 footing cross-reference?
How many roller doors are shown on the floor plan?
What is the floor-to-floor height on the section drawings?
```

Claude reads the indexes first, identifies the relevant sheet, then reads that sheet's text and image. It only opens the raw PDF if polygon extraction is needed for an area takeoff.

### Step 3 — Area takeoffs (optional)

For precise area calculations, Claude runs the polygon extractor on the specific sheet:

```
What is the ground floor slab area? Run polygon extraction to confirm.
```

This extracts closed polygon geometry from the vector layer, applies the drawing scale, and returns area in m². Always cross-checked against dimension annotations.

---

## Project structure

```
drawing-analyzer/
├── README.md                        # This file
├── SKILL.md                         # Claude skill definition
├── scripts/
│   ├── split_drawings.py            # Split merged PDF into individual sheets
│   └── extract_polygons.py          # Polygon extraction for area takeoffs
├── references/
│   ├── drawing-types.md             # Classification guide for 15 drawing types
│   └── takeoff-guide.md             # How to run accurate quantity takeoffs
├── indexes/                         # Created by the analyzer (gitignored)
│   └── .gitkeep
└── sheets/                          # Created by the analyzer (gitignored)
    └── .gitkeep
```

---

## How it works

### Why scripts for splitting, AI for classifying

The skill uses Python scripts for mechanical tasks that do not require intelligence: splitting the PDF, extracting text, rendering images. These are fast and cheap.

It uses Claude for tasks that require actual understanding: classifying what is on each sheet, extracting symbol meanings, mapping cross-references. Pattern-matching scripts fail too often on real construction drawing sets because formatting varies too much between designers and firms.

### The query protocol

When you ask a question after the analyzer has run, Claude follows this order:

1. Read `indexes/drawings.md` — understand the drawing set structure
2. Read `indexes/sheet-classification.md` — identify the relevant sheet(s)
3. Read `indexes/cross-reference.md` — check if other sheets need to be followed
4. Read `indexes/symbol-library.md` — confirm symbol meanings before interpreting
5. Read the target sheet `.txt` — get vector/text data
6. View the target sheet `.png` — visual confirmation
7. Run polygon extraction on the target `.pdf` only if area takeoff is needed

This replaces processing 60,000–70,000 tokens of raw PDF with 5,000–8,000 tokens of targeted reading.

---

## Accuracy and limitations

### What the skill improves

- **Symbol interpretation** — reads actual legend, not general knowledge guesses
- **Element counting** — reads from schedule text files where available
- **Cross-references** — mapped before any query runs
- **Token cost** — ~90% reduction
- **File size issues** — individual sheets are 100–400KB, no upload failures
- **Area takeoffs** — 96% tested accuracy via polygon extraction

### Known limitations

- **Scanned drawings** — no text layer to extract. All quantities are low confidence. Recommend getting CAD/BIM files for cost-critical takeoffs.
- **Dense overlapping geometry** — polygon extraction can double-count. Always run the dimension annotation sanity check alongside.
- **Engineering verification** — this skill produces quantities for estimating. It does not verify structural adequacy or code compliance. All quantities going into contracts need a qualified reviewer.
- **BIM is always better** — if you can get the Revit or ArchiCAD model, use the Autodesk MCP connector instead. This skill exists because most construction firms never receive the BIM model on bid projects.

---

## Contributing

Issues and pull requests welcome. Particularly useful contributions:

- Improved classification prompts for specific drawing types (electrical single line diagrams, fire services)
- Better polygon extraction for scanned drawings (OCR integration)
- Support for DWG files directly (not just PDF exports)
- Additional drawing type reference guides

---

## License

MIT License — free to use, modify, and distribute.

---

## Author

**Hamza Jabbar**  
Construction AI at [hamzajabbar.online](https://hamzajabbar.online)  
Building AI automations for construction firms

If this helped you, share it with someone in construction who is still manually reading drawing sets.
