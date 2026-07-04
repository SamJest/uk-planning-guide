from components.planning_helpers import faq_schema, restriction_messages, scenario_rule_excerpt, useful_local_restrictions
from components.jurisdiction_notices import build_jurisdiction_notice
from components.personalised_guidance import build_personalised_guidance_cta
from components.planning_route_check import (
    build_planning_route_check_cta,
    should_show_route_check_scenario_cta,
)
from components.shared_components import render_result_capture
from components.trust_framework import build_trust_framework, planning_system_label
from data.loaders import load_projects
from data.promoted_links import PROMOTED_LINKS, SCENARIO_SUPPORT_LINK_KEYS
from rules.renderer import render_rules
from utils.internal_links import build_internal_links
from utils.project_scenario_config import rollout_scenarios_for_project
from utils.urls import safe_link


PROJECTS = load_projects()
PROJECTS_BY_SLUG = {project["slug"]: project for project in PROJECTS}
PROJECT_GROUPS = {}
for project in PROJECTS:
    PROJECT_GROUPS.setdefault(project.get("type", ""), []).append(project)


PROJECT_TYPE_PROPERTY_ASSUMPTIONS = {
    "extension": {
        "small": "a typical terraced or compact semi-detached house",
        "medium": "a typical semi-detached family house",
        "large": "a typical semi-detached or townhouse on a tighter urban plot",
    },
    "loft": {
        "small": "a standard house with an existing pitched roof",
        "medium": "a typical family house with loft potential",
        "large": "a standard urban house where roof visibility matters early",
    },
    "outbuilding": {
        "small": "a detached or edge-of-village house with rear garden space",
        "medium": "a family house with a usable rear garden",
        "large": "a house with limited but still functional garden space",
    },
    "microgeneration": {
        "small": "a standard house with some roof or side access options",
        "medium": "a typical house where siting and neighbour impact both matter",
        "large": "an urban house where visibility and neighbour amenity matter early",
    },
    "change-of-use": {
        "small": "a standard dwelling on a residential street",
        "medium": "a family house in a typical residential area",
        "large": "a house on a tighter residential street where amenity pressure can rise quickly",
    },
    "external": {
        "small": "a standard house with visible frontage decisions",
        "medium": "a typical house where frontage and boundary design matter",
        "large": "an urban house where frontage changes are usually more visible",
    },
}

PROJECT_TYPE_SUMMARY_HINTS = {
    "extension": "rear projection, height and neighbour relationship",
    "loft": "roof form, visible alterations and the planning history of the house",
    "outbuilding": "height, boundary siting and whether the structure stays subordinate",
    "microgeneration": "visual siting, amenity impact and whether the equipment still reads as domestic",
    "change-of-use": "local policy, concentration and day-to-day neighbour impact",
    "external": "frontage impact, privacy and how visible the change is from the street",
}

PROJECT_TYPE_VARIATION_INSERTS = {
    "extension": "Extension-led projects usually become less straightforward when scale and neighbour impact start to move together rather than separately.",
    "loft": "Loft and roof-led projects often turn on visibility and roof form much earlier than homeowners expect.",
    "outbuilding": "Outbuilding-style projects usually stay simpler when the structure still reads as clearly secondary to the main house.",
    "microgeneration": "Microgeneration proposals often look simple on paper but can turn on siting, visibility and amenity surprisingly quickly.",
    "change-of-use": "Change-of-use proposals usually depend on local policy and neighbour effect as much as the physical building itself.",
    "external": "External works often become planning-sensitive because they change how the property reads from the street rather than because they are large.",
}

TOWN_SIZE_INSERTS = {
    "small": "In a smaller authority area, visible design changes and neighbour relationships often stand out faster because the local context is easier to read street by street.",
    "medium": "In a mid-sized authority area, the deciding factor is often whether the proposal still looks routine once local policy and site context are layered in.",
    "large": "In a denser or larger authority area, the route often gets harder when visibility, amenity pressure and policy context all stack up at once.",
}

SCENARIO_CONSTRAINT_HINTS = {
    "planning-permission": "whether the proposal still looks comfortably within the simpler route",
    "permitted-development": "whether permitted development still survives once local controls are checked",
    "height-limits": "height and overall bulk",
    "boundary-rules": "boundary siting and neighbour relationship",
    "conservation-areas": "heritage sensitivity and visible design change",
    "article-4": "Article 4 coverage and council-specific controls",
    "listed-buildings": "listed building status and heritage consent risk",
    "roof-alterations": "roof visibility and whether the alteration still feels subordinate",
}

SCENARIO_PAGE_HEADINGS = {
    "planning-permission": "Planning Permission",
    "permitted-development": "Permitted Development",
    "height-limits": "Height Limits",
    "boundary-rules": "Boundary Rules",
    "conservation-areas": "Conservation Areas",
    "article-4": "Article 4",
    "maximum-height": "Maximum Height",
}

SCENARIO_H1_LABELS = {
    "planning-permission": "planning permission rules",
    "permitted-development": "permitted development rules",
    "height-limits": "height limits",
    "maximum-height": "maximum height rules",
    "depth-limits": "depth limits",
    "boundary-rules": "boundary rules",
    "distance-from-boundary": "distance from boundary",
    "roof-alterations": "roof alteration rules",
    "conservation-areas": "conservation area rules",
    "listed-buildings": "listed building rules",
    "article-4": "Article 4 rules",
}

SCENARIO_INTENT_NOTES = {
    "planning-permission": "Most searches for planning permission in {town} are really asking whether the proposal still looks comfortable without a full application.",
    "permitted-development": "In {town}, the live issue is usually whether permitted development still survives once local controls and site history are taken seriously.",
    "height-limits": "For many sites in {town}, height is the rule that settles the route faster than the project label on its own.",
    "boundary-rules": "In {town}, tight boundary relationships often decide the route before the wider design story does.",
    "conservation-areas": "Conservation-area searches in {town} are usually about whether heritage sensitivity makes the normal answer less reliable.",
    "article-4": "The important question in {town} is whether an Article 4 direction removes the fallback people usually assume is still there.",
    "maximum-height": "Maximum-height questions in {town} usually turn on which measurement point actually controls the decision.",
}

SCENARIO_DECISION_NOTES = {
    "planning-permission": "This usually decides whether the next move is a simpler permitted-development route, a certificate check or a fuller planning application.",
    "permitted-development": "This usually decides whether the simpler route still holds up once local controls, site history and the exact property position are checked properly.",
    "height-limits": "This usually decides whether measured drawings keep the scheme viable or whether a redesign is safer before anything is submitted.",
    "boundary-rules": "This usually decides whether the design still feels comfortable near the boundary or whether siting and neighbour impact are already too tight.",
    "conservation-areas": "This usually decides whether the proposal still looks routine or whether heritage controls make the local authority angle the real issue.",
    "article-4": "This usually decides whether the shortcut route still exists at all or whether a formal permission route should be treated as the safer baseline.",
    "maximum-height": "This usually decides whether the design is still comfortably below the limit or whether one measurement point is already pushing the route into doubt.",
}

LOCAL_CONTEXT_VARIANTS = [
    "The local read often turns on whether the scheme still looks obviously policy-compliant without needing caveats or fallback assumptions.",
    "A lot of the practical risk sits in how easily the authority can read the drawings as routine rather than borderline.",
    "What matters locally is often not the headline rule alone but whether the proposal still feels comfortable in context when viewed as a whole.",
    "Schemes that rely on one generous interpretation usually feel weaker locally than schemes that read as comfortably compliant at first glance.",
    "The local authority layer often becomes decisive when the design only works if every assumption is read in the applicant's favour.",
    "This is why two technically similar schemes can land differently once design judgement, setting and local sensitivity are weighed together.",
    "The more the route depends on explanation instead of clear drawings and clear siting, the more locally fragile it usually becomes.",
]

DECISION_PATTERN_VARIANTS = [
    "The cleaner route usually belongs to schemes that can be explained in one sentence without leaning on exceptions or caveats.",
    "Proposals get harder when the planning story has to work around one weak measurement, one awkward siting choice or one sensitive elevation.",
    "Designs that stay obviously subordinate tend to travel better than designs that only just avoid looking overbuilt.",
    "A modest redraw early on is often cheaper than defending a layout that already feels tight on paper.",
    "Where local sensitivity is doing most of the work, better evidence usually matters more than more optimistic wording.",
    "Projects are usually easier to back when the drawings, photos and planning history all point in the same direction.",
    "If the route still depends on several 'probably fine' assumptions, that is often the sign to slow down and verify properly.",
]

