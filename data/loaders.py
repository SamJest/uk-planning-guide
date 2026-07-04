import json

from core.paths import DATA_FOLDER
from data.official_sources import normalize_source_list
from utils.local_note_validation import is_planning_local_note, normalize_local_note
from utils.country_utils import (
    get_baseline_label,
    get_country_name,
    get_country_slug,
    get_householder_label,
    get_system_label,
)


def _read_json(path):
    with open(path, encoding="utf-8") as handle:
        return json.load(handle)


_JURISDICTION_RULE_DEFAULTS = None
_PROJECT_TYPE_LOOKUP = None

PROJECT_FIELD_CONTAMINATION_MARKERS = {
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

def _clean_text(value):
    return normalize_local_note(value)


def _looks_noisy_text(value, field_key):
    text = _clean_text(value)
    if not text:
        return False
    return not is_planning_local_note(text, field_key)


def _project_field_looks_cross_topic(project_slug, field_key, value) -> bool:
    text = _clean_text(value).lower()
    if not text:
        return False

    if any(marker in text for marker in PROJECT_FIELD_CONTAMINATION_MARKERS["all"]):
        return True

    if project_slug != "heat-pumps" and any(
        marker in text for marker in PROJECT_FIELD_CONTAMINATION_MARKERS["heat-pumps"]
    ):
        return True

    if (
        project_slug not in {"driveways", "hard-surfaces", "dropped-kerbs"}
        and field_key == "article4_notes"
        and any(marker in text for marker in PROJECT_FIELD_CONTAMINATION_MARKERS["ev-access"])
    ):
        return True

    return False


def _sanitize_field(value, field_key, project_slug=""):
    if isinstance(value, list):
        items = [item for item in (_sanitize_field(entry, field_key, project_slug) for entry in value) if item]
        return items

    if isinstance(value, dict):
        return {
            key: cleaned
            for key, cleaned in (
                (key, _sanitize_field(entry, field_key, project_slug))
                for key, entry in value.items()
            )
            if cleaned not in ("", None, [], {})
        }

    text = _clean_text(value)
    if (
        not text
        or _looks_noisy_text(text, field_key)
        or _project_field_looks_cross_topic(project_slug, field_key, text)
    ):
        return None
    return text


def _normalize_rule_layer(layer, project_slug=""):
    if not isinstance(layer, dict):
        return {}

    normalized = {
        "permitted_development": _sanitize_field(
            layer.get("permitted_development", ""),
            "permitted_development",
            project_slug,
        )
        or "",
        "rules": {},
        "restrictions": {},
    }

    for field, value in (layer.get("rules") or {}).items():
        cleaned = _sanitize_field(_normalize_rule_value(value), field, project_slug)
        if cleaned not in ("", None, [], {}):
            normalized["rules"][field] = cleaned

    for field, value in (layer.get("restrictions") or {}).items():
        if field == "article4_applies":
            normalized["restrictions"][field] = bool(value)
            continue

        cleaned = _sanitize_field(value, field, project_slug)
        if cleaned not in ("", None, [], {}):
            normalized["restrictions"][field] = cleaned

    last_verified = _clean_text(layer.get("last_verified", ""))
    if last_verified:
        normalized["last_verified"] = last_verified

    return normalized


def _merge_rule_layers(*layers, project_slug=""):
    merged = {
        "permitted_development": "",
        "rules": {},
        "restrictions": {},
        "last_verified": "",
    }

    for layer in layers:
        normalized = _normalize_rule_layer(layer, project_slug)
        if normalized.get("permitted_development"):
            merged["permitted_development"] = normalized["permitted_development"]

        for field, value in normalized.get("rules", {}).items():
            merged["rules"][field] = value

        for field, value in normalized.get("restrictions", {}).items():
            merged["restrictions"][field] = value

        if normalized.get("last_verified"):
            merged["last_verified"] = normalized["last_verified"]

    return merged


def _load_project_type_lookup():
    global _PROJECT_TYPE_LOOKUP
    if _PROJECT_TYPE_LOOKUP is None:
        projects = _read_json(DATA_FOLDER / "projects.json").get("projects", [])
        _PROJECT_TYPE_LOOKUP = {
            project["slug"]: project.get("type", "")
            for project in projects
            if project.get("slug")
        }
    return _PROJECT_TYPE_LOOKUP


def _load_jurisdiction_rule_defaults():
    global _JURISDICTION_RULE_DEFAULTS
    if _JURISDICTION_RULE_DEFAULTS is None:
        path = DATA_FOLDER / "jurisdiction_rule_defaults.json"
        if path.exists():
            _JURISDICTION_RULE_DEFAULTS = _read_json(path)
        else:
            defaults_dir = DATA_FOLDER / "jurisdiction_rule_defaults"
            payload = {}
            if defaults_dir.exists():
                for item in sorted(defaults_dir.glob("*.json")):
                    payload[item.stem] = _read_json(item)
            _JURISDICTION_RULE_DEFAULTS = payload
    return _JURISDICTION_RULE_DEFAULTS


def _jurisdiction_rule_defaults(county_slug, project_slug):
    defaults = _load_jurisdiction_rule_defaults().get(county_slug, {})
    type_slug = _load_project_type_lookup().get(project_slug, "")
    type_defaults = (defaults.get("types") or {}).get(type_slug, {})
    project_defaults = (defaults.get("projects") or {}).get(project_slug, {})
    return _merge_rule_layers(type_defaults, project_defaults, project_slug=project_slug)


def _normalize_rule_value(value):
    if isinstance(value, dict):
        parts = []
        intro = value.get("intro")
        details = value.get("details")
        exceptions = value.get("exceptions")
        rules = value.get("rules", [])

        if intro:
            parts.append(intro)
        if isinstance(rules, list):
            parts.extend(item for item in rules if item)
        if details:
            parts.append(details)
        if exceptions:
            parts.append(f"Exceptions: {exceptions}")

        if len(parts) == 1:
            return parts[0]
        return parts

    return value


def load_projects():
    projects = _read_json(DATA_FOLDER / "projects.json")["projects"]
    return sorted(projects, key=lambda item: item["slug"])


def load_councils():
    councils_by_county = {}

    for path in sorted((DATA_FOLDER / "councils").glob("*.json")):
        data = _read_json(path)
        county_slug = data["county_slug"]
        country_slug = get_country_slug(county_slug)
        country_name = get_country_name(county_slug)
        shared_official_sources = normalize_source_list(data.get("shared_official_sources"))
        councils = []
        for council in data["councils"]:
            item = dict(council)
            item["county_slug"] = county_slug
            item["county_name"] = data.get("county_name", county_slug.replace("-", " ").title())
            item["country_slug"] = country_slug
            item["country_name"] = country_name
            item["official_sources"] = normalize_source_list(council.get("official_sources"))
            item["shared_official_sources"] = shared_official_sources
            item["all_official_sources"] = item["official_sources"] + shared_official_sources
            councils.append(item)
        councils_by_county[county_slug] = councils

    return councils_by_county


def load_rule(project_slug, county_slug, town_slug):
    national_path = DATA_FOLDER / "rules" / project_slug / "national.json"
    county_path = DATA_FOLDER / "rules" / project_slug / f"{county_slug}.json"

    national_data = _read_json(national_path) if national_path.exists() else {}
    county_data = _read_json(county_path) if county_path.exists() else {}
    jurisdiction_defaults = _jurisdiction_rule_defaults(county_slug, project_slug)
    county_defaults = county_data.get("defaults", {}) if isinstance(county_data, dict) else {}

    local_entry = {}
    for entry in county_data.get("rules", []):
        if entry.get("town_slug") == town_slug:
            local_entry = entry
            break

    merged = _merge_rule_layers(
        national_data,
        jurisdiction_defaults,
        county_defaults,
        local_entry,
        project_slug=project_slug,
    )
    merged.update(
        {
            "town_slug": town_slug,
            "county_slug": county_slug,
            "country_slug": get_country_slug(county_slug),
            "country_name": get_country_name(county_slug),
            "planning_system_label": get_system_label(county_slug),
            "householder_label": get_householder_label(county_slug),
            "baseline_label": get_baseline_label(county_slug),
        }
    )

    return merged
