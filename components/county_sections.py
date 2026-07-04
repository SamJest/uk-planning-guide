from components.jurisdiction_notices import build_jurisdiction_notice
from utils.live_links import is_live_internal_href, normalize_internal_href

PRIORITY_SCENARIO_ORDER = [
    "planning-permission",
    "permitted-development",
    "boundary-rules",
    "height-limits",
    "conservation-areas",
    "article-4",
]


def slug_to_name(slug: str) -> str:
    return slug.replace("-", " ").title()


def _sort_scenarios(scenarios):
    priority_index = {slug: index for index, slug in enumerate(PRIORITY_SCENARIO_ORDER)}
    return sorted(
        scenarios,
        key=lambda item: (
            priority_index.get(item.get("slug", ""), len(priority_index) + 1),
            item.get("title", ""),
        ),
    )


def build_county_jump_links(county_name: str) -> str:
    return f"""
<section class="page-jump-links">
<span class="eyebrow">Jump to what matters</span>
<h2>Use This Area Page In The Order That Saves You Time</h2>
<div class="link-grid">
<a href="#county-summary">Start with the quick area summary for {county_name}</a>
<a href="#county-start">Use the fastest council, topic and tool routes first</a>
<a href="#county-projects">Open project hubs if the build type is already clear</a>
<a href="#county-topics">Check the rules that most often change the answer</a>
<a href="#county-councils">Compare the live local authorities in this area</a>
<a href="#county-trust">Use the trust notes if the route still feels mixed</a>
</div>
</section>
"""


def build_county_decision_summary(county_name: str, council_count: int) -> str:
    return f"""
<section class="county-summary" id="county-summary">
<span class="eyebrow">Area overview</span>
<h2>How To Use The {county_name} Planning Pages</h2>
<div class="answer-grid">
<div class="answer-card">
<h3>What usually works best</h3>
<p>Start with the project type first, then narrow the answer by local planning authority. This keeps a broad '{county_name} planning' search short, practical and tied to the live local route.</p>
</div>
<div class="answer-card">
<h3>What this area page adds</h3>
<p>It brings together {council_count} local authority areas so you can move from the broad rule to the right council context without guessing.</p>
</div>
<div class="answer-card">
<h3>Best next step</h3>
<ul class="checklist">
<li>Use the project guides when the build type is the main question.</li>
<li>Use the council links when local restrictions or local policy may change the answer.</li>
<li>Use topic hubs when one specific rule is blocking progress more than the place itself.</li>
</ul>
</div>
</div>
</section>
"""


def build_county_decision_guide(county_name: str, council_count: int) -> str:
    return f"""
<section class="decision-guide" id="county-decision-guide">
<span class="eyebrow">Decision guide</span>
<h2>When This Area Page Is Enough And When You Should Go More Local</h2>
<div class="answer-grid">
<div class="answer-card">
<h3>This page usually works best when</h3>
<ul class="checklist">
<li>The search is still broad and you are deciding which council or project page deserves attention first.</li>
<li>You want to compare the planning area before committing to one local authority route.</li>
<li>The real blocker is choosing the right next page, not settling the full site-specific answer here.</li>
</ul>
</div>
<div class="answer-card">
<h3>Pause and go narrower when</h3>
<ul class="checklist">
<li>One specific council area already matters more than the wider county picture.</li>
<li>A conservation area, Article 4, listed building issue or exact measurement is driving the uncertainty.</li>
<li>The proposal is financially important enough that a broad area summary is no longer a safe stopping point.</li>
</ul>
</div>
<div class="answer-card">
<h3>What usually settles it faster</h3>
<ul class="checklist">
<li>Open the matching local authority page from the {council_count} live council routes below.</li>
<li>Pair the council page with the exact project guide or topic page that fits the job.</li>
<li>If the scheme is close to a limit, use drawings and written confirmation rather than relying on comparison alone.</li>
</ul>
</div>
</div>
</section>
"""


