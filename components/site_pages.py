from data.promoted_links import ABOUT_NEXT_STEP_KEYS, METHODOLOGY_ENTRY_POINT_KEYS, PROMOTED_LINKS
from components.page_authority import build_authority_summary_section
from components.personalised_guidance import build_personalised_guidance_cta
from components.trust_framework import build_trust_framework
from data.loaders import load_councils
from utils.official_sources import OfficialSourceContext, relevant_official_sources
from utils.random_tools import get_month_year


def _render_promoted_cards(keys) -> str:
    return "".join(
        f"""
<a class="card" href="{PROMOTED_LINKS[key]['href']}">
<div class="card-kicker">Useful next step</div>
<h3>{PROMOTED_LINKS[key]['title']}</h3>
<p>{PROMOTED_LINKS[key]['description']}</p>
<span class="cta">{PROMOTED_LINKS[key]['cta']}</span>
</a>
"""
        for key in keys
    )


def build_about_page() -> str:
    return (
        f"""
<section class="hero">
<span class="badge">About UK Planning Guide</span>
<h1 id="sam-jones">Why I Built This Site</h1>
<p>Hi, I'm Sam Jones. I built UK Planning Guide after having a frustrating experience trying to work through planning permission for a few projects of my own. What should have felt like a straightforward early-stage check often felt confusing, slow and much harder to navigate than it needed to be.</p>
<div class="last-updated">Updated {get_month_year()}</div>
</section>

<section>
<span class="eyebrow">The short version</span>
<h2>The Site I Wanted To Find When I Was Stuck</h2>
<div class="answer-grid">
<div class="answer-card">
<h3>What I ran into</h3>
<p>I found it surprisingly difficult to get clear, practical answers at the point where you are just trying to work out the likely route before paying for drawings, applications or specialist advice.</p>
</div>
<div class="answer-card">
<h3>Why this site exists</h3>
<p>I built the site to explain planning questions in plain English, show what usually changes the answer locally and make the next sensible check much easier to spot.</p>
</div>
<div class="answer-card">
<h3>What it does not claim</h3>
<p>It is not a council, a law firm or a substitute for formal planning confirmation. The aim is to give people a practical, trustworthy starting point rather than pretend every case can be settled by one article.</p>
</div>
</div>
</section>

<section>
<h2>What I Am Trying To Make Easier</h2>
<div class="grid">
<div class="mini-card">
<h3>Plain-English Starting Points</h3>
<p>The site is meant to help when you know the project you want to do but do not yet know whether the planning route looks simple, borderline or obviously more sensitive.</p>
</div>
<div class="mini-card">
<h3>Earlier Warning Signs</h3>
<p>The goal is to show the local tripwires earlier, especially where conservation areas, Article 4, listed buildings, planning history or site-specific details may change the answer.</p>
</div>
<div class="mini-card">
<h3>Better Next Decisions</h3>
<p>I want the site to help people avoid wasting time, money and energy by taking the wrong next step too early, whether that means overcommitting to drawings or assuming a project is simpler than it is.</p>
</div>
</div>
</section>

<section>
<span class="eyebrow">How to use it well</span>
<h2>What The Site Helps With, And Where To Be Careful</h2>
<div class="answer-grid">
<div class="answer-card">
<h3>Start with the real question</h3>
<p>Use the project guides when the build type is clear, the rule hubs when one planning issue is the blocker, and the local pages when authority context may change the route.</p>
</div>
<div class="answer-card">
<h3>Use it to narrow the route</h3>
<p>The site works best as a practical first pass: a way to understand what usually applies, what may complicate it locally and what you should verify before spending more money.</p>
</div>
<div class="answer-card">
<h3>Know when to stop</h3>
<p>If your answer depends on exact measurements, planning history, heritage controls or a high-stakes judgement call, the safer move is formal confirmation or specialist input.</p>
</div>
</div>
</section>

"""
        + build_authority_summary_section(
            section_id="about-authority",
            title="Who Is Accountable For The Guidance",
            intro="The site is meant to feel clearly owned and clearly limited. My name is on it because I want the guidance to feel human and accountable, with visible review and clear reminders about when a formal route is safer.",
        )
        + """

<section>
<h2>Standards I Want The Site To Hold</h2>
<ul class="checklist">
<li>No invented qualifications, case studies, testimonials or review claims.</li>
<li>No attempt to make a borderline scheme sound more certain than it is.</li>
<li>No attempt to hide where local authority confirmation or formal help is the safer next step.</li>
</ul>
</section>

"""
        + build_trust_framework(
            section_id="about-trust",
            title="How Trust Is Earned Here",
            purpose="To help users get a practical first answer, understand what usually changes that answer, and decide when to keep using guidance versus when to verify the route formally.",
            not_replace="This site does not replace a council decision, a lawful development certificate, pre-application advice, or paid specialist input where the property, design or planning history makes the answer genuinely delicate.",
            built_from="Pages are built from the national planning baseline, local authority context where available, and the practical tripwires that tend to catch people out early, such as heritage controls, boundaries, previous additions and use questions.",
            verify_when="Stop relying on broad guidance once the proposal is close to a limit, sits on a sensitive site, or depends on an assumption that would be expensive to get wrong later.",
            safest_next_step="Use a lawful development certificate when a scheme appears lawful but certainty matters. Use pre-application advice when local interpretation, design judgement or planning history are doing most of the work.",
            support_links=[
                ("Methodology", "/methodology/"),
                ("Personalised planning guidance", "/personalised-planning-guidance/"),
            ],
        )
        + """

"""
        + build_personalised_guidance_cta(
            title="Need The Site Method Applied To Your Own Case?",
            description="If the broad route is now clear but the live answer still depends on your property, drawings, local sensitivity or planning history, use the personalised guidance route for a more specific informational steer.",
            context_label="about-page",
            email_context="about page",
            compact=True,
        )
        + """

<section>
<h2>Best Next Pages</h2>
<div class="grid">"""
        + _render_promoted_cards(ABOUT_NEXT_STEP_KEYS)
        + """
</div>
</section>
"""
    )


