from __future__ import annotations

import csv
import re
import sys
import zipfile
from collections import defaultdict
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from data.editorial_authority import EDITORIAL_AUTHORITY, PRIORITY_EDITORIAL_PAGES

SCENARIO_SLUGS = {
    "planning-permission",
    "permitted-development",
    "height-limits",
    "boundary-rules",
    "conservation-areas",
}

FAQ_PREFIX = "/planning-faq/"
RULE_KEYWORDS = (
    "planning permission",
    "permitted development",
    "height",
    "boundary",
    "conservation",
    "article 4",
    "listed building",
)
PROJECT_KEYWORDS = (
    "extension",
    "extensions",
    "loft",
    "dormer",
    "garden room",
    "outbuilding",
    "garage",
    "porch",
    "driveway",
    "dropped kerb",
    "fence",
    "wall",
    "solar",
    "heat pump",
    "annexe",
    "hmo",
)

WORD_PATTERN = re.compile(r"[a-z0-9]+")


def _as_int(value: str) -> int:
    try:
        return int(str(value).replace(",", "").strip())
    except Exception:
        return 0


def _as_float(value: str) -> float:
    clean = str(value).replace("%", "").replace(",", "").strip()
    try:
        return float(clean)
    except Exception:
        return 0.0


def _load_csv_from_zip(zip_path: Path, name: str) -> list[dict[str, str]]:
    with zipfile.ZipFile(zip_path) as archive:
        with archive.open(name) as handle:
            text = handle.read().decode("utf-8-sig")
    reader = csv.DictReader(text.splitlines())
    return list(reader)


def _path_from_url(url: str) -> str:
    for prefix in ("https://ukplanningguide.co.uk", "http://ukplanningguide.co.uk"):
        if url.startswith(prefix):
            url = url[len(prefix):]
    return url


def priority_editorial_baseline(pages: list[dict[str, str]]) -> list[tuple[str, str, int, int, float, float]]:
    page_lookup = {
        _path_from_url(row.get("Top pages", "")): row
        for row in pages
    }
    rows = []
    for path in PRIORITY_EDITORIAL_PAGES:
        row = page_lookup.get(path, {})
        record = EDITORIAL_AUTHORITY.get(path, {})
        clicks = _as_int(row.get("Clicks", "0"))
        impressions = _as_int(row.get("Impressions", "0"))
        ctr = _as_float(row.get("CTR", "0"))
        position = _as_float(row.get("Position", "0"))
        rows.append(
            (
                record.get("family", "unknown"),
                path,
                clicks,
                impressions,
                ctr,
                position,
            )
        )
    return rows


def scenario_report(pages: list[dict[str, str]]) -> list[tuple[str, int, int, float]]:
    totals: dict[str, list[float]] = defaultdict(lambda: [0, 0, 0.0, 0])
    for row in pages:
        path = _path_from_url(row.get("Top pages", ""))
        parts = [part for part in path.strip("/").split("/") if part]
        scenario_slug = ""
        if len(parts) == 2 and parts[0] in SCENARIO_SLUGS:
            scenario_slug = parts[0]
        elif len(parts) >= 4 and parts[-1] in SCENARIO_SLUGS:
            scenario_slug = parts[-1]
        if scenario_slug:
            totals[scenario_slug][0] += _as_int(row.get("Clicks", "0"))
            totals[scenario_slug][1] += _as_int(row.get("Impressions", "0"))
            totals[scenario_slug][2] += _as_float(row.get("Position", "0"))
            totals[scenario_slug][3] += 1
    return sorted(
        (
            (
                slug,
                int(values[0]),
                int(values[1]),
                round(values[2] / values[3], 2) if values[3] else 0.0,
            )
            for slug, values in totals.items()
        ),
        key=lambda item: item[2],
        reverse=True,
    )


def faq_ctr_opportunities(pages: list[dict[str, str]]) -> list[tuple[str, int, int, float, float]]:
    rows = []
    for row in pages:
        path = _path_from_url(row.get("Top pages", ""))
        if not path.startswith(FAQ_PREFIX):
            continue
        impressions = _as_int(row.get("Impressions", "0"))
        ctr = _as_float(row.get("CTR", "0"))
        if impressions >= 20 and ctr < 3:
            rows.append(
                (
                    path,
                    _as_int(row.get("Clicks", "0")),
                    impressions,
                    ctr,
                    _as_float(row.get("Position", "0")),
                )
            )
    return sorted(rows, key=lambda item: item[2], reverse=True)[:15]


