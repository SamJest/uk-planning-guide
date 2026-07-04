MAX_PROJECT_LINKS = 12
MAX_NEARBY_COUNCILS = 8
MAX_SCENARIO_LINKS = 6
MAX_RELATED_PROJECTS = 6
from components.faq_blocks import build_faq_section
from components.jurisdiction_notices import build_jurisdiction_notice
from components.personalised_guidance import build_personalised_guidance_cta
from components.trust_framework import build_trust_framework, planning_system_label
from utils.live_links import is_live_internal_href, normalize_internal_href

PRIORITY_PROJECT_ORDER = [
    "garden-rooms",
    "fences-and-walls",
    "outbuildings",
    "house-extensions",
    "dropped-kerbs",
    "loft-conversions",
    "driveways",
]


def _scenario_card_label(title: str) -> str:
    clean = str(title or "").strip().lower()
    if clean == "boundary distance rules":
        return "boundary rules"
    return clean


def _scenario_card_verb(label: str) -> str:
    return "are" if str(label or "").lower().endswith("s") else "is"

PRIORITY_SCENARIO_ORDER = [
    "planning-permission",
    "permitted-development",
    "boundary-rules",
    "height-limits",
    "conservation-areas",
    "article-4",
]

COUNCIL_ROUTE_CONTEXT_VARIANTS = [
    "Use it to choose the right project, rule or council source before paying for drawings or advice.",
    "Start here when the authority area matters more than one national rule headline.",
    "Use the page to move from a broad council search into the project or topic that actually decides the answer.",
    "Treat this as the local check that helps you avoid opening the wrong detailed guide first.",
    "Use it to compare the authority context with the project-specific guidance before treating the answer as settled.",
    "Start with the council layer, then narrow into the rule or project page that best matches the proposal.",
    "Use this guide to keep local policy, official sources and project checks in the same decision path.",
    "Open this first when the location is clear but the exact route still needs sorting.",
]


def _sort_projects(projects):
    priority_index = {slug: index for index, slug in enumerate(PRIORITY_PROJECT_ORDER)}
    return sorted(
        projects,
        key=lambda item: (
            priority_index.get(item.get("slug", ""), len(priority_index) + 1),
            item.get("short_name", item.get("title", "")),
        ),
    )


def _sort_scenarios(scenarios):
    priority_index = {slug: index for index, slug in enumerate(PRIORITY_SCENARIO_ORDER)}
    return sorted(
        scenarios,
        key=lambda item: (
            priority_index.get(item.get("slug", ""), len(priority_index) + 1),
            item.get("title", ""),
        ),
    )


def _restriction_focus(restriction_checks) -> str:
    joined = " ".join(label.lower() for label, _ in (restriction_checks or [])[:4])
    if "article 4" in joined or "hmo" in joined:
        return "policy"
    if "listed" in joined or "conservation" in joined:
        return "heritage"
    return "general"


def build_council_hero(town_name: str, county_name: str) -> str:
    variant_index = sum(ord(char) for char in f"{town_name}|{county_name}") % len(COUNCIL_ROUTE_CONTEXT_VARIANTS)
    route_context = COUNCIL_ROUTE_CONTEXT_VARIANTS[variant_index]
    intro = (
        f"Use this page when your real search is planning permission in {town_name}. A general answer only helps until one project, one restriction or one council check starts doing most of the work. {route_context}"
    )
    return f"""
<section class="hero">
<span class="badge">Local planning authority guide</span>
<h1>Planning Permission In {town_name}</h1>
<p>{intro}</p>
<p>If the build type is already clear, open the matching local project guide first. If it is not, use the local rule and council routes below before paying for drawings, quotes or an application route in {town_name}, {county_name}.</p>
</section>
"""


def build_council_jump_links(town_name: str) -> str:
    return f"""
<section class="page-jump-links">
<span class="eyebrow">Jump to what matters</span>
<h2>Use This Council Page In The Order That Saves You Time</h2>
<div class="link-grid">
<a href="#council-summary">Start with the quick local summary for {town_name}</a>
<a href="#council-start">Use the fastest project, topic and tool routes first</a>
<a href="#projects">Open project guides if the build type is already clear</a>
<a href="#council-topics">Check the local planning topics if one rule is the blocker</a>
<a href="#council-process">Use the practical next-step sequence before you spend money</a>
<a href="#council-trust">Read the trust notes if the answer is still borderline</a>
</div>
</section>
"""


def build_council_jurisdiction_notice(town_name: str, county_slug: str) -> str:
    return build_jurisdiction_notice(county_slug, town_name, "local authority guide")


