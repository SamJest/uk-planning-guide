"""One-off metadata migration; does not mark legacy rule text as verified."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def write(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def main():
    for path in (ROOT / "data/rules").glob("*/national.json"):
        data = json.loads(path.read_text(encoding="utf-8"))
        data["jurisdiction"] = "england"
        data["verification"] = "unverified"
        data["official_sources"] = [{"title": "English permitted development legislation (check the applicable class)", "url": "https://www.legislation.gov.uk/uksi/2015/596/contents"}]
        write(path, data)
    definitions = {
        "england": (
            "https://www.gov.uk/government/publications/permitted-development-rights-for-householders-technical-guidance/permitted-development-rights-for-householders-technical-guidance",
            "GOV.UK: Householder permitted development technical guidance",
            "England's Class A extension rights depend on the house, siting and all applicable limits and conditions.",
            ["Ordinary single-storey rear limits are 4m for detached houses and 3m for other houses.",
             "The larger rear-extension route allows up to 8m detached or 6m other houses, subject to neighbour consultation / prior approval and the remaining conditions.",
             "A multi-storey rear extension is limited to 3m projection and must be at least 7m from the opposite curtilage boundary."],
            ["Single-storey extensions have a 4m overall height limit; eaves within 2m of a boundary are limited to 3m.",
             "Side extensions under Class A must be single storey and no wider than half the original house.",
             "Check designated-land restrictions, prior extensions, materials and whether rights have been removed."]
        ),
        "wales": (
            "https://www.gov.wales/planning-permission-extensions",
            "Welsh Government: Planning permission for extensions",
            "Welsh extension rights have separate rear and side limits. These are summary checks for houses, subject to all Welsh conditions.",
            ["Single-storey rear projection is limited to 4m, for detached, semi-detached and terraced houses alike.",
             "For rear extensions of more than one storey, projection is limited to 4m at ground floor and 3m on upper floors; the extended rear wall must be at least 10.5m from the rear boundary.",
             "Multi-storey side extensions must be at least 10.5m from a side boundary, with at least 1m setback from the principal elevation."],
            ["Single-storey rear and side extensions are limited to 4m height. Within 2m of a boundary, eaves are limited to 3m and overall height to 4m.",
             "Side extensions cannot be closer to a highway than the existing side wall, or 10.5m from the highway, whichever is nearer.",
             "Check width, materials, windows and protected-area restrictions; multi-storey rear and side extensions are excluded on designated land."]
        ),
        "scotland": (
            "https://www.gov.scot/publications/circular-1-2024-householder-permitted-development-rights/pages/4/",
            "Scottish Government: Circular 1/2024, householder permitted development",
            "Scotland uses Class 1A for single-storey ground-floor extensions and Class 1B for ground-floor extensions with more than one storey.",
            ["For Class 1A, on or within 1m of a boundary, rear projection is limited to 3m for a terrace and 4m for other houses, measured from the relevant rear wall.",
             "Class 1B does not permit any part of a multi-storey extension within 10m of a curtilage boundary."],
            ["Class 1A limits overall height to 4m and eaves to 3m. Class 1B cannot exceed the existing house height.",
             "Check footprint and front/rear curtilage coverage limits, road-facing elevations and all remaining conditions.",
             "These extension rights do not apply in conservation areas, to flats or to houses created under Class 18B or 22A; listed building consent may also be required."]
        ),
    }
    for jurisdiction, (url, title, intro, limits, other) in definitions.items():
        write(ROOT / "data/rule_modules" / jurisdiction / "extensions.json", {
            "jurisdiction": jurisdiction, "project_type": "extension", "verification": "source_checked",
            "checked_at": "2026-09-11", "official_sources": [{"url": url, "title": title, "checked_at": "2026-09-11"}],
            "permitted_development": intro, "baseline_label": jurisdiction.title() + " extension baseline",
            "rules": {"depth_rules": {"title": "Extension projection and boundaries", "intro": intro, "rules": limits},
                      "height_rules": {"title": "Other limits and restrictions", "rules": other}},
            "restrictions": {}
        })


if __name__ == "__main__":
    main()
