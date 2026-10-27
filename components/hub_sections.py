from components.editorial_authority import build_editorial_authority_block
from components.download_assets import render_download_asset_cards_for_path
from components.planning_route_check import build_planning_route_check_cta, should_show_route_check_project_cta
from data.download_assets import assets_for_source_path
from data.promoted_links import PROMOTED_LINKS


PROJECT_TYPE_TOPICS = {
    "extension": [
        ("Planning Permission", "/planning-permission/"),
        ("Permitted Development", "/permitted-development/"),
        ("Depth Limits", "/depth-limits/"),
        ("Height Limits", "/height-limits/"),
    ],
    "loft": [
        ("Permitted Development", "/permitted-development/"),
        ("Roof Alterations", "/roof-alterations/"),
        ("Depth Limits", "/depth-limits/"),
        ("Height Limits", "/height-limits/"),
    ],
    "outbuilding": [
        ("Permitted Development", "/permitted-development/"),
        ("Depth Limits", "/depth-limits/"),
        ("Boundary Rules", "/boundary-rules/"),
        ("Maximum Height", "/maximum-height/"),
    ],
    "conversion": [
        ("Planning Permission", "/planning-permission/"),
        ("Permitted Development", "/permitted-development/"),
        ("Depth Limits", "/depth-limits/"),
        ("Boundary Rules", "/boundary-rules/"),
    ],
    "external": [
        ("Planning Permission", "/planning-permission/"),
        ("Depth Limits", "/depth-limits/"),
        ("Boundary Rules", "/boundary-rules/"),
        ("Conservation Areas", "/conservation-areas/"),
    ],
    "microgeneration": [
        ("Planning Permission", "/planning-permission/"),
        ("Permitted Development", "/permitted-development/"),
        ("Conservation Areas", "/conservation-areas/"),
        ("Listed Buildings", "/listed-buildings/"),
    ],
}

