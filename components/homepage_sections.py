from typing import Any

from components.find_help_pages import build_find_help_cta
from components.page_authority import build_authority_summary_section
from data.faq_data import HOMEPAGE_FAQS
from data.local_search_pages import LOCAL_SEARCH_PAGES
from data.promoted_links import PLANNING_TOPIC_LINKS, RETURN_VISIT_CARDS, START_HERE_CARDS
from data.tools_data import load_tools
from components.personalised_guidance import build_personalised_guidance_cta
from utils.random_tools import get_month_year


FEATURED_PROJECT_LIMIT = 6
FEATURED_TOWN_LIMIT = 9
FEATURED_GUIDE_LIMIT = 9
TOPIC_LIMIT = 6
LOCAL_COUNTY_LIMIT = 8
TOP_TOWN_LIMIT = 6
LOCAL_SEARCH_LIMIT = 6


def rank_projects_for_homepage(projects):
    priority_keywords = [
        "extension",
        "loft",
        "garage",
        "garden",
        "driveway",
        "outbuilding",
        "solar",
        "heat pump",
        "hmo",
    ]

    def score(project: dict[str, Any]) -> int:
        title = project.get("title", "").lower()
        return sum(10 for keyword in priority_keywords if keyword in title)

    return sorted(projects, key=score, reverse=True)


def rank_towns_for_homepage(towns):
    major_towns = {
        "cardiff",
        "city-of-edinburgh",
        "glasgow-city",
        "aberdeen-city",
        "dundee-city",
        "newport",
        "swansea",
        "wrexham",
        "barking-and-dagenham",
        "croydon",
        "guildford",
        "york",
    }

    def score(town):
        return 100 if town["town_slug"] in major_towns else 10

    return sorted(towns, key=score, reverse=True)


def _build_card(title: str, description: str, href: str, cta: str, kicker: str = "") -> str:
    kicker_html = f"<div class='card-kicker'>{kicker}</div>" if kicker else ""
    return f"""
<a class="card" href="{href}">
{kicker_html}
<h3>{title}</h3>
<p>{description}</p>
<span class="cta">{cta}</span>
</a>
"""


def _project_cta(project_slug: str) -> str:
    if "extension" in project_slug:
        return "Check extension rules"
    if "loft" in project_slug:
        return "Check loft rules"
    if "garage" in project_slug:
        return "Check garage rules"
    if "garden" in project_slug:
        return "Check garden room rules"
    return "Open guide"


def build_homepage_hero(project_count: int, town_count: int, tool_count: int) -> str:
    return f"""
<section class="hero">
<img src="/assets/images/logo-header.png" class="hero-logo" alt="UK Planning Guide">
<span class="badge">Practical planning help for real decisions</span>
<h1>Check The Planning Route Before You Pay For The Wrong Next Step</h1>
<p>Use project guides, local authority context, topic hubs and planning tools to work out the likely route, see what could change it locally and choose the next check before drawings, quotes or applications start to cost real money.</p>
<div class="hero-ctas">
<a class="btn" href="/tools/planning-route-check/">Check my route</a>
<a class="btn button-secondary" href="/house-extensions/">Browse by project</a>
<a class="btn button-secondary" href="/councils/">Find my council</a>
</div>
<div class="last-updated">Updated {get_month_year()}</div>
<div class="answer-grid">
<div class="answer-card">
<h3>What to do first</h3>
<p>Use the tool if you still need to narrow the route. Use a project guide if the build type is already clear.</p>
</div>
<div class="answer-card">
<h3>What changes the route fastest</h3>
<p>Local restrictions, planning history, frontage visibility, heritage controls and close measurements are usually what turn a simple answer into a project-specific one.</p>
</div>
<div class="answer-card">
<h3>Why it stays practical</h3>
<p>{project_count} project guides, {town_count} local authority paths and {tool_count} tools are organised to get you to the next useful check quickly, not into another broad directory.</p>
</div>
</div>
</section>
"""


def build_goal_chooser() -> str:
    goals = [
        ("Planning an extension", "Check size, height, depth and local restrictions before you pay for drawings.", "/house-extensions/"),
        ("Considering a garden room", "Check incidental use, height, boundaries and whether restrictions change the route.", "/garden-rooms/"),
        ("Need a dropped kerb", "Separate planning permission from the highways or vehicle-crossover approval route.", "/dropped-kerbs/"),
        ("In a conservation area", "Check whether heritage controls make a familiar project more sensitive.", "/conservation-areas/"),
        ("HMO or change of use", "Check Article 4, licensing and council-specific planning risks before assuming the route.", "/hmos/"),
        ("Not sure yet", "Answer a few questions and get a cautious first-pass route.", "/tools/planning-route-check/"),
    ]
    cards = "".join(
        f"""
<a class="home-goal-card" href="{href}">
<strong>{title}</strong>
<span>{description}</span>
</a>
"""
        for title, description, href in goals
    )
    return f"""
<section>
<span class="eyebrow">I am trying to...</span>
<h2>Choose The Planning Question Closest To Your Project</h2>
<p class="section-lead">Start with the route that matches your actual decision, then use the next page to narrow the council, rule or project detail.</p>
<div class="home-goal-grid">{cards}</div>
</section>
"""


