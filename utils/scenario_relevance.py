from data.loaders import load_projects


PROJECT_TYPE_SCENARIOS = {
    "extension": [
        "planning-permission",
        "permitted-development",
        "depth-limits",
        "height-limits",
        "maximum-height",
        "boundary-rules",
        "distance-from-boundary",
        "conservation-areas",
        "article-4",
        "listed-buildings",
    ],
    "loft": [
        "planning-permission",
        "permitted-development",
        "roof-alterations",
        "height-limits",
        "maximum-height",
        "conservation-areas",
        "article-4",
        "listed-buildings",
    ],
    "outbuilding": [
        "planning-permission",
        "permitted-development",
        "height-limits",
        "maximum-height",
        "boundary-rules",
        "distance-from-boundary",
        "conservation-areas",
        "article-4",
        "listed-buildings",
    ],
    "conversion": [
        "planning-permission",
        "permitted-development",
        "roof-alterations",
        "conservation-areas",
        "article-4",
        "listed-buildings",
    ],
    "external": [
        "planning-permission",
        "permitted-development",
        "height-limits",
        "maximum-height",
        "boundary-rules",
        "distance-from-boundary",
        "conservation-areas",
        "article-4",
        "listed-buildings",
    ],
    "microgeneration": [
        "planning-permission",
        "permitted-development",
        "boundary-rules",
        "conservation-areas",
        "article-4",
        "listed-buildings",
    ],
    "change-of-use": [
        "planning-permission",
        "permitted-development",
        "article-4",
        "conservation-areas",
        "listed-buildings",
    ],
    "agricultural": [
        "planning-permission",
        "permitted-development",
        "height-limits",
        "maximum-height",
        "boundary-rules",
        "distance-from-boundary",
        "conservation-areas",
        "article-4",
        "listed-buildings",
    ],
    "temporary": [
        "planning-permission",
        "height-limits",
        "maximum-height",
        "boundary-rules",
        "distance-from-boundary",
        "conservation-areas",
        "article-4",
        "listed-buildings",
    ],
    "demolition": [
        "planning-permission",
        "conservation-areas",
        "article-4",
        "listed-buildings",
    ],
}

PROJECT_TYPE_BY_SLUG = {
    project["slug"]: project.get("type", "")
    for project in load_projects()
}


def relevant_scenario_slugs(project_slug: str) -> list[str]:
    project_type = PROJECT_TYPE_BY_SLUG.get(project_slug, "")
    return PROJECT_TYPE_SCENARIOS.get(project_type, PROJECT_TYPE_SCENARIOS["extension"])


def is_relevant_scenario(project_slug: str, scenario_slug: str) -> bool:
    return scenario_slug in relevant_scenario_slugs(project_slug)


def filter_relevant_scenarios(project_slug: str, scenarios, include_current: str | None = None):
    allowed = set(relevant_scenario_slugs(project_slug))
    if include_current:
        allowed.add(include_current)
    return [scenario for scenario in scenarios if scenario.get("slug") in allowed]
