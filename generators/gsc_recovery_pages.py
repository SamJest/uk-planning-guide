from __future__ import annotations

from html import escape
from pathlib import Path

from components.editorial_authority import build_editorial_authority_block
from components.official_sources import build_official_sources_block
from components.personalised_guidance import build_personalised_guidance_cta
from components.planning_helpers import scenario_rule_excerpt, useful_local_restrictions
from components.shared_components import render_result_capture
from core.files import write_file
from core.paths import BASE_URL, OUTPUT_FOLDER
from core.render import inject_into_base
from data.gsc_recovery_routes import GSC_RECOVERY_ROUTES, recovery_path, recovery_slug
from data.loaders import load_projects, load_rule
from data.scenario_data import SCENARIO_LOOKUP
from utils.country_utils import get_country_slug
from utils.live_links import is_live_internal_href, normalize_internal_href
from utils.random_tools import get_month_year


PROJECTS_BY_SLUG = {project["slug"]: project for project in load_projects()}


def _label_from_slug(slug: str) -> str:
    return slug.replace("-", " ").title()


def _scenario_label(slug: str) -> str:
    return SCENARIO_LOOKUP.get(slug, {}).get("title", _label_from_slug(slug))


def _project_label(project_slug: str) -> str:
    project = PROJECTS_BY_SLUG.get(project_slug, {})
    return project.get("short_name") or project.get("title", _label_from_slug(project_slug))


def _scenario_phrase(scenario_slugs: tuple[str, ...]) -> str:
    labels = [_scenario_label(slug).lower() for slug in scenario_slugs]
    if len(labels) == 1:
        return labels[0]
    return f"{' and '.join(labels)}"


def _scenario_title_phrase(scenario_slugs: tuple[str, ...]) -> str:
    short_labels = {
        "planning-permission": "planning permission",
        "permitted-development": "PD",
        "height-limits": "height limits",
        "maximum-height": "maximum height",
        "distance-from-boundary": "boundary distance",
        "boundary-rules": "boundary rules",
        "conservation-areas": "conservation",
        "article-4": "Article 4",
        "depth-limits": "depth limits",
    }
    labels = [short_labels.get(slug, _scenario_label(slug).lower()) for slug in scenario_slugs]
    return " and ".join(labels)


def _trim_title(text: str, limit: int = 70) -> str:
    clean = " ".join(str(text or "").split()).strip()
    if len(clean) <= limit:
        return clean
    trimmed = clean[:limit].rsplit(" ", 1)[0].rstrip(" :-")
    return trimmed if len(trimmed) >= 30 else clean[:limit].rstrip(" :-")


def _title_for(route: dict) -> str:
    project = _project_label(route["project_slug"]).replace(" Planning Permission", "")
    town = _label_from_slug(route["town_slug"])
    scenario = _scenario_title_phrase(route["scenario_slugs"])
    title = f"{project} in {town}: {scenario} checks"
    if len(title) > 70:
        title = f"{project} {town}: {scenario}"
    return _trim_title(title)


def _description_for(route: dict) -> str:
    project = _project_label(route["project_slug"]).replace(" Planning Permission", "").lower()
    town = _label_from_slug(route["town_slug"])
    scenario = _scenario_phrase(route["scenario_slugs"])
    description = (
        f"Check {project} in {town}: {scenario}. "
        "Use the local guide and rule checks before treating the answer as settled."
    )
    if len(description) <= 155:
        return description
    return f"Check {project} in {town}: {scenario}. Start with the local guide and rule checks."


def _rule_signal(rule: dict, scenario_slug: str, town_name: str) -> str:
    signal = scenario_rule_excerpt(rule, scenario_slug)
    if signal:
        return signal
    label = _scenario_label(scenario_slug).lower()
    if scenario_slug == "article-4":
        return f"Article 4 can remove the simpler permitted-development route in {town_name}, so check the exact property and proposed use before assuming it applies."
    if scenario_slug == "conservation-areas":
        return f"Conservation-area controls in {town_name} can tighten design, demolition, materials and visibility expectations even where the project looks familiar."
    if scenario_slug == "permitted-development":
        return f"Permitted development only helps in {town_name} if the proposal stays inside the relevant limits and no local control removes the simpler route."
    return f"{_scenario_label(scenario_slug)} is one of the checks most likely to change the route for this project in {town_name}."


