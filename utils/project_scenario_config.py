from __future__ import annotations

from data.scenario_data import SCENARIO_LOOKUP


PROJECT_SCENARIO_ROLLOUT: dict[str, tuple[str, ...]] = {
    "dropped-kerbs": (
        "planning-permission",
        "permitted-development",
        "boundary-rules",
        "conservation-areas",
        "listed-buildings",
    ),
    "fences-and-walls": (
        "planning-permission",
        "boundary-rules",
        "height-limits",
        "maximum-height",
        "article-4",
    ),
    "porches": (
        "planning-permission",
        "permitted-development",
        "height-limits",
        "maximum-height",
        "conservation-areas",
    ),
    "house-extensions": (
        "planning-permission",
        "permitted-development",
        "boundary-rules",
        "conservation-areas",
    ),
    "side-extensions": (
        "planning-permission",
        "permitted-development",
        "height-limits",
        "boundary-rules",
        "distance-from-boundary",
        "conservation-areas",
    ),
    "single-storey-extensions": (
        "planning-permission",
        "permitted-development",
        "depth-limits",
        "height-limits",
        "boundary-rules",
    ),
    "rear-extensions": (
        "permitted-development",
        "boundary-rules",
        "conservation-areas",
    ),
    "loft-conversions": (
        "permitted-development",
        "roof-alterations",
        "conservation-areas",
    ),
    "garage-conversions": (
        "planning-permission",
        "permitted-development",
        "roof-alterations",
        "conservation-areas",
    ),
    "outbuildings": (
        "planning-permission",
        "permitted-development",
        "height-limits",
        "boundary-rules",
        "conservation-areas",
    ),
    "garden-rooms": (
        "planning-permission",
        "permitted-development",
        "height-limits",
        "boundary-rules",
        "conservation-areas",
    ),
    "driveways": (
        "planning-permission",
        "permitted-development",
        "boundary-rules",
        "conservation-areas",
    ),
    "solar-panels": (
        "permitted-development",
        "boundary-rules",
        "conservation-areas",
    ),
    "heat-pumps": (
        "permitted-development",
        "boundary-rules",
        "conservation-areas",
    ),
    "hmos": (
        "planning-permission",
        "article-4",
        "conservation-areas",
    ),
    "change-of-use": (
        "planning-permission",
        "permitted-development",
        "article-4",
        "conservation-areas",
    ),
}


for project_slug, scenario_slugs in PROJECT_SCENARIO_ROLLOUT.items():
    if not project_slug:
        raise ValueError("Project-scenario rollout contains an empty project slug")
    for scenario_slug in scenario_slugs:
        if scenario_slug not in SCENARIO_LOOKUP:
            raise ValueError(f"Unknown rollout scenario slug: {scenario_slug}")


def rollout_project_slugs() -> list[str]:
    return list(PROJECT_SCENARIO_ROLLOUT)


def rollout_scenario_slugs_for_project(project_slug: str) -> tuple[str, ...]:
    return PROJECT_SCENARIO_ROLLOUT.get(project_slug, ())


def rollout_scenarios_for_project(project_slug: str) -> list[dict]:
    return [
        SCENARIO_LOOKUP[scenario_slug].copy()
        for scenario_slug in rollout_scenario_slugs_for_project(project_slug)
    ]


def project_has_rollout_scenario(project_slug: str, scenario_slug: str) -> bool:
    return scenario_slug in rollout_scenario_slugs_for_project(project_slug)


def project_scenario_href(project_slug: str, county_slug: str, town_slug: str, scenario_slug: str) -> str:
    if not county_slug or not town_slug or not project_has_rollout_scenario(project_slug, scenario_slug):
        return ""
    return f"/{project_slug}/{county_slug}/{town_slug}/{scenario_slug}/"
