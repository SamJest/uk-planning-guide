from __future__ import annotations

import argparse
from collections import defaultdict
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET
from html import unescape

from components.sitemap_builders import classify_url
from data.download_assets import DOWNLOAD_ASSETS, download_asset_path
from data.building_regulations_pages import BUILDING_REGULATIONS_PAGES, building_regulations_path
from data.find_help import FIND_HELP_DRAFT_ROUTES, FIND_HELP_ENABLED, FIND_HELP_ROUTES
from data.gsc_recovery_routes import GSC_RECOVERY_ROUTES, GSC_RECOVERY_PATHS, recovery_path
from data.local_search_pages import LOCAL_SEARCH_PAGES
from data.loaders import load_councils, load_projects
from data.tools_data import load_tools
from data.faq_data import FAQS
from data.promoted_links import FAQ_INDEX_NEXT_STEP_KEYS, PROMOTED_LINKS
from data.search_demand_priorities import (
    DATA_LED_LOCAL_SEARCH_SLUGS,
    GSC_CLUSTER_HUBS,
    GSC_CLUSTER_HUB_SLUGS,
    GSC_EXPANSION_LOCAL_SEARCH_SLUGS,
    GSC_EXPANSION_RELEASE_LIMITS,
    HMO_ARTICLE_4_PRIORITY_ROUTES,
)
from data.custom_tool_configs import CUSTOM_TOOL_CONFIGS
from utils.sitemap_config import (
    BASE_URL,
    CHILD_SITEMAP_NAME_PATTERN,
    LEGACY_ROOT_SITEMAP_NAME_PATTERN,
    XML_NAMESPACE,
)
from utils.live_links import is_live_internal_href, normalize_internal_href
from utils.local_search_strategy import (
    local_search_authority_href,
    local_search_entry_lead,
    local_search_is_broad_authority_query,
    local_search_next_step_phrase,
    local_search_owner,
    local_search_project_href,
    local_search_scenario_href,
    local_search_topic_phrase,
)
from utils.local_note_validation import (
    FIELD_KEYWORDS,
    KNOWN_CONTAMINATED_SNIPPETS,
    normalize_local_note,
)
from utils.text_cleaning import looks_mojibake
from utils.country_utils import get_country_slug
from utils.official_sources import (
    OfficialSourceContext,
    official_source_coverage_gaps,
    relevant_official_sources,
    validate_official_source_registry,
)
from utils.scenario_config import load_scenarios
from utils.route_contracts import is_legacy_country_bridge_path, route_contract_for_country_path
from utils.content_contracts import page_records_by_route

ROOT_DIR = Path(__file__).resolve().parent
_configured_output = str(os.environ.get("UKPG_OUTPUT_DIR") or "").strip()
OUTPUT_DIR = Path(_configured_output).resolve() if _configured_output else ROOT_DIR / "output"
SITEMAP_DIR = OUTPUT_DIR / "sitemaps"
TOOLS_DIR = OUTPUT_DIR / "tools"
TOOL_SMOKE_SCRIPT = Path(__file__).resolve().parent / "scripts" / "tool_smoke_test.js"
VALIDATION_MODE_FILE = Path(__file__).resolve().parent / ".validate-mode"
MAX_FULL_PAGE_HEALTH_SCAN = 300000
MAX_HEALTH_SCAN_PAGES_PER_FAMILY_KEY = 25
MAX_CONTENT_SCAN_PAGES_PER_FAMILY_KEY = 120
MAX_REPORTED_ERRORS = 25
DUPLICATE_CLUSTER_FAILURE_THRESHOLD = 10
FAMILY_REPETITION_FAILURE_THRESHOLD = 12
FAMILY_REPETITION_SAMPLE_LIMIT = 80
MIN_LOCAL_SEARCH_WORD_COUNT = 220
PROJECT_CROSS_TOPIC_MARKERS = {
    "all": (
        "odour abatement technologies",
        "commercial kitchens",
        "brownfield register",
        "planning performance agreement",
        "pre application meetings with the planning",
    ),
    "heat-pumps": (
        "air source heat pump",
        "compressor unit",
        "0.6 cubic metres",
    ),
    "ev-access": (
        "electric vehicle (ev) chargers",
        "electric vehicle chargers",
        "ev chargers",
    ),
}
PLACEHOLDER_TEXT_MARKERS = (
    "demo-ready ui only",
    "coming soon",
    "no backend is connected yet",
    "placeholder for now",
    "reserved for a light-touch partner message",
    "relevant planning partner placement",
    "designed for a mid-page sponsor",
    "useful planning-side resource",
    "fits a trusted checklist, comparison tool or specialist referral",
    "selected planning partner",
)
USER_FACING_INTERNAL_MARKERS = (
    "source footing",
    "template-like",
    "owner page",
    "owner pages",
    "live blocker",
    "single clearer handoff",
    "handoff page",
    "hand-off guide",
)
TRAILING_META_WORDS = {
    "a",
    "an",
    "and",
    "as",
    "at",
    "before",
    "by",
    "for",
    "from",
    "if",
    "in",
    "into",
    "is",
    "of",
    "on",
    "or",
    "that",
    "the",
    "to",
    "use",
    "where",
    "with",
    "your",
}
GUIDANCE_EMAIL = "guidance@ukplanningguide.co.uk"
GUIDANCE_FORM_ROUTE = "/personalised-planning-guidance/request/"
GUIDANCE_SUCCESS_ROUTE = "/personalised-planning-guidance/request/success/"
GUIDANCE_PAGE = OUTPUT_DIR / "personalised-planning-guidance" / "index.html"
GUIDANCE_REQUEST_PAGE = OUTPUT_DIR / "personalised-planning-guidance" / "request" / "index.html"
GUIDANCE_SUCCESS_PAGE = OUTPUT_DIR / "personalised-planning-guidance" / "request" / "success" / "index.html"
PRIVACY_PAGE = OUTPUT_DIR / "privacy" / "index.html"
GUIDANCE_REQUIRED_PAGE_MARKERS = (
    "personalised planning guidance",
    "what to send",
    "structured request form",
    "what you will get back",
    "what this can and cannot do",
    "privacy and enquiry use",
)
GUIDANCE_REQUIRED_LIMITATION_MARKERS = (
    "informational personalised guidance",
    "not formal legal, architectural, surveying or council advice",
    "site-specific or borderline cases may still need checking",
)
GUIDANCE_REQUIRED_PRIVACY_MARKERS = (
    "used to respond to your request",
    "anonymised themes may be used to improve guides, tools, faqs and site content",
    "identifiable case details are not published without permission",
    "does not sign you up to marketing emails",
)
GUIDANCE_FORBIDDEN_MARKERS = (
    "professional advice",
    "artificial intelligence",
    "openai",
)
GUIDANCE_FORM_LINK_PATTERN = re.compile(
    r'href="(/personalised-planning-guidance/request/)"',
    re.IGNORECASE,
)
GUIDANCE_MAILTO_PATTERN = re.compile(
    r'href="(mailto:guidance@ukplanningguide\.co\.uk[^"]*)"',
    re.IGNORECASE,
)
FIND_HELP_REQUIRED_FILES = [
    OUTPUT_DIR / "find-help" / "index.html",
    OUTPUT_DIR / "find-help" / "homeowners" / "index.html",
    OUTPUT_DIR / "find-help" / "homeowners" / "request" / "index.html",
    OUTPUT_DIR / "find-help" / "homeowners" / "request" / "success" / "index.html",
    OUTPUT_DIR / "find-help" / "specialists" / "index.html",
    OUTPUT_DIR / "find-help" / "specialists" / "apply" / "index.html",
    OUTPUT_DIR / "find-help" / "specialists" / "apply" / "success" / "index.html",
    OUTPUT_DIR / "find-help" / "how-it-works" / "index.html",
    OUTPUT_DIR / "find-help" / "trust" / "index.html",
]
FIND_HELP_PUBLIC_MARKERS = (
    "/find-help/",
    "/find-help/homeowners/",
    "/find-help/specialists/",
    "find help",
    "register interest",
    "register your project",
    "apply to join",
    "apply as a specialist",
)
FIND_HELP_REQUIRED_MARKERS = (
    "pre-launch",
    "staged",
    "curated",
)
FIND_HELP_FORBIDDEN_MARKERS = (
    "best deals",
    "top-rated",
    "top rated",
    "live quote marketplace",
    "instant quotes",
    "fake reviews",
)

CRITICAL_KEYWORDS = [
    "planning-permission",
    "permitted-development",
]

IMPORTANT_KEYWORDS = [
    "height-limits",
    "boundary-rules",
    "maximum-height",
    "distance-from-boundary",
]
INTERNAL_LINK_PATTERN = re.compile(
    r"<a\b[^>]*\bhref\s*=\s*(?:\"([^\"]+)\"|'([^']+)')",
    re.IGNORECASE,
)
CANONICAL_PATTERN = re.compile(
    r'<link rel="canonical" href="([^"]+)"',
    re.IGNORECASE,
)
TITLE_PATTERN = re.compile(
    r"<title>(.*?)</title>",
    re.IGNORECASE | re.DOTALL,
)
META_DESCRIPTION_PATTERN = re.compile(
    r'<meta\s+name="description"\s+content="([^"]*)"',
    re.IGNORECASE,
)
OFFICIAL_SOURCES_COUNT_PATTERN = re.compile(
    r'data-official-sources-count="(\d+)"',
    re.IGNORECASE,
)
LIVE_TOOL_MARKERS: dict[str, list[str]] = {
    "planning-decision-tool": [
        "planning-decision-shell-desktop",
        "planning-decision-shell-mobile",
        "renderPlanningDecisionMobileShell",
    ],
    "planning-rejection-risk-analyzer": [
        "decision-shell-desktop",
        "decision-shell-mobile",
        "renderResponsiveToolShellInto",
    ],
    "what-can-i-build-explorer": [
        "decision-shell-desktop",
        "decision-shell-mobile",
        "renderResponsiveToolShellInto",
    ],
}
RULE_TEXT_FIELDS = tuple(FIELD_KEYWORDS.keys())
LOCAL_RULE_PRIORITY_PROJECTS = {
    "garages",
    "hard-surfaces",
    "heat-pumps",
    "hmos",
    "solar-panels",
    "windows-and-doors",
}
LOCAL_SEARCH_OWNER_CHECKS = {
    "planning-permission-eastleigh": "authority",
    "planning-permission-hounslow": "authority",
    "planning-permission-watford": "authority",
    "hmo-article-4-tamworth": "project",
    "hmo-article-4-leicestershire": "project",
    "hmo-article-4-charnwood": "project",
    "hmo-article-4-stafford": "project",
    "article-4-harrow": "project",
    "southwark-conservation-areas": "scenario",
    "buckinghamshire-conservation-areas": "scenario",
    "dropped-kerb-stoke-on-trent": "project",
}
SOURCE_PROJECT_SLUGS = {project["slug"] for project in load_projects()}
SOURCE_SCENARIO_SLUGS = {scenario["slug"] for scenario in load_scenarios()}
SOURCE_COUNCILS = load_councils()
SOURCE_TOWN_COUNTRY_LOOKUP = {
    council["town_slug"]: council.get("country_slug", get_country_slug(county_slug))
    for county_slug, items in SOURCE_COUNCILS.items()
    for council in items
    if council.get("town_slug")
}
LOCAL_SEARCH_BY_SLUG = {item["slug"]: item for item in LOCAL_SEARCH_PAGES}
VALIDATION_MODES = {"full", "local", "links", "role-metadata", "content", "duplicate"}


def classify_page(url: str) -> str:
    critical_hits = sum(1 for keyword in CRITICAL_KEYWORDS if keyword in url)
    important_hits = sum(1 for keyword in IMPORTANT_KEYWORDS if keyword in url)

    if critical_hits + important_hits > 1:
        return "long_tail"
    if critical_hits == 1:
        return "critical"
    if important_hits == 1:
        return "important"
    return "long_tail"


def normalize(path: str) -> str:
    if not path:
        return ""

    clean = path.split("?", 1)[0].split("#", 1)[0].strip()
    if not clean.startswith("/"):
        clean = "/" + clean

    clean = clean.rstrip("/")
    return clean or "/"


def extract_links(html: str) -> list[str]:
    links: list[str] = []
    for match in INTERNAL_LINK_PATTERN.finditer(html):
        href = match.group(1) or match.group(2) or ""
        if href.startswith("/"):
            links.append(normalize(href))
    return links


def build_existing_url_set(pages: list[Path]) -> set[str]:
    urls: set[str] = set()

    for page in pages:
        relative = str(page.relative_to(OUTPUT_DIR)).replace("\\", "/")
        if relative.endswith("index.html"):
            relative = relative[:-10]
        urls.add(normalize("/" + relative))

    return urls


def expected_url_for_page(page: Path) -> str:
    relative = str(page.relative_to(OUTPUT_DIR)).replace("\\", "/")
    if relative.endswith("index.html"):
        relative = relative[:-10]
    return normalize("/" + relative)


def parse_canonical(html: str) -> str:
    match = CANONICAL_PATTERN.search(html or "")
    return (match.group(1).strip() if match else "")


def parse_title(html: str) -> str:
    match = TITLE_PATTERN.search(html or "")
    return (_normalize_text(unescape(match.group(1))) if match else "")


def parse_meta_description(html: str) -> str:
    match = META_DESCRIPTION_PATTERN.search(html or "")
    return (_normalize_text(unescape(match.group(1))) if match else "")


def _normalize_text(value: str) -> str:
    return " ".join(str(value or "").split()).strip()


def _visible_text(html: str) -> str:
    text = re.sub(r"<script\b[\s\S]*?</script>", " ", html or "", flags=re.IGNORECASE)
    text = re.sub(r"<style\b[\s\S]*?</style>", " ", text, flags=re.IGNORECASE)
    text = re.sub(r"<[^>]+>", " ", text)
    return _normalize_text(unescape(text))


def _slug_label(value: str) -> str:
    return str(value or "").replace("-", " ").title()


def _contains_any(text: str, markers: tuple[str, ...]) -> bool:
    lowered = str(text or "").lower()
    return any(marker in lowered for marker in markers)


def _local_search_page_path(slug: str) -> Path:
    return OUTPUT_DIR / "local-search" / slug / "index.html"


def _has_official_sources_block(html: str) -> bool:
    return 'data-official-sources="true"' in (html or "")


def _official_sources_count(html: str) -> int:
    match = OFFICIAL_SOURCES_COUNT_PATTERN.search(html or "")
    return int(match.group(1)) if match else 0


