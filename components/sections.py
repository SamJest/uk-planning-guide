import re

from components.faq_blocks import build_faq_section
from components.planning_helpers import first_text, restriction_messages, useful_local_restrictions, useful_local_rule_items
from components.find_help_pages import build_find_help_cta, should_show_find_help_project_cta
from components.jurisdiction_notices import build_jurisdiction_notice
from components.personalised_guidance import build_personalised_guidance_cta
from components.planning_route_check import (
    build_planning_route_check_cta,
    should_show_route_check_project_cta,
)
from components.shared_components import render_result_capture
from components.trust_framework import build_trust_framework, planning_system_label
from data.gsc_recovery_routes import gsc_recovery_routes_for_project, recovery_path
from data.search_demand_priorities import hmo_article_4_priority_for
from data.loaders import load_councils, load_projects
from data.promoted_links import PROMOTED_LINKS
from utils.internal_links import build_internal_links, build_nearby_links
from utils.live_links import is_live_internal_href, normalize_internal_href
from utils.project_scenario_config import project_scenario_href
from utils.scenario_relevance import filter_relevant_scenarios
from utils.content_variation import rotate, town_size_bucket, vary_paragraph


PROJECTS = load_projects()
PROJECTS_BY_SLUG = {project["slug"]: project for project in PROJECTS}
COUNCILS_BY_COUNTY = load_councils()

PROJECT_TYPE_VARIATION_INSERTS = {
    "extension": "Extension-led projects often become less straightforward when size, neighbour impact and previous additions all stack together.",
    "loft": "Loft-led projects often turn on roof form, visibility and whether the alteration still reads as subordinate.",
    "outbuilding": "Outbuilding-style projects usually stay simpler when the structure still reads as clearly secondary to the main house.",
    "microgeneration": "Energy projects often look simple at first but can still turn on visibility, siting and local sensitivity.",
    "change-of-use": "Change-of-use proposals usually depend on policy and neighbour impact as much as the physical building itself.",
    "external": "External works often become planning-sensitive because frontage, visibility and drainage issues pile up quickly.",
}

TOWN_SIZE_INSERTS = {
    "small": "In a smaller authority area, visible changes and neighbour relationships often stand out more quickly once the local context is understood.",
    "medium": "In a typical authority area, a proposal can look routine until local policy and site context are checked properly.",
    "large": "In a denser authority area, visibility, amenity pressure and policy context often stack up earlier than expected.",
}

PROJECT_ROUTE_CONTEXT_VARIANTS = [
    "Use the first answer as a route filter, then check the local details before paying for drawings.",
    "Start with the local route, then test the project against the issue most likely to change it.",
    "Read this as practical triage: useful for direction, but still tied to the exact property.",
    "The safest path is to narrow the route first, then verify the measurement or local control doing the most work.",
    "Use this page to avoid the wrong next step before you move into drawings, quotes or a formal application.",
    "Treat the headline route as the beginning of the check, not the final property-specific answer.",
    "The route is easier to judge when the project type, local context and official checks are kept together.",
    "Keep the decision simple at first, then slow down if the proposal is close to a limit or local restriction.",
]

PROJECT_FAMILY_BRIEFS = {
    "loft-conversions": {
        "heading": "Loft Conversion Planning",
        "intro": "For loft conversions in {town}, the real issue is usually whether roof form, dormer bulk and local controls still leave the simpler route intact.",
        "local_change": "Roof form, dormer bulk, visibility and local restrictions are usually the checks that change the answer first.",
        "next_check": "Check roof form, dormer scale and any front-facing change before relying on the simpler route.",
    },
    "dormer-extensions": {
        "heading": "Dormer Extension Planning",
        "intro": "With dormers in {town}, the live question is usually whether the addition still looks subordinate enough to stay on the simpler route.",
        "local_change": "Dormer bulk, roof form, visibility and local restrictions are usually the checks that move the answer.",
        "next_check": "Check dormer scale, roof form and visibility before treating the route as straightforward.",
    },
    "roof-lights": {
        "heading": "Rooflight Planning",
        "intro": "For rooflights in {town}, the answer usually turns on projection, roof slope and any local controls that make a simple job less simple.",
        "local_change": "Projection above the roof plane, visibility and local restrictions are usually the first checks that matter.",
        "next_check": "Check whether the rooflights project beyond the roof plane and whether the elevation is sensitive locally.",
    },
    "dropped-kerbs": {
        "heading": "Dropped Kerb Planning",
        "intro": "Dropped-kerb questions in {town} usually come down to whether planning permission, highways approval or both are doing the real work. This page is built to get you to the local route before you pay for the wrong thing.",
        "local_change": "Highway approval, frontage visibility, drainage and whether the access point sits on the highway side are the checks most likely to change the answer locally.",
        "next_check": "Check whether the proposal also needs highway approval, visibility checks or drainage changes alongside any planning answer.",
    },
    "driveways": {
        "heading": "Driveway Planning",
        "intro": "Driveway questions in {town} usually turn on whether the surface, drainage or access arrangement pushes the route beyond a simple answer.",
        "local_change": "Permeability, frontage treatment, drainage and whether a dropped kerb sits alongside the job are the local checks most likely to change the answer.",
        "next_check": "Check surface drainage and whether the driveway also needs a dropped kerb or other highway-side approval.",
    },
    "hard-surfaces": {
        "heading": "Hard Surfacing Planning",
        "intro": "For hard surfacing, paving and front-garden parking in {town}, the important question is whether the baseline answer still survives the drainage and frontage checks.",
        "local_change": "Drainage, impermeable surfaces and visible frontage changes are the checks most likely to make a hard-surfacing answer less straightforward locally.",
        "next_check": "Check whether the proposed surface is permeable and whether the frontage layout triggers a stricter planning or drainage route.",
    },
    "change-of-use": {
        "heading": "Change Of Use Planning",
        "intro": "Change-of-use cases in {town} usually turn on use class, local policy and neighbour effect rather than physical building work alone.",
        "local_change": "Local policy wording, neighbour impact and whether the use still fits the surrounding street are the issues most likely to change the answer locally.",
        "next_check": "Check the live use class route first, then verify whether local policy or neighbour impact is the real blocker.",
    },
    "hmos": {
        "heading": "HMO Planning",
        "intro": "HMO cases in {town} usually hinge on change of use, local policy and Article 4 rather than the broad housing question people start with.",
        "local_change": "Article 4 coverage, HMO concentration, amenity pressure and the local authority's change-of-use stance are the checks most likely to move the answer.",
        "next_check": "Check Article 4 coverage, concentration pressure and whether the route is really a change-of-use question before anything else.",
    },
    "garden-rooms": {
        "heading": "Garden Room Planning",
        "intro": "With garden rooms in {town}, the key issue is whether the building still reads as a normal incidental outbuilding or starts to need a more formal route.",
        "local_change": "Height, boundary siting, intended use and whether the building still reads as clearly incidental are the local checks most likely to change the answer.",
        "next_check": "Check height, boundary position and how the intended use would be described if the building is larger than a simple incidental structure.",
    },
    "outbuildings": {
        "heading": "Outbuilding Planning",
        "intro": "For outbuildings in {town}, the answer usually turns on height, boundary position, use and any local restrictions that make a modest scheme less routine.",
        "local_change": "Height, siting, use and local restrictions are the checks most likely to turn a simple outbuilding answer into a more cautious one.",
        "next_check": "Check whether the structure still reads as secondary to the house, and whether the proposed use makes the route stricter.",
    },
    "annexes": {
        "heading": "Annexe Planning",
        "intro": "Annexe cases in {town} usually come down to whether the accommodation stays genuinely ancillary to the main house or starts to look self-contained.",
        "local_change": "Self-contained use, scale, boundary position and how the local authority treats ancillary accommodation are the checks most likely to change the answer.",
        "next_check": "Check whether the annexe stays clearly ancillary to the main house or starts to look like a separate dwelling in planning terms.",
    },
    "fences-and-walls": {
        "heading": "Fence And Wall Planning",
        "intro": "For fences, walls and boundary gates in {town}, the real issue is usually the controlling height, the highway side of the site and any local visibility concerns.",
        "local_change": "Highway-facing position, the highest adjoining ground level and local visibility concerns are the checks most likely to change the answer for fences and walls.",
        "next_check": "Check whether the controlling height point sits next to the highway or on the higher side of the ground level before relying on the baseline answer.",
    },
    "house-extensions": {
        "heading": "House Extension Planning",
        "intro": "With house extensions in {town}, the real question is whether the scheme still fits the simpler route or is drifting toward planning permission once the local checks are applied.",
        "local_change": "Depth, height, neighbour relationship, previous additions and local restrictions are the checks most likely to change the extension answer locally.",
        "next_check": "Check the scale against the original house first, then verify whether local restrictions or previous additions make the simpler route less reliable.",
    },
    "wraparound-extensions": {
        "heading": "Wraparound Extension Planning",
        "intro": "Wraparound extensions in {town} usually hinge on whether the combined side-and-rear footprint still feels subordinate once depth, width, neighbour effect and previous additions are checked together.",
        "local_change": "Combined projection, neighbour relationship, original-house baseline and local restrictions are the checks most likely to make a wraparound scheme more cautious.",
        "next_check": "Check the overall side-and-rear footprint against the original house first, then verify whether the local route still survives once neighbour effect and restrictions are added back in.",
    },
    "two-storey-extensions": {
        "heading": "Two-Storey Extension Planning",
        "intro": "Two-storey extensions in {town} usually become planning-sensitive where depth, upper-floor neighbour effect, roof relationship and the original-house baseline start stacking together.",
        "local_change": "Depth, two-storey bulk, upper-floor impact, previous additions and local restrictions are the checks most likely to move the route.",
        "next_check": "Check the upper-floor depth and neighbour relationship early, then verify whether previous additions or local restrictions make the simpler route unrealistic.",
    },
    "windows-and-doors": {
        "heading": "Windows And Doors Planning",
        "intro": "Windows and doors in {town} are usually easiest when the work still reads as like-for-like joinery rather than a new opening pattern, privacy change or broader elevation redesign.",
        "local_change": "New openings, altered privacy relationships, visible frontage change and local restrictions are the checks most likely to change the answer for windows and doors.",
        "next_check": "Check whether the project is still a straightforward replacement job, then verify whether privacy, frontage change or local restrictions make the route stricter.",
    },
    "temporary-buildings": {
        "heading": "Temporary Building Planning",
        "intro": "Temporary building cases in {town} usually turn on duration, physical setup and whether the structure still reads as genuinely short-term once neighbour and site-edge effects are checked.",
        "local_change": "Duration, physical setup, neighbour effect, servicing and local restrictions are the checks most likely to turn a temporary structure into a fuller planning question.",
        "next_check": "Check what keeps the structure genuinely short-term first, then verify whether the site setup, neighbour effect or local restrictions make the route harder to rely on.",
    },
}

