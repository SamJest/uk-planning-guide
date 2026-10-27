import json
import re

from components.planning_helpers import first_text, restriction_messages, scenario_rule_excerpt
from data.search_demand_priorities import (
    metadata_override_for_local_search_slug,
    metadata_override_for_path,
)
from utils.local_note_validation import is_planning_local_note, normalize_local_note
from utils.country_utils import get_system_label
from utils.local_search_strategy import (
    local_search_entry_lead,
    local_search_focus_signal,
    local_search_is_broad_authority_query,
    local_search_next_step_phrase,
    local_search_owner,
    local_search_topic_phrase,
)


PROJECT_LABELS_BY_SLUG = {
    "side-extensions": "Side Extension",
    "dropped-kerbs": "Dropped Kerb",
    "garage-conversions": "Garage Conversion",
    "single-storey-extensions": "Single Storey Extension",
    "two-storey-extensions": "Two Storey Extension",
    "rear-extensions": "Rear Extension",
    "house-extensions": "House Extension",
    "wraparound-extensions": "Wraparound Extension",
    "fences-and-walls": "Fences and Walls",
    "windows-and-doors": "Windows and Doors",
    "agricultural-buildings": "Agricultural Building",
    "annexes": "Annexe",
    "basement-conversions": "Basement Conversion",
    "change-of-use": "Change Of Use",
    "demolition": "Demolition",
    "driveways": "Driveway",
    "garden-rooms": "Garden Room",
    "hard-surfaces": "Hard Surfacing",
    "heat-pumps": "Heat Pump",
    "hmos": "HMO",
    "loft-conversions": "Loft Conversion",
    "outbuildings": "Outbuilding",
    "porches": "Porch",
    "roof-lights": "Roof Light",
    "solar-panels": "Solar Panels",
    "temporary-buildings": "Temporary Building",
}


def _normalize_text(value) -> str:
    return normalize_local_note(value)


def _slug_from_label(value: str) -> str:
    clean = _normalize_text(value).lower()
    clean = re.sub(r"[^a-z0-9]+", "-", clean).strip("-")
    return clean


TRAILING_SNIPPET_WORDS = {
    "a",
    "an",
    "and",
    "are",
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
    "you",
    "your",
    "when",
    "with",
}


def _strip_trailing_snippet_words(text: str) -> str:
    clean = str(text or "").rstrip(" ,;:-")
    while clean:
        last_word = re.sub(r"[^a-z0-9-]+$", "", clean.split()[-1].lower())
        if last_word not in TRAILING_SNIPPET_WORDS:
            break
        clean = " ".join(clean.split()[:-1]).rstrip(" ,;:-")
    return clean


def _trim_text(text: str, limit: int) -> str:
    clean = _normalize_text(text)
    if len(clean) <= limit:
        return clean

    sentence_boundary = max(
        clean.rfind(". ", 0, limit),
        clean.rfind("! ", 0, limit),
        clean.rfind("? ", 0, limit),
    )
    if sentence_boundary >= int(limit * 0.6):
        return _strip_trailing_snippet_words(clean[: sentence_boundary + 1])

    clause_boundary = max(
        clean.rfind("; ", 0, limit),
        clean.rfind(": ", 0, limit),
        clean.rfind(", ", 0, limit),
    )
    if clause_boundary >= int(limit * 0.7):
        return _strip_trailing_snippet_words(clean[:clause_boundary])

    trimmed = _strip_trailing_snippet_words(clean[:limit].rsplit(" ", 1)[0])
    if len(trimmed.split()) >= 3:
        return trimmed

    fallback_clause = clean[:limit].rsplit(",", 1)[0].rstrip(" ,;:-")
    if len(fallback_clause.split()) >= 3:
        return _strip_trailing_snippet_words(fallback_clause)

    return trimmed


def _lead_text(value, limit: int = 110) -> str:
    clean = _normalize_text(value)
    if not clean:
        return ""

    parts = re.split(r"(?<=[.!?])\s+", clean, maxsplit=1)
    return _trim_text(parts[0], limit)


def _project_phrase(value: str) -> str:
    clean = _normalize_text(value)
    if not clean:
        return ""
    return clean if clean.isupper() else clean.lower()


def _is_usable_snippet(text: str) -> bool:
    clean = _normalize_text(text).lower()
    if not clean:
        return False
    if not is_planning_local_note(clean):
        return False
    return clean not in {
        "most householder development follows national permitted development rules unless local restrictions apply.",
        "most householder development follows national permitted development rules unless local restrictions apply",
        "householder development follows national permitted development rules unless local restrictions apply.",
        "householder development follows national permitted development rules unless local restrictions apply",
    }


def _restriction_summary(rule, limit: int = 2) -> str:
    labels = [label.lower() for label, _ in restriction_messages(rule)[:limit]]
    if not labels:
        return ""
    if len(labels) == 1:
        return labels[0]
    return f"{', '.join(labels[:-1])} and {labels[-1]}"


def _restriction_meta_phrase(restrictions: str) -> str:
    clean = _normalize_text(restrictions)
    if not clean:
        return "local restrictions"
    if len(clean) > 34:
        return "local restrictions"
    return clean


def _compose_description(*parts: str, limit: int = 155) -> str:
    text = " ".join(_normalize_text(part) for part in parts if _normalize_text(part))
    return _trim_text(text, limit)


def _project_scenario_description(
    project_phrase: str,
    scenario_title: str,
    town_name: str,
    scenario_slug: str,
    restrictions: str,
) -> str:
    restrictions_phrase = f"including {restrictions}, " if restrictions else ""
    descriptions = {
        "planning-permission": _compose_description(
            f"Check whether {project_phrase} in {town_name} is more likely to need planning permission,",
            f"{restrictions_phrase}the key local tripwires and the safest next check if the route is borderline.",
        ),
        "permitted-development": _compose_description(
            f"Check whether permitted development still covers {project_phrase} in {town_name},",
            f"{restrictions_phrase}the key local tripwires and what to verify next.",
        ),
        "height-limits": _compose_description(
            f"Check the height limits affecting {project_phrase} in {town_name},",
            f"{restrictions_phrase}the controlling measurements and the next check if height is the blocker.",
        ),
        "maximum-height": _compose_description(
            f"Check the maximum height rules affecting {project_phrase} in {town_name},",
            f"{restrictions_phrase}the controlling measurement point and what to verify next.",
        ),
        "depth-limits": _compose_description(
            f"Check the depth limits affecting {project_phrase} in {town_name},",
            f"{restrictions_phrase}the projection tripwires and the next check if the route is borderline.",
        ),
        "boundary-rules": _compose_description(
            f"Check boundary rules for {project_phrase} in {town_name},",
            f"{restrictions_phrase}siting tripwires and the next check if the answer is borderline.",
        ),
        "distance-from-boundary": _compose_description(
            f"Check the distance-from-boundary rules affecting {project_phrase} in {town_name},",
            f"{restrictions_phrase}clearance tripwires and what to verify next.",
        ),
        "roof-alterations": _compose_description(
            f"Check how roof alteration rules affect {project_phrase} in {town_name},",
            f"{restrictions_phrase}visibility tripwires and the next local check.",
        ),
        "conservation-areas": _compose_description(
            f"Check how conservation area rules affect {project_phrase} in {town_name},",
            f"{restrictions_phrase}heritage tripwires and the next local check before you rely on the broad answer.",
        ),
        "listed-buildings": _compose_description(
            f"Check how listed building controls affect {project_phrase} in {town_name},",
            f"{restrictions_phrase}heritage tripwires and the next formal check.",
        ),
        "article-4": _compose_description(
            f"Check whether Article 4 changes the route for {project_phrase} in {town_name},",
            f"{restrictions_phrase}the fallback risks and what to verify next.",
        ),
    }
    return descriptions.get(
        scenario_slug,
        _compose_description(
            f"Check how {scenario_title.lower()} affects {project_phrase} in {town_name},",
            f"{restrictions_phrase}the main tripwires and the next check if the answer is borderline.",
        ),
    )


