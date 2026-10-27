from __future__ import annotations

import csv
import json
from collections import Counter
from pathlib import Path
import sys
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from data.loaders import load_councils
from utils.content_contracts import page_records_by_route


REPORT_DIR = ROOT / "reports" / "recovery-2026-09-05"
BASELINE = REPORT_DIR / "baseline" / "url-inventory.csv"
PERFORMANCE = (
    ROOT
    / "artifacts"
    / "recovery-pack-2026-09-04"
    / "UKPG_RECOVERY_PACK_2026-09-04"
    / "data"
    / "raw_performance_export"
    / "Pages.csv"
)
PRIORITIES = (
    ROOT
    / "artifacts"
    / "recovery-pack-2026-09-04"
    / "UKPG_RECOVERY_PACK_2026-09-04"
    / "data"
    / "recovery_priority_urls.csv"
)
OUTPUT = REPORT_DIR / "url-inventory-and-classification.csv"
SUMMARY = REPORT_DIR / "url-classification-summary.json"
PRODUCTION_COMMIT = "aa7d89ec029c70d5973b7d982fcbe5036316d9b2"
PRODUCTION_DATE = "2026-07-22T17:57:39+01:00"

FIELDS = [
    "url",
    "family",
    "jurisdiction",
    "depth",
    "http_status",
    "indexable",
    "canonical",
    "in_sitemap",
    "internal_links",
    "clicks",
    "impressions",
    "position",
    "conversions",
    "backlinks_if_available",
    "last_generated",
    "last_source_checked",
    "semantic_gate",
    "local_delta",
    "decision",
    "target_url",
    "reason",
    "reviewer",
    "deploy_batch",
]

SEMANTIC_REPAIR_ROUTES = {
    "/permitted-development/north-yorkshire/",
    "/conservation-areas/glasgow-city/",
    "/councils/sheffield/",
}
PROTECTED_EXACT_KEEP = {
    "/fences-and-walls/county-durham/durham/",
}


def path_for(url: str) -> str:
    path = urlparse(url).path or "/"
    return path if path.endswith("/") else f"{path}/"


def normalized_url(url: str) -> str:
    parsed = urlparse(url.strip())
    return f"https://ukplanningguide.co.uk{path_for(url)}"


