from utils.live_links import is_live_internal_href, normalize_internal_href
from utils.project_scenario_config import project_scenario_href, rollout_scenarios_for_project
from components.trust_framework import build_trust_framework, planning_system_label


def slug_to_name(slug: str) -> str:
    return slug.replace("-", " ").title()


def _project_focus(project_name: str) -> str:
    lowered = str(project_name or "").lower()
    if any(token in lowered for token in ("hmo", "change of use")):
        return "use"
    if any(token in lowered for token in ("dropped kerb", "driveway", "hard surfacing", "fence", "wall")):
        return "frontage"
    if any(token in lowered for token in ("loft", "dormer", "roof")):
        return "loft"
    if any(token in lowered for token in ("garden room", "outbuilding", "annexe", "garage")):
        return "outbuilding"
    return "extension"


def _scenario_card_label(title: str) -> str:
    clean = str(title or "").strip().lower()
    if clean == "boundary distance rules":
        return "boundary rules"
    return clean


def _scenario_card_verb(label: str) -> str:
    return "are" if str(label or "").lower().endswith("s") else "is"


def build_county_project_jump_links(project_name: str, county_name: str) -> str:
    return f"""
<section class="page-jump-links">
<span class="eyebrow">Jump to what matters</span>
<h2>Read This Area Project Page In The Order That Saves You Time</h2>
<div class="link-grid">
<a href="#county-project-summary">Start with the quick answer for {project_name.lower()} across {county_name}</a>
<a href="#county-project-decision-guide">See when an area comparison is enough and when you should go local</a>
<a href="#county-project-councils">Open the local authority guides that matter most</a>
<a href="#county-project-topics">Check the rules most likely to change the answer</a>
<a href="#county-project-next-steps">Use the strongest next tools and follow-ups</a>
<a href="#county-project-trust">Read the trust notes if the route still feels borderline</a>
</div>
</section>
"""


def build_county_project_hero(project_name: str, county_name: str, council_count: int) -> str:
    focus = _project_focus(project_name)
    intro = {
        "use": f"Use this page to compare how {project_name.lower()} shifts across {council_count} council areas in {county_name} once local policy, Article 4, amenity pressure and council appetite start to matter.",
        "frontage": f"Use this page to compare the local authority layer for {project_name.lower()} across {council_count} council areas in {county_name}, especially where frontage, access, drainage or highway-side friction changes the practical route.",
        "outbuilding": f"Use this page to compare how {project_name.lower()} is treated across {council_count} council areas in {county_name} once height, siting, original-house baseline and incidental-use questions are layered in.",
        "loft": f"Use this page to compare how {project_name.lower()} shifts across {council_count} council areas in {county_name} once roof form, visibility and local sensitivity start to matter.",
    }.get(
        focus,
        f"Use this page to compare the local authority layer for {project_name.lower()} across {council_count} council areas in {county_name}, find the councils worth checking first and open the rule pages that usually change the answer.",
    )
    return f"""
<section class="hero">
<span class="badge">Area project hub</span>
<h1>{project_name} Across {county_name}</h1>
<p>{intro}</p>
</section>
"""


def build_county_project_summary(project_name: str, county_name: str, council_count: int) -> str:
    focus = _project_focus(project_name)
    changes = {
        "use": "Article 4, local policy wording, amenity pressure, parking standards and concentration concerns can all move the answer quickly across neighbouring councils.",
        "frontage": "Highway approval, frontage visibility, crossover design, drainage and visible street-facing changes can make one authority route feel much stricter than another.",
        "outbuilding": "Height, boundary siting, incidental-versus-separate use, previous additions and local heritage controls can all change the route.",
        "loft": "Roof form, street visibility, heritage sensitivity, ridge/eaves assumptions and previous roof changes can all shift the local answer.",
    }.get(
        focus,
        "Conservation areas, Article 4, listed buildings, local design expectations and the exact dimensions of the scheme can all change the route.",
    )
    next_step = {
        "use": f"Compare the {council_count} council areas below, then open the local project guide and the local rule pages that clarify policy, Article 4 and the practical next step for your site.",
        "frontage": f"Compare the {council_count} council areas below, then open the local project guide and the route pages that separate planning permission from the wider access or frontage checks.",
        "outbuilding": f"Compare the {council_count} council areas below, then open the local project guide and the rule page that best isolates height, siting or use risk for your site.",
        "loft": f"Compare the {council_count} council areas below, then open the local project guide and the roof-led rule pages that are most likely to decide the answer.",
    }.get(
        focus,
        f"Compare the {council_count} council areas below, then open the local project guide and the rule page that looks most likely to decide the answer for your site.",
    )
    return f"""
<section id="county-project-summary">
<span class="eyebrow">Quick area answer</span>
<h2>What This Area Project Page Helps You Decide</h2>
<div class="answer-grid">
<div class="answer-card">
<h3>Broad read</h3>
<p>Area comparison is useful when you are still deciding which council deserves the closer look, not when one exact site is already doing all the work.</p>
</div>
<div class="answer-card">
<h3>What often changes it</h3>
<p>{changes}</p>
</div>
<div class="answer-card">
<h3>Best next step</h3>
<p>{next_step}</p>
</div>
</div>
</section>
"""