def near_win_queries(queries: list[dict[str, str]]) -> list[tuple[str, int, int, float]]:
    rows = []
    for row in queries:
        position = _as_float(row.get("Position", "0"))
        impressions = _as_int(row.get("Impressions", "0"))
        if 11 <= position <= 30 and impressions >= 20:
            rows.append((row.get("Top queries", ""), _as_int(row.get("Clicks", "0")), impressions, position))
    return sorted(rows, key=lambda item: item[2], reverse=True)[:20]


def classify_near_win_queries(
    queries: list[tuple[str, int, int, float]]
) -> dict[str, list[tuple[str, int, int, float]]]:
    buckets = {
        "authority_intent": [],
        "rule_intent": [],
        "project_location": [],
    }

    for row in queries:
        query = row[0].lower().strip()
        tokens = set(WORD_PATTERN.findall(query))
        normalized_query = " ".join(tokens) if tokens else query
        has_project_keyword = False
        for keyword in PROJECT_KEYWORDS:
            if " " in keyword:
                if keyword in query:
                    has_project_keyword = True
                    break
            elif keyword in tokens:
                has_project_keyword = True
                break

        has_rule_keyword = False
        for keyword in RULE_KEYWORDS:
            if " " in keyword:
                if keyword in query:
                    has_rule_keyword = True
                    break
            elif keyword in tokens or keyword in normalized_query:
                has_rule_keyword = True
                break

        if has_project_keyword:
            buckets["project_location"].append(row)
            continue
        if has_rule_keyword:
            buckets["rule_intent"].append(row)
            continue
        buckets["authority_intent"].append(row)

    return buckets


def main() -> int:
    if len(sys.argv) > 1:
        zip_path = Path(sys.argv[1])
    else:
        zip_path = Path.home() / "Downloads" / "https___ukplanningguide.co.uk_-Performance-on-Search-2026-03-27.zip"

    if not zip_path.exists():
        print(f"Search Console export not found: {zip_path}")
        return 1

    pages = _load_csv_from_zip(zip_path, "Pages.csv")
    queries = _load_csv_from_zip(zip_path, "Queries.csv")

    print("=== RETAINED SCENARIO TOPICS ===")
    for slug, clicks, impressions, position in scenario_report(pages):
        print(f"{slug}: clicks={clicks} impressions={impressions} avg_position={position}")

    print("\n=== PRIORITY EDITORIAL COHORT BASELINE ===")
    cohort_rows = priority_editorial_baseline(pages)
    cohort_clicks = sum(item[2] for item in cohort_rows)
    cohort_impressions = sum(item[3] for item in cohort_rows)
    for family, path, clicks, impressions, ctr, position in cohort_rows:
        print(
            f"{family}: {path} | clicks={clicks} impressions={impressions} ctr={ctr}% avg_position={position}"
        )
    print(
        f"cohort totals: clicks={cohort_clicks} impressions={cohort_impressions} "
        f"pages={len(cohort_rows)}"
    )

    print("\n=== FAQ CTR OPPORTUNITIES ===")
    for path, clicks, impressions, ctr, position in faq_ctr_opportunities(pages):
        print(f"{path}: clicks={clicks} impressions={impressions} ctr={ctr}% avg_position={position}")

    near_wins = near_win_queries(queries)
    buckets = classify_near_win_queries(near_wins)

    print("\n=== AUTHORITY-INTENT NEAR-WINS ===")
    for query, clicks, impressions, position in buckets["authority_intent"]:
        print(f"{query}: clicks={clicks} impressions={impressions} avg_position={position}")

    print("\n=== RULE-INTENT NEAR-WINS ===")
    for query, clicks, impressions, position in buckets["rule_intent"]:
        print(f"{query}: clicks={clicks} impressions={impressions} avg_position={position}")

    print("\n=== PROJECT-LOCATION NEAR-WINS ===")
    for query, clicks, impressions, position in buckets["project_location"]:
        print(f"{query}: clicks={clicks} impressions={impressions} avg_position={position}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
