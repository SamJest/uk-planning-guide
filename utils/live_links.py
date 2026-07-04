from __future__ import annotations

from functools import lru_cache

from data.faq_data import FAQS
from data.building_regulations_pages import BUILDING_REGULATIONS_PAGES, building_regulations_path
from data.find_help import FIND_HELP_ROUTES
from data.gsc_recovery_routes import GSC_RECOVERY_PATHS
from data.local_search_pages import LOCAL_SEARCH_PAGES
from data.loaders import load_councils, load_projects
from data.scenario_data import SCENARIOS
from data.tools_data import load_tools
from data.data_assets import DATA_ASSETS, MONETISATION_SURFACES
from data.download_assets import DOWNLOAD_ASSETS, download_asset_path
from components.site_pages import WORKFLOW_PAGES
from utils.project_scenario_config import rollout_project_slugs, rollout_scenarios_for_project
from utils.urls import normalize_url
from utils.country_utils import get_country_slug


def normalize_internal_href(href: str) -> str:
    clean = normalize_url(href or "")
    return clean if clean.startswith("/") else ""


@lru_cache(maxsize=1)
def live_route_set() -> frozenset[str]:
    routes: set[str] = {
        "/",
        "/england/",
        "/england/projects/",
        "/england/process/",
        "/england/rules/",
        "/england/councils/",
        "/england/data/",
        "/england/services/",
        "/england/tools/",
        "/scotland/",
        "/scotland/projects/",
        "/scotland/rules/",
        "/scotland/councils/",
        "/wales/",
        "/wales/projects/",
        "/wales/rules/",
        "/wales/councils/",
        "/about/",
        "/methodology/",
        "/editorial-policy/",
        "/personalised-planning-guidance/",
        "/personalised-planning-guidance/request/",
        "/personalised-planning-guidance/request/success/",
        "/planning-help/",
        "/planning-help/thank-you/",
        "/privacy/",
        "/article-4-hmo-by-council/",
        "/my-planning-project/",
        "/workflows/",
        *FIND_HELP_ROUTES,
        "/tools/",
        "/downloads/",
        "/planning-faq/",
        "/councils/",
        "/local-search/",
        "/building-regulations/",
        *GSC_RECOVERY_PATHS,
    }

    councils_by_county = load_councils()
    county_slugs = sorted(councils_by_county)
    town_slugs = sorted(
        council["town_slug"]
        for councils in councils_by_county.values()
        for council in councils
        if council.get("town_slug")
    )
    project_slugs = sorted(project["slug"] for project in load_projects() if project.get("slug"))
    scenario_slugs = sorted(scenario["slug"] for scenario in SCENARIOS if scenario.get("slug"))

    for county_slug in county_slugs:
        routes.add(normalize_internal_href(f"/{county_slug}/"))

    for town_slug in town_slugs:
        routes.add(normalize_internal_href(f"/councils/{town_slug}/"))
        country = "england"
        for county_slug, councils in councils_by_county.items():
            if any(council.get("town_slug") == town_slug for council in councils):
                country = get_country_slug(county_slug)
                break
        routes.add(normalize_internal_href(f"/{country}/councils/{town_slug}/"))

    for project_slug in project_slugs:
        routes.add(normalize_internal_href(f"/{project_slug}/"))
        routes.add(normalize_internal_href(f"/england/projects/{project_slug}/"))
        for county_slug in county_slugs:
            country = get_country_slug(county_slug)
            routes.add(normalize_internal_href(f"/{project_slug}/{county_slug}/"))
            routes.add(normalize_internal_href(f"/{country}/projects/{project_slug}/{county_slug}/"))
            for council in councils_by_county.get(county_slug, []):
                town_slug = council.get("town_slug")
                if town_slug:
                    routes.add(normalize_internal_href(f"/{project_slug}/{county_slug}/{town_slug}/"))
                    routes.add(normalize_internal_href(f"/{country}/projects/{project_slug}/{town_slug}/"))

    for project_slug in rollout_project_slugs():
        for county_slug in county_slugs:
            for council in councils_by_county.get(county_slug, []):
                town_slug = council.get("town_slug")
                if not town_slug:
                    continue
                for scenario in rollout_scenarios_for_project(project_slug):
                    scenario_slug = scenario.get("slug")
                    if scenario_slug:
                        routes.add(
                            normalize_internal_href(f"/{project_slug}/{county_slug}/{town_slug}/{scenario_slug}/")
                        )
                        routes.add(
                            normalize_internal_href(f"/{get_country_slug(county_slug)}/projects/{project_slug}/{town_slug}/{scenario_slug}/")
                        )

    for scenario_slug in scenario_slugs:
        routes.add(normalize_internal_href(f"/{scenario_slug}/"))
        routes.add(normalize_internal_href(f"/england/rules/{scenario_slug}/"))
        for town_slug in town_slugs:
            routes.add(normalize_internal_href(f"/{scenario_slug}/{town_slug}/"))
            country = "england"
            for county_slug, councils in councils_by_county.items():
                if any(council.get("town_slug") == town_slug for council in councils):
                    country = get_country_slug(county_slug)
                    break
            routes.add(normalize_internal_href(f"/{country}/rules/{scenario_slug}/{town_slug}/"))

    for faq in FAQS:
        if faq.get("slug"):
            routes.add(normalize_internal_href(f"/planning-faq/{faq['slug']}/"))

    routes.update(
        normalize_internal_href(path)
        for path in (
            "/england/process/lawful-development-certificates/",
            "/england/process/prior-approval-vs-planning-permission/",
            "/england/process/pre-application-advice/",
            "/england/process/planning-refused-and-appeals/",
            "/england/process/after-planning-approval/",
            "/england/process/building-regulations/",
        )
    )

    for page in BUILDING_REGULATIONS_PAGES:
        if page.get("slug"):
            routes.add(normalize_internal_href(building_regulations_path(page)))
            routes.add(normalize_internal_href(f"/england/process/building-regulations/{page['slug']}/"))

    for page in LOCAL_SEARCH_PAGES:
        if page.get("slug"):
            routes.add(normalize_internal_href(f"/local-search/{page['slug']}/"))

    for tool in load_tools():
        href = tool.get("href", f"/tools/{tool['slug']}/")
        routes.add(normalize_internal_href(href))
        if tool.get("slug"):
            routes.add(normalize_internal_href(f"/england/tools/{tool['slug']}/"))

    for asset in DATA_ASSETS:
        routes.add(normalize_internal_href(f"/england/data/{asset['slug']}/"))

    for asset in DOWNLOAD_ASSETS:
        routes.add(normalize_internal_href(download_asset_path(asset)))

    for surface in MONETISATION_SURFACES:
        routes.add(normalize_internal_href(f"/england/services/{surface['slug']}/"))

    for workflow in WORKFLOW_PAGES:
        if workflow.get("slug"):
            routes.add(normalize_internal_href(f"/workflows/{workflow['slug']}/"))

    return frozenset(route for route in routes if route)