def build_county_project_decision_guide(project_name: str, county_name: str) -> str:
    return f"""
<section class="decision-guide" id="county-project-decision-guide">
<span class="eyebrow">Decision guide</span>
<h2>When This Area Comparison Usually Helps And When You Should Go Straight To A Local Page</h2>
<div class="answer-grid">
<div class="answer-card">
<h3>Usually enough for a first pass when</h3>
<ul class="checklist">
<li>You are still comparing councils and have not narrowed the project to one site-specific route yet.</li>
<li>The uncertainty is about where {project_name.lower()} feels more sensitive rather than whether one exact drawing already works.</li>
<li>You want to understand the likely local pressure points before paying for more detailed design work.</li>
</ul>
</div>
<div class="answer-card">
<h3>Go more local when</h3>
<ul class="checklist">
<li>One council area, one conservation area or one exact property constraint is already doing most of the work.</li>
<li>The scheme is close to a height, boundary, roof or visibility limit.</li>
<li>You need a reliable route decision rather than a comparison-led briefing.</li>
</ul>
</div>
<div class="answer-card">
<h3>What usually settles it faster</h3>
<ul class="checklist">
<li>Open the matching local project guide for the correct council below.</li>
<li>Pair it with the rule page that looks most likely to block or change the route.</li>
<li>If the scheme is borderline, move to measured drawings and written confirmation rather than relying on comparison alone.</li>
</ul>
</div>
</div>
</section>
"""


def build_council_navigation(councils, project_slug: str, county_slug: str, project_name: str) -> str:
    cards = []

    for council in councils:
        town_slug = council["town_slug"]
        town_name = council["town_name"]
        href = normalize_internal_href(f"/{project_slug}/{county_slug}/{town_slug}/")
        if not is_live_internal_href(href):
            continue

        cards.append(
            f"""
<a class="card council-card" href="{href}">
<div class="card-kicker">Local project page</div>
<h3>{town_name}</h3>
<p>Check the local planning route, restriction signals and next steps for {project_name.lower()} in {town_name}.</p>
<span class="cta">Open local guide</span>
</a>
"""
        )

    return f"""
<section class="council-navigation" id="county-project-councils">
<span class="eyebrow">Compare by local authority</span>
<h2>The Councils To Compare For {project_name}</h2>
<div class="card-grid">{''.join(cards)}</div>
</section>
"""


def build_county_planning_topics(
    scenarios,
    project_slug: str,
    county_slug: str,
    councils,
    project_name: str,
    county_name: str,
) -> str:
    cards = []
    local_rollout = rollout_scenarios_for_project(project_slug)
    ordered_scenarios = local_rollout or scenarios

    for scenario in ordered_scenarios[:6]:
        town = councils[len(cards) % len(councils)] if councils else {}
        example_town = town.get("town_name", county_name)
        town_slug = town.get("town_slug", "")
        scenario_label = _scenario_card_label(scenario["title"])
        scenario_verb = _scenario_card_verb(scenario_label)
        href = project_scenario_href(project_slug, county_slug, town_slug, scenario["slug"]) or normalize_internal_href(
            f"/{scenario['slug']}/"
        )
        if not is_live_internal_href(href):
            continue
        cards.append(
            f"""
<a class="card" href="{href}">
<div class="card-kicker">Rule route</div>
<h3>{scenario['title']}</h3>
<p>Useful when {scenario_label} {scenario_verb} the question most likely to change the answer for {project_name.lower()} in places like {example_town}.</p>
<span class="cta">Open strongest local route</span>
</a>
"""
        )

    return f"""
<section class="planning-topics" id="county-project-topics">
<span class="eyebrow">Rule-first route</span>
<h2>{project_name} Topics Worth Checking Across {county_name}</h2>
<div class="card-grid">{''.join(cards)}</div>
</section>
"""


