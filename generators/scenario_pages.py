from pathlib import Path
import traceback
from html import escape

from components.editorial_authority import build_editorial_authority_block
from components.gsc_answer_capsule import build_gsc_answer_capsule
from components.landing_cta import build_scenario_landing_handoff
from components.official_sources import build_official_sources_block
from components.planning_helpers import first_text, restriction_messages, scenario_rule_excerpt
from components.retention_cta import build_workspace_retention_cta
from components.rule_interpretation import build_rule_interpretation
from components.seo import build_council_scenario_metadata
from components.scenario_sections import *
from core.files import write_file
from core.build_scope import should_render_route
from core.paths import OUTPUT_FOLDER
from core.render import inject_into_base
from data.loaders import load_councils, load_projects, load_rule
from utils.random_tools import page_rng
from utils.scenario_config import load_scenarios
from utils.content_contracts import ContractError, page_records_by_route
from utils.country_utils import get_country_slug
from utils.official_sources import OfficialSourceContext, relevant_official_sources, source_category_label


BASE_URL = "https://ukplanningguide.co.uk"

PRIORITY_PROJECT_SLUGS = [
    "house-extensions",
    "rear-extensions",
    "loft-conversions",
    "outbuildings",
    "garden-rooms",
]


def _generate_source_backed_local_rule_page(
    *,
    council: dict,
    county_slug: str,
    scenario: dict,
    projects: list[dict],
) -> bool:
    town_slug = council["town_slug"]
    town_name = council["town_name"]
    scenario_slug = scenario["slug"]
    scenario_title = scenario["title"]
    country = council.get("country_slug") or get_country_slug(county_slug)
    legacy_path = f"/{scenario_slug}/{town_slug}/"
    country_path = f"/{country}/rules/{scenario_slug}/{town_slug}/"
    from utils.content_contracts import render_record_for_path
    record = render_record_for_path(legacy_path) or render_record_for_path(country_path)
    if record and (record.get("page_family") != "local_rule" or record.get("project_id")):
        raise ContractError(f"Invalid local-rule contract for {legacy_path}")

    sources = relevant_official_sources(
        OfficialSourceContext(
            page_family="scenario",
            authority_slug=town_slug,
            country_slug=country,
            scenario_slug=scenario_slug,
            max_links=5,
        )
    )
    if not record and len(sources) < 3:
        raise ContractError(f"Source-backed local-rule page lacks three official sources: {legacy_path}")

    claims = "".join(
        f'<li data-claim-id="{escape(claim["claim_id"], quote=True)}">{escape(claim["text"])}</li>'
        for claim in (record or {}).get("claims", [])
    )
    facts = "".join(
        f'<li data-local-fact="true">{escape(fact["fact"])}</li>'
        for fact in (record or {}).get("unique_local_facts", [])
    )
    if not facts:
        facts = '<li>No property-specific local facts have been verified for this guide. Check the authority sources below.</li>'
    project_links = "".join(
        f'<a href="/{escape(project["slug"], quote=True)}/{escape(county_slug, quote=True)}/{escape(town_slug, quote=True)}/">{escape(project["short_name"])}</a>'
        for project in projects[:12]
    )
    verification_items = {
        "article-4": (
            "The exact property and the planning authority responsible for it.",
            "The live Article 4 direction, mapped area and schedule covering that property.",
            "The precise permitted development right withdrawn by the direction.",
            "The date the direction took effect and any later variation.",
        ),
        "conservation-areas": (
            "Whether the exact property is inside the current conservation-area boundary.",
            "The current character appraisal or management guidance for that area.",
            "Whether the proposed work affects features that contribute to its character.",
            "Which planning, listed-building or conservation-area consent is required for the exact work.",
        ),
        "permitted-development": (
            "The exact property, planning authority and applicable UK jurisdiction.",
            "The permitted-development class relevant to the selected project—not a guessed project type.",
            "Every limit, condition and prior-approval requirement for that class.",
            "Any planning condition, Article 4 direction, designation or property history that removes or changes the right.",
        ),
    }.get(
        (record or {}).get("rule_id") or scenario_slug,
        (
            "The exact property and planning authority.",
            "The current official rule or mapped designation.",
            "The selected project's dimensions, use and site context.",
            "Any property-specific condition, consent or planning history that changes the route.",
        ),
    )
    verification_html = "".join(f"<li>{escape(item)}</li>" for item in verification_items)
    content = f"""
<section class="hero">
<span class="eyebrow">Local rule check</span>
<h1>{escape(scenario_title)} in {escape(town_name)}</h1>
<p>This page checks the local rule itself without assuming any particular project.</p>
</section>
<section>
<h2>Current source position</h2>
<ul class="checklist" data-purpose="labelled-example">{claims}{facts}</ul>
<p>Where the exact designation is not verified, treat the result as unresolved and check the property with the authority before relying on permitted development.</p>
</section>
<section>
<h2>What to verify</h2>
<ol>{verification_html}</ol>
</section>
<section data-purpose="project-navigation">
<h2>Choose a project after checking the rule</h2>
<p>These links are navigation only and do not describe the current property or proposal.</p>
<div class="link-grid">{project_links}</div>
</section>
{build_official_sources_block(page_family="scenario", authority_slug=town_slug, country_slug=country, scenario_slug=scenario_slug)}
"""
    html = inject_into_base(
        title=f"{scenario_title} in {town_name}: source and property checks",
        content=content,
        options={
            "breadcrumbs": [("Home", "/"), (scenario_title, f"/{scenario_slug}/"), (town_name, "")],
            "year": ((record or {}).get("content_updated_at") or "2026")[:4],
        },
        canonical_url=f"{BASE_URL}{legacy_path}",
        meta_description=f"Check the verified source position for {scenario_title.lower()} in {town_name} without assuming a project type.",
    )
    write_file(OUTPUT_FOLDER / scenario_slug / town_slug, "index.html", html)
    return True


