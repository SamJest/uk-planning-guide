from pathlib import Path

from components.rules import (
    build_local_rule_highlight,
    build_rule_comparison,
    render_national_rule_cards,
)
from components.editorial_authority import build_editorial_authority_block
from components.building_regs_handoff import build_project_building_regs_handoff
from components.gsc_answer_capsule import build_gsc_answer_capsule
from components.growth_internal_links import build_growth_internal_link_boost
from components.landing_cta import build_project_landing_handoff
from components.official_sources import build_official_sources_block
from components.retention_cta import build_workspace_retention_cta
from components.seo import build_local_project_metadata
from components.sections import *
from core.files import write_file
from core.build_scope import should_render_route
from core.paths import OUTPUT_FOLDER
from core.render import inject_into_base
from data.loaders import load_councils, load_projects, load_rule
from utils.data_loader import load_national_rules, validate_rule_data
from utils.country_utils import get_country_slug


BASE_URL = "https://ukplanningguide.co.uk"
FORCE_REBUILD = True

SCENARIOS = [
    {"slug": "planning-permission", "title": "Planning Permission Requirements"},
    {"slug": "height-limits", "title": "Height Limits"},
    {"slug": "depth-limits", "title": "Depth Limits"},
    {"slug": "boundary-rules", "title": "Boundary Rules"},
    {"slug": "conservation-areas", "title": "Conservation Area Rules"},
    {"slug": "permitted-development", "title": "Permitted Development Rights"},
    {"slug": "article-4", "title": "Article 4 Direction Restrictions"},
    {"slug": "listed-buildings", "title": "Listed Building Restrictions"},
    {"slug": "distance-from-boundary", "title": "Distance From Boundary Rules"},
    {"slug": "maximum-height", "title": "Maximum Height Limits"},
    {"slug": "roof-alterations", "title": "Roof Alteration Rules"},
]


def generate_site_core():
    print("Starting core site generation")

    projects = load_projects()
    councils_by_county = load_councils()

    for project in projects:
        project_slug = project["slug"]
        project_title = project["title"]
        clean_project = project_title.replace("Planning Permission", "").strip()

        for county_slug, councils in councils_by_county.items():
            county_name = county_slug.replace("-", " ").title()
            national_rules = load_national_rules(project_slug, get_country_slug(county_slug))

            for council in councils:
                town_slug = council["town_slug"]
                town_name = council["town_name"]
                canonical_path = f"/{project_slug}/{county_slug}/{town_slug}/"
                if not should_render_route(canonical_path):
                    continue

                town_folder = OUTPUT_FOLDER / project_slug / county_slug / town_slug
                town_folder.mkdir(parents=True, exist_ok=True)
                file_path = town_folder / "index.html"

                if file_path.exists() and not FORCE_REBUILD:
                    continue

                rule = validate_rule_data(load_rule(project_slug, county_slug, town_slug))
                if national_rules:
                    national_rules["baseline_label"] = rule.get("baseline_label", national_rules.get("baseline_label", "National rule baseline"))
                title, description = build_local_project_metadata(clean_project, town_name, rule, project_slug)

                components = [
                    build_local_project_hero(project_slug, clean_project, town_name, rule),
                    build_gsc_answer_capsule(canonical_path),
                    build_local_jurisdiction_notice(rule, town_name),
                    build_project_jump_links(project_title, town_name),
                    build_local_answer_box(project_slug, clean_project, town_name, rule),
                    build_workspace_retention_cta(
                        canonical_path,
                        title=f"{clean_project} in {town_name}",
                        page_family="project",
                        project_slug=project_slug,
                        authority_slug=town_slug,
                    ),
                    build_project_route_check_cta(project_slug),
                    build_popular_area_questions(project_slug, county_slug, town_slug, town_name),
                    build_growth_internal_link_boost(project_slug, county_slug, town_slug),
                    build_project_landing_handoff(project_slug, clean_project, county_slug, town_slug, town_name),
                    build_editorial_authority_block(
                        f"/{project_slug}/{county_slug}/{town_slug}/",
                        page_family="project",
                        authority_slug=town_slug,
                        country_slug=rule.get("country_slug", ""),
                        project_slug=project_slug,
                    ),
                    build_official_sources_block(
                        page_family="project",
                        authority_slug=town_slug,
                        country_slug=rule.get("country_slug", ""),
                        project_slug=project_slug,
                    ),
                    build_project_decision_guide(project_slug, clean_project, town_name, rule),
                    build_local_action_links(project_slug, county_slug, town_slug, town_name),
                    build_local_rule_highlight(rule),
                    render_national_rule_cards(national_rules),
                    build_rule_comparison(clean_project, town_name),
                    build_planning_process_block(clean_project, town_name, rule, project_slug),
                    build_documents_checklist(clean_project, project_slug),
                    build_project_building_regs_handoff(project_slug, clean_project, town_name),
                    build_local_topic_handoffs(project_slug, town_slug),
                    build_real_world_examples(clean_project, town_name, rule, project_slug),
                    generate_faq(project_slug, clean_project, town_name, rule),
                    build_project_find_help_cta(project_slug),
                    build_nearby_council_links(project_slug, county_slug, town_slug, councils_by_county),
                    build_related_topic_links(project_slug, county_slug, town_slug),
                    build_project_conversion_hook(project_slug, town_slug, clean_project, town_name),
                    build_trust_section(project_title, town_name, county_name),
                ]

                html = inject_into_base(
                    title=title,
                    content=assemble_core_page_components(components),
                    options={"breadcrumbs": [("Home", "/"), (clean_project, f"/{project_slug}/"), (town_name, "")]},
                    canonical_url=f"{BASE_URL}{canonical_path}",
                    meta_description=description,
                )

                write_file(town_folder, "index.html", html)

    print("Core pages generated successfully")