SCENARIO_TITLE_LABELS = {
    "planning-permission": "planning permission",
    "permitted-development": "permitted development",
    "height-limits": "height limits",
    "maximum-height": "maximum height",
    "depth-limits": "depth limits",
    "boundary-rules": "boundary rules",
    "distance-from-boundary": "distance from boundary",
    "roof-alterations": "roof alteration rules",
    "conservation-areas": "conservation area checks",
    "listed-buildings": "listed building checks",
    "article-4": "Article 4 checks",
}


def _project_scenario_title(
    clean_project: str,
    scenario_title: str,
    town_name: str,
    scenario_slug: str,
    *,
    limit: int = 70,
) -> str:
    scenario_label = SCENARIO_TITLE_LABELS.get(scenario_slug, _normalize_text(scenario_title).lower())
    if scenario_slug == "planning-permission":
        title = f"{clean_project} planning permission in {town_name}"
        if len(_normalize_text(title)) > limit:
            title = f"{clean_project} permission in {town_name}"
        return _trim_text(title, limit)

    title = f"{clean_project} {scenario_label} in {town_name}"
    if len(_normalize_text(title)) > limit:
        title = f"{clean_project} {scenario_label}: {town_name}"
    return _trim_text(title, limit)


def _project_meta_focus(project_slug: str, project_phrase: str, town_name: str) -> tuple[str, str]:
    focus = {
        "fences-and-walls": (
            f"Check fence and wall rules in {town_name}.",
            "including height, highway-side position and the local checks most likely to change the answer.",
        ),
        "garden-rooms": (
            f"Check garden room rules in {town_name}.",
            "including height, siting, use and the next checks if the build is no longer clearly incidental.",
        ),
        "change-of-use": (
            f"Check change-of-use rules in {town_name}.",
            "including use class, local policy and the neighbour-impact issues most likely to decide the route.",
        ),
        "dropped-kerbs": (
            f"Check dropped kerb rules in {town_name}.",
            "including planning permission, highway approval and the access checks most likely to matter next.",
        ),
        "house-extensions": (
            f"Check house extension rules in {town_name}.",
            "including scale, local restrictions and the next checks before you rely on the simpler route.",
        ),
        "annexes": (
            f"Check annexe rules in {town_name}.",
            "including ancillary use, scale and the local checks that decide whether it still reads as part of the main house.",
        ),
        "outbuildings": (
            f"Check outbuilding rules in {town_name}.",
            "including height, siting, use and the local restrictions most likely to change the route.",
        ),
        "driveways": (
            f"Check driveway rules in {town_name}.",
            "including drainage, frontage treatment and whether dropped-kerb approval is part of the route.",
        ),
        "porches": (
            f"Check porch rules in {town_name}.",
            "including size limits, highway-side position and the local checks most likely to change the answer.",
        ),
        "hard-surfaces": (
            f"Check hard surfacing rules in {town_name}.",
            "including permeability, drainage and when a front-garden layout stops looking straightforward.",
        ),
        "hmos": (
            f"Check HMO rules in {town_name}.",
            "including change of use, Article 4 risk and the local policy checks most likely to decide the route.",
        ),
        "solar-panels": (
            f"Check solar panel rules in {town_name}.",
            "including roof position, visibility and the local checks most likely to change the route.",
        ),
        "temporary-buildings": (
            f"Check temporary building rules in {town_name}.",
            "including timing, use and the local checks most likely to decide whether a formal route is safer.",
        ),
    }
    return focus.get(
        project_slug,
        (
            f"Check {project_phrase} in {town_name}.",
            "including the local planning route, the main tripwires and the next checks worth making before you build.",
        ),
    )


def _local_search_title(page: dict, authority_label: str) -> str:
    query = _normalize_text(page.get("query", "")).lower()
    project_slug = str(page.get("project_slug", "")).lower()
    scenario_slug = str(page.get("scenario_slug", "")).lower()

    if project_slug == "hmos" and "article 4" in query:
        if page.get("target_scope") == "county":
            return f"{authority_label} HMO and Article 4: councils and route"
        return f"{authority_label} HMO and Article 4: planning and PD route"
    if scenario_slug == "article-4":
        return f"Article 4 in {authority_label}: what to check locally"
    if scenario_slug == "conservation-areas":
        return f"{authority_label} conservation areas: rules and local checks"
    if scenario_slug == "permitted-development":
        return f"Permitted development in {authority_label}: local checks"
    if "domestic alteration plans" in query:
        if "hagley" in query:
            return "Domestic alteration plans in Hagley: what to check"
        return f"Domestic alteration plans in {authority_label}: what to check"
    if "industrial alteration plans" in query:
        return f"Industrial alteration plans in {authority_label}: local route"
    if local_search_is_broad_authority_query(page) and local_search_owner(page) == "authority":
        if query.startswith("planning permission "):
            return f"{authority_label} planning permission: council checks"
        return f"Planning permission in {authority_label}: council and project checks"

    title_map = {
        "dropped-kerbs": f"Dropped kerbs in {authority_label}: planning and highway checks",
        "driveways": f"Driveway planning in {authority_label}: local checks",
        "house-extensions": f"House extensions in {authority_label}: planning route",
        "rear-extensions": f"Rear extensions in {authority_label}: planning route",
        "side-extensions": f"Side extensions in {authority_label}: planning route",
        "single-storey-extensions": f"Single storey extensions in {authority_label}: planning route",
        "change-of-use": f"Change of use in {authority_label}: planning route",
        "two-storey-extensions": f"Two storey extensions in {authority_label}: local checks",
        "heat-pumps": f"Heat pumps in {authority_label}: planning route and checks",
        "solar-panels": f"Solar panels in {authority_label}: planning route and checks",
        "loft-conversions": f"Loft conversions in {authority_label}: planning route and checks",
        "garage-conversions": f"Garage conversions in {authority_label}: planning route and checks",
        "porches": f"Porch planning in {authority_label}: local checks",
        "garden-rooms": f"Garden rooms in {authority_label}: planning route and checks",
        "outbuildings": f"Outbuildings in {authority_label}: planning route and checks",
        "fences-and-walls": f"Fences and walls in {authority_label}: planning route and checks",
        "windows-and-doors": f"Windows and doors in {authority_label}: planning route and checks",
    }
    if project_slug == "change-of-use" and "industrial alteration" in query:
        return f"Industrial alteration plans in {authority_label}: local route"
    return title_map.get(project_slug, f"{authority_label}: local planning route")


