from __future__ import annotations

import json
from datetime import date, datetime
from pathlib import Path
from xml.sax.saxutils import escape

INPUT = Path("data/contributions.json")
OUTPUT = Path("assets/activity/contributions.svg")

TODAY = datetime.now().date()

BG = "#0D1117"
BORDER = "#30363D"
TEXT = "#F0F6FC"
MUTED = "#8B949E"

LEVEL_COLORS = {
    0: "#161B22",
    1: "#0E4429",
    2: "#006D32",
    3: "#26A641",
    4: "#39D353",
}

CELL = 10
GAP = 3
STEP = CELL + GAP

LEFT = 52
TOP = 76
RIGHT = 24
BOTTOM = 72

YEAR_GAP = 28
HEADER_HEIGHT = 38

FONT = "JetBrains Mono, monospace"


def load_data() -> dict:
    with INPUT.open(encoding="utf-8") as f:
        data = json.load(f)

    days = [
        day
        for day in data["days"]
        if date.fromisoformat(day["date"]) <= TODAY
    ]

    data["days"] = days
    data["total"] = sum(day["count"] for day in days)

    return data


def group_by_year(days: list[dict]) -> dict[int, list[dict]]:
    years: dict[int, list[dict]] = {}

    for day in days:
        year = int(day["date"][:4])
        years.setdefault(year, []).append(day)

    return years


def build_grid(days: list[dict]) -> tuple[list[tuple], int]:
    if not days:
        return [], 0

    first = date.fromisoformat(days[0]["date"])

    # Sunday = 0 ... Saturday = 6
    row = (first.weekday() + 1) % 7
    column = 0

    cells = []

    previous = first

    for index, day in enumerate(days):
        current = date.fromisoformat(day["date"])

        if index > 0:
            delta = (current - previous).days

            for _ in range(delta):
                row += 1

                if row > 6:
                    row = 0
                    column += 1

        cells.append((column, row, day))

        previous = current

    columns = max(cell[0] for cell in cells) + 1

    return cells, columns


def render() -> None:
    data = load_data()
    years = group_by_year(data["days"])

    sorted_years = sorted(years)

    if not sorted_years:
        raise SystemExit("No contribution data found.")

    grids = {}

    for year in sorted_years:
        grids[year] = build_grid(years[year])

    graph_width = sum(
        grids[year][1] * STEP
        for year in sorted_years
    ) + (len(sorted_years) - 1) * YEAR_GAP

    width = LEFT + graph_width + RIGHT
    height = TOP + (7 * STEP) + BOTTOM

    svg = []

    svg.append(
        f'<svg xmlns="http://www.w3.org/2000/svg" '
        f'width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}">'
    )

    svg.append(
        f'<rect width="{width}" height="{height}" '
        f'rx="12" fill="{BG}"/>'
    )

    svg.append(
        f'<rect x="0.5" y="0.5" width="{width - 1}" '
        f'height="{height - 1}" rx="12" '
        f'fill="none" stroke="{BORDER}"/>'
    )

    # Terminal header.
    svg.append(
        f'<line x1="0" y1="{HEADER_HEIGHT}" '
        f'x2="{width}" y2="{HEADER_HEIGHT}" '
        f'stroke="{BORDER}"/>'
    )

    svg.append(
        '<circle cx="18" cy="19" r="5" fill="#FF5F56"/>'
    )
    svg.append(
        '<circle cx="36" cy="19" r="5" fill="#FFBD2E"/>'
    )
    svg.append(
        '<circle cx="54" cy="19" r="5" fill="#27C93F"/>'
    )

    svg.append(
        f'<text x="72" y="24" fill="{MUTED}" '
        f'font-family="{FONT}" font-size="12">'
        f'navneet@github ~ $ ./contributions.sh'
        f'</text>'
    )

    # Title.
    svg.append(
        f'<text x="{LEFT}" y="59" fill="{TEXT}" '
        f'font-family="{FONT}" font-size="12" '
        f'font-weight="700">'
        f'CONTRIBUTION HISTORY'
        f'</text>'
    )

    graph_x = LEFT

    for year in sorted_years:
        cells, columns = grids[year]

        # Year label.
        svg.append(
            f'<text x="{graph_x}" y="{TOP - 18}" '
            f'fill="{TEXT}" font-family="{FONT}" '
            f'font-size="11" font-weight="700">'
            f'{year}'
            f'</text>'
        )

        # Actual contribution cells.
        for column, row, day in cells:
            x = graph_x + column * STEP
            y = TOP + row * STEP

            level = int(day["level"])
            count = int(day["count"])

            fill = LEVEL_COLORS.get(level, LEVEL_COLORS[0])

            title = (
                f'{day["date"]}: '
                f'{count} contribution'
                f'{"s" if count != 1 else ""}'
            )

            svg.append(
                f'<rect x="{x}" y="{y}" '
                f'width="{CELL}" height="{CELL}" '
                f'rx="2" fill="{fill}">'
                f'<title>{escape(title)}</title>'
                f'</rect>'
            )

        graph_x += columns * STEP + YEAR_GAP

    # Footer.
    footer_y = height - 42

    svg.append(
        f'<text x="{LEFT}" y="{footer_y}" '
        f'fill="{TEXT}" font-family="{FONT}" '
        f'font-size="12" font-weight="700">'
        f'{data["total"]:,}'
        f'</text>'
    )

    svg.append(
        f'<text x="{LEFT + 48}" y="{footer_y}" '
        f'fill="{MUTED}" font-family="{FONT}" '
        f'font-size="11">'
        f'contributions · {data["from"]} → {TODAY.isoformat()}'
        f'</text>'
    )

    # Legend.
    legend_x = width - 164
    legend_y = footer_y - 4

    svg.append(
        f'<text x="{legend_x - 48}" y="{legend_y + 9}" '
        f'fill="{MUTED}" font-family="{FONT}" font-size="10">'
        f'less'
        f'</text>'
    )

    for level in range(5):
        x = legend_x + level * 15

        svg.append(
            f'<rect x="{x}" y="{legend_y}" '
            f'width="10" height="10" rx="2" '
            f'fill="{LEVEL_COLORS[level]}"/>'
        )

    svg.append(
        f'<text x="{legend_x + 82}" y="{legend_y + 9}" '
        f'fill="{MUTED}" font-family="{FONT}" font-size="10">'
        f'more'
        f'</text>'
    )

    svg.append("</svg>")

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text("\n".join(svg), encoding="utf-8")

    print(f"Generated: {OUTPUT}")
    print(f"Years:    {sorted_years[0]} → {sorted_years[-1]}")
    print(f"Total:    {data['total']:,}")
    print(f"Size:     {width} × {height}")


if __name__ == "__main__":
    render()
