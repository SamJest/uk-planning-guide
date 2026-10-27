from pathlib import Path

from components.homepage_sections import (
    build_homepage_content,
    rank_projects_for_homepage,
    rank_towns_for_homepage,
)
from components.find_help_pages import (
    build_find_help_homeowner_request_page,
    build_find_help_homeowner_success_page,
    build_find_help_homeowners_page,
    build_find_help_how_it_works_page,
    build_find_help_hub_page,
    build_find_help_specialist_apply_page,
    build_find_help_specialist_success_page,
    build_find_help_specialists_page,
    build_find_help_trust_page,
)
from components.seo import build_home_metadata
from components.personalised_guidance import (
    build_guidance_request_page,
    build_guidance_request_success_page,
    build_personalised_guidance_page,
    build_privacy_page,
)
from components.planning_route_check import (
    build_planning_help_page,
    build_planning_help_thank_you_page,
)
from components.site_pages import (
    WORKFLOW_PAGES,
    build_about_page,
    build_article4_hmo_reference_page,
    build_editorial_policy_page,
    build_methodology_page,
    build_my_planning_project_page,
    build_workflow_page,
    build_workflows_index_page,
)
from core.files import write_file
from core.paths import OUTPUT_FOLDER
from core.render import inject_into_base
from data.loaders import load_councils, load_projects
from data.find_help import FIND_HELP_ENABLED
from utils.location_utils import build_master_town_index


BASE_URL = "https://ukplanningguide.co.uk".rstrip("/")


def _write_static_page(
    slug: str,
    title: str,
    meta_description: str,
    content: str,
    *,
    page_options: dict | None = None,
):
    folder = OUTPUT_FOLDER / slug
    options = {"breadcrumbs": [("Home", "/"), (title, "")]}
    if page_options:
        options.update(page_options)
    html = inject_into_base(
        title=title,
        content=content,
        options=options,
        canonical_url=f"{BASE_URL}/{slug}/",
        meta_description=meta_description,
    )
    write_file(folder, "index.html", html)