def build_home_metadata() -> tuple[str, str]:
    title = "UK Planning Permission Guide: projects, councils and tools"
    description = (
        "Check project guides, local authority pages, planning rule hubs and tools "
        "to see what usually applies, what changes it locally and what to check next."
    )
    return title, _trim_text(description, 155)


def build_councils_hub_metadata(county_count: int) -> tuple[str, str]:
    title = "UK planning authorities: councils, counties and local checks"
    description = (
        f"Browse {county_count} county planning areas and local authority pages to find "
        "the council context most likely to change the planning answer for a project."
    )
    return _trim_text(title, 68), _trim_text(description, 155)


def build_project_hub_metadata(project: dict) -> tuple[str, str]:
    project_slug = str(project.get("slug", "")).strip()
    project_name = project.get("short_name", project.get("title", "Project"))
    project_phrase = _project_phrase(project_name)

    metadata = {
        "garden-rooms": (
            "Garden room planning permission: rules, limits and local checks",
            "Check garden room planning permission, permitted development limits, height and use rules, then compare the local pages if restrictions may change the route.",
        ),
        "house-extensions": (
            "House extension planning permission: rules, limits and local checks",
            "Check house extension planning permission, common size and neighbour-impact limits, and the local checks worth making before drawings move further.",
        ),
        "temporary-buildings": (
            "Temporary buildings planning permission: use, timing and local checks",
            "Check when temporary buildings need planning permission, what makes a structure genuinely temporary and which local factors make a closer check safer.",
        ),
        "agricultural-buildings": (
            "Agricultural building planning permission: PD, conversions and checks",
            "Check agricultural building permitted development, when planning permission or prior approval is more likely and what to verify before a conversion or new build moves on.",
        ),
    }
    title, description = metadata.get(
        project_slug,
        (
            f"{project_name}: planning rules, limits and local checks",
            f"Use this guide to understand {project_phrase}, the rule thresholds most likely to matter and the local pages worth opening next.",
        ),
    )
    return _trim_text(title, 70), _trim_text(description, 155)


def build_local_project_metadata(clean_project: str, town_name: str, rule, project_slug: str = "") -> tuple[str, str]:
    project_phrase = _project_phrase(clean_project)
    country_slug = (rule or {}).get("country_slug", "")
    county_slug = (rule or {}).get("county_slug", "")
    town_slug = (rule or {}).get("town_slug", "") or _slug_from_label(town_name)
    if project_slug and county_slug and town_slug:
        override = metadata_override_for_path(f"/{project_slug}/{county_slug}/{town_slug}/")
        if override:
            return _trim_text(override[0], 70), _trim_text(override[1], 155)

    if project_slug == "porches" and country_slug == "wales":
        return (
            _trim_text(f"Porch planning in {town_name}: 3 sq m rule and checks", 68),
            _compose_description(
                f"Check porch planning in {town_name},",
                "including the 3 square metre limit, height, highway-side position and when planning permission is more likely.",
            ),
        )
    if project_slug == "porches" and country_slug == "scotland":
        return (
            _trim_text(f"Porch planning in {town_name}: 3 sq m official checks", 68),
            _compose_description(
                f"Check Scottish porch planning rules in {town_name},",
                "including the 3 square metre limit, height, road-facing position and the official checks to verify next.",
            ),
        )

    title_templates = {
        "dropped-kerbs": f"Dropped kerb planning in {town_name}: highway checks",
        "driveways": f"Driveways in {town_name}: planning rules",
        "porches": f"Porch planning permission in {town_name}",
        "hard-surfaces": f"Hard surfacing in {town_name}: planning rules",
        "change-of-use": f"Change of use in {town_name}: planning rules",
        "hmos": f"HMO planning in {town_name}: Article 4 and local rules",
        "fences-and-walls": f"Fences and walls in {town_name}: planning rules",
        "garden-rooms": f"Garden rooms in {town_name}: planning rules",
        "annexes": f"Annexe planning in {town_name}: local rules",
        "outbuildings": f"Outbuildings in {town_name}: planning rules",
        "house-extensions": f"House extensions in {town_name}: planning rules",
        "solar-panels": f"Solar panels in {town_name}: planning rules",
        "temporary-buildings": f"Temporary buildings in {town_name}: planning rules",
    }
    title_overrides = {
        "garden-rooms": f"Garden room rules in {town_name}: local checks",
        "fences-and-walls": f"Fences and walls in {town_name}: local planning rules",
        "outbuildings": f"Outbuilding rules in {town_name}: local checks",
        "house-extensions": f"House extensions in {town_name}: local rules and PD checks",
    }
    description_overrides = {
        "garden-rooms": _compose_description(
            f"Check whether a garden room in {town_name} can stay incidental, use permitted development or needs planning permission,",
            "with the local checks most likely to change the answer.",
        ),
        "fences-and-walls": _compose_description(
            f"Check fence and wall rules in {town_name},",
            "including front-boundary height, highway-side limits, gates and the local restrictions most likely to change the route.",
        ),
        "outbuildings": _compose_description(
            f"Check outbuilding rules in {town_name},",
            "including planning permission, permitted development, height, siting, use and the local restrictions most likely to matter.",
        ),
        "house-extensions": _compose_description(
            f"Check house extension planning permission in {town_name},",
            "including permitted development limits, neighbour-sensitive checks and the local restrictions most likely to change the route.",
        ),
        "porches": _compose_description(
            f"Check porch planning permission in {town_name},",
            "including size, height, highway-side position and the local checks most likely to change the answer.",
        ),
        "dropped-kerbs": _compose_description(
            f"Check dropped kerb planning in {town_name},",
            "including when planning permission, highway approval, visibility and drainage need separate checks.",
        ),
        "hmos": _compose_description(
            f"Check HMO planning in {town_name},",
            "including change of use, Article 4, permitted development assumptions and local policy tripwires.",
        ),
    }
    title = title_overrides.get(project_slug, title_templates.get(project_slug, f"{clean_project} in {town_name}: planning rules"))
    system_label = (rule or {}).get("planning_system_label", get_system_label((rule or {}).get("county_slug", "")))
    restrictions = _restriction_summary(rule)
    restriction_phrase = _restriction_meta_phrase(restrictions)
    focus_intro, focus_next = _project_meta_focus(project_slug, project_phrase, town_name)

    if project_slug in description_overrides:
        description = description_overrides[project_slug]
    elif restrictions:
        description = _compose_description(
            focus_intro,
            f"See whether {restriction_phrase} can change the route, and what to verify before drawings or quotes.",
        )
    else:
        description = _compose_description(
            focus_intro,
            f"{focus_next} It is the main local guide for this project in the {system_label}.",
        )

    return _trim_text(title, 68), description