PROJECT_HUB_OVERRIDES = {
    "garden-rooms": {
        "hero_title": "Garden Room Planning Permission",
        "hero_intro": "The key question with a garden room is whether it still reads as incidental to the house, stays within the usual outbuilding-style limits and remains comfortable once local restrictions are added back in.",
        "usual": "Many garden rooms follow the simpler outbuilding route when they remain incidental to the house, stay within the usual height and siting limits and do not drift into self-contained living space.",
        "changes": "Sleeping use, year-round independent occupation, excessive height, forward siting and high site coverage are the main reasons the answer hardens.",
        "safest_next_step": "Settle the incidental-use question first, then check height and boundary siting before you spend money on a larger or more serviced garden-room design.",
        "evidence": [
            "A simple plan showing where the garden room sits relative to the house, boundaries and the principal elevation.",
            "The intended use in plain English, especially if the room could be read as separate living accommodation.",
            "The overall garden coverage after the structure is added, not just the new footprint in isolation.",
        ],
        "thresholds": [
            ("Incidental use", "The easier route depends on the room staying clearly subordinate to the main house rather than acting like a separate dwelling or annexe."),
            ("Height and boundaries", "Boundary-adjacent height, overall ridge height and roof form are the measurements most likely to change the answer quickly."),
            ("Position within the plot", "Forward-of-principal-elevation siting and cramped rear-garden layouts are common reasons the project stops looking routine."),
            ("Local controls", "Conservation areas, listed buildings and Article 4 directions can narrow the normal fallback even when the structure looks modest."),
        ],
        "faq_links": [
            ("Garden Room Planning Permission", "/planning-faq/garden-room-planning-permission/", "Best for the broad planning question before you branch into local pages."),
            ("Garden Room Permitted Development", "/planning-faq/garden-room-permitted-development/", "Useful if the simpler route still looks plausible and you want the main limits in one place."),
            ("Do I Need Planning Permission?", "/planning-faq/do-i-need-planning-permission/", "Helpful if the question still is not specific to garden rooms."),
        ],
    },
    "house-extensions": {
        "hero_title": "House Extension Planning Permission",
        "hero_intro": "For most extensions, the real job is to separate the national baseline from the measurements, site history and local constraints that decide whether the simpler route still holds up.",
        "usual": "Many house extensions stay on the simpler route only when scale, height, depth, neighbour impact and site history all stay comfortably inside the normal envelope.",
        "changes": "Depth, height, width, boundary siting, previous additions and heritage controls are the checks most likely to push an extension into a fuller planning route.",
        "safest_next_step": "Measure the scheme against the original house first, then check neighbour relationship and previous additions before treating the easier route as settled.",
        "evidence": [
            "Measured drawings showing projection, height, roof form and relationship to the original house.",
            "A note of previous extensions or roof additions that may already have used permitted development allowances.",
            "Site photos that show frontage visibility, neighbour relationship and any heritage-sensitive context.",
        ],
        "thresholds": [
            ("Scale and projection", "Rear depth, side width and overall bulk usually decide whether an extension still looks routine."),
            ("Neighbour impact", "Loss of light, overbearing effect and awkward boundary siting are where many borderline schemes start to unravel."),
            ("Original house baseline", "The answer often turns on what counts as the original house and how much earlier development has already changed the position."),
            ("Local and heritage controls", "Conservation areas, listed status and council-specific design expectations can matter more than one headline national rule."),
        ],
        "faq_links": [
            ("Planning Permission For Extensions", "/planning-faq/planning-permission-for-extensions/", "Best for the broad extension route before you narrow down to a subtype."),
            ("Building Regulations For Extensions", "/planning-faq/building-regulations-for-extensions/", "Helpful when planning and technical approvals are getting mixed together."),
            ("What Drawings Do I Need For Planning Permission?", "/planning-faq/what-drawings-do-i-need-for-planning-permission/", "Useful once the extension may be heading toward a formal application or certificate."),
        ],
    },
    "temporary-buildings": {
        "hero_title": "Temporary Buildings Planning Permission",
        "hero_intro": "With temporary buildings, the label often sounds more helpful than it really is. What matters is whether the use, duration and physical setup still attract ordinary planning scrutiny.",
        "usual": "A building is not automatically easier just because it is described as temporary. The planning answer usually turns on purpose, duration, siting, services and how permanent the structure looks in practice.",
        "changes": "Long duration, fixed foundations, independent use, repeated occupation and sensitive sites are the reasons temporary structures often need a closer planning check.",
        "safest_next_step": "Write down the real duration, servicing and removal plan first, then test whether the structure still behaves like something genuinely temporary.",
        "evidence": [
            "A clear statement of how long the structure will stay on site and what event, project or operational need justifies it.",
            "The physical specification: foundations, services, anchoring and whether the building can realistically be removed cleanly.",
            "The use pattern, including whether people will sleep, work, store equipment or treat it as a normal building for an extended period.",
        ],
        "thresholds": [
            ("Duration and intention", "The longer the structure stays and the less credible the removal plan, the harder it is to treat it as genuinely temporary."),
            ("Physical permanence", "Foundations, utilities and substantial groundworks can make a 'temporary' structure look permanent in planning terms."),
            ("Use and intensity", "Operational use, independent occupation and high activity levels can change the route more than the label applied to the building."),
            ("Site sensitivity", "Heritage context, neighbour impact and enforcement risk make temporary-building assumptions much less safe."),
        ],
        "faq_links": [
            ("Temporary Buildings Planning Permission", "/planning-faq/temporary-buildings-planning-permission/", "Best for the broad planning question on temporary structures."),
            ("Temporary Buildings Building Regulations", "/planning-faq/temporary-buildings-building-regulations/", "Helpful when planning and technical compliance are getting mixed together."),
            ("What Counts As A Temporary Building?", "/planning-faq/what-counts-as-a-temporary-building/", "Useful when the live issue is whether the structure is temporary at all."),
        ],
    },
    "agricultural-buildings": {
        "hero_title": "Agricultural Building Planning Permission",
        "hero_intro": "Agricultural building cases usually turn on whether the agricultural route genuinely fits the holding and the proposal, or whether a fuller planning route is the more realistic reading from the start.",
        "usual": "Agricultural buildings often depend on whether the use is genuinely agricultural, whether the holding qualifies for the route being relied on and whether the proposal is really a new building, an operational structure or a conversion plan in disguise.",
        "changes": "Weak agricultural justification, mixed use, residential ambition, conversion plans and transport or neighbour impact are the reasons agricultural cases stop looking routine.",
        "safest_next_step": "Pressure-test the agricultural need first, then check whether access, scale or conversion intent is already pulling the scheme toward a different route.",
        "evidence": [
            "A plain-English explanation of the agricultural need, scale of the holding and how the building supports that use day to day.",
            "A clear distinction between a working agricultural structure, a fallback storage building and any hoped-for later conversion route.",
            "Site drawings showing access, siting, neighbouring properties and any landscape or heritage sensitivity.",
        ],
        "thresholds": [
            ("Real agricultural need", "The route is much weaker when the proposal looks speculative, mixed-use or only loosely connected to agriculture."),
            ("Permitted development or prior approval fit", "Agricultural cases often turn on whether the exact route being claimed is even available to the holding and the proposal."),
            ("Conversion intent", "A building sold as agricultural but designed around later residential or commercial conversion is likely to attract much closer scrutiny."),
            ("Local impact", "Landscape, highways, neighbour impact and heritage issues can matter even where an agricultural route exists in principle."),
        ],
        "faq_links": [
            ("Agricultural Building Permitted Development", "/planning-faq/agricultural-building-permitted-development/", "Best if the simpler agricultural route is the live issue."),
            ("Agricultural Building Conversion Planning Permission", "/planning-faq/agricultural-building-conversion-planning-permission/", "Helpful when the real question is conversion rather than a working agricultural building."),
            ("Prior Approval Vs Planning Permission", "/planning-faq/prior-approval-vs-planning-permission/", "Useful when the route may not be a straightforward full application."),
        ],
    },
}