GENERIC_ROUTE_MARKERS = (
    "most householder development follows national permitted development rules",
    "householder development follows national permitted development rules",
)


def _project_type_from_slug(project_slug: str) -> str:
    return PROJECTS_BY_SLUG.get(project_slug, {}).get("type", "")


def _project_type_from_title(project_title: str) -> str:
    title = str(project_title or "").lower()
    if "loft" in title or "dormer" in title or "roof" in title:
        return "loft"
    if "outbuilding" in title or "garden room" in title or "garage" in title or "annexe" in title:
        return "outbuilding"
    if "solar" in title or "heat pump" in title:
        return "microgeneration"
    if "change of use" in title or "hmo" in title:
        return "change-of-use"
    if "driveway" in title or "window" in title or "door" in title or "hard surfacing" in title:
        return "external"
    return "extension"


def _project_focus_key(project_slug: str, project_title: str = "") -> str:
    slug = str(project_slug or "").strip().lower()
    if slug in {"dropped-kerbs", "driveways", "hard-surfaces", "fences-and-walls"}:
        return "frontage"
    if slug in {"hmos", "change-of-use"}:
        return "use"
    if slug in {"garden-rooms", "outbuildings", "annexes", "garages", "garage-conversions"}:
        return "outbuilding"
    if slug in {"loft-conversions", "dormer-extensions", "roof-lights"}:
        return "loft"
    if slug in {"heat-pumps", "solar-panels"}:
        return "microgeneration"
    if slug in {"windows-and-doors"}:
        return "external"
    project_type = _project_type_from_slug(project_slug) or _project_type_from_title(project_title)
    if project_type == "change-of-use":
        return "use"
    return project_type or "extension"


def _project_guidance_cta(project_slug: str, project_title: str, town_name: str) -> dict[str, str]:
    focus = _project_focus_key(project_slug, project_title)
    if focus == "frontage":
        return {
            "title": "Need The Planning Route Separated From The Access Or Frontage Route?",
            "description": f"If {project_title.lower()} in {town_name} depends on visibility, drainage, frontage layout or highway approval, use the personalised guidance route for a clearer next-step steer before you pay for the wrong work.",
            "intro_label": "Route sense-check",
        }
    if focus == "use":
        return {
            "title": "Need The Policy Route Narrowed Before You Go Further?",
            "description": f"If {project_title.lower()} in {town_name} depends on use intensity, Article 4, amenity pressure, parking or local policy, use the personalised guidance route for a cleaner read on the route and the safest next formal check.",
            "intro_label": "Policy sense-check",
        }
    if focus == "outbuilding":
        return {
            "title": "Need A Clearer Read On Incidental Use, Scale Or Siting?",
            "description": f"If {project_title.lower()} in {town_name} hangs on whether the building stays secondary to the house, use the personalised guidance route for a more specific steer on the route, the likely tripwires and what to verify formally.",
            "intro_label": "Project sense-check",
        }
    if focus == "loft":
        return {
            "title": "Need A Roof-Form And Threshold Sense-Check?",
            "description": f"If {project_title.lower()} in {town_name} is drifting toward a borderline roof change, use the personalised guidance route for a more specific read on the likely route, visibility issues and the next check worth paying for.",
            "intro_label": "Roof-route check",
        }
    return {
        "title": "Need A More Tailored Steer On This Project?",
        "description": f"If {project_title.lower()} in {town_name} still turns on scale, siting, previous additions or local restrictions, use the personalised guidance route for a practical plain-English steer on the likely route and the safest next formal check.",
        "intro_label": "Final sense-check",
    }


def _join_labels(labels: list[str]) -> str:
    clean = [str(label).strip().lower() for label in labels if str(label).strip()]
    if not clean:
        return ""
    if len(clean) == 1:
        return clean[0]
    if len(clean) == 2:
        return f"{clean[0]} and {clean[1]}"
    return f"{', '.join(clean[:-1])} and {clean[-1]}"


def _dedupe_copy_items(items: list[str], *, drop_generic: bool = False) -> list[str]:
    cleaned: list[str] = []
    seen: set[str] = set()

    for item in items:
        text = " ".join(str(item or "").split()).strip()
        if not text:
            continue

        lowered = text.lower()
        key = lowered.rstrip(".")
        if key in seen:
            continue

        seen.add(key)
        cleaned.append(text)

    return cleaned


