"""Publication boundary for national rules. Never substitute another jurisdiction."""
from copy import deepcopy
from functools import lru_cache
import json

from core.paths import DATA_FOLDER

JURISDICTIONS = {"england", "wales", "scotland", "northern-ireland"}
EXTENSIONS = {"house-extensions", "single-storey-extensions", "two-storey-extensions",
              "rear-extensions", "side-extensions", "wraparound-extensions"}


def validate_rule_module(record, jurisdiction):
    if jurisdiction not in JURISDICTIONS or record.get("jurisdiction") != jurisdiction:
        raise ValueError(f"Missing or mismatched rule jurisdiction: {jurisdiction}")
    if record.get("availability") != "unavailable" and not record.get("official_sources"):
        raise ValueError(f"Rule module needs official sources: {jurisdiction}")
    return record


@lru_cache(maxsize=128)
def _module(project, jurisdiction):
    if jurisdiction not in JURISDICTIONS:
        raise ValueError(f"Explicit jurisdiction required: {jurisdiction!r}")
    if project in EXTENSIONS and jurisdiction != "northern-ireland":
        path = DATA_FOLDER / "rule_modules" / jurisdiction / "extensions.json"
    else:
        name = "national.json" if jurisdiction == "england" else f"national-{jurisdiction}.json"
        path = DATA_FOLDER / "rules" / project / name
    if not path.exists():
        return {"jurisdiction": jurisdiction, "availability": "unavailable", "rules": {},
                "restrictions": {}, "official_sources": [],
                "permitted_development": "A verified rule summary for this project is not available here. Check the relevant government's guidance and your planning authority before deciding the route."}
    return validate_rule_module(json.loads(path.read_text(encoding="utf-8")), jurisdiction)


def national_rule_module(project, jurisdiction):
    return deepcopy(_module(project, jurisdiction))


def verified_local_layer(layer, jurisdiction):
    """Legacy scraped prose without fact-level provenance cannot override national law."""
    if not layer or not layer.get("source_url") or not layer.get("checked_at"):
        return {}
    if layer.get("jurisdiction") != jurisdiction:
        raise ValueError("Local rule jurisdiction does not match its national module")
    from datetime import date
    date.fromisoformat(layer["checked_at"])
    return layer
