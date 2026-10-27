from __future__ import annotations

import csv
import argparse
from dataclasses import asdict
from dataclasses import dataclass
import json
from pathlib import Path
import re
import sys


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from core.paths import ROOT
from data.loaders import load_projects
from data.scenario_data import SCENARIOS
from utils.content_contracts import BASE_URL, normalize_path
from utils.content_integrity import lint_rendered_html, simhash64, simhash_similarity, visible_text


LIVE_OUTPUT = ROOT / "output"
REPORT_DIR = ROOT / "reports" / "phase-0"
GSC_PAGES = ROOT / "artifacts" / "_tmp_sc" / "Pages.csv"
SOURCE_COUNT_PATTERN = re.compile(r'data-official-sources-count="(\d+)"', re.IGNORECASE)
SOURCE_FAMILY_PATTERN = re.compile(r'data-official-sources-family="([^"]+)"', re.IGNORECASE)
CANONICAL_PATTERN = re.compile(r'<link\s+rel="canonical"\s+href="([^"]+)"', re.IGNORECASE)

PROJECT_SLUGS = {project["slug"] for project in load_projects()}
RULE_SLUGS = {scenario["slug"] for scenario in SCENARIOS}
COUNTRIES = {"england", "wales", "scotland", "northern-ireland"}


@dataclass
class PageAudit:
    route: str
    family: str
    word_count: int
    fingerprint: int
    local_fact_count: int
    source_count: int
    source_family_match: bool
    contamination_flags: list[str]
    clicks: int
    impressions: int
    canonical: str
    similarity: float = 0.0
    proposed_action: str = "keep"

    def to_dict(self) -> dict:
        return {
            "url": BASE_URL.rstrip("/") + self.route,
            "route": self.route,
            "family": self.family,
            "word_count": self.word_count,
            "content_similarity_score": round(self.similarity, 4),
            "local_fact_count": self.local_fact_count,
            "source_count": self.source_count,
            "source_family_match": self.source_family_match,
            "contamination_flags": "|".join(self.contamination_flags),
            "last_28d_uk_clicks": self.clicks,
            "last_28d_uk_impressions": self.impressions,
            "organic_importance": "high" if self.clicks >= 2 or self.impressions >= 100 else "medium" if self.clicks or self.impressions >= 20 else "unknown",
            "canonical": self.canonical,
            "proposed_action": self.proposed_action,
        }

    def to_raw_dict(self) -> dict:
        return asdict(self)


def _route_for_page(path: Path) -> str:
    relative = path.relative_to(LIVE_OUTPUT)
    parts = list(relative.parts)
    if parts and parts[-1] == "index.html":
        parts.pop()
    return normalize_path("/" + "/".join(parts))


def _classify(route: str) -> tuple[str, str, str | None, str | None, str | None]:
    parts = [part for part in route.strip("/").split("/") if part]
    if not parts:
        return "national_guide", "uk", None, None, None
    if parts[0] in COUNTRIES:
        country = parts[0]
        section = parts[1] if len(parts) > 1 else ""
        if section == "projects":
            return ("local_project" if len(parts) >= 4 else "project_guide", country, parts[3] if len(parts) >= 4 else None, parts[2] if len(parts) >= 3 else None, None)
        if section == "rules":
            return ("local_rule" if len(parts) >= 4 else "rule_guide", country, parts[3] if len(parts) >= 4 else None, None, parts[2] if len(parts) >= 3 else None)
        if section == "councils":
            if len(parts) >= 3:
                return "authority_profile", country, parts[2], None, None
            return "national_guide", country, None, None, None
        if section == "tools":
            return "tool", country, None, None, None
        if section == "data":
            return "data_report", country, None, None, None
        return "national_guide", country, None, None, None
    if parts[0] == "councils" and len(parts) >= 2:
        return "authority_profile", "england", parts[1], None, None
    if parts[0] in RULE_SLUGS:
        return ("local_rule" if len(parts) >= 2 else "rule_guide", "england", parts[1] if len(parts) >= 2 else None, None, parts[0])
    if parts[0] in PROJECT_SLUGS:
        return ("local_project" if len(parts) >= 3 else "project_guide", "uk", parts[2] if len(parts) >= 3 else None, parts[0], None)
    if parts[0] == "tools" or parts[0] == "my-planning-project":
        return "tool", "uk", None, None, None
    if parts[0] == "workflows":
        return "workflow", "uk", None, None, None
    if parts[0] == "updates":
        return "news", "uk", None, None, None
    return "national_guide", "uk", None, None, None


def _gsc_metrics() -> dict[str, tuple[int, int]]:
    if not GSC_PAGES.exists():
        return {}
    metrics = {}
    with GSC_PAGES.open("r", encoding="utf-8-sig", newline="") as handle:
        for row in csv.DictReader(handle):
            route = normalize_path(row.get("Top pages", ""))
            try:
                clicks = int(float(row.get("Last 28 days Clicks", 0) or 0))
                impressions = int(float(row.get("Last 28 days Impressions", 0) or 0))
            except ValueError:
                clicks = impressions = 0
            metrics[route] = (clicks, impressions)
    return metrics


