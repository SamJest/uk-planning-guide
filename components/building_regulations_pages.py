from __future__ import annotations

from html import escape

from components.editorial_authority import build_editorial_authority_block
from components.faq_blocks import build_faq_section
from components.building_regs_handoff import build_generic_building_regs_handoff
from components.shared_components import render_result_capture
from data.building_regulations_pages import (
    BUILDING_REGULATIONS_PAGES,
    OFFICIAL_BUILDING_REGULATIONS_SOURCES,
    building_regulations_path,
)


PROJECT_PAGE_LINKS = {
    "house-extensions": "/house-extensions/",
    "loft-conversions": "/loft-conversions/",
    "garage-conversions": "/garage-conversions/",
    "porches": "/porches/",
    "temporary-buildings": "/temporary-buildings/",
    "outbuildings": "/outbuildings/",
    "driveways": "/driveways/",
}


def _page_href(page: dict) -> str:
    return building_regulations_path(page)


def _render_checklist(items: list[str]) -> str:
    return "".join(f"<li>{escape(str(item))}</li>" for item in items if str(item).strip())


def _render_cards(items: list[dict], *, kicker: str, cta: str) -> str:
    cards = []
    for item in items:
        href = escape(str(item.get("href", "")), quote=True)
        title = escape(str(item.get("title", "")))
        description = escape(str(item.get("description", "")))
        cards.append(
            f"""
<a class="card" href="{href}">
<div class="card-kicker">{escape(kicker)}</div>
<h3>{title}</h3>
<p>{description}</p>
<span class="cta">{escape(cta)}</span>
</a>
"""
        )
    return f"<div class='grid'>{''.join(cards)}</div>"


def _first_answer(page: dict) -> str:
    blocks = page.get("answer_blocks", [])
    if blocks:
        return str(blocks[0].get("body", "")).strip()
    questions = page.get("primary_questions", [])
    if questions:
        return str(questions[0][1]).strip()
    return "Check building regulations separately from planning permission before you rely on a home-project route."


def _approval_route_label(page: dict) -> str:
    intent = str(page.get("intent", "")).lower()
    if "regularisation" in intent:
        return "regularisation"
    if "competent person" in intent:
        return "competent person scheme"
    if "completion certificate" in intent:
        return "completion evidence"
    if "checklist" in intent:
        return "pre-start checklist"
    if page.get("project_slug") in {"house-extensions", "loft-conversions"}:
        return "full plans or building notice"
    return "building control route"


def _hub_pages() -> list[dict]:
    return [
        page
        for page in BUILDING_REGULATIONS_PAGES
        if page.get("slug")
        in {
            "extensions",
            "loft-conversions",
            "garage-conversions",
            "porches",
            "temporary-buildings",
            "outbuildings",
            "driveways",
        }
    ]


def _support_pages() -> list[dict]:
    project_slugs = {page["slug"] for page in _hub_pages()}
    excluded = project_slugs | {"index"}
    preferred = [
        "before-you-start-checklist",
        "building-notice-vs-full-plans",
        "building-control-inspections",
        "drawings-and-specifications",
        "structural-calculations",
        "drainage-and-waste",
        "competent-person-schemes",
        "regularisation-certificates",
        "completion-certificates",
        "windows-and-doors",
        "roof-lights",
        "solar-panels",
        "heat-pumps",
    ]
    by_slug = {page["slug"]: page for page in BUILDING_REGULATIONS_PAGES if page.get("slug") not in excluded}
    ordered = [by_slug[slug] for slug in preferred if slug in by_slug]
    ordered.extend(page for slug, page in sorted(by_slug.items()) if page not in ordered)
    return ordered


