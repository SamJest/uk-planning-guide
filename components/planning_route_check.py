from __future__ import annotations

from html import escape

from components.faq_blocks import build_faq_section
from components.trust_framework import build_trust_framework
from utils.random_tools import get_month_year


ROUTE_CHECK_PATH = "/tools/planning-route-check/"
PLANNING_HELP_PATH = "/planning-help/"
PLANNING_HELP_THANK_YOU_PATH = "/planning-help/thank-you/"

ROUTE_CHECK_PROJECT_SLUGS = {
    "garden-rooms",
    "outbuildings",
    "garages",
    "garage-conversions",
    "house-extensions",
    "single-storey-extensions",
    "two-storey-extensions",
    "rear-extensions",
    "side-extensions",
    "wraparound-extensions",
    "loft-conversions",
    "dormer-extensions",
    "dropped-kerbs",
    "driveways",
    "hard-surfaces",
    "fences-and-walls",
    "solar-panels",
    "change-of-use",
    "hmos",
}

ROUTE_CHECK_SCENARIO_SLUGS = {
    "planning-permission",
    "permitted-development",
    "conservation-areas",
    "listed-buildings",
    "article-4",
}

CTA_VARIANTS = {
    "a": {
        "title": "Unsure What Rules Apply To Your Home?",
        "body": "Answer a few questions and get a simple planning route check for your project.",
        "button": "Start the free route check",
    },
    "b": {
        "title": "Planning Rules Can Change By Project, Property And Location.",
        "body": "Use the free route check to see your likely next step before you spend money on drawings or applications.",
        "button": "Check my planning route",
    },
    "c": {
        "title": "Need A Clearer Next Step?",
        "body": "Use the free route check to see whether your project may involve permitted development, planning permission, council approval or professional review.",
        "button": "Use the route check",
    },
}


def should_show_route_check_project_cta(project_slug: str) -> bool:
    return str(project_slug or "").strip().lower() in ROUTE_CHECK_PROJECT_SLUGS


def should_show_route_check_scenario_cta(scenario_slug: str) -> bool:
    return str(scenario_slug or "").strip().lower() in ROUTE_CHECK_SCENARIO_SLUGS


def build_planning_route_check_cta(
    *,
    variant: str = "a",
    source_page_type: str = "",
    project_slug: str = "",
    scenario_slug: str = "",
    compact: bool = True,
) -> str:
    copy = CTA_VARIANTS.get(str(variant or "").lower(), CTA_VARIANTS["a"])
    attrs = {
        "data-planning-route-cta": "true",
        "data-cta-variant": str(variant or "a").lower(),
        "data-source-page-type": source_page_type,
        "data-project-slug": project_slug,
        "data-scenario-slug": scenario_slug,
    }
    attr_html = " ".join(
        f'{name}="{escape(value, quote=True)}"'
        for name, value in attrs.items()
        if value
    )
    compact_class = " planning-route-cta-compact" if compact else ""
    return f"""
<section class="planning-route-cta{compact_class}" {attr_html}>
<span class="eyebrow">Free planning route check</span>
<h2>{copy['title']}</h2>
<p>{copy['body']}</p>
<div class="hero-ctas">
<a class="btn" href="{ROUTE_CHECK_PATH}" data-planning-route-cta-link="true">{copy['button']}</a>
<a class="btn button-secondary" href="{PLANNING_HELP_PATH}">See help options</a>
</div>
<p class="route-check-disclaimer">General guidance only. The result depends on property details, local restrictions and council interpretation.</p>
</section>
<script src="/assets/js/planning-route-check.js"></script>
"""


def _option(value: str, label: str) -> str:
    return f'<option value="{escape(value, quote=True)}">{escape(label)}</option>'


def _checkbox(name: str, value: str, label: str) -> str:
    safe_value = escape(value, quote=True)
    safe_label = escape(label)
    safe_id = f"route-{name}-{value}".replace("_", "-")
    return f"""
<label class="route-check-option">
<input type="checkbox" id="{safe_id}" name="{escape(name, quote=True)}" value="{safe_value}">
<span>{safe_label}</span>
</label>
"""