ROUTE_CONTEXT_VARIANTS = [
    "Read the first answer as an early route filter, then use the rest of the page to check the detail that could change it.",
    "Start with the plain-English route, then test it against the drawings, planning history and any local control.",
    "Use the first answer to avoid the wrong path, then slow down where one measurement or designation could change the result.",
    "Treat the headline as a triage step; the safer decision comes from checking the exact site context below.",
    "Begin with the most likely route, then check whether the property has a local reason to be treated more cautiously.",
    "Use this page to separate the broad rule from the detail that would matter before drawings, quotes or an application.",
    "Let the first answer narrow the route, then use the follow-up checks to decide whether formal confirmation is sensible.",
    "Keep the route practical: answer the main question first, then verify the local factor that could make it less simple.",
    "Use the opening answer to sort the route, then check whether local evidence supports that reading.",
    "Start broad, then narrow quickly into the property-specific point that would matter to a council officer.",
    "The first answer should save time, but the safer route still comes from checking the exact constraint below.",
    "Use this page to decide whether the issue is routine, borderline or already asking for formal confirmation.",
    "Begin with the likely route, then check whether the proposal relies on one generous assumption.",
    "Treat the first screen as a route sorter before you move into measurements, design details and official sources.",
    "Use the top answer to choose the right lane, then check whether the local record keeps that lane open.",
    "Start here to reduce the guesswork, then verify the factor that would be hardest to fix later.",
    "The aim is to get you into the right next check quickly, not to turn a broad rule into a false guarantee.",
    "Use the route summary to decide what to read next, then confirm the point that could cost money if missed.",
    "Open with the likely answer, then pressure-test it against the site detail that matters most.",
    "Use this as a practical sorting step before you decide whether a certificate, pre-app check or application is sensible.",
    "Let the first answer remove obvious dead ends, then check the evidence needed before anyone relies on the route.",
    "Start with the route that looks most likely, then use the page to find the reason it might not hold.",
    "The first screen is deliberately cautious; the useful work is spotting what would make the answer change.",
    "Use the answer to choose the next move, then keep the council or formal-check route in view if the project is close to a limit.",
]


def _scenario_copy_label(scenario_slug: str = "", scenario_title: str = "") -> str:
    clean_slug = str(scenario_slug or "").strip()
    clean_title = str(scenario_title or "").strip().lower()
    labels = {
        "planning-permission": "planning permission",
        "permitted-development": "permitted development",
        "height-limits": "height limits",
        "maximum-height": "maximum height",
        "depth-limits": "depth limits",
        "boundary-rules": "boundary rules",
        "distance-from-boundary": "boundary distance",
        "roof-alterations": "roof alterations",
        "conservation-areas": "conservation area controls",
        "listed-buildings": "listed building controls",
        "article-4": "Article 4",
    }
    title_labels = {
        "boundary distance rules": "boundary rules",
        "distance from boundary": "boundary distance",
    }
    return labels.get(clean_slug) or title_labels.get(clean_title) or clean_title


def _scenario_copy_verb(label: str) -> str:
    return "are" if str(label or "").lower().endswith("s") else "is"


def _scenario_guidance_cta(scenario_slug: str, scenario_title: str, project_title: str, town_name: str) -> dict[str, str]:
    scenario_label = _scenario_copy_label(scenario_slug, scenario_title)
    scenario_verb = _scenario_copy_verb(scenario_label)
    if scenario_slug in {"article-4", "planning-permission", "permitted-development"}:
        return {
            "title": "Need A More Confident Read Before You Rely On It?",
            "description": f"If {scenario_label} {scenario_verb} the point keeping {project_title.lower()} alive in {town_name}, use the personalised guidance route for a more specific steer on whether the safer next move is a certificate, a pre-app check or a fuller application route.",
            "intro_label": "Route sense-check",
        }
    if scenario_slug in {"conservation-areas", "listed-buildings"}:
        return {
            "title": "Need A Heritage-Sensitive Read On This Rule?",
            "description": f"If {scenario_label} {scenario_verb} doing most of the work for {project_title.lower()} in {town_name}, use the personalised guidance route for a more careful steer on what changes locally and when formal heritage or council input becomes the safer route.",
            "intro_label": "Heritage sense-check",
        }
    if scenario_slug in {"boundary-rules", "height-limits", "maximum-height", "distance-from-boundary"}:
        return {
            "title": "Need A Threshold And Measurement Sense-Check?",
            "description": f"If {scenario_label} {scenario_verb} the controlling issue for {project_title.lower()} in {town_name}, use the personalised guidance route for a clearer read on the controlling measurements, the local tripwires and the safest next verification step.",
            "intro_label": "Measurement check",
        }
    return {
        "title": "Need A More Tailored View On This Rule Question?",
        "description": f"If you are still weighing up whether {scenario_title.lower()} changes the route for {project_title.lower()} in {town_name}, use the personalised guidance route for a more case-specific plain-English steer.",
        "intro_label": "Next step",
    }


def _seed_value(*parts) -> int:
    return sum(ord(char) for part in parts for char in str(part))


def _rotate(items, *seed_parts):
    ordered = [item for item in items if item]
    if not ordered:
        return []
    offset = _seed_value(*seed_parts) % len(ordered)
    return ordered[offset:] + ordered[:offset]


def _town_size_bucket(county_slug: str, town_name: str) -> str:
    clean_county = str(county_slug or "").strip().lower()
    clean_town = str(town_name or "").strip().lower()
    if clean_county == "greater-london":
        return "large"
    if "city" in clean_town or len(clean_town.split()) >= 3:
        return "large"
    if clean_county in {"cornwall", "cumbria", "herefordshire", "lincolnshire", "northumberland", "somerset", "wales"}:
        return "small"
    return "medium"


def _property_assumption(project_type: str, county_slug: str, town_name: str) -> str:
    town_size = _town_size_bucket(county_slug, town_name)
    family = PROJECT_TYPE_PROPERTY_ASSUMPTIONS.get(project_type or "", PROJECT_TYPE_PROPERTY_ASSUMPTIONS["extension"])
    return family.get(town_size, family.get("medium", "a typical family house"))


def _scenario_constraint(rule, scenario_slug: str) -> str:
    restrictions = useful_local_restrictions(rule)
    if restrictions:
        return restrictions[0][0].lower()
    return SCENARIO_CONSTRAINT_HINTS.get(scenario_slug, "the exact site constraints and measured drawings")


def _scenario_permission_score(project_type: str, scenario_slug: str, rule) -> int:
    score = 1
    restrictions = useful_local_restrictions(rule)
    score += min(len(restrictions), 2)
    if scenario_slug in {"planning-permission", "conservation-areas", "article-4", "listed-buildings"}:
        score += 2
    elif scenario_slug in {"permitted-development", "boundary-rules", "height-limits"}:
        score += 1
    if project_type in {"change-of-use", "microgeneration"}:
        score += 1
    if (rule or {}).get("restrictions", {}).get("article4_applies"):
        score += 1
    return score


def _likelihood_label(score: int) -> str:
    if score >= 5:
        return "Higher chance a formal permission route or certificate check will be needed"
    if score >= 3:
        return "Mixed picture: a certificate or formal application is plausible"
    return "Lower chance of needing a full permission route if the measurements stay comfortable"


def _risk_label(score: int) -> str:
    if score >= 5:
        return "High"
    if score >= 3:
        return "Medium"
    return "Low"


def _format_restriction_labels(restrictions, limit: int = 2) -> str:
    labels = [label.lower() for label, _ in restrictions[:limit] if label]
    if not labels:
        return ""
    if len(labels) == 1:
        return labels[0]
    if len(labels) == 2:
        return f"{labels[0]} and {labels[1]}"
    return f"{', '.join(labels[:-1])}, and {labels[-1]}"


def _next_step_hint(project_type: str, scenario_slug: str, rule) -> str:
    restrictions = useful_local_restrictions(rule)
    if restrictions:
        labels = _format_restriction_labels(restrictions)
        return f"Confirm whether {labels} can change the route before you rely on the baseline answer."
    if scenario_slug in {"planning-permission", "permitted-development"}:
        return "Run the planning decision tool, then compare the local project guide if the route still feels borderline."
    if scenario_slug in {"boundary-rules", "height-limits", "maximum-height", "distance-from-boundary"}:
        return "Measure the controlling dimensions first, then compare the local project guide before finalising drawings."
    if scenario_slug in {"conservation-areas", "listed-buildings", "article-4"}:
        return "Check the heritage or local-control status first, then move to the council guide if the site is affected."
    if project_type == "loft":
        return "Check roof form, visibility and measured drawings before assuming the simpler route still holds."
    return "Open the matching local project guide next, then verify formally if the proposal sits close to a limit."


