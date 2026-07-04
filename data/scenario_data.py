SCENARIOS = [
    {
        "slug": "planning-permission",
        "title": "Planning Permission",
        "type": "approval",
        "intent": "approval requirement",
        "seo_angle": "do i need planning permission",
    },
    {
        "slug": "permitted-development",
        "title": "Permitted Development Rights",
        "type": "exemption",
        "intent": "legal exemption",
        "seo_angle": "can i build without planning permission",
    },
    {
        "slug": "height-limits",
        "title": "Height Limits",
        "type": "structural",
        "intent": "physical restriction",
        "seo_angle": "maximum height allowed",
    },
    {
        "slug": "depth-limits",
        "title": "Depth Limits",
        "type": "scale",
        "intent": "projection distance",
        "seo_angle": "how far can i build out",
    },
    {
        "slug": "boundary-rules",
        "title": "Boundary Distance Rules",
        "type": "neighbour",
        "intent": "neighbour impact",
        "seo_angle": "distance from boundary",
    },
    {
        "slug": "conservation-areas",
        "title": "Conservation Area Restrictions",
        "type": "heritage",
        "intent": "heritage planning control",
        "seo_angle": "rules in conservation areas",
    },
    {
        "slug": "listed-buildings",
        "title": "Listed Building Restrictions",
        "type": "heritage",
        "intent": "listed building consent",
        "seo_angle": "listed building consent",
    },
    {
        "slug": "article-4",
        "title": "Article 4 Restrictions",
        "type": "policy",
        "intent": "local planning control",
        "seo_angle": "article 4 direction",
    },
    {
        "slug": "maximum-height",
        "title": "Maximum Height Rules",
        "type": "structural",
        "intent": "structural restriction",
        "seo_angle": "maximum building height",
    },
    {
        "slug": "distance-from-boundary",
        "title": "Distance From Boundary",
        "type": "neighbour",
        "intent": "neighbour distance",
        "seo_angle": "distance from boundary rules",
    },
    {
        "slug": "roof-alterations",
        "title": "Roof Alterations",
        "type": "design",
        "intent": "design modification",
        "seo_angle": "roof changes planning permission",
    },
]

SCENARIO_LOOKUP = {scenario["slug"]: scenario for scenario in SCENARIOS}


def select_scenarios(slugs):
    return [SCENARIO_LOOKUP[slug].copy() for slug in slugs if slug in SCENARIO_LOOKUP]