def build_scenario_metadata(
    clean_project: str,
    scenario_title: str,
    town_name: str,
    rule,
    scenario_slug: str,
    project_slug: str = "",
) -> tuple[str, str]:
    project_phrase = _project_phrase(clean_project)
    county_slug = (rule or {}).get("county_slug", "")
    town_slug = (rule or {}).get("town_slug", "") or _slug_from_label(town_name)
    if project_slug and county_slug and town_slug and scenario_slug:
        override = metadata_override_for_path(f"/{project_slug}/{county_slug}/{town_slug}/{scenario_slug}/")
        if override:
            return _trim_text(override[0], 70), _trim_text(override[1], 155)

    title_templates = {
        slug: _project_scenario_title(clean_project, scenario_title, town_name, slug)
        for slug in SCENARIO_TITLE_LABELS
    }
    title = title_templates.get(
        scenario_slug,
        _project_scenario_title(clean_project, scenario_title, town_name, scenario_slug),
    )
    title_overrides = {
        ("garden-rooms", "planning-permission"): f"Planning permission for a garden room in {town_name}",
        ("garden-rooms", "permitted-development"): f"Garden room permitted development in {town_name}",
        ("garden-rooms", "height-limits"): f"Garden room height limits in {town_name}",
        ("garden-rooms", "boundary-rules"): f"Garden room boundary rules in {town_name}",
        ("fences-and-walls", "planning-permission"): f"Fence planning permission in {town_name}",
        ("fences-and-walls", "boundary-rules"): f"Boundary fence rules in {town_name}",
        ("fences-and-walls", "height-limits"): f"Fence height limits in {town_name}",
        ("fences-and-walls", "maximum-height"): f"Maximum fence height in {town_name}",
        ("outbuildings", "planning-permission"): f"Outbuilding planning permission in {town_name}",
        ("outbuildings", "boundary-rules"): f"Outbuilding boundary rules in {town_name}",
        ("outbuildings", "height-limits"): f"Outbuilding height limits in {town_name}",
        ("house-extensions", "planning-permission"): f"House extension planning permission in {town_name}",
        ("house-extensions", "boundary-rules"): f"House extension boundary rules in {town_name}",
    }
    description_overrides = {
        ("garden-rooms", "planning-permission"): _compose_description(
            f"Check whether a garden room in {town_name} needs planning permission,",
            "including incidental-use tests, local restrictions and the next check if the route is borderline.",
        ),
        ("garden-rooms", "permitted-development"): _compose_description(
            f"Check whether permitted development covers a garden room in {town_name},",
            "including incidental use, height, boundary siting and the next check if the route feels borderline.",
        ),
        ("garden-rooms", "height-limits"): _compose_description(
            f"Check garden room height limits in {town_name},",
            "including the boundary-sensitive measurements most likely to change the route.",
        ),
        ("garden-rooms", "boundary-rules"): _compose_description(
            f"Check garden room boundary rules in {town_name},",
            "including siting, clearance and the local restrictions most likely to change the answer.",
        ),
        ("fences-and-walls", "planning-permission"): _compose_description(
            f"Check when fences and walls in {town_name} need planning permission,",
            "including front-boundary position, height and the local checks most likely to matter next.",
        ),
        ("fences-and-walls", "boundary-rules"): _compose_description(
            f"Check boundary fence rules in {town_name},",
            "including highway-side boundaries, gates and the local checks most likely to change the answer.",
        ),
        ("fences-and-walls", "height-limits"): _compose_description(
            f"Check fence height limits in {town_name},",
            "including the controlling ground level and when the answer changes on a front boundary.",
        ),
        ("fences-and-walls", "maximum-height"): _compose_description(
            f"Check maximum fence height in {town_name},",
            "including the measurement point and when front-boundary or highway-side rules make the limit stricter.",
        ),
        ("outbuildings", "planning-permission"): _compose_description(
            f"Check whether an outbuilding in {town_name} needs planning permission,",
            "including permitted development, height, use and the local restrictions most likely to change the route.",
        ),
        ("outbuildings", "boundary-rules"): _compose_description(
            f"Check outbuilding boundary rules in {town_name},",
            "including siting, neighbour relationship and the next check if the route is borderline.",
        ),
        ("outbuildings", "height-limits"): _compose_description(
            f"Check outbuilding height limits in {town_name},",
            "including boundary-sensitive measurements and the next check if height is the blocker.",
        ),
        ("house-extensions", "planning-permission"): _compose_description(
            f"Check whether a house extension in {town_name} needs planning permission,",
            "including permitted development limits, previous additions and the local checks most likely to matter.",
        ),
        ("house-extensions", "boundary-rules"): _compose_description(
            f"Check house extension boundary rules in {town_name},",
            "including neighbour relationship, siting and the next check if the route is borderline.",
        ),
    }
    title = title_overrides.get((project_slug, scenario_slug), title)
    restrictions = _restriction_summary(rule, limit=1)
    description = description_overrides.get(
        (project_slug, scenario_slug),
        _project_scenario_description(
            project_phrase,
            scenario_title,
            town_name,
            scenario_slug,
            restrictions,
        ),
    )

    return _trim_text(title, 70), description


