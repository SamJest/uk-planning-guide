from __future__ import annotations

from html import escape

from components.faq_blocks import build_faq_section
from components.trust_framework import build_trust_framework
from data.find_help import (
    FIND_HELP_ENABLED,
    FIND_HELP_CTA_FAQ_SLUGS,
    FIND_HELP_CTA_PROJECT_SLUGS,
    FORM_NOSCRIPT_NOTE,
    FORM_PRIVACY_NOTE,
    HOMEOWNER_REQUEST_FIELDS,
    ROLL_OUT_NOTE,
    SPECIALIST_APPLICATION_FIELDS,
)
from utils.random_tools import get_month_year


def _render_option(value: str) -> str:
    safe = escape(value)
    return f'<option value="{safe}">{safe}</option>'


def _render_field(field: dict) -> str:
    field_id = f"find-help-{field['name']}"
    label = f"{field['label']}{' *' if field.get('required') else ''}"
    help_html = f"<p class='field-help'>{field['help']}</p>" if field.get("help") else ""
    required = " required" if field.get("required") else ""
    autocomplete = f' autocomplete="{escape(field["autocomplete"], quote=True)}"' if field.get("autocomplete") else ""

    if field["type"] == "textarea":
        rows = int(field.get("rows", 5))
        control = f'<textarea id="{field_id}" name="{field["name"]}" rows="{rows}"{required}{autocomplete}></textarea>'
    elif field["type"] == "select":
        options = "".join(_render_option(option) for option in field.get("options", []))
        control = (
            f'<select id="{field_id}" name="{field["name"]}"{required}{autocomplete}>'
            '<option value="">Select an option</option>'
            f"{options}</select>"
        )
    else:
        field_type = escape(field["type"], quote=True)
        control = f'<input id="{field_id}" name="{field["name"]}" type="{field_type}"{required}{autocomplete}>'

    wide_class = " form-field-wide" if field["type"] == "textarea" else ""
    return f"""
<div class="form-field{wide_class}">
<label for="{field_id}">{label}</label>
{control}
{help_html}
</div>
"""


def _render_form(fields: list[dict], *, action: str, submit_label: str, form_key: str) -> str:
    fields_html = "".join(_render_field(field) for field in fields)
    return f"""
<form class="find-help-form" method="post" action="{action}" data-find-help-form="{form_key}" data-static-submit="redirect" data-success-url="{action}">
<div class="form-grid">
{fields_html}
</div>
<div class="form-note">
<p><strong>Current service status:</strong> This form records structured demand or applications while coverage is being assembled. Submitting it does not mean live matching is already active in every category or area.</p>
<p><strong>Privacy:</strong> {FORM_PRIVACY_NOTE} <a href="/privacy/">Privacy notice</a>.</p>
<noscript><p><strong>If the form does not submit:</strong> {FORM_NOSCRIPT_NOTE}</p></noscript>
</div>
<div class="hero-ctas">
<button type="submit" class="btn">{submit_label}</button>
</div>
</form>
"""


def _render_path_cards(cards: list[tuple[str, str, str, str]]) -> str:
    return "".join(
        f"""
<a class="card" href="{href}">
<div class="card-kicker">{kicker}</div>
<h3>{title}</h3>
<p>{description}</p>
<span class="cta">Open page</span>
</a>
"""
        for href, kicker, title, description in cards
    )


def build_find_help_cta(*, audience_label: str = "homeowners", compact: bool = True) -> str:
    if not FIND_HELP_ENABLED:
        return ""
    description = (
        "Use Find Help when broad guidance is no longer enough and you want the cleanest route into the right kind of formal or professional support."
    )
    label = "Need a clearer formal-help route?"
    if audience_label == "specialists":
        label = "Join the curated specialist network"
        description = (
            "Applications are reviewed manually for a carefully limited service built around quality, clarity and homeowner fit."
        )

    return f"""
<section class="find-help-cta{' find-help-cta-compact' if compact else ''}" data-find-help-cta="true">
<span class="eyebrow">Find Help</span>
<h2>{label}</h2>
<p>{description}</p>
<div class="hero-ctas">
<a class="btn" href="/find-help/">Open Find Help</a>
<a class="btn button-secondary" href="/find-help/homeowners/request/">Register your project</a>
</div>
<p class="find-help-rollout-note">{ROLL_OUT_NOTE}</p>
</section>
"""