def _official_source_context_for_page(page: Path) -> OfficialSourceContext | None:
    parts = page.relative_to(OUTPUT_DIR).parts
    if not parts or parts[-1] != "index.html":
        return None

    if len(parts) == 5 and parts[0] in SOURCE_PROJECT_SLUGS:
        return OfficialSourceContext(
            page_family="project",
            authority_slug=parts[2],
            country_slug=SOURCE_TOWN_COUNTRY_LOOKUP.get(parts[2], ""),
            project_slug=parts[0],
            scenario_slug=parts[3],
        )

    if len(parts) == 4 and parts[0] in SOURCE_PROJECT_SLUGS:
        return OfficialSourceContext(
            page_family="project",
            authority_slug=parts[2],
            country_slug=SOURCE_TOWN_COUNTRY_LOOKUP.get(parts[2], ""),
            project_slug=parts[0],
        )

    if len(parts) == 3 and parts[0] == "councils":
        return OfficialSourceContext(
            page_family="council",
            authority_slug=parts[1],
            country_slug=SOURCE_TOWN_COUNTRY_LOOKUP.get(parts[1], ""),
        )

    if len(parts) == 3 and parts[0] in SOURCE_SCENARIO_SLUGS:
        return OfficialSourceContext(
            page_family="scenario",
            authority_slug=parts[1],
            country_slug=SOURCE_TOWN_COUNTRY_LOOKUP.get(parts[1], ""),
            scenario_slug=parts[0],
        )

    if len(parts) == 3 and parts[0] == "local-search":
        entry = LOCAL_SEARCH_BY_SLUG.get(parts[1])
        if not entry:
            return None
        return OfficialSourceContext(
            page_family="local-search",
            authority_slug=entry.get("council_slug") or entry.get("scenario_authority_slug") or entry["authority_slug"],
            country_slug=get_country_slug(entry["county_slug"]),
            project_slug=entry.get("project_slug", ""),
            scenario_slug=entry.get("scenario_slug", ""),
        )

    return None


def _route_section(href: str) -> str:
    clean = normalize_internal_href(href)
    if not clean:
        return ""
    return classify_url(f"{BASE_URL}{clean}")


def _extract_section_by_marker(html: str, marker: str) -> str:
    pattern = re.compile(rf"<section\b[^>]*{re.escape(marker)}[^>]*>[\s\S]*?</section>", re.IGNORECASE)
    match = pattern.search(html or "")
    return match.group(0) if match else ""


def _section_text(section_html: str) -> str:
    text = re.sub(r"<script\b[\s\S]*?</script>", " ", section_html or "", flags=re.IGNORECASE)
    text = re.sub(r"<style\b[\s\S]*?</style>", " ", text, flags=re.IGNORECASE)
    text = re.sub(r"<[^>]+>", " ", text)
    text = unescape(text)
    return " ".join(text.split()).strip().lower()


def _local_search_title_topic_marker(page: dict, authority_label: str) -> str:
    phrase = local_search_topic_phrase(page, authority_label).lower()
    authority_lower = authority_label.lower()
    for separator in (f" in {authority_lower}", f" across {authority_lower}"):
        if separator in phrase:
            return phrase.split(separator, 1)[0].strip()
    return phrase.strip()


def _normalize_duplicate_fingerprint(text: str, replacements: list[str]) -> str:
    normalized = str(text or "")
    for item in sorted({value.lower() for value in replacements if value}, key=len, reverse=True):
        normalized = normalized.replace(item, " ")
    normalized = re.sub(r"\b[a-z0-9-]{2,}\b", lambda match: match.group(0).replace("-", " "), normalized)
    normalized = re.sub(r"\s+", " ", normalized).strip()
    return normalized


def validate_duplicate_content(pages: list[Path]) -> None:
    print("=== DUPLICATE CONTENT AUDIT ===\n")

    councils = load_councils()
    projects = load_projects()
    scenario_slugs = {item["slug"] for item in load_scenarios()}
    project_slugs = {item["slug"] for item in projects}
    project_lookup = {
        item["slug"]: {
            "title": item.get("title", ""),
            "short_name": item.get("short_name", ""),
        }
        for item in projects
    }
    town_lookup = {
        council["town_slug"]: {
            "town_name": council["town_name"],
            "county_slug": county_slug,
            "county_name": council.get("county_name", county_slug.replace("-", " ").title()),
        }
        for county_slug, items in councils.items()
        for council in items
    }

    family_markers = {
        "scenario": ["situation-summary", "scenario-intro", "local-context", "decision-patterns"],
        "project": ["local-answer-box", "planning-process", "planning-examples"],
        "project-scenario": ["situation-summary", "scenario-intro", "local-context", "decision-patterns"],
    }
    fingerprints: dict[tuple[str, str, str], list[str]] = defaultdict(list)

    for page in pages:
        parts = page.relative_to(OUTPUT_DIR).parts
        family = ""
        replacements: list[str] = []

        if len(parts) == 3 and parts[0] in scenario_slugs and parts[2] == "index.html":
            family = "scenario"
            family_slug = parts[0]
            town = town_lookup.get(parts[1], {})
            replacements = [
                parts[0].replace("-", " "),
                parts[1].replace("-", " "),
                town.get("town_name", ""),
                town.get("county_name", ""),
            ]
        elif len(parts) == 4 and parts[0] in project_slugs and parts[3] == "index.html":
            family = "project"
            family_slug = parts[0]
            town = town_lookup.get(parts[2], {})
            project_title = project_lookup.get(parts[0], {}).get("title", "")
            project_short = project_lookup.get(parts[0], {}).get("short_name", "")
            replacements = [
                parts[0].replace("-", " "),
                parts[1].replace("-", " "),
                parts[2].replace("-", " "),
                town.get("town_name", ""),
                town.get("county_name", ""),
                project_title,
                project_short,
            ]
        elif len(parts) == 5 and parts[0] in project_slugs and parts[4] == "index.html":
            family = "project-scenario"
            family_slug = f"{parts[0]}:{parts[3]}"
            town = town_lookup.get(parts[2], {})
            project_title = project_lookup.get(parts[0], {}).get("title", "")
            project_short = project_lookup.get(parts[0], {}).get("short_name", "")
            replacements = [
                parts[0].replace("-", " "),
                parts[1].replace("-", " "),
                parts[2].replace("-", " "),
                parts[3].replace("-", " "),
                town.get("town_name", ""),
                town.get("county_name", ""),
                project_title,
                project_short,
            ]
        else:
            continue

        html = page.read_text(encoding="utf-8", errors="ignore")
        sections = [
            _section_text(_extract_section_by_marker(html, marker))
            for marker in family_markers[family]
        ]
        sections = [section for section in sections if len(section) > 80]
        if len(sections) < 2:
            continue

        fingerprint = _normalize_duplicate_fingerprint(" ".join(sections), replacements)
        if len(fingerprint) < 250:
            continue

        url = expected_url_for_page(page)
        fingerprints[(family, family_slug, fingerprint)].append(url)

    failures: list[str] = []
    for (family, family_slug, _), urls in fingerprints.items():
        if len(urls) > DUPLICATE_CLUSTER_FAILURE_THRESHOLD:
            failures.append(
                f"{family} pages within {family_slug} share the same normalized core content ({len(urls)} pages), e.g. {urls[0]}"
            )
        if len(failures) >= MAX_REPORTED_ERRORS:
            break

    if failures:
        print("Duplicate-content audit failures:")
        for error in failures:
            print(f" - {error}")
        raise RuntimeError("Duplicate content audit failed")

    print("Duplicate-content audit passed\n")


def _extract_hero_intro(html: str) -> str:
    match = re.search(r"<h1\b[^>]*>[\s\S]*?</h1>\s*<p>([\s\S]*?)</p>", html or "", re.IGNORECASE)
    return _section_text(match.group(1)) if match else ""


def _extract_guidance_cta(html: str) -> str:
    match = re.search(
        r"<section\b[^>]*personalised-guidance-cta[^>]*>[\s\S]*?</section>",
        html or "",
        re.IGNORECASE,
    )
    return _section_text(match.group(0)) if match else ""


def validate_family_repetition(pages: list[Path]) -> None:
    print("=== FAMILY REPETITION AUDIT ===\n")

    councils = load_councils()
    projects = load_projects()
    project_slugs = {item["slug"] for item in projects}
    scenario_slugs = {item["slug"] for item in load_scenarios()}
    project_titles = {item["slug"]: item.get("title", "") for item in projects}
    town_lookup = {
        council["town_slug"]: (
            council["town_name"],
            council.get("county_name", county_slug.replace("-", " ").title()),
        )
        for county_slug, items in councils.items()
        for council in items
    }

    fingerprints: dict[tuple[str, str, str], list[str]] = defaultdict(list)
    sampled_counts: defaultdict[tuple[str, str], int] = defaultdict(int)
    skipped_counts: defaultdict[tuple[str, str], int] = defaultdict(int)

    for page in pages:
        parts = page.relative_to(OUTPUT_DIR).parts
        family = ""
        family_key = ""
        replacements: list[str] = []

        if len(parts) == 4 and parts[0] in project_slugs and parts[3] == "index.html":
            family = "project"
            family_key = parts[0]
            town_name, county_name = town_lookup.get(parts[2], ("", ""))
            replacements = [
                parts[0].replace("-", " "),
                parts[1].replace("-", " "),
                parts[2].replace("-", " "),
                town_name,
                county_name,
                project_titles.get(parts[0], ""),
            ]
        elif len(parts) == 5 and parts[0] in project_slugs and parts[4] == "index.html":
            family = "project-scenario"
            family_key = f"{parts[0]}:{parts[3]}"
            town_name, county_name = town_lookup.get(parts[2], ("", ""))
            replacements = [
                parts[0].replace("-", " "),
                parts[1].replace("-", " "),
                parts[2].replace("-", " "),
                parts[3].replace("-", " "),
                town_name,
                county_name,
                project_titles.get(parts[0], ""),
            ]
        elif len(parts) == 3 and parts[0] in project_slugs and parts[2] == "index.html":
            family = "county-project"
            family_key = parts[0]
            replacements = [
                parts[0].replace("-", " "),
                parts[1].replace("-", " "),
                project_titles.get(parts[0], ""),
            ]
        elif len(parts) == 3 and parts[0] == "councils" and parts[2] == "index.html":
            family = "council"
            family_key = "councils"
            town_name, county_name = town_lookup.get(parts[1], ("", ""))
            replacements = [parts[1].replace("-", " "), town_name, county_name]
        elif len(parts) == 3 and parts[0] == "local-search" and parts[2] == "index.html":
            family = "local-search"
            family_key = "local-search"
            replacements = [parts[1].replace("-", " ")]
        elif len(parts) == 3 and parts[0] in scenario_slugs and parts[2] == "index.html":
            family = "scenario"
            family_key = parts[0]
            town_name, county_name = town_lookup.get(parts[1], ("", ""))
            replacements = [parts[0].replace("-", " "), parts[1].replace("-", " "), town_name, county_name]
        else:
            continue

        sample_key = (family, family_key)
        if sampled_counts[sample_key] >= FAMILY_REPETITION_SAMPLE_LIMIT:
            skipped_counts[sample_key] += 1
            continue
        sampled_counts[sample_key] += 1

        html = page.read_text(encoding="utf-8", errors="ignore")
        fingerprint = _normalize_duplicate_fingerprint(
            " ".join(
                item for item in (_extract_hero_intro(html), _extract_guidance_cta(html)) if item
            ),
            replacements,
        )
        if len(fingerprint) < 120:
            continue
        fingerprints[(family, family_key, fingerprint)].append(expected_url_for_page(page))

    failures: list[str] = []
    for (family, family_key, _), urls in fingerprints.items():
        if len(urls) > FAMILY_REPETITION_FAILURE_THRESHOLD:
            failures.append(
                f"{family} pages within {family_key} repeat the same normalized hero/CTA pattern ({len(urls)} pages), e.g. {urls[0]}"
            )
        if len(failures) >= MAX_REPORTED_ERRORS:
            break

    if failures:
        print("Family-repetition audit warnings:")
        for error in failures:
            print(f" - {error}")
        if skipped_counts:
            skipped_total = sum(skipped_counts.values())
            print(
                f"Sampled up to {FAMILY_REPETITION_SAMPLE_LIMIT} pages per family key; "
                f"skipped {skipped_total} pages after sampling."
            )
        print("Family-repetition audit completed with warnings\n")
        return

    if skipped_counts:
        skipped_total = sum(skipped_counts.values())
        print(
            f"Family-repetition audit sampled up to {FAMILY_REPETITION_SAMPLE_LIMIT} pages per family key; "
            f"skipped {skipped_total} pages after sampling."
        )
    print("Family-repetition audit passed\n")


def validate_placeholder_content(pages: list[Path]) -> None:
    print("=== PLACEHOLDER CONTENT AUDIT ===\n")

    failures: list[str] = []
    for page in pages:
        text = _visible_text(page.read_text(encoding="utf-8", errors="ignore")).lower()
        for marker in PLACEHOLDER_TEXT_MARKERS:
            if marker in text:
                failures.append(f"{page.relative_to(OUTPUT_DIR)} contains placeholder wording: {marker}")
                break
        if len(failures) >= MAX_REPORTED_ERRORS:
            break

    if failures:
        print("Placeholder-content failures:")
        for error in failures:
            print(f" - {error}")
        raise RuntimeError("Placeholder content audit failed")

    print("Placeholder content audit passed\n")


