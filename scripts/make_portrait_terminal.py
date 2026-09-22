from pathlib import Path
from xml.etree import ElementTree as ET

SOURCE = Path("assets/portrait/portrait.svg")
OUTPUT = Path("assets/portrait/terminal-portrait.svg")

BACKGROUND = "#0D1117"
MUTED = "#8B949E"
ACCENT = "#58A6FF"
BORDER = "#30363D"

HEADER_HEIGHT = 38
PROMPT_HEIGHT = 30
PORTRAIT_GAP = 10

PADDING_X = 18
PADDING_BOTTOM = 18

# Read the already-working portrait SVG.
tree = ET.parse(SOURCE)
root = tree.getroot()

viewbox = root.get("viewBox")

if not viewbox:
    raise SystemExit("portrait.svg does not contain a viewBox.")

_, _, portrait_width, portrait_height = map(float, viewbox.split())

portrait_x = PADDING_X
portrait_y = HEADER_HEIGHT + PROMPT_HEIGHT + PORTRAIT_GAP

width = portrait_width + (PADDING_X * 2)
height = portrait_y + portrait_height + PADDING_BOTTOM

svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg
    xmlns="http://www.w3.org/2000/svg"
    width="{width:.0f}"
    height="{height:.0f}"
    viewBox="0 0 {width:.0f} {height:.0f}"
>

    <!-- Terminal background -->
    <rect
        width="100%"
        height="100%"
        rx="10"
        fill="{BACKGROUND}"
    />

    <!-- Terminal border -->
    <rect
        x="0.5"
        y="0.5"
        width="{width - 1:.0f}"
        height="{height - 1:.0f}"
        rx="10"
        fill="none"
        stroke="{BORDER}"
    />

    <!-- Header divider -->
    <line
        x1="0"
        y1="{HEADER_HEIGHT}"
        x2="{width:.0f}"
        y2="{HEADER_HEIGHT}"
        stroke="{BORDER}"
    />

    <!-- Window controls -->
    <circle cx="16" cy="18" r="5" fill="#484F58"/>
    <circle cx="34" cy="18" r="5" fill="#484F58"/>
    <circle cx="52" cy="18" r="5" fill="#484F58"/>

    <!-- Terminal title -->
    <text
        x="{width / 2:.0f}"
        y="22"
        text-anchor="middle"
        font-family="monospace"
        font-size="11"
        fill="{MUTED}"
    >navneet@github ~</text>

    <!-- Command -->
    <text
        x="{PADDING_X}"
        y="{HEADER_HEIGHT + 19}"
        font-family="monospace"
        font-size="11"
        fill="#F0F6FC"
    >
        <tspan fill="{ACCENT}">$</tspan>
        <tspan> whoami</tspan>
    </text>

    <!-- Proven-good portrait -->
    <svg
        x="{portrait_x}"
        y="{portrait_y}"
        width="{portrait_width:.0f}"
        height="{portrait_height:.0f}"
        viewBox="0 0 {portrait_width:.0f} {portrait_height:.0f}"
        preserveAspectRatio="none"
    >
'''

# Extract the working portrait's children and place them inside
# the nested SVG. This preserves its exact existing rendering.
for child in root:
    tag = child.tag

    # Don't duplicate the outer SVG's XML namespace declarations.
    svg += ET.tostring(child, encoding="unicode")

svg += '''
    </svg>
</svg>
'''

OUTPUT.write_text(svg, encoding="utf-8")

print(f"Created: {OUTPUT}")
print(f"Portrait: {portrait_width:.0f} × {portrait_height:.0f}")
print(f"Terminal: {width:.0f} × {height:.0f}")
