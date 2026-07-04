import itertools

from components.planning_helpers import restriction_messages, scenario_rule_excerpt
from data.promoted_links import PROMOTED_LINKS
from data.scenario_data import SCENARIO_LOOKUP
from utils.live_links import is_live_internal_href, normalize_internal_href
from utils.project_scenario_config import project_scenario_href


def build_combinations(scenarios, max_combinations):
    combos = []

    for a, b in itertools.combinations(scenarios, 2):
        if a["type"] == b["type"]:
            continue

        slug = f"{a['slug']}-{b['slug']}"
        title = f"{a['title']} and {b['title']}"

        combos.append((a, b, slug, title))

        if len(combos) >= max_combinations:
            break

    return combos


def _scenario_title(slug):
    return SCENARIO_LOOKUP.get(slug, {}).get("title", slug.replace("-", " ").title())


def _combo_excerpt(rule, slug, town_name):
    excerpt = scenario_rule_excerpt(rule, slug)
    if excerpt:
        return excerpt

    title = _scenario_title(slug).lower()
    if slug == "article-4":
        return f"Article 4 directions in {town_name} can remove the simpler permitted development route and force a fuller planning check."
    if slug == "listed-buildings":
        return f"Listed building controls in {town_name} can trigger a separate consent route even where the wider planning position looks familiar."
    if slug == "conservation-areas":
        return f"Conservation area status in {town_name} can tighten design expectations and make broad rule-of-thumb answers less reliable."
    return f"{_scenario_title(slug)} is one of the checks most likely to change the planning route for borderline schemes in {town_name}."


def build_combo_hero(clean_project, combo_title, town_name, county_name, rule, a_slug, b_slug):
    primary_signal = _combo_excerpt(rule, a_slug, town_name)
    secondary_signal = _combo_excerpt(rule, b_slug, town_name)
    return f"""
    <section class="hero">
        <span class="badge">Local rule overlap guide</span>
        <h1>{clean_project} in {town_name}: {combo_title}</h1>
        <p>
        Use this page when one rule is not enough on its own. It shows how {combo_title.lower()} can overlap for
        {clean_project.lower()} in {town_name}, {county_name}, what usually matters first, and what is worth checking next.
        </p>
        <div class="tool-result">
            <strong>Quick answer:</strong> {primary_signal} {secondary_signal}
        </div>
    </section>
    """


def build_combo_intro(project_title, combo_title, town_name, rng):
    intro_variants = [
        f"Understanding how {combo_title.lower()} overlap is often the difference between a quick answer and a false sense of confidence for {project_title.lower()} in {town_name}.",
        f"When a scheme in {town_name} looks borderline, the answer usually depends on how these two rules combine rather than on either rule in isolation.",
        f"This guide focuses on the decision point between {combo_title.lower()} so you can see which issue deserves the next local check.",
    ]

    return f"""
    <section class="combo-intro">
        <span class="eyebrow">Why this page exists</span>
        <h2>Where This Combination Usually Becomes Important</h2>
        <p>{rng.choice(intro_variants)}</p>
    </section>
    """


def render_combo_rules(rule, a_slug, b_slug, town_name):
    a_title = _scenario_title(a_slug)
    b_title = _scenario_title(b_slug)
    a_excerpt = _combo_excerpt(rule, a_slug, town_name)
    b_excerpt = _combo_excerpt(rule, b_slug, town_name)

    return (
        f"""
        <section class='rule-section'>
            <span class="eyebrow">First rule to pin down</span>
            <h2>{a_title} in {town_name}</h2>
            <p>{a_excerpt}</p>
        </section>
        """,
        f"""
        <section class='rule-section'>
            <span class="eyebrow">Second rule that can shift the answer</span>
            <h2>{b_title} in {town_name}</h2>
            <p>{b_excerpt}</p>
        </section>
        """,
    )


def build_rule_interaction_section(a_title, b_title, clean_project, town_name, rule):
    restrictions = restriction_messages(rule)
    restriction_note = (
        f"Local controls such as {', '.join(label.lower() for label, _ in restrictions[:2])} can make this combination harder to rely on without written confirmation."
        if restrictions
        else "If the design is close to a limit, the interaction between these rules is usually a sign to measure carefully rather than rely on a single broad answer."
    )

    return f"""
    <section class="rule-interaction">
        <span class="eyebrow">Interaction summary</span>
        <h2>How {a_title} And {b_title} Usually Work Together</h2>
        <p>
        For {clean_project.lower()} in {town_name}, {a_title.lower()} can look manageable on its own and {b_title.lower()} can also look manageable on its own, but the planning route often changes when both pressures land on the same design.
        </p>
        <p>{restriction_note}</p>
    </section>
    """