def build_start_here_section(town_name: str, county_slug: str, town_slug: str, priority_project_checks) -> str:
    lead_project = priority_project_checks[0]["href"] if priority_project_checks else f"/house-extensions/{county_slug}/{town_slug}/"
    if not is_live_internal_href(lead_project):
        lead_project = "/councils/"
    topic_href = normalize_internal_href(f"/planning-permission/{town_slug}/")
    if not is_live_internal_href(topic_href):
        topic_href = "/planning-permission/"
    return f"""
<section class="start-here-local" id="council-start">
<span class="eyebrow">Start here in this authority</span>
<h2>The Best First Clicks From {town_name} Planning Searches</h2>
<div class="grid">
<a class="card" href="{lead_project}">
<div class="card-kicker">Project path</div>
<h3>Open the most likely local project guide</h3>
<p>Best when the build type is already clear and you want the fastest route to the local answer, not another general council summary.</p>
<span class="cta">Open project guide</span>
</a>
<a class="card" href="{topic_href}">
<div class="card-kicker">Local topic path</div>
<h3>Open planning permission in {town_name}</h3>
<p>Use the local topic page when the route question matters more than one exact build type or one project detail.</p>
<span class="cta">Open local topic page</span>
</a>
<a class="card" href="/planning-faq/do-i-need-planning-permission/">
<div class="card-kicker">FAQ path</div>
<h3>Read the route-level answer</h3>
<p>Useful when the search intent is still broad and needs narrowing before you choose the wrong local page.</p>
<span class="cta">Read answer</span>
</a>
<a class="card" href="/tools/planning-decision-tool/">
<div class="card-kicker">Tool path</div>
<h3>Run the quick planning tool</h3>
<p>Use the tool when you want a faster first steer before opening multiple detailed local pages.</p>
<span class="cta">Open tool</span>
</a>
</div>
</section>
"""


def build_local_decision_summary(town_name, county_name, project_checks, restriction_checks):
    focus = _restriction_focus(restriction_checks)
    restriction_html = (
        "<ul class='checklist'>" + "".join(f"<li><strong>{label}:</strong> {text}</li>" for label, text in restriction_checks[:3]) + "</ul>"
        if restriction_checks
        else "<p>No standout local restriction note is surfaced in this sampled data, but conservation area, listed building and Article 4 checks are still worth confirming before you rely on the baseline answer.</p>"
    )
    broad_answer = {
        "heritage": f"The national planning answer is only a starting point in {town_name} when heritage controls, conservation areas or listed-building issues are doing most of the work.",
        "policy": f"The broad planning answer in {town_name} becomes less reliable when policy, Article 4 or council-specific controls are the real reasons the route may change.",
    }.get(
        focus,
        f"Planning permission in {town_name} is rarely one answer for every project. The local authority layer matters once one project type, one restriction or one borderline measurement starts driving the route.",
    )

    return f"""
<section id="council-summary">
<span class="eyebrow">Quick local summary</span>
<h2>What A Broad {town_name} Planning Search Usually Needs Next</h2>
<div class="answer-grid">
<div class="answer-card">
<h3>Working answer</h3>
<p>{broad_answer}</p>
</div>
<div class="answer-card">
<h3>What often changes the answer</h3>
{restriction_html}
</div>
<div class="answer-card">
<h3>Best next step</h3>
<ul class="checklist">
<li>If the build type is clear, open that local project guide first.</li>
<li>If the blocker is still broad, switch to the local planning-permission or rule page next.</li>
<li>If the answer only works on a borderline measurement or sensitive designation, stop reading and verify formally.</li>
</ul>
</div>
</div>
</section>
"""


def build_local_authority_faq(town_name: str, restriction_checks, project_checks) -> str:
    restriction_labels = [label.lower() for label, _text in (restriction_checks or [])[:2]]
    if restriction_labels:
        local_tripwires = (
            f"In {town_name}, the main local tripwires currently surfaced here are "
            f"{' and '.join(restriction_labels)}."
        )
    else:
        local_tripwires = (
            f"In {town_name}, the main local tripwires are usually conservation areas, listed-building issues, "
            "Article 4 and any proposal that only works if a measurement lands comfortably inside the limit."
        )

    lead_project = project_checks[0]["title"].lower() if project_checks else "the matching local project guide"
    faq_items = [
        (
            "Why can the local authority layer change the normal answer?",
            f"Because the national rule-of-thumb does not remove the need to check local policy, heritage controls, Article 4 and how the council applies those issues in {town_name}.",
        ),
        (
            "Are Article 4 directions or conservation areas the main tripwires here?",
            local_tripwires,
        ),
        (
            "Should I check local validation requirements before applying?",
            f"Yes. Once a proposal in {town_name} is drifting toward a formal application, it is worth checking the local validation expectations before you pay for the wrong drawing or document package.",
        ),
        (
            "When is the national answer still fairly reliable here?",
            "When the project is routine, comfortably inside the main limits and not affected by a conservation area, listed-building issue, Article 4 or awkward planning history.",
        ),
        (
            "What is the safest next local check?",
            f"Open {lead_project} first if the work type is already clear, then move into the relevant rule page or formal verification route if the answer still feels borderline.",
        ),
    ]
    return build_faq_section(
        faq_items,
        section_id="council-faq",
        eyebrow="Local FAQ",
        title="Questions People Usually Ask About The Local Layer",
        intro=f"Use this compact block to resolve the local objections and follow-up questions that usually appear after the broad planning answer has been narrowed for {town_name}.",
    )


