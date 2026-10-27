import os

from data.scenario_data import SCENARIOS, select_scenarios


DEFAULT_SCENARIO_SLUGS = [
    "planning-permission",
    "permitted-development",
    "height-limits",
    "depth-limits",
    "boundary-rules",
    "conservation-areas",
    "listed-buildings",
    "article-4",
    "maximum-height",
    "distance-from-boundary",
    "roof-alterations",
]


def load_scenarios():
    configured = os.environ.get("SCENARIO_PAGE_SLUGS", "").strip()
    if configured:
        slugs = [slug.strip() for slug in configured.split(",") if slug.strip()]
        return select_scenarios(slugs)

    return select_scenarios(DEFAULT_SCENARIO_SLUGS)