def build_methodology_page() -> str:
    return (
        f"""
<section class="hero">
<span class="badge">Methodology</span>
<h1>How UK Planning Guide Builds Its Guidance</h1>
<p>The site keeps three jobs separate: the national planning baseline, the local authority layer and the point where broad guidance stops being enough on its own. That separation is what keeps the content useful without overclaiming certainty.</p>
<div class="last-updated">Updated {get_month_year()}</div>
</section>

<section>
<span class="eyebrow">Method in plain English</span>
<h2>How The Guidance Is Built And Why The Layers Stay Deliberately Separate</h2>
<div class="answer-grid">
<div class="answer-card">
<h3>National baseline first</h3>
<p>Project guides start with the planning position that commonly applies nationally, including the usual permitted development principles, thresholds and common route questions.</p>
</div>
<div class="answer-card">
<h3>Local layer second</h3>
<p>Local project, council and area pages then layer in authority context such as conservation areas, listed building controls, Article 4, local policy pressure and council-specific friction points.</p>
</div>
<div class="answer-card">
<h3>Rule page when needed</h3>
<p>Scenario hubs and rule pages isolate the one issue that is actually blocking progress, such as height, boundary position, conservation-area effect or whether permitted development still survives.</p>
</div>
</div>
</section>

<section>
<h2>Editorial And Source Standards</h2>
<ul class="checklist">
<li>Pages should answer a real planning question in plain English.</li>
<li>Tools should improve the next decision, not just create another click.</li>
<li>FAQ pages should cover process, restrictions and verification points people genuinely get stuck on.</li>
<li>Where an answer depends on measurements, planning history or special controls, the page should say so plainly.</li>
</ul>
</section>

"""
        + build_authority_summary_section(
            section_id="methodology-authority",
            title="Who Writes And Reviews The Method",
            intro="Authority here should come from visible accountability, clear official sources and honest escalation points rather than vague expert language.",
        )
        + """

<section>
<h2>What Users Should Still Verify Before They Spend Money</h2>
<ul class="checklist">
<li>Exact dimensions, overall site coverage and roof heights.</li>
<li>Whether previous extensions or outbuildings have already used development allowances.</li>
<li>Whether the property is listed, in a conservation area or affected by an Article 4 direction.</li>
<li>Whether a separate consent is needed, such as listed building consent, highway approval or building regulations approval.</li>
</ul>
<p>If a proposal is close to a limit or there is any doubt about the planning route, a lawful development certificate or pre-application advice is usually more valuable than relying on assumptions.</p>
</section>

"""
        + build_trust_framework(
            section_id="methodology-trust",
            title="How The Method Signals Trust Without Pretending To Be Final",
            purpose="To show where the likely baseline comes from, what local factors usually move it, and which page or formal route is safest once the answer stops being routine.",
            not_replace="The method does not replace the local planning authority record, official designation checks, or formal specialist input where site-specific evidence and design judgement are doing most of the work.",
            built_from="The site works from the national baseline first, layers in local authority context second, and then adds page-specific tripwires such as height, siting, use intensity, heritage sensitivity and previous additions.",
            verify_when="Escalate once the route depends on a tight measurement, a sensitive designation, an uncertain planning history or an interpretation you would not want to defend after money has been spent.",
            safest_next_step="Use a lawful development certificate when certainty matters around an apparently lawful scheme. Use pre-application advice when the council's planning judgement is likely to matter more than the headline rule.",
            support_links=[
                ("About", "/about/"),
                ("Planning FAQ", "/planning-faq/"),
                ("Personalised planning guidance", "/personalised-planning-guidance/"),
            ],
        )
        + """

"""
        + build_personalised_guidance_cta(
            title="Want The Method Applied To A Specific Project?",
            description="The methodology explains how the site reasons about planning risk. If you want that logic applied to your own facts, the personalised guidance route is the cleanest next step.",
            context_label="methodology-page",
            email_context="methodology page",
            compact=True,
        )
        + """

<section>
<h2>Useful Entry Points</h2>
<div class="grid">"""
        + _render_promoted_cards(METHODOLOGY_ENTRY_POINT_KEYS)
        + """
</div>
</section>
"""
    )