def _project_brief(project_slug: str, project_type: str, clean_project: str) -> dict:
    brief = PROJECT_FAMILY_BRIEFS.get(project_slug, {})
    heading = brief.get("heading") or f"{clean_project} Planning"
    fallback_intro = vary_paragraph(
        [
            "The broad project route may already be clear, but the local detail still needs tightening.",
            "The project may be obvious, but the local tripwires and next check often are not.",
            "This page is there to turn a broad project idea into the local answer that matters.",
        ],
        seed_key="project-brief",
        sentence_count=1,
        conditional_inserts=PROJECT_TYPE_VARIATION_INSERTS,
        project_type=project_type,
        town_name=clean_project,
    )
    fallback_local_change = (
        "Local restrictions, boundary conditions, design detail and a proposal that sits close to a limit are still the checks most likely to change the answer."
    )
    fallback_next_check = "Measure the proposal against the controlling limits, then verify the local restrictions before relying on the baseline answer."
    return {
        "heading": heading,
        "intro": brief.get("intro", fallback_intro),
        "local_change": brief.get("local_change", fallback_local_change),
        "next_check": brief.get("next_check", fallback_next_check),
    }


def _project_type_for_page(project_slug: str, project_title: str = "") -> str:
    focus = _project_focus_key(project_slug, project_title)
    if focus == "frontage":
        return "external"
    if focus == "use":
        return "change-of-use"
    if focus == "outbuilding":
        return "outbuilding"
    if focus == "loft":
        return "loft"
    if focus == "microgeneration":
        return "microgeneration"
    return _project_type_from_slug(project_slug) or _project_type_from_title(project_title)


def _project_route_answer(project_slug: str, project_title: str, town_name: str, rule) -> str:
    permitted = first_text((rule or {}).get("permitted_development", ""))
    if permitted and not any(marker in permitted.lower() for marker in GENERIC_ROUTE_MARKERS):
        return permitted

    focus = _project_focus_key(project_slug, project_title)
    project_label = project_title.lower()

    if focus == "use":
        return (
            f"For {project_label} in {town_name}, the route usually depends on use class, local policy, Article 4 and neighbour impact, not just the building work."
        )
    if focus == "frontage":
        return (
            f"For {project_label} in {town_name}, the key checks are usually frontage layout, drainage, visibility and any linked highway approval."
        )
    if focus == "outbuilding":
        return (
            f"For {project_label} in {town_name}, the main question is whether the structure still reads as secondary to the house once height, siting, use and local restrictions are checked."
        )
    if focus == "loft":
        return (
            f"For {project_label} in {town_name}, roof form, dormer bulk, visibility and local controls usually decide whether the simpler route still works."
        )
    return (
        f"For {project_label} in {town_name}, scale, siting, previous additions and local restrictions usually decide whether this stays straightforward."
    )


def _permission_trigger_bullets(project_slug: str, project_title: str, town_name: str, rule) -> list[str]:
    focus = _project_focus_key(project_slug, project_title)
    restrictions = useful_local_restrictions(rule)
    local_control = (
        f"the site is affected by {_join_labels([label for label, _ in restrictions[:2]])}"
        if restrictions
        else "the site is affected by conservation area, listed building, Article 4 or planning-history constraints"
    )
    if focus == "frontage":
        return [
            "the work changes vehicle access, visibility, drainage or the public highway edge",
            "a new dropped kerb, crossover, retaining work or engineered frontage is part of the project",
            local_control,
        ]
    if focus == "use":
        return [
            "the proposal changes how the property is used, occupied or managed day to day",
            "Article 4, HMO concentration, parking or amenity pressure could affect the route",
            local_control,
        ]
    if focus == "outbuilding":
        return [
            "the building is close to a height, boundary or coverage limit",
            "the use starts to look residential, self-contained or more intensive than incidental use",
            local_control,
        ]
    if focus == "loft":
        return [
            "the roof change is visible, bulky or changes the main roof form",
            "the scheme depends on dormer volume, ridge height or a front-facing alteration being acceptable",
            local_control,
        ]
    return [
        "the scale, height, depth or neighbour relationship is close to a planning threshold",
        "previous additions may already have used up the simpler route",
        local_control,
    ]


def _usually_pd_bullets(project_slug: str, project_title: str, town_name: str, rule) -> list[str]:
    focus = _project_focus_key(project_slug, project_title)
    if focus == "frontage":
        return [
            "the work is minor, drains properly and does not alter the vehicle access route",
            "the frontage layout remains safe, visible and clearly domestic",
        ]
    if focus == "use":
        return [
            "the existing and proposed use remain in a clearly lawful route",
            "the property is not affected by Article 4 or local policy controls for the proposed use",
        ]
    if focus == "outbuilding":
        return [
            "the structure stays clearly secondary to the house and comfortably within height and siting limits",
            "the use remains incidental and does not look like separate living accommodation",
        ]
    if focus == "loft":
        return [
            "the roof alteration stays subordinate, within volume limits and away from sensitive elevations",
            "the property history and local controls do not remove the simpler fallback",
        ]
    return [
        "the design is comfortably inside the normal size, height, depth and siting limits",
        "no local restriction, planning history or sensitive designation changes the baseline answer",
    ]


def _first_sentence(text: str) -> str:
    clean = " ".join(str(text or "").split()).strip()
    if not clean:
        return ""
    parts = re.split(r"(?<=[.!?])\s+", clean, maxsplit=1)
    return parts[0].strip()


def _project_hero_intro(project_slug: str, project_title: str, town_name: str, rule) -> str:
    curated_intro = PROJECT_FAMILY_BRIEFS.get(project_slug, {}).get("intro", "").format(town=town_name).strip()
    base_intro = curated_intro or _project_route_answer(project_slug, project_title, town_name, rule)

    for signal in useful_local_rule_items(rule, limit_per_key=1):
        sentence = _first_sentence(signal)
        if sentence and sentence.lower() not in base_intro.lower():
            return f"{base_intro} {sentence}"

    restrictions = useful_local_restrictions(rule)
    if restrictions:
        sentence = _first_sentence(restrictions[0][1])
        if sentence and sentence.lower() not in base_intro.lower():
            return f"{base_intro} {sentence}"

    return base_intro


def build_local_project_hero(project_slug: str, clean_project: str, town_name: str, rule) -> str:
    project_type = _project_type_for_page(project_slug, clean_project)
    brief = _project_brief(project_slug, project_type, clean_project)
    restrictions = useful_local_restrictions(rule)
    direct_answer = _project_hero_intro(project_slug, clean_project, town_name, rule)
    route_context = rotate(PROJECT_ROUTE_CONTEXT_VARIANTS, project_slug, clean_project, town_name)[0]
    local_change = (
        f"In {town_name}, checks on {_join_labels([label for label, _ in restrictions[:2]])} can change the route quickly."
        if restrictions
        else brief["local_change"]
    )
    return f"""
<section class='hero'>
<span class='badge'>Local Project Guide</span>
<h1>{brief['heading']} In {town_name}</h1>
<p>{direct_answer} {route_context}</p>
<p>{local_change}</p>
<p>Start with the quick local answer below, then use the local rule and council links if the route still depends on one sensitive detail, one local restriction or one borderline measurement.</p>
</section>
"""