def build_county_start_here_section(county_slug: str, county_name: str, councils) -> str:
    first_council = councils[0] if councils else {"town_slug": county_slug, "town_name": county_name}
    council_href = normalize_internal_href(f"/councils/{first_council['town_slug']}/")
    if not is_live_internal_href(council_href):
        council_href = "/councils/"
    topic_href = normalize_internal_href(f"/planning-permission/{first_council['town_slug']}/")
    if not is_live_internal_href(topic_href):
        topic_href = "/planning-permission/"
    return f"""
<section class="county-start-here" id="county-start">
<span class="eyebrow">Start here in this planning area</span>
<h2>The Fastest Local Routes For {county_name} Searches</h2>
<div class="grid">
<a class="card" href="{council_href}">
<div class="card-kicker">Council path</div>
<h3>Open a council guide first</h3>
<p>Best when the search is really about planning permission in {county_name} and the local authority layer is likely to change the answer.</p>
<span class="cta">View council guide</span>
</a>
<a class="card" href="{topic_href}">
<div class="card-kicker">Local topic path</div>
<h3>Open planning permission in a live authority area</h3>
<p>Use the local topic layer when the route question matters more than one exact project type.</p>
<span class="cta">Open local topic page</span>
</a>
<a class="card" href="/planning-faq/do-i-need-planning-permission/">
<div class="card-kicker">FAQ path</div>
<h3>Read the route-level answer</h3>
<p>Useful when the user intent is still broad and needs narrowing before choosing a project or council page.</p>
<span class="cta">Read answer</span>
</a>
<a class="card" href="/tools/planning-decision-tool/">
<div class="card-kicker">Tool path</div>
<h3>Run the quick planning tool</h3>
<p>Use the tool for a first-pass route check before moving into the more detailed local pages.</p>
<span class="cta">Open tool</span>
</a>
</div>
</section>
"""


def build_county_jurisdiction_notice(county_slug: str, county_name: str) -> str:
    return build_jurisdiction_notice(county_slug, county_name, "area guide")


def build_county_topic_links(county_slug: str, scenarios) -> str:
    cards = []

    for scenario in _sort_scenarios(scenarios)[:6]:
        href = normalize_internal_href(f"/{scenario['slug']}/")
        if not is_live_internal_href(href):
            continue
        cards.append(
            f"""
<a class="card" href="{href}">
<div class="card-kicker">Topic hub</div>
<h3>{scenario['title']}</h3>
<p>Useful when this is the rule most likely to decide whether a project in {slug_to_name(county_slug)} needs permission or a closer check before you narrow into one council page.</p>
<span class="cta">Open topic</span>
</a>
"""
        )

    return f"""
<section class="county-topics" id="county-topics">
<span class="eyebrow">Rules that often change the answer</span>
<h2>Planning Topics That Commonly Decide The Next Step Across {slug_to_name(county_slug)}</h2>
<div class="card-grid">{''.join(cards)}</div>
</section>
"""


def build_trust_section(topic: str, county_name: str, scope: str) -> str:
    system_label = "English planning system"
    if county_name.lower() == "wales":
        system_label = "Welsh planning system"
    elif county_name.lower() == "scotland":
        system_label = "Scottish planning system"
    elif county_name.lower() == "northern ireland":
        system_label = "Northern Ireland planning system"
    return f"""
<section class="trust-section" id="county-trust">
<span class="eyebrow">Trust and caveats</span>
<h2>How To Use This Area Guide Well</h2>
<p>This guide summarises {topic.lower()} guidance across {county_name}. It helps you reach the right local authority and the right project guide faster, while staying clear about what still needs site-specific confirmation under the {system_label}. It is strongest as a comparison and routing page, not as the final permission answer for one exact site.</p>
<div class="info-columns">
<div class="mini-card">
<h3>Useful for</h3>
<ul class="checklist">
<li>Choosing the right council path quickly.</li>
<li>Comparing project hubs across the planning area.</li>
<li>Finding the topic hubs most likely to change the answer.</li>
</ul>
</div>
<div class="mini-card">
<h3>Still worth verifying</h3>
<ul class="checklist">
<li>Exact dimensions and site coverage.</li>
<li>Whether local designations affect the property.</li>
<li>Whether a borderline scheme needs written confirmation.</li>
</ul>
</div>
</div>
</section>
"""
