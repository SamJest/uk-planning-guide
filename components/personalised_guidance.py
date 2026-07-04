from html import escape
from urllib.parse import urlencode
from urllib.parse import quote

from components.faq_blocks import build_faq_section
from components.next_steps import build_next_step_cards
from components.trust_framework import build_trust_framework
from data.authority_profiles import GUIDANCE_EMAIL, GUIDANCE_FORM_PATH, GUIDANCE_SUCCESS_PATH
from utils.random_tools import get_month_year


SERVICE_NAME = "Personalised planning guidance"
GUIDANCE_PATH = "/personalised-planning-guidance/"
PRIVACY_PATH = "/privacy/"

DISCLAIMER_TEXT = (
    "Replies are informational personalised guidance based on the details you provide "
    "and publicly available information. They are not formal legal, architectural, "
    "surveying or council advice."
)
VERIFICATION_TEXT = (
    "Site-specific or borderline cases may still need checking with the local authority "
    "or a qualified specialist before drawings, applications or contractor spend move ahead."
)
PRIVACY_TEXT = (
    "Your enquiry details are used to respond to your request. Anonymised themes may be "
    "used to improve guides, tools, FAQs and site content. Identifiable case details are "
    "not published without permission, and sending an enquiry does not sign you up to marketing emails."
)
CONSENT_TEXT = (
    "If you want, you can also say that anonymous themes from your enquiry may be used to "
    "improve future guides and FAQs. This is optional and does not affect whether you receive a reply."
)

GUIDANCE_REQUEST_FIELDS = [
    {"name": "name", "label": "Full name", "type": "text", "required": True, "autocomplete": "name"},
    {"name": "email", "label": "Email", "type": "email", "required": True, "autocomplete": "email"},
    {"name": "property_type", "label": "Property type", "type": "text", "required": True, "autocomplete": "off"},
    {"name": "authority", "label": "Council / local authority area", "type": "text", "required": True, "autocomplete": "off"},
    {"name": "location", "label": "Town or location", "type": "text", "required": True, "autocomplete": "address-level2"},
    {
        "name": "project_stage",
        "label": "Project stage",
        "type": "select",
        "required": True,
        "options": [
            "Just exploring the route",
            "Comparing options and measurements",
            "Preparing for drawings or a certificate",
            "Preparing for an application or pre-app",
            "Trying to fix a stalled or awkward case",
        ],
    },
    {
        "name": "special_constraints",
        "label": "Known special constraints",
        "type": "select",
        "required": False,
        "options": [
            "No known special constraints",
            "Conservation area",
            "Listed building",
            "Article 4 concerns",
            "Flat or maisonette",
            "Previous additions or history concerns",
            "Not sure yet",
        ],
    },
    {
        "name": "project_summary",
        "label": "What you want to build or change",
        "type": "textarea",
        "required": True,
        "rows": 6,
        "help": "Keep it concise. The most useful summary is usually the project, the rough dimensions and the part that feels uncertain or risky.",
    },
    {
        "name": "key_dimensions",
        "label": "Approximate size / height / position",
        "type": "textarea",
        "required": False,
        "rows": 4,
    },
    {
        "name": "site_history",
        "label": "Previous extensions or planning-history notes",
        "type": "textarea",
        "required": False,
        "rows": 4,
    },
    {
        "name": "main_worry",
        "label": "Main thing you are worried about",
        "type": "textarea",
        "required": True,
        "rows": 4,
    },
]