def build_start_here_section():
    cards = []
    for index, card in enumerate(START_HERE_CARDS, start=1):
        cards.append(
            _build_card(
                f"{index}. {card['title']}",
                card["description"],
                card["href"],
                card["cta"],
                kicker="Best starting path",
            )
        )

    return f"""
<section>
<span class="eyebrow">Start with the right question</span>
<h2>Top Journeys In The First 30 Seconds</h2>
<p class="section-lead">If you are not sure where to begin, choose the path that matches the uncertainty you actually have.</p>
<div class="grid">{''.join(cards)}</div>
</section>
"""


def build_tool_spotlight() -> str:
    tools = load_tools()
    featured = tools[:3]
    spotlight_cards = "".join(
        _build_card(
            tool["title"],
            tool.get("summary", "Use a quick self-check before you rely on a rule of thumb."),
            tool.get("href", f"/tools/{tool['slug']}/"),
            "Open tool",
            kicker="Fast triage",
        )
        for tool in featured
    )

    return f"""
<section>
<div class="split-grid">
<div class="cta-band">
<span class="eyebrow">Decision system</span>
<h2>Use The Tools As A Fast Triage Layer, Not As Isolated Calculators</h2>
<p>The tools work best when you need a fast route call before you commit to deeper reading. They are there to tell you whether the project still looks routine, what is making it less routine and what to open next.</p>
<ul class="checklist">
<li>Good for early-stage decisions before you pay for drawings.</li>
<li>Good for spotting when conservation areas, Article 4 or listed buildings may change the route.</li>
<li>Best followed by the matching project guide, rule page and local authority layer.</li>
</ul>
<div class="hero-ctas">
<a class="btn" href="/tools/">See all planning tools</a>
<a class="btn button-secondary" href="/tools/planning-decision-tool/">Start with the main tool</a>
</div>
</div>
<div class="grid-tight">{spotlight_cards}</div>
</div>
</section>
"""


def build_personalised_guidance_spotlight() -> str:
    return build_personalised_guidance_cta(
        title="Want A More Tailored Steer Before You Spend Money?",
        description="For projects that feel borderline, location-sensitive or awkwardly specific, start with the quick checks. Use the structured request form only when the remaining answer still depends on your property, design or local context.",
        context_label="homepage",
        email_context="homepage enquiry",
        intro_label="New personal next step",
    )


def build_find_help_spotlight() -> str:
    return build_find_help_cta(compact=True)


def build_project_cards(projects):
    cards = []
    for project in projects[:FEATURED_PROJECT_LIMIT]:
        cards.append(
            _build_card(
                project["title"],
                project.get("description", "Check the usual planning route, the limits that matter and the next local checks worth making."),
                f"/{project['slug']}/",
                _project_cta(project["slug"]),
                kicker="Popular project type",
            )
        )

    return f"""
<section>
<span class="eyebrow">Project-first guidance</span>
<h2>Start With The Build Type You Are Actually Planning</h2>
<p class="section-lead">These guides work best when the main question is the project itself rather than one narrow planning topic.</p>
<div class="project-grid">{''.join(cards)}</div>
</section>
"""


def build_featured_guides(projects, towns):
    cards = []
    for project in projects[:FEATURED_PROJECT_LIMIT]:
        for town in towns[:FEATURED_TOWN_LIMIT]:
            cards.append(
                _build_card(
                f"{project['short_name']} in {town['town_name']}",
                "See the likely route, the local friction points and the rule pages people usually need next.",
                f"/{project['slug']}/{town['county_slug']}/{town['town_slug']}/",
                "View local guide",
                kicker="Answer-first local page",
                )
            )
            if len(cards) >= FEATURED_GUIDE_LIMIT:
                break
        if len(cards) >= FEATURED_GUIDE_LIMIT:
            break

    return f"""
<section>
<span class="eyebrow">Useful local entry points</span>
<h2>Curated Local Guides Worth Opening Next</h2>
<p class="section-lead">These guides work best once the project is already clear and you need to see whether local restrictions, authority context or a nearby comparison changes the safer route.</p>
<div class="grid">{''.join(cards)}</div>
</section>
"""