def build_local_answer_box(project_slug: str, project: str, town: str, rule) -> str:
    project_type = _project_type_for_page(project_slug, project)
    focus = _project_focus_key(project_slug, project)
    town_size = town_size_bucket((rule or {}).get("county_slug", ""), town)
    brief = _project_brief(project_slug, project_type, project)
    permitted = _project_route_answer(project_slug, project, town, rule)
    restrictions = useful_local_restrictions(rule)
    rule_snapshots = useful_local_rule_items(rule)

    local_changes = [
        f"{label} can change the answer in {town}."
        for label, _ in restrictions[:2]
    ]
    local_changes.extend(rule_snapshots[:2])
    local_changes = _dedupe_copy_items(rotate(local_changes, project, town, project_type, town_size))

    if focus == "frontage":
        next_checks = [
            brief["next_check"],
            "Separate planning permission from highway or vehicle-crossing consent before paying for drawings or works.",
            "Check frontage visibility, drainage, road classification and usable parking depth before relying on the planning headline alone.",
            f"Check whether conservation area controls, listed building controls or Article 4 directions apply in {town}.",
            "If the frontage is tight or engineered, prepare a measured frontage plan before treating the route as settled.",
        ]
    elif focus == "use":
        next_checks = [
            brief["next_check"],
            "Confirm the existing and proposed use class before relying on a broad planning summary.",
            "Check whether Article 4, local policy, parking pressure or neighbour impact is doing more work than the building changes alone.",
            f"Check whether conservation area controls, listed building controls or Article 4 directions apply in {town}.",
            "If the route only works because the simpler fallback is assumed, verify the exact property position before moving on.",
        ]
    else:
        next_checks = [
            "Measure the proposal against the main size, height, roof and boundary limits.",
            f"Check whether conservation area controls, listed building controls or Article 4 directions apply in {town}.",
            "If the design is close to a threshold, prepare drawings and consider formal written confirmation before work starts.",
        ]
        if project_type == "extension":
            next_checks.append("Sense-check whether previous additions to the original house have already used up the simpler route.")
        elif project_type == "loft":
            next_checks.append("Check roof form, ridge and visibility early because loft changes often stop being straightforward there first.")
        elif project_type == "outbuilding":
            next_checks.extend(
                [
                    "If the structure needs to stay ancillary, make sure the layout and servicing do not start to read like separate living accommodation.",
                ]
            )
    next_checks.insert(0, brief["next_check"])
    next_checks = _dedupe_copy_items(rotate(next_checks, "next-checks", project, town, project_type))
    caveat_intro = {
        "frontage": f"Start here if the real question is whether the proposal in {town} is mainly a planning route, a highway route or a mix of both.",
        "use": f"Start here if the real question is whether the proposal in {town} turns on use class, Article 4 or local policy rather than on the building work itself.",
        "outbuilding": "Start here if the real question is whether the structure still reads as clearly secondary to the house once the local details are checked.",
        "loft": f"Start here if the real question is whether roof form, visible change or local controls make the simpler route less reliable in {town}.",
    }.get(
        focus,
        vary_paragraph(
            [
                f"This section gives the short answer first, then the local checks most likely to change it in {town}.",
                f"Use this as the quick route call before you open deeper pages.",
                f"Start here when the planning question is broad but the next decision needs to be practical.",
                f"This section narrows the question to the one or two local checks most likely to matter next.",
                f"It shows the baseline answer first, then the local detail that can shift it.",
            ],
            seed_key="local-answer-box",
            sentence_count=1,
            conditional_inserts={**TOWN_SIZE_INSERTS, **PROJECT_TYPE_VARIATION_INSERTS},
            project_type=project_type,
            town_size=town_size,
            town_name=town,
        ),
    )

    cards = [
        """
<div class="answer-card">
<h3>Likely route</h3>
<p>{permitted}</p>
</div>
""".format(permitted=permitted)
    ]

    if local_changes:
        cards.append(
            f"""
<div class="answer-card">
<h3>What often changes it locally</h3>
<ul class="checklist">{''.join(f"<li>{item}</li>" for item in local_changes[:3])}</ul>
</div>
"""
        )

    permission_bullets = _permission_trigger_bullets(project_slug, project, town, rule)
    pd_bullets = _usually_pd_bullets(project_slug, project, town, rule)
    cards.extend(
        [
            f"""
<div class="answer-card">
<h3>You may need planning permission if</h3>
<ul class="checklist">{''.join(f"<li>{item}</li>" for item in permission_bullets[:3])}</ul>
</div>
""",
            f"""
<div class="answer-card">
<h3>Usually simpler if</h3>
<ul class="checklist">{''.join(f"<li>{item}</li>" for item in pd_bullets[:2])}</ul>
<p><a href="/tools/planning-decision-tool/">Check if your project is likely to need permission</a></p>
</div>
""",
        ]
    )

    cards.append(
        f"""
<div class="answer-card">
<h3>Best next checks</h3>
<ul class="checklist">{''.join(f"<li>{item}</li>" for item in next_checks)}</ul>
</div>
"""
    )

    return f"""
<section class="local-answer-box" id="quick-answer">
<span class="eyebrow">Quick local answer</span>
<h2>The Likely Route, The Local Tripwires And The Safest Next Checks</h2>
<p class="section-lead">{caveat_intro}</p>
<div class="answer-grid">
{''.join(cards)}
</div>
</section>
"""


def build_popular_area_questions(project_slug: str, county_slug: str, town_slug: str, town_name: str) -> str:
    project = PROJECTS_BY_SLUG.get(project_slug, {})
    project_name = project.get("short_name", project.get("title", "This project"))
    priority = hmo_article_4_priority_for(county_slug, town_slug) if project_slug == "hmos" else {}
    recovery_links = [
        (
            recovery_path(route),
            f"Check the focused route for {' and '.join(slug.replace('-', ' ') for slug in route['scenario_slugs'])}",
            "Focused route",
        )
        for route in gsc_recovery_routes_for_project(project_slug, county_slug, town_slug)
    ]
    candidates = [
        *recovery_links,
        *(
            [
                (
                    f"/local-search/{priority['local_search_slug']}/",
                    f"Start with the exact HMO Article 4 search route for {town_name}",
                    "Search demand",
                ),
                (
                    f"/hmos/{county_slug}/{town_slug}/article-4/",
                    f"Check whether Article 4 changes the HMO route in {town_name}",
                    "Article 4 route",
                ),
                (
                    f"/hmos/{county_slug}/{town_slug}/planning-permission/",
                    f"Check HMO planning permission in {town_name}",
                    "HMO route",
                ),
            ]
            if priority
            else []
        ),
        (
            f"/councils/{town_slug}/",
            f"What does the local authority context change in {town_name}?",
            "Council context",
        ),
        (
            f"/planning-permission/{town_slug}/",
            f"Does this need planning permission in {town_name}?",
            "Local topic",
        ),
        (
            f"/permitted-development/{town_slug}/",
            f"Can permitted development still apply in {town_name}?",
            "Local topic",
        ),
        (
            f"/conservation-areas/{town_slug}/",
            f"Do conservation area rules affect this site?",
            "Local topic",
        ),
        (
            f"/article-4/{town_slug}/",
            f"Could Article 4 remove the simpler route?",
            "Local topic",
        ),
        (
            f"/{project_slug}/{county_slug}/",
            f"How does {project_name.lower()} compare across the wider area?",
            "Area comparison",
        ),
        (
            "/tools/site-constraint-checker/",
            "Check local constraints before you apply",
            "Tool",
        ),
        (
            "/tools/project-requirements-generator/",
            "Generate a planning requirements checklist",
            "Tool",
        ),
    ]

    links = []
    for href, label, kicker in candidates:
        clean_href = normalize_internal_href(href)
        if not is_live_internal_href(clean_href):
            continue
        links.append(
            f"""
<a class="card" href="{clean_href}">
<div class="card-kicker">{kicker}</div>
<h3>{label}</h3>
<span class="cta">Open check</span>
</a>
"""
        )
        if len(links) >= 6:
            break

    if not links:
        return ""

    return f"""
<section class="area-question-links" id="popular-local-questions">
<span class="eyebrow">Popular planning questions in this area</span>
<h2>Useful Checks Near {town_name}</h2>
<div class="grid-tight">{''.join(links)}</div>
</section>
"""


def build_project_jump_links(project_title: str, town_name: str) -> str:
    clean_title = project_title.replace("Planning Permission", "").strip().lower()
    return f"""
<section class="page-jump-links">
<span class="eyebrow">Jump to what matters</span>
<h2>Read This Page In The Order That Saves You Time</h2>
<div class="link-grid">
<a href="#quick-answer">Start with the quick answer for {clean_title} in {town_name}</a>
<a href="#decision-guide">See when the route usually stays simple and when it does not</a>
<a href="#process">Use the practical next-step sequence before paying for drawings</a>
<a href="#popular-local-questions">Check related local questions and tools</a>
<a href="#faq">Check the common questions people ask before they commit</a>
<a href="#next-steps">Open the best tool, guide or follow-up page next</a>
<a href="#trust">Use the trust notes if the project feels close to a limit</a>
</div>
</section>
"""