def should_show_find_help_project_cta(project_slug: str) -> bool:
    return FIND_HELP_ENABLED and project_slug in FIND_HELP_CTA_PROJECT_SLUGS


def should_show_find_help_faq_cta(faq_slug: str) -> bool:
    return FIND_HELP_ENABLED and faq_slug in FIND_HELP_CTA_FAQ_SLUGS


def build_find_help_faq(*, focus: str = "hub") -> str:
    if focus == "homeowners":
        items = [
            (
                "What happens after I register my project?",
                "Your brief is recorded so demand, project type and area can be reviewed before matching expands.",
            ),
            (
                "What should I include?",
                "Include the project type, stage, location, likely constraints and the kind of specialist help you expect to need next.",
            ),
            (
                "Is the vetted local network already live?",
                "Not everywhere. Coverage is still being assembled carefully, so registration does not mean live matching is already active for every project type or area.",
            ),
            (
                "Is this formal advice?",
                "No. The Find Help route is about moving toward the right kind of support, not replacing formal planning, legal or professional advice.",
            ),
            (
                "When should I go straight to a specialist instead?",
                "Go straight to a specialist or council route if the project is urgent, already at a formal stage or too high-stakes to wait for coverage to expand.",
            ),
        ]
        intro = "Use this block to resolve the trust and expectation questions that usually come up before someone registers interest."
    else:
        items = [
            (
                "What happens after I send my details?",
                "Homeowner requests are logged in a structured format so coverage, category demand and the right future match route can be reviewed properly.",
            ),
            (
                "What should I include?",
                "Include the project type, location, stage reached, likely constraints and the kind of help you think you need next.",
            ),
            (
                "Is this formal advice?",
                "No. Find Help is an escalation route into the right kind of support, not a substitute for formal planning, legal or specialist advice.",
            ),
            (
                "Is the vetted local network already live?",
                "Only selectively. Coverage is still being expanded carefully and the site is explicit that live matching is not yet available for every category or area.",
            ),
            (
                "When should I go straight to a specialist instead?",
                "Go directly to a specialist or council route if the project is already formal, urgent or too high-stakes to leave on a limited-coverage matching process.",
            ),
        ]
        intro = "Keep this FAQ for the trust, scope and next-step questions that usually matter before someone decides whether Find Help is the right route."

    return build_faq_section(
        items,
        section_id=f"find-help-{focus}-faq",
        eyebrow="Find Help FAQ",
        title="Questions People Usually Ask Before They Commit",
        intro=intro,
    )