def validate_personalised_guidance_feature(pages: list[Path]) -> None:
    print("=== PERSONALISED GUIDANCE FEATURE AUDIT ===\n")

    errors: list[str] = []
    if not GUIDANCE_PAGE.exists():
        errors.append("Missing dedicated personalised planning guidance page")
    if not GUIDANCE_REQUEST_PAGE.exists():
        errors.append("Missing guided planning request page")
    if not GUIDANCE_SUCCESS_PAGE.exists():
        errors.append("Missing guidance request success page")
    if not PRIVACY_PAGE.exists():
        errors.append("Missing privacy notice page")

    if errors:
        print("Personalised guidance failures:")
        for error in errors:
            print(f" - {error}")
        raise RuntimeError("Personalised guidance audit failed")

    guidance_html = GUIDANCE_PAGE.read_text(encoding="utf-8", errors="ignore")
    guidance_text = _visible_text(guidance_html).lower()
    guidance_request_html = GUIDANCE_REQUEST_PAGE.read_text(encoding="utf-8", errors="ignore")
    guidance_request_text = _visible_text(guidance_request_html).lower()
    guidance_success_html = GUIDANCE_SUCCESS_PAGE.read_text(encoding="utf-8", errors="ignore")
    guidance_success_text = _visible_text(guidance_success_html).lower()
    privacy_html = PRIVACY_PAGE.read_text(encoding="utf-8", errors="ignore")
    privacy_text = _visible_text(privacy_html).lower()
    homepage_path = OUTPUT_DIR / "index.html"
    homepage_html = homepage_path.read_text(encoding="utf-8", errors="ignore")

    for marker in GUIDANCE_REQUIRED_PAGE_MARKERS:
        if marker not in guidance_text:
            errors.append(f"Dedicated guidance page is missing required wording: {marker}")

    for marker in GUIDANCE_REQUIRED_LIMITATION_MARKERS:
        if marker not in guidance_text:
            errors.append(f"Dedicated guidance page is missing limitation wording: {marker}")

    for marker in GUIDANCE_REQUIRED_PRIVACY_MARKERS:
        if marker not in guidance_text and marker not in privacy_text:
            errors.append(f"Guidance feature is missing privacy wording: {marker}")

    if '/personalised-planning-guidance/' not in homepage_html:
        errors.append("Homepage is missing the personalised guidance promotion link")
    if GUIDANCE_FORM_ROUTE not in guidance_html:
        errors.append("Dedicated guidance page is missing the structured request-form link")
    if 'data-guidance-form="' not in guidance_html:
        errors.append("Dedicated guidance page is missing the structured guidance form markup")
    if 'data-static-submit="redirect"' not in guidance_html:
        errors.append("Dedicated guidance page lost the static form redirect handling")
    if 'action="/personalised-planning-guidance/request/success/"' not in guidance_html:
        errors.append("Dedicated guidance page has a form without the success redirect target")
    if 'meta name="robots" content="noindex, follow"' not in guidance_request_html.lower():
        errors.append("Guidance request page should be marked noindex")
    if 'meta name="robots" content="noindex, follow"' not in guidance_success_html.lower():
        errors.append("Guidance request success page should be marked noindex")
    if "submit a case-specific planning guidance request" not in guidance_request_text:
        errors.append("Guidance request page lost its submission framing")
    if "your planning guidance request has been captured" not in guidance_success_text:
        errors.append("Guidance request success page lost its confirmation wording")

    guidance_cta_pages: list[Path] = []
    project_cta_present = False
    local_search_cta_present = False
    faq_cta_present = False
    tool_cta_present = False
    methodology_cta_present = False

    project_slugs = {item["slug"] for item in load_projects()}

    for page in pages:
        html = page.read_text(encoding="utf-8", errors="ignore")
        cta_count = html.count('data-guidance-cta="')
        if cta_count:
            guidance_cta_pages.append(page)
            if 'data-guidance-disclaimer="true"' not in html:
                errors.append(f"{page.relative_to(OUTPUT_DIR)} has a guidance CTA without disclaimer markup")
            if 'data-guidance-privacy="true"' not in html:
                errors.append(f"{page.relative_to(OUTPUT_DIR)} has a guidance CTA without privacy wording")
            form_links = GUIDANCE_FORM_LINK_PATTERN.findall(html)
            if not form_links:
                errors.append(f"{page.relative_to(OUTPUT_DIR)} has a guidance CTA without a request-form link")

            lowered = _visible_text(html).lower()
            for marker in GUIDANCE_FORBIDDEN_MARKERS:
                if marker in lowered:
                    errors.append(f"{page.relative_to(OUTPUT_DIR)} contains forbidden guidance wording: {marker}")
                    break

        expected_url = expected_url_for_page(page)
        if expected_url == "/personalised-planning-guidance":
            if cta_count < 2:
                errors.append("Dedicated guidance page should repeat the CTA at least twice")
        elif cta_count > 1:
            errors.append(f"{page.relative_to(OUTPUT_DIR)} repeats the guidance CTA more than once")

        parts = page.relative_to(OUTPUT_DIR).parts
        if cta_count and len(parts) == 4 and parts[0] in project_slugs and parts[3] == "index.html":
            project_cta_present = True
        if (
            cta_count
            and len(parts) >= 4
            and parts[0] in {"england", "scotland", "wales", "northern-ireland"}
            and parts[1] == "projects"
            and parts[-1] == "index.html"
        ):
            project_cta_present = True
        if cta_count and len(parts) == 3 and parts[0] == "local-search" and parts[2] == "index.html" and parts[1] != "index":
            local_search_cta_present = True
        if cta_count and len(parts) == 3 and parts[0] == "planning-faq" and parts[2] == "index.html":
            faq_cta_present = True
        if cta_count and (
            (len(parts) == 2 and parts[0] == "tools" and parts[1] == "index.html")
            or (len(parts) == 3 and parts[0] == "tools" and parts[2] == "index.html")
            or (
                len(parts) >= 3
                and parts[0] in {"england", "scotland", "wales", "northern-ireland"}
                and parts[1] == "tools"
                and parts[-1] == "index.html"
            )
        ):
            tool_cta_present = True
        if cta_count and expected_url == "/methodology":
            methodology_cta_present = True

        if len(errors) >= MAX_REPORTED_ERRORS:
            break

    if not guidance_cta_pages:
        errors.append("No reusable personalised guidance CTA blocks were generated")
    if not project_cta_present:
        errors.append("No project page contains the personalised guidance CTA")
    if not local_search_cta_present:
        errors.append("No local search page contains the personalised guidance CTA")
    if not faq_cta_present:
        errors.append("No FAQ page contains the personalised guidance CTA")
    if not tool_cta_present:
        errors.append("No tool page contains the personalised guidance CTA")
    if not methodology_cta_present:
        errors.append("The methodology page is missing the personalised guidance CTA")

    if errors:
        print("Personalised guidance failures:")
        for error in errors[:MAX_REPORTED_ERRORS]:
            print(f" - {error}")
        raise RuntimeError("Personalised guidance audit failed")

    print(f"[OK] Guidance CTA pages audited: {len(guidance_cta_pages)}")
    print("Personalised guidance audit passed\n")


def validate_find_help_feature(pages: list[Path]) -> None:
    print("=== FIND HELP FEATURE AUDIT ===\n")

    errors: list[str] = []
    existing_urls = build_existing_url_set([page for page in pages if page.suffix == ".html"])

    if FIND_HELP_ENABLED:
        for path in FIND_HELP_REQUIRED_FILES:
            if not path.exists():
                errors.append(f"Missing Find Help page: {path.relative_to(OUTPUT_DIR)}")

        if errors:
            print("Find Help failures:")
            for error in errors[:MAX_REPORTED_ERRORS]:
                print(f" - {error}")
            raise RuntimeError("Find Help audit failed")

        hub_text = _visible_text((OUTPUT_DIR / "find-help" / "index.html").read_text(encoding="utf-8", errors="ignore")).lower()
        homeowners_html = (OUTPUT_DIR / "find-help" / "homeowners" / "request" / "index.html").read_text(encoding="utf-8", errors="ignore")
        specialists_html = (OUTPUT_DIR / "find-help" / "specialists" / "apply" / "index.html").read_text(encoding="utf-8", errors="ignore")
        homeowner_success_html = (OUTPUT_DIR / "find-help" / "homeowners" / "request" / "success" / "index.html").read_text(encoding="utf-8", errors="ignore")
        specialist_success_html = (OUTPUT_DIR / "find-help" / "specialists" / "apply" / "success" / "index.html").read_text(encoding="utf-8", errors="ignore")
        homeowner_success_text = _visible_text((OUTPUT_DIR / "find-help" / "homeowners" / "request" / "success" / "index.html").read_text(encoding="utf-8", errors="ignore")).lower()
        specialist_success_text = _visible_text((OUTPUT_DIR / "find-help" / "specialists" / "apply" / "success" / "index.html").read_text(encoding="utf-8", errors="ignore")).lower()
        trust_text = _visible_text((OUTPUT_DIR / "find-help" / "trust" / "index.html").read_text(encoding="utf-8", errors="ignore")).lower()

        for marker in FIND_HELP_REQUIRED_MARKERS:
            if marker not in hub_text:
                errors.append(f"Find Help hub is missing rollout wording: {marker}")

        for route in FIND_HELP_ROUTES:
            if normalize(route) not in existing_urls:
                errors.append(f"Find Help route missing from generated URL set: {route}")

        homeowner_field_names = [
            "name",
            "email",
            "phone",
            "postcode",
            "town_or_city",
            "project_type",
            "project_stage",
            "help_needed",
            "planning_route",
            "special_constraints",
            "budget_band",
            "preferred_timing",
            "notes",
        ]
        for field_name in homeowner_field_names:
            if f'name="{field_name}"' not in homeowners_html:
                errors.append(f"Homeowner request form is missing field {field_name}")

        specialist_field_names = [
            "full_name",
            "company_name",
            "email",
            "phone",
            "website",
            "specialist_type",
            "areas_covered",
            "years_operating",
            "services_offered",
            "project_types_handled",
            "recent_examples",
            "insurance_confirmation",
            "pricing_approach",
            "fit_statement",
        ]
        for field_name in specialist_field_names:
            if f'name="{field_name}"' not in specialists_html:
                errors.append(f"Specialist application form is missing field {field_name}")

        if 'action="/find-help/homeowners/request/success/"' not in homeowners_html:
            errors.append("Homeowner request form action is missing or incorrect")
        if 'action="/find-help/specialists/apply/success/"' not in specialists_html:
            errors.append("Specialist apply form action is missing or incorrect")
        if 'method="post"' not in homeowners_html or 'method="get"' in homeowners_html:
            errors.append("Homeowner request form must avoid GET submissions")
        if 'method="post"' not in specialists_html or 'method="get"' in specialists_html:
            errors.append("Specialist application form must avoid GET submissions")
        if 'data-static-submit="redirect"' not in homeowners_html:
            errors.append("Homeowner request form lost the static redirect submit handler")
        if 'data-static-submit="redirect"' not in specialists_html:
            errors.append("Specialist application form lost the static redirect submit handler")
        if "not used to sign you up to marketing emails" not in _visible_text(homeowners_html).lower():
            errors.append("Homeowner request form is missing privacy and enquiry-use wording")
        if "not used to sign you up to marketing emails" not in _visible_text(specialists_html).lower():
            errors.append("Specialist application form is missing privacy and enquiry-use wording")
        if "<!-- TODO:" in homeowners_html or "<!-- TODO:" in specialists_html:
            errors.append("Find Help forms are still shipping public TODO comments")

        if "may be contacted once relevant coverage is available" not in homeowner_success_text:
            errors.append("Homeowner success page lost staged follow-up wording")
        if "only selected applicants may be contacted" not in specialist_success_text:
            errors.append("Specialist success page lost manual review wording")
        if 'meta name="robots" content="noindex, follow"' not in homeowner_success_html.lower():
            errors.append("Homeowner success page should be marked noindex")
        if 'meta name="robots" content="noindex, follow"' not in specialist_success_html.lower():
            errors.append("Specialist success page should be marked noindex")

        sitemap_text = "\n".join(
            path.read_text(encoding="utf-8", errors="ignore")
            for path in sorted(SITEMAP_DIR.glob("*.xml"))
        ).lower()
        if "https://ukplanningguide.co.uk/find-help/homeowners/request/success/" in sitemap_text:
            errors.append("Homeowner success page leaked into the sitemap")
        if "https://ukplanningguide.co.uk/find-help/specialists/apply/success/" in sitemap_text:
            errors.append("Specialist success page leaked into the sitemap")

        for marker in (
            "small curated matches",
            "no hidden ranking tricks",
            "project fit over volume",
            "reviewed manually",
        ):
            if marker not in trust_text:
                errors.append(f"Find Help trust page is missing principle wording: {marker}")

        homepage_html = (OUTPUT_DIR / "index.html").read_text(encoding="utf-8", errors="ignore")
        if "/find-help/" not in homepage_html:
            errors.append("Homepage is missing the Find Help link or spotlight")

        project_cta_present = False
        faq_cta_present = False
        other_cta_count = 0

        project_slugs = {item["slug"] for item in load_projects()}
        for page in pages:
            html = page.read_text(encoding="utf-8", errors="ignore")
            if 'data-find-help-cta="true"' in html:
                other_cta_count += 1
                parts = page.relative_to(OUTPUT_DIR).parts
                if len(parts) == 4 and parts[0] in project_slugs and parts[3] == "index.html":
                    project_cta_present = True
                if len(parts) == 3 and parts[0] == "planning-faq" and parts[2] == "index.html" and parts[1] != "index":
                    faq_cta_present = True

                lowered = _visible_text(html).lower()
                for marker in FIND_HELP_FORBIDDEN_MARKERS:
                    if marker in lowered:
                        errors.append(f"{page.relative_to(OUTPUT_DIR)} contains forbidden Find Help wording: {marker}")
                        break

        if not project_cta_present:
            errors.append("No targeted project pages include the Find Help CTA")
        if not faq_cta_present:
            errors.append("No targeted FAQ pages include the Find Help CTA")
        if other_cta_count < 3:
            errors.append("Too few Find Help CTA placements were generated")

        if errors:
            print("Find Help failures:")
            for error in errors[:MAX_REPORTED_ERRORS]:
                print(f" - {error}")
            raise RuntimeError("Find Help audit failed")

        print(f"[OK] Find Help CTA pages audited: {other_cta_count}")
        print("Find Help audit passed\n")
        return

    generated_find_help_pages = [page for page in pages if "find-help" in page.relative_to(OUTPUT_DIR).parts]
    if generated_find_help_pages:
        for page in generated_find_help_pages[:MAX_REPORTED_ERRORS]:
            errors.append(f"Disabled Find Help page was generated: {page.relative_to(OUTPUT_DIR)}")

    for route in FIND_HELP_DRAFT_ROUTES:
        if normalize(route) in existing_urls:
            errors.append(f"Disabled Find Help route is still live in output: {route}")

    sitemap_text = "\n".join(
        path.read_text(encoding="utf-8", errors="ignore")
        for path in sorted(SITEMAP_DIR.glob("*.xml"))
    ).lower()
    for route in FIND_HELP_DRAFT_ROUTES:
        absolute_url = f"{BASE_URL}{route}".lower()
        if absolute_url in sitemap_text:
            errors.append(f"Disabled Find Help route leaked into the sitemap: {route}")

    flagged_pages = 0
    for page in pages:
        html = page.read_text(encoding="utf-8", errors="ignore")
        lowered = _visible_text(html).lower()
        for marker in FIND_HELP_PUBLIC_MARKERS:
            if marker in html.lower() or marker in lowered:
                errors.append(f"{page.relative_to(OUTPUT_DIR)} still contains disabled Find Help content: {marker}")
                flagged_pages += 1
                break
        if 'data-find-help-cta="true"' in html:
            errors.append(f"{page.relative_to(OUTPUT_DIR)} still contains a disabled Find Help CTA")
        if len(errors) >= MAX_REPORTED_ERRORS:
            break

    if errors:
        print("Find Help failures:")
        for error in errors[:MAX_REPORTED_ERRORS]:
            print(f" - {error}")
        raise RuntimeError("Find Help audit failed")

    print(f"[OK] Find Help is disabled and absent from {len(FIND_HELP_DRAFT_ROUTES)} routes")
    print("Find Help audit passed\n")


