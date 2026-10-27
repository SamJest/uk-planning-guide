from __future__ import annotations

import csv
import json
import re
from dataclasses import asdict, dataclass
from functools import lru_cache
from pathlib import Path
from urllib.parse import urlparse

from core.paths import BASE_URL, ROOT
from data.organic_growth import (
    CTR_TEST_ID,
    PROTECTED_SEARCH_FAMILIES,
    growth_cohort_for_path,
)
from data.search_demand_priorities import gsc_target_for_local_search_slug


GROWTH_ARTIFACT_DIR = ROOT / "artifacts" / "growth"
INDEXATION_MANIFEST_CSV = GROWTH_ARTIFACT_DIR / "indexation-manifest.csv"
INDEXATION_MANIFEST_JSON = GROWTH_ARTIFACT_DIR / "indexation-manifest.json"

INDEXABLE = "index"
NOINDEX = "noindex"
CANONICAL = "canonical"
REVIEW = "review"

CANONICAL_PATTERN = re.compile(
    r'<link\s+rel=["\']canonical["\']\s+href=["\']([^"\']+)["\']',
    re.IGNORECASE,
)
ROBOTS_PATTERN = re.compile(
    r'<meta\s+name=["\']robots["\']\s+content=["\']([^"\']+)["\']',
    re.IGNORECASE,
)


@dataclass(frozen=True)
class IndexationDecision:
    path: str
    search_owner: str
    index_state: str
    canonical_target: str
    cohort: str
    evidence_reason: str
    last_28d_uk_clicks: str = ""
    last_28d_uk_impressions: str = ""
    last_28d_uk_position: str = ""

    def to_dict(self) -> dict[str, str]:
        return asdict(self)


def normalize_path(path: str) -> str:
    clean = str(path or "").strip()
    if clean.startswith(("http://", "https://")):
        clean = urlparse(clean).path
    clean = clean.split("?", 1)[0].split("#", 1)[0]
    if not clean.startswith("/"):
        clean = "/" + clean
    clean = clean.rstrip("/")
    return clean + "/" if clean else "/"


def path_from_canonical(canonical: str) -> str:
    if not canonical:
        return ""
    return normalize_path(canonical)


def search_owner_for_path(path: str) -> str:
    clean = normalize_path(path)
    parts = [part for part in clean.strip("/").split("/") if part]
    if not parts:
        return "/"

    if parts[0] == "local-search" and len(parts) >= 2:
        target = gsc_target_for_local_search_slug(parts[-1])
        owner = target.get("search_owner") or target.get("primary_href")
        return normalize_path(owner) if owner else clean

    if parts[0] == "councils" and len(parts) == 2:
        return clean

    if parts[0] in {
        "article-4",
        "boundary-rules",
        "conservation-areas",
        "height-limits",
        "maximum-height",
        "permitted-development",
        "planning-permission",
    } and len(parts) == 2:
        return clean

    return clean


def _canonical_from_html(html: str) -> str:
    match = CANONICAL_PATTERN.search(html or "")
    return match.group(1).strip() if match else ""


def _robots_from_html(html: str) -> str:
    match = ROBOTS_PATTERN.search(html or "")
    return match.group(1).strip().lower() if match else ""


def derive_indexation_decision(
    path: str,
    html: str,
    metrics: dict[str, object] | None = None,
) -> IndexationDecision:
    clean = normalize_path(path)
    metrics = metrics or {}
    canonical = path_from_canonical(_canonical_from_html(html)) or clean
    robots = _robots_from_html(html)
    owner = search_owner_for_path(clean)
    cohort = growth_cohort_for_path(clean)
    parts = [part for part in clean.strip("/").split("/") if part]

    if "noindex" in robots:
        state = NOINDEX
        reason = "Page explicitly declares noindex."
    elif canonical != clean:
        state = CANONICAL
        reason = "Page canonical points to a different search owner."
    elif parts and parts[0] == "local-search" and clean != "/local-search/":
        state = INDEXABLE
        reason = "Bridge retained pending page-query-country validation; no automatic deindexing."
    elif cohort == CTR_TEST_ID:
        state = INDEXABLE
        reason = "Protected 28-day CTR test cohort with a self-canonical search owner."
    elif parts and parts[0] in PROTECTED_SEARCH_FAMILIES:
        state = INDEXABLE
        reason = "Protected search family with proven click-through performance."
    else:
        state = INDEXABLE
        reason = "Self-canonical page retained until two complete 28-day evidence windows exist."

    return IndexationDecision(
        path=clean,
        search_owner=owner,
        index_state=state,
        canonical_target=canonical,
        cohort=cohort,
        evidence_reason=reason,
        last_28d_uk_clicks=str(metrics.get("clicks", "")),
        last_28d_uk_impressions=str(metrics.get("impressions", "")),
        last_28d_uk_position=str(metrics.get("position", "")),
    )


def write_indexation_manifest(decisions: list[IndexationDecision]) -> None:
    rows = [decision.to_dict() for decision in sorted(decisions, key=lambda item: item.path)]
    GROWTH_ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)
    INDEXATION_MANIFEST_JSON.write_text(
        json.dumps(rows, indent=2, sort_keys=True),
        encoding="utf-8",
    )
    fieldnames = list(IndexationDecision.__dataclass_fields__)
    with INDEXATION_MANIFEST_CSV.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    load_indexation_manifest.cache_clear()


@lru_cache(maxsize=1)
def load_indexation_manifest() -> dict[str, dict[str, str]]:
    if not INDEXATION_MANIFEST_CSV.exists():
        return {}
    with INDEXATION_MANIFEST_CSV.open("r", encoding="utf-8-sig", newline="") as handle:
        return {
            normalize_path(row.get("path", "")): row
            for row in csv.DictReader(handle)
            if row.get("path")
        }


def manifest_decision_for_path(path: str) -> dict[str, str]:
    return load_indexation_manifest().get(normalize_path(path), {})


def should_include_in_sitemap(path: str, html: str) -> bool:
    clean = normalize_path(path)
    decision = manifest_decision_for_path(clean)
    if decision:
        if decision.get("index_state") in {NOINDEX, CANONICAL}:
            return False
        target = normalize_path(decision.get("canonical_target") or clean)
        if target != clean:
            return False
        return decision.get("index_state") == INDEXABLE

    derived = derive_indexation_decision(clean, html)
    return derived.index_state == INDEXABLE and derived.canonical_target == clean
