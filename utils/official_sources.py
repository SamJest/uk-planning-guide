from __future__ import annotations

from dataclasses import dataclass
import re
from urllib.parse import urlparse

from data.loaders import load_councils, load_projects
from data.official_sources import (
    SOURCE_CATEGORIES,
    SOURCE_PAGE_FAMILIES,
    OfficialSource,
    build_official_source,
)
from data.scenario_data import SCENARIOS


PROJECTS = load_projects()
PROJECT_SLUGS = {project["slug"] for project in PROJECTS}
SCENARIO_SLUGS = {scenario["slug"] for scenario in SCENARIOS}
COUNCILS_BY_COUNTY = load_councils()
COUNCIL_LOOKUP = {
    council["town_slug"]: council
    for councils in COUNCILS_BY_COUNTY.values()
    for council in councils
    if council.get("town_slug")
}
LAST_REVIEWED_PATTERN = re.compile(r"^\d{4}-\d{2}(?:-\d{2})?$")

SOURCE_CATEGORY_LABELS = {
    "planning_portal": "Planning portal",
    "householder_guidance": "Householder guidance",
    "validation_requirements": "Validation requirements",
    "conservation_area": "Conservation areas",
    "listed_buildings": "Listed buildings",
    "article_4": "Article 4",
    "dropped_kerb_or_vehicle_access": "Dropped kerb or access",
    "pre_application_advice": "Pre-application advice",
    "local_plan": "Local plan",
    "design_guide": "Design guide",
    "enforcement": "Enforcement",
    "trees": "Trees",
    "heritage": "Heritage",
    "highways": "Highways",
    "building_regulations": "Building regulations",
    "building_control": "Building control",
    "building_control_application": "Building control application",
    "approved_documents": "Approved Documents",
    "competent_person_scheme": "Competent person scheme",
    "permitted_development_guidance": "Permitted development",
    "other_official": "Official guidance",
}

COUNCIL_CATEGORY_ORDER = [
    "planning_portal",
    "validation_requirements",
    "pre_application_advice",
    "local_plan",
    "design_guide",
    "conservation_area",
    "listed_buildings",
    "article_4",
    "heritage",
    "trees",
    "highways",
    "enforcement",
    "other_official",
]

BUILDING_REGULATIONS_CATEGORY_ORDER = [
    "building_regulations",
    "building_control",
    "building_control_application",
    "approved_documents",
    "competent_person_scheme",
    "householder_guidance",
    "planning_portal",
    "validation_requirements",
    "other_official",
]

DEFAULT_PROJECT_CATEGORY_ORDER = [
    "householder_guidance",
    "permitted_development_guidance",
    "planning_portal",
    "validation_requirements",
    "pre_application_advice",
    "conservation_area",
    "listed_buildings",
    "article_4",
    "heritage",
    "design_guide",
    "trees",
    "highways",
    "other_official",
]

PROJECT_CATEGORY_ORDERS = {
    "dropped-kerbs": [
        "dropped_kerb_or_vehicle_access",
        "highways",
        "planning_portal",
        "validation_requirements",
        "pre_application_advice",
        "householder_guidance",
        "other_official",
    ],
    "driveways": [
        "dropped_kerb_or_vehicle_access",
        "highways",
        "planning_portal",
        "validation_requirements",
        "pre_application_advice",
        "householder_guidance",
        "other_official",
    ],
    "hard-surfaces": [
        "dropped_kerb_or_vehicle_access",
        "highways",
        "planning_portal",
        "validation_requirements",
        "pre_application_advice",
        "householder_guidance",
        "other_official",
    ],
    "hmos": [
        "article_4",
        "local_plan",
        "planning_portal",
        "pre_application_advice",
        "validation_requirements",
        "householder_guidance",
        "other_official",
    ],
    "heat-pumps": [
        "permitted_development_guidance",
        "planning_portal",
        "pre_application_advice",
        "validation_requirements",
        "design_guide",
        "heritage",
        "other_official",
    ],
    "solar-panels": [
        "permitted_development_guidance",
        "planning_portal",
        "pre_application_advice",
        "validation_requirements",
        "design_guide",
        "heritage",
        "other_official",
    ],
    "windows-and-doors": [
        "householder_guidance",
        "permitted_development_guidance",
        "planning_portal",
        "conservation_area",
        "listed_buildings",
        "heritage",
        "validation_requirements",
        "pre_application_advice",
    ],
}