def _best_rule_for_scenario(projects, county_slug, town_slug, scenario_slug):
    candidates = []

    for index, project in enumerate(projects):
        rule = load_rule(project["slug"], county_slug, town_slug) or {}
        excerpt = scenario_rule_excerpt(rule, scenario_slug)
        restrictions = restriction_messages(rule)
        permitted = first_text(rule.get("permitted_development", ""))
        score = 0
        if excerpt:
            score += 4
        if restrictions:
            score += 2
        if permitted:
            score += 1
        if project["slug"] in PRIORITY_PROJECT_SLUGS:
            score += 2
        score -= index / 1000
        candidates.append((score, project, rule, excerpt))

    candidates.sort(key=lambda item: item[0], reverse=True)
    return candidates[0][1], candidates[0][2]


def _project_links_for_scenario(projects, county_slug, town_slug, scenario_slug):
    items = []

    for project in projects:
        rule = load_rule(project["slug"], county_slug, town_slug) or {}
        excerpt = scenario_rule_excerpt(rule, scenario_slug)
        restrictions = restriction_messages(rule)
        if not excerpt and not restrictions and project["slug"] not in PRIORITY_PROJECT_SLUGS[:3]:
            continue

        summary = excerpt or first_text(
            rule.get("permitted_development", ""),
            f"Check the local planning route and restriction signals for {project['short_name'].lower()} in this council area.",
        )
        items.append(
            {
                "title": project["short_name"],
                "href": f"/{project['slug']}/{county_slug}/{town_slug}/",
                "summary": summary,
                "priority": 0 if project["slug"] in PRIORITY_PROJECT_SLUGS else 1,
            }
        )

    items.sort(key=lambda item: (item["priority"], item["title"]))
    return items[:4]


