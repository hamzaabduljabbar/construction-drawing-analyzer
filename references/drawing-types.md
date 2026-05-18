# Drawing Types Reference Guide

This file tells Claude how to classify each construction drawing sheet and what specific information to extract from each type. Read this when classifying sheets in Phase 2 of the Drawing Analyzer.

---

## Cover Sheet / Drawing Index

**Identify by:** Title block says "Drawing List", "Index", or "Cover Sheet". Lists all other drawings.

**Extract:**
- Full drawing list with sheet numbers and titles
- Project name, address, date
- Revision history
- Consultant list (architect, structural, civil, hydraulic, electrical, mechanical)

---

## General Notes / Specification Sheet

**Identify by:** Predominantly text. Contains numbered notes, material specifications, or legend/key.

**Extract:**
- ALL legend items and what each symbol/line type represents (critical for symbol library)
- Material specifications mentioned (concrete grade, steel grade, timber species)
- Referenced standards (AS, NZS, EN, ASTM)
- General notes that apply across multiple drawings

---

## Site Plan

**Identify by:** Shows entire site boundary, building footprint from above, north arrow, site features.

**Extract:**
- Site area if stated
- Building setbacks
- Site access points
- Contour levels or RL references
- Services shown on site (water, sewer, power)

---

## Floor Plan / Layout

**Identify by:** Horizontal cut through building showing room layout, walls, doors, windows from above.

**Extract:**
- Overall building dimensions if annotated
- Room names and areas if shown
- Door and window references (links to schedules)
- Grid lines and their spacing
- Section cut markers and which sheets they reference
- North arrow and scale

---

## Foundation Plan

**Identify by:** Shows footing layout, pad footings, strip footings, piles from above.

**Extract:**
- All footing types shown and their reference codes (F1, F2, PAD-A, etc.)
- Footing locations relative to grid
- Which sheet contains the footing schedule
- Any footing quantities if annotated
- Slab edge details referenced

---

## Structural Layout

**Identify by:** Shows beams, columns, slabs, structural grid. Often separate from architectural floor plan.

**Extract:**
- Column grid with spacing
- Beam references and sizes
- Slab thicknesses if noted
- Connection details referenced
- Steel member designations (UB, UC, RHS, etc.) if visible

---

## Section View

**Identify by:** Vertical cut through building showing internal heights, floor-to-floor, construction layers.

**Extract:**
- Floor-to-floor heights
- Overall building height
- Foundation depth / RL
- Wall and roof construction build-up
- Any material specifications in section notes

---

## Detail Drawing

**Identify by:** Large-scale view of a specific connection, joint, or element. Scale typically 1:10 or 1:5.

**Extract:**
- What element is being detailed (connection, joint, edge, penetration)
- Which plan/section this detail relates to
- Materials and fastener specifications
- Referenced standards or specs

---

## Elevation

**Identify by:** External face of building viewed straight on. Shows facade, windows, doors, levels.

**Extract:**
- Overall building height and width
- Level / RL annotations
- Window and door references
- Facade material notes
- Which face (north, south, east, west)

---

## Roof Plan

**Identify by:** View from above showing roof form, drainage, penetrations, plant locations.

**Extract:**
- Roof area if annotated or scaleable
- Drainage outlets / downpipe locations
- Roof fall directions
- Plant and equipment locations
- Any roof edge or parapet details referenced

---

## Hydraulic / Plumbing Drawing

**Identify by:** Shows pipes, fixtures, drains. Line types vary by service (cold water, hot water, sewer, stormwater).

**Extract:**
- ALL line type definitions from legend (critical — lines look almost identical)
- Fixture schedule reference
- Invert levels if shown
- Pipe sizes annotated
- Drainage type codes (TD7, etc.) and what they reference

---

## Mechanical / HVAC Drawing

**Identify by:** Shows ductwork, equipment, grilles, diffusers.

**Extract:**
- Equipment schedule references
- Duct sizes if annotated
- Equipment locations
- Control and zone references

---

## Electrical Drawing

**Identify by:** Shows power outlets, lighting, switchboards, cable routes.

**Extract:**
- Circuit references and what they serve
- Switchboard locations
- Any load schedule references
- Symbol legend (critical — many symbols look similar)

---

## Single Line Diagram (Electrical)

**Identify by:** Schematic (not scaled) showing electrical hierarchy from mains to sub-boards.

**Extract:**
- Mains supply voltage and capacity
- Sub-board references
- Protection device specifications
- Any load values shown

---

## Fire Services Drawing

**Identify by:** Shows sprinkler heads, hydrants, hose reels, detection devices, panel locations.

**Extract:**
- System type (wet pipe, dry pipe, gaseous suppression)
- Head types and spacing
- Hydrant and hose reel locations
- Panel location and reference

---

## Schedule (Door / Window / Finish / Footing / Equipment)

**Identify by:** Table format. Lists items by reference code with dimensions and specifications.

**Extract:**
- EVERY row of the schedule (this is structured data — extract it completely)
- Column headings
- Any notes below the schedule

For footing schedules specifically: extract all footing types, dimensions, reinforcement, and bearing capacity.

---

## Notes for classification

- One sheet may contain multiple drawing types (e.g. a foundation plan with a footing schedule)
- Classify by the PRIMARY content but note secondary content
- If uncertain between two types, read the title block — it usually states the drawing type
- Scanned drawings (no text layer) must be classified by image only — note this in the index
