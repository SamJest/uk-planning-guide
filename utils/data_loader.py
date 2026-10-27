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


def load_national_rules(project_slug: str, country_slug: str):
    from utils.jurisdiction_rules import national_rule_module
    return national_rule_module(project_slug, country_slug)


def load_projects():
    return load_projects_data()


def load_councils():
    return load_councils_data()