def build_find_help_hub_page() -> str:
    cards = [
        (
            "/find-help/homeowners/",
            "Homeowners",
            "Register A Project",
            "See how the matching service is being assembled and register your project interest now.",
        ),
        (
            "/find-help/specialists/",
            "Specialists",
            "Apply To Join",
            "Read how the curated network is being assembled and apply for manual review.",
        ),
        (
            "/find-help/how-it-works/",
            "Future flow",
            "How It Will Work",
            "Understand the intended matching process and the current service status.",
        ),
        (
            "/find-help/trust/",
            "Trust and fairness",
            "How The Service Stays Selective",
            "Read the homeowner-first principles behind the review process and future matching model.",
        ),
    ]

    return f"""
<section class="hero" data-find-help-page="hub">
<span class="badge">Find Help</span>
<h1>When Broad Guidance Stops Being Enough, Find The Right Next Kind Of Help</h1>
<p>Find Help explains the route from general guidance into more formal or specialist support. It keeps three paths separate: broad site guidance, tailored informational guidance, and the point where council or professional input becomes the safer next move.</p>
<div class="last-updated">Updated {get_month_year()}</div>
</section>

<section class="notice">
<span class="eyebrow">Current service status</span>
<h2>Selective Service, Honest About Coverage</h2>
<p>{ROLL_OUT_NOTE}</p>
</section>

<section>
<span class="eyebrow">Choose the path that fits</span>
<h2>Use The Route That Matches The Stage You Are Actually At</h2>
<div class="answer-grid">
<div class="answer-card">
<h3>Broad guidance</h3>
<p>Stay with the guides, tools and FAQ pages when you are still narrowing the route and the next task is understanding what usually applies.</p>
</div>
<div class="answer-card">
<h3>Tailored informational guidance</h3>
<p>Use personalised guidance when the broad route is clear but the live answer still depends on your exact property, local authority area or project details.</p>
</div>
<div class="answer-card">
<h3>Formal or professional help</h3>
<p>Use Find Help and the council-facing routes when the cost of being wrong is rising and the next step needs to be more formal, local or specialist.</p>
</div>
</div>
</section>

<section>
<span class="eyebrow">Current routes</span>
<h2>Homeowner And Specialist Paths</h2>
<div class="grid">{_render_path_cards(cards)}</div>
</section>

{build_find_help_faq(focus="hub")}

{build_trust_framework(
    section_id="find-help-trust",
    title="What Find Help Is For And Where It Stops",
    purpose="To help users move from answer-first planning guidance into the right next kind of support without pretending every project needs a marketplace or that coverage already exists everywhere.",
    not_replace="It does not replace checking the council route, choosing your own adviser carefully, or taking direct specialist input where the project is already at a formal or high-stakes stage.",
    built_from="The service is shaped around the same site method: broad guidance first, tailored informational support second, then cleaner escalation into council checks or specialist help when the case becomes more specific.",
    verify_when="Stop relying on broad guidance alone when the project is borderline, the local authority angle is doing most of the work, or the next spend depends on getting the route right.",
    safest_next_step="Use personalised guidance when the issue is still mainly informational. Use council confirmation or specialist support when the project needs a certificate, a pre-app view, a formal application strategy or project delivery help.",
    support_links=[
        ('Personalised planning guidance', '/personalised-planning-guidance/'),
        ('Methodology', '/methodology/'),
        ('Privacy notice', '/privacy/'),
    ],
)}
"""


def build_find_help_homeowners_page() -> str:
    return f"""
<section class="hero" data-find-help-page="homeowners">
<span class="badge">Find Help for homeowners</span>
<h1>Register Your Project While The Curated Local Network Is Still Being Assembled</h1>
<p>This future service is being built for homeowners who want clear, reputable local help after the planning route starts to narrow. The aim is to offer a small number of suitable specialist options, not endless listings or a noisy quote race.</p>
<div class="last-updated">Updated {get_month_year()}</div>
</section>

<section class="notice">
<span class="eyebrow">Service status</span>
<h2>Not A Live Marketplace Yet</h2>
<p>{ROLL_OUT_NOTE}</p>
</section>

<section>
<span class="eyebrow">What the future service will do</span>
<h2>How This Will Help Once Coverage Is Ready</h2>
<div class="answer-grid">
<div class="answer-card">
<h3>Review the brief properly</h3>
<p>The future flow starts with the homeowner project brief, so the matching logic is based on the real planning and delivery question rather than a generic category click.</p>
</div>
<div class="answer-card">
<h3>Offer a short curated match set</h3>
<p>Where coverage exists, the aim is to identify a small number of relevant local specialists rather than a huge directory with hidden ranking logic.</p>
</div>
<div class="answer-card">
<h3>Keep the next step clear</h3>
<p>The service is intended to sit naturally after guidance, tools and tailored planning support, so homeowners can move from "what route am I on?" into "who is the right kind of help for this stage?"</p>
</div>
</div>
</section>

<section>
<span class="eyebrow">What you can do now</span>
<h2>Register Interest While The Network Is Being Built</h2>
<p>Homeowners can register a project now so UK Planning Guide can understand where demand is building first. Matching will launch carefully in stages, and you may be contacted once relevant coverage is available for your project type and area.</p>
<div class="hero-ctas">
<a class="btn" href="/find-help/homeowners/request/">Register your project</a>
<a class="btn button-secondary" href="/find-help/how-it-works/">See how it is intended to work</a>
</div>
</section>

{build_find_help_faq(focus="homeowners")}
"""