def generate_scenario_pages():
    try:
        print("Generating scenario pages")

        scenarios = load_scenarios()
        projects = load_projects()
        councils_by_county = load_councils()

        high_intent_scenarios = {
            "planning-permission",
            "permitted-development",
            "height-limits",
            "boundary-rules",
            "conservation-areas",
        }

        for county_slug, councils in councils_by_county.items():
            county_name = county_slug.replace("-", " ").title()

            for council in councils:
                town_slug = council["town_slug"]
                town_name = council["town_name"]
                rng = page_rng("scenario", county_slug, town_slug)

                for scenario in scenarios:
                    scenario_slug = scenario["slug"]
                    scenario_title = scenario["title"]
                    if not should_render_route(f"/{scenario_slug}/{town_slug}/"):
                        continue
                    if _generate_source_backed_local_rule_page(
                        council=council,
                        county_slug=county_slug,
                        scenario=scenario,
                        projects=projects,
                    ):
                        continue
                    raise ContractError(
                        "Refusing to synthesize a local-rule page from an unrelated "
                        f"project record: /{scenario_slug}/{town_slug}/ has no reviewed "
                        "local_rule content contract."
                    )
                    lead_project, rule = _best_rule_for_scenario(projects, county_slug, town_slug, scenario_slug)
                    lead_project_label = (
                        lead_project.get("short_name")
                        or lead_project["title"].replace("Planning Permission", "").strip()
                        or lead_project["title"]
                    )
                    clean_project = lead_project_label
                    project_type = lead_project.get("type", "")
                    project_links = _project_links_for_scenario(projects, county_slug, town_slug, scenario_slug)
                    title, description = build_council_scenario_metadata(
                        scenario_title,
                        town_name,
                        rule,
                        scenario_slug,
                    )

                    folder = OUTPUT_FOLDER / scenario_slug / town_slug
                    folder.mkdir(parents=True, exist_ok=True)

                    sections = [
                        build_council_scenario_hero(
                            scenario_title,
                            town_name,
                            county_name,
                            rule,
                            scenario_slug,
                            project_type,
                        ),
                        build_gsc_answer_capsule(f"/{scenario_slug}/{town_slug}/"),
                        build_your_situation_summary(
                            lead_project_label,
                            project_type,
                            scenario_title,
                            town_name,
                            county_slug,
                            rule,
                            scenario_slug,
                        ),
                        build_workspace_retention_cta(
                            f"/{scenario_slug}/{town_slug}/",
                            title=f"{scenario_title} in {town_name}",
                            page_family="scenario",
                            project_slug=lead_project["slug"],
                            authority_slug=town_slug,
                        ),
                        build_scenario_route_check_cta(scenario_slug),
                        build_scenario_landing_handoff(
                            page_family="scenario",
                            authority_slug=town_slug,
                            town_name=town_name,
                            project_slug=lead_project["slug"],
                            clean_project=lead_project_label,
                            county_slug=county_slug,
                            scenario_slug=scenario_slug,
                        ),
                        build_editorial_authority_block(
                            f"/{scenario_slug}/{town_slug}/",
                            page_family="scenario",
                            authority_slug=town_slug,
                            country_slug=council.get("country_slug", ""),
                            project_slug=lead_project["slug"],
                            scenario_slug=scenario_slug,
                        ),
                        build_council_scenario_jurisdiction_notice(county_slug, town_name),
                        build_scenario_jump_links(scenario_title, town_name),
                        build_council_scenario_intro(scenario_title, town_name, rng, project_type, county_slug, scenario_slug),
                        build_council_scenario_search_intent(scenario_title, town_name, rule, scenario_slug, project_type, county_slug),
                        build_council_scenario_priority_routes(project_links, scenario_slug, town_name, town_slug),
                        build_council_scenario_signal_block(scenario_title, town_name, rule, scenario_slug),
                        build_scenario_decision_guide(lead_project_label, scenario_title, town_name, rule, scenario_slug, project_type),
                        build_local_restriction_snapshot(rule, town_name),
                        build_official_sources_block(
                            page_family="scenario",
                            authority_slug=town_slug,
                            country_slug=council.get("country_slug", ""),
                            scenario_slug=scenario_slug,
                        ),
                        build_rule_interpretation(rule, lead_project_label, scenario_slug, town_name),
                        render_scenario_rules(rule, scenario_slug),
                        build_scenario_calculator_block(
                            lead_project_label,
                            scenario_title,
                            town_name,
                            rule,
                            scenario_slug,
                        ),
                    ]

                    if scenario_slug in high_intent_scenarios:
                        sections.append(build_tool_cta(scenario_slug))

                    sections.extend(
                        [
                            build_council_scenario_project_links(project_links, town_name),
                            build_council_scenario_support_links(scenario_slug, town_name, town_slug),
                            build_local_planning_context(town_name, county_name, clean_project, project_type, county_slug, scenario_slug),
                            build_rule_comparison(lead_project_label, town_name),
                            build_real_world_examples(lead_project_label, scenario_title, town_name, rule, project_type, county_slug, scenario_slug),
                            build_scenario_internal_link_boost(lead_project["slug"], county_slug, town_slug, councils_by_county),
                            build_council_scenario_faq(scenario_title, town_name, rule, scenario_slug),
                            build_council_scenario_navigation(
                                town_slug,
                                scenarios,
                                scenario_slug,
                            ),
                            build_council_scenario_global_links(
                                town_slug,
                                county_slug,
                                councils_by_county,
                                scenario_slug,
                            ),
                            build_council_scenario_trust_section(scenario_title, town_name, county_name),
                            build_conversion_hook(lead_project_label, scenario_title, town_name, scenario_slug, town_slug),
                        ]
                    )

                    content = assemble_scenario_page(sections)
                    html = inject_into_base(
                        title,
                        content,
                        {"breadcrumbs": [("Home", "/"), (scenario_title, f"/{scenario_slug}/"), (town_name, "")]},
                        f"{BASE_URL}/{scenario_slug}/{town_slug}/",
                        description,
                    )

                    write_file(folder, "index.html", html)

        print("Scenario pages generated successfully")

    except Exception:
        print("Error generating scenario pages")
        traceback.print_exc()
        raise
