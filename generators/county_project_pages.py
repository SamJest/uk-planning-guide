from pathlib import Path

from components.county_project_sections import (
    assemble_county_project_page,
    build_county_planning_context,
    build_county_planning_topics,
    build_county_project_decision_guide,
    build_county_project_hero,
    build_county_project_jump_links,
    build_county_project_summary,
    build_county_project_support_sections,
    build_council_navigation,
    build_nearby_county_links,
    build_next_steps,
    build_regional_planning_insights,
    build_related_project_links,
    build_scenario_links,
    build_trust_section,
    slug_to_name,
)
from components.seo import build_county_project_metadata
from core.files import write_file
from core.paths import OUTPUT_FOLDER
from core.render import inject_into_base
from data.loaders import load_councils, load_projects
from utils.county_project_config import load_scenarios
from utils.random_tools import get_month_year, page_rng


BASE_URL = "https://ukplanningguide.co.uk"


def generate_county_project_pages():
    print("Generating county project pages")

    projects = load_projects()
    councils_by_county = load_councils()
    scenarios = load_scenarios()
    county_slugs = sorted(councils_by_county.keys())

    for project in projects:
        project_slug = project["slug"]
        project_title = project["title"]
        clean_project = project_title.replace("Planning Permission", "").strip()

        for county_slug, councils in councils_by_county.items():
            county_name = slug_to_name(county_slug)
            page_rng(project_slug, county_slug, county_slug)

            folder = OUTPUT_FOLDER / project_slug / county_slug
            folder.mkdir(parents=True, exist_ok=True)

            content = assemble_county_project_page(
                [
                    build_county_project_hero(clean_project, county_name, len(councils)),
                    build_county_project_jump_links(clean_project, county_name),
                    build_county_project_summary(clean_project, county_name, len(councils)),
                    build_county_project_decision_guide(clean_project, county_name),
                    build_council_navigation(councils, project_slug, county_slug, clean_project),
                    build_county_planning_topics(
                        scenarios,
                        project_slug,
                        county_slug,
                        councils,
                        clean_project,
                        county_name,
                    ),
                    build_county_planning_context(clean_project, county_name),
                    build_regional_planning_insights(county_name),
                    build_next_steps(project_slug, county_slug, county_name),
                    build_county_project_support_sections(
                        build_scenario_links(project_slug, county_slug, councils, scenarios),
                        build_nearby_county_links(project_slug, county_slugs, county_slug, clean_project),
                        build_related_project_links(projects, project_slug),
                    ),
                    build_trust_section(project_title, county_name),
                    f"<div class='last-updated'>Updated {get_month_year()}</div>",
                ]
            )

            title, description = build_county_project_metadata(
                clean_project,
                county_name,
                len(councils),
            )

            html = inject_into_base(
                title=title,
                content=content,
                options={
                    "breadcrumbs": [
                        ("Home", "/"),
                        (project_title, f"/{project_slug}/"),
                        (county_name, ""),
                    ],
                    "year": get_month_year().split()[-1],
                },
                canonical_url=f"{BASE_URL}/{project_slug}/{county_slug}/",
                meta_description=description,
            )

            write_file(folder, "index.html", html)

    print("County project pages generated successfully")
