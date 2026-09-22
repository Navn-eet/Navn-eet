from pathlib import Path
import re

portrait = Path("assets/portrait/portrait.svg").read_text()
neofetch = Path("assets/cards/neofetch.svg").read_text()

def inner(svg):
    svg = re.sub(r'<\?xml[^>]*\?>', '', svg)
    svg = re.sub(r'<!DOCTYPE[^>]*>', '', svg)
    match = re.search(r'<svg[^>]*>(.*)</svg>', svg, re.S)
    return match.group(1) if match else svg

def make_static(svg):
    # Reveal groups that are hidden only because of the original
    # line-by-line SMIL animation.
    svg = re.sub(
        r'<g\s+opacity="0"\s*>',
        '<g opacity="1">',
        svg
    )

    # Remove the animation elements from the embedded copy.
    svg = re.sub(
        r'<animate\b[^>]*/>',
        '',
        svg,
        flags=re.S
    )

    svg = re.sub(
        r'<animate\b[^>]*>.*?</animate>',
        '',
        svg,
        flags=re.S
    )

    return svg

portrait_inner = inner(portrait)
neofetch_inner = make_static(inner(neofetch))

out = """<svg xmlns="http://www.w3.org/2000/svg"
     width="1000"
     height="650"
     viewBox="0 0 1000 650">

<rect width="1000" height="650" rx="14" fill="#0D1117"/>
<rect x="1" y="1" width="998" height="648" rx="14"
      fill="none" stroke="#30363D"/>

<circle cx="24" cy="22" r="6" fill="#FF5F56"/>
<circle cx="44" cy="22" r="6" fill="#FFBD2E"/>
<circle cx="64" cy="22" r="6" fill="#27C93F"/>

<text x="90" y="27"
      font-family="monospace"
      font-size="14"
      fill="#8B949E">navneet@github ~ $ whoami</text>

<line x1="20" y1="48" x2="980" y2="48"
      stroke="#30363D"/>

<g transform="translate(25 65) scale(0.78)">
""" + portrait_inner + """
</g>

<g transform="translate(500 75) scale(0.86)">
""" + neofetch_inner + """
</g>

</svg>
"""

Path("assets/cards/whoami.svg").write_text(out)
print("Generated static assets/cards/whoami.svg")