def _scenario_trigger_bullets(project_type: str, scenario_slug: str, rule) -> tuple[list[str], list[str]]:
    restrictions = useful_local_restrictions(rule)
    local_control = (
        f"local controls such as {_format_restriction_labels(restrictions)} apply"
        if restrictions
        else "local controls, planning history or site constraints change the baseline answer"
    )
    needs_permission = {
        "planning-permission": [
            "the proposal is close to a size, use, siting or neighbour-impact threshold",
            local_control,
        ],
        "permitted-development": [
            "the simpler fallback has been removed or narrowed for the exact property",
            "the design only works if several borderline measurements are read generously",
        ],
        "height-limits": [
            "the height is close to the controlling measurement point",
            "boundary position, roof form or ground levels make the measurement less straightforward",
        ],
        "boundary-rules": [
            "the proposal sits close to a boundary, highway or neighbour-sensitive edge",
            "siting, privacy or access issues are doing more work than the project label",
        ],
        "conservation-areas": [
            "the work is visible, changes materials or affects a heritage-sensitive elevation",
            "the proposal depends on the heritage effect being treated as minor",
        ],
        "article-4": [
            "the direction removes the permitted-development right the project would otherwise rely on",
            "the exact property or use is inside the affected area or class of work",
        ],
    }.get(
        scenario_slug,
        [
            "the rule is close enough to the limit that drawings or formal confirmation would settle it faster",
            local_control,
        ],
    )
    simpler_route = {
        "planning-permission": [
            "the design is comfortably within the normal limits and local controls do not change the route",
            "the next check is only confirmation, not a rescue plan for a borderline scheme",
        ],
        "permitted-development": [
            "the property, site history and local controls still leave the fallback intact",
            "the measurements are comfortably inside the limits rather than just under them",
        ],
        "conservation-areas": [
            "the change is modest, visually quiet and backed by the local conservation context",
            "materials, frontage and setting do not create a heritage-led objection",
        ],
        "article-4": [
            "the direction does not cover this property, use or class of work",
            "the remaining issue is ordinary design detail rather than loss of the fallback route",
        ],
    }.get(
        scenario_slug,
        [
            "the controlled measurement or local issue is comfortably resolved",
            "the project can be explained without leaning on exceptions or optimistic assumptions",
        ],
    )
    return needs_permission[:2], simpler_route[:2]


def _scenario_heading(scenario_slug: str, scenario_title: str, town_name: str) -> str:
    base = SCENARIO_PAGE_HEADINGS.get(scenario_slug, scenario_title)
    return f"{base} In {town_name}"


def _scenario_h1(clean_project: str, scenario_slug: str, scenario_title: str, town_name: str) -> str:
    clean_lower = clean_project.lower()
    specific = {
        ("garden room", "planning-permission"): f"Planning permission for a garden room in {town_name}",
        ("garden room", "permitted-development"): f"Garden room permitted development in {town_name}",
        ("garden room", "height-limits"): f"Garden room height limits in {town_name}",
        ("garden room", "boundary-rules"): f"Garden room boundary rules in {town_name}",
        ("fences and walls", "planning-permission"): f"Fence planning permission in {town_name}",
        ("fences and walls", "boundary-rules"): f"Boundary fence rules in {town_name}",
        ("fences and walls", "height-limits"): f"Fence height limits in {town_name}",
        ("fences and walls", "maximum-height"): f"Maximum fence height in {town_name}",
        ("outbuildings", "planning-permission"): f"Outbuilding planning permission in {town_name}",
        ("outbuildings", "boundary-rules"): f"Outbuilding boundary rules in {town_name}",
        ("outbuildings", "height-limits"): f"Outbuilding height limits in {town_name}",
        ("house extension", "planning-permission"): f"House extension planning permission in {town_name}",
        ("house extension", "boundary-rules"): f"House extension boundary rules in {town_name}",
    }
    if (clean_lower, scenario_slug) in specific:
        return specific[(clean_lower, scenario_slug)]
    label = SCENARIO_H1_LABELS.get(scenario_slug, scenario_title.lower())
    return f"{clean_project} in {town_name}: {label}"


def _scenario_intent_note(scenario_slug: str, town_name: str) -> str:
    return SCENARIO_INTENT_NOTES.get(
        scenario_slug,
        "This page is most useful when one local planning rule is doing most of the work and the council-level reading matters more than a broad explainer.",
    ).format(town=town_name)


def _scenario_first_step_note(scenario_slug: str, town_name: str) -> str:
    notes = {
        "planning-permission": f"Use this page when the live question is planning permission in {town_name} and you need to know what usually changes the route locally before you open the wrong next page.",
        "permitted-development": f"Use this page when the live question is permitted development in {town_name} and you need to know whether the simpler route still survives once local controls, site history and the exact property position are checked properly.",
        "conservation-areas": f"Use this page when conservation areas in {town_name} are the reason a familiar project has stopped looking straightforward.",
        "article-4": f"Use this page when Article 4 in {town_name} may be removing the fallback route people usually assume is still there.",
        "boundary-rules": f"Use this page when boundary rules in {town_name} are doing more work than the project label on its own.",
        "height-limits": f"Use this page when height limits in {town_name} look like the rule most likely to settle the route quickly.",
        "maximum-height": f"Use this page when maximum height in {town_name} is the measurement most likely to settle the route quickly.",
        "depth-limits": f"Use this page when depth limits in {town_name} are doing most of the work in the planning answer.",
        "distance-from-boundary": f"Use this page when distance from boundary in {town_name} is the measurement most likely to change the route.",
        "roof-alterations": f"Use this page when roof alterations in {town_name} are the part most likely to change the planning route.",
        "listed-buildings": f"Use this page when listed building controls in {town_name} may make the usual project route too broad.",
    }
    return notes.get(
        scenario_slug,
        f"Use this page when {scenario_slug.replace('-', ' ')} in {town_name} looks like the rule doing most of the work in the planning answer.",
    )


def vary_paragraph(base_sentences, project_type="", town_size="", scenario_slug="", town_name="", seed_key="", sentence_count=2, conditional_inserts=None):
    ordered = _rotate(base_sentences, seed_key, project_type, town_size, scenario_slug, town_name)
    if conditional_inserts:
        if conditional_inserts.get(project_type):
            ordered.append(conditional_inserts[project_type])
        if conditional_inserts.get(town_size):
            ordered.append(conditional_inserts[town_size])
        if conditional_inserts.get(scenario_slug):
            ordered.append(conditional_inserts[scenario_slug])
    final_sentences = _rotate(ordered, "final", seed_key, project_type, town_size, scenario_slug, town_name)
    return " ".join(final_sentences[: max(1, min(sentence_count, len(final_sentences)))])


def build_your_situation_summary(project_title, project_type, scenario_title, town_name, county_slug, rule, scenario_slug):
    risk_score = _scenario_permission_score(project_type, scenario_slug, rule)
    key_constraint = _scenario_constraint(rule, scenario_slug)
    risk_label = _risk_label(risk_score)
    likelihood = _likelihood_label(risk_score)
    property_assumption = _property_assumption(project_type, county_slug, town_name)
    next_step = _next_step_hint(project_type, scenario_slug, rule)

    items = [
        f"<li><strong>Assumed setup:</strong> {project_title} on {property_assumption} in {town_name}.</li>",
        f"<li><strong>Likely permission position:</strong> {likelihood}.</li>",
        f"<li><strong>Likely key constraint:</strong> The live issue is usually {key_constraint}.</li>",
        f"<li><strong>Likely risk level:</strong> {risk_label}.</li>",
        f"<li><strong>What to check next:</strong> {next_step}</li>",
    ]

    return f"""
<section class="situation-summary" id="scenario-summary">
<span class="eyebrow">Working view</span>
<h2>What This Usually Means On A Typical Site</h2>
<ul class="checklist">{''.join(items)}</ul>
</section>
"""


def build_scenario_jump_links(scenario_title: str, town_name: str) -> str:
    return f"""
<section class="page-jump-links">
<span class="eyebrow">Jump to what matters</span>
<h2>How To Read This Page Quickly</h2>
<div class="link-grid">
<a href="#scenario-summary">Start with the practical local read for {scenario_title.lower()} in {town_name}</a>
<a href="#scenario-signal">See the local signals that usually change the answer</a>
<a href="#scenario-decision-guide">Check when this rule stays manageable and when it usually escalates</a>
<a href="#scenario-faq">Read the most common follow-up questions</a>
<a href="#scenario-next-steps">Open the best next pages once the blocker is clearer</a>
<a href="#scenario-trust">Use the trust notes if the proposal is close to a limit</a>
</div>
</section>
"""


def _render_cta_cards(card_keys, *, include_council=False, town_name="", town_slug=""):
    cards = []
    seen = set()

    for key in card_keys:
        item = PROMOTED_LINKS.get(key)
        if not item or item["href"] in seen:
            continue
        seen.add(item["href"])
        cards.append(
            f"""
<a class="card" href="{item['href']}">
<div class="card-kicker">Planning tool</div>
<h3>{item['title']}</h3>
<p>{item['description']}</p>
<span class="cta">{item['cta']}</span>
</a>
"""
        )

    if include_council and town_slug:
        href = f"/councils/{town_slug}/"
        if href not in seen:
            cards.append(
                f"""
<a class="card" href="{href}">
<div class="card-kicker">Council guide</div>
<h3>Wider {town_name} planning context</h3>
<p>Open the council guide if local policy, heritage coverage or authority-specific behaviour matters more than this one rule.</p>
<span class="cta">View council guide</span>
</a>
"""
            )

    return "".join(cards)