def _cta_profile(context_label: str, compact: bool) -> dict[str, str]:
    label = str(context_label or "").lower()
    if "scenario" in label or "rule" in label:
        return {
            "button": "Open the rule form",
            "best_for": "Rule-led questions where the route depends on one control such as height, boundary position, heritage or Article 4 rather than the project type alone.",
            "reply": "The reply aims to separate the controlling rule from the surrounding noise, explain what is most likely to change locally, and point you to the safest follow-up check.",
        }
    if "local-search" in label or "council" in label:
        return {
            "button": "Open the local case form",
            "best_for": "Location-sensitive questions where the local page, authority context or formal next step matters more than a general national answer.",
            "reply": "The reply aims to narrow the local route, highlight the authority or site details most likely to change the answer, and show which check is worth doing next.",
        }
    if "methodology" in label or "about" in label:
        return {
            "button": "Start the request form",
            "best_for": "Cases where you understand the broad method already but want it applied to your own drawings, property history or local sensitivity.",
            "reply": "The reply aims to turn the site method into a project-specific informational steer, including where the answer still needs a certificate, pre-app advice or other formal confirmation.",
        }
    if compact:
        return {
            "button": "Open the request form",
            "best_for": "Borderline, awkward or site-specific cases where the guides have helped, but the answer still turns on facts unique to your property or proposal.",
            "reply": "The reply aims to narrow the likely route, flag the details that matter most, and tell you which verification step is safest before more money is spent.",
        }
    return {
        "button": "Start the request form",
        "best_for": "Projects that feel too specific for a broad guide yet too early for formal submissions or a full professional appointment.",
        "reply": "The reply aims to give a practical informational steer on the likely route, the local or site details most likely to change it, and the safest next move when certainty matters.",
    }


def _mailto_subject(context: str = "") -> str:
    clean = " ".join(str(context or "").split()).strip(" -")
    if clean:
        return f"{SERVICE_NAME} enquiry - {clean}"
    return f"{SERVICE_NAME} enquiry"


def build_guidance_prompt(context: str = "", *, include_page_reference: bool = False) -> str:
    lines = [
        "Hello,",
        "",
        "I would like some personalised planning guidance on this project:",
        "",
        "Property type:",
        "Council / local authority area:",
        "Town or location:",
        "What I want to build or change:",
        "Approximate size / height / position:",
        "Listed building / conservation area / flat / maisonette details if relevant:",
        "Previous extensions or outbuildings if relevant:",
        "Anything I am especially worried about:",
        "",
        "Optional: anonymous themes from this enquiry may be used to improve future guides and FAQs: Yes / No",
    ]

    clean_context = " ".join(str(context or "").split()).strip()
    if clean_context:
        lines.insert(3, f"Project or question: {clean_context}")

    if include_page_reference:
        lines.extend(["", "Page I was reading:"])

    return "\n".join(lines)


def build_guidance_mailto(context: str = "", *, include_page_reference: bool = False) -> str:
    subject = quote(_mailto_subject(context))
    body = quote(build_guidance_prompt(context, include_page_reference=include_page_reference))
    return escape(f"mailto:{GUIDANCE_EMAIL}?subject={subject}&body={body}", quote=True)


def build_guidance_request_href(context_label: str = "", email_context: str = "", prefill: dict[str, str] | None = None) -> str:
    return GUIDANCE_FORM_PATH


def _render_option(value: str) -> str:
    safe = escape(value)
    return f'<option value="{safe}">{safe}</option>'


def _render_form_field(field: dict) -> str:
    field_id = f"guidance-{field['name']}"
    label = f"{field['label']}{' *' if field.get('required') else ''}"
    required = " required" if field.get("required") else ""
    autocomplete = f' autocomplete="{escape(field.get("autocomplete", ""), quote=True)}"' if field.get("autocomplete") else ""
    help_html = f"<p class='field-help'>{field['help']}</p>" if field.get("help") else ""

    if field["type"] == "textarea":
        rows = int(field.get("rows", 5))
        control = f'<textarea id="{field_id}" name="{field["name"]}" rows="{rows}"{required}{autocomplete}></textarea>'
        wide_class = " form-field-wide"
    elif field["type"] == "select":
        options = "".join(_render_option(option) for option in field.get("options", []))
        control = (
            f'<select id="{field_id}" name="{field["name"]}"{required}{autocomplete}>'
            '<option value="">Select an option</option>'
            f"{options}</select>"
        )
        wide_class = ""
    else:
        control = f'<input id="{field_id}" name="{field["name"]}" type="{escape(field["type"], quote=True)}"{required}{autocomplete}>'
        wide_class = ""

    return f"""
<div class="form-field{wide_class}">
<label for="{field_id}">{label}</label>
{control}
{help_html}
</div>
"""


