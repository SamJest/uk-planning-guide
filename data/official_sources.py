from __future__ import annotations

from dataclasses import dataclass

from utils.text_cleaning import clean_display_text


SOURCE_CATEGORIES = (
    "planning_portal",
    "householder_guidance",
    "validation_requirements",
    "conservation_area",
    "listed_buildings",
    "article_4",
    "dropped_kerb_or_vehicle_access",
    "pre_application_advice",
    "local_plan",
    "design_guide",
    "enforcement",
    "trees",
    "heritage",
    "highways",
    "building_regulations",
    "building_control",
    "building_control_application",
    "approved_documents",
    "competent_person_scheme",
    "permitted_development_guidance",
    "other_official",
)

SOURCE_PAGE_FAMILIES = (
    "council",
    "project",
    "scenario",
    "local-search",
    "building-regulations",
)

SPECIAL_AUTHORITY_IDENTIFIERS = (
    "england",
    "wales",
    "scotland",
    "national",
)


@dataclass(frozen=True)
class OfficialSource:
    authority_slug: str
    title: str
    url: str
    category: str
    page_families: tuple[str, ...] = ()
    project_slugs: tuple[str, ...] = ()
    scenario_slugs: tuple[str, ...] = ()
    notes: str = ""
    last_reviewed: str = ""
    active: bool = True
    priority: int = 50


def _clean_sequence(values) -> tuple[str, ...]:
    if not isinstance(values, (list, tuple)):
        return ()
    return tuple(
        clean
        for clean in (str(value or "").strip() for value in values)
        if clean
    )


def normalize_source_entry(entry: dict | None) -> dict[str, object]:
    payload = dict(entry or {})
    priority = payload.get("priority", 50)
    if priority in ("", None):
        priority = 50

    return {
        "title": clean_display_text(payload.get("title", "")),
        "url": str(payload.get("url", "")).strip(),
        "category": str(payload.get("category", "")).strip(),
        "page_families": _clean_sequence(payload.get("page_families")),
        "project_slugs": _clean_sequence(payload.get("project_slugs")),
        "scenario_slugs": _clean_sequence(payload.get("scenario_slugs")),
        "notes": clean_display_text(payload.get("notes", "")),
        "last_reviewed": str(payload.get("last_reviewed") or payload.get("last_checked") or "").strip(),
        "active": bool(payload.get("active", True)),
        "priority": int(priority),
    }


def normalize_source_list(entries) -> tuple[dict[str, object], ...]:
    if not isinstance(entries, list):
        return ()
    return tuple(normalize_source_entry(entry) for entry in entries if isinstance(entry, dict))


def build_official_source(authority_slug: str, entry: dict | None) -> OfficialSource:
    normalized = normalize_source_entry(entry)
    return OfficialSource(
        authority_slug=str(authority_slug or "").strip(),
        title=str(normalized["title"]),
        url=str(normalized["url"]),
        category=str(normalized["category"]),
        page_families=tuple(normalized["page_families"]),
        project_slugs=tuple(normalized["project_slugs"]),
        scenario_slugs=tuple(normalized["scenario_slugs"]),
        notes=str(normalized["notes"]),
        last_reviewed=str(normalized["last_reviewed"]),
        active=bool(normalized["active"]),
        priority=int(normalized["priority"]),
    )
