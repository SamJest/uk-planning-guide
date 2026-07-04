import json
from typing import Dict, Any

# ✅ DATA
from data.loaders import load_projects, load_councils

# ✅ CONFIG / COMPONENTS (unchanged)
from utils.link_config import OUTPUT_FILE
from components.link_builders import *


def build_link_graph() -> Dict:

    print("Generating internal link graph")

    projects = load_projects()
    councils_by_county = load_councils()

    project_slugs = [p["slug"] for p in projects]
    county_slugs = list(councils_by_county.keys())

    council_slugs = [
        council["town_slug"]
        for councils in councils_by_county.values()
        for council in councils
    ]

    link_index: Dict[str, Any] = {
        "projects": build_project_links(projects, project_slugs),
        "counties": build_county_links(councils_by_county, county_slugs, project_slugs),
        "councils": build_council_links(councils_by_county, project_slugs),
        "nearby_councils": calculate_nearby_councils(councils_by_county),
        "scenarios": build_scenario_links(project_slugs, county_slugs, council_slugs),
        "discovery": build_discovery_links(project_slugs, county_slugs, council_slugs),
    }

    validate_link_graph(link_index)

    return link_index


def save_link_index(link_index: Dict):

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    with OUTPUT_FILE.open("w", encoding="utf-8") as f:
        json.dump(link_index, f, indent=2)

    print("Internal link index saved")


def generate_links():

    link_index = build_link_graph()
    save_link_index(link_index)