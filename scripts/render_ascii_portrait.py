from pathlib import Path
from html import escape

SOURCE = Path("assets/portrait/ascii-art.txt")
OUTPUT = Path("assets/portrait/portrait.svg")

FONT_SIZE = 8
CHAR_WIDTH = 4.8
LINE_HEIGHT = 8.5

text = SOURCE.read_text(encoding="utf-8")
lines = text.splitlines()

while lines and not lines[-1]:
    lines.pop()

if not lines:
    raise SystemExit("ASCII source file is empty.")

max_columns = max(len(line) for line in lines)

width = max_columns * CHAR_WIDTH
height = len(lines) * LINE_HEIGHT

svg = [
    '<?xml version="1.0" encoding="UTF-8"?>',
    (
        f'<svg xmlns="http://www.w3.org/2000/svg" '
        f'width="{width:.0f}" height="{height:.0f}" '
        f'viewBox="0 0 {width:.0f} {height:.0f}">'
    ),
    '<rect width="100%" height="100%" fill="#0D1117"/>',
    (
        '<g '
        'font-family="monospace" '
        f'font-size="{FONT_SIZE}px" '
        'font-weight="700" '
        'fill="#F0F6FC" '
        'xml:space="preserve">'
    ),
]

for row, line in enumerate(lines):
    y = (row + 1) * LINE_HEIGHT

    svg.append(
        f'<text x="0" y="{y:.2f}">'
        f'{escape(line)}'
        '</text>'
    )

svg.extend([
    '</g>',
    '</svg>',
])

OUTPUT.write_text("\n".join(svg), encoding="utf-8")

print(f"Created: {OUTPUT}")
print(f"Rows: {len(lines)}")
print(f"Columns: {max_columns}")
print(f"Size: {width:.0f} × {height:.0f}")