def build_editorial_policy_page() -> str:
    return (
        f"""
<section class="hero">
<span class="badge">Editorial policy</span>
<h1>How UK Planning Guide Handles Authorship, Review And Updates</h1>
<p>This policy exists to make the site easier to trust. It explains who writes the guidance, how pages are reviewed, how official sources are used and where the site deliberately stops short of pretending to be a formal decision-maker.</p>
<div class="last-updated">Updated {get_month_year()}</div>
</section>

"""
        + build_authority_summary_section(
            section_id="editorial-policy-authority",
            title="Visible Ownership And Review",
            intro="Pages should show who wrote them, who reviewed them, which official sources they rely on and what kind of case still needs a stronger formal route.",
        )
        + """

<section>
<span class="eyebrow">Editorial standards</span>
<h2>What The Site Tries To Do Consistently</h2>
<ul class="checklist">
<li>Keep the national planning baseline separate from the local authority layer.</li>
<li>Use official sources where they actually ground the next decision.</li>
<li>Avoid making borderline schemes sound more certain than they are.</li>
<li>Surface when a lawful development certificate, pre-application advice or specialist input is the safer move.</li>
</ul>
</section>

<section>
<span class="eyebrow">Update policy</span>
<h2>How Pages Are Reviewed And Updated</h2>
<div class="answer-grid">
<div class="answer-card">
<h3>Core pages</h3>
<p>Homepage, methodology, about, planning-permission hubs and the strongest local authority routes should be reviewed first whenever the trust or routing model changes.</p>
</div>
<div class="answer-card">
<h3>Priority local pages</h3>
<p>Pages already earning impressions are upgraded first, especially where stronger trust signals can help CTR and ranking without a full content rewrite.</p>
</div>
<div class="answer-card">
<h3>Change notes</h3>
<p>Priority pages should carry a short note when the authority footing, source basis or safer next-step wording changes materially.</p>
</div>
</div>
</section>

<section>
<span class="eyebrow">Important limits</span>
<h2>What This Policy Does Not Claim</h2>
<p>It does not claim that the site replaces council decisions, formal legal advice, architectural design advice or any regulated service. It is an accountability framework for practical planning guidance, not a substitute for the formal routes that still settle live cases.</p>
</section>

<section>
<span class="eyebrow">Visible trust signals</span>
<h2>What Priority Pages Should Show Clearly</h2>
<div class="answer-grid">
<div class="answer-card">
<h3>Visible ownership</h3>
<p>High-value pages should show who wrote them so the guidance feels clearly owned rather than system-generated.</p>
</div>
<div class="answer-card">
<h3>Visible review</h3>
<p>High-value pages should show when they were last reviewed and who checked the wording, official sources and escalation point.</p>
</div>
<div class="answer-card">
<h3>Visible official sources</h3>
<p>High-value pages should say which official source matters here and why it matters for this route, not just that an official source exists somewhere.</p>
</div>
</div>
</section>
"""
    )