def validate_key_section_markers(pages: list[Path]) -> None:
    print("=== SECTION STRUCTURE AUDIT ===\n")

    project_slugs = {item["slug"] for item in load_projects()}
    scenario_slugs = {item["slug"] for item in load_scenarios()}
    failures: list[str] = []

    for page in pages:
        parts = page.relative_to(OUTPUT_DIR).parts
        html = page.read_text(encoding="utf-8", errors="ignore")
        required_markers: tuple[str, ...] = ()

        if len(parts) == 4 and parts[0] in project_slugs and parts[3] == "index.html":
            required_markers = ('id="quick-answer"', 'id="next-steps"', 'id="trust"')
        elif len(parts) == 5 and parts[0] in project_slugs and parts[4] == "index.html" and parts[3] in scenario_slugs:
            required_markers = ('id="scenario-summary"', 'id="scenario-next-steps"', 'id="scenario-trust"')
        elif len(parts) == 3 and parts[0] == "councils" and parts[2] == "index.html":
            required_markers = ('id="council-summary"', 'id="council-start"', 'id="council-process"', 'id="council-trust"')
        elif len(parts) == 3 and parts[0] == "planning-faq" and parts[2] == "index.html" and parts[1] != "index":
            required_markers = ('id="faq-summary"', 'id="faq-detail"', 'id="faq-trust"')
        elif len(parts) == 3 and parts[0] == "local-search" and parts[2] == "index.html" and parts[1] != "index":
            required_markers = ('id="local-search-answer"', 'id="local-search-routes"', 'id="local-search-verify"')

        for marker in required_markers:
            if marker not in html:
                failures.append(f"{page.relative_to(OUTPUT_DIR)} is missing required section marker {marker}")
                break
        if len(failures) >= MAX_REPORTED_ERRORS:
            break

    if failures:
        print("Section structure failures:")
        for error in failures:
            print(f" - {error}")
        raise RuntimeError("Section structure audit failed")

    print("Section structure audit passed\n")


def validate_rule_inventory() -> None:
    print("=== GENERATOR INPUT CHECK ===\n")

    projects = load_projects()
    councils = load_councils()
    errors: list[str] = []
    rule_root = Path(__file__).resolve().parent / "data" / "rules"

    if not projects:
        errors.append("No projects loaded from data/projects.json")
    if not councils:
        errors.append("No council datasets loaded from data/councils")

    expected_counties = len(councils)
    expected_local_entries = sum(len(items) for items in councils.values())

    seen_projects: set[str] = set()
    for project in projects:
        slug = project.get("slug", "")
        if not slug:
            errors.append("Project entry missing slug")
            continue
        if slug in seen_projects:
            errors.append(f"Duplicate project slug: {slug}")
        seen_projects.add(slug)

        national_path = rule_root / slug / "national.json"
        if not national_path.exists():
            errors.append(f"Missing national rule file for {slug}: {national_path}")

        if slug in LOCAL_RULE_PRIORITY_PROJECTS:
            county_files_present = 0
            local_entries_present = 0
            for county_slug in councils:
                county_path = rule_root / slug / f"{county_slug}.json"
                if not county_path.exists():
                    errors.append(f"Missing county rule file for {slug}: {county_path}")
                    continue
                county_files_present += 1
                try:
                    payload = json.loads(county_path.read_text(encoding="utf-8"))
                except (OSError, ValueError) as exc:
                    errors.append(f"Unreadable county rule file for {slug}: {county_path} ({exc})")
                    continue
                local_entries_present += len(payload.get("rules", []))

            if county_files_present != expected_counties:
                errors.append(
                    f"Incomplete county rule coverage for {slug}: {county_files_present}/{expected_counties} files present"
                )
            if local_entries_present < expected_local_entries:
                errors.append(
                    f"Incomplete local rule coverage for {slug}: {local_entries_present}/{expected_local_entries} local entries present"
                )

    if errors:
        print("Generator input failures:")
        for error in errors[:MAX_REPORTED_ERRORS]:
            print(f" - {error}")
        raise RuntimeError("Generator input audit failed")

    print(f"[OK] Projects loaded: {len(projects)}")
    print(f"[OK] Planning areas loaded: {len(councils)}\n")


def _collect_invalid_local_note_errors(container: dict, path_label: str) -> list[str]:
    errors: list[str] = []

    permitted = normalize_local_note(container.get("permitted_development", ""))
    if permitted and any(snippet in permitted.lower() for snippet in KNOWN_CONTAMINATED_SNIPPETS):
        errors.append(f"{path_label} -> permitted_development")

    rules = container.get("rules", {})
    if isinstance(rules, dict):
        for field in RULE_TEXT_FIELDS:
            text = normalize_local_note(rules.get(field, ""))
            if text and any(snippet in text.lower() for snippet in KNOWN_CONTAMINATED_SNIPPETS):
                errors.append(f"{path_label} -> rules.{field}")

    restrictions = container.get("restrictions", {})
    if isinstance(restrictions, dict):
        for field in ("conservation_area", "listed_building", "article4_notes"):
            text = normalize_local_note(restrictions.get(field, ""))
            if text and any(snippet in text.lower() for snippet in KNOWN_CONTAMINATED_SNIPPETS):
                errors.append(f"{path_label} -> restrictions.{field}")

    return errors


def _collect_cross_topic_rule_errors(container: dict, path_label: str, project_slug: str) -> list[str]:
    errors: list[str] = []

    def check(field_label: str, text: str) -> None:
        clean = normalize_local_note(text).lower()
        if not clean:
            return
        if any(marker in clean for marker in PROJECT_CROSS_TOPIC_MARKERS["all"]):
            errors.append(f"{path_label} -> {field_label} contains non-planning or boilerplate rule text")
        if project_slug != "heat-pumps" and any(
            marker in clean for marker in PROJECT_CROSS_TOPIC_MARKERS["heat-pumps"]
        ):
            errors.append(f"{path_label} -> {field_label} contains heat-pump text on a non-heat-pump rule file")
        if (
            project_slug not in {"driveways", "hard-surfaces", "dropped-kerbs"}
            and field_label.endswith("article4_notes")
            and any(marker in clean for marker in PROJECT_CROSS_TOPIC_MARKERS["ev-access"])
        ):
            errors.append(f"{path_label} -> {field_label} contains EV-charger text on an unrelated project rule file")

    check("permitted_development", container.get("permitted_development", ""))

    rules = container.get("rules", {})
    if isinstance(rules, dict):
        for field in RULE_TEXT_FIELDS:
            check(f"rules.{field}", rules.get(field, ""))

    restrictions = container.get("restrictions", {})
    if isinstance(restrictions, dict):
        for field in ("conservation_area", "listed_building", "article4_notes"):
            check(f"restrictions.{field}", restrictions.get(field, ""))

    return errors


def validate_local_rule_notes() -> None:
    print("=== LOCAL NOTE AUDIT ===\n")

    rule_root = Path(__file__).resolve().parent / "data" / "rules"
    errors: list[str] = []

    for county_path in sorted(rule_root.glob("*/*.json")):
        if county_path.name.startswith("national"):
            continue
        project_slug = county_path.parent.name

        try:
            payload = json.loads(county_path.read_text(encoding="utf-8"))
        except (OSError, ValueError) as exc:
            errors.append(f"{county_path.relative_to(rule_root)} unreadable ({exc})")
            if len(errors) >= MAX_REPORTED_ERRORS:
                break
            continue

        defaults = payload.get("defaults")
        if isinstance(defaults, dict):
            errors.extend(
                _collect_invalid_local_note_errors(defaults, f"{county_path.relative_to(rule_root)} defaults")
            )
            errors.extend(
                _collect_cross_topic_rule_errors(
                    defaults,
                    f"{county_path.relative_to(rule_root)} defaults",
                    project_slug,
                )
            )

        for index, entry in enumerate(payload.get("rules", []), start=1):
            if not isinstance(entry, dict):
                continue
            town_slug = entry.get("town_slug", f"entry-{index}")
            errors.extend(
                _collect_invalid_local_note_errors(
                    entry,
                    f"{county_path.relative_to(rule_root)} {town_slug}",
                )
            )
            errors.extend(
                _collect_cross_topic_rule_errors(
                    entry,
                    f"{county_path.relative_to(rule_root)} {town_slug}",
                    project_slug,
                )
            )
            if len(errors) >= MAX_REPORTED_ERRORS:
                break

        if len(errors) >= MAX_REPORTED_ERRORS:
            break

    if errors:
        print("Local note audit failures:")
        for error in errors[:MAX_REPORTED_ERRORS]:
            print(f" - {error}")
        raise RuntimeError("Local note audit failed")

    print("Local note audit passed\n")


def validate_known_contaminated_snippets_absent(pages: list[Path]) -> None:
    print("=== CONTAMINATED TEXT AUDIT ===\n")

    failures: list[str] = []
    for page in pages:
        html = page.read_text(encoding="utf-8", errors="ignore").lower()
        for snippet in KNOWN_CONTAMINATED_SNIPPETS:
            if snippet in html:
                failures.append(f"{page.relative_to(OUTPUT_DIR)} contains contaminated local-note text")
                break
        if len(failures) >= MAX_REPORTED_ERRORS:
            break

    if failures:
        print("Contaminated text failures:")
        for error in failures[:MAX_REPORTED_ERRORS]:
            print(f" - {error}")
        raise RuntimeError("Contaminated text audit failed")

    print("Contaminated text audit passed\n")


def validate_user_facing_copy_quality(pages: list[Path]) -> None:
    print("=== USER-FACING COPY QUALITY AUDIT ===\n")

    failures: list[str] = []
    for page in pages:
        html = page.read_text(encoding="utf-8", errors="ignore")
        visible_lower = _visible_text(html).lower()
        for marker in USER_FACING_INTERNAL_MARKERS:
            if marker in visible_lower:
                failures.append(f"{page.relative_to(OUTPUT_DIR)} contains internal wording: {marker}")
                break
        if len(failures) >= MAX_REPORTED_ERRORS:
            break

    if failures:
        print("User-facing copy quality failures:")
        for error in failures:
            print(f" - {error}")
        raise RuntimeError("User-facing copy quality audit failed")

    print("User-facing copy quality audit passed\n")


def validate_no_mojibake(pages: list[Path]) -> None:
    print("=== ENCODING ARTIFACT AUDIT ===\n")

    failures: list[str] = []
    for page in pages:
        html = page.read_text(encoding="utf-8", errors="ignore")
        visible_text = re.sub(r"<script[\s\S]*?</script>", " ", html, flags=re.IGNORECASE)
        visible_text = re.sub(r"<style[\s\S]*?</style>", " ", visible_text, flags=re.IGNORECASE)
        visible_text = re.sub(r"<[^>]+>", " ", visible_text)
        visible_text = " ".join(unescape(visible_text).split())
        if looks_mojibake(visible_text):
            failures.append(f"{page.relative_to(OUTPUT_DIR)} contains likely mojibake")
        if len(failures) >= MAX_REPORTED_ERRORS:
            break

    if failures:
        print("Encoding artifact failures:")
        for error in failures:
            print(f" - {error}")
        raise RuntimeError("Encoding artifact audit failed")

    print("Encoding artifact audit passed\n")


def pages_for_health_scan(pages: list[Path]) -> list[Path]:
    if os.environ.get("UKPG_FULL_HEALTH_SCAN", "").strip().lower() in {"1", "true", "yes"}:
        return [
            page
            for page in pages
            if page != OUTPUT_DIR / "404.html"
            and classify_url(f"{BASE_URL}{expected_url_for_page(page)}")
            not in {"scenario-combinations", "supplemental-scenarios"}
            and not is_legacy_country_bridge_path(expected_url_for_page(page))
        ]

    selected: list[Path] = []
    counts: defaultdict[tuple[str, str], int] = defaultdict(int)
    skipped = 0
    always_scan_sections = {
        "root",
        "tools",
        "england-tools",
        "england-tools-hub",
        "tools-hub",
        "faq",
        "faq-hub",
        "local-search",
        "local-search-hub",
        "building-regulations",
        "building-regulations-hub",
        "council",
        "council-hubs",
        "trust-pages",
        "misc-hubs",
        "area-hubs",
        "scenario-hubs",
        "projects",
    }

    for page in sorted(pages, key=lambda item: str(item.relative_to(OUTPUT_DIR))):
        if page == OUTPUT_DIR / "404.html":
            continue
        url = expected_url_for_page(page)
        if is_legacy_country_bridge_path(url):
            continue
        section = classify_url(f"{BASE_URL}{url}")
        if section in {"scenario-combinations", "supplemental-scenarios"}:
            continue
        if section in always_scan_sections:
            selected.append(page)
            continue
        key = _content_scan_key(page)
        if counts[key] >= MAX_HEALTH_SCAN_PAGES_PER_FAMILY_KEY:
            skipped += 1
            continue
        counts[key] += 1
        selected.append(page)
    if skipped:
        print(
            f"Health audits sampling {len(selected)}/{len(pages)} pages "
            f"(skipped {skipped} after family-key sampling). "
            "Set UKPG_FULL_HEALTH_SCAN=1 for a full health scan."
        )
    return selected


def _content_scan_key(page: Path) -> tuple[str, str]:
    parts = page.relative_to(OUTPUT_DIR).parts
    if not parts:
        return ("misc", "")
    if len(parts) >= 5:
        return (parts[0], parts[3])
    if len(parts) >= 4:
        return (parts[0], "project")
    if len(parts) >= 3:
        return (parts[0], parts[1])
    return (parts[0], "")


def pages_for_content_scan(pages: list[Path]) -> list[Path]:
    selected: list[Path] = []
    counts: defaultdict[tuple[str, str], int] = defaultdict(int)
    skipped = 0

    for page in sorted(pages, key=lambda item: str(item.relative_to(OUTPUT_DIR))):
        if is_legacy_country_bridge_path(expected_url_for_page(page)):
            continue
        section = classify_url(f"{BASE_URL}{expected_url_for_page(page)}")
        if section in {"root", "tools", "tools-hub", "england-tools", "england-tools-hub", "faq", "faq-hub", "local-search", "local-search-hub", "building-regulations", "building-regulations-hub", "council", "council-hubs", "trust-pages"}:
            selected.append(page)
            continue

        key = _content_scan_key(page)
        if counts[key] >= MAX_CONTENT_SCAN_PAGES_PER_FAMILY_KEY:
            skipped += 1
            continue

        counts[key] += 1
        selected.append(page)

    if skipped:
        print(
            f"Content audits sampling {len(selected)}/{len(pages)} pages "
            f"(skipped {skipped} after family-key sampling)."
        )
    return selected


def _print_validation_header(mode: str) -> None:
    print("\n=== VALIDATION REPORT ===\n")
    print(f"Mode: {mode}\n")


def _load_generated_pages() -> list[Path]:
    pages = list(OUTPUT_DIR.rglob("*.html"))
    print(f"Discovered {len(pages)} generated HTML pages.")
    return pages


def _local_search_targets() -> list[Path]:
    return [
        OUTPUT_DIR / "local-search" / page["slug"] / "index.html"
        for page in LOCAL_SEARCH_PAGES
    ]