PROJECT_HUB_FALLBACKS = {
    "extension": {
        "hero_intro": "Once the project type is clear, the next job is to separate the national baseline from the measurements and local constraints that usually decide the route.",
        "usual": "The simpler route usually survives only when the design stays comfortably inside the normal size, height and neighbour-impact envelope.",
        "changes": "Boundary siting, heritage controls, previous additions and borderline measurements are the checks most likely to push the route into doubt.",
        "thresholds": [
            ("Scale", "Keep the proposal comfortably within the normal size and projection envelope rather than merely close to it."),
            ("Neighbour impact", "Loss of light, overbearing effect and awkward boundary relationships are common reasons the route hardens."),
            ("Site history", "Previous additions can matter as much as the current design when you rely on the simpler route."),
            ("Local controls", "Conservation areas, listed status and council-specific design expectations can override broad assumptions quickly."),
        ],
    },
    "outbuilding": {
        "hero_intro": "With outbuilding-style projects, the important question is whether the structure still looks incidental, subordinate and comfortably within the normal envelope.",
        "usual": "The easier route usually depends on incidental use, comfortable siting and a structure that still reads as secondary to the main house.",
        "changes": "Sleeping use, independent occupation, high site coverage and awkward boundary or frontage siting are what usually change the answer.",
        "thresholds": [
            ("Use", "Incidental use is often the dividing line between the simpler route and a much harder planning question."),
            ("Height", "Height near boundaries is one of the first measurements to cause trouble."),
            ("Plot position", "Frontage impact and cramped siting can make a modest building look much less routine."),
            ("Local controls", "Heritage and local design controls make outbuilding assumptions less reliable."),
        ],
    },
}

OFFICIAL_CHECK_LINKS = [
    (
        "Planning Portal: do you need planning permission?",
        "https://www.planningportal.co.uk/permission/home-improvement/getting-started/do-you-need-planning-permission",
        "Use the official starter route when the basic permission question is still unresolved.",
    ),
    (
        "Planning Portal: permitted development rights",
        "https://www.planningportal.co.uk/permission/responsibilities/planning-permission/permitted-development-rights/",
        "Use the national baseline when the simpler route may still apply.",
    ),
    (
        "GOV.UK: before submitting an application",
        "https://www.gov.uk/guidance/before-submitting-an-application",
        "Use the official process guide before paying for a weak application package.",
    ),
]