def build_find_help_homeowner_request_page() -> str:
    form = _render_form(
        HOMEOWNER_REQUEST_FIELDS,
        action="/find-help/homeowners/request/success/",
        submit_label="Register project interest",
        form_key="homeowner-request",
    )
    return f"""
<section class="hero" data-find-help-page="homeowner-request">
<span class="badge">Homeowner request</span>
<h1>Register Your Project Interest</h1>
<p>Use this form to tell UK Planning Guide what kind of project help you may need. The network is still being assembled, so this is a structured early-interest registration rather than a promise of immediate live matching.</p>
<div class="last-updated">Updated {get_month_year()}</div>
</section>

<section class="notice">
<span class="eyebrow">Before you submit</span>
<h2>Keep It Practical And Concise</h2>
<p>Short, specific briefs are more useful than long sales-style descriptions. The point is to understand the project, the stage it has reached, and the kind of specialist help likely to matter once coverage is ready.</p>
</section>

<section>
<span class="eyebrow">Request form</span>
<h2>Project Interest Form</h2>
{form}
</section>
"""


def build_find_help_homeowner_success_page() -> str:
    return f"""
<section class="hero" data-find-help-page="homeowner-success">
<span class="badge">Request received</span>
<h1>Your Project Interest Has Been Recorded</h1>
<p>Thank you for registering your project. Find Help is still expanding carefully, so this confirmation does not mean live matching is already active for every category or area.</p>
</section>

<section>
<span class="eyebrow">What happens next</span>
<h2>Coverage Is Still Being Assembled Carefully</h2>
<div class="answer-grid">
<div class="answer-card">
<h3>Request received</h3>
<p>Your project brief has been received and logged for review.</p>
</div>
<div class="answer-card">
<h3>Coverage is still limited</h3>
<p>{ROLL_OUT_NOTE}</p>
</div>
<div class="answer-card">
<h3>Possible follow-up</h3>
<p>You may be contacted once relevant coverage is available for your project type and area.</p>
</div>
</div>
<div class="hero-ctas">
<a class="btn" href="/find-help/">Back to Find Help</a>
<a class="btn button-secondary" href="/find-help/trust/">Read trust principles</a>
</div>
</section>
"""


def build_find_help_specialists_page() -> str:
    groups = [
        "Planning consultants",
        "Architectural technologists",
        "Residential architects",
        "Residential drawing and package providers",
    ]
    return f"""
<section class="hero" data-find-help-page="specialists">
<span class="badge">Find Help for specialists</span>
<h1>Apply To Join A Carefully Reviewed Specialist Network</h1>
<p>UK Planning Guide is building a vetted network of specialists for homeowners who have already narrowed the planning question and need the right next kind of practical help. This is curated and selective, not an open directory.</p>
<div class="last-updated">Updated {get_month_year()}</div>
</section>

<section class="notice">
<span class="eyebrow">How applications are handled</span>
<h2>Manual Review Before Scale</h2>
<p>Applications are reviewed manually. The aim is to assemble a relevant homeowner-focused network where quality, clarity and fit matter more than volume.</p>
</section>

<section>
<span class="eyebrow">Who this is for</span>
<h2>Specialist Types Currently In Scope</h2>
<ul class="checklist">{''.join(f"<li>{escape(group)}</li>" for group in groups)}</ul>
</section>

<section>
<span class="eyebrow">Why it is selective</span>
<h2>Not An Open Directory</h2>
<div class="answer-grid">
<div class="answer-card">
<h3>Homeowner relevance first</h3>
<p>The network is being built around the kinds of support homeowners actually need at the moment a project moves beyond general guidance.</p>
</div>
<div class="answer-card">
<h3>Manual review</h3>
<p>Applications are screened manually because a smaller, clearer network is more useful than scale for its own sake.</p>
</div>
<div class="answer-card">
<h3>Careful expansion</h3>
<p>Coverage will expand carefully by category and area rather than being rushed into a noisy all-at-once launch.</p>
</div>
</div>
<div class="hero-ctas">
<a class="btn" href="/find-help/specialists/apply/">Apply as a specialist</a>
<a class="btn button-secondary" href="/find-help/trust/">Read trust principles</a>
</div>
</section>
"""