def build_guidance_request_form(*, form_key: str = "guidance-request", action: str = GUIDANCE_SUCCESS_PATH) -> str:
    fields_html = "".join(_render_form_field(field) for field in GUIDANCE_REQUEST_FIELDS)
    return f"""
<form class="find-help-form guidance-request-form" method="post" action="{action}" data-guidance-form="{form_key}" data-static-submit="redirect" data-success-url="{action}">
<div class="form-grid">
{fields_html}
</div>
<div class="form-note">
<p><strong>How this works:</strong> This guided form is the fallback route for case-specific planning questions after the quick checks have narrowed the issue. It captures the key facts cleanly before you move into a reply or a stronger formal check.</p>
<p><strong>Privacy:</strong> {PRIVACY_TEXT} <a href="{PRIVACY_PATH}">Privacy notice</a>.</p>
<noscript><p><strong>If the form does not submit:</strong> Email <a href="mailto:{escape(GUIDANCE_EMAIL, quote=True)}">{escape(GUIDANCE_EMAIL)}</a> with the same details.</p></noscript>
</div>
<div class="hero-ctas">
<button type="submit" class="btn">Submit guidance request</button>
</div>
</form>
"""


def build_guidance_prompt_box(context: str = "") -> str:
    prompt = escape(build_guidance_prompt(context))
    return f"""
<section class="guidance-prompt-block" id="guidance-what-to-send">
<span class="eyebrow">What to send</span>
<h2>The Email Checklist That Usually Gets The Clearest Reply</h2>
<p class="section-lead">Keep it concise, but include enough detail to show what the project is, where it is and why the route may not be straightforward.</p>
<div class="answer-grid">
<div class="answer-card">
<h3>Useful details to include</h3>
<ul class="checklist">
<li>Property type.</li>
<li>Council or local authority area.</li>
<li>Town or location.</li>
<li>What you want to build or change.</li>
<li>Approximate size, height and position.</li>
<li>Whether the property is listed, in a conservation area, or is a flat or maisonette if relevant.</li>
<li>Any previous extensions or outbuildings that may already affect the answer.</li>
<li>The main thing you are worried about.</li>
</ul>
</div>
<div class="answer-card">
<h3>Suggested email format</h3>
<p>Paste this into your email and fill in the blanks:</p>
<textarea class="guidance-prompt" readonly aria-label="Suggested personalised planning guidance email prompt">{prompt}</textarea>
</div>
</div>
</section>
"""


def build_guidance_value_grid() -> str:
    return """
<section id="guidance-what-you-get">
<span class="eyebrow">What you will get back</span>
<h2>A Practical Reply That Helps You Spend Money In The Right Order</h2>
<div class="answer-grid">
<div class="answer-card">
<h3>Likely route</h3>
<p>A plain-English steer on the likely planning route, including where the answer still looks routine and where it starts to tighten.</p>
</div>
<div class="answer-card">
<h3>What may change it locally</h3>
<p>The local designations, authority context or property details most likely to move the answer away from the broad national baseline.</p>
</div>
<div class="answer-card">
<h3>Best next steps</h3>
<p>The details to verify next, the checks worth doing before you pay for more work, and when formal confirmation starts to look worthwhile.</p>
</div>
</div>
</section>
"""


