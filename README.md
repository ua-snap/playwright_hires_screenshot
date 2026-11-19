# Screenshot to SVG

A Python utility for exporting webpages as high-resolution PNGs and hybrid vector SVGs, primarily for use in large-format scientific posters and technical publications.

The script uses Playwright and Chromium to render a webpage and export it as a PDF, then uses PyMuPDF to convert the PDF to SVG. The default target is the [Arctic-EDS AZCOT deployment](http://azcot.arcticeds.org/).

## Setup

Requires Python and [uv](https://docs.astral.sh/uv/).

```bash
uv sync
uv run playwright install chromium
```

## Usage

```bash
uv run capture_svg.py
```

The script writes three files to `screenshots/`:

| File | Description |
| --- | --- |
| `azcot.png` | High-resolution raster screenshot (4800 × 3000 px by default). |
| `azcot.pdf` | Chromium PDF export containing vector and raster content. |
| `azcot.svg` | SVG converted from the PDF, with text rendered as vector paths. |

## Configuration

Modify the constants at the top of `capture_svg.py`:

| Constant | Default | Description |
| --- | --- | --- |
| `URL` | `http://azcot.arcticeds.org/` | Target webpage. |
| `WIDTH` | `1600` | Browser viewport width in CSS pixels. |
| `HEIGHT` | `1000` | Browser viewport height in CSS pixels. |
| `SCALE` | `3` | Device pixel ratio for the PNG screenshot. |
| `OUTPUT` | `screenshots/` | Output directory. |

The script waits an additional five seconds after page load for asynchronous content to render. Adjust this delay as necessary, or replace it with an application-specific readiness check. Output filenames are currently hard-coded in the script.

## Limitations

- The SVG is derived from Chromium's PDF export, not from the PNG screenshot. PDF rendering may differ from the on-screen layout.
- Raster imagery, canvas-based charts, WebGL maps, and raster map tiles do not become vector graphics through conversion.
- Only the first page of the PDF is exported. Increase the document height if additional content is needed.
- Text is converted to vector outlines to avoid font substitution. Set `text_as_path=False` in `get_svg_image()` to retain text where possible.
- `SCALE` increases PNG resolution but does not improve the resolution of embedded raster content in the SVG or PDF.

## Dependencies

- [Playwright](https://playwright.dev/python/) — browser automation and webpage capture.
- [PyMuPDF](https://pymupdf.readthedocs.io/) — PDF-to-SVG conversion.