def build_find_help_specialist_apply_page() -> str:
    form = _render_form(
        SPECIALIST_APPLICATION_FIELDS,
        action="/find-help/specialists/apply/success/",
        submit_label="Submit specialist application",
        form_key="specialist-application",
    )
    return f"""
<section class="hero" data-find-help-page="specialist-apply">
<span class="badge">Specialist application</span>
<h1>Apply For Manual Review</h1>
<p>Use this form if you are applying to join the early UK Planning Guide specialist network. Applications are reviewed manually and the service is being assembled carefully rather than opened as a public directory.</p>
<div class="last-updated">Updated {get_month_year()}</div>
</section>

<section class="notice">
<span class="eyebrow">Before you apply</span>
<h2>Clarity Beats Volume</h2>
<p>Keep your application focused on the homeowner work you genuinely handle well, the areas you really cover, and why your service approach is a good fit for a careful homeowner-first network.</p>
</section>

<section>
<span class="eyebrow">Application form</span>
<h2>Specialist Application Form</h2>
{form}
</section>
"""


def build_find_help_specialist_success_page() -> str:
    return f"""
<section class="hero" data-find-help-page="specialist-success">
<span class="badge">Application received</span>
<h1>Your Application Has Been Received</h1>
<p>Thank you for applying. The network is being assembled carefully, and applications are reviewed manually rather than admitted automatically.</p>
</section>

<section>
<span class="eyebrow">What happens next</span>
<h2>Manual Review, Then Selective Follow-Up</h2>
<div class="answer-grid">
<div class="answer-card">
<h3>Application received</h3>
<p>Your application is now part of the review queue.</p>
</div>
<div class="answer-card">
<h3>Reviewed manually</h3>
<p>Quality, transparency and homeowner fit are reviewed before any expansion decisions are made.</p>
</div>
<div class="answer-card">
<h3>Selective contact</h3>
<p>Only selected applicants may be contacted as the network is built out by category and area.</p>
</div>
</div>
<div class="hero-ctas">
<a class="btn" href="/find-help/">Back to Find Help</a>
<a class="btn button-secondary" href="/find-help/trust/">Read trust principles</a>
</div>
</section>
"""