def _scenario_cta_keys(scenario_slug: str, *, for_conversion=False):
    mapping = {
        "planning-permission": ["planning_decision_tool", "planning_rejection_risk_tool"],
        "permitted-development": ["planning_decision_tool", "planning_rejection_risk_tool"],
        "height-limits": ["planning_decision_tool", "site_constraint_checker"],
        "boundary-rules": ["planning_decision_tool", "site_constraint_checker"],
        "conservation-areas": ["planning_route_planner", "planning_decision_tool"],
        "listed-buildings": ["planning_route_planner", "planning_decision_tool"],
        "article-4": ["planning_route_planner", "planning_decision_tool"],
    }
    keys = mapping.get(scenario_slug, ["planning_decision_tool", "what_can_i_build_explorer"])
    if for_conversion and scenario_slug in {"planning-permission", "permitted-development"}:
        return ["planning_decision_tool", "planning_rejection_risk_tool"]
    if for_conversion:
        return [keys[0], "faq_need_planning"]
    return keys


def _scenario_support_cta_keys(scenario_slug: str):
    mapping = {
        "planning-permission": ["project_requirements_generator"],
        "permitted-development": ["project_requirements_generator"],
        "height-limits": ["planning_route_planner"],
        "boundary-rules": ["planning_route_planner"],
        "conservation-areas": ["site_constraint_checker"],
        "listed-buildings": ["site_constraint_checker"],
        "article-4": ["site_constraint_checker"],
    }
    return mapping.get(scenario_slug, [])


def build_scenario_navigation(project_slug, county_slug, town_slug, scenarios, current_slug):
    links = []

    for scenario in scenarios:
        slug = scenario["slug"]
        title = scenario["title"]
        url = f"/{project_slug}/{county_slug}/{town_slug}/{slug}/"
        cls = "active" if slug == current_slug else ""

        link = safe_link(url, title)
        link = link.replace('<a ', f'<a class="scenario-nav {cls}" ')
        links.append(link)

    return f"""
<section>
<span class="eyebrow">Related local rule pages</span>
<h2>Switch To The Rule That Looks More Relevant</h2>
<div class='scenario-navigation'>{''.join(links)}</div>
</section>
"""


def build_scenario_hero(clean_project, scenario_title, town_name, county_name, rule, scenario_slug, project_type=""):
    quick_answer = scenario_rule_excerpt(rule, scenario_slug) or (
        f"{scenario_title} can change whether {clean_project.lower()} in {town_name} needs planning permission or a more formal planning check."
    )
    intro = _scenario_first_step_note(scenario_slug, town_name)
    route_context = _rotate(ROUTE_CONTEXT_VARIANTS, town_name, county_name, scenario_slug, clean_project)[0]
    blocker_label = {
        "boundary-rules": "boundary rules",
        "distance-from-boundary": "boundary distance",
        "height-limits": "height",
        "maximum-height": "maximum height",
        "depth-limits": "depth",
        "roof-alterations": "roof alterations",
    }.get(scenario_slug, scenario_title.lower())
    blocker_verb = "are" if blocker_label.endswith("s") else "is"
    next_step = (
        f"Start here if {blocker_label} {blocker_verb} the controlling issue, then move to the main {clean_project.lower()} page or the council guide if the answer still depends on wider local context."
    )

    permission_bullets, simpler_bullets = _scenario_trigger_bullets(project_type, scenario_slug, rule)

    return f"""
<section class="hero">
<span class="badge">Local rule guide</span>
<h1>{_scenario_h1(clean_project, scenario_slug, scenario_title, town_name)}</h1>
<p>{intro} {route_context}</p>
<p>{next_step}</p>
<div class="tool-result">
<strong>Quick answer:</strong> {quick_answer}
</div>
<div class="answer-grid">
<div class="answer-card">
<h3>You may need planning permission if</h3>
<ul class="checklist">{''.join(f"<li>{item}</li>" for item in permission_bullets)}</ul>
</div>
<div class="answer-card">
<h3>Usually simpler if</h3>
<ul class="checklist">{''.join(f"<li>{item}</li>" for item in simpler_bullets)}</ul>
</div>
<div class="answer-card">
<h3>Best next check</h3>
<p><a href="/tools/planning-decision-tool/">Check if your project is likely to need permission</a> or <a href="/tools/site-constraint-checker/">check local constraints before you apply</a>.</p>
</div>
</div>
</section>
"""


def build_scenario_jurisdiction_notice(rule, town_name):
    return build_jurisdiction_notice((rule or {}).get("county_slug", ""), town_name, "rule guide")


def render_scenario_rules(rule, scenario_slug):
    if not rule:
        return ""

    rule_label_map = {
        "planning-permission": "Planning permission position",
        "permitted-development": "Permitted development position",
        "height-limits": "Height rule detail",
        "maximum-height": "Maximum height rule detail",
        "depth-limits": "Depth rule detail",
        "boundary-rules": "Boundary rule detail",
        "distance-from-boundary": "Boundary distance detail",
        "roof-alterations": "Roof alteration detail",
        "conservation-areas": "Conservation area detail",
        "listed-buildings": "Listed building detail",
        "article-4": "Article 4 detail",
    }
    detail = scenario_rule_excerpt(rule, scenario_slug)
    restrictions = useful_local_restrictions(rule)
    if not detail and not restrictions:
        return ""

    restriction_html = ""
    if restrictions:
        restriction_html = (
            "<ul class='checklist'>"
            + "".join(f"<li><strong>{label}:</strong> {text}</li>" for label, text in restrictions[:3])
            + "</ul>"
        )

    return f"""
<section class="rule-detail">
<span class="eyebrow">Rule detail</span>
<h2>{rule_label_map.get(scenario_slug, "Local rule detail")}</h2>
{f"<p>{detail}</p>" if detail else ""}
{restriction_html}
</section>
"""


def build_scenario_intro(project_title, scenario_title, town_name, rng, project_type="", county_slug=""):
    town_size = _town_size_bucket(county_slug, town_name)
    scenario_label = _scenario_copy_label(scenario_title=scenario_title)
    scenario_verb = _scenario_copy_verb(scenario_label)
    intro = vary_paragraph(
        [
            f"This page focuses on how {scenario_label} affect {project_title.lower()} projects in {town_name}.",
            f"For {project_title.lower()} projects in {town_name}, {scenario_label} {scenario_verb} often what separates a straightforward route from a more cautious one.",
            f"If {scenario_label} {scenario_verb} the part making the answer feel uncertain in {town_name}, this page is meant to settle that question first.",
        ],
        project_type=project_type,
        town_size=town_size,
        scenario_slug=scenario_title.lower().replace(" ", "-"),
        town_name=town_name,
        seed_key="scenario-intro",
        sentence_count=2,
        conditional_inserts=TOWN_SIZE_INSERTS,
    )

    return f"""
<section class='scenario-intro'>
<span class="eyebrow">Why this page exists</span>
<h2>Why This Rule Deserves A Separate Check</h2>
<p>{intro}</p>
</section>
"""


def build_local_restriction_snapshot(rule, town_name):
    restrictions = useful_local_restrictions(rule)
    if not restrictions:
        return ""

    items = "".join(f"<li><strong>{label}:</strong> {text}</li>" for label, text in restrictions)
    return f"""
<section class="local-restrictions">
<span class="eyebrow">Local restriction snapshot</span>
<h2>Extra Local Checks For {town_name}</h2>
<ul class="checklist">{items}</ul>
</section>
"""


