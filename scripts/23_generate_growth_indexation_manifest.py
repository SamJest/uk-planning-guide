from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor
import csv
import os
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from core.paths import OUTPUT_FOLDER
from core.build_scope import build_mode
from utils.indexation import (
    derive_indexation_decision,
    normalize_path,
    write_indexation_manifest,
)


def _number(value: str) -> float:
    try:
        return float(str(value or "").replace(",", "").replace("%", "").strip())
    except ValueError:
        return 0.0


def _first(row: dict[str, str], *names: str) -> str:
    lowered = {str(key).strip().lower(): value for key, value in row.items()}
    for name in names:
        value = lowered.get(name.lower())
        if value not in (None, ""):
            return str(value)
    return ""


def load_page_metrics(path: Path | None) -> dict[str, dict[str, object]]:
    if not path or not path.exists():
        return {}
    totals: dict[str, dict[str, float]] = {}
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        for row in csv.DictReader(handle):
            country = _first(row, "country")
            if country and country.lower() not in {"gbr", "united kingdom", "uk"}:
                continue
            page = _first(row, "page", "top pages")
            if not page:
                continue
            clean = normalize_path(page)
            item = totals.setdefault(clean, {"clicks": 0.0, "impressions": 0.0, "position_total": 0.0})
            clicks = _number(_first(row, "clicks"))
            impressions = _number(_first(row, "impressions"))
            position = _number(_first(row, "position", "average position"))
            item["clicks"] += clicks
            item["impressions"] += impressions
            item["position_total"] += position * impressions

    return {
        key: {
            "clicks": int(value["clicks"]),
            "impressions": int(value["impressions"]),
            "position": round(value["position_total"] / value["impressions"], 2)
            if value["impressions"]
            else "",
        }
        for key, value in totals.items()
    }


def output_path_to_route(page: Path) -> str:
    relative = page.relative_to(OUTPUT_FOLDER)
    parts = list(relative.parts)
    if parts and parts[-1] == "index.html":
        parts = parts[:-1]
    return normalize_path("/" + "/".join(parts))


def read_html_head(page: Path, limit: int = 65536) -> str:
    with page.open("r", encoding="utf-8", errors="ignore") as handle:
        return handle.read(limit)


def route_needs_head_inspection(route: str) -> bool:
    clean = normalize_path(route)
    return bool(
        clean == "/local-search/"
        or clean.startswith("/england/services/")
        or clean in {
            "/planning-help/thank-you/",
            "/personalised-planning-guidance/request/",
            "/personalised-planning-guidance/request/success/",
            "/find-help/homeowners/request/success/",
            "/find-help/specialists/apply/success/",
        }
    )


def build_manifest(metrics_csv: Path | None = None) -> int:
    metrics = load_page_metrics(metrics_csv)
    pages = sorted(OUTPUT_FOLDER.rglob("index.html"))

    def decision_for_page(page: Path):
        route = output_path_to_route(page)
        # Sitemap eligibility is a property of the rendered page, not its route
        # shape. Read every head so noindex and non-self-canonical pages can
        # never be promoted by a synthetic default during a full build.
        html = read_html_head(page)
        return derive_indexation_decision(route, html, metrics.get(route))

    worker_count = max(1, min(16, int(os.environ.get("UKPG_INDEXATION_READ_WORKERS", "8"))))
    with ThreadPoolExecutor(max_workers=worker_count) as executor:
        decisions = list(executor.map(decision_for_page, pages))
    write_indexation_manifest(decisions)
    print(f"Growth indexation manifest generated: {len(decisions)} routes")
    return len(decisions)


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate the auditable organic-growth indexation manifest.")
    parser.add_argument(
        "--metrics-csv",
        type=Path,
        help="Optional GSC page/query export containing UK page metrics.",
    )
    args = parser.parse_args()
    build_manifest(args.metrics_csv)


if __name__ == "__main__":
    main()