def build_building_regulations_hero(page: dict) -> str:
    answer = _first_answer(page)
    project_slug = str(page.get("project_slug") or "")
    project_href = PROJECT_PAGE_LINKS.get(project_slug, "/planning-faq/planning-permission-vs-building-regulations/")
    project_label = "planning route" if not project_slug else project_slug.replace("-", " ")
    approval_route = _approval_route_label(page)
    return f"""
<section class="hero" id="building-regulations-answer">
<span class="badge">{escape(page.get("jurisdiction", "England"))} building regulations</span>
<h1>{escape(page["title"])}</h1>
<p>{escape(answer)}</p>
<div class="tool-result tool-result-visible">
<strong>Quick answer:</strong> Treat the {escape(approval_route)} question as separate from planning permission. UK Planning Guide keeps this as bridge guidance; the detailed technical route now lives on BuildingRegsGuide.
</div>
<div class="hero-ctas">
<a class="button" href="#building-control-questions">What to ask building control</a>
<a class="button secondary" href="https://buildingregsguide.co.uk/tools/building-control-route-checker/">Run sister route checker</a>
<a class="button secondary" href="{escape(project_href, quote=True)}">Open {escape(project_label)} checks</a>
</div>
</section>
"""


def build_building_regulations_jump_links(page: dict) -> str:
    return """
<section class="page-jump-links">
<div class="link-grid">
<a href="#approval-sequence">Compare planning and building regulations</a>
<a href="#route-playbook">Choose the approval route</a>
<a href="#building-control-questions">Prepare building control questions</a>
<a href="#proof-to-keep">See what proof to keep</a>
<a href="#official-sources">Check official sources</a>
<a href="#related-routes">Open the next planning route</a>
</div>
</section>
"""


def build_building_regulations_summary(page: dict) -> str:
    blocks = page.get("answer_blocks", [])
    cards = []
    for block in blocks[:3]:
        checks = block.get("checks", [])
        checklist = f"<ul class='checklist'>{_render_checklist(checks)}</ul>" if checks else ""
        cards.append(
            f"""
<div class="answer-card">
<h3>{escape(block.get("title", ""))}</h3>
<p>{escape(block.get("body", ""))}</p>
{checklist}
</div>
"""
        )

    if len(cards) < 3:
        cards.append(
            """
<div class="answer-card">
<h3>England-first scope</h3>
<p>This pilot does not try to flatten England, Wales and Scotland into one answer. Use the linked official sources before relying on a close route.</p>
<ul class="checklist"><li>England baseline</li><li>Official source links</li><li>Planning route handoff</li></ul>
</div>
"""
        )

    return f"""
<section id="approval-sequence">
<span class="eyebrow">Working summary</span>
<h2>Planning First, Building Control Next, Evidence Always</h2>
<p class="section-lead">Use this page to separate the project permission question from the technical compliance question. That split is what keeps the guidance useful instead of turning every home project into one blurry approval answer.</p>
<div class="answer-grid">
{''.join(cards[:3])}
</div>
</section>
"""


def build_route_playbook(page: dict) -> str:
    route_label = _approval_route_label(page)
    project = str(page.get("project_slug") or "home project").replace("-", " ")
    first_question = ""
    questions = page.get("primary_questions", [])
    if questions:
        first_question = str(questions[0][1]).strip()
    if not first_question:
        first_question = "Start by separating planning permission from the building regulations route."

    return f"""
<section id="route-playbook">
<span class="eyebrow">Practical route playbook</span>
<h2>Use This Sequence Before The Job Becomes Expensive To Reverse</h2>
<p class="section-lead">A good building-regulations answer should leave you with a next action, not just a definition. For this {escape(project)}, the useful route is to pin down the planning risk, choose the right building-control conversation, then keep evidence as the work moves on.</p>
<div class="answer-grid">
<div class="answer-card">
<h3>1. Separate the approvals</h3>
<p>{escape(first_question)} Planning permission decides whether the development is acceptable in planning terms; building regulations decide whether the work is technically compliant.</p>
</div>
<div class="answer-card">
<h3>2. Pick the route to discuss</h3>
<p>Ask whether the next step is {escape(route_label)}, full plans, building notice, competent person certification, regularisation, or a planning-first pause.</p>
</div>
<div class="answer-card">
<h3>3. Keep the proof trail</h3>
<p>Save drawings, specifications, inspection records, installer certificates and completion evidence together so the route can be understood later.</p>
</div>
</div>
</section>
"""