def build_council_scenario_metadata(
    scenario_title: str,
    town_name: str,
    rule,
    scenario_slug: str,
) -> tuple[str, str]:
    town_slug = (rule or {}).get("town_slug", "") or _slug_from_label(town_name)
    override = metadata_override_for_path(f"/{scenario_slug}/{town_slug}/")
    if override:
        return _trim_text(override[0], 70), _trim_text(override[1], 155)

    gsc_ctr_overrides = {
        ("conservation-areas", "Glasgow City"): (
            "Glasgow City conservation areas: official planning checks",
            "Check Glasgow City conservation areas, heritage controls, official sources and the next local planning step before relying on a broad answer.",
        ),
        ("conservation-areas", "Westminster"): (
            "Westminster conservation areas: official checks and rules",
            "Check Westminster conservation-area rules, official local sources, heritage tripwires and the project pages most likely to settle the route.",
        ),
        ("conservation-areas", "Portsmouth"): (
            "Portsmouth conservation areas: planning rules and checks",
            "Check Portsmouth conservation-area planning rules, heritage controls, official sources and what to verify before spending on drawings.",
        ),
        ("conservation-areas", "Leeds"): (
            "Leeds conservation areas: planning rules and official checks",
            "Check Leeds conservation-area planning rules, heritage controls, official sources and the next local planning page to open.",
        ),
        ("planning-permission", "Carmarthenshire"): (
            "Planning permission in Carmarthenshire: local checks",
            "Check planning permission in Carmarthenshire, the council route, local project pages and what to verify before relying on a broad answer.",
        ),
    }
    override = gsc_ctr_overrides.get((scenario_slug, town_name))
    if override:
        return _trim_text(override[0], 70), _trim_text(override[1], 155)

    title_templates = {
        "planning-permission": f"Planning permission in {town_name}: local rules and next steps",
        "permitted-development": f"Permitted development in {town_name}: local rules and checks",
        "height-limits": f"Height limits in {town_name}: planning rules",
        "maximum-height": f"{town_name} maximum height: planning rules",
        "depth-limits": f"Depth limits in {town_name}",
        "boundary-rules": f"{town_name} boundary rules: planning checks",
        "distance-from-boundary": f"Distance from boundary in {town_name}",
        "roof-alterations": f"Roof alteration rules in {town_name}",
        "conservation-areas": f"{town_name} conservation areas: local rules and checks",
        "listed-buildings": f"Listed building rules in {town_name}",
        "article-4": f"Article 4 in {town_name}: local restrictions and next steps",
    }
    title = title_templates.get(
        scenario_slug,
        f"{scenario_title} in {town_name}",
    )
    if scenario_slug == "planning-permission" and len(_normalize_text(title)) > 70:
        title = f"Planning permission route: {town_name}"
    rule_signal = _lead_text(scenario_rule_excerpt(rule, scenario_slug))
    if not _is_usable_snippet(rule_signal):
        rule_signal = ""
    restrictions = _restriction_summary(rule, limit=1)

    high_intent_descriptions = {
        "planning-permission": _compose_description(
            f"Check planning permission in {town_name},",
            "including the council layer, the main local tripwires and the best next page if the route is borderline.",
        ),
        "permitted-development": _compose_description(
            f"Check permitted development in {town_name},",
            "including local limits, local restrictions and what to verify before you rely on the simpler route.",
        ),
        "height-limits": _compose_description(
            f"Check height limits in {town_name},",
            "including the controlling measurements, local signals and when extra checks matter.",
        ),
        "boundary-rules": _compose_description(
            f"Check boundary rules in {town_name},",
            "including distance issues, local signals and the next step if siting is driving the route.",
        ),
        "conservation-areas": _compose_description(
            f"Check conservation area rules in {town_name},",
            "including heritage tripwires, local restrictions and the next local step before you rely on a broad answer.",
        ),
        "listed-buildings": _compose_description(
            f"Check listed building rules in {town_name},",
            "including consent triggers, heritage tripwires and the next formal check before you rely on a simpler route.",
        ),
        "article-4": _compose_description(
            f"Check Article 4 restrictions in {town_name},",
            "including whether local directions remove permitted development rights and what to verify next.",
        ),
        "maximum-height": _compose_description(
            f"Check maximum height rules in {town_name},",
            "including the controlling measurement point, local restrictions and the next steps if height is the real blocker.",
        ),
        "depth-limits": _compose_description(
            f"Check depth limits in {town_name},",
            "including projection thresholds, local tripwires and what to verify next if the route still feels borderline.",
        ),
        "distance-from-boundary": _compose_description(
            f"Check distance-from-boundary rules in {town_name},",
            "including clearance tripwires, local restrictions and the next check if siting is deciding the route.",
        ),
        "roof-alterations": _compose_description(
            f"Check roof alteration rules in {town_name},",
            "including visibility, local restrictions and what to verify next before you rely on a broad answer.",
        ),
    }

    if scenario_slug in high_intent_descriptions:
        return _trim_text(title, 70), high_intent_descriptions[scenario_slug]

    if rule_signal and restrictions:
        description = _compose_description(
            rule_signal,
            f"Check whether restrictions such as {restrictions} in {town_name} change the normal route before you rely on it.",
        )
    elif rule_signal:
        description = _compose_description(
            rule_signal,
            f"See the local rule signal, the main tripwires and the next council-level checks for {town_name}.",
        )
    else:
        description = _compose_description(
            f"Check how {scenario_title.lower()} can affect planning decisions in {town_name},",
            "including local restrictions, practical tripwires and the safest next step if the answer still feels borderline.",
        )

    return _trim_text(title, 70), description


def build_council_metadata(town_name: str, priority_project_checks, restriction_checks) -> tuple[str, str]:
    override = metadata_override_for_path(f"/councils/{_slug_from_label(town_name)}/")
    if override:
        return _trim_text(override[0], 70), _trim_text(override[1], 155)

    gsc_ctr_overrides = {
        "Sheffield": (
            "Planning permission in Sheffield: council page and checks",
            "Use the Sheffield council page for local routes, project checks and the next official source before relying on a broad portal search.",
        ),
        "Aberdeen City": (
            "Planning permission in Aberdeen City: council page and checks",
            "Use the Aberdeen City council page for local routes, project checks and official sources before relying on a broad answer.",
        ),
        "Croydon": (
            "Planning permission in Croydon: council page and checks",
            "Use the Croydon council page for local routes, project checks, Article 4 or conservation tripwires and next checks.",
        ),
        "Barking And Dagenham": (
            "Planning permission in Barking and Dagenham: local checks",
            "Use the Barking and Dagenham council page for local routes, project pages and official checks before you commit.",
        ),
        "Flintshire": (
            "Planning permission in Flintshire: council page and checks",
            "Use the Flintshire council page for local routes, project checks and official sources before relying on a broad search.",
        ),
        "Cumberland": (
            "Planning permission in Cumberland: council page and checks",
            "Use the Cumberland council page for local routes, project checks and official sources before relying on a broad search.",
        ),
    }
    override = gsc_ctr_overrides.get(town_name)
    if override:
        return _trim_text(override[0], 70), _trim_text(override[1], 155)

    lead_projects = ", ".join(
        item["title"].lower()
        for item in (priority_project_checks or [])[:2]
        if item.get("title")
    )
    title = f"Planning permission in {town_name}: council, projects and checks"
    restriction_names = [label.lower() for label, _ in restriction_checks[:2]]
    restrictions = " and ".join(restriction_names)
    restriction_phrase = _restriction_meta_phrase(restrictions)

    if restrictions:
        description = _compose_description(
            f"Check planning permission in {town_name},",
            f"including the council page, strongest project routes and whether {restriction_phrase} can change the answer.",
        )
    elif lead_projects:
        description = _compose_description(
            f"Check planning permission in {town_name},",
            f"the council page, the strongest local routes for {lead_projects} and the next verification step before you rely on the broad answer.",
        )
    else:
        description = _compose_description(
            f"Check planning permission in {town_name},",
            "the council page, the strongest local routes and the next verification step before you rely on the broad answer.",
        )

    return _trim_text(title, 70), description