def metrics_by_url(path: Path) -> dict[str, dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        rows = csv.DictReader(handle)
        return {
            normalized_url(row["Top pages"]): row
            for row in rows
            if row.get("Top pages", "").strip()
        }


def priority_urls(path: Path) -> set[str]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return {
            normalized_url(row["url"])
            for row in csv.DictReader(handle)
            if row.get("url", "").strip()
        }


def authority_jurisdictions() -> dict[str, str]:
    result: dict[str, str] = {}
    for councils in load_councils().values():
        for council in councils:
            result[council["town_slug"]] = council.get("country_slug", "england")
    return result


def infer_jurisdiction(url_path: str, authority_map: dict[str, str]) -> str:
    parts = [part for part in url_path.strip("/").split("/") if part]
    if parts and parts[0] in {"england", "scotland", "wales", "northern-ireland"}:
        return parts[0]
    for part in reversed(parts):
        if part in authority_map:
            return authority_map[part]
    return "uk_or_unresolved"


def classify(row: dict[str, str], missing: bool, priority_urls: set[str]) -> tuple[str, str, str, str]:
    url = row["url"]
    route = path_for(url)
    clicks = int(float(row.get("clicks") or 0))
    if missing:
        return (
            "IMPROVE",
            "Clicked URL is a verified live 404; preserve demand evidence and decide exact restoration versus evidence-led retirement.",
            "missing-click-recovery-1",
            "live_404_protected",
        )
    if str(row.get("noindex", "")).lower() == "true" or row.get("canonical") != url:
        submitted = str(row.get("sitemap", "")).lower() == "true"
        return (
            "NOINDEX/UTILITY",
            "Technical exclusion: noindex and/or non-self-canonical URL must not remain in the submitted sitemap."
            if submitted
            else "Useful noindex route already excluded from the submitted sitemap; retain without expanding indexation.",
            "sitemap-technical-exclusions-1" if submitted else "noindex-existing-not-submitted",
            "technical_exclusion_verified" if submitted else "noindex_existing_verified",
        )
    if route in SEMANTIC_REPAIR_ROUTES:
        return (
            "IMPROVE",
            "Known cross-template contamination repaired in the reviewed canary; keep the exact URL and deploy only the bounded page replacement.",
            "semantic-recovery-1",
            "source_checked_canary_pass",
        )
    if route in PROTECTED_EXACT_KEEP:
        return (
            "KEEP",
            "Proven search-performing page with verified local fence measurements; exact path and local answer are protected.",
            "protected-no-change",
            "protected_verified_sample",
        )
    if clicks > 0 or url in priority_urls:
        return (
            "IMPROVE",
            "Demand-protected URL: keep the exact path while semantic accuracy, sourcing and CTR are reviewed.",
            "protected-review-backlog",
            "protected_pending_semantic_review",
        )
    return (
        "IMPROVE",
        "Generated URL is technically present but lacks URL-level quality approval; preserve it while the semantic cohort is reviewed.",
        "unreviewed-corpus-hold",
        "not_reviewed_do_not_bulk_change",
    )


def main() -> None:
    performance = metrics_by_url(PERFORMANCE)
    priorities = priority_urls(PRIORITIES)
    records = page_records_by_route()
    authority_map = authority_jurisdictions()

    with BASELINE.open(newline="", encoding="utf-8-sig") as handle:
        baseline_rows = list(csv.DictReader(handle))
    present_urls = {normalized_url(row["url"]) for row in baseline_rows}
    rows = list(baseline_rows)
    for url, metrics in performance.items():
        if url in present_urls:
            continue
        rows.append(
            {
                "url": normalized_url(url),
                "family": path_for(url).strip("/").split("/")[0] or "root",
                "canonical": "",
                "noindex": "",
                "sitemap": "False",
                "clicks": metrics.get("Clicks", "0"),
                "impressions": metrics.get("Impressions", ""),
                "position": metrics.get("Position", ""),
                "local_output_same": "False",
            }
        )

    decision_counts: Counter[str] = Counter()
    batch_counts: Counter[str] = Counter()
    missing_count = 0
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        writer.writeheader()
        for source in sorted(rows, key=lambda item: item["url"]):
            url = normalized_url(source["url"])
            source["url"] = url
            route = path_for(url)
            missing = url not in present_urls
            missing_count += int(missing)
            record = records.get(route)
            decision, reason, batch, semantic_gate = classify(source, missing, priorities)
            decision_counts[decision] += 1
            batch_counts[batch] += 1
            parts = [part for part in route.strip("/").split("/") if part]
            metrics = performance.get(url, {})
            writer.writerow(
                {
                    "url": url,
                    "family": source.get("family") or (parts[0] if parts else "root"),
                    "jurisdiction": record.get("jurisdiction") if record else infer_jurisdiction(route, authority_map),
                    "depth": len(parts),
                    "http_status": "404_verified_2026-09-05" if missing else "static_file_present_live_sampled",
                    "indexable": "no" if str(source.get("noindex", "")).lower() == "true" else "technical_yes_semantic_pending",
                    "canonical": source.get("canonical", ""),
                    "in_sitemap": source.get("sitemap", "False"),
                    "internal_links": "not_available",
                    "clicks": source.get("clicks") or metrics.get("Clicks", "0"),
                    "impressions": source.get("impressions") or metrics.get("Impressions", ""),
                    "position": source.get("position") or metrics.get("Position", ""),
                    "conversions": "not_available",
                    "backlinks_if_available": "not_available",
                    "last_generated": f"{PRODUCTION_DATE} {PRODUCTION_COMMIT}",
                    "last_source_checked": record.get("verified_at", "not_available") if record else "not_available",
                    "semantic_gate": semantic_gate,
                    "local_delta": "reviewed_canary_change" if route in SEMANTIC_REPAIR_ROUTES else ("missing_from_production" if missing else ("none" if source.get("local_output_same") == "True" else "unreviewed_local_difference")),
                    "decision": decision,
                    "target_url": "",
                    "reason": reason,
                    "reviewer": "Codex technical classification; owner/content sign-off pending where noted",
                    "deploy_batch": batch,
                }
            )

    summary = {
        "generated_at": "2026-09-06",
        "production_commit": PRODUCTION_COMMIT,
        "total_urls": len(rows),
        "production_files": len(present_urls),
        "verified_live_404_click_urls": missing_count,
        "decision_counts": dict(sorted(decision_counts.items())),
        "deploy_batch_counts": dict(sorted(batch_counts.items())),
        "limitations": [
            "Internal-link counts were not present in the supplied evidence and were not inferred.",
            "Conversion and backlink exports were not supplied.",
            "IMPROVE does not authorize path changes, deletion, redirect, or publication; affected URLs remain protected until cohort review.",
        ],
    }
    SUMMARY.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
