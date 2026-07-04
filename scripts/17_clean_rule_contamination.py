from __future__ import annotations

import json
import sys
from pathlib import Path


CURRENT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = CURRENT_DIR.parent
sys.path.append(str(PROJECT_ROOT))

from utils.local_note_validation import is_planning_local_note, normalize_local_note  # noqa: E402


RULE_FIELDS = ("height_rules", "depth_rules", "boundary_rules", "roof_rules", "materials_rules")
RESTRICTION_FIELDS = ("conservation_area", "listed_building", "article4_notes")
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


def _clean_text(value) -> str:
    return normalize_local_note(value)


def _looks_cross_topic(project_slug: str, field_key: str, value: str) -> bool:
    text = _clean_text(value).lower()
    if not text:
        return False

    if any(marker in text for marker in PROJECT_CROSS_TOPIC_MARKERS["all"]):
        return True

    if project_slug != "heat-pumps" and any(
        marker in text for marker in PROJECT_CROSS_TOPIC_MARKERS["heat-pumps"]
    ):
        return True

    if (
        project_slug not in {"driveways", "hard-surfaces", "dropped-kerbs"}
        and field_key == "article4_notes"
        and any(marker in text for marker in PROJECT_CROSS_TOPIC_MARKERS["ev-access"])
    ):
        return True

    return False


def _clean_field(container: dict, field_key: str, project_slug: str) -> bool:
    original = container.get(field_key, "")
    if not isinstance(original, str):
        return False

    cleaned = _clean_text(original)
    if not cleaned:
        if original != "":
            container[field_key] = ""
            return True
        return False

    if not is_planning_local_note(cleaned, field_key) or _looks_cross_topic(project_slug, field_key, cleaned):
        if original != "":
            container[field_key] = ""
            return True
        return False

    if cleaned != original:
        container[field_key] = cleaned
        return True

    return False


def _clean_layer(layer: dict, project_slug: str) -> bool:
    changed = False

    permitted = layer.get("permitted_development", "")
    if isinstance(permitted, str):
        cleaned = _clean_text(permitted)
        if cleaned and is_planning_local_note(cleaned, "permitted_development") and not _looks_cross_topic(
            project_slug, "permitted_development", cleaned
        ):
            if cleaned != permitted:
                layer["permitted_development"] = cleaned
                changed = True
        elif permitted != "":
            layer["permitted_development"] = ""
            changed = True

    rules = layer.get("rules")
    if isinstance(rules, dict):
        for field_key in RULE_FIELDS:
            changed = _clean_field(rules, field_key, project_slug) or changed

    restrictions = layer.get("restrictions")
    if isinstance(restrictions, dict):
        for field_key in RESTRICTION_FIELDS:
            changed = _clean_field(restrictions, field_key, project_slug) or changed

    return changed


def main() -> int:
    rule_root = PROJECT_ROOT / "data" / "rules"
    changed_files = 0
    changed_fields = 0

    for path in sorted(rule_root.glob("*/*.json")):
        if path.name == "national.json":
            continue

        with path.open("r", encoding="utf-8") as handle:
            payload = json.load(handle)

        project_slug = path.parent.name
        file_changed = False

        defaults = payload.get("defaults")
        if isinstance(defaults, dict):
            before = json.dumps(defaults, sort_keys=True, ensure_ascii=False)
            if _clean_layer(defaults, project_slug):
                after = json.dumps(defaults, sort_keys=True, ensure_ascii=False)
                if before != after:
                    file_changed = True
                    changed_fields += 1

        for entry in payload.get("rules", []):
            if not isinstance(entry, dict):
                continue
            before = json.dumps(entry, sort_keys=True, ensure_ascii=False)
            if _clean_layer(entry, project_slug):
                after = json.dumps(entry, sort_keys=True, ensure_ascii=False)
                if before != after:
                    file_changed = True
                    changed_fields += 1

        if file_changed:
            with path.open("w", encoding="utf-8") as handle:
                json.dump(payload, handle, ensure_ascii=False, indent=2)
                handle.write("\n")
            changed_files += 1
            print(f"cleaned {path.relative_to(PROJECT_ROOT)}")

    print(f"updated {changed_files} files")
    print(f"updated {changed_fields} rule entries")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