def render_planning_route_check_tool() -> str:
    project_options = [
        ("single-storey-extension", "Single-storey extension"),
        ("two-storey-extension", "Two-storey extension"),
        ("loft-conversion", "Loft conversion"),
        ("garage-conversion", "Garage conversion"),
        ("garden-room-outbuilding", "Garden room / outbuilding"),
        ("shed-greenhouse", "Shed / greenhouse"),
        ("fence-wall-gate", "Fence, wall or gate"),
        ("driveway-hardstanding", "Driveway / hardstanding"),
        ("dropped-kerb-vehicle-access", "Dropped kerb / vehicle access"),
        ("solar-panels", "Solar panels"),
        ("porch", "Porch"),
        ("hmo-change-of-use", "HMO / change of use"),
        ("other", "Other"),
    ]
    property_options = [
        ("detached-house", "Detached house"),
        ("semi-detached-house", "Semi-detached house"),
        ("terraced-house", "Terraced house"),
        ("bungalow", "Bungalow"),
        ("flat-maisonette", "Flat / maisonette"),
        ("listed-building", "Listed building"),
        ("commercial-mixed-use", "Commercial / mixed-use"),
        ("not-sure", "Not sure"),
    ]
    timeframe_options = [
        ("researching", "Just researching"),
        ("within-3-months", "Within 3 months"),
        ("3-6-months", "3-6 months"),
        ("6-12-months", "6-12 months"),
        ("already-started", "Already started"),
        ("urgent-problem", "Urgent/problem has come up"),
    ]
    help_options = [
        ("route-only", "Just show me the likely route"),
        ("professional-planning-design-help", "I may want professional planning/design help"),
        ("drawings-application-help", "I need drawings/application help"),
        ("refusal-enforcement-help", "I need help after a refusal/enforcement issue"),
        ("contractor-specialist", "I need a contractor/specialist"),
    ]
    restrictions = [
        ("conservation-area", "Conservation area"),
        ("listed-building", "Listed building"),
        ("article-4", "Article 4 direction"),
        ("protected-landscape", "National park / AONB / protected landscape"),
        ("previous-condition", "Previous planning condition"),
        ("leasehold-shared-freeholder", "Leasehold/shared/freeholder restriction"),
        ("not-sure", "Not sure"),
    ]

    return f"""
<div class="route-check-shell" data-tool-root="planning-route-check" data-tool-kind="route-check">
<form id="planning-route-check-form" class="route-check-form" novalidate>
<div class="route-check-progress" aria-label="Planning route check progress">
<span class="route-check-progress-step">1 Project</span>
<span class="route-check-progress-step">2 Property</span>
<span class="route-check-progress-step">3 Restrictions</span>
<span class="route-check-progress-step">4 Help</span>
</div>

<fieldset class="route-check-step">
<legend>1. What are you planning?</legend>
<div class="form-field">
<label for="route-project-type">Project type *</label>
<select id="route-project-type" name="project_type" required>
<option value="">Select a project</option>
{''.join(_option(value, label) for value, label in project_options)}
</select>
</div>
</fieldset>

<fieldset class="route-check-step">
<legend>2. What type of property is it?</legend>
<div class="form-field">
<label for="route-property-type">Property type *</label>
<select id="route-property-type" name="property_type" required>
<option value="">Select a property type</option>
{''.join(_option(value, label) for value, label in property_options)}
</select>
</div>
</fieldset>

<fieldset class="route-check-step">
<legend>3. Where is the property?</legend>
<div class="form-grid">
<div class="form-field">
<label for="route-location">Postcode or town *</label>
<input id="route-location" name="postcode_or_town" type="text" autocomplete="postal-code" required>
</div>
<div class="form-field">
<label for="route-council">Council/local authority <span class="field-help-inline">optional</span></label>
<input id="route-council" name="council" type="text" autocomplete="off">
</div>
</div>
</fieldset>

<fieldset class="route-check-step">
<legend>4. Are any restrictions likely?</legend>
<div class="route-check-options">
{''.join(_checkbox("restrictions", value, label) for value, label in restrictions)}
</div>
</fieldset>

<fieldset class="route-check-step">
<legend>5. How soon are you planning the work?</legend>
<div class="form-field">
<label for="route-timeframe">Timeframe *</label>
<select id="route-timeframe" name="timeframe" required>
<option value="">Select a timeframe</option>
{''.join(_option(value, label) for value, label in timeframe_options)}
</select>
</div>
</fieldset>

<fieldset class="route-check-step">
<legend>6. What do you want help with?</legend>
<div class="form-field">
<label for="route-desired-help">Preferred next step *</label>
<select id="route-desired-help" name="desired_help" required>
<option value="">Select an option</option>
{''.join(_option(value, label) for value, label in help_options)}
</select>
</div>
</fieldset>

<fieldset class="route-check-step">
<legend>7. Optional notes</legend>
<div class="form-field">
<label for="route-user-notes">Notes</label>
<textarea id="route-user-notes" name="user_notes" rows="5" placeholder="Add dimensions, property history, access issues or anything you are unsure about."></textarea>
</div>
</fieldset>

<div id="route-check-errors" class="route-check-errors" role="alert" aria-live="polite"></div>
<div class="hero-ctas">
<button class="btn" type="submit">Show my likely route</button>
<button class="btn button-secondary" type="reset">Clear answers</button>
</div>
</form>

<section id="planning-route-result" class="route-result-panel" aria-live="polite" hidden></section>
<section id="planning-route-help" class="route-help-panel" hidden></section>
</div>
<script src="/assets/js/lead-config.js"></script>
<script src="/assets/js/planning-route-check.js"></script>
"""