def _card(title: str, description: str, href: str, cta: str, kicker: str = "") -> str:
    kicker_html = f"<div class='card-kicker'>{kicker}</div>" if kicker else ""
    return f"""
<a class="card" href="{href}">
{kicker_html}
<h3>{title}</h3>
<p>{description}</p>
<span class="cta">{cta}</span>
</a>
"""


def _jump_section(title: str, links: list[tuple[str, str]]) -> str:
    items = "".join(f'<a href="{href}">{label}</a>' for label, href in links)
    return f"""
<section class="page-jump-links">
<span class="eyebrow">Jump to what matters</span>
<h2>{title}</h2>
<div class="link-grid">{items}</div>
</section>
"""


def _project_hub_brief(project: dict) -> dict:
    project_type = project.get("type", "")
    fallback = PROJECT_HUB_FALLBACKS.get(project_type, PROJECT_HUB_FALLBACKS["extension"])
    override = PROJECT_HUB_OVERRIDES.get(project["slug"], {})
    safest_next_step = override.get(
        "safest_next_step",
        {
            "extension": "Settle the measurements against the original house first, then open the local page only if the scheme is still close to a live threshold.",
            "outbuilding": "Settle use, height and siting first, then go local if the structure is no longer obviously secondary to the house.",
            "loft": "Settle roof form, visibility and the main dimensions first, then go local if the route still looks borderline.",
            "microgeneration": "Settle siting, visibility and local sensitivity first, then go local if the equipment no longer looks routine.",
        }.get(
            project_type,
            "Settle the broad route first, then go local only if one authority, one restriction or one borderline measurement is still doing the real work.",
        ),
    )
    return {
        "hero_title": override.get("hero_title", project["title"]),
        "hero_intro": override.get("hero_intro", fallback["hero_intro"]),
        "usual": override.get("usual", fallback["usual"]),
        "changes": override.get("changes", fallback["changes"]),
        "safest_next_step": safest_next_step,
        "evidence": override.get(
            "evidence",
            [
                "Measured drawings or a sketch with the dimensions most likely to affect the route.",
                "Site photos showing neighbour relationship, frontage impact and anything visually sensitive.",
                "A note of local controls, planning history and the question you would actually want a council or consultant to answer.",
            ],
        ),
        "thresholds": override.get("thresholds", fallback["thresholds"]),
        "faq_links": override.get(
            "faq_links",
            [
                ("Do I Need Planning Permission?", "/planning-faq/do-i-need-planning-permission/", "Start broader if the route itself is still the main uncertainty."),
                ("Planning Permission Vs Permitted Development", "/planning-faq/planning-permission-vs-permitted-development/", "Helpful when the route split is still the live question."),
                ("Lawful Development Certificate", "/planning-faq/lawful-development-certificate/", "Useful when certainty matters before work starts."),
            ],
        ),
    }