def build_county_metadata(county_name: str, council_count: int, county_slug: str = "") -> tuple[str, str]:
    title = f"Planning permission in {county_name}: entry page and councils"
    description = (
        f"Use this entry page to compare {council_count} councils in {county_name}, "
        "then open the council page, project guide or local rule page that best matches the live planning question."
    )
    return _trim_text(title, 68), _trim_text(description, 155)


def build_county_project_metadata(clean_project: str, county_name: str, council_count: int) -> tuple[str, str]:
    title = f"{clean_project} in {county_name}: compare councils and routes"
    description = (
        f"Compare {clean_project.lower()} pages across {council_count} authorities in {county_name}, "
        "then open the strongest local project or rule page for the council area that matters."
    )
    return _trim_text(title, 68), _trim_text(description, 155)


def build_scenario_hub_metadata(scenario_title: str) -> tuple[str, str]:
    hub_titles = {
        "Planning Permission": "Planning permission hub: what changes the route",
        "Permitted Development Rights": "Permitted development hub: local limits and tripwires",
        "Height Limits": "Height limits hub: when height becomes the blocker",
        "Depth Limits": "Depth limits hub: when depth becomes the blocker",
        "Boundary Distance Rules": "Boundary rules hub: siting, distance and neighbour checks",
        "Conservation Area Restrictions": "Conservation areas hub: heritage rules and next checks",
        "Listed Building Restrictions": "Listed buildings hub: heritage controls and next checks",
        "Article 4 Restrictions": "Article 4 hub: what local directions remove",
        "Maximum Height Rules": "Maximum height hub: how the limit is applied",
        "Distance From Boundary": "Distance from boundary hub: clearance and neighbour checks",
        "Roof Alterations": "Roof alterations hub: when roof changes alter the route",
    }
    hub_descriptions = {
        "Planning Permission": "Use this hub to understand the planning-permission question, then move into the local project, council or rule page that gives the real answer.",
        "Permitted Development Rights": "Use this hub to understand the permitted-development question, then open the local page where restrictions and site context are applied properly.",
        "Height Limits": "Use this hub when height is the live issue, then move into the local rule page where the measurement and site context are applied directly.",
        "Depth Limits": "Use this hub when depth is the live issue, then move into the local rule or project page where projection limits are applied directly.",
        "Boundary Distance Rules": "Use this hub when siting and boundary distance are the live issue, then open the local rule or project page that resolves the real question.",
        "Conservation Area Restrictions": "Use this hub to understand conservation-area controls, then open the local conservation page where heritage context is applied properly.",
        "Listed Building Restrictions": "Use this hub to understand listed-building controls, then open the local heritage page where consent and site context are applied properly.",
        "Article 4 Restrictions": "Use this hub to understand Article 4 directions, then move into the local project or rule page that shows whether the simpler route is actually gone.",
        "Maximum Height Rules": "Use this hub when maximum height is the live issue, then open the local rule page where the measurement point and site context matter.",
        "Distance From Boundary": "Use this hub when boundary clearance is the live issue, then open the local rule or project page where siting is applied directly.",
        "Roof Alterations": "Use this hub when roof changes are the live issue, then move into the local rule or project page where design and context are applied properly.",
    }
    title = hub_titles.get(scenario_title, f"{scenario_title} hub: when it changes the planning route")
    description = hub_descriptions.get(
        scenario_title,
        f"Use this hub to understand how {scenario_title.lower()} can change the planning route, then open the local page where the real site context is applied.",
    )
    return _trim_text(title, 68), _trim_text(description, 155)


def build_scenario_combination_metadata(
    clean_project: str,
    combo_title: str,
    town_name: str,
    rule,
    a_slug: str,
    b_slug: str,
) -> tuple[str, str]:
    title = f"{clean_project} in {town_name}: {combo_title} local checks"
    first_signal = _lead_text(scenario_rule_excerpt(rule, a_slug), limit=90)
    second_signal = _lead_text(scenario_rule_excerpt(rule, b_slug), limit=90)
    key_signal = first_signal or second_signal

    if key_signal:
        description = _compose_description(
            key_signal,
            f"See how {combo_title.lower()} can change the planning route for {clean_project.lower()} in {town_name}.",
        )
    else:
        description = _compose_description(
            f"Check how {combo_title.lower()} interact for {clean_project.lower()} in {town_name},",
            "including the key tripwires and the next check if the route still feels borderline.",
        )

    return _trim_text(title, 72), description


def build_tools_index_metadata() -> tuple[str, str]:
    title = "Planning tools: permission, PD and local constraint checks"
    description = (
        "Use planning tools to sense-check permission routes, permitted development questions "
        "and the local checks worth doing before you go deeper."
    )
    return _trim_text(title, 70), _trim_text(description, 155)


def build_tool_metadata(tool: dict) -> tuple[str, str]:
    title = tool.get("meta_title") or f"{tool['title']}: quick planning tool"
    description = tool.get("meta_description", "").strip()

    if not description:
        summary = _lead_text(tool.get("summary", ""), limit=115)
        if summary:
            description = _compose_description(summary)
        else:
            description = _compose_description(
                f"Use the {tool['title'].lower()} to get a quick planning steer,",
                "then move into the detailed guidance if the answer is close to a limit.",
    )
    tool_slug = str(tool.get("slug", "")).strip()
    stronger_titles = {
        "permitted-development-calculator": "Permitted development calculator: quick planning check",
        "planning-decision-tool": "Planning decision tool: check if permission may be needed",
        "what-can-i-build-explorer": "What can I build? Planning project explorer",
        "extension-value-estimator": "Extension value estimator: cost, uplift and planning checks",
        "site-constraint-checker": "Site constraint checker: local planning risk check",
        "planning-route-planner": "Planning route planner: application, LDC or pre-app",
        "project-requirements-generator": "Planning requirements checklist generator",
        "planning-rejection-risk-analyzer": "Planning rejection risk analyzer: refusal tripwires",
        "project-roadmap-builder": "Project roadmap builder: staged planning workflow",
        "planning-task-checklist-builder": "Planning task checklist builder",
        "evidence-pack-builder": "Evidence pack builder: planning photos and drawings",
        "local-constraint-finder": "Local constraint finder: Article 4 and heritage checks",
        "planning-timeline-planner": "Planning timeline planner: route and timing workflow",
    }
    if tool_slug in stronger_titles:
        title = stronger_titles[tool_slug]
    elif tool_slug in {
        "article-4",
        "boundary-rules",
        "conservation-areas",
        "depth-limits",
        "distance-from-boundary",
        "height-limits",
        "listed-buildings",
        "maximum-height",
        "roof-alterations",
    }:
        title = f"{tool['title']}: self-check and local tripwires"
    return _trim_text(title, 68), description