def validate_recovery_targets() -> None:
    recovery_targets = [
        OUTPUT_DIR / "planning-permission" / "wandsworth" / "index.html",
        OUTPUT_DIR / "permitted-development" / "sevenoaks" / "index.html",
        OUTPUT_DIR / "height-limits" / "windsor-and-maidenhead" / "index.html",
        OUTPUT_DIR / "boundary-rules" / "dacorum" / "index.html",
        OUTPUT_DIR / "conservation-areas" / "wandsworth" / "index.html",
        OUTPUT_DIR / "planning-faq" / "planning-permission-vs-permitted-development" / "index.html",
        OUTPUT_DIR / "planning-faq" / "lawful-development-certificate-vs-planning-permission" / "index.html",
        OUTPUT_DIR / "planning-faq" / "prior-approval-vs-planning-permission" / "index.html",
        OUTPUT_DIR / "planning-faq" / "is-pre-application-advice-worth-it" / "index.html",
        OUTPUT_DIR / "planning-faq" / "what-drawings-do-i-need-for-planning-permission" / "index.html",
        OUTPUT_DIR / "planning-faq" / "can-neighbours-stop-planning-permission" / "index.html",
        OUTPUT_DIR / "planning-faq" / "what-happens-after-planning-permission-is-approved" / "index.html",
        OUTPUT_DIR / "planning-faq" / "what-happens-if-planning-permission-is-refused" / "index.html",
        OUTPUT_DIR / "planning-faq" / "does-an-extension-add-value-to-a-house" / "index.html",
        OUTPUT_DIR / "planning-faq" / "rear-extension-value-added" / "index.html",
        OUTPUT_DIR / "planning-faq" / "loft-conversion-value-added" / "index.html",
        OUTPUT_DIR / "planning-faq" / "two-storey-extension-value-added" / "index.html",
        OUTPUT_DIR / "planning-faq" / "extension-cost-vs-value-added" / "index.html",
        OUTPUT_DIR / "planning-faq" / "does-planning-permission-affect-property-value" / "index.html",
        OUTPUT_DIR / "planning-faq" / "side-extension-value-added" / "index.html",
        OUTPUT_DIR / "planning-faq" / "wraparound-extension-value-added" / "index.html",
        OUTPUT_DIR / "planning-faq" / "which-extension-adds-the-most-value" / "index.html",
        OUTPUT_DIR / "planning-faq" / "does-an-extra-bedroom-add-value" / "index.html",
        OUTPUT_DIR / "planning-faq" / "is-a-loft-conversion-worth-it" / "index.html",
    ] + _local_search_targets()

    missing_targets = [str(path.relative_to(OUTPUT_DIR)) for path in recovery_targets if not path.exists()]
    if missing_targets:
        raise RuntimeError(
            "Recovery audit failed: missing expected pages: "
            + ", ".join(missing_targets[:MAX_REPORTED_ERRORS])
        )


def _validation_context() -> tuple[list[Path], set[str], list[Path]]:
    pages = _load_generated_pages()
    validate_recovery_targets()
    existing_urls = build_existing_url_set(pages)
    validate_sitemaps(existing_urls)
    validate_local_search_inventory(existing_urls)
    validate_building_regulations_pages(existing_urls)
    validate_download_assets(existing_urls)
    health_pages = pages_for_health_scan(pages)
    if len(health_pages) > MAX_FULL_PAGE_HEALTH_SCAN:
        raise RuntimeError(
            f"Health scan skipped because {len(health_pages)} pages exceeds the configured cap "
            f"of {MAX_FULL_PAGE_HEALTH_SCAN}."
        )
    return pages, existing_urls, health_pages


def scan_canonicals_and_links(
    health_pages: list[Path],
    existing_urls: set[str],
) -> defaultdict[str, int]:
    print(f"Scanning {len(health_pages)} generated HTML pages for canonicals and internal links...")

    incoming_counts: defaultdict[str, int] = defaultdict(int)
    broken_links: list[str] = []
    stale_route_links: list[str] = []
    canonical_errors: list[str] = []

    for index, page in enumerate(health_pages, start=1):
        html = page.read_text(encoding="utf-8", errors="ignore")
        expected_url = expected_url_for_page(page)
        canonical = parse_canonical(html)
        canonical_path = "/" if expected_url == "/" else f"{expected_url}/"
        expected_canonical = f"{BASE_URL.rstrip('/')}{canonical_path}"

        if canonical != expected_canonical and len(canonical_errors) < MAX_REPORTED_ERRORS:
            canonical_errors.append(
                f"{page.relative_to(OUTPUT_DIR)} -> actual={canonical or 'missing'} expected={expected_canonical}"
            )

        for link in extract_links(html):
            if link in existing_urls:
                incoming_counts[link] += 1
                if not is_live_internal_href(link) and len(stale_route_links) < MAX_REPORTED_ERRORS:
                    stale_route_links.append(f"{page.relative_to(OUTPUT_DIR)} -> {link}")
            elif len(broken_links) < MAX_REPORTED_ERRORS:
                broken_links.append(f"{page.relative_to(OUTPUT_DIR)} -> {link}")

        if index % 5000 == 0 or index == len(health_pages):
            print(f"Validated {index}/{len(health_pages)} pages...")

    if canonical_errors:
        print("\nCanonical failures:")
        for error in canonical_errors:
            print(f" - {error}")
        raise RuntimeError("Canonical audit failed")

    if broken_links:
        print("\nBroken internal links:")
        for error in broken_links:
            print(f" - {error}")
        raise RuntimeError("Internal link audit failed")

    if stale_route_links:
        print("\nStale internal route references:")
        for error in stale_route_links:
            print(f" - {error}")
        raise RuntimeError("Stale route audit failed")

    return incoming_counts


def report_page_health(
    incoming_counts: defaultdict[str, int],
    existing_urls: set[str],
    health_pages: list[Path],
) -> None:
    critical: list[str] = []
    important: list[str] = []
    long_tail: list[str] = []

    for url in (expected_url_for_page(page) for page in health_pages):
        category = classify_page(url)
        if category == "critical":
            critical.append(url)
        elif category == "important":
            important.append(url)
        else:
            long_tail.append(url)

    def coverage(urls: list[str]) -> float:
        if not urls:
            return 0.0
        return sum(1 for url in urls if incoming_counts[url] > 0) / len(urls)

    critical_cov = coverage(critical)
    important_cov = coverage(important)
    long_tail_cov = coverage(long_tail)
    avg_links = sum(incoming_counts.values()) / len(existing_urls) if existing_urls else 0

    print("=== PAGE HEALTH ===\n")
    print(f"Critical pages coverage: {critical_cov * 100:.1f}%")
    print(f"Important pages coverage: {important_cov * 100:.1f}%")
    print(f"Long tail coverage: {long_tail_cov * 100:.1f}%")
    print(f"\nAverage incoming links per page: {avg_links:.2f}")

    if critical_cov > 0.9 and important_cov > 0.75:
        print("\nOverall health: HEALTHY")
    elif critical_cov > 0.75:
        print("\nOverall health: GOOD")
    else:
        print("\nOverall health: NEEDS IMPROVEMENT")

    weak_critical = [url for url in critical if incoming_counts[url] == 0][:10]
    if weak_critical:
        print("\nCritical pages with no internal links:")
        for url in weak_critical:
            print(f" - {url}")


def validate_sitemaps(existing_urls: set[str]) -> None:
    print("=== SITEMAP AUDIT ===\n")

    sitemap_index = OUTPUT_DIR / "sitemap.xml"
    if not sitemap_index.exists():
        raise RuntimeError("Missing sitemap index at output/sitemap.xml")

    namespace = {"sm": XML_NAMESPACE}
    root = ET.parse(sitemap_index).getroot()
    sitemap_urls = [
        node.text.strip()
        for node in root.findall("sm:sitemap/sm:loc", namespace)
        if node.text
    ]

    if not sitemap_urls:
        raise RuntimeError("Sitemap index does not contain any child sitemap files")

    errors: list[str] = []
    referenced = 0
    referenced_names: set[str] = set()
    referenced_urls: set[str] = set()

    legacy_root_children = sorted(
        item.name
        for item in OUTPUT_DIR.iterdir()
        if item.is_file() and LEGACY_ROOT_SITEMAP_NAME_PATTERN.fullmatch(item.name)
    )
    if legacy_root_children:
        errors.append(
            "Legacy root sitemap files still exist in output: "
            + ", ".join(legacy_root_children[:MAX_REPORTED_ERRORS])
        )

    if not SITEMAP_DIR.exists():
        errors.append("Missing sitemap child folder at output/sitemaps")
        print(f"Sitemap files: {len(sitemap_urls)}")
        print(f"Indexed sitemap URLs audited: {referenced}")
        print("\nSitemap audit failures:")
        for error in errors:
            print(f" - {error}")
        raise RuntimeError("Sitemap audit failed")

    actual_child_names = sorted(
        item.name
        for item in SITEMAP_DIR.iterdir()
        if item.is_file() and item.suffix.lower() == ".xml"
    )

    for filename in actual_child_names:
        if not CHILD_SITEMAP_NAME_PATTERN.fullmatch(filename):
            errors.append(f"Malformed sitemap child filename in output/sitemaps: {filename}")
            if len(errors) >= MAX_REPORTED_ERRORS:
                break

    for sitemap_url in sitemap_urls:
        if not sitemap_url.startswith(f"{BASE_URL}/sitemaps/"):
            errors.append(f"Sitemap index references malformed child path: {sitemap_url}")
            if len(errors) >= MAX_REPORTED_ERRORS:
                break
            continue
        filename = sitemap_url.rstrip("/").split("/")[-1]
        if not CHILD_SITEMAP_NAME_PATTERN.fullmatch(filename):
            errors.append(f"Sitemap index references malformed child filename: {filename}")
            if len(errors) >= MAX_REPORTED_ERRORS:
                break
            continue
        if filename in referenced_names:
            errors.append(f"Sitemap index references duplicate child sitemap: {filename}")
            if len(errors) >= MAX_REPORTED_ERRORS:
                break
            continue
        referenced_names.add(filename)
        sitemap_path = OUTPUT_DIR / "sitemaps" / filename
        if not sitemap_path.exists():
            errors.append(f"Sitemap index references missing file: {filename}")
            continue

        try:
            child_root = ET.parse(sitemap_path).getroot()
        except ET.ParseError as exc:
            errors.append(f"Unreadable child sitemap XML: {filename} ({exc})")
            continue

        child_urls = child_root.findall("sm:url/sm:loc", namespace)
        if not child_urls:
            errors.append(f"Sitemap child does not contain any URLs: {filename}")
            continue
        for loc in child_urls:
            if not loc.text:
                continue

            raw_url = loc.text.strip()
            if not raw_url.startswith(f"{BASE_URL}/") and raw_url != f"{BASE_URL}/":
                errors.append(f"Sitemap child contains malformed URL: {filename} -> {raw_url}")
                if len(errors) >= MAX_REPORTED_ERRORS:
                    break
                continue

            url = normalize(raw_url.replace(BASE_URL, ""))
            referenced += 1
            if url in referenced_urls:
                errors.append(f"Sitemap references duplicate page across children: {url}")
            referenced_urls.add(url)
            if url not in existing_urls:
                errors.append(f"Sitemap references non-existent page: {url}")
            elif not is_live_internal_href(url):
                errors.append(f"Sitemap references non-live route: {url}")
            section = classify_url(f"{BASE_URL}{url}")
            if section in {"scenario-combinations", "supplemental-scenarios"}:
                errors.append(f"Excluded section leaked into sitemap: {url}")

            if len(errors) >= MAX_REPORTED_ERRORS:
                break
        if len(errors) >= MAX_REPORTED_ERRORS:
            break

    orphaned_children = sorted(set(actual_child_names) - referenced_names)
    if orphaned_children and len(errors) < MAX_REPORTED_ERRORS:
        errors.append(
            "Orphaned sitemap child files not referenced by sitemap.xml: "
            + ", ".join(orphaned_children[:MAX_REPORTED_ERRORS])
        )

    print(f"Sitemap files: {len(sitemap_urls)}")
    print(f"Indexed sitemap URLs audited: {referenced}")

    if errors:
        print("\nSitemap audit failures:")
        for error in errors:
            print(f" - {error}")
        raise RuntimeError("Sitemap audit failed")

    print("Sitemap audit passed\n")


def _tool_page_path(slug: str) -> Path:
    return TOOLS_DIR / slug / "index.html"


def _find_tool_root_markers(html: str) -> list[str]:
    return re.findall(r'data-tool-root="([^"]+)"', html)


def _count_inline_scripts(html: str) -> int:
    return len(
        re.findall(
            r"<script(?![^>]*application/ld\+json)(?![^>]*\bsrc=)[^>]*>[\s\S]*?</script>",
            html,
            re.IGNORECASE,
        )
    )


def _duplicate_ids(html: str) -> list[str]:
    ids = re.findall(r'(?:^|[\s<])id="([^"]+)"', html)
    counts: defaultdict[str, int] = defaultdict(int)
    for item in ids:
        counts[item] += 1
    return sorted(item for item, count in counts.items() if count > 1)


def validate_tool_pages() -> None:
    print("=== TOOL AUDIT ===\n")

    tools = load_tools()
    index_page = TOOLS_DIR / "index.html"
    errors: list[str] = []

    if not index_page.exists():
        raise RuntimeError("Tools index was not generated at output/tools/index.html")

    index_html = index_page.read_text(encoding="utf-8", errors="ignore")
    seen_hrefs: set[str] = set()

    for tool in tools:
        slug = tool["slug"]
        href = tool.get("href", f"/tools/{slug}/")
        page_path = _tool_page_path(slug)

        if href in seen_hrefs:
            errors.append(f"Duplicate tool href on registry: {href}")
        seen_hrefs.add(href)

        if not page_path.exists():
            errors.append(f"Missing tool page: {page_path}")
            continue

        html = page_path.read_text(encoding="utf-8", errors="ignore")
        root_markers = _find_tool_root_markers(html)
        inline_scripts = _count_inline_scripts(html)
        duplicate_ids = _duplicate_ids(html)

        if href not in index_html:
            errors.append(f"Tools index is missing card link for {href}")

        if slug not in root_markers:
            errors.append(f"{slug}: missing interactive root marker data-tool-root=\"{slug}\"")

        if inline_scripts < 2:
            errors.append(f"{slug}: missing inline tool script (found {inline_scripts} inline scripts)")

        if duplicate_ids:
            errors.append(f"{slug}: duplicate ids detected: {', '.join(duplicate_ids)}")

        print(
            f"[OK] {slug}: page exists, root marker found, inline scripts={inline_scripts}"
        )

    if errors:
        print("\nTool audit failures:")
        for error in errors:
            print(f" - {error}")
        raise RuntimeError("Tool audit failed")

    print("\nTool audit passed\n")