def build_article4_hmo_reference_page() -> str:
    councils_by_county = load_councils()
    cards = []
    for county_slug, councils in councils_by_county.items():
        for council in councils:
            authority_slug = council["town_slug"]
            authority_name = council["town_name"]
            article4_sources = relevant_official_sources(
                OfficialSourceContext(
                    page_family="scenario",
                    authority_slug=authority_slug,
                    country_slug=council.get("country_slug", ""),
                    scenario_slug="article-4",
                    max_links=2,
                )
            )
            hmo_sources = relevant_official_sources(
                OfficialSourceContext(
                    page_family="project",
                    authority_slug=authority_slug,
                    country_slug=council.get("country_slug", ""),
                    project_slug="hmos",
                    max_links=2,
                )
            )
            if not article4_sources and not hmo_sources:
                continue
            evidence_bits = []
            if article4_sources:
                evidence_bits.append("Article 4 source available")
            if hmo_sources:
                evidence_bits.append("HMO route source available")
            cards.append(
                f"""
<a class="card" href="/councils/{authority_slug}/">
<div class="card-kicker">Council reference</div>
<h3>{authority_name}</h3>
<p>{", ".join(evidence_bits)}. Use the council guide first, then open the HMO or Article 4 page if the property-level fallback still needs checking.</p>
<span class="cta">Open authority guide</span>
</a>
"""
            )

    return f"""
<section class="hero">
<span class="badge">Authority reference asset</span>
<h1>Article 4 And HMO By Council</h1>
<p>This reference page exists for the local-intent queries where the live issue is not just whether Article 4 exists, but whether it changes the HMO route in the exact authority you care about.</p>
<div class="last-updated">Updated {get_month_year()}</div>
</section>

{build_authority_summary_section(
    section_id="article4-hmo-authority",
    title="Why This Reference Page Exists",
    intro="Article 4 and HMO searches are highly local. The safest route is to show the authority layer, the official sources and the exact point where a property-level check is still needed.",
    include_placeholder_note=False,
)}

<section>
<span class="eyebrow">How to use it</span>
<h2>What This Asset Is Trying To Do Well</h2>
<div class="answer-grid">
<div class="answer-card">
<h3>What it helps with</h3>
<p>It helps you move from a broad HMO or Article 4 query into the right authority guide without pretending a district-wide mention settles the property-level answer.</p>
</div>
<div class="answer-card">
<h3>What usually changes the route</h3>
<p>The live issue is usually whether Article 4 removes the fallback for the exact property, and whether local policy pressure or concentration concerns push the HMO route into a fuller planning check.</p>
</div>
<div class="answer-card">
<h3>When to verify formally</h3>
<p>Verify formally when the simpler route only works if Article 4 does not apply to the exact property, or when the financial consequences of being wrong are meaningful.</p>
</div>
</div>
</section>

<section>
<span class="eyebrow">Authority references</span>
<h2>Council Pages With Article 4 Or HMO Official Sources</h2>
<p class="section-lead">These links are the quickest route into the authorities where the dataset already surfaces official sources for Article 4, HMO route questions or both.</p>
<div class="grid">{''.join(cards[:60])}</div>
</section>
"""