def build_faq_metadata(faq: dict) -> tuple[str, str]:
    overrides = {
        "outbuilding-height-rules": (
            "Outbuilding height rules: boundary limits and planning checks",
            "Check outbuilding height rules near boundaries, including roof height, siting and when planning permission becomes more likely.",
        ),
        "extension-depth-rules": (
            "Extension depth rules: rear extension limits and planning",
            "Check extension depth rules, rear extension limits, how depth is measured and when a deeper scheme is more likely to need planning permission.",
        ),
        "planning-permission-vs-permitted-development": (
            "Planning permission vs permitted development: which route applies?",
            "Check the difference between planning permission and permitted development, what pushes a project out of the simpler route and what to verify next.",
        ),
        "lawful-development-certificate-vs-planning-permission": (
            "Lawful development certificate vs planning permission",
            "Check when a lawful development certificate is the right route, when planning permission is still needed and what evidence matters before you choose.",
        ),
        "what-drawings-do-i-need-for-planning-permission": (
            "What drawings do I need for planning permission?",
            "Check which planning drawings and plans usually matter first, what causes validation delays and how to avoid paying for the wrong drawing pack.",
        ),
    }
    title, description = overrides.get(
        faq["slug"],
        (faq.get("title", "Planning FAQ"), faq.get("meta", faq.get("summary", ""))),
    )
    return _trim_text(title, 70), _trim_text(description, 155)


def build_faq_index_metadata() -> tuple[str, str]:
    title = "Planning permission FAQ: rules, restrictions and next steps"
    description = (
        "Browse practical planning FAQ covering permission routes, permitted development, "
        "local restrictions, applications, timings and what to verify next."
    )
    return _trim_text(title, 70), _trim_text(description, 155)


def build_local_search_metadata(page: dict, rule: dict) -> tuple[str, str]:
    authority_label = page.get("authority_slug", "").replace("-", " ").title()
    override = metadata_override_for_local_search_slug(page.get("slug", ""))
    if override:
        return _trim_text(override[0], 70), _trim_text(override[1], 155)

    if page.get("meta_title") and page.get("meta_description"):
        return _trim_text(page["meta_title"], 70), _trim_text(page["meta_description"], 155)

    scenario_slug = page.get("scenario_slug") or "planning-permission"
    scenario_signal = _lead_text(scenario_rule_excerpt(rule, scenario_slug), limit=95)
    if not _is_usable_snippet(scenario_signal):
        scenario_signal = ""

    fallback_signal = _lead_text(first_text((rule or {}).get("permitted_development", "")), limit=95)
    if not _is_usable_snippet(fallback_signal):
        fallback_signal = ""

    generic_route_markers = (
        "most householder development follows national permitted development rules",
        "householder development follows national permitted development rules",
    )
    if scenario_slug == "planning-permission":
        if any(marker in scenario_signal.lower() for marker in generic_route_markers):
            scenario_signal = ""
        if any(marker in fallback_signal.lower() for marker in generic_route_markers):
            fallback_signal = ""

    restrictions = _restriction_summary(rule, limit=2)
    query = _normalize_text(page.get("query", ""))
    project_slug = page.get("project_slug", "")
    owner = local_search_owner(page)
    entry_lead = local_search_entry_lead(page, authority_label)
    next_step = local_search_next_step_phrase(page)
    title = _local_search_title(page, authority_label)
    if len(_normalize_text(title)) > 70 and scenario_slug == "permitted-development":
        title = f"Permitted development in {authority_label}: local checks"

    detail = ""
    if scenario_signal and restrictions:
        detail = f"{scenario_signal} Check whether {restrictions} in {authority_label} changes the route."
    elif scenario_signal:
        detail = scenario_signal
    elif fallback_signal:
        detail = fallback_signal
    elif owner == "scenario":
        detail = local_search_focus_signal(page, authority_label)
    elif owner == "project":
        detail = local_search_focus_signal(page, authority_label)
    else:
        detail = local_search_focus_signal(page, authority_label)

    if len(f"{entry_lead} {next_step}") > 130:
        detail = ""

    description = _compose_description(entry_lead, next_step, detail)
    next_step_marker = {
        "authority": "authority guide",
        "scenario": "topic page",
        "project": "project guide first",
    }[owner]
    if next_step_marker not in description.lower():
        topic = local_search_topic_phrase(page, authority_label)
        if owner == "authority":
            description = _compose_description(
                f"Check planning permission in {authority_label}.",
                "Use the authority guide, then the matching project check.",
            )
        elif owner == "scenario":
            description = _compose_description(
                f"Check {topic}.",
                "Use the topic page, then the authority or project context.",
            )
        else:
            description = _compose_description(
                f"Check {topic}.",
                "Use the project guide first, then the authority or topic check.",
            )

    return _trim_text(title, 70), description