def build_topic_links():
    cards = []
    for title, href in PLANNING_TOPIC_LINKS[:TOPIC_LIMIT]:
        cards.append(
            _build_card(
                title,
                "Open the rule hub when one planning issue is the blocker and you do not need a full project guide first.",
                href,
                "Open topic hub",
                kicker="Rule-first route",
            )
        )

    return f"""
<section>
<span class="eyebrow">Rule hubs that earn their place</span>
<h2>Planning Topics Worth Opening Before You Over-Read The Wrong Guide</h2>
<p class="section-lead">These pages help when the real issue is height, boundaries, permitted development, conservation areas or another rule that cuts across multiple project types.</p>
<div class="grid">{''.join(cards)}</div>
</section>
"""


def build_council_authority_grid(councils_by_county):
    cards = []
    for county_slug, councils in list(councils_by_county.items())[:LOCAL_COUNTY_LIMIT]:
        county_name = county_slug.replace("-", " ").title()
        sample_towns = ", ".join(council["town_name"] for council in councils[:3])
        description = f"Browse {len(councils)} authority areas in {county_name} and see whether local policy, conservation areas or Article 4 make the usual answer less reliable."
        if sample_towns:
            description += f" Includes {sample_towns}."
        cards.append(
            _build_card(
                county_name,
                description,
                f"/{county_slug}/",
                "Browse area and councils",
                kicker="Local authority explorer",
            )
        )

    return f"""
<section>
<span class="eyebrow">Local context</span>
<h2>Compare Planning Authorities Without Falling Into A Directory Maze</h2>
<p class="section-lead">Area and council pages exist to answer the local question cleanly: does this authority context make the usual national answer less reliable?</p>
<div class="county-grid">{''.join(cards)}</div>
</section>
"""


def build_top_town_links(towns):
    cards = []
    for town in towns[:TOP_TOWN_LIMIT]:
        cards.append(
            _build_card(
                town["town_name"],
                "Open the council overview, then jump into the local project page or topic guide that matches the issue you need to check.",
                f"/councils/{town['town_slug']}/",
                "View council guide",
                kicker="Local authority page",
            )
        )

    return f"""
<section>
<h2>Popular Local Authority Starting Points</h2>
<div class="grid">{''.join(cards)}</div>
</section>
"""


def build_trending_questions():
    cards = []
    for faq in HOMEPAGE_FAQS:
        cards.append(
            _build_card(
                faq["title"],
                faq["description"],
                faq["href"],
                "Read the answer",
                kicker="FAQ shortcut",
            )
        )

    return f"""
<section>
<span class="eyebrow">Useful process answers</span>
<h2>Planning Questions People Ask Before They Spend Money</h2>
<p class="section-lead">These FAQ pages are best when the uncertainty is about process, permissions, timing or verification rather than one exact build type.</p>
<div class="grid">{''.join(cards)}</div>
</section>
"""


def build_recovery_topic_section():
    topics = [
        ("Planning Permission", "/planning-permission/", "/planning-permission/wandsworth/", "Recovered local-intent topic", "Best when the route question is still the main blocker."),
        ("Permitted Development", "/permitted-development/", "/permitted-development/sevenoaks/", "Recovered local-intent topic", "Useful when the shortcut route is still plausible but local context matters."),
        ("Height Limits", "/height-limits/", "/height-limits/windsor-and-maidenhead/", "Recovered local-intent topic", "Good for schemes where one dimension may be doing most of the damage."),
        ("Boundary Rules", "/boundary-rules/", "/boundary-rules/dacorum/", "Recovered local-intent topic", "Useful when neighbour relationship and siting are the live issue."),
        ("Conservation Areas", "/conservation-areas/", "/conservation-areas/wandsworth/", "Recovered local-intent topic", "Strong when heritage context may be changing a normally simple route."),
    ]
    cards = []
    for title, hub_href, local_href, kicker, description in topics:
        cards.append(
            _build_card(
                title,
                description + f" Start with the hub, then compare a local example path like {local_href.strip('/')}.",
                hub_href,
                "Open topic hub",
                kicker=kicker,
            )
        )

    return f"""
<section>
<span class="eyebrow">High-value rule routes</span>
<h2>Local Topic Paths Most Likely To Recover Search Demand</h2>
<p class="section-lead">These are the rule families most likely to bring users back into the site through the rebuilt council-level topic layer.</p>
<div class="grid">{''.join(cards)}</div>
</section>
"""


