# Contributing to Drawing Analyzer

Thanks for wanting to contribute. This is an open project built for construction professionals. Useful contributions are practical ones — things that make the skill work better on real drawing sets.

## Most useful contributions right now

- **Better classification prompts** for specific drawing types that are currently misclassified
- **Electrical single line diagram handling** — these have a unique structure that needs specific extraction rules
- **Fire services drawing support** — symbol libraries vary significantly by authority and designer
- **OCR integration for scanned drawings** — currently the skill flags scanned sheets as low confidence. Adding Tesseract or similar would improve this significantly
- **DWG file support** — directly reading AutoCAD DWG files rather than requiring PDF export
- **Improved polygon extraction** — better handling of overlapping geometry in dense structural drawings

## How to contribute

1. Fork the repository
2. Create a branch: `git checkout -b your-feature-name`
3. Make your changes
4. Test on at least one real construction drawing set
5. Submit a pull request with a clear description of what changed and why

## Testing

Before submitting a PR, test your changes on a real drawing set. Include in your PR description:

- What type of drawing set you tested on (residential, commercial, industrial)
- What the result was before your change
- What the result is after your change
- Any edge cases you found

## Reporting issues

Open an issue and include:

- What drawing type caused the problem
- What Claude returned (wrong answer)
- What the correct answer was
- Whether the drawing was CAD-exported or scanned

## Code style

Plain Python. No unnecessary dependencies beyond `pypdf` and `PyMuPDF`. Scripts should run with `python scripts/script_name.py` with no additional configuration.