def build_guidance_limitations() -> str:
    return f"""
<section id="guidance-limits">
<span class="eyebrow">Clear limits</span>
<h2>What This Can And Cannot Do</h2>
<div class="answer-grid">
<div class="answer-card">
<h3>What it can do well</h3>
<ul class="checklist">
<li>Review the details you send and give a case-specific plain-English steer.</li>
<li>Highlight the likely planning route and the local or site details most likely to change it.</li>
<li>Help you decide what to verify next before you spend more money.</li>
</ul>
</div>
<div class="answer-card">
<h3>What it cannot do</h3>
<ul class="checklist">
<li>Confirm a planning outcome or guarantee that permission is or is not required.</li>
<li>Replace formal legal, architectural, surveying or council input.</li>
<li>Override local authority records, property history or site-specific facts that still need formal checking.</li>
</ul>
</div>
<div class="answer-card">
<h3>When formal verification is worth it</h3>
<ul class="checklist">
<li>The proposal is close to a limit.</li>
<li>The site is listed, in a conservation area or may be affected by Article 4.</li>
<li>The financial or timing consequences of getting the route wrong are meaningful.</li>
</ul>
</div>
</div>
<p class="guidance-disclaimer guidance-disclaimer-standalone" data-guidance-disclaimer="true"><strong>Important:</strong> {DISCLAIMER_TEXT} {VERIFICATION_TEXT}</p>
</section>
"""


def build_guidance_privacy_section() -> str:
    return f"""
<section id="guidance-privacy">
<span class="eyebrow">Privacy and enquiry use</span>
<h2>How Enquiries Are Used</h2>
<div class="answer-grid">
<div class="answer-card">
<h3>Used to reply</h3>
<p>Your email and enquiry details are used to read the case, frame the reply and send a response to you.</p>
</div>
<div class="answer-card">
<h3>Used to improve the site</h3>
<p>Anonymised themes and repeated question patterns may be used to improve guides, tools, FAQs and site content over time.</p>
</div>
<div class="answer-card">
<h3>What is not done</h3>
<p>Identifiable case details are not published as examples without permission, and sending an enquiry does not sign you up to marketing emails.</p>
</div>
</div>
<p class="guidance-privacy-note" data-guidance-privacy="true">{PRIVACY_TEXT}</p>
<p class="guidance-consent-note">{CONSENT_TEXT}</p>
<p><a href="{PRIVACY_PATH}">Read the privacy notice</a></p>
</section>
"""


def build_guidance_faq() -> str:
    items = [
        (
            "What happens after I submit the form?",
            "The case details are read and used to frame a practical reply about the likely route, the local details that could change it and the next checks worth making, with the response sent by email.",
        ),
        (
            "What details should I include?",
            "Send the property type, local authority area, town or location, what you want to build or change, the approximate size or position, any heritage or flat-related constraints, previous additions, and the main thing worrying you.",
        ),
        (
            "Is this formal advice?",
            "No. It is informational personalised guidance based on the details you provide and publicly available information, not formal legal, architectural, surveying or council advice.",
        ),
        (
            "Can you tell me if I definitely need permission?",
            "No one should promise that from a short email alone. The aim is to give a practical steer on the likely route, the local or property details most likely to change it, and the next checks worth making.",
        ),
        (
            "When should I skip this route and go straight to a specialist?",
            "Do that when the project is urgent, already at a formal stage, or too high-stakes to leave on an informational steer before formal checking.",
        ),
    ]
    return build_faq_section(
        items,
        section_id="guidance-faq",
        eyebrow="Common questions",
        title="What People Usually Want To Know Before They Submit A Request",
        intro="Keep this block for the trust, scope and response-time questions that usually come up once the service looks relevant.",
    )


