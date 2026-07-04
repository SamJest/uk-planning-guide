SCENARIO_HUB_INTROS = {
    "Planning Permission": "Use this hub when the real question is whether planning permission is needed, what usually changes the answer, and which local page or project guide to open next.",
    "Permitted Development Rights": "Use this hub when the real question is whether permitted development still works once local restrictions, site history and project detail are checked properly.",
    "Height Limits": "Use this hub when height is the controlling issue and you need to know which measurement, project type or local page to open next.",
    "Boundary Distance Rules": "Use this hub when boundary position is the real planning issue and the answer depends more on siting than on the project label alone.",
    "Conservation Area Restrictions": "Use this hub when heritage context is the real planning issue and conservation area rules may make the usual answer less reliable.",
    "Article 4 Restrictions": "Use this hub when the real question is whether an Article 4 direction removes permitted development rights and changes the route entirely.",
    "Maximum Height Rules": "Use this hub when the live question is maximum height, which measurement point controls it and where the answer usually changes.",
}

SCENARIO_HUB_SUMMARIES = {
    "Planning Permission": "This topic usually decides whether a project still looks like a simpler permitted-development case or whether a formal application should be treated as the safer baseline.",
    "Permitted Development Rights": "This topic usually decides whether the simpler route still survives once local restrictions, site history and project detail are layered in.",
    "Conservation Area Restrictions": "This topic usually decides whether visible change, heritage character and local authority context now matter more than the generic national answer.",
    "Article 4 Restrictions": "This topic usually decides whether the shortcut route still exists at all once local policy is checked properly.",
    "Height Limits": "This topic usually decides whether the design still feels comfortably within the normal envelope or whether a measured redesign is safer.",
    "Boundary Distance Rules": "This topic usually decides whether neighbour relationship and siting are the real blockers rather than the project type itself.",
    "Maximum Height Rules": "This topic usually decides whether one controlling measurement point is already pushing the proposal into a stricter route.",
}


def build_trust_section() -> str:
    return """
<section class="trust">
<span class="eyebrow">Trust and caveats</span>
<h2>How To Use A Topic Hub Properly</h2>
<p>Topic hubs exist to isolate the one planning issue that is blocking progress. They are most useful when paired with the matching project guide and the relevant local authority page.</p>
<ul class="checklist">
<li>Start here when one rule is the real uncertainty.</li>
<li>Move to a local project page when dimensions, site history or local restrictions start to matter.</li>
<li>Verify formally if the proposal is borderline or affected by special controls.</li>
</ul>
</section>
"""


def assemble_scenario_hub_page(blocks) -> str:
    return "\n".join(block for block in blocks if block)


def build_scenario_hub_hero(scenario_title: str) -> str:
    return f"""
<section class="hero">
<span class="badge">Planning topic hub</span>
<h1>{scenario_title}</h1>
<p>{SCENARIO_HUB_INTROS.get(scenario_title, 'Use this hub when this topic is the part of the planning question that matters most. It helps you move quickly into the right project type, the right local example and the next local check worth making.')}</p>
</section>
"""


def build_project_navigation(projects, scenario_slug: str, scenario_title: str) -> str:
    cards = []

    for project in projects:
        cards.append(
            f"""
<a class="card project-card" href="/{project['slug']}/">
<div class="card-kicker">Project hub</div>
<h3>{project['short_name']}</h3>
<p>Browse guidance on {scenario_title.lower()} for {project['short_name'].lower()} projects, then move into the local pages if needed.</p>
<span class="cta">Open project hub</span>
</a>
"""
        )

    return f"""
<section class="project-navigation">
<span class="eyebrow">Choose the project type first</span>
<h2>Project Types People Usually Pair With This Topic</h2>
<div class="card-grid">{''.join(cards)}</div>
</section>
"""


def build_scenario_explanation(scenario_title: str) -> str:
    return f"""
<section class="scenario-explanation">
<span class="eyebrow">Answer-first explanation</span>
<h2>What This Topic Usually Changes</h2>
<div class="answer-grid">
<div class="answer-card">
<h3>What usually applies</h3>
<p>{SCENARIO_HUB_SUMMARIES.get(scenario_title, f'{scenario_title} can change whether planning permission is required, what can be built under permitted development, and how much confidence you can place in a simple rule of thumb.')}</p>
</div>
<div class="answer-card">
<h3>What often complicates it</h3>
<p>Local designations, site history, measured drawings and the exact project shape often matter more than people expect once this topic is in play.</p>
</div>
<div class="answer-card">
<h3>Best next step</h3>
<p>Open the matching project type first, then use the local example pages to see where this topic actually changes the route in practice.</p>
</div>
</div>
</section>
"""


def build_rule_examples(scenario_title: str) -> str:
    return f"""
<section class="rule-examples">
<span class="eyebrow">Common use cases</span>
<h2>Where {scenario_title} Usually Shows Up</h2>
<ul class="checklist">
<li>{scenario_title} affecting common extension proposals.</li>
<li>{scenario_title} influencing what can be built without a planning application.</li>
<li>{scenario_title} forcing design changes before a project proceeds.</li>
</ul>
</section>
"""


def build_example_local_guides(projects, example_councils, scenario_slug: str, scenario_title: str) -> str:
    cards = []

    for project in projects:
        for council in example_councils:
            cards.append(
                f"""
<a class="card example-card" href="/{project['slug']}/{council['county_slug']}/{council['town_slug']}/">
<div class="card-kicker">Local guide</div>
<h3>{project['short_name']} in {council['town_name']}</h3>
<p>Open the main local guide, then use the tool and local planning context to see how {scenario_title.lower()} may change the answer on the ground.</p>
<span class="cta">Open local guide</span>
</a>
"""
            )

            if len(cards) >= 8:
                return f"""
<section class="example-local-guides">
<span class="eyebrow">See it locally</span>
<h2>Example Local Rule Pages</h2>
<div class="card-grid">{''.join(cards)}</div>
</section>
"""

    return f"""
<section class="example-local-guides">
<span class="eyebrow">See it locally</span>
<h2>Example Local Rule Pages</h2>
<div class="card-grid">{''.join(cards)}</div>
</section>
"""


def build_related_scenario_links(current_slug: str, scenarios) -> str:
    links = []

    for scenario in scenarios:
        if scenario["slug"] == current_slug:
            continue

        links.append(
            f"""
<a class="card related-card" href="/{scenario['slug']}/">
<div class="card-kicker">Related topic</div>
<h3>{scenario['title']}</h3>
<p>Open a connected planning topic when the first question turns into a different kind of constraint.</p>
<span class="cta">Open topic</span>
</a>
"""
        )

    return f"""
<section class="related-scenarios">
<span class="eyebrow">Useful next topic hubs</span>
<h2>Related Topics If The First Constraint Leads To Another One</h2>
<div class="card-grid">{''.join(links)}</div>
</section>
"""


def build_planning_law_context(scenario_title: str) -> str:
    return f"""
<section class="planning-law-context">
<span class="eyebrow">Method and legal context</span>
<h2>{scenario_title} In The Wider Planning Picture</h2>
<p>This topic is shaped by national planning legislation, permitted development rights and local authority interpretation where protected areas or policy constraints apply.</p>
<p>Checking both the national baseline and the local council context gives a more reliable view of whether a project can proceed as planned.</p>
</section>
"""