def build_route_checker_cta(page: dict) -> str:
    return """
<section class="conversion-hook" id="building-control-route-checker">
<span class="eyebrow">Interactive route check</span>
<h2>Not Sure Which Building Control Route To Ask About?</h2>
<p>Use the BuildingRegsGuide route checker when the project is stuck between full plans, building notice, competent person certification, regularisation or a planning-first pause. It is a quick triage step, not a substitute for building control advice.</p>
<div class="hero-ctas">
<a class="button" href="https://buildingregsguide.co.uk/tools/building-control-route-checker/">Run the sister route checker</a>
<a class="button secondary" href="/building-regulations/before-you-start-checklist/">Open the before-you-start checklist</a>
</div>
</section>
"""


def build_common_mistakes(page: dict) -> str:
    route_label = _approval_route_label(page)
    return f"""
<section id="common-mistakes">
<span class="eyebrow">Common mistakes</span>
<h2>Small Assumptions That Create Bigger Problems Later</h2>
<div class="answer-grid">
<div class="answer-card">
<h3>Using one approval to answer another</h3>
<p>Planning permission, permitted development, building regulations and installer certification answer different questions. Do not let one reassuring phrase carry the whole project.</p>
</div>
<div class="answer-card">
<h3>Choosing the route too late</h3>
<p>If the likely route is {escape(route_label)}, settle that before work is hidden, dates are fixed or the contractor has already moved past the inspection point.</p>
</div>
<div class="answer-card">
<h3>Keeping proof as an afterthought</h3>
<p>Certificates, inspection notes, photos and specifications are much easier to collect while the project is live than years later during a sale or remortgage.</p>
</div>
</div>
</section>
"""


def build_building_control_questions(page: dict) -> str:
    project = str(page.get("project_slug") or "home project").replace("-", " ")
    return f"""
<section id="building-control-questions">
<span class="eyebrow">Building control questions</span>
<h2>What To Ask Before You Commit</h2>
<div class="answer-grid">
<div class="answer-card">
<h3>Approval route</h3>
<p>Ask whether this {escape(project)} should use a building notice, full plans route, regularisation route, competent person scheme or another building control path.</p>
</div>
<div class="answer-card">
<h3>Information needed</h3>
<p>Ask what drawings, structural notes, specifications, declarations or site details should be ready before work starts or before an application is made.</p>
</div>
<div class="answer-card">
<h3>Inspection and sign-off</h3>
<p>Ask when inspections are expected, who books them, what should not be covered up too early and what completion evidence should be issued at the end.</p>
</div>
</div>
</section>
"""


def build_proof_to_keep(page: dict) -> str:
    return f"""
<section id="proof-to-keep" class="conversion-hook">
<span class="eyebrow">Retention and evidence</span>
<h2>What Proof To Keep Before Selling Or Remortgaging</h2>
<p>Keep the building-control record with the planning record. The useful paperwork is not just for the build itself; it can matter years later when a buyer, lender, insurer or adviser asks how the work was approved.</p>
<div class="grid-tight">
<div class="mini-card">
<h3>Before work</h3>
<p>Save the quote, drawings, specifications, approval route and any written advice from the building control body.</p>
</div>
<div class="mini-card">
<h3>During work</h3>
<p>Save inspection dates, photos before work is covered up, design changes and any contractor or competent person records.</p>
</div>
<div class="mini-card">
<h3>After completion</h3>
<p>Save the completion certificate, compliance certificates, planning decision or lawful development certificate, and final drawings.</p>
</div>
</div>
{render_result_capture("building-regulations-result-capture")}
</section>
"""


