import json
from collections import defaultdict
from pathlib import Path
import sys


CURRENT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = CURRENT_DIR.parent
sys.path.append(str(PROJECT_ROOT))

from core.paths import DATA_FOLDER  # noqa: E402
from data.loaders import load_projects, load_councils  # noqa: E402


PRIORITY_PROJECTS = {
    "house-extensions",
    "single-storey-extensions",
    "rear-extensions",
    "side-extensions",
    "wraparound-extensions",
    "two-storey-extensions",
    "loft-conversions",
    "dormer-extensions",
    "roof-lights",
    "garden-rooms",
    "outbuildings",
    "annexes",
    "porches",
}

RULE_FIELDS = ("height_rules", "depth_rules", "boundary_rules", "roof_rules", "materials_rules")


def _read_json(path: Path):
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def _text_length(value) -> int:
    if isinstance(value, str):
        return len(" ".join(value.split()))
    if isinstance(value, list):
        return sum(_text_length(item) for item in value)
    if isinstance(value, dict):
        return sum(_text_length(item) for item in value.values())
    return 0


def audit_national_rules(projects):
    rows = []
    for project in projects:
        path = DATA_FOLDER / "rules" / project["slug"] / "national.json"
        if not path.exists():
            rows.append(
                {
                    "project": project["slug"],
                    "status": "missing-national-file",
                    "missing_fields": list(RULE_FIELDS),
                }
            )
            continue

        payload = _read_json(path)
        rules = payload.get("rules", {})
        missing_fields = [field for field in RULE_FIELDS if not rules.get(field)]
        weak_fields = [field for field in RULE_FIELDS if 0 < _text_length(rules.get(field)) < 80]
        rows.append(
            {
                "project": project["slug"],
                "status": "ok" if not missing_fields and not weak_fields else "needs-review",
                "missing_fields": missing_fields,
                "weak_fields": weak_fields,
                "pd_present": bool(payload.get("permitted_development")),
            }
        )
    return rows


def audit_jurisdiction_defaults(projects, country_slug):
    path = DATA_FOLDER / "jurisdiction_rule_defaults" / f"{country_slug}.json"
    payload = _read_json(path)
    type_defaults = payload.get("types", {})
    project_defaults = payload.get("projects", {})

    by_type = defaultdict(list)
    for project in projects:
        by_type[project["type"]].append(project["slug"])

    missing_type_defaults = [project_type for project_type in sorted(by_type) if project_type not in type_defaults]
    missing_priority_project_overrides = [
        project["slug"]
        for project in projects
        if project["slug"] in PRIORITY_PROJECTS and project["slug"] not in project_defaults
    ]

    weak_project_overrides = []
    for slug, value in sorted(project_defaults.items()):
        pd_length = _text_length(value.get("permitted_development", ""))
        rule_lengths = {
            field: _text_length((value.get("rules") or {}).get(field, ""))
            for field in RULE_FIELDS
        }
        populated_rule_count = sum(1 for field_length in rule_lengths.values() if field_length > 0)
        if pd_length < 90 or populated_rule_count == 0:
            weak_project_overrides.append(
                {
                    "project": slug,
                    "pd_length": pd_length,
                    "populated_rule_count": populated_rule_count,
                }
            )

    return {
        "country": country_slug,
        "missing_type_defaults": missing_type_defaults,
        "missing_priority_project_overrides": missing_priority_project_overrides,
        "weak_project_overrides": weak_project_overrides,
    }


def audit_local_rule_inventory(projects, councils_by_county):
    rows = []
    for project in projects:
        project_dir = DATA_FOLDER / "rules" / project["slug"]
        local_entries = 0
        counties_present = 0
        for county_slug in councils_by_county:
            path = project_dir / f"{county_slug}.json"
            if not path.exists():
                continue
            counties_present += 1
            payload = _read_json(path)
            local_entries += len(payload.get("rules", []))

        rows.append(
            {
                "project": project["slug"],
                "county_rule_files": counties_present,
                "local_entries": local_entries,
            }
        )
    return rows


def main():
    projects = load_projects()
    councils_by_county = load_councils()

    report = {
        "summary": {
            "project_count": len(projects),
            "planning_area_count": len(councils_by_county),
        },
        "national_rules": audit_national_rules(projects),
        "jurisdiction_defaults": {
            "wales": audit_jurisdiction_defaults(projects, "wales"),
            "scotland": audit_jurisdiction_defaults(projects, "scotland"),
        },
        "local_rule_inventory": audit_local_rule_inventory(projects, councils_by_county),
    }

    artifacts_dir = PROJECT_ROOT / "artifacts"
    artifacts_dir.mkdir(parents=True, exist_ok=True)
    output_path = artifacts_dir / "rule_coverage_audit.json"
    output_path.write_text(json.dumps(report, indent=2), encoding="utf-8")

    print("Rule coverage audit complete")
    print(f"Projects audited: {report['summary']['project_count']}")
    print(f"Planning areas audited: {report['summary']['planning_area_count']}")
    print(f"Audit report: {output_path}")
    for country in ("wales", "scotland"):
        payload = report["jurisdiction_defaults"][country]
        print(
            f"{country.title()} missing priority overrides: {len(payload['missing_priority_project_overrides'])}; "
            f"weak overrides: {len(payload['weak_project_overrides'])}"
        )


if __name__ == "__main__":
    main()