def build_scenario_decision_guide(project_title, scenario_title, town_name, rule, scenario_slug, project_type=""):
    restrictions = useful_local_restrictions(rule)
    manageable = {
        "planning-permission": [
            "The proposal still reads as a routine householder change once the actual design is measured properly.",
            "Local restrictions are not obviously removing the simpler route or making the scheme more sensitive.",
            "The drawings do not rely on optimistic assumptions about scale, neighbour effect or site history.",
        ],
        "permitted-development": [
            "The design still looks comfortably inside the normal limits for this rule, not merely close to them.",
            "The property type, site history and local designations do not obviously remove the simpler fallback.",
            "The proposal can be explained cleanly without stretching the baseline interpretation.",
        ],
        "conservation-areas": [
            "The change is modest, visually quiet and does not depend on aggressive alterations in a heritage setting.",
            "Materials, frontage impact and the wider setting still support a routine-looking answer.",
            "The site is not relying on the heritage context being ignored or read generously.",
        ],
        "article-4": [
            "The property is not actually affected by the direction for the work in question.",
            "The route can still be supported by the live local wording rather than a broad assumption.",
            "The remaining uncertainty is about the project detail, not whether the simpler right has gone.",
        ],
    }.get(
        scenario_slug,
        [
            "The proposal can be measured and described cleanly against the rule without stretching the interpretation.",
            "The local restrictions are not doing most of the work in the answer.",
            "The design is not sitting right on the line where formal confirmation becomes the safer route.",
        ],
    )

    escalation = {
        "planning-permission": [
            "The route already depends on a generous reading of the scheme rather than a comfortable one.",
            "Local restrictions, heritage coverage or neighbour impact are likely to do more work than the headline rule.",
            "The project is close enough to a limit that a formal application or certificate check may be cheaper than redesign later.",
        ],
        "permitted-development": [
            "The answer only works if multiple borderline measurements all break your way.",
            "The property type, planning history or local controls may already remove the simpler route.",
            "You would be relying on the broad national wording rather than the exact local position.",
        ],
        "conservation-areas": [
            "Visibility, demolition, materials or setting changes are already likely to attract a closer heritage reading.",
            "The design is only viable if the authority treats the heritage impact as minor when that still needs proving.",
            "The local conservation context is more important than the underlying project type alone.",
        ],
        "article-4": [
            "The direction may already remove the fallback route for the exact class of work or change of use.",
            "The live question is really the legal coverage of the direction, not the project details alone.",
            "The proposal cannot sensibly proceed until the local wording and coverage are checked properly.",
        ],
    }.get(
        scenario_slug,
        [
            "The proposal is close to a hard limit or depends on a generous interpretation of the rule.",
            "Local restrictions or site history may already be doing more work than the rule headline suggests.",
            "Drawings or a formal check would likely settle the issue faster than more generic reading.",
        ],
    )

    if restrictions:
        labels = _format_restriction_labels(restrictions)
        escalation.insert(0, f"In {town_name}, {labels} can tighten how this rule lands locally.")

    evidence = [
        "Measured drawings showing the exact part of the proposal this rule controls.",
        "Photos or notes that show the relevant heritage, boundary, frontage or visibility context.",
        "A clean note on planning history, permitted development assumptions or local constraints that may alter the baseline answer.",
    ]

    return f"""
<section class="decision-guide" id="scenario-decision-guide">
<span class="eyebrow">Decision guide</span>
<h2>When This Rule Usually Stays Manageable And When It Pushes The Route Harder</h2>
<div class="answer-grid">
<div class="answer-card">
<h3>Often manageable when</h3>
<ul class="checklist">{''.join(f"<li>{item}</li>" for item in manageable[:3])}</ul>
</div>
<div class="answer-card">
<h3>Pause and check when</h3>
<ul class="checklist">{''.join(f"<li>{item}</li>" for item in escalation[:3])}</ul>
</div>
<div class="answer-card">
<h3>Evidence that usually settles it faster</h3>
<ul class="checklist">{''.join(f"<li>{item}</li>" for item in evidence)}</ul>
</div>
</div>
</section>
"""


def build_scenario_calculator_block(project_title, scenario_title, town_name, rule, scenario_slug):
    main_point = scenario_rule_excerpt(rule, scenario_slug) or "Measure the proposal carefully against the relevant planning limits."
    restrictions = restriction_messages(rule)
    local_check = (
        f"Review local controls such as {_format_restriction_labels(restrictions)} before relying on the general rule."
        if restrictions
        else "Check whether any local designations, previous permissions or site history change the normal answer."
    )

    return f"""
<section class="self-check">
<span class="eyebrow">Self-check</span>
<h2>What To Check Before You Rely On This Rule</h2>
<ul class="checklist">
<li>{main_point}</li>
<li>{local_check}</li>
<li>If the design is close to a limit, prepare measured drawings and consider written confirmation before work starts in {town_name}.</li>
</ul>
</section>
"""


def build_rule_comparison(project_title, town_name):
    return f"""
<section class="rule-comparison">
<span class="eyebrow">Simple route vs harder route</span>
<h2>{project_title} In {town_name}: When This Rule Usually Stays Manageable And When It Does Not</h2>
<table>
<tr><th>If the proposal stays comfortably within the usual envelope</th><th>If it pushes the limit or local controls apply</th></tr>
<tr><td>You may be able to rely on the simpler planning route.</td><td>You are more likely to need a planning application, written confirmation or a more cautious redesign.</td></tr>
</table>
<p>In {town_name}, the correct route still depends on design details, site constraints and the wider local context.</p>
</section>
"""


def build_local_planning_context(town_name, county_name, clean_project, project_type="", county_slug="", scenario_slug=""):
    system_label = "English planning system"
    if county_name.lower() == "wales":
        system_label = "Welsh planning system"
    elif county_name.lower() == "scotland":
        system_label = "Scottish planning system"
    elif county_name.lower() == "northern ireland":
        system_label = "Northern Ireland planning system"
    town_size = _town_size_bucket(county_slug or county_name.lower().replace(" ", "-"), town_name)
    context_intro = vary_paragraph(
        [
            f"The local planning authority for {town_name}, {county_name} may apply policies or design expectations that sit alongside the {system_label}.",
            f"Even where the headline national rule looks familiar, {town_name} can still produce a different planning route once local controls are layered in.",
            f"The local authority angle matters because the same rule can feel straightforward on one site and much less comfortable on another nearby plot.",
        ],
        project_type=project_type,
        town_size=town_size,
        scenario_slug=scenario_slug,
        town_name=town_name,
        seed_key="local-context",
        sentence_count=2,
        conditional_inserts=TOWN_SIZE_INSERTS,
    )
    local_emphasis = _rotate(
        LOCAL_CONTEXT_VARIANTS,
        "local-context-emphasis",
        project_type,
        scenario_slug,
        county_slug,
        town_name,
    )[0]
    return f"""
<section class="local-context">
<span class="eyebrow">Local context</span>
<h2>Why The Same Rule Can Land Differently Locally</h2>
<p>{context_intro}</p>
<p>That is why two similar {clean_project.lower()} proposals can follow different routes if the site sits in a conservation area, affects a listed building or has awkward boundary conditions.</p>
<p>{local_emphasis}</p>
</section>
"""


def build_real_world_examples(project_title, scenario_title, town_name, rule, project_type="", county_slug="", scenario_slug=""):
    main_point = scenario_rule_excerpt(rule, scenario_title.lower().replace(" ", "-"))
    if not main_point:
        main_point = "A proposal close to the planning threshold often needs a more careful review."
    town_size = _town_size_bucket(county_slug, town_name)

    patterns = _rotate(
        [
            f"Straightforward schemes tend to progress better when the drawings clearly prove compliance with the {scenario_title.lower()} rule.",
            f"Borderline proposals in {town_name} often need revision when the first design assumes too much flexibility.",
            "Where the planning route is uncertain, written confirmation is usually cheaper than redesigning later.",
            PROJECT_TYPE_VARIATION_INSERTS.get(project_type, ""),
            TOWN_SIZE_INSERTS.get(town_size, ""),
            _rotate(
                DECISION_PATTERN_VARIANTS,
                "decision-pattern-variant",
                project_type,
                scenario_slug,
                county_slug,
                town_name,
            )[0],
        ],
        "decision-patterns",
        project_type,
        scenario_slug,
        town_name,
    )

    items = "".join(f"<li>{item}</li>" for item in patterns)
    return f"""
<section class='decision-patterns'>
<span class="eyebrow">Common tripwires</span>
<h2>What Usually Makes These Projects Easier Or Harder</h2>
<p>{main_point}</p>
<ul class="checklist">{items}</ul>
</section>
"""


def build_scenario_faq(project_title, scenario_title, town_name, rule, scenario_slug):
    rule_answer = scenario_rule_excerpt(rule, scenario_slug) or (
        f"{scenario_title} should be checked against the exact dimensions, design and site context of the proposal."
    )
    restrictions = restriction_messages(rule)
    local_answer = (
        "Yes. Local designations can change the planning route or remove permitted development rights."
        if restrictions
        else "Yes. Councils can still apply local policy and site-specific constraints even where the national rule looks similar."
    )

    faqs = [
        (
            f"Do I need planning permission for {project_title} in {town_name}?",
            rule_answer,
        ),
        (
            f"What should I measure first for {scenario_title.lower()}?",
            "Start with the dimension or design feature that this rule controls, then check how the whole proposal sits relative to the house and the boundary.",
        ),
        (
            "Can the answer change because of local restrictions?",
            local_answer,
        ),
        (
            "What is the safest next step if the proposal is close to the limit?",
            "Prepare measured drawings and consider written confirmation or a lawful development certificate before work starts.",
        ),
    ]

    html = "".join(f"<div class='faq-item'><h3>{q}</h3><p>{a}</p></div>" for q, a in faqs)
    return f"""
<section class='faq' id="scenario-faq">
<span class="eyebrow">Frequently asked questions</span>
<h2>Questions People Usually Ask At This Point</h2>
{html}
<script type="application/ld+json">{faq_schema(faqs)}</script>
</section>
"""


def build_internal_rule_links(project_slug, county_slug, town_slug, scenario_slug):
    links = build_internal_links(
        project_slug,
        county_slug,
        town_slug,
        scenario_slug=scenario_slug,
    )
    if not links:
        return ""

    return f"""
<section class='internal-links'>
<span class="eyebrow">Useful follow-up pages</span>
<h2>What To Check Next For This Project</h2>
{links}
</section>
"""


