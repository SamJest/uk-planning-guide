from pathlib import Path
from html import escape

from components.editorial_authority import build_editorial_authority_block
from components.gsc_answer_capsule import build_gsc_answer_capsule
from components.landing_cta import build_council_landing_handoff
from components.official_sources import build_official_sources_block
from components.retention_cta import build_workspace_retention_cta
from components.seo import build_council_metadata
from core.paths import OUTPUT_FOLDER, BASE_URL
from core.files import write_file
from core.build_scope import should_render_route
from core.render import inject_into_base

from data.loaders import load_projects, load_councils, load_rule

from utils.random_tools import page_rng
from components.planning_helpers import first_text, restriction_messages

from utils.council_config import load_scenarios
from components.council_sections import *

from utils.random_tools import get_month_year
from utils.content_contracts import page_records_by_route
from utils.country_utils import get_country_slug


def _generate_contract_authority_profile(council, projects, county_slug: str) -> bool:
    town_slug = council["town_slug"]
    town_name = council["town_name"]
    country = council.get("country_slug") or get_country_slug(county_slug)
    canonical_path = f"/{country}/councils/{town_slug}/"
    record = page_records_by_route().get(canonical_path)
    if not record or record.get("page_family") != "authority_profile":
        return False

    fact_items = "".join(
        f'<li data-local-fact="true">{escape(fact["fact"])}</li>'
        for fact in record.get("unique_local_facts", [])
    )
    project_cards = "".join(
        '<a class="card" href="/{slug}/{county}/{town}/"><h3>{title}</h3>'
        '<p>Open the explicitly selected local project guide.</p></a>'.format(
            slug=escape(project["slug"], quote=True),
            county=escape(county_slug, quote=True),
            town=escape(town_slug, quote=True),
            title=escape(project["short_name"]),
        )
        for project in projects[:12]
    )
    content = f"""
<section class="hero">
<span class="eyebrow">Local planning authority profile</span>
<h1>{escape(town_name)} planning information</h1>
<p>Start with the authority's application, validation, policy and advice services. Choose a project only when you are ready to narrow the question.</p>
</section>
<section>
<h2>Authority-level checks</h2>
<div class="answer-grid">
<div class="answer-card"><h3>Applications and validation</h3><p>Confirm the current submission route and document requirements before preparing an application.</p></div>
<div class="answer-card"><h3>Policy and design context</h3><p>Use the adopted plan and published design guidance when the proposal needs a local policy reading.</p></div>
<div class="answer-card"><h3>Constraints and advice</h3><p>Check property-specific designations and use pre-application advice when the route remains uncertain.</p></div>
</div>
</section>
<section>
<h2>Verified local context</h2>
<ul class="checklist">{fact_items}</ul>
</section>
<section data-purpose="project-navigation">
<h2>Choose a project</h2>
<p>These links are navigation, not assumptions about your proposal.</p>
<div class="card-grid">{project_cards}</div>
</section>
"""
    html = inject_into_base(
        title=f"{town_name} planning authority guide",
        content=content,
        options={
            "breadcrumbs": [("Home", "/"), (country.replace("-", " ").title(), f"/{country}/"), ("Councils", f"/{country}/councils/"), (town_name, "")],
            "year": record["content_updated_at"][:4],
        },
        canonical_url=f"{BASE_URL}/councils/{town_slug}/",
        meta_description=f"Official-source planning routes, validation, policy and local checks for {town_name}, without assuming a project type.",
    )
    write_file(OUTPUT_FOLDER / "councils" / town_slug, "index.html", html)
    return True