def build_project_decision_guide(project_slug: str, project_title: str, town_name: str, rule) -> str:
    project_type = _project_type_for_page(project_slug, project_title)
    focus = _project_focus_key(project_slug, project_title)
    clean_title = project_title.replace("Planning Permission", "").strip()
    restrictions = restriction_messages(rule)

    simpler_when = {
        "extension": [
            "The scale still looks comfortably within the normal householder limits for depth, height and neighbour impact.",
            "Previous additions have not already used up the easier route for the original house.",
            "The site is not being complicated by heritage controls or a visibly sensitive design position.",
        ],
        "loft": [
            "The roof change stays subordinate and does not rely on a more aggressive visible alteration.",
            "The proposal is not already pushing the roof form, ridge relationship or local sensitivity.",
            "The property is not listed and does not sit in a more sensitive heritage setting.",
        ],
        "outbuilding": [
            "The building still reads as clearly secondary to the house rather than a separate living space.",
            "Height, boundary siting and intended use all stay comfortably within the simpler route.",
            "The proposal is not drifting toward self-contained or visibly dominant use.",
        ],
        "microgeneration": [
            "The equipment sits discreetly and neighbour amenity concerns, especially noise or visibility, are manageable.",
            "The proposal does not rely on a prominent position that will be harder to defend locally.",
            "Local heritage controls are not doing most of the work in the answer.",
        ],
        "change-of-use": [
            "The proposed use still looks compatible with the surrounding street and local policy.",
            "Concentration pressure, neighbour effect and local restrictions are not obviously pointing the other way.",
            "The route does not depend on an optimistic assumption about how the authority will read the use.",
        ],
        "external": [
            "The work stays visually routine from the street and does not create a highway, drainage or visibility problem.",
            "The dimensions stay comfortably within the normal thresholds for this type of change.",
            "The site is not in a more sensitive location where frontage design matters more than expected.",
        ],
    }.get(
        project_type,
        [
            "The proposal stays comfortably inside the usual size, siting and design limits.",
            "Local restrictions do not appear to be doing most of the work in the answer.",
            "The project is not already close to a threshold that makes formal confirmation worth paying for.",
        ],
    )

    pause_and_check = {
        "extension": [
            "Depth, height or neighbour relationship already feels close to the edge of the simpler route.",
            "The property has previous additions, awkward site history or an original-house question that changes the baseline.",
            "Conservation area, listed building or Article 4 controls may matter locally.",
        ],
        "loft": [
            "The roof change is visible, bulky or starts to alter the original roof form too aggressively.",
            "The proposal is already relying on optimistic assumptions about ridge, eaves or dormer scale.",
            "Heritage controls or local design sensitivity are likely to tighten the answer.",
        ],
        "outbuilding": [
            "The use starts to look residential, self-contained or more intensive than a clearly incidental outbuilding.",
            "Height, boundary position or massing is already close to the practical limit.",
            "Local restrictions make a routine-looking structure less routine in this authority.",
        ],
        "microgeneration": [
            "Noise, neighbour amenity or frontage siting is likely to become the real issue.",
            "The equipment is prominent, oversized or in a sensitive local setting.",
            "The route depends on local restrictions not applying when that still needs checking.",
        ],
        "change-of-use": [
            "The use class point is not clean, or neighbour impact is likely to attract resistance.",
            "Local concentration pressure or policy wording may already be pointing to a stricter route.",
            "Article 4, heritage or authority-specific controls may remove the simpler fallback.",
        ],
        "external": [
            "Highway position, drainage, boundary conditions or visibility from the street is doing more work than the project looks at first glance.",
            "The design is close to a hard limit for size, siting or permeability.",
            "Local heritage or design controls may make a routine alteration harder to defend.",
        ],
    }.get(
        project_type,
        [
            "The proposal is close to a limit for size, siting or visual impact.",
            "The local restrictions may matter more than the national baseline suggests.",
            "You would be relying on guesswork rather than drawings and a measured check.",
        ],
    )

    if restrictions:
        labels = _join_labels([label for label, _ in restrictions[:2]])
        pause_and_check.insert(0, f"In {town_name}, {labels} can change the answer quickly.")

    if focus == "frontage":
        evidence = [
            f"A measured frontage or site plan showing the exact part of the {clean_title.lower()} that affects access, visibility or drainage.",
            "Photos showing the road, kerb line, frontage visibility and any street furniture, trees or parking controls that may matter.",
            "A short note on whether the route depends on highway approval, planning permission or both before any spend is committed.",
        ]
    elif focus == "use":
        evidence = [
            f"A short note showing the existing and proposed use for the {clean_title.lower()} and why that route is being relied on.",
            "A site or layout plan that shows parking, servicing, amenity relationships and the part of the property most likely to matter locally.",
            "The live Article 4, policy or planning-history note that could remove the simpler fallback route.",
        ]
    elif project_type == "outbuilding":
        evidence = [
            f"Measured drawings showing the height, boundary siting and intended layout of the {clean_title.lower()}.",
            "A simple note on how the structure will be used and why it still reads as clearly secondary to the house.",
            "Photos showing the garden, boundaries and the part of the site most likely to matter locally.",
        ]
    elif project_type == "loft":
        evidence = [
            f"Measured roof drawings showing the exact part of the {clean_title.lower()} most likely to trigger the threshold.",
            "Photos of the roof form, street-facing elevation and the visibility issues most likely to matter locally.",
            "A short note on previous roof changes, local restrictions or planning history that may already change the baseline answer.",
        ]
    else:
        evidence = [
            f"Measured drawings showing the part of the {clean_title.lower()} most likely to trigger a planning threshold.",
            "A simple note on previous additions, site history or restrictions that may already change the baseline answer.",
            "Photos showing boundaries, roof form, frontage visibility or the part of the site most likely to matter locally.",
        ]

    return f"""
<section class="decision-guide" id="decision-guide">
<span class="eyebrow">Decision guide</span>
<h2>When The Answer Usually Stays Simpler And When It Needs A Closer Check</h2>
<div class="answer-grid">
<div class="answer-card">
<h3>Often stays simpler when</h3>
<ul class="checklist">{''.join(f"<li>{item}</li>" for item in simpler_when[:3])}</ul>
</div>
<div class="answer-card">
<h3>Pause and check when</h3>
<ul class="checklist">{''.join(f"<li>{item}</li>" for item in pause_and_check[:3])}</ul>
</div>
<div class="answer-card">
<h3>Evidence that usually settles it faster</h3>
<ul class="checklist">{''.join(f"<li>{item}</li>" for item in evidence)}</ul>
</div>
</div>
</section>
"""


