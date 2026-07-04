from pathlib import Path

# ✅ DATA
from data.download_assets import assets_for_source_path
from data.loaders import load_projects, load_councils
from components.download_assets import render_download_asset_cards_for_path
from components.seo import build_scenario_hub_metadata

# ✅ CORE
from core.render import inject_into_base
from core.files import write_file
from core.build_scope import should_render_route
from core.paths import OUTPUT_FOLDER

# ✅ UTILS
from utils.random_tools import page_rng
from utils.random_tools import get_month_year

# ✅ EXISTING
from utils.scenario_hub_config import SCENARIOS
from components.scenario_hub_sections import *
from components.planning_route_check import build_planning_route_check_cta, should_show_route_check_scenario_cta

BASE_URL = "https://ukplanningguide.co.uk"

MAX_PROJECT_LINKS = 12
MAX_EXAMPLE_LINKS = 8
MAX_RELATED_SCENARIOS = 6



def generate_scenario_hub_pages():

    print("Generating scenario hub pages")

    projects = load_projects()
    councils_by_county = load_councils()

    example_councils = []

    for county_slug, councils in councils_by_county.items():
        for council in councils:
            example_councils.append({
                "county_slug": county_slug,
                "town_slug": council["town_slug"],
                "town_name": council["town_name"],
            })

    for scenario in SCENARIOS:

        scenario_slug = scenario["slug"]
        scenario_title = scenario["title"]
        if not should_render_route(f"/{scenario_slug}/"):
            continue

        page_rng("scenario-hub", scenario_slug, scenario_slug)

        folder = OUTPUT_FOLDER / scenario_slug
        folder.mkdir(parents=True, exist_ok=True)

        hero = build_scenario_hub_hero(scenario_title)

        project_navigation = (
            '<aside data-purpose="project-navigation">'
            + build_project_navigation(projects, scenario_slug, scenario_title)
            + "</aside>"
        )

        explanation = build_scenario_explanation(scenario_title)
        download_assets = render_download_asset_cards_for_path(
            f"/{scenario_slug}/",
            assets_for_source_path(f"/{scenario_slug}/"),
        )
        route_check_cta = (
            build_planning_route_check_cta(
                variant="c" if scenario_slug in {"conservation-areas", "listed-buildings", "article-4"} else "b",
                source_page_type="scenario-hub",
                scenario_slug=scenario_slug,
                compact=True,
            )
            if should_show_route_check_scenario_cta(scenario_slug)
            else ""
        )

        examples = '<aside data-purpose="labelled-example">' + build_rule_examples(scenario_title) + "</aside>"

        local_guides = (
            '<aside data-purpose="project-navigation">'
            + build_example_local_guides(projects, example_councils, scenario_slug, scenario_title)
            + "</aside>"
        )

        related_scenarios = build_related_scenario_links(
            scenario_slug,
            SCENARIOS,
        )

        law_context = build_planning_law_context(scenario_title)

        trust = build_trust_section()

        last_updated = f"<div class='last-updated'>Updated {get_month_year()}</div>"

        content = assemble_scenario_hub_page([
            hero,
            project_navigation,
            route_check_cta,
            download_assets,
            explanation,
            examples,
            local_guides,
            related_scenarios,
            law_context,
            trust,
            last_updated,
        ])

        breadcrumbs = [
            ("Home", "/"),
            (scenario_title, f"{scenario_slug}/"),
        ]

        title, description = build_scenario_hub_metadata(scenario_title)

        canonical = f"{BASE_URL}/{scenario_slug}/"

        html = inject_into_base(
            title,
            content,
            {
                "breadcrumbs": breadcrumbs,
                "structured_data": None,
            },
            canonical,
            description,
        )

        write_file(folder, "index.html", html)

    print("Scenario hub pages generated successfully")