def build_nearby_council_links(project_slug, county_slug, town_slug, councils_by_county):
    councils = councils_by_county.get(county_slug, [])
    links = []
    project_name = PROJECTS_BY_SLUG.get(project_slug, {}).get("short_name", "This project")

    for council in councils:
        other_slug = council.get("town_slug")
        other_name = council.get("town_name")
        if not other_slug or other_slug == town_slug:
            continue

        url = f"/{project_slug}/{county_slug}/{other_slug}/"
        links.append(safe_link(url, f"{project_name} in {other_name}"))

    if not links:
        return ""

    return f"""
<section class='nearby-links'>
<span class="eyebrow">Nearby comparison</span>
<h2>Compare Nearby Areas</h2>
<div class='link-grid'>{''.join(links)}</div>
</section>
"""


def build_related_projects(project_slug, county_slug, town_slug):
    links = []
    project_type = PROJECTS_BY_SLUG.get(project_slug, {}).get("type", "")
    related_projects = [
        project for project in PROJECT_GROUPS.get(project_type, [])
        if project["slug"] != project_slug
    ]

    for project in related_projects[:6]:
        links.append(
            safe_link(
                f"/{project['slug']}/{county_slug}/{town_slug}/",
                f"{project['short_name']} in {town_slug.replace('-', ' ').title()}",
            )
        )

    if not links:
        return ""

    return f"""
<section class='related-projects'>
<span class="eyebrow">Related local project pages</span>
<h2>Compare Similar Project Types</h2>
<div class='link-grid'>{''.join(links)}</div>
</section>
"""


def build_global_link_cluster(project_slug, county_slug, town_slug, scenarios, current_slug, councils_by_county):
    return f"""
<section class="link-cluster" id="scenario-next-steps">
<span class="eyebrow">Where to look next</span>
<h2>Useful Next Steps From This Rule Page</h2>
<div class="grid-tight">
<a class="card" href="/tools/what-can-i-build-explorer/">
<div class="card-kicker">Explorer</div>
<h3>Explore the likely project options</h3>
<p>Use the explorer if you are still deciding between extensions, loft space or other project directions for the property.</p>
<span class="cta">Explore options</span>
</a>
<a class="card" href="/tools/planning-decision-tool/">
<div class="card-kicker">Tool</div>
<h3>Run the quick planning tool</h3>
<p>Use the tool when you need a faster first steer before comparing detailed local pages.</p>
<span class="cta">Open tool</span>
</a>
<a class="card" href="/tools/planning-rejection-risk-analyzer/">
<div class="card-kicker">Risk tool</div>
<h3>Check the likely refusal risks</h3>
<p>Use the risk analyzer when the route looks real and you want to see the objections most likely to derail the application.</p>
<span class="cta">Open analyzer</span>
</a>
<a class="card" href="/councils/{town_slug}/">
<div class="card-kicker">Council page</div>
<h3>See the wider local authority context</h3>
<p>Open the council page if the bigger local planning picture matters more than this one rule.</p>
<span class="cta">View council guide</span>
</a>
</div>
<details class="support-disclosure">
<summary>Show more rule follow-ups, nearby comparisons and related project pages</summary>
{build_internal_rule_links(project_slug, county_slug, town_slug, current_slug)}
{build_nearby_council_links(project_slug, county_slug, town_slug, councils_by_county)}
{build_related_projects(project_slug, county_slug, town_slug)}
</details>
</section>
"""


def build_trust_section(project_title, town_name, county_name):
    return build_trust_framework(
        section_id="scenario-trust",
        eyebrow="Trust and caveats",
        title="How To Use This Rule Page Responsibly",
        purpose=f"This page is designed to make one planning rule easier to interpret for {project_title.lower()} in {town_name} so the controlling issue, the main tripwires and the safest next step are easier to judge.",
        not_replace="It does not replace the council record, the exact property position or any formal confirmation needed when this rule is the thing keeping the route alive.",
        built_from=f"The page combines the {planning_system_label(county_name)} baseline with local authority context and rule-specific evidence such as measured thresholds, heritage sensitivity, planning history and site constraints.",
        verify_when="Escalate once the answer depends on a tight measurement, a sensitive site, or an interpretation you would not want to defend after drawings or applications are in motion.",
        safest_next_step="Use a lawful development certificate when the scheme appears lawful but this rule is carrying too much of the risk. Use pre-application advice when local judgement or policy weight is likely to matter more than the headline rule.",
        support_links=[
            (PROMOTED_LINKS[key]["title"], PROMOTED_LINKS[key]["href"])
            for key in SCENARIO_SUPPORT_LINK_KEYS
        ],
    )


def build_printable_guide():
    return "<section class='printable-guide'><h2>Want A Printable Version?</h2><p>Print this page if you want a straightforward note to review measurements, questions and next checks away from the screen.</p><button onclick='window.print()'>Print this planning guide</button></section>"


def assemble_scenario_page(components):
    return "\n".join(component for component in components if component)


def build_tool_cta(slug):
    card_keys = _scenario_cta_keys(slug)
    if not card_keys:
        return ""
    return f"""
<section class="tool-cta">
<span class="eyebrow">Use the tools</span>
<h2>Need A Faster First Answer?</h2>
<p>These tools work best when the route is still unresolved and you want a more personalised first steer before opening more pages.</p>
<div class="grid-tight">
{_render_cta_cards(card_keys)}
</div>
</section>
"""


def build_council_scenario_signal_block(scenario_title, town_name, rule, scenario_slug):
    restriction_items = useful_local_restrictions(rule)
    rule_signal = scenario_rule_excerpt(rule, scenario_slug) or (
        f"{scenario_title} is one of the local checks most likely to change the planning route in {town_name}."
    )
    restriction_html = (
        "<ul class='checklist'>"
        + "".join(f"<li><strong>{label}:</strong> {text}</li>" for label, text in restriction_items[:3])
        + "</ul>"
        if restriction_items
        else "<p>No standout local designation is surfaced in this local rule set, but site-specific controls and planning history should still be checked before relying on the baseline answer.</p>"
    )

    return f"""
<section id="scenario-signal">
<span class="eyebrow">What changes the answer here</span>
<h2>The Local Signals Most Likely To Change The Answer In {town_name}</h2>
<div class="answer-grid">
<div class="answer-card">
<h3>Main local rule signal</h3>
<p>{rule_signal}</p>
</div>
<div class="answer-card">
<h3>Restrictions worth checking</h3>
{restriction_html}
</div>
<div class="answer-card">
<h3>Why it matters</h3>
<p>{SCENARIO_DECISION_NOTES.get(scenario_slug, 'These are the local triggers most likely to push a seemingly simple scheme into a more cautious route, a redesign, or a formal certificate or planning application.')}</p>
</div>
</div>
</section>
"""


def build_council_scenario_hero(scenario_title, town_name, county_name, rule, scenario_slug, project_type=""):
    quick_answer = scenario_rule_excerpt(rule, scenario_slug) or (
        f"{scenario_title} can change whether a project in {town_name} stays on the simpler route or needs a more formal council check."
    )
    intro = _scenario_first_step_note(scenario_slug, town_name)
    next_step = (
        f"Use the rule summary below to decide whether the real next move is the matching project guide, the wider council page or a stronger formal check before drawings or submissions."
    )

    return f"""
<section class="hero">
<span class="badge">Local rule guide</span>
<h1>{_scenario_heading(scenario_slug, scenario_title, town_name)}</h1>
<p>{intro}</p>
<p>{next_step}</p>
<div class="tool-result">
<strong>Quick answer:</strong> {quick_answer}
</div>
</section>
"""


def build_council_scenario_jurisdiction_notice(county_slug: str, town_name: str) -> str:
    return build_jurisdiction_notice(county_slug, town_name, "local rule guide")


def build_council_scenario_intro(scenario_title, town_name, rng, project_type="", county_slug="", scenario_slug=""):
    town_size = _town_size_bucket(county_slug, town_name)
    scenario_label = _scenario_copy_label(scenario_slug or scenario_title.lower().replace(" ", "-"), scenario_title)
    scenario_verb = _scenario_copy_verb(scenario_label)
    intro = vary_paragraph(
        [
            _scenario_intent_note(scenario_slug or scenario_title.lower().replace(" ", "-"), town_name),
            f"This page isolates the local {scenario_label} picture in {town_name} so you can move faster from a vague concern into the right next check.",
            f"For homeowners in {town_name}, {scenario_label} {scenario_verb} often easier to understand once the local authority context is pulled into one place.",
        ],
        project_type=project_type,
        town_size=town_size,
        scenario_slug=scenario_slug or scenario_title.lower().replace(" ", "-"),
        town_name=town_name,
        seed_key="council-scenario-intro",
        sentence_count=2,
        conditional_inserts=TOWN_SIZE_INSERTS,
    )

    return f"""
<section class='scenario-intro'>
<span class="eyebrow">Why this page exists</span>
<h2>The Local Version Of This Planning Question</h2>
<p>{intro}</p>
</section>
"""