def build_combo_examples(a_title, b_title, clean_project, town_name):
    return f"""
    <section class="combo-examples">
        <span class="eyebrow">Practical next checks</span>
        <h2>What To Review Before You Rely On This Combination</h2>
        <ul>
            <li>Measure the part of the {clean_project.lower()} most likely to trigger {a_title.lower()} before assuming the wider design still fits.</li>
            <li>Check whether {b_title.lower()} in {town_name} makes the first answer less reliable once the site context is included.</li>
            <li>If both rules feel close to the limit, treat that as a prompt for drawings and formal confirmation rather than more guesswork.</li>
        </ul>
    </section>
    """


def build_related_rule_links(project_slug, county_slug, town_slug, scenarios, a_slug, b_slug, max_links):
    items = []

    for s in scenarios:
        slug = s["slug"]

        if slug in (a_slug, b_slug):
            continue

        href = project_scenario_href(project_slug, county_slug, town_slug, slug) or normalize_internal_href(
            f"/{slug}/{town_slug}/"
        )
        if not is_live_internal_href(href):
            continue

        items.append(f'<li><a href="{href}">{s["title"]}</a></li>')

        if len(items) >= max_links:
            break

    return f"""
    <section class="related-rules">
        <span class="eyebrow">Closest related topics</span>
        <h2>Other Rules That Commonly Follow This Combination</h2>
        <ul>{''.join(items)}</ul>
    </section>
    """


def build_trust_section(town_name):
    methodology = PROMOTED_LINKS["methodology"]
    planning_tool = PROMOTED_LINKS["planning_decision_tool"]
    return f"""
    <section class="trust">
        <span class="eyebrow">Trust and caveats</span>
        <h2>How To Use This Combination Page Responsibly</h2>
        <p>
        Planning decisions in {town_name} are still made against national legislation, local policy and the specific facts of the site. This page is here to make the combination clearer, not to pretend every overlap can be settled by a templated answer.
        </p>
        <p>
        If the overlap still feels borderline, use <a href="{planning_tool['href']}">{planning_tool['title']}</a> for a quick route check, then verify the evidence against the <a href="{methodology['href']}">{methodology['title'].lower()}</a>.
        </p>
    </section>
    """


def assemble_combo_page(blocks):
    return "\n".join(b for b in blocks if b)

def build_combo_link_cluster(project_slug, county_slug, town_slug, scenarios, a_slug, b_slug, max_links=12):

    links = []

    for s in scenarios:
        slug = s["slug"]

        if slug in (a_slug, b_slug):
            continue

        href = project_scenario_href(project_slug, county_slug, town_slug, slug) or normalize_internal_href(
            f"/{slug}/{town_slug}/"
        )
        if not is_live_internal_href(href):
            continue

        links.append(f'<a href="{href}">{s["title"]}</a>')

        if len(links) >= max_links:
            break

    if not links:
        return ""

    return f"""
    <section class="link-cluster">
        <span class="eyebrow">Editorial follow-ups</span>
        <h2>Open The Most Relevant Local Single-Rule Guides Next</h2>
        <div class="link-grid">
            {''.join(links)}
        </div>
    </section>
    """


def build_combo_next_steps(project_slug, county_slug, town_slug, clean_project, combo_title, a_slug, b_slug):
    project_href = normalize_internal_href(f"/{project_slug}/{county_slug}/{town_slug}/")
    first_rule_href = project_scenario_href(project_slug, county_slug, town_slug, a_slug) or normalize_internal_href(
        f"/{a_slug}/{town_slug}/"
    )
    second_rule_href = project_scenario_href(project_slug, county_slug, town_slug, b_slug) or normalize_internal_href(
        f"/{b_slug}/{town_slug}/"
    )

    cards = []
    if is_live_internal_href(project_href):
        cards.append(
            f"""
<a class="card" href="{project_href}">
<div class="card-kicker">Main local guide</div>
<h3>{clean_project} in {town_slug.replace('-', ' ').title()}</h3>
<p>Open the main project guide if the live question is wider than {combo_title.lower()} on its own.</p>
<span class="cta">Open project guide</span>
</a>
"""
        )
    if is_live_internal_href(first_rule_href):
        cards.append(
            f"""
<a class="card" href="{first_rule_href}">
<div class="card-kicker">Single-rule page</div>
<h3>{_scenario_title(a_slug)}</h3>
<p>Open the single-rule page if this is the first issue you need to pin down before the overlap question.</p>
<span class="cta">Open rule page</span>
</a>
"""
        )
    if is_live_internal_href(second_rule_href):
        cards.append(
            f"""
<a class="card" href="{second_rule_href}">
<div class="card-kicker">Single-rule page</div>
<h3>{_scenario_title(b_slug)}</h3>
<p>Open the single-rule page if this is the second issue still doing most of the work in the route.</p>
<span class="cta">Open rule page</span>
</a>
"""
        )

    if not cards:
        return ""

    return f"""
    <section class="combo-next-steps">
        <span class="eyebrow">Best next routes</span>
        <h2>Use The Strongest Local Follow-Up Page Next</h2>
        <div class="grid">
            {''.join(cards)}
        </div>
    </section>
    """