def build_guidance_triage_cards() -> str:
    return f"""
<section id="guidance-triage" class="guidance-triage">
<span class="eyebrow">Start lighter first</span>
<h2>Use The Shortest Useful Route Before The Full Form</h2>
<p class="section-lead">Most visitors should get value before sending details. Use the quick checks below first, then use the longer form when the remaining question is genuinely case-specific.</p>
<div class="next-step-grid">
<a class="next-step-card" href="/tools/planning-route-check/" data-guidance-triage="route-check" data-next-step-card="guidance-route-check" data-page-family="guidance" data-tool-slug="planning-route-check">
<span class="card-kicker">Quick route</span>
<strong>Run the planning route check</strong>
<span>Best when you still need the basic planning, permitted development, certificate or council route narrowed.</span>
<em>Check route</em>
</a>
<a class="next-step-card" href="/tools/lawful-development-certificate-checker/" data-guidance-triage="ldc-checker" data-next-step-card="guidance-ldc-checker" data-page-family="guidance" data-tool-slug="lawful-development-certificate-checker">
<span class="card-kicker">Formal proof</span>
<strong>Check whether an LDC is worth it</strong>
<span>Best when permitted development may work but the cost of being wrong would matter later.</span>
<em>Check LDC</em>
</a>
<a class="next-step-card" href="/tools/drawings-cost-readiness-checker/" data-guidance-triage="drawings-readiness" data-next-step-card="guidance-drawings-readiness" data-page-family="guidance" data-tool-slug="drawings-cost-readiness-checker">
<span class="card-kicker">Spend order</span>
<strong>Check drawing readiness</strong>
<span>Best when you are close to paying for drawings but the route or brief may still be thin.</span>
<em>Check readiness</em>
</a>
<a class="next-step-card" href="#guidance-request-form" data-guidance-triage="full-form" data-next-step-card="guidance-full-form" data-page-family="guidance">
<span class="card-kicker">Fallback</span>
<strong>Use the full guidance form</strong>
<span>Best when the quick checks have helped but your exact property, drawings or local context still decide the answer.</span>
<em>Open form</em>
</a>
</div>
</section>
"""


def build_personalised_guidance_cta(
    *,
    title: str,
    description: str,
    context_label: str,
    email_context: str = "",
    intro_label: str = SERVICE_NAME,
    secondary_href: str = GUIDANCE_PATH,
    secondary_label: str = "See how it works",
    compact: bool = False,
    prefill: dict[str, str] | None = None,
    tracking_context: dict[str, str] | None = None,
) -> str:
    profile = _cta_profile(context_label, compact)
    guidance_href = build_guidance_request_href(context_label=context_label, email_context=email_context, prefill=prefill)
    context_attrs = []
    if context_label:
        context_attrs.append(f'data-guidance-context="{escape(" ".join(str(context_label).split()), quote=True)}"')
    if email_context:
        context_attrs.append(f'data-guidance-email-context="{escape(" ".join(str(email_context).split()), quote=True)}"')
    if prefill:
        serialized_prefill = urlencode(
            {
                str(key or "").strip(): " ".join(str(value or "").split()).strip()
                for key, value in prefill.items()
                if str(key or "").strip() and " ".join(str(value or "").split()).strip()
            }
        )
        if serialized_prefill:
            context_attrs.append(f'data-guidance-prefill="{escape(serialized_prefill, quote=True)}"')
    for key, value in (tracking_context or {}).items():
        clean_value = " ".join(str(value or "").split()).strip()
        if not clean_value:
            continue
        clean_key = str(key or "").strip().lower().replace("_", "-")
        clean_key = "".join(ch if ch.isalnum() or ch == "-" else "-" for ch in clean_key).strip("-")
        if clean_key:
            context_attrs.append(f'data-guidance-{clean_key}="{escape(clean_value, quote=True)}"')
    extra_attrs = f" {' '.join(context_attrs)}" if context_attrs else ""
    return f"""
<section class="personalised-guidance-cta{' personalised-guidance-cta-compact' if compact else ''}" data-guidance-cta="{escape(context_label, quote=True)}">
<span class="eyebrow">{intro_label}</span>
<h2>{title}</h2>
<p>{description}</p>
<div class="hero-ctas guidance-actions">
<a class="btn" href="{guidance_href}" data-guidance-form-link="true"{extra_attrs}>{profile['button']}</a>
<a class="btn button-secondary" href="{secondary_href}">{secondary_label}</a>
</div>
<div class="answer-grid guidance-cta-grid">
<div class="answer-card">
<h3>Best for</h3>
<p>{profile['best_for']}</p>
</div>
<div class="answer-card">
<h3>What the reply aims to do</h3>
<p>{profile['reply']}</p>
</div>
<div class="answer-card">
<h3>What to include</h3>
<p>Property type, council area, location, the change you want to make, approximate dimensions, relevant heritage or flat-related details, previous additions and the main concern.</p>
</div>
</div>
<p class="guidance-disclaimer" data-guidance-disclaimer="true"><strong>Important:</strong> {DISCLAIMER_TEXT} {VERIFICATION_TEXT}</p>
<p class="guidance-privacy-note" data-guidance-privacy="true">{PRIVACY_TEXT} <a href="{PRIVACY_PATH}">Privacy notice</a>.</p>
<p class="guidance-consent-note">{CONSENT_TEXT}</p>
</section>
"""