def validate_curated_internal_routes() -> None:
    print("=== CURATED LINK AUDIT ===\n")

    errors: list[str] = []

    for key in FAQ_INDEX_NEXT_STEP_KEYS:
        href = PROMOTED_LINKS.get(key, {}).get("href", "")
        if href and not is_live_internal_href(href):
            errors.append(f"FAQ index promoted link is not live: {key} -> {href}")

    for faq in FAQS:
        for title, href, _description in faq.get("related_links", []):
            if href and not is_live_internal_href(href):
                errors.append(f"FAQ related link is not live: {faq['slug']} -> {title} ({href})")
            if len(errors) >= MAX_REPORTED_ERRORS:
                break
        if len(errors) >= MAX_REPORTED_ERRORS:
            break

    tools = load_tools()
    for tool in tools:
        for item in tool.get("guidance_links", []) + tool.get("faq_links", []):
            href = item.get("href", "")
            if href and not is_live_internal_href(href):
                errors.append(f"Tool link is not live: {tool['slug']} -> {href}")
            if len(errors) >= MAX_REPORTED_ERRORS:
                break
        if len(errors) >= MAX_REPORTED_ERRORS:
            break

    for page in LOCAL_SEARCH_PAGES:
        authority_href = f"/{page['authority_slug']}/" if page["target_scope"] == "county" else f"/councils/{page['authority_slug']}/"
        if not is_live_internal_href(authority_href):
            errors.append(f"Local search authority link is not live: {page['slug']} -> {authority_href}")
        if len(errors) >= MAX_REPORTED_ERRORS:
            break

    for tool_slug, config in CUSTOM_TOOL_CONFIGS.items():
        for item in config.get("links", []):
            href = item.get("href", "")
            if href and not is_live_internal_href(href):
                errors.append(f"Custom tool link is not live: {tool_slug} -> {href}")
            if len(errors) >= MAX_REPORTED_ERRORS:
                break
        if len(errors) >= MAX_REPORTED_ERRORS:
            break

        for question in config.get("questions", []):
            for option in question.get("options", []):
                for item in option.get("links_add", []):
                    href = item.get("href", "")
                    if href and not is_live_internal_href(href):
                        errors.append(
                            f"Custom tool option link is not live: {tool_slug}.{question.get('id', 'question')}[{option.get('value', '')}] -> {href}"
                        )
                    if len(errors) >= MAX_REPORTED_ERRORS:
                        break
                if len(errors) >= MAX_REPORTED_ERRORS:
                    break
            if len(errors) >= MAX_REPORTED_ERRORS:
                break

    if errors:
        print("Curated link audit failures:")
        for error in errors:
            print(f" - {error}")
        raise RuntimeError("Curated link audit failed")

    print("Curated link audit passed\n")


def validate_local_search_inventory(existing_urls: set[str]) -> None:
    print("=== LOCAL SEARCH AUDIT ===\n")

    councils = load_councils()
    council_slugs_by_county = {
        county_slug: {
            council["town_slug"]
            for council in items
            if council.get("town_slug")
        }
        for county_slug, items in councils.items()
    }
    all_council_slugs = {
        council_slug
        for council_slugs in council_slugs_by_county.values()
        for council_slug in council_slugs
    }

    errors: list[str] = []
    seen_slugs: set[str] = set()

    for page in LOCAL_SEARCH_PAGES:
        slug = str(page.get("slug", "")).strip()
        if not slug:
            errors.append("Local search entry missing slug")
            continue
        if slug in seen_slugs:
            errors.append(f"Duplicate local search slug: {slug}")
        seen_slugs.add(slug)

        county_slug = str(page.get("county_slug", "")).strip()
        authority_slug = str(page.get("authority_slug", "")).strip()
        council_slug = str(page.get("council_slug", "")).strip()
        target_scope = str(page.get("target_scope", "")).strip()
        project_scope = str(page.get("project_scope", "")).strip()
        scenario_authority_slug = str(page.get("scenario_authority_slug", "")).strip()
        owner = local_search_owner(page)

        if slug in LOCAL_SEARCH_OWNER_CHECKS and owner != LOCAL_SEARCH_OWNER_CHECKS[slug]:
            errors.append(
                f"Local search owner mismatch for {slug}: actual={owner} expected={LOCAL_SEARCH_OWNER_CHECKS[slug]}"
            )

        if county_slug not in council_slugs_by_county:
            errors.append(f"Local search page uses unknown county slug: {slug} -> {county_slug}")
            if len(errors) >= MAX_REPORTED_ERRORS:
                break
            continue

        if target_scope == "county":
            if authority_slug != county_slug:
                errors.append(
                    f"County local search page should point at its county entry page: {slug} -> authority={authority_slug} county={county_slug}"
                )
        elif target_scope == "council":
            if not council_slug:
                errors.append(f"Council local search page missing council_slug: {slug}")
            elif council_slug not in council_slugs_by_county[county_slug]:
                errors.append(f"Local search council slug is not valid for {county_slug}: {slug} -> {council_slug}")
            if authority_slug != council_slug:
                errors.append(
                    f"Council local search authority should match council_slug: {slug} -> authority={authority_slug} council={council_slug}"
                )
        else:
            errors.append(f"Local search page uses unsupported target_scope: {slug} -> {target_scope}")

        if project_scope not in {"county", "council"}:
            errors.append(f"Local search page uses unsupported project_scope: {slug} -> {project_scope}")

        if scenario_authority_slug and scenario_authority_slug not in all_council_slugs:
            errors.append(
                f"Local search page points scenario authority at an unknown live route: {slug} -> {scenario_authority_slug}"
            )

        authority_href = normalize_internal_href(local_search_authority_href(page))
        project_href = normalize_internal_href(local_search_project_href(page) or "")
        scenario_href = normalize_internal_href(local_search_scenario_href(page) or "")
        authority_link_target = normalize(authority_href)
        project_link_target = normalize(project_href)
        scenario_link_target = normalize(scenario_href)

        if not authority_href or not is_live_internal_href(authority_href):
            errors.append(f"Local search authority route is not live: {slug} -> {authority_href or 'missing'}")
        elif _route_section(authority_href) not in {"area-hubs", "council"}:
            errors.append(f"Local search authority route points at the wrong page type: {slug} -> {authority_href}")

        if project_href:
            if not is_live_internal_href(project_href):
                errors.append(f"Local search project route is not live: {slug} -> {project_href}")
            elif _route_section(project_href) not in {"county-projects", "council-projects"}:
                errors.append(f"Local search project route points at the wrong page type: {slug} -> {project_href}")

        if scenario_href:
            if not is_live_internal_href(scenario_href):
                errors.append(f"Local search scenario route is not live: {slug} -> {scenario_href}")
            elif _route_section(scenario_href) not in {"scenario-hubs", "scenario-pages"}:
                errors.append(f"Local search scenario route points at the wrong page type: {slug} -> {scenario_href}")

        if owner == "project":
            if not project_href:
                errors.append(f"Project-led local search page is missing a project owner route: {slug}")
            elif _route_section(project_href) not in {"county-projects", "council-projects"}:
                errors.append(f"Project-led local search page does not point at a project owner page: {slug} -> {project_href}")
        elif owner == "scenario":
            if not scenario_href:
                errors.append(f"Scenario-led local search page is missing a scenario owner route: {slug}")
            elif _route_section(scenario_href) != "scenario-pages":
                errors.append(f"Scenario-led local search page does not point at a scenario owner page: {slug} -> {scenario_href}")

        page_url = normalize(f"/local-search/{slug}")
        if page_url not in existing_urls:
            errors.append(f"Missing generated local search page: {page_url}")
            if len(errors) >= MAX_REPORTED_ERRORS:
                break
            continue

        page_path = _local_search_page_path(slug)
        if not page_path.exists():
            errors.append(f"Missing local search output file: {page_path.relative_to(OUTPUT_DIR)}")
            if len(errors) >= MAX_REPORTED_ERRORS:
                break
            continue

        html = page_path.read_text(encoding="utf-8", errors="ignore")
        title = parse_title(html)
        description = parse_meta_description(html)
        description_lower = description.lower()
        links = set(extract_links(html))
        has_custom_meta = bool(page.get("meta_title") or page.get("meta_description"))

        if not title:
            errors.append(f"Local search page is missing a title: {slug}")
        route_markers = ("entry page", "council route", "matching project", "project guide", "topic page")
        if has_custom_meta:
            answer_led_markers = (
                "check",
                "route",
                "local",
                "official",
                "project",
                "council",
                "article 4",
                "conservation",
                "permitted-development",
                "planning controls",
            )
            if not any(marker in description_lower for marker in answer_led_markers):
                errors.append(f"Local search custom metadata lost answer-led routing: {slug}")
        elif not any(marker in description_lower for marker in route_markers):
            errors.append(f"Local search metadata lost routing phrasing: {slug}")
        if "owner page" in description_lower:
            errors.append(f"Local search metadata sounds like an owner page: {slug}")
        next_step_marker = {
            "authority": "authority guide",
            "scenario": "topic page",
            "project": "project guide first",
        }[owner]

        if not has_custom_meta and next_step_marker not in description_lower:
            errors.append(f"Local search metadata lost its bridge routing cue: {slug}")

        authority_label = _slug_label(authority_slug)
        expected_entry_lead = local_search_entry_lead(page, authority_label).lower()
        if not has_custom_meta and expected_entry_lead[:35] not in description_lower:
            errors.append(f"Local search metadata no longer includes its entry-page framing: {slug}")

        title_lower = title.lower()
        if owner == "project":
            topic_marker = _local_search_title_topic_marker(page, authority_label)
            if f"{authority_label.lower()} planning" in title_lower:
                errors.append(f"Project-led local search title fell back to generic authority wording: {slug} -> {title}")
            if not has_custom_meta and topic_marker and topic_marker not in title_lower:
                errors.append(f"Project-led local search title lost its topic wording: {slug} -> {title}")
        elif owner == "scenario":
            topic_phrase = local_search_topic_phrase(page, authority_label).lower()
            if "conservation" not in title_lower and topic_phrase not in title_lower:
                errors.append(f"Scenario-led local search title lost its rule wording: {slug} -> {title}")
        elif owner == "authority" and not local_search_is_broad_authority_query(page):
            errors.append(f"Authority-led local search page no longer looks like a broad planning query: {slug}")

        if authority_link_target and authority_link_target not in links:
            errors.append(f"Local search page is missing its authority link: {slug} -> {authority_href}")
        if project_link_target and project_link_target not in links:
            errors.append(f"Local search page is missing its project link: {slug} -> {project_href}")
        if scenario_link_target and scenario_link_target not in links:
            errors.append(f"Local search page is missing its scenario link: {slug} -> {scenario_href}")

        primary_href = {
            "authority": authority_link_target,
            "project": project_link_target,
            "scenario": scenario_link_target,
        }[owner]
        if primary_href and primary_href not in links:
            errors.append(f"Local search page is missing its primary owner handoff: {slug} -> {primary_href}")

        if len(errors) >= MAX_REPORTED_ERRORS:
            break

    if errors:
        print("Local search audit failures:")
        for error in errors:
            print(f" - {error}")
        raise RuntimeError("Local search audit failed")

    print(f"[OK] Local search pages audited: {len(LOCAL_SEARCH_PAGES)}")
    print("Local search audit passed\n")


def validate_building_regulations_pages(existing_urls: set[str]) -> None:
    print("=== BUILDING REGULATIONS AUDIT ===\n")

    required_fields = {
        "slug",
        "title",
        "meta_title",
        "meta_description",
        "intent",
        "jurisdiction",
        "project_slug",
        "primary_questions",
        "answer_blocks",
        "official_sources",
        "related_routes",
    }
    errors: list[str] = []
    seen_slugs: set[str] = set()

    for page in BUILDING_REGULATIONS_PAGES:
        slug = str(page.get("slug", "")).strip()
        missing_fields = sorted(field for field in required_fields if field not in page)
        if missing_fields:
            errors.append(f"Building regulations page missing fields: {slug or 'missing-slug'} -> {', '.join(missing_fields)}")
            continue
        if not slug:
            errors.append("Building regulations page missing slug")
            continue
        if slug in seen_slugs:
            errors.append(f"Duplicate building regulations slug: {slug}")
        seen_slugs.add(slug)

        if page.get("jurisdiction") != "England":
            errors.append(f"Building regulations page is not England scoped: {slug}")

        url = normalize(building_regulations_path(page))
        if url not in existing_urls:
            errors.append(f"Missing generated building regulations page: {url}")
            continue

        output_parts = [part for part in url.strip("/").split("/") if part]
        page_path = OUTPUT_DIR.joinpath(*output_parts, "index.html")
        if not page_path.exists():
            errors.append(f"Missing building regulations output file: {url}")
            continue

        html = page_path.read_text(encoding="utf-8", errors="ignore")
        text = _visible_text(html).lower()
        links = {normalize(href) for href in extract_links(html)}
        title = parse_title(html)
        meta = parse_meta_description(html)

        if "england" not in text or "building regulations" not in text or "planning permission" not in text:
            errors.append(f"Building regulations page lost scope or approval-system wording: {slug}")
        if 'data-official-sources-family="building-regulations"' not in html:
            errors.append(f"Building regulations page missing official source block marker: {slug}")
        if html.count('class="official-source-link"') < 2:
            errors.append(f"Building regulations page has too few official source links: {slug}")
        if 'class="result-capture"' not in html:
            errors.append(f"Building regulations page missing result-capture block: {slug}")
        if len(title) > 72:
            errors.append(f"Building regulations title too long: {slug} -> {title}")
        if len(meta) > 160:
            errors.append(f"Building regulations meta too long: {slug} -> {meta}")

        for item in page.get("related_routes", []):
            href = normalize_internal_href(item.get("href", ""))
            if not href or not is_live_internal_href(href):
                errors.append(f"Building regulations related route is not live: {slug} -> {href or 'missing'}")
            elif normalize(href) not in links:
                errors.append(f"Building regulations page missing related route link: {slug} -> {href}")

        if len(errors) >= MAX_REPORTED_ERRORS:
            break

    if errors:
        print("Building regulations audit failures:")
        for error in errors[:MAX_REPORTED_ERRORS]:
            print(f" - {error}")
        raise RuntimeError("Building regulations audit failed")

    print(f"[OK] Building regulations pages audited: {len(BUILDING_REGULATIONS_PAGES)}")
    print("Building regulations audit passed\n")


