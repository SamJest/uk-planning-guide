from __future__ import annotations

from pathlib import Path

from components.editorial_authority import build_editorial_authority_block
from components.gsc_answer_capsule import build_gsc_answer_capsule
from components.landing_cta import build_scenario_landing_handoff
from components.official_sources import build_official_sources_block
from components.retention_cta import build_workspace_retention_cta
from components.rule_interpretation import build_rule_interpretation
from components.scenario_sections import (
    assemble_scenario_page,
    build_conversion_hook,
    build_local_planning_context,
    build_local_restriction_snapshot,
    build_project_scenario_priority_routes,
    build_project_scenario_signal_block,
    build_real_world_examples,
    build_scenario_calculator_block,
    build_scenario_decision_guide,
    build_scenario_faq,
    build_scenario_hero,
    build_scenario_internal_link_boost,
    build_scenario_intro,
    build_scenario_jurisdiction_notice,
    build_scenario_jump_links,
    build_scenario_navigation,
    build_tool_cta,
    build_trust_section,
    build_your_situation_summary,
    render_scenario_rules,
)
from components.seo import build_scenario_metadata
from core.files import write_file
from core.paths import OUTPUT_FOLDER
from core.render import inject_into_base
from data.loaders import load_councils, load_projects, load_rule
from utils.project_scenario_config import rollout_project_slugs, rollout_scenarios_for_project
from utils.random_tools import page_rng


BASE_URL = "https://ukplanningguide.co.uk"


def generate_project_scenario_pages() -> None:
    print("Generating project-specific scenario pages")

    projects_by_slug = {
        project["slug"]: project
        for project in load_projects()
        if project["slug"] in set(rollout_project_slugs())
    }
    councils_by_county = load_councils()

    for county_slug, councils in councils_by_county.items():
        county_name = county_slug.replace("-", " ").title()

        for council in councils:
            town_slug = council["town_slug"]
            town_name = council["town_name"]

            for project_slug, project in projects_by_slug.items():
                project_title = project["title"]
                clean_project = project_title.replace("Planning Permission", "").strip()
                project_type = project.get("type", "")
                rule = load_rule(project_slug, county_slug, town_slug) or {}
                country_slug = rule.get("country_slug", council.get("country_slug", ""))
                project_scenarios = rollout_scenarios_for_project(project_slug)

                for scenario in project_scenarios:
                    scenario_slug = scenario["slug"]
                    scenario_title = scenario["title"]
                    rng = page_rng("project-scenario", project_slug, county_slug, town_slug, scenario_slug)

                    folder = OUTPUT_FOLDER / project_slug / county_slug / town_slug / scenario_slug
                    folder.mkdir(parents=True, exist_ok=True)

                    title, description = build_scenario_metadata(
                        clean_project,
                        scenario_title,
                        town_name,
                        rule,
                        scenario_slug,
                        project_slug=project_slug,
                    )
                    canonical_path = f"/{project_slug}/{county_slug}/{town_slug}/{scenario_slug}/"

                    sections = [
                        build_scenario_hero(
                            clean_project,
                            scenario_title,
                            town_name,
                            county_name,
                            rule,
                            scenario_slug,
                            project_type,
                        ),
                        build_scenario_jurisdiction_notice(rule, town_name),
                        build_scenario_jump_links(scenario_title, town_name),
                        build_your_situation_summary(
                            clean_project,
                            project_type,
                            scenario_title,
                            town_name,
                            county_slug,
                            rule,
                            scenario_slug,
                        ),
                        build_gsc_answer_capsule(canonical_path),
                        build_workspace_retention_cta(
                            canonical_path,
                            title=f"{clean_project} {scenario_title} in {town_name}",
                            page_family="project-scenario",
                            project_slug=project_slug,
                            authority_slug=town_slug,
                        ),
                        build_scenario_landing_handoff(
                            page_family="project",
                            authority_slug=town_slug,
                            town_name=town_name,
                            project_slug=project_slug,
                            clean_project=clean_project,
                            county_slug=county_slug,
                            scenario_slug=scenario_slug,
                        ),
                        build_editorial_authority_block(
                            canonical_path,
                            page_family="project",
                            authority_slug=town_slug,
                            country_slug=country_slug,
                            project_slug=project_slug,
                            scenario_slug=scenario_slug,
                        ),
                        build_scenario_intro(
                            clean_project,
                            scenario_title,
                            town_name,
                            rng,
                            project_type,
                            county_slug,
                        ),
                        build_project_scenario_signal_block(
                            clean_project,
                            scenario_title,
                            town_name,
                            rule,
                            scenario_slug,
                        ),
                        build_scenario_decision_guide(
                            project_title,
                            scenario_title,
                            town_name,
                            rule,
                            scenario_slug,
                            project_type,
                        ),
                        build_local_restriction_snapshot(rule, town_name),
                        build_official_sources_block(
                            page_family="project",
                            authority_slug=town_slug,
                            country_slug=country_slug,
                            project_slug=project_slug,
                            scenario_slug=scenario_slug,
                        ),
                        build_rule_interpretation(rule, clean_project, scenario_slug, town_name),
                        render_scenario_rules(rule, scenario_slug),
                        build_scenario_calculator_block(
                            project_title,
                            scenario_title,
                            town_name,
                            rule,
                            scenario_slug,
                        ),
                        build_tool_cta(scenario_slug),
                        build_project_scenario_priority_routes(
                            project_slug,
                            county_slug,
                            town_slug,
                            town_name,
                            scenario_slug,
                            scenario_title,
                        ),
                        build_scenario_navigation(
                            project_slug,
                            county_slug,
                            town_slug,
                            project_scenarios,
                            scenario_slug,
                        ),
                        build_local_planning_context(
                            town_name,
                            county_name,
                            clean_project,
                            project_type,
                            county_slug,
                            scenario_slug,
                        ),
                        build_real_world_examples(
                            clean_project,
                            scenario_title,
                            town_name,
                            rule,
                            project_type,
                            county_slug,
                            scenario_slug,
                        ),
                        build_scenario_faq(
                            clean_project,
                            scenario_title,
                            town_name,
                            rule,
                            scenario_slug,
                        ),
                        build_scenario_internal_link_boost(
                            project_slug,
                            county_slug,
                            town_slug,
                            councils_by_county,
                        ),
                        build_trust_section(clean_project, town_name, county_name),
                        build_conversion_hook(
                            clean_project,
                            scenario_title,
                            town_name,
                            scenario_slug,
                            town_slug,
                        ),
                    ]

                    html = inject_into_base(
                        title=title,
                        content=assemble_scenario_page(sections),
                        options={
                            "breadcrumbs": [
                                ("Home", "/"),
                                (clean_project, f"/{project_slug}/"),
                                (town_name, f"/{project_slug}/{county_slug}/{town_slug}/"),
                                (scenario_title, ""),
                            ]
                        },
                        canonical_url=f"{BASE_URL}{canonical_path}",
                        meta_description=description,
                    )

                    write_file(folder, "index.html", html)

    print("Project-specific scenario pages generated successfully")