def build_building_regulations_official_sources(page: dict) -> str:
    keys = page.get("official_sources", [])
    items = []
    for key in keys:
        source = OFFICIAL_BUILDING_REGULATIONS_SOURCES.get(key)
        if not source:
            continue
        items.append(
            f"""
<a class="official-source-link" href="{escape(source['url'], quote=True)}">
<strong>{escape(source['title'])}</strong>
<span>{escape(source['category'].replace("_", " ").title())}</span>
<span>{escape(source['notes'])}</span>
</a>
"""
        )

    if not items:
        return ""

    return f"""
<section class="official-sources" id="official-sources" data-official-sources="true" data-official-sources-family="building-regulations" data-official-sources-authority="england" data-official-sources-count="{len(items)}">
<span class="eyebrow">Official sources</span>
<h2>Official Sources Worth Checking</h2>
<p class="section-lead">Building regulations can change by project type, building-control route and jurisdiction. This pilot is England-first, so use these official sources before relying on a close or expensive route.</p>
<div class="official-sources-list">
{''.join(items)}
</div>
</section>
"""


def build_building_regulations_navigation(current_slug: str) -> str:
    cards = []
    for page in _hub_pages():
        slug = page["slug"]
        if slug == current_slug:
            continue
        cards.append(
            {
                "title": page["title"].replace("Building Regulations For ", ""),
                "href": _page_href(page),
                "description": page["meta_description"],
            }
        )
    if not cards:
        return ""
    return f"""
<section id="building-regulations-projects">
<span class="eyebrow">Project routes</span>
<h2>Building Regulations By Project Type</h2>
<p class="section-lead">Use these pages when the planning question is no longer the only thing to settle.</p>
{_render_cards(cards, kicker="Building regulations", cta="Open route")}
</section>
"""


def build_building_regulations_support_navigation(current_slug: str) -> str:
    cards = []
    for page in _support_pages():
        slug = page["slug"]
        if slug == current_slug:
            continue
        cards.append(
            {
                "title": page["title"],
                "href": _page_href(page),
                "description": page["meta_description"],
            }
        )
        if len(cards) >= 9:
            break
    if not cards:
        return ""
    return f"""
<section id="building-regulations-support">
<span class="eyebrow">Deeper checks</span>
<h2>Useful Building Regulations Follow-Up Guides</h2>
<p class="section-lead">Open these when the project question has moved from “do I need approval?” into drawings, inspections, certification, drainage, structure or proof.</p>
{_render_cards(cards, kicker="Building regulations", cta="Open guide")}
</section>
"""


def build_related_routes(page: dict) -> str:
    related = page.get("related_routes", [])
    if not related:
        return ""
    return f"""
<section id="related-routes">
<span class="eyebrow">Useful next pages</span>
<h2>Open The Route That Settles The Next Decision</h2>
<p class="section-lead">These links keep the building-regulations answer connected to the planning, evidence and project-preparation pages that users are likely to need next.</p>
{_render_cards(related, kicker="Related route", cta="Open page")}
</section>
"""


def build_building_regulations_faq(page: dict) -> str:
    return build_faq_section(
        page.get("primary_questions", []),
        section_id="building-regulations-faq",
        eyebrow="Quick follow-up questions",
        title="Questions People Usually Ask Next",
        intro="Use these as short route checks before you rely on a contractor answer, order drawings or submit through building control.",
    )


def build_building_regulations_content(page: dict) -> str:
    path = _page_href(page)
    return "\n".join(
        [
            build_building_regulations_hero(page),
            build_building_regulations_jump_links(page),
            build_building_regulations_summary(page),
            build_route_playbook(page),
            build_route_checker_cta(page),
            build_common_mistakes(page),
            build_generic_building_regs_handoff(
                title="Continue The Technical Route On BuildingRegsGuide",
                destination_key="route-checker",
            ),
            build_editorial_authority_block(
                path,
                page_family="building-regulations",
                country_slug="england",
                project_slug=page.get("project_slug", ""),
            ),
            build_building_control_questions(page),
            build_proof_to_keep(page),
            build_building_regulations_official_sources(page),
            build_building_regulations_navigation(page.get("slug", "")),
            build_building_regulations_support_navigation(page.get("slug", "")),
            build_related_routes(page),
            build_building_regulations_faq(page),
        ]
    )