def refine_metadata(title: str, meta_description: str, canonical_url: str = "") -> tuple[str, str]:
    title = _normalize_text(title)
    meta_description = _normalize_text(meta_description)
    path = canonical_url.replace("https://ukplanningguide.co.uk", "").strip("/")
    path_parts = [part for part in path.split("/") if part]
    is_question_title = title.lower().startswith("do you need planning permission for ")
    locked_project_scenario_title = title.lower().startswith(
        (
            "planning permission for ",
            "garden room permitted development in ",
            "garden room height limits in ",
            "garden room boundary rules in ",
            "fence planning permission in ",
            "boundary fence rules in ",
            "fence height limits in ",
            "maximum fence height in ",
            "outbuilding planning permission in ",
            "outbuilding boundary rules in ",
            "outbuilding height limits in ",
            "house extension planning permission in ",
            "house extension boundary rules in ",
        )
    )

    local_project_match = re.fullmatch(r"(.+?) Planning Permission in (.+)", title)
    scenario_match = re.fullmatch(r"(.+?) (.+?) in (.+)", title)
    council_match = re.fullmatch(r"Planning Permission in (.+)", title)
    county_match = re.fullmatch(r"Planning Permission Rules in (.+)", title)

    if len(path_parts) >= 4 and path_parts[0] in PROJECT_LABELS_BY_SLUG:
        project_label = PROJECT_LABELS_BY_SLUG[path_parts[0]]
        scenario_slug = path_parts[3]
        place = path_parts[2].replace("-", " ").title()
        if title.lower() == f"{project_label.lower()} in {place.lower()}":
            if scenario_slug == "planning-permission":
                replacement = f"{project_label} planning permission in {place}"
                if len(_normalize_text(replacement)) > 70:
                    replacement = f"{project_label} permission in {place}"
                title = _trim_text(replacement, 70)
            else:
                title = _project_scenario_title(project_label, scenario_slug.replace("-", " "), place, scenario_slug)
        elif ":" not in title and not locked_project_scenario_title and scenario_slug in SCENARIO_TITLE_LABELS:
            title = _project_scenario_title(project_label, scenario_slug.replace("-", " "), place, scenario_slug)
    elif local_project_match:
        project, place = local_project_match.groups()
        title = _trim_text(f"{project} in {place}: planning permission and local rules", 68)
    elif county_match:
        county_name = county_match.group(1)
        title = _trim_text(f"{county_name} planning rules: councils and local checks", 68)
    elif council_match:
        place = council_match.group(1)
        title = _trim_text(f"Planning permission in {place}: local rules and council checks", 70)
    elif path.startswith("tools/") and ":" not in title:
        title = _trim_text(f"{title}: quick planning check", 68)
    elif path == "tools":
        title = _trim_text("Planning tools: permission and local rule checks", 68)
    elif path == "planning-faq":
        title = _trim_text("Planning permission FAQ: rules, restrictions and next steps", 70)
    elif path == "":
        title = _trim_text("UK Planning Permission Guide: projects, councils and tools", 70)
    elif (
        len(path.split("/")) >= 4
        and ":" not in title
        and scenario_match
        and not title.lower().startswith("planning permission in ")
        and not is_question_title
        and not locked_project_scenario_title
    ):
        project, rule_name, place = scenario_match.groups()
        title = _trim_text(f"{project} in {place}: {rule_name} local checks", 70)

    if not meta_description or meta_description.lower().startswith("planning permission guidance for "):
        if local_project_match:
            project, place = local_project_match.groups()
            meta_description = _trim_text(
                f"Check the planning route for {project.lower()} in {place}, including the local rules, likely restrictions and the next steps worth taking.",
                155,
            )
        elif council_match:
            place = council_match.group(1)
            meta_description = _trim_text(
                f"Check the main local planning questions in {place}, including project guides, local restrictions and the next council checks worth making.",
                155,
            )
        elif county_match:
            county_name = county_match.group(1)
            meta_description = _trim_text(
                f"Browse councils, project guides and planning topics in {county_name} to find the local authority context most likely to change the answer.",
                155,
            )
        elif path == "tools":
            meta_description = _trim_text(
                "Use planning tools to sense-check permission routes, permitted development questions and the local checks worth doing next.",
                155,
            )
        elif path == "planning-faq":
            meta_description = _trim_text(
                "Browse practical planning FAQ covering permission routes, restrictions, applications, timings and what to verify next.",
                155,
            )
        elif path == "":
            meta_description = _trim_text(
                "Check project guides, local authority pages, planning rule hubs and tools to see what usually applies, what changes it locally and what to check next.",
                155,
            )
    else:
        meta_description = _trim_text(meta_description, 155)

    return title, meta_description


def _absolute_url(href: str, canonical_url: str) -> str:
    href = str(href or "").strip()
    canonical_url = str(canonical_url or "").strip()

    if not href:
        return canonical_url

    if href.startswith(("http://", "https://")):
        return href

    if not canonical_url:
        return href

    base = canonical_url.rstrip("/")
    if href == "/":
        return base.split("/", 3)[0] + "//" + base.split("/", 3)[2] + "/"

    root = canonical_url.split("/", 3)
    if len(root) >= 3:
        site_root = root[0] + "//" + root[2]
        return site_root + "/" + href.lstrip("/")

    return href


def build_webpage_schema(title: str, canonical_url: str, meta_description: str) -> dict:
    schema = {
        "@type": "WebPage",
        "name": title,
        "url": canonical_url,
        "description": meta_description,
        "isPartOf": {
            "@type": "WebSite",
            "name": "UK Planning Guide",
            "url": _absolute_url("/", canonical_url),
        },
    }

    return {key: value for key, value in schema.items() if value}


def build_website_schema(canonical_url: str) -> dict:
    site_url = _absolute_url("/", canonical_url).rstrip("/") + "/"
    return {
        "@type": "WebSite",
        "@id": site_url.rstrip("/") + "/#website",
        "name": "UK Planning Guide",
        "url": site_url,
        "publisher": {"@id": site_url.rstrip("/") + "/#organization"},
    }


def build_software_application_schema(tool: dict, canonical_url: str) -> dict:
    return {
        "@type": "SoftwareApplication",
        "@id": canonical_url.rstrip("/") + "#software-application",
        "name": tool.get("title") or tool.get("name") or "Planning tool",
        "applicationCategory": "PlanningApplication",
        "operatingSystem": "Web",
        "url": canonical_url,
        "description": tool.get("summary") or tool.get("meta_description") or "",
        "offers": {
            "@type": "Offer",
            "price": "0",
            "priceCurrency": "GBP",
        },
    }


def build_faq_schema(faq_items: list[dict]) -> dict | None:
    questions = []
    for item in faq_items or []:
        question = _normalize_text(item.get("question") or item.get("title") or "")
        answer = _normalize_text(item.get("answer") or item.get("body") or "")
        if not question or not answer:
            continue
        questions.append(
            {
                "@type": "Question",
                "name": question,
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": answer,
                },
            }
        )
    if not questions:
        return None
    return {"@type": "FAQPage", "mainEntity": questions}


def build_breadcrumb_schema(breadcrumbs, canonical_url: str):
    if not breadcrumbs or isinstance(breadcrumbs, str):
        return None

    items = []
    for index, (label, href) in enumerate(breadcrumbs, start=1):
        target = canonical_url if not href else _absolute_url(href, canonical_url)
        items.append(
            {
                "@type": "ListItem",
                "position": index,
                "name": str(label),
                "item": target,
            }
        )

    if not items:
        return None

    return {
        "@type": "BreadcrumbList",
        "itemListElement": items,
    }


def render_schema_markup(title, canonical_url, meta_description, breadcrumbs=None, extra_schema=None) -> str:
    graph = [build_website_schema(canonical_url), build_webpage_schema(title, canonical_url, meta_description)]

    breadcrumb_schema = build_breadcrumb_schema(breadcrumbs, canonical_url)
    if breadcrumb_schema:
        graph.append(breadcrumb_schema)

    if extra_schema:
        if isinstance(extra_schema, str):
            extra_schema = json.loads(extra_schema)

        if isinstance(extra_schema, list):
            graph.extend(extra_schema)
        else:
            graph.append(extra_schema)

    payload = {
        "@context": "https://schema.org",
        "@graph": [item for item in graph if item],
    }

    return f'<script type="application/ld+json">{json.dumps(payload)}</script>'