SCENARIO_CATEGORY_ORDERS = {
    "planning-permission": [
        "planning_portal",
        "validation_requirements",
        "pre_application_advice",
        "householder_guidance",
        "permitted_development_guidance",
        "local_plan",
        "other_official",
    ],
    "permitted-development": [
        "permitted_development_guidance",
        "householder_guidance",
        "planning_portal",
        "article_4",
        "conservation_area",
        "listed_buildings",
        "pre_application_advice",
    ],
    "conservation-areas": [
        "conservation_area",
        "heritage",
        "listed_buildings",
        "article_4",
        "planning_portal",
        "pre_application_advice",
    ],
    "listed-buildings": [
        "listed_buildings",
        "heritage",
        "planning_portal",
        "pre_application_advice",
        "validation_requirements",
    ],
    "article-4": [
        "article_4",
        "conservation_area",
        "local_plan",
        "planning_portal",
        "pre_application_advice",
        "permitted_development_guidance",
    ],
    "height-limits": [
        "householder_guidance",
        "permitted_development_guidance",
        "planning_portal",
        "design_guide",
        "pre_application_advice",
    ],
    "maximum-height": [
        "householder_guidance",
        "permitted_development_guidance",
        "planning_portal",
        "design_guide",
        "pre_application_advice",
    ],
    "depth-limits": [
        "householder_guidance",
        "permitted_development_guidance",
        "planning_portal",
        "design_guide",
        "pre_application_advice",
    ],
    "boundary-rules": [
        "householder_guidance",
        "permitted_development_guidance",
        "planning_portal",
        "design_guide",
        "pre_application_advice",
        "trees",
        "highways",
    ],
    "distance-from-boundary": [
        "householder_guidance",
        "permitted_development_guidance",
        "planning_portal",
        "design_guide",
        "pre_application_advice",
        "trees",
        "highways",
    ],
    "roof-alterations": [
        "householder_guidance",
        "permitted_development_guidance",
        "planning_portal",
        "conservation_area",
        "listed_buildings",
        "pre_application_advice",
    ],
}


@dataclass(frozen=True)
class OfficialSourceContext:
    page_family: str
    authority_slug: str
    country_slug: str = ""
    project_slug: str = ""
    scenario_slug: str = ""
    max_links: int = 5


_OFFICIAL_SOURCES_BY_AUTHORITY = {
    authority_slug: tuple(
        build_official_source(authority_slug, entry)
        for entry in council.get("all_official_sources", ())
    )
    for authority_slug, council in COUNCIL_LOOKUP.items()
}


def load_official_sources() -> tuple[OfficialSource, ...]:
    return tuple(
        source
        for sources in _OFFICIAL_SOURCES_BY_AUTHORITY.values()
        for source in sources
    )


def source_category_label(category: str) -> str:
    return SOURCE_CATEGORY_LABELS.get(category, "Official guidance")


def preferred_source_categories(context: OfficialSourceContext) -> list[str]:
    if context.page_family == "council":
        return list(COUNCIL_CATEGORY_ORDER)
    if context.page_family == "scenario":
        return list(SCENARIO_CATEGORY_ORDERS.get(context.scenario_slug, COUNCIL_CATEGORY_ORDER))
    if context.page_family == "project":
        return list(PROJECT_CATEGORY_ORDERS.get(context.project_slug, DEFAULT_PROJECT_CATEGORY_ORDER))
    if context.page_family == "local-search":
        categories: list[str] = []
        for group in (
            SCENARIO_CATEGORY_ORDERS.get(context.scenario_slug, []),
            PROJECT_CATEGORY_ORDERS.get(context.project_slug, DEFAULT_PROJECT_CATEGORY_ORDER),
            COUNCIL_CATEGORY_ORDER,
        ):
            for category in group:
                if category not in categories:
                    categories.append(category)
        return categories
    if context.page_family == "building-regulations":
        return list(BUILDING_REGULATIONS_CATEGORY_ORDER)
    return list(COUNCIL_CATEGORY_ORDER)