def build_council_conversion_hook(town_name: str, project_checks) -> str:
    lead_title = project_checks[0]["title"] if project_checks else "the right local guide"
    variant_index = sum(ord(char) for char in town_name) % len(COUNCIL_ROUTE_CONTEXT_VARIANTS)
    route_context = COUNCIL_ROUTE_CONTEXT_VARIANTS[variant_index]
    description = (
        f"If the answer in {town_name} is clearer than before but you still need help choosing between the council context, {lead_title.lower()} or a formal next step, use personalised guidance after the quick checks. {route_context}"
    )
    return build_personalised_guidance_cta(
        title=f"Need A Cleaner Local Planning Read For {town_name}?",
        description=description,
        context_label="council-page",
        email_context=f"Planning permission in {town_name}",
        intro_label="Local route check",
        compact=True,
        prefill={
            "authority": town_name,
            "location": town_name,
            "project_stage": "Just exploring the route",
            "project_summary": f"Planning permission route in {town_name}",
            "main_worry": description,
        },
    )


def build_project_navigation(projects, town_name, county_slug, town_slug):
    cards = []

    for project in _sort_projects(projects)[:MAX_PROJECT_LINKS]:
        href = normalize_internal_href(f"/{project['slug']}/{county_slug}/{town_slug}/")
        if not is_live_internal_href(href):
            continue
        cards.append(
            f"""
<a class="card project-card" href="{href}">
<div class="card-kicker">Local project guide</div>
<h3>{project['short_name']}</h3>
<p>Open the answer-first guide for {project['short_name'].lower()} in {town_name}.</p>
<span class="cta">Open local guide</span>
</a>
"""
        )

    return f"""
<section id="projects">
<span class="eyebrow">Project-first navigation</span>
<h2>Project Guides Worth Opening In {town_name}</h2>
<div class="project-grid">{''.join(cards)}</div>
</section>
"""


def build_priority_project_checks(project_checks, town_name):
    cards = []

    for check in project_checks:
        href = normalize_internal_href(check.get("href", ""))
        if not is_live_internal_href(href):
            continue
        cards.append(
            f"""
<a class="card project-card" href="{href}">
<div class="card-kicker">Best local starting point</div>
<h3>{check['title']} in {town_name}</h3>
<p>{check['summary']}</p>
<span class="cta">Check this guide</span>
</a>
"""
        )

    if not cards:
        return ""

    return f"""
<section id="council-topics">
<span class="eyebrow">High-value starting pages</span>
<h2>Local Guides People Usually Need First</h2>
<div class="project-grid">{''.join(cards)}</div>
</section>
"""


def build_common_planning_topics(projects, scenarios, county_slug, town_slug, town_name):
    cards = []

    for scenario in _sort_scenarios(scenarios)[:MAX_SCENARIO_LINKS]:
        href = normalize_internal_href(f"/{scenario['slug']}/{town_slug}/")
        if not is_live_internal_href(href):
            continue
        scenario_label = _scenario_card_label(scenario["title"])
        scenario_verb = _scenario_card_verb(scenario_label)
        cards.append(
            f"""
<a class="card" href="{href}">
<div class="card-kicker">Local topic page</div>
<h3>{scenario['title']}</h3>
<p>Use this when {scenario_label} {scenario_verb} the rule most likely to decide the answer in {town_name}.</p>
<span class="cta">Open local topic page</span>
</a>
"""
        )

    return f"""
<section>
<span class="eyebrow">Rule-first route</span>
<h2>Planning Topics Worth Checking In {town_name}</h2>
<div class="grid">{''.join(cards)}</div>
</section>
"""