def build_local_search_spotlight():
    cards = []
    for page in LOCAL_SEARCH_PAGES[:LOCAL_SEARCH_LIMIT]:
        cards.append(
            _build_card(
                page["title"],
                "See the local reading, the checks that matter and the strongest next pages for this search without getting dropped into a generic directory first.",
                f"/local-search/{page['slug']}/",
                "Open local route",
                kicker="Search-intent shortcut",
            )
        )

    return f"""
<section>
<span class="eyebrow">Curated local capture</span>
<h2>High-Intent Local Search Pages That Earn Their Place</h2>
<p class="section-lead">These pages answer the local query quickly, show the checks that matter and hand the user into the strongest authority, project, topic or tool page without feeling like a doorway.</p>
<div class="grid">{''.join(cards)}</div>
</section>
"""


def build_return_visit_section():
    cards = []
    for card in RETURN_VISIT_CARDS:
        link = (
            f'<div class="hero-ctas"><a class="btn button-secondary" href="{card["href"]}">{card["link_text"]}</a></div>'
            if card.get("href")
            else ""
        )
        cards.append(
            f"""
<div class="mini-card">
<h3>{card['title']}</h3>
<p>{card['description']}</p>
{link}
</div>
"""
        )

    return f"""
<section>
<span class="eyebrow">Built for next-step flow</span>
<h2>What To Do When The Answer Still Feels Borderline</h2>
<p class="section-lead">The strongest next step depends on why the answer is still uncertain, not on which page you happened to land on first.</p>
<div class="info-columns">{''.join(cards)}</div>
</section>
"""


def build_homepage_authority_summary() -> str:
    return build_authority_summary_section(
        section_id="homepage-authority",
        title="Why The Guidance Should Feel More Accountable",
        intro="High-traffic pages should feel clearly owned, clearly reviewed and clear about the official sources behind the answer, especially before someone spends money on the wrong next step.",
    )


def build_homepage_founder_story() -> str:
    return """
<section>
<span class="eyebrow">Why this site exists</span>
<h2>Built After A Frustrating Planning Permission Experience</h2>
<div class="split-grid">
<div class="cta-band">
<p>I built UK Planning Guide after trying to move forward with a few projects of my own and finding the planning permission side far more confusing, slow and difficult to navigate than it should have been.</p>
<p>What I wanted at the time was not a wall of jargon or another council directory. I wanted a practical starting point that explained the likely route in plain English, showed the local complication early and made the next sensible check clearer before more time or money was spent.</p>
<div class="hero-ctas">
<a class="btn button-secondary" href="/about/">Read why I built it</a>
</div>
</div>
<div class="mini-card">
<h3>What that means for the site</h3>
<p>The aim is to help people get clearer answers earlier, avoid obvious dead ends and understand when general guidance is enough versus when formal confirmation matters.</p>
</div>
</div>
</section>
"""


def build_downloads_spotlight() -> str:
    return """
<section class="download-related-assets" data-download-internal-links="true">
<span class="eyebrow">Free printable resources</span>
<h2>Planning Checklists You Can Print, Copy And Share</h2>
<p class="section-lead">Use the download library when you need a clean checklist for a builder, designer, neighbour conversation or council query before the project becomes expensive.</p>
<div class="grid">
<a class="card" href="/downloads/permitted-development-homeowner-checklist/"><div class="card-kicker">Popular checklist</div><h3>Permitted Development Homeowner Checklist</h3><p>Check the obvious permitted development blockers before relying on the simpler route.</p><span class="cta">Open checklist</span></a>
<a class="card" href="/downloads/extension-planning-prep-checklist/"><div class="card-kicker">Project prep</div><h3>Extension Planning Prep Checklist</h3><p>Collect the measurements, constraints and questions that matter before drawings or applications.</p><span class="cta">Open checklist</span></a>
<a class="card" href="/downloads/"><div class="card-kicker">Library</div><h3>Browse All Printable Planning Resources</h3><p>Find worksheets for refusals, objections, site constraints, listed buildings and application prep.</p><span class="cta">Open downloads</span></a>
</div>
</section>
"""


def build_homepage_content(projects, towns, councils_by_county):
    tool_count = len(load_tools())
    return f"""
{build_homepage_hero(len(projects), len(towns), tool_count)}
{build_goal_chooser()}
{build_start_here_section()}
{build_homepage_authority_summary()}
{build_homepage_founder_story()}
{build_tool_spotlight()}
{build_personalised_guidance_spotlight()}
{build_find_help_spotlight()}
{build_downloads_spotlight()}
{build_project_cards(projects)}
{build_featured_guides(projects, towns)}
{build_topic_links()}
{build_council_authority_grid(councils_by_county)}
{build_top_town_links(towns)}
{build_recovery_topic_section()}
{build_trending_questions()}
{build_return_visit_section()}
"""