def build_county_planning_context(project_name: str, county_name: str) -> str:
    return f"""
<section class="planning-context" id="county-project-context">
<span class="eyebrow">Why area comparison helps</span>
<h2>How The Same Project Can Feel Different Across One Planning Area</h2>
<p>Planning rules for {project_name.lower()} in {county_name} may start from the same national footing, but the confidence you can place in that footing changes once local designations, property context and authority interpretation enter the picture.</p>
<p>This area hub is there to show where the answer still looks routine, where it tightens up and which council page is worth the deeper read.</p>
</section>
"""


def build_regional_planning_insights(county_name: str) -> str:
    return f"""
<section class="regional-insights" id="county-project-insights">
<span class="eyebrow">Common area-wide tripwires</span>
<h2>What Usually Deserves A Closer Look In {county_name}</h2>
<ul class="checklist">
<li>Urban and heritage-sensitive authority areas often feel stricter even where the national rule sounds similar.</li>
<li>Projects close to a boundary, roof limit or visual-impact threshold are more likely to need a careful local check.</li>
<li>Where the route still feels uncertain, comparing one or two neighbouring councils often clarifies whether the issue is policy, heritage, scale or pure site context.</li>
</ul>
</section>
"""


def build_scenario_links(project_slug: str, county_slug: str, councils, scenarios) -> str:
    links = []
    project_label = project_slug.replace("-", " ").title()
    local_rollout = rollout_scenarios_for_project(project_slug)
    ordered_scenarios = local_rollout or scenarios

    for council in councils[:3]:
        town_slug = council["town_slug"]
        town_name = council["town_name"]
        for scenario in ordered_scenarios[:3]:
            href = project_scenario_href(project_slug, county_slug, town_slug, scenario["slug"]) or normalize_internal_href(
                f"/{scenario['slug']}/{town_slug}/"
            )
            if not is_live_internal_href(href):
                continue
            links.append(
                f'<a href="{href}">{scenario["title"]} for {project_label} in {town_name}</a>'
            )

    return f"""
<section class="scenario-links">
<span class="eyebrow">Useful local follow-ups</span>
<h2>Rule Pages That Usually Decide The Next Step</h2>
<div class="link-grid">{''.join(links[:12])}</div>
</section>
"""


def build_nearby_county_links(project_slug: str, county_slugs, current_county_slug: str, project_name: str) -> str:
    cards = []

    for slug in county_slugs:
        if slug == current_county_slug:
            continue

        county_name = slug.replace("-", " ").title()

        href = normalize_internal_href(f"/{project_slug}/{slug}/")
        if not is_live_internal_href(href):
            continue
        cards.append(
            f"""
<a class="card county-card" href="{href}">
<div class="card-kicker">Area comparison</div>
<h3>{county_name}</h3>
<p>Compare {project_name.lower()} guidance in {county_name} when you want broader local context.</p>
<span class="cta">Compare area</span>
</a>
"""
        )

        if len(cards) >= 8:
            break

    return f"""
<section class="nearby-counties">
<span class="eyebrow">Broader comparison</span>
<h2>Nearby Area Project Hubs</h2>
<div class="card-grid">{''.join(cards)}</div>
</section>
"""


def build_related_project_links(projects, current_project_slug: str) -> str:
    cards = []

    for project in projects:
        slug = project["slug"]
        title = project["title"]

        if slug == current_project_slug:
            continue
        href = normalize_internal_href(f"/{slug}/")
        if not is_live_internal_href(href):
            continue

        cards.append(
            f"""
<a class="card" href="{href}">
<div class="card-kicker">Related project hub</div>
<h3>{title}</h3>
<p>Switch project type if the build you are planning has drifted into a different planning route.</p>
<span class="cta">Open project hub</span>
</a>
"""
        )

        if len(cards) >= 6:
            break

    return f"""
<section class="related-projects">
<span class="eyebrow">Project alternatives</span>
<h2>Related Project Hubs If The Brief Has Shifted</h2>
<div class="card-grid">{''.join(cards)}</div>
</section>
"""