def build_project_hub_content(project: dict, councils_by_county: dict, towns: list[dict]) -> str:
    project_slug = project["slug"]
    project_name = project["short_name"]
    brief = _project_hub_brief(project)
    related_topics = PROJECT_TYPE_TOPICS.get(project.get("type"), PROJECT_TYPE_TOPICS["extension"])
    editorial_block = build_editorial_authority_block(
        f"/{project_slug}/",
        page_family="hub",
        project_slug=project_slug,
    )

    featured_locals = []
    for town in towns[:10]:
        featured_locals.append(
            _card(
                f"{project_name} in {town['town_name']}",
                "Open a local page that starts with the normal route, then shows the local restriction signals and what to check next.",
                f"/{project_slug}/{town['county_slug']}/{town['town_slug']}/",
                "View local guide",
                "Curated local guide",
            )
        )
        if len(featured_locals) >= 8:
            break

    county_cards = []
    for county_slug, councils in councils_by_county.items():
        county_name = county_slug.replace("-", " ").title()
        county_cards.append(
            _card(
                county_name,
                f"Compare {project_name.lower()} guidance across {len(councils)} local authority areas in {county_name}, then drill into the right council page.",
                f"/{project_slug}/{county_slug}/",
                "Compare this area",
                "Area project hub",
            )
        )

    topic_cards = "".join(
        _card(
            title,
            f"Open this topic hub when the real blocker for {project_name.lower()} is {title.lower()}.",
            href,
            "Open topic",
            "Useful next rule",
        )
        for title, href in related_topics
    )

    tools = PROMOTED_LINKS["planning_decision_tool"]
    explorer_tool = PROMOTED_LINKS["what_can_i_build_explorer"]
    risk_tool = PROMOTED_LINKS["planning_rejection_risk_tool"]
    value_tool = PROMOTED_LINKS["extension_value_estimator"]
    route_tool = PROMOTED_LINKS["planning_route_planner"]
    requirements_tool = PROMOTED_LINKS["project_requirements_generator"]
    faq = PROMOTED_LINKS["faq_need_planning"]
    route_check_cta = (
        build_planning_route_check_cta(
            variant="b",
            source_page_type="project-hub",
            project_slug=project_slug,
            compact=True,
        )
        if should_show_route_check_project_cta(project_slug)
        else ""
    )
    extension_value_card = ""
    download_assets = render_download_asset_cards_for_path(
        f"/{project_slug}/",
        assets_for_source_path(f"/{project_slug}/"),
    )
    if project.get("type") in {"extension", "loft"}:
        extension_value_card = _card(
            value_tool["title"],
            "Estimate likely value uplift for this kind of project before relying on rough ROI claims or generic rules of thumb.",
            value_tool["href"],
            value_tool["cta"],
            "Value tool",
        )

    threshold_cards = "".join(
        _card(title, description, "#project-hub-counties", "Use local pages below", kicker="Threshold to keep in view")
        for title, description in brief["thresholds"]
    )
    evidence_items = "".join(f"<li>{item}</li>" for item in brief["evidence"])
    faq_cards = "".join(
        _card(title, description, href, "Open guide", kicker="Deeper evergreen guide")
        for title, href, description in brief["faq_links"]
    )
    official_cards = "".join(
        _card(title, description, href, "Open source", kicker="Official source")
        for title, href, description in OFFICIAL_CHECK_LINKS
    )

    return f"""
<section class="hero">
<span class="badge">Project planning hub</span>
<h1>{brief['hero_title']}</h1>
<p>{brief['hero_intro']}</p>
<div class="answer-grid">
<div class="answer-card">
<h3>Working position</h3>
<p>{brief['usual']}</p>
</div>
<div class="answer-card">
<h3>What changes it fastest</h3>
<p>{brief['changes']}</p>
</div>
<div class="answer-card">
<h3>Safest next step</h3>
<p>{brief['safest_next_step']}</p>
</div>
</div>
</section>

{editorial_block}

{route_check_cta}

{download_assets}

{_jump_section(
    "How To Use This Guide Efficiently",
    [
        ("Start with the broad answer and evidence checks", "#project-hub-overview"),
        ("Check the thresholds that most often change the route", "#project-hub-thresholds"),
        ("Open the deeper evergreen guides first", "#project-hub-faqs"),
        ("Compare the right planning area only if the local layer matters", "#project-hub-counties"),
    ],
)}

<section id="project-hub-overview">
<span class="eyebrow">Answer-first overview</span>
<h2>The Broad Planning Position, The Main Tripwires And The Evidence Worth Gathering</h2>
<div class="split-grid">
<div class="mini-card">
<h3>What to gather before you spend more</h3>
<ul class="checklist">{evidence_items}</ul>
</div>
<div class="cta-band">
<span class="eyebrow">Useful support tools</span>
<h3>Helpful while the route is still broad</h3>
<p>The tools are useful for an early steer. Once the project type is clear, the stronger move is usually one good guide and one good local page rather than more browsing.</p>
<div class="hero-ctas">
<a class="btn" href="/tools/planning-decision-tool/">Open the main tool</a>
<a class="btn button-secondary" href="/planning-faq/do-i-need-planning-permission/">Read the core route guide</a>
</div>
</div>
</div>
</section>

<section id="project-hub-thresholds">
<span class="eyebrow">Where projects tighten up</span>
<h2>Thresholds And Practical Checks Worth Treating Seriously</h2>
<div class="grid">{threshold_cards}</div>
</section>

<section id="project-hub-faqs">
<span class="eyebrow">Deeper evergreen guidance</span>
<h2>Start With These Broader Guides Before Going Hyper-Local</h2>
<p class="section-lead">These guides deal with the bigger planning questions first, so local pages only need to do the genuinely local work.</p>
<div class="grid">{faq_cards}</div>
</section>

<section id="project-hub-routes">
<span class="eyebrow">Fast route tools and comparisons</span>
<h2>Useful Once The Broad Rule Is Clear Enough To Name</h2>
<div class="grid">
{_card(explorer_tool['title'], "Use the explorer if you are still choosing between extensions, lofts, outbuildings and other project types.", explorer_tool['href'], explorer_tool['cta'], "Explorer")}
{_card(tools['title'], "Use the tool for a first-pass steer before you dive into the local project pages.", tools['href'], tools['cta'], "Tool")}
{extension_value_card}
{_card(route_tool['title'], "Use the route planner when the live question is which approval path or parallel consent is most likely to matter.", route_tool['href'], route_tool['cta'], "Route tool")}
{_card(requirements_tool['title'], "Use the requirements generator to turn the project into a practical prep pack before drawings or applications move further.", requirements_tool['href'], requirements_tool['cta'], "Prep tool")}
{_card(risk_tool['title'], "Use the risk analyzer when you want to see the objections most likely to cause trouble before an application goes in.", risk_tool['href'], risk_tool['cta'], "Risk tool")}
{_card("Browse councils first", "Choose this route when the local authority or conservation area question matters more than the project type.", "/councils/", "Open council hub", "Local layer")}
{_card(faq['title'], "Read the core process answer if you are still unsure about the basic planning permission question.", faq['href'], faq['cta'], "FAQ shortcut")}
</div>
</section>

<section id="project-hub-official">
<span class="eyebrow">Official checks</span>
<h2>Official Sources Worth Keeping In The Loop</h2>
<p class="section-lead">These sources should support the guide above, not replace it. Use them when you need the official baseline or you are close to a formal application decision.</p>
<div class="grid">{official_cards}</div>
</section>

<section id="project-hub-counties">
<span class="eyebrow">Compare by area only when needed</span>
<h2>Find The Right Local Authority Layer</h2>
<p class="section-lead">Go to the area layer once the broad route is clear enough. It matters most where one authority, one heritage context or one local policy culture could change the safer next step.</p>
<div class="county-grid">{''.join(county_cards)}</div>
</section>

<section id="project-hub-locals">
<span class="eyebrow">Strong local follow-ups</span>
<h2>Local Pages Worth Opening Next</h2>
<p class="section-lead">These are practical next reads, chosen to shorten the jump from a broad guide into the local answer rather than send you into another directory trail.</p>
<div class="grid">{''.join(featured_locals)}</div>
</section>

<section id="project-hub-topics">
<span class="eyebrow">Rules people usually need next</span>
<h2>Topic Hubs That Matter For This Project Type</h2>
<div class="grid">{topic_cards}</div>
</section>
"""