def generate_faq(project_slug: str, project: str, town: str, rule) -> str:
    permitted = _project_route_answer(project_slug, project, town, rule)
    height = first_text(
        (rule or {}).get("rules", {}).get("height_rules", ""),
        "Height limits are one of the key checks for most domestic projects.",
    )
    boundary = first_text(
        (rule or {}).get("rules", {}).get("boundary_rules", ""),
        "Boundary position can affect both height and the overall planning route.",
    )
    restrictions = restriction_messages(rule)
    local_controls = (
        f"Yes. In {town}, {_join_labels([label for label, _ in restrictions[:2]])} can change the route even where the national baseline looks familiar."
        if restrictions
        else f"Possibly. No standout restriction is surfaced here, but local constraints and borderline dimensions should still be checked in {town}."
    )
    focus = _project_focus_key(project_slug, project)

    if focus == "use":
        pressure_answer = (
            "Change of use, Article 4, parking pressure, amenity impact and local policy wording are the things most likely to push the route toward a formal application."
        )
        verify_answer = "Check the exact property position and the local policy context before paying for drawings or relying on a simpler fallback route."
        next_answer = "Open the local planning-permission page if policy is the blocker, or the planning route planner if the approval path still feels mixed."
    elif focus == "frontage":
        pressure_answer = (
            "Frontage visibility, drainage, highway approval and how the access works on the street are the things most likely to make the answer less straightforward."
        )
        verify_answer = "Check the frontage layout, visibility and any linked highway approval before paying for drawings or construction work."
        next_answer = "Open the local planning-permission page if the route is still unclear, or the site-constraint checker if one blocker is doing most of the work."
    elif focus == "outbuilding":
        pressure_answer = (
            "Height, boundary siting, previous additions and whether the building still reads as clearly secondary to the house are usually the checks that change the route fastest."
        )
        verify_answer = "Check the measurements and intended use formally before paying for drawings if the structure is close to a limit or no longer feels clearly incidental."
        next_answer = "Open the boundary or maximum-height rule page if one measurement is the blocker, or the local council page if restrictions are the bigger issue."
    elif focus == "loft":
        pressure_answer = (
            "Roof form, dormer bulk, front-facing changes, previous roof alterations and local heritage sensitivity are the things most likely to push the route out of the simpler answer."
        )
        verify_answer = "Check the roof changes formally before paying for drawings if the scheme depends on a borderline dormer, roof enlargement or visible alteration."
        next_answer = "Open the local permitted-development or height page if roof thresholds are the blocker, or the planning decision tool if the route is still unresolved."
    else:
        pressure_parts = _dedupe_copy_items([height, boundary], drop_generic=True)
        pressure_answer = (
            "Height, boundary position, previous additions and local restrictions are usually the first checks that change the answer."
            if not pressure_parts
            else " ".join(pressure_parts[:2])
        )
        verify_answer = "If the project is close to a planning threshold, get measured drawings together and consider written confirmation before work starts."
        next_answer = "Open the local council page if restrictions may change the answer, or the planning decision tool if the overall route still feels unclear."

    faq_items = [
        (
            f"Do I usually need planning permission for {project} in {town}?",
            permitted,
        ),
        (
            f"What most often pushes {project.lower()} out of the simpler route?",
            pressure_answer,
        ),
        (
            "Do conservation areas, listed buildings or Article 4 change the answer here?",
            local_controls,
        ),
        (
            "When is it worth checking formally before paying for drawings?",
            verify_answer,
        ),
        (
            "What should I open next if I still have doubts?",
            next_answer,
        ),
    ]
    return build_faq_section(
        faq_items,
        section_id="faq",
        eyebrow="Project-specific FAQ",
        title="Questions People Usually Ask Before They Commit",
        intro=f"Keep this block for the project-specific objections and follow-up checks that usually matter once the broad route is understood for {project.lower()} in {town}.",
    )


def build_planning_process_block(project_title: str, town_name: str = "", rule=None, project_slug: str = "") -> str:
    clean_title = project_title.replace("Planning Permission", "").strip()
    project_type = _project_type_for_page(project_slug, project_title)
    focus = _project_focus_key(project_slug, project_title)
    intro = vary_paragraph(
        [
            f"Use this sequence while {clean_title.lower()} is still easy to adjust.",
            f"This order works best when the route still feels uncertain and the next step needs to be practical rather than theoretical.",
            f"The point here is to get from first idea to the one check that really matters.",
            f"Treat this like a filter: each step should either keep the simpler route alive or show you exactly why it is weakening.",
            f"This checklist is there to stop the project drifting into drawings or applications before the live planning issue is clear.",
        ],
        seed_key="planning-process",
        sentence_count=1,
        conditional_inserts=PROJECT_TYPE_VARIATION_INSERTS,
        project_type=project_type,
        town_name=town_name,
    )
    if focus == "frontage":
        steps = [
            f"Use the quick local answer above to separate the planning route from the highway or access route for {clean_title.lower()}.",
            "Check frontage visibility, drainage, road classification and whether a vehicle crossover or highway consent is the controlling issue.",
            "Measure the usable frontage and keep street trees, parking controls and public-realm constraints in view before paying for works.",
            "If the route is still mixed, prepare a measured frontage plan and verify formally before work starts.",
        ]
    elif focus == "use":
        steps = [
            f"Use the quick local answer above to check whether {clean_title.lower()} is really a use-class or policy problem first.",
            "Confirm the existing and proposed use, then check Article 4, local policy, parking pressure and neighbour impact together.",
            "Treat the route as unresolved until the local policy layer and any property-specific controls line up cleanly.",
            "If the scheme is borderline, prepare the core layout and use details before relying on the simpler route.",
        ]
    else:
        steps = [
            f"Use the quick local answer above to sense-check whether {clean_title.lower()} may fit within the normal route.",
            "Measure the parts of the proposal most likely to hit a planning threshold.",
            "Check local restrictions and site history before assuming the broad national answer still applies cleanly.",
            "If the project is borderline, prepare measured drawings and verify formally before work starts.",
        ]
        if project_type == "extension":
            steps.append("Compare the scale against the original house rather than judging it only by the new drawings in isolation.")
        elif project_type == "loft":
            steps.append("Check roof changes and visibility before assuming the route is governed by floor area alone.")
        elif project_type == "outbuilding":
            steps.append("Check height, boundary position and whether the building still looks secondary to the main house.")
        elif project_type == "microgeneration":
            steps.append("Check whether visual siting and local sensitivity matter more than the equipment spec itself.")
    steps = rotate(steps, "planning-process-steps", project_title, town_name, project_type)
    return f"""
<section class="planning-process" id="process">
<span class="eyebrow">How to use this page well</span>
<h2>Before You Spend On Drawings Or An Application</h2>
<p class="section-lead">{intro}</p>
<ol>
{''.join(f"<li>{step}</li>" for step in steps[:4])}
</ol>
</section>
"""


def build_local_jurisdiction_notice(rule, town_name: str) -> str:
    county_slug = (rule or {}).get("county_slug", "")
    return build_jurisdiction_notice(county_slug, town_name, "local project guide")


def build_documents_checklist(project_title: str, project_slug: str = "") -> str:
    clean_title = project_title.replace("Planning Permission", "").strip()
    focus = _project_focus_key(project_slug, project_title)
    if focus == "frontage":
        items = [
            f"A simple site plan showing the frontage, kerb line and the position of the proposed {clean_title.lower()}.",
            "Measured frontage widths, visibility notes and any drainage or level details that may affect the route.",
            "Photos of the frontage, road layout, street furniture and anything that may affect highway approval.",
            "Any council or highway notes that already explain crossover, access or frontage standards for the site.",
        ]
    elif focus == "use":
        items = [
            f"A short note explaining the existing and proposed use for the {clean_title.lower()}.",
            "A basic layout or site plan showing the space, access, parking and servicing arrangement.",
            "Notes on local policy, Article 4, planning history or neighbour issues that may already change the route.",
            "Photos or simple plans that show the surrounding context the authority is most likely to weigh.",
        ]
    else:
        items = [
            f"A simple site plan showing boundaries and the position of the proposed {clean_title.lower()}.",
            "Measured heights, distances to boundaries and any roof details that affect the planning route.",
            "Photos of the existing house and the immediate surrounding context.",
            "Notes on previous extensions, outbuildings or permissions that may already use up allowances.",
        ]
    return f"""
<section class="documents-checklist">
<span class="eyebrow">Useful prep work</span>
<h2>Documents Worth Pulling Together Early</h2>
<ul class="checklist">
{''.join(f"<li>{item}</li>" for item in items)}
</ul>
</section>
"""