def build_planning_route_check_faq() -> str:
    return build_faq_section(
        [
            (
                "Is this a legal planning decision?",
                "No. It is a practical route check to help you understand the likely next step. Councils, lawful development certificates and formal advice are what settle site-specific questions.",
            ),
            (
                "Can permitted development still need checks?",
                "Yes. Even where permitted development may be possible, measurements, previous additions, Article 4 directions, conservation areas and building regulations can still matter.",
            ),
            (
                "What if my home is in a conservation area?",
                "Treat the result more cautiously. Conservation areas can restrict normal permitted development, especially visible changes, roof alterations, demolition and frontage works.",
            ),
            (
                "Do flats have permitted development rights?",
                "Flats and maisonettes usually have fewer householder permitted development rights than houses, so council or professional checks are often sensible before relying on a simple route.",
            ),
            (
                "Do I need a planning consultant?",
                "Not always. A consultant or architectural designer is more useful where the project is restricted, close to a limit, listed, locally sensitive, refused before, or likely to need drawings and a formal application.",
            ),
            (
                "What happens if I request help?",
                "UK Planning Guide may contact you about the enquiry and, only if you consent, may share it with a relevant planning, design or home-improvement professional if suitable help is available. A match is not guaranteed.",
            ),
        ],
        section_id="planning-route-check-faq",
        eyebrow="Planning route check FAQ",
        title="Questions People Usually Ask Before They Rely On A Route Check",
        intro="Use these answers to keep the result in proportion before you spend money on drawings, applications or building work.",
    )