def _source_matches_context(source: OfficialSource, context: OfficialSourceContext) -> bool:
    if not source.active:
        return False
    if source.page_families and context.page_family not in source.page_families:
        return False
    if source.project_slugs and context.project_slug not in source.project_slugs:
        return False
    if source.scenario_slugs and context.scenario_slug not in source.scenario_slugs:
        return False
    return True


def relevant_official_sources(context: OfficialSourceContext) -> list[OfficialSource]:
    if context.page_family not in SOURCE_PAGE_FAMILIES:
        return []

    categories = preferred_source_categories(context)
    category_rank = {category: index for index, category in enumerate(categories)}
    candidates = [
        source
        for source in _OFFICIAL_SOURCES_BY_AUTHORITY.get(context.authority_slug, ())
        if _source_matches_context(source, context)
    ]

    candidates.sort(
        key=lambda source: (
            category_rank.get(source.category, len(category_rank) + 10),
            source.priority,
            source.title.lower(),
        )
    )

    selected: list[OfficialSource] = []
    seen_urls: set[str] = set()
    for source in candidates:
        if source.url in seen_urls:
            continue
        seen_urls.add(source.url)
        selected.append(source)
        if len(selected) >= max(1, min(5, int(context.max_links or 5))):
            break

    return selected


def official_source_coverage_gaps() -> list[str]:
    return sorted(
        authority_slug
        for authority_slug, council in COUNCIL_LOOKUP.items()
        if not council.get("official_sources")
    )


def validate_official_source_registry() -> list[str]:
    errors: list[str] = []

    for authority_slug, council in COUNCIL_LOOKUP.items():
        combined_sources = _OFFICIAL_SOURCES_BY_AUTHORITY.get(authority_slug, ())
        seen_urls: set[str] = set()

        if not combined_sources:
            errors.append(f"Authority has no official source coverage: {authority_slug}")
            continue

        for source in combined_sources:
            if not source.title:
                errors.append(f"Official source is missing title for authority {authority_slug}")

            parsed = urlparse(source.url)
            if parsed.scheme != "https" or not parsed.netloc:
                errors.append(f"Official source has malformed URL: {authority_slug} -> {source.url}")

            if source.category not in SOURCE_CATEGORIES:
                errors.append(f"Official source uses unknown category: {authority_slug} -> {source.category}")

            for family in source.page_families:
                if family not in SOURCE_PAGE_FAMILIES:
                    errors.append(f"Official source uses unknown page family: {authority_slug} -> {family}")

            for project_slug in source.project_slugs:
                if project_slug not in PROJECT_SLUGS:
                    errors.append(f"Official source uses unknown project slug: {authority_slug} -> {project_slug}")

            for scenario_slug in source.scenario_slugs:
                if scenario_slug not in SCENARIO_SLUGS:
                    errors.append(f"Official source uses unknown scenario slug: {authority_slug} -> {scenario_slug}")

            if source.last_reviewed and not LAST_REVIEWED_PATTERN.fullmatch(source.last_reviewed):
                errors.append(
                    f"Official source has invalid last_reviewed date: {authority_slug} -> {source.last_reviewed}"
                )

            if source.url in seen_urls:
                errors.append(f"Official source duplicates URL within authority {authority_slug}: {source.url}")
            seen_urls.add(source.url)

        if not council.get("official_sources") and not council.get("shared_official_sources"):
            errors.append(f"Authority is missing official source data: {authority_slug}")

    return errors
