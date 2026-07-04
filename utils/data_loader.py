from __future__ import annotations

import json

from core.paths import DATA_FOLDER
from data.loaders import load_councils as load_councils_data
from data.loaders import load_projects as load_projects_data


def validate_rule_data(rule):
    if not isinstance(rule, dict):
        return None

    rules = rule.get("rules", {})
    restrictions = rule.get("restrictions", {})

    rule["rules"] = rules if isinstance(rules, dict) else {}
    rule["restrictions"] = restrictions if isinstance(restrictions, dict) else {}

    return rule


def load_national_rules(project_slug: str, country_slug: str = ""):
    candidate_paths = []
    if country_slug:
        candidate_paths.append(DATA_FOLDER / "rules" / project_slug / f"national-{country_slug}.json")
    candidate_paths.append(DATA_FOLDER / "rules" / project_slug / "national.json")

    path = next((item for item in candidate_paths if item.exists()), None)
    if path is None:
        return None

    try:
        with path.open("r", encoding="utf-8") as handle:
            return validate_rule_data(json.load(handle))
    except (OSError, json.JSONDecodeError):
        return None


def load_projects():
    return load_projects_data()


def load_councils():
    return load_councils_data()