WORKFLOW_PAGES = [
    {
        "slug": "house-extension-planning",
        "title": "House Extension Planning Workflow",
        "meta": "Use a step-by-step house extension planning workflow covering rules, local constraints, drawings, certificates and application readiness.",
        "project": "House extension",
        "tool_href": "/tools/project-roadmap-builder/",
        "primary_href": "/house-extensions/",
        "secondary_href": "/tools/planning-task-checklist-builder/",
        "risk": "depth, height, boundary position, previous additions and local restrictions",
    },
    {
        "slug": "garden-room-planning",
        "title": "Garden Room Planning Workflow",
        "meta": "Use a garden room planning workflow to check use, height, boundaries, local constraints and whether formal proof is sensible.",
        "project": "Garden room",
        "tool_href": "/tools/evidence-pack-builder/",
        "primary_href": "/garden-rooms/",
        "secondary_href": "/tools/local-constraint-finder/",
        "risk": "height, incidental use, boundary position, land coverage and local restrictions",
    },
    {
        "slug": "loft-conversion-planning",
        "title": "Loft Conversion Planning Workflow",
        "meta": "Use a loft conversion planning workflow covering roof changes, volume, local sensitivity, drawings and proof routes.",
        "project": "Loft conversion",
        "tool_href": "/tools/project-roadmap-builder/",
        "primary_href": "/loft-conversions/",
        "secondary_href": "/tools/drawings-cost-readiness-checker/",
        "risk": "roof visibility, volume, front-facing changes, property type and local controls",
    },
    {
        "slug": "dropped-kerb-planning",
        "title": "Dropped Kerb Planning Workflow",
        "meta": "Use a dropped kerb planning workflow to separate planning, highway approval, frontage, drainage and evidence checks.",
        "project": "Dropped kerb",
        "tool_href": "/tools/planning-timeline-planner/",
        "primary_href": "/dropped-kerbs/",
        "secondary_href": "/tools/evidence-pack-builder/",
        "risk": "highway approval, frontage layout, drainage, visibility and local process",
    },
    {
        "slug": "hmo-article-4-check",
        "title": "HMO Article 4 Check Workflow",
        "meta": "Use an HMO Article 4 workflow to check local directions, HMO planning routes, licensing context and official council sources.",
        "project": "HMO or change of use",
        "tool_href": "/tools/local-constraint-finder/",
        "primary_href": "/article-4-hmo-by-council/",
        "secondary_href": "/tools/planning-route-planner/",
        "risk": "Article 4 coverage, use class, local policy pressure, HMO licensing and property-level evidence",
    },
    {
        "slug": "conservation-area-project",
        "title": "Conservation Area Project Workflow",
        "meta": "Use a conservation area planning workflow to check heritage sensitivity, visible changes, evidence and council-source verification.",
        "project": "Conservation area project",
        "tool_href": "/tools/local-constraint-finder/",
        "primary_href": "/conservation-areas/",
        "secondary_href": "/tools/evidence-pack-builder/",
        "risk": "heritage sensitivity, visible change, Article 4 overlap, demolition and design judgement",
    },
]


def _workflow_card(page: dict) -> str:
    return f"""
<a class="card" href="/workflows/{page['slug']}/">
<div class="card-kicker">Workflow</div>
<h3>{page['title']}</h3>
<p>Use the {page['project'].lower()} route to move from broad research into saved tasks, evidence and the next check worth doing.</p>
<span class="cta">Open workflow</span>
</a>
"""


def build_my_planning_project_page() -> str:
    return f"""
<section class="hero">
<span class="badge">My Planning Project</span>
<h1>Pick Up The Planning Work Without Starting Again</h1>
<p>Save useful guides, tool results and next tasks in this browser only. No account is created, and nothing is sent anywhere unless you choose to submit a form.</p>
<div class="last-updated">Updated {get_month_year()}</div>
</section>

<div data-workspace-page="true">
<section>
<span class="eyebrow">Loading workspace</span>
<h2>Your Saved Planning Workspace</h2>
<p class="section-lead">If you have saved pages or tool results on this device, they will appear here once the page loads.</p>
</section>
</div>

<section>
<span class="eyebrow">Useful workflow tools</span>
<h2>Build A Project Route You Can Return To</h2>
<div class="grid">
<a class="card" href="/tools/project-roadmap-builder/"><div class="card-kicker">Workflow tool</div><h3>Project Roadmap Builder</h3><p>Build the staged route for your project before committing to drawings or application prep.</p><span class="cta">Build roadmap</span></a>
<a class="card" href="/tools/planning-task-checklist-builder/"><div class="card-kicker">Workflow tool</div><h3>Planning Task Checklist Builder</h3><p>Create a checklist you can save, print and work through across several visits.</p><span class="cta">Build checklist</span></a>
<a class="card" href="/tools/evidence-pack-builder/"><div class="card-kicker">Workflow tool</div><h3>Evidence Pack Builder</h3><p>List the photos, measurements, official checks and drawings most likely to matter next.</p><span class="cta">Build evidence pack</span></a>
</div>
</section>
"""


