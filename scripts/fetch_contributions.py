from __future__ import annotations

import json
import subprocess
from datetime import date, datetime, timezone
from pathlib import Path

USERNAME = "Navn-eet"
OUTPUT = Path("data/contributions.json")

# GitHub was launched in 2008. We walk from 2008 through the
# current year, then remove years before the first real contribution.
FIRST_YEAR = 2008

QUERY = """
query($login: String!, $from: DateTime!, $to: DateTime!) {
  user(login: $login) {
    contributionsCollection(from: $from, to: $to) {
      contributionCalendar {
        totalContributions
        weeks {
          contributionDays {
            date
            contributionCount
            contributionLevel
          }
        }
      }
    }
  }
}
"""

LEVELS = {
    "NONE": 0,
    "FIRST_QUARTILE": 1,
    "SECOND_QUARTILE": 2,
    "THIRD_QUARTILE": 3,
    "FOURTH_QUARTILE": 4,
}


def run_graphql(start: date, end: date) -> dict:
    from_value = f"{start.isoformat()}T00:00:00Z"
    to_value = f"{end.isoformat()}T00:00:00Z"

    command = [
        "gh",
        "api",
        "graphql",
        "-f",
        f"query={QUERY}",
        "-F",
        f"login={USERNAME}",
        "-F",
        f"from={from_value}",
        "-F",
        f"to={to_value}",
    ]

    result = subprocess.run(
        command,
        capture_output=True,
        text=True,
    )

    if result.returncode != 0:
        error = result.stderr.strip()

        print()
        print("GitHub GraphQL request failed.")
        print(f"Range: {start} → {end}")
        print()
        print(error)

        raise SystemExit(result.returncode)

    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError as exc:
        raise SystemExit(
            "GitHub returned invalid JSON."
        ) from exc


def fetch_year(year: int) -> tuple[list[dict], int]:
    start = date(year, 1, 1)
    end = date(year + 1, 1, 1)

    print(f"Fetching {year}...", end=" ", flush=True)

    payload = run_graphql(start, end)

    if payload.get("errors"):
        messages = [
            error.get("message", str(error))
            for error in payload["errors"]
        ]

        print("FAILED")
        for message in messages:
            print(f"  {message}")

        raise SystemExit(1)

    user = payload.get("data", {}).get("user")

    if user is None:
        print("FAILED")
        raise SystemExit("GitHub returned no user data.")

    calendar = user["contributionsCollection"]["contributionCalendar"]

    days: list[dict] = []

    for week in calendar["weeks"]:
        for contribution_day in week["contributionDays"]:
            day_date = contribution_day["date"]

            # Keep only dates belonging to this exact year.
            if not day_date.startswith(f"{year}-"):
                continue

            days.append(
                {
                    "date": day_date,
                    "level": LEVELS.get(
                        contribution_day["contributionLevel"],
                        0,
                    ),
                    "count": contribution_day["contributionCount"],
                }
            )

    total = sum(day["count"] for day in days)

    print(f"{total} contributions")

    return days, total


def main() -> None:
    today = datetime.now(timezone.utc).date()
    current_year = today.year

    all_days: list[dict] = []
    yearly_totals: dict[str, int] = {}

    print(f"Fetching contribution history for {USERNAME}")
    print(f"Years: {FIRST_YEAR} → {current_year}")
    print()

    for year in range(FIRST_YEAR, current_year + 1):
        days, total = fetch_year(year)

        if total > 0:
            yearly_totals[str(year)] = total
            all_days.extend(days)

    if not all_days:
        raise SystemExit(
            "No contributions were returned from GitHub."
        )

    all_days.sort(key=lambda item: item["date"])

    # Remove zero-contribution years before the first actual contribution.
    first_contribution_date = next(
        day["date"]
        for day in all_days
        if day["count"] > 0
    )

    all_days = [
        day
        for day in all_days
        if day["date"] >= first_contribution_date
    ]

    total = sum(day["count"] for day in all_days)

    first_year = int(all_days[0]["date"][:4])
    last_year = int(all_days[-1]["date"][:4])

    output = {
        "username": USERNAME,
        "fetched_at": today.isoformat(),
        "from": all_days[0]["date"],
        "to": all_days[-1]["date"],
        "first_contribution_date": first_contribution_date,
        "total": total,
        "years": {
            year: yearly_totals[year]
            for year in sorted(yearly_totals)
        },
        "days": all_days,
    }

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)

    OUTPUT.write_text(
        json.dumps(output, indent=2) + "\n",
        encoding="utf-8",
    )

    print()
    print("=" * 50)
    print("Contribution history fetched successfully")
    print("=" * 50)
    print(f"Username : {USERNAME}")
    print(f"Years    : {first_year} → {last_year}")
    print(f"First    : {first_contribution_date}")
    print(f"Days     : {len(all_days)}")
    print(f"Total    : {total}")
    print()

    print("Yearly totals:")
    for year, year_total in sorted(yearly_totals.items()):
        print(f"  {year}: {year_total}")

    print()
    print(f"Output   : {OUTPUT}")


if __name__ == "__main__":
    main()
