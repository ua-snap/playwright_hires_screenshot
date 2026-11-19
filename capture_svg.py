from pathlib import Path

import pymupdf
from playwright.sync_api import sync_playwright

URL = "http://azcot.arcticeds.org/"
WIDTH = 1600
HEIGHT = 1000
SCALE = 3
OUTPUT = Path("screenshots")

OUTPUT.mkdir(exist_ok=True)

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)

    page = browser.new_page(
        viewport={"width": WIDTH, "height": HEIGHT},
        device_scale_factor=SCALE,
    )

    page.goto(URL, wait_until="load", timeout=60_000)
    page.evaluate("document.fonts.ready")

    # Allow asynchronous maps and charts to render.
    page.wait_for_timeout(5000)

    # Save a high-resolution raster screenshot for comparison.
    page.screenshot(
        path=OUTPUT / "azcot.png",
        animations="disabled",
    )

    # Preserve screen styling rather than print styling.
    page.emulate_media(media="screen")

    page.add_style_tag(
        content="""
        * {
            -webkit-print-color-adjust: exact !important;
            print-color-adjust: exact !important;
        }

        @page {
            margin: 0;
        }
        """
    )

    # Export the first viewport-sized PDF page.
    page.pdf(
        path=OUTPUT / "azcot.pdf",
        width=f"{WIDTH}px",
        height=f"{HEIGHT}px",
        print_background=True,
        page_ranges="1",
        margin={
            "top": "0",
            "bottom": "0",
            "left": "0",
            "right": "0",
        },
    )

    browser.close()

# Convert PDF to SVG, preserving vector geometry.
with pymupdf.open(OUTPUT / "azcot.pdf") as doc:
    svg = doc[0].get_svg_image(text_as_path=True)

    (OUTPUT / "azcot.svg").write_text(
        svg, encoding="utf-8"
    )

print(f"Exports saved to {OUTPUT.resolve()}")