def build_find_help_how_it_works_page() -> str:
    steps = [
        "Tell us about your project.",
        "We review the brief.",
        "We identify a small number of suitable local specialists.",
        "You compare clearly.",
        "You choose what to do next.",
    ]
    return f"""
<section class="hero" data-find-help-page="how-it-works">
<span class="badge">How it will work</span>
<h1>The Intended Future Matching Flow</h1>
<p>This page explains the intended service shape once coverage is ready. It is not a claim that live matching is already fully active across all categories and areas.</p>
<div class="last-updated">Updated {get_month_year()}</div>
</section>

<section class="notice">
<span class="eyebrow">Service status</span>
<h2>Future Flow, Careful Expansion</h2>
<p>{ROLL_OUT_NOTE}</p>
</section>

<section>
<span class="eyebrow">Planned sequence</span>
<h2>Five Steps, Built To Stay Clear</h2>
<div class="steps-grid">
{''.join(f"<div class='mini-card'><strong>Step {index}</strong><p>{escape(step)}</p></div>" for index, step in enumerate(steps, start=1))}
</div>
</section>

<section>
<span class="eyebrow">Why the flow stays small</span>
<h2>Shortlists Instead Of Marketplace Noise</h2>
<div class="answer-grid">
<div class="answer-card">
<h3>Review before routing</h3>
<p>The brief is meant to be reviewed before any specialist introduction so the shortlist is shaped by project fit, not by whoever shouts loudest.</p>
</div>
<div class="answer-card">
<h3>Small number of matches</h3>
<p>The goal is a manageable comparison set where coverage exists, not an endless list with hidden ranking tricks.</p>
</div>
<div class="answer-card">
<h3>Homeowner control</h3>
<p>The homeowner should be able to compare clearly and then decide what to do next without being pushed into a rushed quote funnel.</p>
</div>
</div>
</section>
"""


def build_find_help_trust_page() -> str:
    principles = [
        "Small curated matches, not endless directories.",
        "No hidden ranking tricks.",
        "Project fit over volume.",
        "Specialist applications reviewed manually.",
        "Quality and clarity before scale.",
        "Careful expansion by category and area.",
    ]
    return f"""
<section class="hero" data-find-help-page="trust">
<span class="badge">Trust and fairness</span>
<h1>How Find Help Tries To Stay Clear, Selective And Honest</h1>
<p>Find Help is meant to be a calm escalation path after planning guidance, not a noisy quote funnel. This page explains the rules the service is built around and the limits that still matter while coverage is being assembled.</p>
<div class="last-updated">Updated {get_month_year()}</div>
</section>

<section>
<span class="eyebrow">Core principles</span>
<h2>The Service Is Being Built Around These Rules</h2>
<ul class="checklist">{''.join(f"<li>{escape(item)}</li>" for item in principles)}</ul>
</section>

{build_trust_framework(
    section_id="find-help-principles",
    title="How Find Help Builds Trust Without Overclaiming",
    purpose="To explain when Find Help is the right next step, how matching is meant to work where coverage exists, and why the service stays selective instead of pretending to be a universal marketplace.",
    not_replace="It does not replace choosing your own adviser carefully, checking credentials directly, or taking formal council or specialist input where the project already needs it.",
    built_from="The service is designed around structured project briefs, manual specialist review, homeowner-first fit and clear coverage limits by category and area.",
    verify_when="Treat the coverage note seriously. If coverage is not in place for the project or area, the safer next move is still the direct council or professional route rather than waiting for a matching promise that has not been made.",
    safest_next_step="Use the homeowner request route when you want to register demand for a careful match. Use the specialist route when you want to apply for review. Use direct formal help immediately when the project cannot wait for coverage to expand.",
    support_links=[
        ('Find Help hub', '/find-help/'),
        ('Homeowner requests', '/find-help/homeowners/request/'),
        ('Specialist applications', '/find-help/specialists/apply/'),
    ],
)}

<section>
<span class="eyebrow">What is already in place</span>
<h2>How The Pre-Launch System Is Being Kept Careful</h2>
<div class="answer-grid">
<div class="answer-card">
<h3>Structured project briefs</h3>
<p>Homeowner requests are being gathered in a consistent format so the service can review project type, stage, local sensitivity and timing without turning the process into a noisy directory search.</p>
</div>
<div class="answer-card">
<h3>Manual specialist review</h3>
<p>Applications are being collected in a structured way so specialist fit, service clarity, coverage and homeowner relevance can be reviewed properly before the network expands.</p>
</div>
<div class="answer-card">
<h3>Staged expansion</h3>
<p>The network can expand carefully by category and area because project demand and specialist coverage are being assembled in a way that supports selective matching rather than rushed scale.</p>
</div>
</div>
</section>
"""