def _card(href: str, kicker: str, title: str, body: str, cta: str) -> str:
    clean = normalize_internal_href(href)
    if not clean or not is_live_internal_href(clean):
        return ""
    return f"""
<a class="card" href="{clean}">
<div class="card-kicker">{escape(kicker)}</div>
<h3>{escape(title)}</h3>
<p>{escape(body)}</p>
<span class="cta">{escape(cta)}</span>
</a>
"""


def _route_cards(route: dict, town_name: str, project_name: str) -> str:
    project_slug = route["project_slug"]
    county_slug = route["county_slug"]
    town_slug = route["town_slug"]
    scenario_slugs = route["scenario_slugs"]
    cards = [
        _card(
            f"/{project_slug}/{county_slug}/{town_slug}/",
            "Main local guide",
            f"{project_name} in {town_name}",
            "Use this first if the project type matters more than the recovered query wording.",
            "Open local guide",
        ),
        _card(
            f"/councils/{town_slug}/",
            "Council context",
            f"Planning permission in {town_name}",
            "Use this if local policy, design sensitivity or planning history is doing the real work.",
            "Open council guide",
        ),
    ]

    for scenario_slug in scenario_slugs:
        cards.append(
            _card(
                f"/{scenario_slug}/{town_slug}/",
                "Topic guide",
                f"{_scenario_label(scenario_slug)} in {town_name}",
                "Use this to isolate the rule before applying it back to the project.",
                "Open topic page",
            )
        )
        cards.append(
            _card(
                f"/{project_slug}/{county_slug}/{town_slug}/{scenario_slug}/",
                "Project topic",
                f"{project_name}: {_scenario_label(scenario_slug)}",
                "Use this if the specific project and the local rule both matter.",
                "Open project topic",
            )
        )

    cards.append(
        _card(
            "/tools/planning-decision-tool/",
            "Fast route check",
            "Planning decision tool",
            "Use this if the next step could still be permitted development, planning permission or a formal proof route.",
            "Check likely route",
        )
    )
    return "".join(card for card in cards if card)


def _tripwire_items(route: dict, rule: dict, town_name: str) -> list[str]:
    restrictions = useful_local_restrictions(rule)
    items = [f"{label} can change the recovered search answer in {town_name}." for label, _ in restrictions[:2]]
    for scenario_slug in route["scenario_slugs"]:
        if scenario_slug == "article-4":
            items.append("Article 4 needs checking against the exact property and use, not just the authority name.")
        elif scenario_slug == "conservation-areas":
            items.append("Heritage sensitivity can make materials, demolition, frontage and visibility more important than the broad project label.")
        elif scenario_slug in {"height-limits", "maximum-height"}:
            items.append("Height-sensitive routes need measured drawings and the correct ground-level reference before the answer is safe.")
        elif scenario_slug == "permitted-development":
            items.append("Permitted development only helps if the proposal stays inside the limits and no local control removes the fallback.")
        elif scenario_slug == "planning-permission":
            items.append("Planning permission becomes more likely when scale, use, design sensitivity or previous work changes the baseline.")
    output = []
    seen = set()
    for item in items:
        clean = " ".join(item.split())
        if clean and clean not in seen:
            seen.add(clean)
            output.append(clean)
    return output[:4]


