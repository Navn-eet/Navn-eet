#!/usr/bin/env python3

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageEnhance
import base64
import io

SOURCE = Path("assets/portrait/source-prepped.png")
PNG_OUTPUT = Path("assets/portrait/navneet-ascii.png")
SVG_OUTPUT = Path("assets/portrait/navneet-ascii.svg")

# Higher resolution = much better facial detail.
COLS = 140
ROWS = 70

FONT_SIZE = 9
CHAR_W = 5.4
LINE_H = 9

BG = "#0B1118"
FG = "#D7E0EA"

# Much denser ramp preserves facial gradients.
RAMP = " .'`^\",:;Il!i~+_-?][}{1)(|\\/"
RAMP += "tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$"


FONT_PATHS = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
]


def get_font():
    for path in FONT_PATHS:
        if Path(path).exists():
            return ImageFont.truetype(path, FONT_SIZE)

    return ImageFont.load_default()


def to_char(value):
    index = round(
        (255 - value)
        / 255
        * (len(RAMP) - 1)
    )

    return RAMP[
        max(
            0,
            min(
                len(RAMP) - 1,
                index,
            ),
        )
    ]


def main():
    if not SOURCE.exists():
        raise SystemExit(
            f"Missing {SOURCE}. Run prep_photo.py first."
        )

    image = Image.open(SOURCE).convert("L")

    # Slightly increase local contrast.
    image = ImageEnhance.Contrast(image).enhance(1.35)

    # Preserve the original aspect ratio while accounting
    # for terminal characters being taller than wide.
    char_ratio = CHAR_W / LINE_H

    target_ratio = (COLS * char_ratio) / ROWS
    source_ratio = image.width / image.height

    if source_ratio > target_ratio:
        new_width = COLS
        new_height = round(
            COLS
            / source_ratio
            / char_ratio
        )
    else:
        new_height = ROWS
        new_width = round(
            ROWS
            * source_ratio
            * char_ratio
        )

    new_width = max(1, min(COLS, new_width))
    new_height = max(1, min(ROWS, new_height))

    image = image.resize(
        (new_width, new_height),
        Image.Resampling.LANCZOS,
    )

    # Dark background.
    canvas = Image.new(
        "L",
        (COLS, ROWS),
        255,
    )

    offset_x = (COLS - new_width) // 2
    offset_y = (ROWS - new_height) // 2

    canvas.paste(
        image,
        (offset_x, offset_y),
    )

    # Build ASCII.
    lines = []

    for y in range(ROWS):
        chars = []

        for x in range(COLS):
            chars.append(
                to_char(
                    canvas.getpixel((x, y))
                )
            )

        lines.append(
            "".join(chars).rstrip()
        )

    width = round(COLS * CHAR_W) + 20
    height = ROWS * LINE_H + 20

    output = Image.new(
        "RGB",
        (width, height),
        BG,
    )

    draw = ImageDraw.Draw(output)
    font = get_font()

    for row, line in enumerate(lines):
        draw.text(
            (
                10,
                5 + row * LINE_H,
            ),
            line,
            font=font,
            fill=FG,
        )

    output.save(
        PNG_OUTPUT,
        "PNG",
        optimize=True,
    )

    # Embed PNG in SVG.
    buffer = io.BytesIO()

    output.save(
        buffer,
        format="PNG",
        optimize=True,
    )

    encoded = base64.b64encode(
        buffer.getvalue()
    ).decode("ascii")

    svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg
    xmlns="http://www.w3.org/2000/svg"
    width="{width}"
    height="{height}"
    viewBox="0 0 {width} {height}"
    role="img"
    aria-label="ASCII portrait of Navneet Verma">

    <rect
        width="{width}"
        height="{height}"
        rx="14"
        fill="{BG}"/>

    <image
        href="data:image/png;base64,{encoded}"
        width="{width}"
        height="{height}">

        <animate
            attributeName="opacity"
            from="0"
            to="1"
            dur="1.5s"
            fill="freeze"/>
    </image>

</svg>
'''

    SVG_OUTPUT.write_text(
        svg,
        encoding="utf-8",
    )

    print(f"Created: {PNG_OUTPUT}")
    print(f"Created: {SVG_OUTPUT}")


if __name__ == "__main__":
    main()
