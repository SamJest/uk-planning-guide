# ------------------------------------------------
# Scenario Combination Generator
# ------------------------------------------------

from __future__ import annotations

from pathlib import Path

# ✅ DATA
from data.loaders import load_projects, load_councils, load_rule
from components.seo import build_scenario_combination_metadata

# ✅ CORE
from core.render import inject_into_base
from core.files import write_file
from core.paths import OUTPUT_FOLDER

# ✅ UTILS
from utils.random_tools import page_rng
from utils.random_tools import get_month_year

# ✅ DATA (unchanged)
from data.scenario_data import SCENARIOS

# ✅ COMPONENTS (unchanged)
from components.scenario_combinations import *

BASE_URL = "https://ukplanningguide.co.uk"

MAX_COMBINATIONS = 24
MAX_RELATED_RULES = 6



def generate_scenario_combinations():

    print("Generating scenario combination pages")

    projects = load_projects()
    councils_by_county = load_councils()

    combos = build_combinations(SCENARIOS, MAX_COMBINATIONS)

    for project in projects:

        project_slug = project["slug"]
        project_title = project["title"]
        clean_project = project_title.replace("Planning Permission", "").strip()

        for county_slug, councils in councils_by_county.items():

            county_name = county_slug.replace("-", " ").title()

            for council in councils:

                town_slug = council["town_slug"]
                town_name = council["town_name"]

                rng = page_rng(project_slug, county_slug, town_slug)
                rule = load_rule(project_slug, county_slug, town_slug) or {}

                for a, b, combo_slug, combo_title in combos:

                    folder = OUTPUT_FOLDER / project_slug / county_slug / town_slug / combo_slug
                    folder.mkdir(parents=True, exist_ok=True)

                    content = assemble_combo_page(
                        [
                            build_combo_hero(clean_project, combo_title, town_name, county_name, rule, a["slug"], b["slug"]),
                            build_combo_intro(project_title, combo_title, town_name, rng),
                            *render_combo_rules(rule, a["slug"], b["slug"], town_name),
                            build_rule_interaction_section(a["title"], b["title"], clean_project, town_name, rule),
                            build_combo_examples(a["title"], b["title"], clean_project, town_name),
                            build_combo_next_steps(project_slug, county_slug, town_slug, clean_project, combo_title, a["slug"], b["slug"]),
                            build_related_rule_links(
                                project_slug,
                                county_slug,
                                town_slug,
                                SCENARIOS,
                                a["slug"],
                                b["slug"],
                                MAX_RELATED_RULES,
                            ),
                            build_combo_link_cluster(project_slug, county_slug, town_slug, SCENARIOS, a["slug"], b["slug"]),
                            build_trust_section(town_name),
                            f"<div class='last-updated'>Updated {get_month_year()}</div>",
                        ]
                    )

                    canonical = f"{BASE_URL}/{project_slug}/{county_slug}/{town_slug}/{combo_slug}/"
                    title, description = build_scenario_combination_metadata(
                        clean_project,
                        combo_title,
                        town_name,
                        rule,
                        a["slug"],
                        b["slug"],
                    )

                    html = inject_into_base(
                        title,
                        content,
                        {},
                        canonical,
                        description,
                    )

                    write_file(folder, "index.html", html)

    print("Scenario combination pages generated successfully")