def build_council_scenario_search_intent(scenario_title, town_name, rule, scenario_slug, project_type="", county_slug=""):
    search_prompts = {
        "planning-permission": f"planning permission {town_name}",
        "permitted-development": f"permitted development {town_name}",
        "height-limits": f"height limits {town_name}",
        "boundary-rules": f"boundary rules {town_name}",
        "conservation-areas": f"{town_name} conservation areas",
        "article-4": f"{town_name} article 4",
        "maximum-height": f"maximum height {town_name}",
    }
    search_prompt = search_prompts.get(scenario_slug, f"{scenario_title.lower()} {town_name}")
    rule_signal = scenario_rule_excerpt(rule, scenario_slug) or (
        f"{scenario_title} is one of the main local rule checks that can change the answer in {town_name}."
    )
    restrictions = restriction_messages(rule)
    local_shift = (
        f"The main local shifts here are {_format_restriction_labels(restrictions)}."
        if restrictions
        else SCENARIO_DECISION_NOTES.get(
            scenario_slug,
            "The biggest local shifts usually come from heritage controls, Article 4, site history or a proposal that is close to a limit.",
        )
    )
    search_match = vary_paragraph(
        [
            f"Useful when the real question sounds like {search_prompt} and you want the local version rather than a broad national answer.",
            f"Open this when the search is really about {search_prompt} and the next step depends on the local authority angle.",
            f"This page works best when the live question is closer to {search_prompt} than to a general planning explainer.",
        ],
        project_type=project_type,
        town_size=_town_size_bucket(county_slug, town_name),
        scenario_slug=scenario_slug,
        town_name=town_name,
        seed_key="search-intent",
        sentence_count=1,
        conditional_inserts=None,
    )

    return f"""
<section>
<span class="eyebrow">What this page helps settle</span>
<h2>What This Local Rule Usually Helps You Decide</h2>
<div class="answer-grid">
<div class="answer-card">
<h3>Searches this page best answers</h3>
<p>{search_match}</p>
</div>
<div class="answer-card">
<h3>What most often changes the result</h3>
<p>{rule_signal}</p>
</div>
<div class="answer-card">
<h3>What to keep in view</h3>
<p>{local_shift}</p>
</div>
</div>
</section>
"""


def build_scenario_internal_link_boost(project_slug, county_slug, town_slug, councils_by_county):
    project = PROJECTS_BY_SLUG.get(project_slug, {})
    project_name = project.get("short_name", project.get("title", "This project"))
    local_links = []
    local_seen = set()
    non_local_links = []
    non_local_seen = set()

    def add_local(href, label):
        if href not in local_seen and len(local_links) < 12:
            local_seen.add(href)
            local_links.append((href, label))

    def add_non_local(href, label):
        if href not in non_local_seen and len(non_local_links) < 12:
            non_local_seen.add(href)
            non_local_links.append((href, label))

    add_local(f"/{project_slug}/{county_slug}/", f"{project_name} across {county_slug.replace('-', ' ').title()}")
    local_councils = _rotate(
        [item for item in councils_by_county.get(county_slug, []) if item.get("town_slug") != town_slug],
        "local-link-boost",
        project_slug,
        county_slug,
        town_slug,
    )
    for council in local_councils:
        add_local(
            f"/{project_slug}/{county_slug}/{council['town_slug']}/",
            f"{project_name} in {council['town_name']}",
        )
    for council in local_councils:
        if len(local_links) >= 12:
            break
        add_local(f"/councils/{council['town_slug']}/", f"{council['town_name']} planning authority guide")

    other_counties = _rotate(
        [item for item in sorted(councils_by_county) if item != county_slug],
        "non-local-link-boost",
        project_slug,
        county_slug,
        town_slug,
    )
    for other_county in other_counties:
        add_non_local(
            f"/{project_slug}/{other_county}/",
            f"{project_name} in {other_county.replace('-', ' ').title()}",
        )
        if len(non_local_links) >= 12:
            break

    local_html = "".join(f'<a href="{href}">{label}</a>' for href, label in local_links)
    non_local_html = "".join(f'<a href="{href}">{label}</a>' for href, label in non_local_links)

    return f"""
<section class="scenario-link-boost">
<span class="eyebrow">Keep exploring</span>
<h2>Compare Local And Wider Project Pages Without Losing The Thread</h2>
<div class="info-columns">
<div class="mini-card">
<h3>Local county project pages</h3>
<div class="link-grid">{local_html}</div>
</div>
<div class="mini-card">
<h3>Same project in other planning areas</h3>
<div class="link-grid">{non_local_html}</div>
</div>
</div>
</section>
"""


def _council_scenario_faq_card(scenario_slug):
    faq_map = {
        "planning-permission": (
            "Do I Need Planning Permission?",
            "/planning-faq/do-i-need-planning-permission/",
            "Useful when the route question is still broader than one local rule page.",
        ),
        "permitted-development": (
            "When A Lawful Development Certificate Is Worth It",
            "/planning-faq/lawful-development-certificate/",
            "A strong follow-up when the simpler route may apply but certainty still matters.",
        ),
        "height-limits": (
            "How To Measure Height For Planning Permission",
            "/planning-faq/how-to-measure-height-for-planning-permission/",
            "Useful when the rule turns on exactly how the height is measured in practice.",
        ),
        "boundary-rules": (
            "How To Measure Distance From Boundary",
            "/planning-faq/how-to-measure-distance-from-boundary/",
            "Useful when siting and measurements are doing most of the work in the planning answer.",
        ),
        "conservation-areas": (
            "Planning Rules In Conservation Areas",
            "/planning-faq/conservation-area-planning-rules/",
            "Useful when heritage context is the real reason the route feels less straightforward.",
        ),
    }
    return faq_map.get(
        scenario_slug,
        (
            "Planning Permission Questions, Answered Clearly",
            "/planning-faq/",
            "Use the wider FAQ library when this rule page is only part of the planning question.",
        ),
    )


def build_project_scenario_signal_block(project_title, scenario_title, town_name, rule, scenario_slug):
    restriction_items = useful_local_restrictions(rule)
    rule_signal = scenario_rule_excerpt(rule, scenario_slug) or (
        f"{scenario_title} is one of the local checks most likely to change the planning route for {project_title.lower()} in {town_name}."
    )
    restriction_html = (
        "<ul class='checklist'>"
        + "".join(f"<li><strong>{label}:</strong> {text}</li>" for label, text in restriction_items[:3])
        + "</ul>"
        if restriction_items
        else "<p>No standout local designation is surfaced in this local rule set, but site-specific controls and planning history should still be checked before relying on the baseline answer.</p>"
    )

    return f"""
<section id="scenario-signal">
<span class="eyebrow">What changes because of this rule</span>
<h2>The Local Signals Most Likely To Change The Answer For {project_title} In {town_name}</h2>
<div class="answer-grid">
<div class="answer-card">
<h3>Main local rule signal</h3>
<p>{rule_signal}</p>
</div>
<div class="answer-card">
<h3>Restrictions worth checking</h3>
{restriction_html}
</div>
<div class="answer-card">
<h3>What this usually changes</h3>
<p>{SCENARIO_DECISION_NOTES.get(scenario_slug, 'These are the local triggers most likely to push a seemingly simple scheme into a more cautious route, a redesign, or a formal certificate or planning application.')}</p>
</div>
</div>
</section>
"""


def build_project_scenario_priority_routes(
    project_slug,
    county_slug,
    town_slug,
    town_name,
    scenario_slug,
    scenario_title,
):
    title, href, description = _council_scenario_faq_card(scenario_slug)
    project = PROJECTS_BY_SLUG.get(project_slug, {})
    project_name = project.get("short_name", project.get("title", "This project"))
    tool_cards = _render_cta_cards(_scenario_cta_keys(scenario_slug)[:1])
    sibling_cards = []

    for scenario in rollout_scenarios_for_project(project_slug):
        sibling_slug = scenario.get("slug", "")
        sibling_title = scenario.get("title", "")
        if not sibling_slug or sibling_slug == scenario_slug:
            continue
        sibling_cards.append(
            f"""
<a class="card" href="/{project_slug}/{county_slug}/{town_slug}/{sibling_slug}/">
<div class="card-kicker">Same project, next rule</div>
<h3>{project_name} and {sibling_title.lower()} in {town_name}</h3>
<p>Open the sister rule page if the remaining doubt is about {sibling_title.lower()} rather than the wider project route.</p>
<span class="cta">Open rule page</span>
</a>
"""
        )
        if len(sibling_cards) >= 2:
            break

    return f"""
<section id="scenario-next-steps">
<span class="eyebrow">Best next routes</span>
<h2>Open The Page That Matches The Remaining Question</h2>
<div class="grid">
<a class="card" href="/{project_slug}/{county_slug}/{town_slug}/">
<div class="card-kicker">Main project guide</div>
<h3>{project_name} in {town_name}</h3>
<p>Go back to the main local project page if the live question is wider than {scenario_title.lower()} on its own.</p>
<span class="cta">Open project guide</span>
</a>
{''.join(sibling_cards)}
<a class="card" href="/{scenario_slug}/{town_slug}/">
<div class="card-kicker">Top-level rule page</div>
<h3>{scenario_title} in {town_name}</h3>
<p>Use the broader local rule page if the blocker applies across multiple project types and you need the rule first.</p>
<span class="cta">Open rule page</span>
</a>
<a class="card" href="{href}">
<div class="card-kicker">FAQ follow-up</div>
<h3>{title}</h3>
<p>{description}</p>
<span class="cta">Read answer</span>
</a>
{tool_cards}
</div>
</section>
"""


