from __future__ import annotations

import argparse
import csv
from pathlib import Path


DEFAULT_MIN_IMPRESSIONS = 50
DEFAULT_MAX_CTR = 0.02
DEFAULT_MAX_POSITION = 30.0


def _number(value: str) -> float:
    clean = str(value or "").replace("%", "").replace(",", "").strip()
    if not clean:
        return 0.0
    try:
        return float(clean)
    except ValueError:
        return 0.0


def _ctr(value: str) -> float:
    number = _number(value)
    return number / 100 if "%" in str(value) or number > 1 else number


def _get(row: dict[str, str], *names: str) -> str:
    lowered = {key.strip().lower(): value for key, value in row.items()}
    for name in names:
        if name.lower() in lowered:
            return lowered[name.lower()]
    return ""


def load_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def score_row(row: dict[str, str]) -> tuple[float, dict[str, str | float]]:
    page = _get(row, "Page", "Pages", "Top pages")
    query = _get(row, "Query", "Queries", "Top queries")
    clicks = _number(_get(row, "Clicks"))
    impressions = _number(_get(row, "Impressions"))
    ctr = _ctr(_get(row, "CTR"))
    position = _number(_get(row, "Position", "Average position"))
    score = impressions * max(DEFAULT_MAX_CTR - ctr, 0.001) * max(DEFAULT_MAX_POSITION - min(position, DEFAULT_MAX_POSITION), 1)
    return score, {
        "page": page,
        "query": query,
        "clicks": clicks,
        "impressions": impressions,
        "ctr": ctr,
        "position": position,
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Create a small Search Console-driven title/meta/content refresh batch."
    )
    parser.add_argument("csv_path", type=Path, help="Search Console Pages.csv or Queries.csv export")
    parser.add_argument("--limit", type=int, default=25)
    parser.add_argument("--min-impressions", type=float, default=DEFAULT_MIN_IMPRESSIONS)
    parser.add_argument("--max-ctr", type=float, default=DEFAULT_MAX_CTR)
    parser.add_argument("--max-position", type=float, default=DEFAULT_MAX_POSITION)
    args = parser.parse_args()

    candidates = []
    for row in load_rows(args.csv_path):
        score, item = score_row(row)
        if item["impressions"] < args.min_impressions:
            continue
        if item["ctr"] > args.max_ctr:
            continue
        if item["position"] > args.max_position:
            continue
        candidates.append((score, item))

    candidates.sort(key=lambda pair: pair[0], reverse=True)

    print("# Search Console Refresh Batch")
    print()
    print("Use these rows for title/meta, first-answer and internal-link refreshes. Do not create new pages unless the current target is clearly mismatched.")
    print()
    print("| Priority | Page | Query | Clicks | Impressions | CTR | Position |")
    print("|---:|---|---|---:|---:|---:|---:|")
    for index, (_, item) in enumerate(candidates[: args.limit], start=1):
        page = item["page"] or "-"
        query = item["query"] or "-"
        print(
            f"| {index} | {page} | {query} | {item['clicks']:.0f} | "
            f"{item['impressions']:.0f} | {item['ctr']:.2%} | {item['position']:.2f} |"
        )


if __name__ == "__main__":
    main()