def build_personalised_guidance_page() -> str:
    top_cta = build_personalised_guidance_cta(
        title="Get A Practical Plain-English Steer Only When The Quick Checks Are Not Enough",
        description="Start with the lower-friction tools if the route, certificate value or drawing readiness is still unclear. Use the full form after that when your exact project facts still decide the safest next move.",
        context_label="dedicated-page-top",
        email_context="specific planning question",
        secondary_href="#guidance-triage",
        secondary_label="Start with quick checks",
    )
    bottom_cta = build_personalised_guidance_cta(
        title="Ready To Submit The Details?",
        description="Use the checklist below, keep the summary concise, and include enough detail to show why your case may not fit a broad one-size-fits-all answer.",
        context_label="dedicated-page-bottom",
        email_context="ready to submit",
        secondary_href=PRIVACY_PATH,
        secondary_label="Read privacy notice",
    )

    return f"""
<section class="hero" data-guidance-page="true">
<span class="badge">{SERVICE_NAME}</span>
<h1>Case-Specific Planning Guidance In Plain English</h1>
<p>Use this when the broad route and quick tools are not enough on their own, but the project is still too early, too borderline or too local for guesswork. The full form is a fallback for the real planning questions that still turn on your project, property and local context.</p>
<div class="last-updated">Updated {get_month_year()}</div>
</section>

<section class="page-jump-links">
<span class="eyebrow">Jump to what matters</span>
<h2>Use This Page In The Order That Makes The Service Easiest To Judge</h2>
<div class="link-grid">
<a href="#guidance-who-for">Check whether it is the right fit</a>
<a href="#guidance-triage">Use quick checks first</a>
<a href="#guidance-what-to-send">See what to send</a>
<a href="#guidance-request-form">Open the guided form</a>
<a href="#guidance-what-you-get">See what you will get back</a>
<a href="#guidance-limits">Read the limits and verification notes</a>
<a href="#guidance-privacy">Read the privacy and enquiry-use wording</a>
<a href="#guidance-faq">Check the common questions</a>
</div>
</section>

{top_cta}

{build_guidance_triage_cards()}

{build_next_step_cards(page_family="guidance", title="Other Useful Next Steps Before The Form", intro="If the question is mainly about proof, cost or readiness, these checks usually give a faster answer than sending a full case summary.")}

<section id="guidance-who-for">
<span class="eyebrow">Who it is for</span>
<h2>Useful When The Real Question Is Specific, Borderline Or Locally Sensitive</h2>
<div class="answer-grid">
<div class="answer-card">
<h3>Useful for homeowners</h3>
<p>Helpful when you want to understand the likely route for an extension, loft, outbuilding, frontage change or other domestic project before the costlier stages begin.</p>
</div>
<div class="answer-card">
<h3>Useful for awkward edge cases</h3>
<p>Especially useful where previous additions, listed status, conservation-area context, flats, maisonettes, or local sensitivities may change the normal answer.</p>
</div>
<div class="answer-card">
<h3>Useful before you spend more</h3>
<p>Best used as a practical early steer so you can decide whether the next move is more reading, a certificate, a council check, a redesign or formal specialist input.</p>
</div>
</div>
</section>

<section id="guidance-request-form">
<span class="eyebrow">Structured request form</span>
<h2>The Fallback Route For A Case-Specific Planning Question</h2>
<p class="section-lead">Use the form once the quick checks have narrowed the route but the remaining answer still depends on your exact property, project details, planning history or local authority context.</p>
{build_guidance_request_form()}
</section>

{build_guidance_prompt_box()}

{build_guidance_value_grid()}

{build_guidance_limitations()}

{build_trust_framework(
    section_id="guidance-trust",
    title="What This Guidance Is For And Where It Stops",
    purpose="To give a case-specific informational steer once the guides and quick tools have narrowed the question but the answer still depends on the proposal details, the site or the local authority context.",
    not_replace="It does not replace a council decision, legal advice, architectural design advice, surveying advice or any formal confirmation needed for a borderline or high-stakes scheme.",
    built_from="Replies are framed around the details you send, the same national and local planning logic used across the site, and the public information needed to identify the checks most likely to matter next.",
    verify_when="Stop relying on this guidance alone when the route depends on a tight threshold, a sensitive site, uncertain planning history or a decision you would not want to revisit after paying for drawings or works.",
    safest_next_step="Use a lawful development certificate when the scheme appears lawful but certainty matters. Use pre-application advice or formal professional input when local judgement, heritage controls or design complexity are doing most of the work.",
    support_links=[
        ("Methodology", "/methodology/"),
        ("Privacy notice", "/privacy/"),
    ],
)}

<section id="guidance-verify">
<span class="eyebrow">When to verify formally</span>
<h2>Situations Where This Guidance Should Lead To A Stronger Formal Check</h2>
<div class="answer-grid">
<div class="answer-card">
<h3>Close to a threshold</h3>
<p>If the route only works because a measurement, height, volume or siting point stays inside a tight limit, measured drawings and formal confirmation are usually worth it.</p>
</div>
<div class="answer-card">
<h3>Heritage or special controls</h3>
<p>If listed-building issues, conservation-area context, Article 4 coverage or similar controls may be doing most of the work, the safest route is to verify the exact property position rather than assume.</p>
</div>
<div class="answer-card">
<h3>Meaningful cost risk</h3>
<p>If getting the route wrong would create wasted fees, a redesign, delays or a poor submission strategy, treat that as the point to step up into formal checking.</p>
</div>
</div>
</section>

{build_guidance_privacy_section()}

{build_guidance_faq()}

{bottom_cta}
"""