def build_planning_help_page() -> str:
    return f"""
<section class="hero">
<span class="badge">Planning help</span>
<h1>Get A Clearer Planning Next Step Without A Noisy Quote Funnel</h1>
<p>UK Planning Guide is building a careful network of planning, design and home-improvement professionals. The first step is still guidance: use the free route check to understand whether your project may involve permitted development, planning permission, council approval or professional review.</p>
<div class="hero-ctas">
<a class="btn" href="{ROUTE_CHECK_PATH}">Start the free route check</a>
<a class="btn button-secondary" href="/personalised-planning-guidance/">See personalised guidance</a>
</div>
<div class="last-updated">Updated {get_month_year()}</div>
</section>

<section class="notice">
<span class="eyebrow">Honest service status</span>
<h2>Professional Help May Be Available, But It Is Not Guaranteed</h2>
<p>UK Planning Guide may be able to connect you with a suitable planning, design or home-improvement professional if one is available for your project type and location. This is not an instant matching promise, an approved-professionals claim or a guarantee that a professional will be introduced.</p>
</section>

<section>
<span class="eyebrow">Best starting point</span>
<h2>Use The Route Check Before You Ask For Help</h2>
<div class="answer-grid">
<div class="answer-card">
<h3>Useful without contact details</h3>
<p>The route check gives an instant result on the page. You do not need to submit your name, email or phone to get the guidance.</p>
</div>
<div class="answer-card">
<h3>Optional enquiry only</h3>
<p>If the result suggests the project is restricted, formal or professionally sensitive, you can choose whether to request help afterwards.</p>
</div>
<div class="answer-card">
<h3>Consent stays separate</h3>
<p>Contact and sharing consent are shown as separate unticked choices. Details are only shared where you have asked for that.</p>
</div>
</div>
<div class="hero-ctas">
<a class="btn" href="{ROUTE_CHECK_PATH}">Check my planning route</a>
</div>
</section>

{build_trust_framework(
    section_id="planning-help-trust",
    title="What This Help Route Is For",
    purpose="To help homeowners move from broad planning guidance into the right next step without making inflated promises about professional matching.",
    not_replace="It does not replace a council decision, a lawful development certificate, legal advice or formal professional input where those are needed.",
    built_from="The flow starts with a static route check, then allows an optional enquiry only if the user wants help checking the result properly.",
    verify_when="Verify formally where the property is listed, in a conservation area, affected by Article 4, close to a threshold, or already facing refusal or enforcement issues.",
    safest_next_step="Use the route check first. If suitable help is not available, use the result to speak directly to the council, gather project evidence or choose independent advice.",
    support_links=[
        ("Planning Route Check", ROUTE_CHECK_PATH),
        ("Privacy notice", "/privacy/"),
        ("Methodology", "/methodology/"),
    ],
)}
"""


def build_planning_help_thank_you_page() -> str:
    return f"""
<section class="hero">
<span class="badge">Planning help request</span>
<h1>Thank You For Sending Your Planning Help Enquiry</h1>
<p>Thanks for sending your project details through the Planning Route Check flow. UK Planning Guide may review the enquiry and contact you about the project, but a professional match is not guaranteed.</p>
</section>

<section>
<span class="eyebrow">What happens next</span>
<h2>Keep The Next Step Practical</h2>
<div class="answer-grid">
<div class="answer-card">
<h3>Enquiry review</h3>
<p>The details may be reviewed to understand the project type, location, likely route and whether suitable help may be available.</p>
</div>
<div class="answer-card">
<h3>No guaranteed match</h3>
<p>Suitable professional coverage may not exist for every project type or location, so this confirmation is not a promise of introduction.</p>
</div>
<div class="answer-card">
<h3>Useful fallback</h3>
<p>If no suitable help is available, use the result summary to check your council planning portal, gather project evidence or seek independent professional advice.</p>
</div>
</div>
</section>

<section>
<span class="eyebrow">While the details are fresh</span>
<h2>Useful Things To Gather Now</h2>
<ul class="checklist">
<li>Check the relevant local council planning portal and any conservation-area, Article 4 or listed-building records before starting work.</li>
<li>Gather site photos, rough measurements, boundary details and a simple sketch of the proposed work.</li>
<li>Save your project details and route-check summary so you can reuse the same facts consistently.</li>
<li>Use a qualified professional promptly for urgent enforcement, refusal, listed-building or high-stakes heritage issues.</li>
<li>Consider independent professional advice where the site is restricted, the project is close to a limit or the cost of getting the route wrong is meaningful.</li>
</ul>
<div class="hero-ctas">
<a class="btn" href="{ROUTE_CHECK_PATH}">Run another route check</a>
<a class="btn button-secondary" href="/councils/">Find your council guide</a>
</div>
</section>

<section>
<span class="eyebrow">Important reminder</span>
<h2>Do Not Treat This Confirmation As Planning Approval</h2>
<p>This page only confirms that an optional enquiry was sent through the route-check flow. It does not confirm that permitted development applies, that planning permission will be granted or that a professional has accepted the enquiry.</p>
<p>Before work starts, check the council record, any property-specific restrictions and the formal approval route that applies to the exact address.</p>
</section>
"""