def build_local_planning_context(town_name, county_name):
    system_label = "English planning system"
    if county_name.lower() == "wales":
        system_label = "Welsh planning system"
    elif county_name.lower() == "scotland":
        system_label = "Scottish planning system"
    elif county_name.lower() == "northern ireland":
        system_label = "Northern Ireland planning system"
    return f"""
<section id="planning-context">
<span class="eyebrow">Why local pages matter</span>
<h2>How The Local Authority Layer Changes The Planning Question</h2>
<p>The {system_label} sets the baseline for many home projects, but local policy, conservation areas and Article 4 directions can still change what is allowed in {town_name}, {county_name}.</p>
<p>That is why similar projects can follow different routes depending on the street, the property history and whether the site sits in a more restricted part of the authority.</p>
</section>
"""


def build_planning_process_section(town_name):
    return f"""
<section id="council-process">
<span class="eyebrow">Practical next-step flow</span>
<h2>Before You Spend Money In {town_name}</h2>
<ol>
<li>Open the project guide that matches the work you are actually planning.</li>
<li>Check the local restriction signals affecting {town_name}, especially heritage designations and Article 4.</li>
<li>If the proposal is close to a limit, get measured drawings ready and consider written confirmation before work starts.</li>
</ol>
</section>
"""


def build_planning_examples(town_name):
    return f"""
<section id="council-trust">
<span class="eyebrow">Common decision patterns</span>
<h2>What Usually Triggers A Closer Check In {town_name}</h2>
<ul class="checklist">
<li>Householder extensions where scale, height or neighbour impact start to look aggressive.</li>
<li>Loft and roof proposals where roof alterations or visual impact matter more than expected.</li>
<li>Outbuildings, driveways and boundary-facing work where siting and local restrictions change the answer quickly.</li>
</ul>
</section>
"""


def build_scenario_links(projects, scenarios, county_slug, town_slug, town_name):
    links = []

    for scenario in _sort_scenarios(scenarios)[:MAX_SCENARIO_LINKS]:
        href = normalize_internal_href(f"/{scenario['slug']}/{town_slug}/")
        if not is_live_internal_href(href):
            continue
        links.append(
            f"""
<a href="{href}">
{scenario['title']} in {town_name}
</a>
"""
        )

    return f"""
<section>
<span class="eyebrow">Useful local rule guides</span>
<h2>The Rule Pages Most Likely To Answer The Follow-Up Question</h2>
<div class="link-grid">{''.join(links[:MAX_SCENARIO_LINKS])}</div>
</section>
"""


def build_nearby_council_links(councils_by_county, county_slug, town_slug):
    links = []

    for council in councils_by_county.get(county_slug, []):
        if council["town_slug"] == town_slug:
            continue
        href = normalize_internal_href(f"/councils/{council['town_slug']}/")
        if not is_live_internal_href(href):
            continue

        links.append(
            f'<a href="{href}">{council["town_name"]}</a>'
        )

        if len(links) >= MAX_NEARBY_COUNCILS:
            break

    return f"""
<section>
<span class="eyebrow">Compare nearby authorities</span>
<h2>Local Authorities Worth Comparing</h2>
<div class="link-grid">{''.join(links)}</div>
</section>
"""


def build_related_projects(projects):
    items = []
    for project in _sort_projects(projects)[:MAX_RELATED_PROJECTS]:
        href = normalize_internal_href(f'/{project["slug"]}/')
        if not is_live_internal_href(href):
            continue
        items.append(f'<a href="{href}">{project["short_name"]}</a>')

    return f"""
<section>
<span class="eyebrow">Broader site routes</span>
<h2>Project Hubs To Use If The Work Type Changes</h2>
<div class="link-grid">{''.join(items)}</div>
</section>
"""


def build_trust_section(town_name, county_name):
    return build_trust_framework(
        section_id="council-trust",
        title="Why This Local Authority Guide Is Useful Without Overclaiming",
        purpose=f"This page is designed to help you narrow the planning question in {town_name} before you spend time on drawings or an application, then push you toward the project, rule and verification route that matters most.",
        not_replace="It does not replace the council record, designation checks, or any formal confirmation needed when the route is close, sensitive or financially important.",
        built_from=f"The guide combines the {planning_system_label(county_name)} baseline with {town_name} local authority context, then highlights the project types and local rules most likely to change the answer in practice.",
        verify_when="Verify formally if the project is close to a hard limit, if the property may be listed or in a conservation area, or if Article 4 or another local restriction may decide the outcome.",
        safest_next_step="Open the matching local project guide first. If the answer is still finely balanced, move to a lawful development certificate, pre-application advice or another formal check rather than relying on one council summary.",
    )


def assemble_council_page(components):
    return "\n".join(component for component in components if component)