def is_live_internal_href(href: str) -> bool:
    clean = normalize_internal_href(href)
    return bool(clean) and clean in live_route_set()


def filter_live_pairs(links: list[tuple[str, str]], exclude: set[str] | None = None) -> list[tuple[str, str]]:
    seen = set(exclude or set())
    output: list[tuple[str, str]] = []

    for href, text in links:
        clean = normalize_internal_href(href)
        if not clean or clean in seen or clean not in live_route_set():
            continue
        seen.add(clean)
        output.append((clean, text))

    return output


def filter_live_card_links(links: list[tuple[str, str, str]], exclude: set[str] | None = None) -> list[tuple[str, str, str]]:
    seen = set(exclude or set())
    output: list[tuple[str, str, str]] = []

    for title, href, description in links:
        clean = normalize_internal_href(href)
        if not clean or clean in seen or clean not in live_route_set():
            continue
        seen.add(clean)
        output.append((title, clean, description))

    return output


def filter_live_dict_links(items: list[dict], href_key: str = "href", exclude: set[str] | None = None) -> list[dict]:
    seen = set(exclude or set())
    output: list[dict] = []

    for item in items:
        clean = normalize_internal_href(item.get(href_key, ""))
        if not clean or clean in seen or clean not in live_route_set():
            continue
        seen.add(clean)
        updated = dict(item)
        updated[href_key] = clean
        output.append(updated)

    return output