def build_trust_section(project_title: str, town_name: str, county_name: str) -> str:
    methodology = PROMOTED_LINKS["methodology"]
    faq = PROMOTED_LINKS["faq"]
    system_label = planning_system_label(county_name)
    return build_trust_framework(
        section_id="trust",
        eyebrow="Trust and caveats",
        title="How To Use This Local Guide Responsibly",
        purpose=f"This page starts with the {system_label} baseline, then adds the local checks most likely to matter in {town_name}.",
        not_replace="It does not replace the council record, a lawful development certificate, pre-application advice or professional input where the route is tight, sensitive or financially important.",
        built_from="The guide starts with the national route, then adds local restriction signals, planning-history cautions and the project details most likely to change the answer in practice.",
        verify_when="Stop relying on the broad answer once the project is close to a limit, depends on heritage or Article 4 assumptions, or would be expensive to revisit after drawings or works begin.",
        safest_next_step="Use a lawful development certificate when the scheme appears lawful but certainty matters. Use pre-application advice when local judgement, design sensitivity or policy pressure is doing too much work to leave on assumption.",
        support_links=[
            (methodology["title"], methodology["href"]),
            (faq["title"], faq["href"]),
        ],
    )


def build_scenario_grid(project_slug: str, county_slug: str, town_slug: str, scenarios) -> str:
    cards = []
    relevant_scenarios = filter_relevant_scenarios(project_slug, scenarios)
    descriptions = {
        "planning-permission": "Use this local topic page to see whether the scheme still avoids a formal application in this council area.",
        "permitted-development": "Check whether the national PD baseline still holds locally once council-level restrictions and site history are considered.",
        "height-limits": "Useful when the proposal feels close to the vertical limit and the local context may tighten the answer.",
        "depth-limits": "Useful when the real question is how far the project can project or spread before permission is needed.",
        "boundary-rules": "Use this if boundary position is the likely tripwire and local context may change how cautious you need to be.",
        "conservation-areas": "Important if heritage controls may tighten the route for this council area.",
        "article-4": "Important where local directions may remove PD rights.",
    }

    for scenario in relevant_scenarios:
        url = f"/{scenario['slug']}/{town_slug}/"
        cards.append(
            f"""
<a class="card" href="{url}">
<div class="card-kicker">Rule guide</div>
<h3>{scenario['title']}</h3>
<p>{descriptions.get(scenario['slug'], 'See how this rule affects the project locally and what to check next.')}</p>
<span class="cta">Open local rule page</span>
</a>
"""
        )

    return f"""
<section class="scenario-grid">
<span class="eyebrow">Rules that usually decide the answer</span>
<h2>Open The Specific Planning Issue That Could Change The Route</h2>
<div class="grid">{''.join(cards)}</div>
</section>
"""


def build_local_topic_handoffs(project_slug: str, town_slug: str) -> str:
    project_name = project_slug.replace("-", " ").title()
    focus = _project_focus_key(project_slug, project_name)
    county_slug = ""
    for project_county_slug, councils in COUNCILS_BY_COUNTY.items():
        for council in councils:
            if council.get("town_slug") == town_slug:
                county_slug = project_county_slug
                break
        if county_slug:
            break

    def scenario_href(scenario_slug: str, fallback: str) -> str:
        return project_scenario_href(project_slug, county_slug, town_slug, scenario_slug) or fallback

    if focus == "use":
        primary_href = scenario_href("planning-permission", f"/planning-permission/{town_slug}/")
        primary_title = "Planning permission for this project locally"
        primary_description = "Best when local policy, Article 4 and the overall route matter more than one narrow project detail."
        secondary_href = scenario_href("permitted-development", f"/permitted-development/{town_slug}/")
        secondary_title = "Permitted development for this project locally"
        secondary_description = "Useful when the live question is whether the simpler fallback survives once local controls are checked properly."
        faq_href = "/planning-faq/planning-permission-vs-permitted-development/"
        faq_title = "Read the permission-vs-PD answer"
    elif focus == "loft":
        primary_href = scenario_href("permitted-development", f"/permitted-development/{town_slug}/")
        primary_title = "Permitted development for this project locally"
        primary_description = "Best when the live question is whether the simpler route still survives once local controls and roof changes are checked."
        secondary_href = scenario_href("height-limits", f"/height-limits/{town_slug}/")
        secondary_title = "Height limits for this project locally"
        secondary_description = "Useful when ridge, dormer bulk, roof form or a borderline height assumption is driving the risk."
        faq_href = "/planning-faq/lawful-development-certificate/"
        faq_title = "Read the lawful development certificate answer"
    else:
        primary_href = scenario_href("planning-permission", f"/planning-permission/{town_slug}/")
        primary_title = "Planning permission for this project locally"
        primary_description = "Best when the main uncertainty is whether the project still avoids a formal application."
        secondary_slug = "height-limits" if project_slug == "fences-and-walls" else "boundary-rules"
        secondary_href = scenario_href(secondary_slug, f"/{secondary_slug}/{town_slug}/")
        secondary_title = "Height limits for this project locally" if secondary_slug == "height-limits" else "Boundary rules for this project locally"
        secondary_description = (
            "Useful when the controlling height point is doing most of the work."
            if secondary_slug == "height-limits"
            else "Useful when siting, neighbour relationship or edge-of-plot conditions are driving the risk."
        )
        faq_href = "/planning-faq/do-i-need-planning-permission/"
        faq_title = "Read the route-level answer"
    return f"""
<section class="local-topic-handoffs">
<span class="eyebrow">Rule-first next steps</span>
<h2>If The Local Rule Is The Real Blocker, Start Here</h2>
<div class="grid">
<a class="card" href="{primary_href}">
<div class="card-kicker">Local topic page</div>
<h3>{primary_title}</h3>
<p>{primary_description}</p>
<span class="cta">Open local topic page</span>
</a>
<a class="card" href="{secondary_href}">
<div class="card-kicker">Local topic page</div>
<h3>{secondary_title}</h3>
<p>{secondary_description}</p>
<span class="cta">Open local topic page</span>
</a>
<a class="card" href="{faq_href}">
<div class="card-kicker">FAQ</div>
<h3>{faq_title}</h3>
<p>Read the broader route answer if the planning question is still bigger than {project_name.lower()} itself.</p>
<span class="cta">Read answer</span>
</a>
</div>
</section>
"""


def build_related_topic_links(project_slug: str, county_slug: str, town_slug: str) -> str:
    links = build_internal_links(project_slug, county_slug, town_slug)

    return f"""
<section class="related-topics" id="compare">
<span class="eyebrow">Recommended next pages</span>
<h2>Open The Next Check That Actually Narrows The Answer</h2>
<p class="section-lead">The high-priority next actions are already surfaced above. Open this section when you want deeper comparisons, related project types or broader hierarchy links without losing the main answer.</p>
<details class="support-disclosure">
<summary>Show more comparisons, related pages and next-step routes</summary>
{links}
</details>
</section>
"""


def build_nearby_council_links(project_slug, county_slug, town_slug, councils_by_county) -> str:
    links = build_nearby_links(project_slug, county_slug, town_slug, councils_by_county)

    return f"""
<section class="nearby-councils">
<span class="eyebrow">Compare the local layer</span>
<h2>Nearby Areas Worth Comparing</h2>
<p>Neighbouring councils can read the same broad planning position differently once designations, policy and site context start to matter.</p>
<div class="link-grid">{links}</div>
</section>
"""


