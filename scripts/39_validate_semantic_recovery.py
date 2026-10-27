"""Validate the first semantic recovery cohort against an explicit live-tree baseline."""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from core.paths import BASE_URL
from utils.content_contracts import page_records_by_route
from utils.content_integrity import lint_rendered_html
from utils.phase0_validation import output_file_for_route


RECOVERY_ROUTES = (
    "/permitted-development/north-yorkshire/",
    "/conservation-areas/glasgow-city/",
    "/councils/sheffield/",
)
PRESERVED_BASELINE_ROUTES = (
    "/dropped-kerbs/",
    "/solar-panels/",
    "/article-4-hmo-by-council/",
    "/fences-and-walls/county-durham/durham/",
)
PRODUCT_JOURNEY_ROUTE = "/tools/"
PRODUCT_JOURNEY_MARKERS = (
    "Planning Route Check",
    "Local Constraint Check",
    "Project Readiness",
    "My Planning Project",
    "Show all specialist planning tools",
)
CANONICAL = re.compile(r'<link\s+rel=["\']canonical["\']\s+href=["\']([^"\']+)', re.I)
ROBOTS = re.compile(r'<meta\s+name=["\']robots["\']\s+content=["\']([^"\']+)', re.I)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--site", type=Path, required=True)
    parser.add_argument("--baseline", type=Path, required=True)
    parser.add_argument("--report", type=Path, required=True)
    args = parser.parse_args(argv)
    records = page_records_by_route()
    errors: list[dict[str, str]] = []
    pages = []
    for route in RECOVERY_ROUTES:
        page = output_file_for_route(args.site, route)
        record = records[route]
        if not page.is_file():
            errors.append({"route": route, "code": "missing-page"})
            continue
        html = page.read_text(encoding="utf-8", errors="ignore")
        canonical_match = CANONICAL.search(html)
        expected = BASE_URL.rstrip("/") + route
        canonical = canonical_match.group(1) if canonical_match else ""
        if canonical != expected:
            errors.append({"route": route, "code": "canonical", "detail": canonical})
        if "noindex" in " ".join(ROBOTS.findall(html)).lower():
            errors.append({"route": route, "code": "unexpected-noindex"})
        for finding in lint_rendered_html(record, html):
            if finding.severity == "error":
                errors.append({"route": route, "code": finding.code, "detail": finding.message})
        if "editorial desk" in html.lower() or "assumed setup" in html.lower():
            errors.append({"route": route, "code": "creator-or-assumption-language"})
        pages.append({"route": route, "bytes": page.stat().st_size, "canonical": canonical, "project_id": record["project_id"], "rule_id": record["rule_id"], "jurisdiction": record["jurisdiction"], "authority_id": record["authority_id"]})
    preserved = []
    for route in PRESERVED_BASELINE_ROUTES:
        page = output_file_for_route(args.baseline, route)
        if not page.is_file():
            errors.append({"route": route, "code": "missing-protected-baseline-page"})
            continue
        html = page.read_text(encoding="utf-8", errors="ignore")
        canonical_match = CANONICAL.search(html)
        canonical = canonical_match.group(1) if canonical_match else ""
        expected = BASE_URL.rstrip("/") + route
        if canonical != expected:
            errors.append({"route": route, "code": "protected-canonical", "detail": canonical})
        if route.endswith("/durham/") and not all(marker in html.lower() for marker in ("1 metre", "2 metres", "highway")):
            errors.append({"route": route, "code": "durham-height-rule-lost"})
        preserved.append({"route": route, "bytes": page.stat().st_size, "canonical": canonical})
    product_page = output_file_for_route(args.site, PRODUCT_JOURNEY_ROUTE)
    if not product_page.is_file():
        errors.append({"route": PRODUCT_JOURNEY_ROUTE, "code": "missing-product-journey-page"})
        product_markers = []
    else:
        product_html = product_page.read_text(encoding="utf-8", errors="ignore")
        product_markers = [marker for marker in PRODUCT_JOURNEY_MARKERS if marker in product_html]
        if len(product_markers) != len(PRODUCT_JOURNEY_MARKERS):
            errors.append({"route": PRODUCT_JOURNEY_ROUTE, "code": "four-capability-journey-incomplete"})
    report = {
        "status": "passed" if not errors else "failed",
        "errors": errors,
        "recovery_pages": pages,
        "product_journey": {"route": PRODUCT_JOURNEY_ROUTE, "markers": product_markers},
        "preserved_baseline_pages": preserved,
    }
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