def build_council_scenario_priority_routes(project_links, scenario_slug, town_name, town_slug):
    title, href, description = _council_scenario_faq_card(scenario_slug)
    lead_project_card = ""
    if project_links:
        project = project_links[0]
        lead_project_card = f"""
<a class="card" href="{project['href']}">
<div class="card-kicker">Local project guide</div>
<h3>{project['title']} in {town_name}</h3>
<p>{project['summary']}</p>
<span class="cta">Open project guide</span>
</a>
"""

    return f"""
<section id="scenario-next-steps">
<span class="eyebrow">Best next routes</span>
<h2>Open The Page That Matches The Remaining Question</h2>
<div class="grid">
{lead_project_card}
<a class="card" href="{href}">
<div class="card-kicker">FAQ follow-up</div>
<h3>{title}</h3>
<p>{description}</p>
<span class="cta">Read answer</span>
</a>
<a class="card" href="/councils/{town_slug}/">
<div class="card-kicker">Council guide</div>
<h3>Wider {town_name} planning context</h3>
<p>Open the council guide if local policy, heritage controls or authority-specific context matters more than this one rule.</p>
<span class="cta">View council guide</span>
</a>
{_render_cta_cards(_scenario_cta_keys(scenario_slug)[:1], town_name=town_name, town_slug="", include_council=False)}
</div>
</section>
"""


def build_council_scenario_project_links(project_links, town_name):
    if not project_links:
        return ""

    cards = []
    for item in project_links:
        cards.append(
            f"""
<a class="card" href="{item['href']}">
<div class="card-kicker">Local project guide</div>
<h3>{item['title']} in {town_name}</h3>
<p>{item['summary']}</p>
<span class="cta">Open project guide</span>
</a>
"""
        )

    return f"""
<section>
<span class="eyebrow">Best local follow-ups</span>
<h2>Project Guides Where This Rule Usually Matters Most</h2>
<div class="grid">{''.join(cards)}</div>
</section>
"""


def build_council_scenario_support_links(scenario_slug, town_name, town_slug):
    title, href, description = _council_scenario_faq_card(scenario_slug)
    secondary_keys = _scenario_support_cta_keys(scenario_slug)

    return f"""
<section>
<span class="eyebrow">Process and verification help</span>
<h2>Useful Follow-Ups If {scenario_slug.replace('-', ' ')} Is Not The Only Question</h2>
<div class="grid">
<a class="card" href="{href}">
<div class="card-kicker">FAQ follow-up</div>
<h3>{title}</h3>
<p>{description}</p>
<span class="cta">Read answer</span>
</a>
<a class="card" href="/councils/{town_slug}/">
<div class="card-kicker">Council context</div>
<h3>Wider {town_name} planning context</h3>
<p>Open the council guide if local policy, heritage coverage or authority behaviour matters more than this one rule.</p>
<span class="cta">View council guide</span>
</a>
{_render_cta_cards(secondary_keys)}
</div>
</section>
"""


def build_council_scenario_navigation(town_slug, scenarios, current_slug):
    links = []

    for scenario in scenarios:
        slug = scenario["slug"]
        title = scenario["title"]
        url = f"/{slug}/{town_slug}/"
        cls = "active" if slug == current_slug else ""
        link = safe_link(url, title)
        link = link.replace('<a ', f'<a class="scenario-nav {cls}" ')
        links.append(link)

    return f"""
<section>
<span class="eyebrow">Related local rule pages</span>
<h2>Switch To The Rule That Looks More Relevant</h2>
<div class='scenario-navigation'>{''.join(links)}</div>
</section>
"""


def build_council_scenario_faq(scenario_title, town_name, rule, scenario_slug):
    scenario_label = _scenario_copy_label(scenario_slug, scenario_title)
    scenario_verb = _scenario_copy_verb(scenario_label)
    rule_answer = scenario_rule_excerpt(rule, scenario_slug) or (
        f"{scenario_title} should be checked against the exact dimensions, design and site context of the proposal."
    )
    restrictions = restriction_messages(rule)
    local_answer = (
        "Yes. Local designations can change the planning route or remove permitted development rights."
        if restrictions
        else "Yes. The council context can still change how straightforward the national baseline really is."
    )

    faqs = [
        (
            f"How do {scenario_label} affect projects in {town_name}?" if scenario_verb == "are" else f"How does {scenario_label} affect projects in {town_name}?",
            rule_answer,
        ),
        (
            "Can the answer change because of local restrictions?",
            local_answer,
        ),
        (
            "What is the safest next step if the proposal is close to the limit?",
            "Prepare measured drawings, compare the relevant local project guide and consider written confirmation before work starts.",
        ),
        (
            f"Where should I click next if {scenario_label} {scenario_verb} the live issue?",
            f"Open the matching project guide in {town_name}, then compare the council page and the planning tools if the route still feels borderline.",
        ),
    ]

    html = "".join(f"<div class='faq-item'><h3>{q}</h3><p>{a}</p></div>" for q, a in faqs)
    return f"""
<section class='faq'>
<span class="eyebrow">Frequently asked questions</span>
<h2>Questions People Usually Ask At This Point</h2>
{html}
<script type="application/ld+json">{faq_schema(faqs)}</script>
</section>
"""


def build_council_scenario_global_links(town_slug, county_slug, councils_by_county, scenario_slug=""):
    nearby_links = []
    for council in councils_by_county.get(county_slug, []):
        other_slug = council.get("town_slug")
        other_name = council.get("town_name")
        if not other_slug or other_slug == town_slug:
            continue
        nearby_links.append(f'<a href="/councils/{other_slug}/">{other_name}</a>')
        if len(nearby_links) >= 6:
            break

    return f"""
<section class="link-cluster">
<span class="eyebrow">Where to look next</span>
<h2>Useful Next Steps From This Rule Page</h2>
<div class="grid-tight">
{_render_cta_cards(["what_can_i_build_explorer", "planning_route_planner"], include_council=True, town_name=town_slug.replace("-", " ").title(), town_slug=town_slug)}
</div>
<div class="card">
<div class="card-kicker">Nearby comparison</div>
<h2>Compare Nearby Authorities</h2>
<div class="link-grid">{''.join(nearby_links)}</div>
</div>
</section>
"""


def build_council_scenario_trust_section(scenario_title, town_name, county_name):
    scenario_label = _scenario_copy_label(scenario_title=scenario_title)
    return build_trust_framework(
        eyebrow="Trust and caveats",
        title="How To Use This Rule Page Responsibly",
        purpose=f"This page is designed to make {scenario_label} easier to interpret in {town_name} so you can narrow the issue quickly and move into the right project, council or formal route.",
        not_replace="It does not replace the exact property checks, council records or formal confirmation needed when this rule is deciding whether the route survives.",
        built_from=f"The page combines the {planning_system_label(county_name)} baseline with local authority context and the rule-specific evidence most likely to change the answer on a real site.",
        verify_when="Verify formally if the design depends on this rule breaking your way, if the site is sensitive, or if the planning-history position is still unclear.",
        safest_next_step="Use pre-application advice or another formal check when the scheme only works if this rule is read in the most favourable way. Use a lawful development certificate where the route appears lawful but certainty matters.",
        support_links=[
            (PROMOTED_LINKS[key]["title"], PROMOTED_LINKS[key]["href"])
            for key in SCENARIO_SUPPORT_LINK_KEYS
        ],
    )


def build_conversion_hook(project_title, scenario_title, town_name, scenario_slug="", town_slug=""):
    cta = _scenario_guidance_cta(scenario_slug, scenario_title, project_title, town_name)
    cta_variation = _rotate(ROUTE_CONTEXT_VARIANTS, town_name, scenario_slug, project_title)[0]
    return build_personalised_guidance_cta(
        title=cta["title"],
        description=f"{cta['description']} {cta_variation}",
        context_label="scenario-page",
        email_context=f"{scenario_title} in {town_name}",
        intro_label=cta["intro_label"],
        compact=True,
        prefill={
            "authority": town_name,
            "location": town_name,
            "project_stage": "Comparing options and measurements",
            "project_summary": f"{project_title} in {town_name}",
            "main_worry": cta["description"],
        },
    ) + render_result_capture(f"scenario-{scenario_slug or 'route'}-{town_slug or town_name.lower().replace(' ', '-')}-capture")


def build_scenario_route_check_cta(scenario_slug: str) -> str:
    if not should_show_route_check_scenario_cta(scenario_slug):
        return ""
    variant = "c" if scenario_slug in {"conservation-areas", "listed-buildings", "article-4"} else "b"
    return build_planning_route_check_cta(
        variant=variant,
        source_page_type="scenario-page",
        scenario_slug=scenario_slug,
        compact=True,
    )