def build_local_action_links(project_slug: str, county_slug: str, town_slug: str, town_name: str) -> str:
    focus = _project_focus_key(project_slug, project_slug.replace("-", " "))
    if focus == "use":
        primary = {
            "kicker": "Route planner",
            "href": PROMOTED_LINKS["planning_route_planner"]["href"],
            "title": "Map the permission route before you commit",
            "description": "Use the route planner when the live question is whether policy, Article 4 or a fuller application route is doing most of the work.",
            "cta": PROMOTED_LINKS["planning_route_planner"]["cta"],
        }
        second = {
            "kicker": "Local rule page",
            "href": f"/planning-permission/{town_slug}/",
            "title": f"Check the policy route in {town_name}",
            "description": "Open the local planning-permission page if local policy, Article 4 or the overall route needs a clearer local reading.",
            "cta": "Open local rule page",
        }
        third = {
            "kicker": "FAQ",
            "href": "/planning-faq/planning-permission-vs-permitted-development/",
            "title": "Read the planning permission vs permitted development answer",
            "description": "Use this when the real uncertainty is still the route distinction rather than one design detail.",
            "cta": "Read answer",
        }
        extra = PROMOTED_LINKS["site_constraint_checker"]
    elif focus == "frontage":
        primary = {
            "kicker": "Constraint tool",
            "href": PROMOTED_LINKS["site_constraint_checker"]["href"],
            "title": "Check the site and frontage constraints first",
            "description": "Use the constraint checker when access, drainage, visibility or a sensitive frontage may be doing more work than the headline planning answer.",
            "cta": PROMOTED_LINKS["site_constraint_checker"]["cta"],
        }
        second = {
            "kicker": "Local topic page",
            "href": f"/planning-permission/{town_slug}/",
            "title": f"Planning permission in {town_name}",
            "description": "Open the local route page when the planning answer and the wider access route need separating cleanly.",
            "cta": "Open local topic page",
        }
        third = {
            "kicker": "FAQ",
            "href": "/planning-faq/do-i-need-planning-permission/",
            "title": "Read the core permission answer",
            "description": "Use the FAQ when you still need the route-level answer before moving deeper into local detail.",
            "cta": "Read answer",
        }
        extra = PROMOTED_LINKS["planning_route_planner"]
    else:
        primary = {
            "kicker": "Tool",
            "href": PROMOTED_LINKS["planning_decision_tool"]["href"],
            "title": "Run the quick planning tool",
            "description": "Use the main decision tool when the overall route is still unclear and you need a faster first steer before reading more local pages.",
            "cta": PROMOTED_LINKS["planning_decision_tool"]["cta"],
        }
        second = {
            "kicker": "Local authority page",
            "href": f"/councils/{town_slug}/",
            "title": f"See the wider {town_name} planning context",
            "description": "Use the council page when local policy, conservation-area coverage, listed-building status or Article 4 matters more than this project type alone.",
            "cta": "View council guide",
        }
        third = {
            "kicker": "FAQ",
            "href": "/planning-faq/lawful-development-certificate/",
            "title": "Read when a lawful development certificate is worth it",
            "description": "Use this when the route looks plausible but the cost of being wrong makes written certainty worthwhile.",
            "cta": "Read answer",
        }
        extra = PROMOTED_LINKS["project_requirements_generator"] if focus in {"extension", "loft", "outbuilding"} else PROMOTED_LINKS["planning_rejection_risk_tool"]

    return f"""
<section class="local-actions" id="next-steps">
<span class="eyebrow">Strong next actions</span>
<h2>What To Open Next If This Local Guide Still Leaves Doubt</h2>
<div class="grid">
<a class="card" href="{primary['href']}">
<div class="card-kicker">{primary['kicker']}</div>
<h3>{primary['title']}</h3>
<p>{primary['description']}</p>
<span class="cta">{primary['cta']}</span>
</a>
<a class="card" href="{second['href']}">
<div class="card-kicker">{second['kicker']}</div>
<h3>{second['title']}</h3>
<p>{second['description']}</p>
<span class="cta">{second['cta']}</span>
</a>
<a class="card" href="/{project_slug}/{county_slug}/">
<div class="card-kicker">Area comparison</div>
<h3>Compare this project across the wider planning area</h3>
<p>Use the area project hub when a neighbouring-authority comparison is the quickest way to see whether this answer is unusually strict or fairly typical.</p>
<span class="cta">Compare this project</span>
</a>
<a class="card" href="{third['href']}">
<div class="card-kicker">{third['kicker']}</div>
<h3>{third['title']}</h3>
<p>{third['description']}</p>
<span class="cta">{third['cta']}</span>
</a>
<a class="card" href="{extra['href']}">
<div class="card-kicker">Useful follow-up</div>
<h3>{extra['title']}</h3>
<p>{extra['description']}</p>
<span class="cta">{extra['cta']}</span>
</a>
</div>
</section>
"""


def build_project_find_help_cta(project_slug: str) -> str:
    if not should_show_find_help_project_cta(project_slug):
        return ""
    return build_find_help_cta()


def build_project_route_check_cta(project_slug: str) -> str:
    if not should_show_route_check_project_cta(project_slug):
        return ""
    variant = "b" if project_slug in {"dropped-kerbs", "driveways", "hard-surfaces"} else "a"
    if project_slug in {"hmos", "change-of-use", "conservation-areas", "listed-buildings"}:
        variant = "c"
    return build_planning_route_check_cta(
        variant=variant,
        source_page_type="project-page",
        project_slug=project_slug,
        compact=True,
    )


def build_real_world_examples(project_title: str, town_name: str, rule=None, project_slug: str = "") -> str:
    clean_title = project_title.replace("Planning Permission", "").strip()
    project_type = _project_type_for_page(project_slug, project_title)
    focus = _project_focus_key(project_slug, project_title)
    restrictions = restriction_messages(rule)
    restriction_hint = (
        f"Local controls such as {_join_labels([label for label, _ in restrictions[:2]])} can make a routine-looking scheme more sensitive very quickly."
        if restrictions
        else "Where no standout local designation is surfaced, borderline dimensions and site history usually become the real deciding factors."
    )
    route_pattern = {
        "frontage": "Frontage-led projects move more smoothly when the drawings show visibility, drainage and the usable access arrangement on one plan.",
        "use": "Use-led projects move more smoothly when the existing use, proposed use and local policy angle all line up before design work gets too far.",
        "outbuilding": "Secondary buildings move more smoothly when the drawings prove the structure stays clearly subordinate to the house.",
        "loft": "Roof projects move more smoothly when the drawings prove the roof form and visibility story as clearly as the measurements.",
    }.get(
        focus,
        "Projects usually move more smoothly when the drawings clearly show scale, height, roof form and boundary position.",
    )
    escalation_pattern = {
        "frontage": f"{clean_title} proposals are more likely to need escalation when highway approval, frontage geometry or drainage is treated as an afterthought.",
        "use": f"{clean_title} proposals are more likely to need escalation when the route depends on a generous reading of use class, policy or Article 4 coverage.",
        "outbuilding": f"{clean_title} proposals are more likely to need escalation when use, servicing or boundary siting stop the structure reading as clearly secondary to the house.",
        "loft": f"{clean_title} proposals are more likely to need escalation when roof form, visibility or previous alterations are assumed away too early.",
    }.get(
        focus,
        f"{clean_title} proposals are more likely to need escalation when they rely on assumptions about previous extensions, awkward boundaries or local controls.",
    )
    patterns = rotate(
        [
            route_pattern,
            escalation_pattern,
            f"In {town_name}, written confirmation is often more valuable than guesswork when the design is close to a threshold.",
            PROJECT_TYPE_VARIATION_INSERTS.get(project_type, ""),
            restriction_hint,
        ],
        "project-examples",
        project_title,
        town_name,
        project_type,
    )
    return f"""
<section class="planning-examples">
<span class="eyebrow">Common tripwires</span>
<h2>What Usually Makes These Projects Easier Or Harder</h2>
<ul class="checklist">
{''.join(f'<li>{item}</li>' for item in patterns[:4])}
</ul>
</section>
"""


def build_project_conversion_hook(project_slug: str, town_slug: str, project_title: str, town_name: str) -> str:
    cta = _project_guidance_cta(project_slug, project_title, town_name)
    return build_personalised_guidance_cta(
        title=cta["title"],
        description=cta["description"],
        context_label="project-page",
        email_context=f"{project_title} in {town_name}",
        intro_label=cta["intro_label"],
        compact=True,
        prefill={
            "authority": town_name,
            "location": town_name,
            "project_stage": "Comparing options and measurements",
            "project_summary": f"{project_title} in {town_name}",
            "main_worry": cta["description"],
        },
    ) + render_result_capture(f"project-{project_slug}-{town_slug}-capture")


def assemble_core_page_components(components) -> str:
    return "\n".join(component for component in components if component)