def build_privacy_page() -> str:
    mailto_href = build_guidance_mailto("privacy question")
    return f"""
<section class="hero">
<span class="badge">Privacy notice</span>
<h1>Privacy Notice For Email Enquiries</h1>
<p>This notice explains how UK Planning Guide uses email enquiry details for personalised planning guidance and related site-improvement work.</p>
<div class="last-updated">Updated {get_month_year()}</div>
</section>

<section>
<span class="eyebrow">Scope</span>
<h2>What This Notice Covers</h2>
<p>This notice is mainly about guidance requests sent through the structured form and follow-up emails sent to {GUIDANCE_EMAIL}. It sits alongside the wider site trust material and keeps the enquiry use clear in plain English.</p>
</section>

<section>
<span class="eyebrow">How enquiry details are used</span>
<h2>What Happens When You Email</h2>
<div class="answer-grid">
<div class="answer-card">
<h3>Used to respond</h3>
<p>We use the email address and case details you send to read the enquiry, prepare a reply and respond to your request.</p>
</div>
<div class="answer-card">
<h3>Used to improve the site</h3>
<p>Anonymised themes, repeated questions and non-identifiable patterns may be used to improve guides, tools, FAQs and site content.</p>
</div>
<div class="answer-card">
<h3>Not used as marketing sign-up</h3>
<p>Sending an enquiry does not sign you up to marketing emails.</p>
</div>
</div>
<p class="guidance-privacy-note" data-guidance-privacy="true">{PRIVACY_TEXT}</p>
</section>

<section>
<span class="eyebrow">Examples and permissions</span>
<h2>Anonymous Themes And Identifiable Details</h2>
<p>Identifiable case details are not published as examples without permission. If you want, you may optionally agree that anonymous themes from your enquiry can help improve future guides and FAQs. This is optional and does not affect whether you receive a reply.</p>
</section>

<section>
<span class="eyebrow">Planning help enquiries</span>
<h2>How Optional Planning Help Requests Are Used</h2>
<div class="answer-grid">
<div class="answer-card">
<h3>What is collected</h3>
<p>If you choose to request planning help after using the route check, the form may collect your name, email, optional phone number, project type, property type, location, council area, timeframe, restrictions, route-check result and project notes.</p>
</div>
<div class="answer-card">
<h3>Why it is collected</h3>
<p>The details are used to receive and store the enquiry, contact you about it and assess whether suitable planning, design or home-improvement help may be available for the project type and location.</p>
</div>
<div class="answer-card">
<h3>Sharing only with consent</h3>
<p>Your enquiry details may be shared with a relevant professional only where you have requested help and given the separate sharing consent. A professional match is not guaranteed.</p>
</div>
</div>
<p>Planning help submissions may be sent to a dedicated enquiry endpoint so the request can be stored and reviewed. Personal details from the enquiry are not sent to Google Analytics or used as analytics event fields.</p>
<p>You can request deletion of enquiry details or ask a privacy question by emailing <a href="{mailto_href}" data-guidance-mailto="true">{GUIDANCE_EMAIL}</a>. Do not include unnecessary sensitive personal information in a planning help request.</p>
</section>

<section>
<span class="eyebrow">Limits</span>
<h2>What This Service Is And Is Not</h2>
<p class="guidance-disclaimer guidance-disclaimer-standalone" data-guidance-disclaimer="true"><strong>Important:</strong> {DISCLAIMER_TEXT} {VERIFICATION_TEXT}</p>
<p>If you have a privacy question about an enquiry, email <a href="{mailto_href}" data-guidance-mailto="true">{GUIDANCE_EMAIL}</a>.</p>
</section>
"""