def generate_gsc_recovery_pages() -> None:
    print("Generating targeted GSC recovery pages")

    for route in GSC_RECOVERY_ROUTES:
        project_slug = route["project_slug"]
        county_slug = route["county_slug"]
        town_slug = route["town_slug"]
        town_name = _label_from_slug(town_slug)
        project_name = _project_label(project_slug).replace(" Planning Permission", "")
        rule = load_rule(project_slug, county_slug, town_slug) or {}
        scenario_slugs = route["scenario_slugs"]
        scenario_phrase = _scenario_phrase(scenario_slugs)
        route_url = recovery_path(route)
        signals = [_rule_signal(rule, slug, town_name) for slug in scenario_slugs]
        tripwires = _tripwire_items(route, rule, town_name)
        route_cards = _route_cards(route, town_name, project_name)
        content = f"""
<section class="hero">
<span class="badge">Focused local guide</span>
<h1>{escape(project_name)} in {escape(town_name)}: {escape(scenario_phrase.title())}</h1>
<p>This page is for searches about {escape(route['query'])}. It gives the answer-led route, then points you to the stronger local guide and rule pages.</p>
<p>The important check is whether {escape(scenario_phrase)} changes the normal {escape(project_name.lower())} answer in {escape(town_name)} before you rely on a broad search result.</p>
<div class="last-updated">Updated {get_month_year()}</div>
</section>

<section class="local-answer-box" id="scenario-summary">
<span class="eyebrow">Recovered search answer</span>
<h2>What This Query Usually Needs To Settle</h2>
<div class="answer-grid">
<div class="answer-card">
<h3>Direct answer</h3>
<p>Treat this as a {escape(project_name.lower())} question in {escape(town_name)} where {escape(scenario_phrase)} may change the route. If that rule is the blocker, verify it before relying on a broad permitted-development or planning-permission answer.</p>
</div>
<div class="answer-card">
<h3>Rule signals</h3>
<ul class="checklist">{''.join(f"<li>{escape(signal)}</li>" for signal in signals)}</ul>
</div>
<div class="answer-card">
<h3>Why this page exists</h3>
<p>The query combines a project, a place and one or more planning rules, so a focused route is more useful than sending you back to a broad hub.</p>
</div>
</div>
</section>

<section class="local-search-sensitivity">
<span class="eyebrow">Before you rely on it</span>
<h2>The Checks Most Likely To Change The Route</h2>
<div class="answer-grid">
<div class="answer-card">
<h3>Checks most likely to matter</h3>
<ul class="checklist">{''.join(f"<li>{escape(item)}</li>" for item in tripwires)}</ul>
</div>
<div class="answer-card">
<h3>When to slow down</h3>
<p>If the proposal depends on the simpler route surviving, use measured drawings, planning history and official local checks before paying for design work or starting the application route.</p>
</div>
<div class="answer-card">
<h3>Best next move</h3>
<p>Open the strongest page below that matches the real blocker: project type, council context, the individual rule, or a quick route check.</p>
</div>
</div>
</section>

{build_official_sources_block(
    page_family="project",
    authority_slug=town_slug,
    country_slug=rule.get("country_slug", get_country_slug(county_slug)),
    project_slug=project_slug,
    scenario_slug=scenario_slugs[0],
)}

<section class="local-search-routes" id="scenario-next-steps">
<span class="eyebrow">Deeper route options</span>
<h2>Open The Page Most Likely To Settle This Search</h2>
<div class="grid">
{route_cards}
</div>
{render_result_capture(f"gsc-recovery-{project_slug}-{town_slug}-{recovery_slug(route)}-capture")}
</section>

<section class="trust" id="scenario-trust">
<span class="eyebrow">How to use this page</span>
<h2>Use This Focused Route As A Starting Point</h2>
<p>This page narrows a specific local search, but the safer decision still comes from the main project guide, official local sources and a formal check when the design is close to a limit.</p>
</section>

{build_editorial_authority_block(
    route_url,
    page_family="project",
    authority_slug=town_slug,
    country_slug=rule.get("country_slug", get_country_slug(county_slug)),
    project_slug=project_slug,
    scenario_slug=scenario_slugs[0],
)}

{build_personalised_guidance_cta(
    title="Need This Recovered Route Narrowed To Your Property?",
    description=f"If {project_name.lower()} in {town_name} still depends on the exact design, local control or planning history, use the quick tools first, then the structured form if the answer is still case-specific.",
    context_label="focused-route",
    email_context=f"{project_name} in {town_name}: {scenario_phrase}",
    compact=True,
)}
"""

        html = inject_into_base(
            title=_title_for(route),
            content=content,
            options={
                "breadcrumbs": [
                    ("Home", "/"),
                    (project_name, f"/{project_slug}/"),
                    (town_name, f"/{project_slug}/{county_slug}/{town_slug}/"),
                    (scenario_phrase.title(), ""),
                ],
            },
            canonical_url=f"{BASE_URL}{route_url}",
            meta_description=_description_for(route),
        )
        folder = OUTPUT_FOLDER / project_slug / county_slug / town_slug / recovery_slug(route)
        write_file(folder, "index.html", html)

    print("Targeted GSC recovery pages generated successfully")