def _audit_page(path: Path, metrics: dict[str, tuple[int, int]]) -> PageAudit:
    route = _route_for_page(path)
    family, jurisdiction, authority, project, rule = _classify(route)
    html = path.read_text(encoding="utf-8", errors="ignore")
    text = visible_text(html)
    source_match = SOURCE_FAMILY_PATTERN.search(html)
    expected_source_family = {
        "authority_profile": "council",
        "local_project": "project",
        "local_rule": "scenario",
    }.get(family)
    source_count_match = SOURCE_COUNT_PATTERN.search(html)
    record = {
        "page_family": family,
        "jurisdiction": jurisdiction,
        "authority_id": authority,
        "project_id": project,
        "rule_id": rule,
        "review_status": "published",
        "index_status": "index",
    }
    flags = sorted({finding.code for finding in lint_rendered_html(record, html)})
    canonical_match = CANONICAL_PATTERN.search(html)
    clicks, impressions = metrics.get(route, (0, 0))
    return PageAudit(
        route=route,
        family=family,
        word_count=len(text.split()),
        fingerprint=simhash64(text),
        local_fact_count=html.count('data-local-fact="true"'),
        source_count=int(source_count_match.group(1)) if source_count_match else 0,
        source_family_match=not expected_source_family or bool(source_match and source_match.group(1) == expected_source_family),
        contamination_flags=flags,
        clicks=clicks,
        impressions=impressions,
        canonical=canonical_match.group(1) if canonical_match else "",
    )


def _score_similarity(pages: list[PageAudit]) -> None:
    buckets: dict[tuple[str, int], list[PageAudit]] = {}
    for page in pages:
        key = (page.family, page.fingerprint >> 52)
        candidates = buckets.setdefault(key, [])
        if candidates:
            page.similarity = max(simhash_similarity(page.fingerprint, candidate.fingerprint) for candidate in candidates[-64:])
        candidates.append(page)


def _choose_action(page: PageAudit) -> str:
    canonical_path = normalize_path(page.canonical) if page.canonical else page.route
    if canonical_path != page.route:
        return "redirect"
    if page.contamination_flags or not page.source_family_match:
        return "noindex"
    if page.family in {"authority_profile", "local_project", "local_rule"} and (page.source_count < 3 or page.local_fact_count < 5):
        return "repair"
    if page.similarity >= 0.95 and page.clicks == 0:
        return "merge"
    if page.word_count < 250:
        return "repair"
    return "keep"


def _write_final_reports(pages: list[PageAudit]) -> dict:
    _score_similarity(pages)
    for page in pages:
        page.proposed_action = _choose_action(page)
    rows = [page.to_dict() for page in pages]
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    (REPORT_DIR / "page-inventory.json").write_text(json.dumps(rows, indent=2) + "\n", encoding="utf-8")
    with (REPORT_DIR / "page-inventory.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]) if rows else ["url"])
        writer.writeheader()
        writer.writerows(rows)
    summary = {
        "route_count": len(rows),
        "actions": {action: sum(1 for row in rows if row["proposed_action"] == action) for action in ("keep", "repair", "merge", "noindex", "redirect", "410")},
        "note": "Recommendations only. No live URL, indexation or redirect state was changed.",
    }
    (REPORT_DIR / "page-inventory-summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2))
    return summary


def generate_inventory(*, shard_index: int | None = None, shard_count: int = 1) -> dict:
    metrics = _gsc_metrics()
    paths = sorted(LIVE_OUTPUT.rglob("index.html"))
    if shard_index is not None:
        if shard_count < 1 or shard_index < 0 or shard_index >= shard_count:
            raise ValueError("Invalid shard selection")
        paths = paths[shard_index::shard_count]
    pages = []
    for position, path in enumerate(paths, start=1):
        pages.append(_audit_page(path, metrics))
        if position % 1000 == 0:
            print(f"Audited {position}/{len(paths)} pages", flush=True)
    if shard_index is None:
        return _write_final_reports(pages)
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    shard_path = REPORT_DIR / f"page-inventory-shard-{shard_index}-of-{shard_count}.json"
    shard_path.write_text(json.dumps([page.to_raw_dict() for page in pages]) + "\n", encoding="utf-8")
    result = {"shard_index": shard_index, "shard_count": shard_count, "route_count": len(pages), "path": str(shard_path)}
    print(json.dumps(result, indent=2))
    return result


def merge_inventory_shards(shard_count: int) -> dict:
    pages: list[PageAudit] = []
    for index in range(shard_count):
        path = REPORT_DIR / f"page-inventory-shard-{index}-of-{shard_count}.json"
        if not path.exists():
            raise FileNotFoundError(f"Missing inventory shard: {path}")
        payload = json.loads(path.read_text(encoding="utf-8"))
        pages.extend(PageAudit(**item) for item in payload)
    pages.sort(key=lambda page: page.route)
    return _write_final_reports(pages)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Audit current generated routes without changing live output.")
    parser.add_argument("--shard-index", type=int)
    parser.add_argument("--shard-count", type=int, default=1)
    parser.add_argument("--merge", action="store_true")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    if args.merge:
        merge_inventory_shards(args.shard_count)
    else:
        generate_inventory(shard_index=args.shard_index, shard_count=args.shard_count)