def build_councils_hub_content(councils_by_county: dict, towns: list[dict]) -> str:
    county_cards = []
    for county_slug, councils in councils_by_county.items():
        county_name = county_slug.replace("-", " ").title()
        examples = ", ".join(council["town_name"] for council in councils[:3])
        description = f"Browse {len(councils)} local authority areas in {county_name}."
        if examples:
            description += f" Start here for places like {examples}."
        county_cards.append(
            _card(
                county_name,
                description,
                f"/{county_slug}/",
                "Open area guide",
                "Area overview",
            )
        )

    town_cards = []
    for town in towns[:12]:
        town_cards.append(
            _card(
                town["town_name"],
                "Open the local authority overview, then jump into project guides and rule pages that match the issue you need to check.",
                f"/councils/{town['town_slug']}/",
                "View council page",
                "Popular local authority",
            )
        )

    methodology = PROMOTED_LINKS["methodology"]
    tools = PROMOTED_LINKS["tools"]

    return f"""
<section class="hero">
<span class="badge">Local authority hub</span>
<h1>UK Local Planning Authorities</h1>
<p>Use this section when the local authority layer is the real source of uncertainty, especially for conservation areas, heritage controls, Article 4 directions or council-specific guidance.</p>
<div class="answer-grid">
<div class="answer-card">
<h3>What this hub is for</h3>
<p>It helps you move from a broad planning question into the right planning area, the right council and the most useful local project page quickly.</p>
</div>
<div class="answer-card">
<h3>What it does not replace</h3>
<p>It does not replace the local planning authority, site-specific design review or formal confirmation where the proposal is close to a limit.</p>
</div>
<div class="answer-card">
<h3>Fastest next step</h3>
<p>Pick the planning area first, then compare the local authority page with the matching project guide and the planning topic that is causing uncertainty.</p>
</div>
</div>
</section>

{_jump_section(
    "Use This Council Hub In The Order That Saves You Time",
    [
        ("Start with the planning area", "#councils-hub-areas"),
        ("Open a live local authority entry point", "#councils-hub-popular"),
        ("Pair the local layer with the right tool or method", "#councils-hub-tools"),
    ],
)}

<section class="decision-guide" id="councils-hub-decision-guide">
<span class="eyebrow">Decision guide</span>
<h2>When The Council Hub Is The Right Starting Point And When It Is Not</h2>
<div class="answer-grid">
<div class="answer-card">
<h3>Best when</h3>
<ul class="checklist">
<li>The local authority layer is the main uncertainty.</li>
<li>You want to compare planning areas before choosing one council path.</li>
<li>Conservation areas, Article 4 or heritage controls may be the real blocker.</li>
</ul>
</div>
<div class="answer-card">
<h3>Go elsewhere first when</h3>
<ul class="checklist">
<li>You already know the exact project type and need the answer-first local project page.</li>
<li>The question is still broad enough that a tool or FAQ would narrow it faster.</li>
<li>You need a site-specific route decision rather than a navigation layer.</li>
</ul>
</div>
<div class="answer-card">
<h3>What usually settles it faster</h3>
<ul class="checklist">
<li>Pick the planning area first, then the council, then the matching project or rule page.</li>
<li>Use a tool first if the route is still broad and the local authority is not yet clear.</li>
<li>Use the local authority page alongside the project guide when local controls may change the answer.</li>
</ul>
</div>
</div>
</section>

<section id="councils-hub-areas">
<span class="eyebrow">Area-level navigation</span>
<h2>Choose The Planning Area First</h2>
<div class="county-grid">{''.join(county_cards)}</div>
</section>

<section id="councils-hub-popular">
<h2>Popular Local Authority Entry Points</h2>
<div class="grid">{''.join(town_cards)}</div>
</section>

<section id="councils-hub-tools">
<div class="split-grid">
<div class="cta-band">
<span class="eyebrow">Useful alongside council pages</span>
<h2>Pair The Local Layer With The Right Next Tool</h2>
<p>Most users get the clearest answer when they use a tool first for triage, then read the local authority page, then check the exact project guide or rule hub that could change the route.</p>
<div class="hero-ctas">
<a class="btn" href="{tools['href']}">{tools['cta']}</a>
<a class="btn button-secondary" href="{methodology['href']}">{methodology['cta']}</a>
</div>
</div>
<div class="mini-card">
<h3>What to verify locally</h3>
<ul class="checklist">
<li>Whether the property is in a conservation area or affected by Article 4.</li>
<li>Whether heritage controls or local design expectations raise the bar.</li>
<li>Whether the proposal is close enough to a limit that formal written confirmation is safer.</li>
</ul>
</div>
</div>
</section>
"""