def validate_download_assets(existing_urls: set[str]) -> None:
    print("=== DOWNLOAD ASSET AUDIT ===\n")

    errors: list[str] = []
    seen: set[str] = set()
    sitemap_urls = _load_sitemap_url_set()
    incoming_counts: defaultdict[str, int] = defaultdict(int)
    pages_to_scan: set[Path] = {OUTPUT_DIR / "downloads" / "index.html"}
    for asset in DOWNLOAD_ASSETS:
        for source_path in asset.get("source_pages", []):
            parts = [part for part in normalize(source_path).strip("/").split("/") if part]
            pages_to_scan.add(OUTPUT_DIR.joinpath(*parts, "index.html") if parts else OUTPUT_DIR / "index.html")

    for page in sorted(pages_to_scan):
        if not page.exists():
            continue
        html = page.read_text(encoding="utf-8", errors="ignore")
        for href in extract_links(html):
            incoming_counts[href] += 1
    required_fields = (
        "slug",
        "title",
        "meta_title",
        "meta_description",
        "summary",
        "last_checked",
        "official_sources",
        "checklist_sections",
        "related_tools",
        "related_guides",
        "cta_next_step",
    )

    if "/downloads" not in existing_urls:
        errors.append("Missing generated download assets index")

    for asset in DOWNLOAD_ASSETS:
        slug = str(asset.get("slug") or "").strip()
        missing = [field for field in required_fields if not asset.get(field)]
        if missing:
            errors.append(f"Download asset missing fields: {slug or 'missing-slug'} -> {', '.join(missing)}")
            continue
        if slug in seen:
            errors.append(f"Duplicate download asset slug: {slug}")
        seen.add(slug)

        route = download_asset_path(asset)
        route_key = normalize(route)
        url = f"{BASE_URL}{route}"
        page_path = OUTPUT_DIR / route.strip("/") / "index.html"
        if route_key not in existing_urls:
            errors.append(f"Missing generated download asset page: {url}")
            continue
        if route_key not in sitemap_urls:
            errors.append(f"Download asset missing from sitemap: {url}")
        if incoming_counts.get(route_key, 0) < 1:
            errors.append(f"Download asset has no internal links pointing to it: {route}")
        if not page_path.exists():
            errors.append(f"Missing download asset output file: {route}")
            continue

        html = page_path.read_text(encoding="utf-8", errors="ignore")
        visible = _visible_text(html).lower()
        links = {normalize(href) for href in extract_links(html)}
        word_count = len(re.findall(r"[a-zA-Z][a-zA-Z'-]+", visible))
        markers = {
            "canonical": f'<link rel="canonical" href="{url}">',
            "print control": 'data-download-action="print"',
            "copy-link control": 'data-download-action="copy-link"',
            "disclaimer": "general guidance",
            "official source block": 'data-download-official-sources="true"',
        }
        for label, marker in markers.items():
            if marker not in html and marker not in visible:
                errors.append(f"Download asset missing {label}: {slug}")
        if word_count < 600:
            errors.append(f"Download asset looks thin: {slug} ({word_count} words)")

        for collection_name in ("related_tools", "related_guides"):
            for item in asset.get(collection_name, []):
                href = item.get("path", "")
                normalized_href = normalize(href)
                if normalize(href) not in links:
                    errors.append(f"Download asset missing {collection_name} link: {slug} -> {href}")
                if href.startswith("/") and normalized_href not in existing_urls:
                    errors.append(f"Download asset related route is not live: {slug} -> {href}")

        if len(errors) >= MAX_REPORTED_ERRORS:
            break

    if len(seen) != len(DOWNLOAD_ASSETS):
        errors.append("Download asset registry has duplicate or skipped slugs")

    if errors:
        print("Download asset failures:")
        for error in errors[:MAX_REPORTED_ERRORS]:
            print(f" - {error}")
        raise RuntimeError("Download asset audit failed")

    print(f"[OK] Download assets audited: {len(DOWNLOAD_ASSETS)}")
    print("Download asset audit passed\n")


def validate_role_metadata(pages: list[Path]) -> None:
    print("=== ROLE METADATA AUDIT ===\n")

    errors: list[str] = []

    for page in pages:
        html = page.read_text(encoding="utf-8", errors="ignore")
        title = parse_title(html)
        description = parse_meta_description(html)
        url = expected_url_for_page(page)
        section = classify_url(f"{BASE_URL}{url}")
        combined = f"{title} {description}".lower()

        if not title:
            errors.append(f"Missing <title> on {page.relative_to(OUTPUT_DIR)}")
        if not description:
            errors.append(f"Missing meta description on {page.relative_to(OUTPUT_DIR)}")

        if section == "local-search" or url.startswith("/find-help"):
            continue

        if section in {"scenario-hubs", "projects", "county-projects", "council-hubs", "tools-hub", "faq-hub", "building-regulations-hub"}:
            if _contains_any(combined, ("where to start", "entry page", "owner page")):
                errors.append(f"Navigation layer uses owner or bridge metadata: {url}")
            if section == "scenario-hubs" and "hub" not in combined:
                errors.append(f"Scenario hub metadata stopped describing itself as a hub: {url}")
            if section == "projects" and not _contains_any(
                combined,
                ("planning permission", "planning rules", "local checks", "permitted development"),
            ):
                errors.append(f"Project hub metadata lost evergreen search framing: {url}")
            if section == "county-projects" and not _contains_any(combined, ("compare", "councils", "authorities")):
                errors.append(f"County project hub metadata lost comparison framing: {url}")
            if section == "council-hubs" and not _contains_any(combined, ("browse", "authorities", "councils")):
                errors.append(f"Council hub metadata lost navigation framing: {url}")
            if section == "building-regulations-hub" and not _contains_any(combined, ("building regulations", "building control", "approval")):
                errors.append(f"Building regulations hub metadata lost approval framing: {url}")
        elif section in {"area-hubs", "council"}:
            if _contains_any(combined, ("where to start", "owner page", " hub")):
                errors.append(f"Planning entry page is using the wrong role language: {url}")
            if section == "area-hubs" and not _contains_any(combined, ("entry page", "local authority", "councils")):
                errors.append(f"County page metadata lost entry-page framing: {url}")
            if section == "council" and not _contains_any(combined, ("council page", "planning entry page", "local routes")):
                errors.append(f"Council page metadata lost planning-entry framing: {url}")
        elif section in {"council-projects", "scenario-pages", "project-scenario-pages"}:
            if _contains_any(combined, ("where to start", "entry page")):
                errors.append(f"Owner page is using bridge metadata: {url}")
            if section == "council-projects" and not _contains_any(
                combined,
                ("planning rules", "local rules", "planning and highway checks", "check ", "see "),
            ):
                errors.append(f"Project owner page lost direct local-topic phrasing: {url}")
            if section in {"scenario-pages", "project-scenario-pages"} and not _contains_any(
                combined,
                ("planning rules", "local rules", "planning checks", "check ", "see "),
            ):
                errors.append(f"Scenario owner page lost direct local-topic phrasing: {url}")
        elif section == "building-regulations":
            if not _contains_any(combined, ("building regulations", "building control", "approval")):
                errors.append(f"Building regulations page lost approval framing: {url}")

        if len(errors) >= MAX_REPORTED_ERRORS:
            break

    if errors:
        print("Role metadata audit failures:")
        for error in errors:
            print(f" - {error}")
        raise RuntimeError("Role metadata audit failed")

    print("Role metadata audit passed\n")


def _metadata_family_for_url(url: str) -> str:
    country_contract = route_contract_for_country_path(url)
    if country_contract:
        if country_contract.intent_type == "projects" and country_contract.project_slug and country_contract.rule_slug:
            return f"{country_contract.country}:project:{country_contract.project_slug}:{country_contract.rule_slug}"
        if country_contract.intent_type == "projects" and country_contract.project_slug:
            return f"{country_contract.country}:project:{country_contract.project_slug}"
        if country_contract.intent_type == "rules" and country_contract.rule_slug:
            return f"{country_contract.country}:rule:{country_contract.rule_slug}"
        return f"{country_contract.country}:{country_contract.intent_type}"
    section = classify_url(f"{BASE_URL}{url}")
    parts = [part for part in url.strip("/").split("/") if part]
    if section == "project-scenario-pages" and len(parts) >= 4:
        return f"{parts[0]}:{parts[3]}"
    if section == "council-projects" and parts:
        return f"{parts[0]}:local-project"
    return section


ALLOWED_NOINDEX_SECTIONS = {
    "utility",
    "local-search-hub",
    "england-services",
    "england-services-hub",
}
ALLOWED_NOINDEX_PATHS = {
    "/homeproof/workspace/",
    "/updates/phase-0-integrity-repair/",
}


def _is_allowed_noindex(url: str, section: str) -> bool:
    """Return whether a rendered noindex is an explicit release-policy exclusion."""
    normalized_url = "/" if url == "/" else f"{url.rstrip('/')}/"
    declared_record = page_records_by_route().get(normalized_url)
    declared_noindex = bool(declared_record and declared_record.get("index_status") == "noindex")
    return declared_noindex or section in ALLOWED_NOINDEX_SECTIONS or normalized_url in ALLOWED_NOINDEX_PATHS


def validate_metadata_quality(pages: list[Path]) -> None:
    print("=== METADATA QUALITY AUDIT ===\n")

    errors: list[str] = []
    duplicate_titles: defaultdict[tuple[str, str], list[str]] = defaultdict(list)
    duplicate_metas: defaultdict[tuple[str, str], list[str]] = defaultdict(list)
    bland_title_markers = (
        "planning permission guidance for",
        "local route and next steps",
        "quick planning tool",
    )
    bland_meta_markers = (
        "planning permission guidance for",
        "use this page to understand",
        "the local route, the main tripwires and the next checks",
    )
    for page in pages:
        html = page.read_text(encoding="utf-8", errors="ignore")
        title = parse_title(html)
        meta = parse_meta_description(html)
        url = expected_url_for_page(page)
        if is_legacy_country_bridge_path(url):
            continue
        family = _metadata_family_for_url(url)
        section = classify_url(f"{BASE_URL}{url}")
        rel = str(page.relative_to(OUTPUT_DIR))
        title_lower = title.lower()
        meta_lower = meta.lower()

        if not title:
            errors.append(f"Missing title: {rel}")
        elif len(title) > 72:
            errors.append(f"Title too long ({len(title)}): {rel} -> {title}")
        elif _contains_any(title_lower, bland_title_markers):
            errors.append(f"Bland repeated title template: {rel} -> {title}")

        if not meta:
            errors.append(f"Missing meta description: {rel}")
        elif len(meta) > 160:
            errors.append(f"Meta description too long ({len(meta)}): {rel} -> {meta}")
        elif _contains_any(meta_lower, bland_meta_markers):
            errors.append(f"Bland repeated meta template: {rel} -> {meta}")
        elif meta and (
            meta.rstrip().endswith((",", ";", ":"))
            or re.sub(r"[^a-z0-9-]+$", "", meta.split()[-1].lower()) in TRAILING_META_WORDS
        ):
            errors.append(f"Meta description appears truncated: {rel} -> {meta}")

        if title:
            duplicate_titles[(family, title_lower)].append(rel)
        if meta:
            duplicate_metas[(family, meta_lower)].append(rel)

        if 'meta name="robots" content="noindex' in html.lower() and not _is_allowed_noindex(url, section):
            errors.append(f"Unexpected noindex on indexable page: {rel}")

        if len(errors) >= MAX_REPORTED_ERRORS:
            break

    for (family, title), rels in duplicate_titles.items():
        if len(rels) > 1 and family not in {"utility"}:
            errors.append(f"Duplicate title in {family}: {title} -> {', '.join(rels[:3])}")
        if len(errors) >= MAX_REPORTED_ERRORS:
            break

    duplicate_meta_warnings = [
        (family, meta, rels)
        for (family, meta), rels in duplicate_metas.items()
        if len(rels) > 3 and family not in {"utility"}
    ]

    if errors:
        print("Metadata quality failures:")
        for error in errors[:MAX_REPORTED_ERRORS]:
            print(f" - {error}")
        raise RuntimeError("Metadata quality audit failed")

    if duplicate_meta_warnings:
        print("Metadata duplicate warnings:")
        for family, meta, rels in duplicate_meta_warnings[:MAX_REPORTED_ERRORS]:
            print(f" - {family}: {meta[:90]} -> {', '.join(rels[:3])}")

    print("Metadata quality audit passed\n")


def validate_official_sources(pages: list[Path]) -> None:
    print("=== OFFICIAL SOURCES AUDIT ===\n")

    errors = validate_official_source_registry()
    coverage_gaps = official_source_coverage_gaps()

    checked_pages = 0
    for page in pages:
        context = _official_source_context_for_page(page)
        if context is None:
            continue

        checked_pages += 1
        html = page.read_text(encoding="utf-8", errors="ignore")
        has_block = _has_official_sources_block(html)
        expected_sources = relevant_official_sources(context)

        if has_block and _official_sources_count(html) < 1:
            errors.append(f"Rendered official source block is empty on {page.relative_to(OUTPUT_DIR)}")

        if has_block and 'class="official-source-link"' not in html:
            errors.append(f"Rendered official source block has no links on {page.relative_to(OUTPUT_DIR)}")

        if expected_sources and not has_block:
            errors.append(f"Missing official source block on {page.relative_to(OUTPUT_DIR)}")

        if len(errors) >= MAX_REPORTED_ERRORS:
            break

    if errors:
        print("Official source audit failures:")
        for error in errors[:MAX_REPORTED_ERRORS]:
            print(f" - {error}")
        raise RuntimeError("Official source audit failed")

    if coverage_gaps:
        sample = ", ".join(coverage_gaps[:10])
        suffix = " ..." if len(coverage_gaps) > 10 else ""
        print(
            f"[WARN] Authorities still relying on shared-only official sources: "
            f"{len(coverage_gaps)} ({sample}{suffix})"
        )

    print(f"[OK] Official source contexts audited: {checked_pages}")
    print("Official source audit passed\n")


def _repeated_long_sentences(text: str) -> list[str]:
    candidates = re.split(r"(?<=[.!?])\s+", text)
    fingerprints: defaultdict[str, int] = defaultdict(int)
    originals: dict[str, str] = {}
    for sentence in candidates:
        clean = _normalize_text(sentence)
        if len(clean) < 90:
            continue
        normalized = re.sub(r"[^a-z0-9\s]", "", clean.lower())
        normalized = re.sub(r"\s+", " ", normalized).strip()
        if len(normalized) < 80:
            continue
        fingerprints[normalized] += 1
        originals.setdefault(normalized, clean)
    return [originals[key] for key, count in fingerprints.items() if count > 1]


def validate_local_search_depth(existing_urls: set[str]) -> None:
    print("=== LOCAL SEARCH QUALITY AUDIT ===\n")

    errors: list[str] = []
    for page in LOCAL_SEARCH_PAGES:
        slug = page["slug"]
        page_url = normalize(f"/local-search/{slug}")
        if page_url not in existing_urls:
            errors.append(f"Missing generated local search page: {page_url}")
            continue

        page_path = _local_search_page_path(slug)
        html = page_path.read_text(encoding="utf-8", errors="ignore")
        text = _visible_text(html)
        route_card_count = html.count('<a class="card" href="')
        repeated = _repeated_long_sentences(text)

        if len(text.split()) < MIN_LOCAL_SEARCH_WORD_COUNT:
            errors.append(f"Local search page looks thin: {slug}")
        if route_card_count < 3:
            errors.append(f"Local search page has too few route cards: {slug}")
        if repeated:
            errors.append(f"Local search page repeats the same long sentence: {slug} -> {repeated[0][:100]}")
        if len(errors) >= MAX_REPORTED_ERRORS:
            break

    if errors:
        print("Local search quality failures:")
        for error in errors:
            print(f" - {error}")
        raise RuntimeError("Local search quality audit failed")

    print("Local search quality audit passed\n")