def generate_council_pages():

    print("Generating council pages")

    projects = load_projects()
    councils_by_county = load_councils()
    scenarios = load_scenarios()

    councils_folder = OUTPUT_FOLDER / "councils"
    councils_folder.mkdir(parents=True, exist_ok=True)
    priority_project_slugs = [
        "garden-rooms",
        "fences-and-walls",
        "outbuildings",
        "house-extensions",
        "dropped-kerbs",
        "loft-conversions",
    ]

    for county_slug, councils in councils_by_county.items():

        county_name = county_slug.replace("-", " ").title()

        for council in councils:

            town_slug = council["town_slug"]
            town_name = council["town_name"]
            if not should_render_route(f"/councils/{town_slug}/"):
                continue

            if _generate_contract_authority_profile(council, projects, county_slug):
                continue

            page_rng("council", county_slug, town_slug)

            folder = councils_folder / town_slug
            folder.mkdir(parents=True, exist_ok=True)

            priority_project_checks = []
            restriction_checks = []

            for project in projects:
                if project["slug"] not in priority_project_slugs:
                    continue

                rule = load_rule(project["slug"], county_slug, town_slug)
                summary = first_text(
                    rule.get("permitted_development", ""),
                    f"Start with the local {project['short_name'].lower()} guide for the main planning route and any local restrictions.",
                )
                priority_project_checks.append(
                    {
                        "title": project["short_name"],
                        "href": f"/{project['slug']}/{county_slug}/{town_slug}/",
                        "summary": summary,
                    }
                )

                for label, text in restriction_messages(rule):
                    if (label, text) not in restriction_checks:
                        restriction_checks.append((label, text))

            content = assemble_council_page([
                build_council_hero(town_name, county_name),
                build_gsc_answer_capsule(f"/councils/{town_slug}/"),
                build_council_jurisdiction_notice(town_name, county_slug),
                build_council_jump_links(town_name),
                build_local_decision_summary(town_name, county_name, priority_project_checks, restriction_checks),
                build_workspace_retention_cta(
                    f"/councils/{town_slug}/",
                    title=f"{town_name} planning route",
                    page_family="council",
                    authority_slug=town_slug,
                ),
                build_council_landing_handoff(
                    town_slug,
                    town_name,
                    priority_project_checks[0]["href"] if priority_project_checks else "",
                    priority_project_checks[0]["title"] if priority_project_checks else "the strongest local project guide",
                ),
                build_editorial_authority_block(
                    f"/councils/{town_slug}/",
                    page_family="council",
                    authority_slug=town_slug,
                    country_slug=council.get("country_slug", ""),
                ),
                build_start_here_section(town_name, county_slug, town_slug, priority_project_checks),
                build_priority_project_checks(priority_project_checks, town_name),
                build_project_navigation(projects, town_name, county_slug, town_slug),
                build_common_planning_topics(projects, scenarios, county_slug, town_slug, town_name),
                build_planning_process_section(town_name),
                build_local_planning_context(town_name, county_name),
                build_planning_examples(town_name),
                build_local_authority_faq(town_name, restriction_checks, priority_project_checks),
                build_council_conversion_hook(town_name, priority_project_checks),
                build_scenario_links(projects, scenarios, county_slug, town_slug, town_name),
                build_nearby_council_links(councils_by_county, county_slug, town_slug),
                build_related_projects(projects),
                build_official_sources_block(
                    page_family="council",
                    authority_slug=town_slug,
                    country_slug=council.get("country_slug", ""),
                ),
                build_trust_section(town_name, county_name),
                f"<div class='last-updated'>Updated {get_month_year()}</div>",
            ])
            title, description = build_council_metadata(
                town_name,
                priority_project_checks,
                restriction_checks,
            )

            html = inject_into_base(
                title=title,
                content=content,
                options={
                    "breadcrumbs": [("Home", "/"), ("Councils", "/councils/"), (town_name, "")],
                    "schema": None,
                    "navigation_links": "",
                    "year": get_month_year().split()[-1],
                },
                canonical_url=f"{BASE_URL}/councils/{town_slug}/",
                meta_description=description,
            )

            write_file(folder, "index.html", html)

    print("Council pages generated successfully")