def generate_homepage():
    OUTPUT_FOLDER.mkdir(parents=True, exist_ok=True)

    projects = load_projects()
    councils_by_county = load_councils()
    towns = build_master_town_index(councils_by_county)

    ranked_projects = rank_projects_for_homepage(projects)
    ranked_towns = rank_towns_for_homepage(towns)

    homepage_content = build_homepage_content(
        ranked_projects,
        ranked_towns,
        councils_by_county,
    )
    title, description = build_home_metadata()

    html = inject_into_base(
        title=title,
        content=homepage_content,
        options={"breadcrumbs": [("Home", "/")]},
        canonical_url=f"{BASE_URL}/",
        meta_description=description,
    )

    write_file(OUTPUT_FOLDER, "index.html", html)

    _write_static_page(
        "about",
        "About UK Planning Guide",
        "What UK Planning Guide covers, how to use it and what it does not replace.",
        build_about_page(),
    )
    _write_static_page(
        "methodology",
        "Planning Guidance Methodology",
        "How UK Planning Guide builds planning content from national rules, local authority context and scenario-based guidance.",
        build_methodology_page(),
    )
    _write_static_page(
        "personalised-planning-guidance",
        "Personalised planning guidance",
        "Use the structured request form for a practical case-specific steer on the likely planning route, local tripwires and the next checks worth making.",
        build_personalised_guidance_page(),
    )
    _write_static_page(
        "personalised-planning-guidance/request",
        "Planning Guidance Request",
        "Submit a guided planning request with the project, authority area and the main risk or uncertainty.",
        build_guidance_request_page(),
        page_options={"meta_robots": "noindex, follow"},
    )
    _write_static_page(
        "personalised-planning-guidance/request/success",
        "Planning Guidance Request Received",
        "Confirmation page for a planning guidance request submitted through the structured UK Planning Guide form.",
        build_guidance_request_success_page(),
        page_options={"meta_robots": "noindex, follow"},
    )
    _write_static_page(
        "privacy",
        "Privacy Notice",
        "How UK Planning Guide uses email enquiry details for personalised planning guidance and site improvement.",
        build_privacy_page(),
    )
    _write_static_page(
        "planning-help",
        "Planning Help",
        "Use the free route check and request planning help if suitable support may be available for your project.",
        build_planning_help_page(),
    )
    _write_static_page(
        "planning-help/thank-you",
        "Planning Help Enquiry Received",
        "Confirmation page for an optional planning help enquiry submitted through the UK Planning Guide route check.",
        build_planning_help_thank_you_page(),
        page_options={"meta_robots": "noindex, follow"},
    )
    _write_static_page(
        "editorial-policy",
        "Editorial Policy",
        "How UK Planning Guide handles authorship, review, official sources and page updates.",
        build_editorial_policy_page(),
    )
    _write_static_page(
        "article-4-hmo-by-council",
        "Article 4 And HMO By Council",
        "Use this reference page to move from broad Article 4 and HMO queries into the right authority guide and official sources.",
        build_article4_hmo_reference_page(),
    )
    _write_static_page(
        "my-planning-project",
        "My Planning Project",
        "Save planning guides, workflow results, task checklists and next steps in this browser without creating an account.",
        build_my_planning_project_page(),
    )
    _write_static_page(
        "workflows",
        "Planning Workflows",
        "Use workflow-led planning routes for extensions, garden rooms, loft conversions, dropped kerbs, HMOs and conservation areas.",
        build_workflows_index_page(),
    )
    for workflow_page in WORKFLOW_PAGES:
        _write_static_page(
            f"workflows/{workflow_page['slug']}",
            workflow_page["title"],
            workflow_page["meta"],
            build_workflow_page(workflow_page),
            page_options={"breadcrumbs": [("Home", "/"), ("Workflows", "/workflows/"), (workflow_page["title"], "")]},
        )
    if FIND_HELP_ENABLED:
        _write_static_page(
            "find-help",
            "Find Help",
            "Pre-launch homeowner-focused matching from UK Planning Guide, built to connect suitable projects with a small curated set of reputable local specialists over time.",
            build_find_help_hub_page(),
        )
        _write_static_page(
            "find-help/homeowners",
            "Find Help For Homeowners",
            "Register your project while UK Planning Guide assembles a vetted local specialist network and launches matching carefully in stages.",
            build_find_help_homeowners_page(),
        )
        _write_static_page(
            "find-help/homeowners/request",
            "Register Your Project",
            "Structured early-interest homeowner request form for the UK Planning Guide Find Help service.",
            build_find_help_homeowner_request_page(),
        )
        _write_static_page(
            "find-help/homeowners/request/success",
            "Project Interest Received",
            "Confirmation page for homeowner project interest registered through the UK Planning Guide Find Help service.",
            build_find_help_homeowner_success_page(),
            page_options={"meta_robots": "noindex, follow"},
        )
        _write_static_page(
            "find-help/specialists",
            "Find Help For Specialists",
            "Apply to join the carefully reviewed UK Planning Guide specialist network as coverage expands carefully by category and area.",
            build_find_help_specialists_page(),
        )
        _write_static_page(
            "find-help/specialists/apply",
            "Apply As A Specialist",
            "Specialist application form for the UK Planning Guide Find Help network.",
            build_find_help_specialist_apply_page(),
        )
        _write_static_page(
            "find-help/specialists/apply/success",
            "Specialist Application Received",
            "Confirmation page for specialist applications submitted to the UK Planning Guide Find Help network.",
            build_find_help_specialist_success_page(),
            page_options={"meta_robots": "noindex, follow"},
        )
        _write_static_page(
            "find-help/how-it-works",
            "How Find Help Will Work",
            "See the intended future homeowner-to-specialist flow for the UK Planning Guide Find Help service as coverage expands.",
            build_find_help_how_it_works_page(),
        )
        _write_static_page(
            "find-help/trust",
            "Find Help Trust Principles",
            "Trust and fairness principles for the early UK Planning Guide Find Help system.",
            build_find_help_trust_page(),
        )