def build_next_steps(project_slug: str, county_slug: str, county_name: str) -> str:
    focus = _project_focus(project_slug.replace("-", " "))
    if focus == "use":
        primary_title = "Map the policy and permission route"
        primary_description = "Use the route planner when the live question is whether policy, Article 4 or a fuller application route is doing most of the work."
        primary_href = "/tools/planning-route-planner/"
        primary_cta = "Plan route"
        secondary_title = "Check the local constraints first"
        secondary_description = "Use the constraint checker when site-specific controls may decide the route faster than another broad comparison."
        secondary_href = "/tools/site-constraint-checker/"
        secondary_cta = "Check constraints"
    elif focus == "frontage":
        primary_title = "Check the site and frontage constraints"
        primary_description = "Use the constraint checker when visibility, drainage, frontage design or access geometry may be the real blocker."
        primary_href = "/tools/site-constraint-checker/"
        primary_cta = "Check constraints"
        secondary_title = "Map the approval route"
        secondary_description = "Use the route planner when planning permission and the wider access route need separating cleanly."
        secondary_href = "/tools/planning-route-planner/"
        secondary_cta = "Plan route"
    else:
        primary_title = "Build a cleaner prep pack"
        primary_description = "Use the project requirements generator when you want the documents, checks and follow-up work arranged in a safer order."
        primary_href = "/tools/project-requirements-generator/"
        primary_cta = "Build prep pack"
        secondary_title = "Run the quick planning tool"
        secondary_description = "Use the main planning decision tool when you need a first steer before comparing the local pages in detail."
        secondary_href = "/tools/planning-decision-tool/"
        secondary_cta = "Open tool"
    return f"""
<section class="local-actions" id="county-project-next-steps">
<span class="eyebrow">Strong next actions</span>
<h2>What To Do If You Still Need A Faster Answer</h2>
<div class="grid">
<a class="card" href="{primary_href}">
<div class="card-kicker">Primary next step</div>
<h3>{primary_title}</h3>
<p>{primary_description}</p>
<span class="cta">{primary_cta}</span>
</a>
<a class="card" href="{secondary_href}">
<div class="card-kicker">Useful second move</div>
<h3>{secondary_title}</h3>
<p>{secondary_description}</p>
<span class="cta">{secondary_cta}</span>
</a>
<a class="card" href="/tools/planning-rejection-risk-analyzer/">
<div class="card-kicker">Risk tool</div>
<h3>Analyse the likely refusal risks</h3>
<p>Use the risk analyzer when the proposal is taking shape and you want to stress-test the main reasons it could be refused.</p>
<span class="cta">Open analyzer</span>
</a>
<a class="card" href="/{county_slug}/">
<div class="card-kicker">Area guide</div>
<h3>See the wider {county_name} planning hub</h3>
<p>Use the area page to switch from this project to broader council and topic navigation.</p>
<span class="cta">Open area hub</span>
</a>
<a class="card" href="/planning-faq/do-i-need-planning-permission/">
<div class="card-kicker">FAQ</div>
<h3>Read the core planning permission answer</h3>
<p>Open the FAQ when the uncertainty is still about the overall route rather than the local layer.</p>
<span class="cta">Read answer</span>
</a>
</div>
</section>
"""


def build_trust_section(project_title: str, county_name: str) -> str:
    return build_trust_framework(
        section_id="county-project-trust",
        title="How To Use This Area Project Guide Responsibly",
        purpose=f"This page helps you compare {project_title.lower()} guidance across {county_name} so you can identify which local authority path, rule page and verification step deserve attention first.",
        not_replace="It does not replace the council-specific project guide, the exact property checks or any formal confirmation needed for a borderline scheme.",
        built_from=f"The comparison sits on the same {planning_system_label(county_name)} baseline across the area, then focuses on the local authority differences most likely to change the route in practice.",
        verify_when="Stop relying on area comparison alone once one council, one conservation-area issue, one Article 4 question or one measured threshold is clearly doing most of the work.",
        safest_next_step="Open the matching local project guide first. If the route still looks borderline, move to measured drawings and then to a lawful development certificate, pre-application advice or another formal check as needed.",
    )


def assemble_county_project_page(components) -> str:
    return "\n".join(c for c in components if c)


def build_county_project_support_sections(*sections: str) -> str:
    content = "".join(section for section in sections if section)
    if not content:
        return ""
    return f"""
<section class="support-stack">
<span class="eyebrow">Deeper comparison routes</span>
<h2>More Area Comparisons And Related Follow-Ups</h2>
<p class="section-lead">Use these only after the local authority route and main next steps above. They are helpful, but they should not compete with the primary answer.</p>
<details class="support-disclosure">
<summary>Show more rule comparisons, nearby area hubs and related project alternatives</summary>
{content}
</details>
</section>
"""