def build_guidance_request_page() -> str:
    return f"""
<section class="hero">
<span class="badge">Guidance request form</span>
<h1>Submit A Case-Specific Planning Guidance Request</h1>
<p>Use this form after the lighter checks have helped but the remaining planning answer still depends on your exact project, property, local authority area or planning history.</p>
<div class="last-updated">Updated {get_month_year()}</div>
</section>

{build_guidance_triage_cards()}

{build_guidance_request_form()}

<section>
<span class="eyebrow">Before you submit</span>
<h2>What Usually Makes The Reply More Useful</h2>
<div class="answer-grid">
<div class="answer-card">
<h3>Be concrete</h3>
<p>Describe the real project, not just the broad category. The useful details are usually the part of the house or site affected, the scale and the local sensitivity.</p>
</div>
<div class="answer-card">
<h3>Say what feels risky</h3>
<p>If the concern is Article 4, a conservation area, a boundary issue or planning history, say that directly. That is often what determines the safest next step.</p>
</div>
<div class="answer-card">
<h3>Keep formal checks separate</h3>
<p>This form helps narrow the route. It does not replace a lawful development certificate, pre-application advice or a formal council decision.</p>
</div>
</div>
</section>
"""


def build_guidance_request_success_page() -> str:
    return f"""
<section class="hero">
<span class="badge">Guidance request received</span>
<h1>Your Planning Guidance Request Has Been Captured</h1>
<p>The request has been recorded through the guided form flow. Keep your drawings, site photos and planning-history notes together so the next reply or formal check can be handled more cleanly.</p>
</section>

<section>
<span class="eyebrow">What to do next</span>
<h2>While The Details Are Still Fresh</h2>
<div class="answer-grid">
<div class="answer-card">
<h3>Keep the evidence together</h3>
<p>Have the rough dimensions, site photos and any planning-history notes ready in case the next step needs more detail.</p>
</div>
<div class="answer-card">
<h3>Re-open the most relevant guide</h3>
<p>If the route still feels broad, go back to the strongest project, council or rule page rather than continuing with a generic search trail.</p>
</div>
<div class="answer-card">
<h3>Escalate if the case is high-stakes</h3>
<p>If the proposal is close to a limit or financially sensitive, treat a lawful development certificate, pre-application advice or another formal check as the safer route.</p>
</div>
</div>
<div class="hero-ctas">
<a class="btn" href="/tools/planning-decision-tool/">Open the planning decision tool</a>
<a class="btn button-secondary" href="/methodology/">Read the methodology</a>
</div>
</section>
"""
