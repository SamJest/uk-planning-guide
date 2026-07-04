import random
from typing import Dict, List, Any
from utils.link_config import *


def build_project_links(projects, project_slugs):

    project_links = {}

    for project in projects:
        slug = project["slug"]

        related_projects = [p for p in project_slugs if p != slug]
        random.shuffle(related_projects)

        project_links[slug] = {
            "related_projects": related_projects[:MAX_RELATED_PROJECTS],
            "scenarios": SCENARIOS[:MAX_RELATED_SCENARIOS],
        }

    return project_links


def build_county_links(councils_by_county, county_slugs, project_slugs):

    county_links = {}

    for county_slug, councils in councils_by_county.items():

        councils = [c["town_slug"] for c in councils]

        nearby = [c for c in county_slugs if c != county_slug]
        random.shuffle(nearby)

        county_links[county_slug] = {
            "projects": project_slugs[:MAX_RELATED_PROJECTS],
            "councils": councils,
            "nearby_counties": nearby[:MAX_NEARBY_COUNTIES],
            "scenarios": SCENARIOS[:MAX_RELATED_SCENARIOS],
        }

    return county_links


def build_council_links(councils_by_county, project_slugs):

    council_links = {}

    for county_slug, councils in councils_by_county.items():

        for council in councils:

            town_slug = council["town_slug"]

            nearby = [
                c["town_slug"]
                for c in councils
                if c["town_slug"] != town_slug
            ]

            random.shuffle(nearby)

            council_links[town_slug] = {
                "county": county_slug,
                "projects": project_slugs[:MAX_RELATED_PROJECTS],
                "nearby_councils": nearby[:MAX_NEARBY_COUNCILS],
                "scenarios": SCENARIOS[:MAX_RELATED_SCENARIOS],
            }

    return council_links


def calculate_nearby_councils(councils_by_county):

    nearby_map = {}
    all_councils = []

    for councils in councils_by_county.values():
        for council in councils:
            all_councils.append(council["town_slug"])

    for councils in councils_by_county.values():

        for council in councils:

            town_slug = council["town_slug"]

            same_county = [
                c["town_slug"]
                for c in councils
                if c["town_slug"] != town_slug
            ]

            nearby = same_county[:MAX_NEARBY_COUNCILS]

            if len(nearby) < MAX_NEARBY_COUNCILS:
                others = [c for c in all_councils if c not in nearby and c != town_slug]
                random.shuffle(others)
                nearby.extend(others[: MAX_NEARBY_COUNCILS - len(nearby)])

            nearby_map[town_slug] = nearby[:MAX_NEARBY_COUNCILS]

    return nearby_map


def build_scenario_links(project_slugs, county_slugs, council_slugs):

    return {
        scenario: {
            "projects": project_slugs[:MAX_RELATED_PROJECTS],
            "counties": county_slugs[:MAX_RELATED_PROJECTS],
            "councils": council_slugs[:MAX_RELATED_PROJECTS],
        }
        for scenario in SCENARIOS
    }


def build_discovery_links(projects, counties, councils):

    return {
        "projects": projects[:MAX_RELATED_PROJECTS],
        "counties": counties[:MAX_RELATED_PROJECTS],
        "councils": councils[:MAX_RELATED_PROJECTS],
        "scenarios": SCENARIOS[:MAX_RELATED_SCENARIOS],
    }


def validate_link_graph(link_index):

    required_sections = ["projects", "counties", "councils", "scenarios", "discovery"]

    for section in required_sections:
        if section not in link_index:
            raise ValueError(f"Missing link graph section: {section}")