def build_workflows_index_page() -> str:
    cards = "".join(_workflow_card(page) for page in WORKFLOW_PAGES)
    return f"""
<section class="hero">
<span class="badge">Planning workflows</span>
<h1>Planning Workflows For Projects That Take More Than One Visit</h1>
<p>Use these workflows when the real job is not just reading one guide, but keeping the route, local checks, evidence and next tasks together until the project is clearer.</p>
<div class="last-updated">Updated {get_month_year()}</div>
</section>

<section>
<span class="eyebrow">Workflow library</span>
<h2>Choose The Route That Matches The Project</h2>
<div class="grid">{cards}</div>
</section>
"""


def build_workflow_page(page: dict) -> str:
    return f"""
<section class="hero">
<span class="badge">Planning workflow</span>
<h1>{page['title']}</h1>
<p>Use this workflow to move from a broad {page['project'].lower()} question into saved checks, local constraints, evidence and the next route decision worth making.</p>
<div class="last-updated">Updated {get_month_year()}</div>
</section>

<section>
<span class="eyebrow">Answer first</span>
<h2>The Useful Order For This Project</h2>
<div class="answer-grid">
<div class="answer-card">
<h3>1. Check the project route</h3>
<p>Start with the core project guide so the usual planning route, permitted development limits and common tripwires are clear.</p>
</div>
<div class="answer-card">
<h3>2. Check the local layer</h3>
<p>Do not rely on the broad rule until you have checked {page['risk']} for the exact property or authority area.</p>
</div>
<div class="answer-card">
<h3>3. Save the next action</h3>
<p>Use a workflow tool to save the result, add a task, print the pack or copy a summary before spending money.</p>
</div>
</div>
</section>

<section>
<span class="eyebrow">Workflow actions</span>
<h2>Build The Route, Then Save It</h2>
<div class="grid">
<a class="card" href="{page['tool_href']}"><div class="card-kicker">Start workflow</div><h3>Build the project route</h3><p>Use the most relevant workflow tool for this project and save the output into My Planning Project.</p><span class="cta">Open tool</span></a>
<a class="card" href="{page['primary_href']}"><div class="card-kicker">Core guide</div><h3>Read the main project guide</h3><p>Use the project guide to understand the baseline before checking local constraints.</p><span class="cta">Open guide</span></a>
<a class="card" href="{page['secondary_href']}"><div class="card-kicker">Follow-up check</div><h3>Pressure-test the next step</h3><p>Use this when the answer depends on evidence, drawings, route timing or local constraints.</p><span class="cta">Run check</span></a>
<button class="next-step-card next-step-card-button" type="button" data-project-action="save-page"><span class="card-kicker">Save</span><strong>Save this workflow</strong><span>Keep this page in My Planning Project so you can come back later.</span><em>Save page</em></button>
</div>
</section>

<section>
<span class="eyebrow">Where people get stuck</span>
<h2>What Usually Changes The Route</h2>
<p>For a {page['project'].lower()}, the answer often changes once {page['risk']} become site-specific rather than generic. Treat those as checks to complete, not details to leave until the end.</p>
<p>Where the result is borderline, use official council sources, a lawful development certificate, pre-application advice or suitable professional input rather than assuming the shortcut applies.</p>
</section>

{build_trust_framework(
    title="How To Use This Workflow Safely",
    purpose="To turn a broad planning question into a sequence of useful checks, saved tasks and evidence-gathering steps.",
    not_replace="This workflow does not replace official council confirmation, a lawful development certificate, pre-application advice or specialist input where the exact property decides the answer.",
    built_from="It combines the existing UK Planning Guide project, rule, local authority and tool layers into a more return-friendly route.",
    verify_when="Verify formally when the project is close to a limit, locally restricted, heritage-sensitive or expensive to get wrong.",
    safest_next_step="Use the workflow tool first, then open the core guide and council layer before committing to drawings or application preparation.",
    support_links=[("My Planning Project", "/my-planning-project/"), ("Planning tools", "/tools/")],
)}
"""