def validate_data_led_search_targets(existing_urls: set[str]) -> None:
    print("=== DATA-LED SEARCH TARGET AUDIT ===\n")

    errors: list[str] = []

    for slug in DATA_LED_LOCAL_SEARCH_SLUGS:
        page_url = normalize(f"/local-search/{slug}/")
        page_path = _local_search_page_path(slug)
        if page_url not in existing_urls or not page_path.exists():
            errors.append(f"Missing data-led local search target: {page_url}")
            continue

        html = page_path.read_text(encoding="utf-8", errors="ignore")
        text = _visible_text(html).lower()
        links = {normalize(href) for href in extract_links(html)}

        for marker in ('id="local-search-answer"', 'id="local-search-routes"', 'id="local-search-verify"'):
            if marker not in html:
                errors.append(f"Data-led search target lost answer module marker {marker}: {slug}")
                break

        page = LOCAL_SEARCH_BY_SLUG.get(slug, {})
        query = str(page.get("query", "")).lower()
        if "hmo" in query and "article 4" in query:
            if "hmo" not in text or "article 4" not in text:
                errors.append(f"HMO Article 4 page lost exact intent wording: {slug}")

            project_href = normalize(local_search_project_href(page) or "")
            scenario_href = normalize(local_search_scenario_href(page) or "")
            authority_href = normalize(local_search_authority_href(page))
            for href in (project_href, scenario_href, authority_href):
                if href and href not in links:
                    errors.append(f"HMO Article 4 local-search page lost route link: {slug} -> {href}")

        if len(errors) >= MAX_REPORTED_ERRORS:
            break

    for (county_slug, town_slug), route in HMO_ARTICLE_4_PRIORITY_ROUTES.items():
        project_path = OUTPUT_DIR / "hmos" / county_slug / town_slug / "index.html"
        project_url = normalize(f"/hmos/{county_slug}/{town_slug}/")
        if project_url not in existing_urls or not project_path.exists():
            errors.append(f"Missing HMO priority project page: {project_url}")
            continue

        html = project_path.read_text(encoding="utf-8", errors="ignore")
        links = {normalize(href) for href in extract_links(html)}
        required_links = {
            normalize(f"/local-search/{route['local_search_slug']}/"),
            normalize(f"/hmos/{county_slug}/{town_slug}/article-4/"),
            normalize(f"/hmos/{county_slug}/{town_slug}/planning-permission/"),
        }
        missing = sorted(required_links - links)
        if missing:
            errors.append(f"HMO priority project page lost data-led route links: {project_url} -> {', '.join(missing)}")

        if 'id="quick-answer"' not in html or 'id="popular-local-questions"' not in html:
            errors.append(f"HMO priority project page lost first-screen answer or demand links: {project_url}")

        if len(errors) >= MAX_REPORTED_ERRORS:
            break

    if errors:
        print("Data-led search target failures:")
        for error in errors[:MAX_REPORTED_ERRORS]:
            print(f" - {error}")
        raise RuntimeError("Data-led search target audit failed")

    print("Data-led search target audit passed\n")


def validate_gsc_expansion_targets(existing_urls: set[str]) -> None:
    print("=== SECOND-STAGE GSC EXPANSION AUDIT ===\n")

    errors: list[str] = []
    expansion_count = len(GSC_EXPANSION_LOCAL_SEARCH_SLUGS)
    min_pages = int(GSC_EXPANSION_RELEASE_LIMITS["min_pages"])
    max_pages = int(GSC_EXPANSION_RELEASE_LIMITS["max_pages"])
    expected_hub_clusters = {
        cluster
        for cluster, hub in GSC_CLUSTER_HUBS.items()
        if hub.get("publication_status") != "blocked"
    }

    if not min_pages <= expansion_count <= max_pages:
        errors.append(f"GSC expansion page count outside release cap: {expansion_count} not in {min_pages}-{max_pages}")
    missing_hub_clusters = sorted(expected_hub_clusters - set(GSC_CLUSTER_HUBS))
    if missing_hub_clusters:
        errors.append(f"GSC expansion hub clusters missing: {', '.join(missing_hub_clusters)}")
    if len(GSC_CLUSTER_HUB_SLUGS) != len(expected_hub_clusters):
        errors.append(
            "GSC expansion hub count changed: "
            f"expected {len(expected_hub_clusters)}, found {len(GSC_CLUSTER_HUB_SLUGS)}"
        )

    for slug in GSC_EXPANSION_LOCAL_SEARCH_SLUGS:
        page_url = normalize(f"/local-search/{slug}/")
        page_path = _local_search_page_path(slug)
        if page_url not in existing_urls or not page_path.exists():
            errors.append(f"Missing second-stage GSC expansion page: {page_url}")
            continue

        html = page_path.read_text(encoding="utf-8", errors="ignore")
        links = {normalize(href) for href in extract_links(html)}
        required_markers = (
            "gsc-answer-capsule",
            'data-gsc-cluster-links="true"',
            'data-guidance-query-bucket=',
            'data-guidance-route-family=',
            'id="local-search-routes"',
            'id="local-search-verify"',
        )
        for marker in required_markers:
            if marker not in html:
                errors.append(f"GSC expansion page missing marker {marker}: {slug}")
                break

        if slug in GSC_CLUSTER_HUB_SLUGS:
            related_links = [
                href
                for href in links
                if href.startswith("/local-search/") and href not in {page_url, "/local-search/"}
            ]
            if len(related_links) < 3:
                errors.append(f"GSC expansion hub has too few related local-search links: {slug}")

        if len(errors) >= MAX_REPORTED_ERRORS:
            break

    if errors:
        print("Second-stage GSC expansion failures:")
        for error in errors[:MAX_REPORTED_ERRORS]:
            print(f" - {error}")
        raise RuntimeError("Second-stage GSC expansion audit failed")

    print(f"Second-stage GSC expansion audit passed: {expansion_count} pages, {len(GSC_CLUSTER_HUB_SLUGS)} hubs\n")


def _load_sitemap_url_set() -> set[str]:
    sitemap_index = OUTPUT_DIR / "sitemap.xml"
    if not sitemap_index.exists():
        return set()

    namespace = {"sm": XML_NAMESPACE}
    urls: set[str] = set()
    root = ET.parse(sitemap_index).getroot()
    for sitemap_node in root.findall("sm:sitemap/sm:loc", namespace):
        sitemap_url = (sitemap_node.text or "").strip()
        filename = sitemap_url.rstrip("/").split("/")[-1]
        child_path = OUTPUT_DIR / "sitemaps" / filename
        if not child_path.exists():
            continue
        child_root = ET.parse(child_path).getroot()
        for loc_node in child_root.findall("sm:url/sm:loc", namespace):
            loc = (loc_node.text or "").strip()
            if loc.startswith(BASE_URL):
                urls.add(normalize(loc.replace(BASE_URL, "")))
    return urls


def validate_gsc_recovery_targets(existing_urls: set[str]) -> None:
    print("=== GSC RECOVERY TARGET AUDIT ===\n")

    errors: list[str] = []
    sitemap_urls = _load_sitemap_url_set()
    generic_markers = (
        "where to start",
        "owner page",
        "local route and next steps",
        "use this page to understand",
        "broad hub",
    )

    for route in GSC_RECOVERY_ROUTES:
        url = normalize(recovery_path(route))
        page_path = OUTPUT_DIR / url.strip("/") / "index.html"
        if url not in existing_urls or not page_path.exists():
            errors.append(f"Missing GSC recovery target: {url}")
            continue
        if url not in sitemap_urls:
            errors.append(f"GSC recovery target missing from sitemap: {url}")

        html = page_path.read_text(encoding="utf-8", errors="ignore")
        title = parse_title(html)
        meta = parse_meta_description(html)
        visible = _visible_text(html).lower()
        combined = f"{title} {meta}".lower()
        links = {normalize(href) for href in extract_links(html)}

        if 'meta name="robots" content="noindex' in html.lower():
            errors.append(f"GSC recovery target is unexpectedly noindex: {url}")
        if not title or not meta:
            errors.append(f"GSC recovery target lost title/meta: {url}")
        if any(marker in combined for marker in generic_markers):
            errors.append(f"GSC recovery target has generic bridge metadata: {url}")
        for marker in ("focused local guide", "what this query usually needs to settle", "deeper route options"):
            if marker not in visible:
                errors.append(f"GSC recovery target lost answer-led marker '{marker}': {url}")
                break

        required_links = {
            normalize(f"/{route['project_slug']}/{route['county_slug']}/{route['town_slug']}/"),
            normalize(f"/councils/{route['town_slug']}/"),
        }
        missing_links = sorted(link for link in required_links if link and link not in links)
        if missing_links:
            errors.append(f"GSC recovery target lost core internal links: {url} -> {', '.join(missing_links)}")

        if len(errors) >= MAX_REPORTED_ERRORS:
            break

    for path in GSC_RECOVERY_PATHS:
        if normalize(path) not in existing_urls:
            errors.append(f"Registry path does not resolve to generated output: {path}")
        if len(errors) >= MAX_REPORTED_ERRORS:
            break

    if errors:
        print("GSC recovery target failures:")
        for error in errors[:MAX_REPORTED_ERRORS]:
            print(f" - {error}")
        raise RuntimeError("GSC recovery target audit failed")

    print("GSC recovery target audit passed\n")


def _fetch_live_html(url: str) -> str:
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": "UKPlanningGuideValidator/1.0",
            "Accept": "text/html,application/xhtml+xml",
        },
    )
    with urllib.request.urlopen(request, timeout=20) as response:
        charset = response.headers.get_content_charset() or "utf-8"
        return response.read().decode(charset, errors="ignore")


def validate_live_tool_parity() -> None:
    print("=== LIVE TOOL PARITY ===\n")

    errors: list[str] = []
    checked = 0

    for slug, markers in LIVE_TOOL_MARKERS.items():
        page_path = _tool_page_path(slug)
        if not page_path.exists():
            errors.append(f"{slug}: local output page is missing, cannot compare against live site")
            continue

        local_html = page_path.read_text(encoding="utf-8", errors="ignore")
        expected_markers = [marker for marker in markers if marker in local_html]
        if not expected_markers:
            print(f"[SKIP] {slug}: no local parity markers found")
            continue

        live_url = f"{BASE_URL}/tools/{slug}/"
        try:
            live_html = _fetch_live_html(live_url)
        except urllib.error.URLError as exc:
            print(f"[WARN] Could not fetch {live_url}: {exc}")
            print("\nLive parity check skipped because the site could not be reached.\n")
            return

        missing = [marker for marker in expected_markers if marker not in live_html]
        checked += 1
        if missing:
            errors.append(
                f"{slug}: live page is missing current build markers: {', '.join(missing)}"
            )
        else:
            print(f"[OK] {slug}: live page matches current tool renderer markers")

    if errors:
        print("\nLive parity failures:")
        for error in errors:
            print(f" - {error}")
        raise RuntimeError("Live tool parity audit failed")

    if checked:
        print("\nLive tool parity passed\n")
    else:
        print("No live tool pages required parity checks\n")


def run_tool_smoke_test() -> None:
    if not TOOL_SMOKE_SCRIPT.exists():
        raise RuntimeError(f"Missing smoke test script: {TOOL_SMOKE_SCRIPT}")

    print("=== TOOL SMOKE TEST ===\n")
    subprocess.run(
        ["node", str(TOOL_SMOKE_SCRIPT)],
        cwd=str(Path(__file__).resolve().parent),
        check=True,
    )
    print("\nTool smoke test passed\n")


def validate_site(*, include_live_tool_parity: bool = True, include_tool_smoke: bool = True) -> None:
    validate_rule_inventory()
    validate_local_rule_notes()
    validate_curated_internal_routes()
    validate_tool_pages()
    if include_live_tool_parity:
        validate_live_tool_parity()
    if include_tool_smoke:
        run_tool_smoke_test()

    _, existing_urls, health_pages = _validation_context()
    incoming_counts = scan_canonicals_and_links(health_pages, existing_urls)
    content_pages = pages_for_content_scan(health_pages)

    validate_role_metadata(health_pages)
    validate_metadata_quality(health_pages)
    validate_no_mojibake(content_pages)
    validate_known_contaminated_snippets_absent(content_pages)
    validate_user_facing_copy_quality(content_pages)
    validate_official_sources(content_pages)
    validate_placeholder_content(content_pages)
    validate_personalised_guidance_feature(content_pages)
    validate_find_help_feature(content_pages)
    validate_key_section_markers(content_pages)
    validate_duplicate_content(content_pages)
    validate_family_repetition(content_pages)
    validate_local_search_depth(existing_urls)
    validate_data_led_search_targets(existing_urls)
    validate_gsc_expansion_targets(existing_urls)
    validate_gsc_recovery_targets(existing_urls)
    report_page_health(incoming_counts, existing_urls, health_pages)
    print("\nBUILD PASSED")


def validate_links_mode() -> None:
    _, existing_urls, health_pages = _validation_context()
    incoming_counts = scan_canonicals_and_links(health_pages, existing_urls)
    report_page_health(incoming_counts, existing_urls, health_pages)
    print("\nLINK VALIDATION PASSED")


def validate_role_metadata_mode() -> None:
    _, _, health_pages = _validation_context()
    validate_role_metadata(health_pages)
    validate_metadata_quality(health_pages)
    content_pages = pages_for_content_scan(health_pages)
    validate_no_mojibake(content_pages)
    validate_user_facing_copy_quality(content_pages)
    print("\nROLE METADATA PASSED")


def validate_content_mode() -> None:
    _, existing_urls, health_pages = _validation_context()
    content_pages = pages_for_content_scan(health_pages)
    validate_no_mojibake(content_pages)
    validate_known_contaminated_snippets_absent(content_pages)
    validate_user_facing_copy_quality(content_pages)
    validate_official_sources(content_pages)
    validate_placeholder_content(content_pages)
    validate_personalised_guidance_feature(content_pages)
    validate_find_help_feature(content_pages)
    validate_key_section_markers(content_pages)
    validate_duplicate_content(content_pages)
    validate_family_repetition(content_pages)
    validate_local_search_depth(existing_urls)
    validate_data_led_search_targets(existing_urls)
    validate_gsc_expansion_targets(existing_urls)
    validate_gsc_recovery_targets(existing_urls)
    print("\nCONTENT VALIDATION PASSED")


def _resolve_validation_mode(requested_mode: str | None = None) -> str:
    mode = (requested_mode or "").strip().lower()
    if not mode and VALIDATION_MODE_FILE.exists():
        mode = VALIDATION_MODE_FILE.read_text(encoding="utf-8").strip().lower()
    mode = mode or "full"
    if mode not in VALIDATION_MODES:
        raise RuntimeError(f"Unsupported validation mode: {mode}")
    return mode


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate generated UK Planning Guide output.")
    parser.add_argument(
        "--mode",
        choices=sorted(VALIDATION_MODES),
        help="Validation lane to run. Defaults to full unless .validate-mode is present.",
    )
    return parser.parse_args(argv)


def run_validation(*, mode: str | None = None) -> None:
    resolved_mode = _resolve_validation_mode(mode)
    _print_validation_header(resolved_mode)

    if resolved_mode == "duplicate":
        pages = _load_generated_pages()
        validate_duplicate_content(pages)
        return
    if resolved_mode == "local":
        validate_site(include_live_tool_parity=False, include_tool_smoke=True)
        return
    if resolved_mode == "links":
        validate_links_mode()
        return
    if resolved_mode == "role-metadata":
        validate_role_metadata_mode()
        return
    if resolved_mode == "content":
        validate_content_mode()
        return

    validate_site()


if __name__ == "__main__":
    args = parse_args()
    run_validation(mode=args.mode)
