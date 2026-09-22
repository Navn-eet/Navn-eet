from pathlib import Path
import re

def parse_svg(path):
    svg = Path(path).read_text()
    svg = re.sub(r'<\?xml[^>]*\?>', '', svg)
    svg = re.sub(r'<!DOCTYPE[^>]*>', '', svg)

    match = re.search(r'<svg\b([^>]*)>(.*)</svg>\s*$', svg, re.S)
    if not match:
        raise ValueError(f"Invalid SVG: {path}")

    attrs = match.group(1)
    content = match.group(2)

    def attr(name, default=None):
        m = re.search(rf'\b{name}="([^"]*)"', attrs)
        return m.group(1) if m else default

    return {
        "width": attr("width"),
        "height": attr("height"),
        "viewBox": attr("viewBox"),
        "content": content,
    }


portrait = parse_svg("assets/portrait/portrait.svg")
neofetch = parse_svg("assets/cards/neofetch.svg")

out = f'''<svg xmlns="http://www.w3.org/2000/svg"
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

<!-- ASCII portrait -->
<svg x="25"
     y="65"
     width="450"
     height="433.5"
     viewBox="{portrait["viewBox"]}"
     preserveAspectRatio="xMidYMid meet">

{portrait["content"]}

</svg>

<!-- Neofetch -->
<svg x="500"
     y="65"
     width="450"
     height="433.5"
     viewBox="{neofetch["viewBox"]}"
     preserveAspectRatio="xMidYMid meet">

{neofetch["content"]}

</svg>

</svg>
'''

Path("assets/cards/whoami.svg").write_text(out)
print("Generated assets/cards/whoami.svg")
