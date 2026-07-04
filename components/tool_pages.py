from components.content_blocks import build_scenario_calculator
from components.custom_tool_suite import render_custom_planning_tool
from components.extension_value_estimator_tool import render_extension_value_estimator_tool
from components.faq_blocks import build_faq_section
from components.pd_calculator import render_pd_calculator
from components.planning_decision_tool import render_planning_decision_tool
from components.planning_route_check import build_planning_route_check_faq, render_planning_route_check_tool
from components.planning_rejection_risk_tool import render_planning_rejection_risk_tool
from components.personalised_guidance import build_personalised_guidance_cta
from components.what_can_i_build_explorer_tool import render_what_can_i_build_explorer_tool
from components.next_steps import build_next_step_cards, build_project_tracker_prompt
from components.building_regs_handoff import build_generic_building_regs_handoff
from data.promoted_links import PROMOTED_LINKS, TOOL_GUIDANCE_LINKS, TOOL_USAGE_STEPS
from components.trust_framework import build_trust_framework
from utils.live_links import filter_live_dict_links, is_live_internal_href, normalize_internal_href


def build_tool_hero(tool: dict) -> str:
    tool_title = tool["title"]
    intro = tool.get(
        "hero_intro",
        "Use this tool as a fast planning triage step before you rely on drawings, council pages or formal advice. It is designed to tell you what usually applies, what can change the answer and which next page is most worth opening.",
    )
    badges = "".join(f"<span>{badge}</span>" for badge in tool.get("hero_badges", []))
    badges_html = f"<div class='inline-badges'>{badges}</div>" if badges else ""

    return f"""
<section class="hero">
<span class="badge">Planning tool</span>
<h1>{tool_title}</h1>
<p>{intro}</p>
{badges_html}
</section>
"""


def get_tool_component(component_name, tool_slug: str) -> str:
    if component_name == "pd_calculator":
        return render_pd_calculator()
    if component_name == "planning_decision_tool":
        return render_planning_decision_tool()
    if component_name == "planning_route_check_tool":
        return render_planning_route_check_tool()
    if component_name == "planning_rejection_risk_tool":
        return render_planning_rejection_risk_tool()
    if component_name == "what_can_i_build_explorer_tool":
        return render_what_can_i_build_explorer_tool()
    if component_name == "extension_value_estimator_tool":
        return render_extension_value_estimator_tool()
    if component_name == "custom_planning_tool":
        return render_custom_planning_tool(tool_slug)
    return build_scenario_calculator(tool_slug)


def build_tool_calculator(tool) -> str:
    calculator = get_tool_component(tool.get("component"), tool["slug"])
    heading = tool.get("calculator_heading", "Run The Quick Check")
    intro = tool.get("calculator_intro", "")
    intro_html = f"<p class='section-lead'>{intro}</p>" if intro else ""
    return f"""
<section class="tool-calculator" data-tool-page="{tool['slug']}">
<span class="eyebrow">Interactive check</span>
<h2>{heading}</h2>
{intro_html}
{calculator}
</section>
"""


def build_tool_next_steps(tool: dict) -> str:
    return build_next_step_cards(
        page_family="tool",
        tool_slug=tool["slug"],
        context_text=f"{tool.get('title', '')} {tool.get('summary', '')}",
        title="Choose The Next Useful Step",
        intro="The tool result should lead to a practical action. Save the project, check whether formal proof is worth it, estimate cost, or test readiness before using the longer guidance form.",
    )


def build_tool_project_tracker(tool: dict) -> str:
    return build_project_tracker_prompt(page_family="tool", tool_slug=tool["slug"])


def build_tool_explanation(tool) -> str:
    tool_title = tool["title"]
    cards = tool.get("explanation_cards")

    if cards:
        card_html = "".join(
            f"""
<div class="answer-card">
<h3>{card['title']}</h3>
<p>{card['body']}</p>
</div>
"""
            for card in cards
        )
    else:
        card_html = f"""
<div class="answer-card">
<h3>Best use case</h3>
<p>{tool_title} helps homeowners sense-check the planning route before they commit to drawings, applications or contractor quotes.</p>
</div>
<div class="answer-card">
<h3>What can still change the answer</h3>
<p>Exact measurements, local designations, site history and the detailed project design can all shift the final planning route.</p>
</div>
<div class="answer-card">
<h3>Best next step</h3>
<p>Use the result to choose the right project guide, local authority page or rule hub rather than treating the tool as the last word.</p>
</div>
"""

    return f"""
<section class="tool-explanation">
<span class="eyebrow">How to use the result</span>
<h2>What This Tool Is Good For</h2>
<div class="answer-grid">
{card_html}
</div>
</section>
"""


def build_tool_search_intents(tool: dict) -> str:
    intents = tool.get("search_intents") or []
    if not intents:
        return ""

    items = "".join(f"<li>{intent}</li>" for intent in intents[:6])
    return f"""
<section class="tool-search-intents">
<span class="eyebrow">Good search matches</span>
<h2>Questions This Tool Is Best At Narrowing</h2>
<ul class="checklist">{items}</ul>
</section>
"""


def build_guidance_links(tool: dict, max_links: int) -> str:
    guidance_links = tool.get("guidance_links") or [
        {"title": title, "href": href}
        for title, href in TOOL_GUIDANCE_LINKS[:max_links]
    ]
    guidance_links = filter_live_dict_links(guidance_links)

    cards = [
        f"""
<a class="card" href="{item['href']}">
<div class="card-kicker">Next page</div>
<h3>{item['title']}</h3>
<p>{item.get('description', 'Open the detailed guidance once the tool has narrowed the real planning question.')}</p>
<span class="cta">Open guide</span>
</a>
"""
        for item in guidance_links[:max_links]
    ]

    return f"""
<section class="tool-guidance-links">
<span class="eyebrow">Where to go after the tool</span>
<h2>Detailed Guidance Worth Opening Next</h2>
<div class="grid">{''.join(cards)}</div>
</section>
"""


def build_tool_faq_links(tool: dict) -> str:
    faq_links = filter_live_dict_links(tool.get("faq_links") or [])
    if not faq_links:
        return ""

    cards = [
        f"""
<a class="card" href="{item['href']}">
<div class="card-kicker">FAQ follow-up</div>
<h3>{item['title']}</h3>
<p>{item['description']}</p>
<span class="cta">Read answer</span>
</a>
"""
        for item in faq_links[:3]
    ]

    return f"""
<section class="tool-faq-links">
<span class="eyebrow">Good follow-up reads</span>
<h2>FAQ Pages Worth Opening After The Tool</h2>
<div class="grid">{''.join(cards)}</div>
</section>
"""


def build_tool_embedded_faq(tool: dict) -> str:
    guidance_links = filter_live_dict_links(tool.get("guidance_links") or [])
    title = tool["title"]
    slug = tool["slug"]
    next_step_answer = ""

    if slug == "planning-route-check":
        return build_planning_route_check_faq()

    if slug == "planning-decision-tool":
        change_answer = "Property type, exact measurements, previous additions, flats, listed buildings, conservation areas and Article 4 are the factors most likely to move the result."
        verify_answer = "Stop relying on the tool alone once the route only works inside a tight threshold or the cost of being wrong is meaningful."
        next_step_answer = "Open the project guide or rule page the result has just isolated, then go local if the answer still depends on council-specific controls."
    elif slug == "planning-route-planner":
        change_answer = "Listed-building issues, Article 4, highway approvals, planning history and mixed-consent situations are the things most likely to change the route map."
        verify_answer = "Verify formally once the route depends on a parallel consent, a sensitive site or a scheme that only works if one approval path falls your way."
        next_step_answer = "Open the route page or consent type the result has narrowed it to, not a generic project guide."
    elif slug == "site-constraint-checker":
        change_answer = "The exact measurement point, the tightest edge of the site and any local control layered on top of the blocker are the details most likely to change the result."
        verify_answer = "Check measured drawings before relying on the output if one blocker is doing almost all the work."
        next_step_answer = "Open the matching rule page next, then move into the local project or council page if the blocker still depends on site context."
    elif slug == "extension-value-estimator":
        change_answer = "Planning certainty, bedroom gain, finish level, usable layout and the true build cost are the details most likely to move the range."
        verify_answer = "Treat the estimate as directional only if the planning route is still speculative or the market assumptions are not yet grounded in the real project."
        next_step_answer = "Open the matching project guide for the extension type you priced, then open the planning route page only if permission certainty is still the main blocker."
    elif slug == "planning-rejection-risk-analyzer":
        change_answer = "Design quality, neighbour impact, heritage sensitivity, parking and local policy context are the details most likely to make the risk profile worse or better."
        verify_answer = "Verify the next move formally once the scheme is still worth pursuing but the risks are high enough that redesign or pre-app advice could save time."
        next_step_answer = "Open the matching project guide next, then use the local authority layer if policy or site context is driving the risk."
    elif slug == "project-requirements-generator":
        change_answer = "The exact route, local validation needs and any heritage or policy issue are the things most likely to change which documents really matter first."
        verify_answer = "Check the prep pack formally before commissioning drawings if the project is sensitive, local-policy driven or already leaning toward a full application."
        next_step_answer = "Open the guide or local page that matches the route you are preparing for, then use the checklist as the evidence pack."
    elif slug == "building-control-route-checker":
        change_answer = "The stage of the work, the amount of structural or fire-safety work, whether installer certification applies, and whether planning is already settled are the details most likely to change the result."
        verify_answer = "Contact building control or a registered installer before work starts, and urgently if work has already started or completion evidence is missing."
        next_step_answer = "Open the matching building regulations guide first, then ask exactly which route, inspections and certificates should exist."
    else:
        change_answer = "Exact measurements, local controls, planning history and the detailed project design are the things most likely to change the result."
        verify_answer = "Verify formally once the output still feels borderline, expensive to get wrong or dependent on one tight assumption."
        if guidance_links:
            next_step_answer = f"Open {guidance_links[0]['title']} next if the result has already isolated the main issue."
        else:
            next_step_answer = "Open the matching guide next if the result has already isolated the main issue."

    if slug == "building-control-route-checker":
        final_answer = "No. The checker narrows the building regulations route to discuss next, but it does not approve work, replace building control, or prove that planning permission is unnecessary."
    else:
        final_answer = f"No. {title} is built to narrow the planning question quickly, not to replace the project guide, local authority layer or formal verification where certainty matters."

    faq_items = [
        (
            f"Is {title.lower()} a final answer?",
            final_answer,
        ),
        (
            "What details most often change the result?",
            change_answer,
        ),
        (
            "When should I verify formally?",
            verify_answer,
        ),
        (
            "What page should I open next?",
            next_step_answer,
        ),
        (
            "Why does local context still matter after the tool?",
            "Because conservation areas, listed buildings, Article 4, planning history and council-specific judgement can still make a familiar-looking result less reliable on a real site.",
        ),
    ]
    return build_faq_section(
        faq_items,
        section_id="tool-faq",
        eyebrow="Tool FAQ",
        title="Questions People Usually Ask After The Result",
        intro="Keep this block for the interpretation and trust questions that usually appear once the tool has narrowed the answer.",
    )


def _tool_href(tool: dict) -> str:
    return tool.get("href", f"/tools/{tool['slug']}/")


def build_tool_links(tool_slug: str, tools, max_links: int) -> str:
    cards = []
    seen_hrefs = {normalize_internal_href(f"/tools/{tool_slug}/")}

    for tool in tools:
        if tool["slug"] == tool_slug:
            continue
        href = normalize_internal_href(_tool_href(tool))
        if not href or href in seen_hrefs or not is_live_internal_href(href):
            continue
        seen_hrefs.add(href)

        cards.append(
            f"""
<a class="card" href="{href}">
<div class="card-kicker">Related tool</div>
<h3>{tool["title"]}</h3>
<p>{tool.get("summary", "Use another quick self-check when the first tool does not isolate the right planning issue.")}</p>
<span class="cta">Open tool</span>
</a>
"""
        )

        if len(cards) >= max_links:
            break

    return f"""
<section class="related-tools">
<span class="eyebrow">Useful companion tools</span>
<h2>Related Planning Tools</h2>
<div class="grid">{''.join(cards)}</div>
</section>
"""


def build_planning_context(tool_title: str) -> str:
    if "Building Control Route" in tool_title:
        return f"""
<section class="planning-context">
<span class="eyebrow">Context and caveats</span>
<h2>How This Tool Fits Building Regulations Work</h2>
<p>{tool_title} is a triage tool for England building regulations and building control questions. It is designed to help you ask a better next question, not to approve work or replace the building control body.</p>
<p>Use the result to decide whether the next step is full plans, building notice, competent person certification, regularisation, or a planning-first pause. Keep the planning route separate, because building control does not decide whether the development itself needs planning permission.</p>
</section>
"""
    return f"""
<section class="planning-context">
<span class="eyebrow">Context and caveats</span>
<h2>How This Tool Fits Into The Wider Planning Process</h2>
<p>{tool_title} is intended as a fast planning triage step based on common UK planning considerations and permitted development limits.</p>
<p>Use it to narrow the question, then move into project guides, local authority pages or formal confirmation if the scheme is close to a limit. The tool should help you spend money in the right order, not tempt you to stop checking too early.</p>
</section>
"""


def build_tool_guidance_cta(tool_title: str) -> str:
    if "Building Control Route" in tool_title:
        return build_personalised_guidance_cta(
            title="Need Help Separating Planning From Building Control?",
            description="If the route checker shows that planning, building control, certification or missing evidence are tangled together, use the structured guidance form to frame the next practical question before spending more.",
            context_label="tool-page",
            email_context=tool_title,
            compact=True,
        )
    return build_personalised_guidance_cta(
        title="Need A More Tailored Steer Than The Tool Result?",
        description=f"If {tool_title.lower()} has narrowed the question but the answer still depends on your exact site, local authority area or project details, use the structured guidance form instead of relying on another broad rule of thumb.",
        context_label="tool-page",
        email_context=tool_title,
        compact=True,
    )


def build_tool_building_regs_handoff(tool: dict) -> str:
    text = " ".join(
        [
            str(tool.get("title", "")),
            str(tool.get("summary", "")),
            str(tool.get("hero_intro", "")),
            str(tool.get("meta_description", "")),
        ]
    ).lower()
    if "building control" in text or "building regulations" in text or "competent person" in text:
        return build_generic_building_regs_handoff(
            title="Use BuildingRegsGuide For The Technical Approval Route",
            destination_key="route-checker",
        )
    return ""


def build_trust_section() -> str:
    methodology = PROMOTED_LINKS["methodology"]
    faq = PROMOTED_LINKS["faq"]
    return build_trust_framework(
        title="Use These Tools Properly",
        purpose="To reduce uncertainty quickly, point you to the next page that matters, and show when a broad tool result is still too weak to rely on for a live project decision.",
        not_replace="These tools do not replace formal confirmation for borderline schemes, local authority checking where special controls apply, or paid specialist input for genuinely complex cases.",
        built_from="Tool results are based on common planning and permitted development baselines, then framed to push you toward the project, local authority and rule pages most likely to settle the remaining doubt.",
        verify_when="Escalate when the route only works inside a tight threshold, when local controls may be doing most of the work, or when you need written certainty before drawings, applications or contractor spend.",
        safest_next_step="Use the tool result as triage, then move into the matching guide. If certainty still matters, step up to a lawful development certificate, pre-application advice or professional help rather than rerunning broad checks.",
        support_links=[
            (methodology["title"], methodology["href"]),
            (faq["title"], faq["href"]),
        ],
    )


def build_tools_index_content(tools) -> str:
    cards = []

    for tool in tools:
        cards.append(
            f"""
<a class="card" href="{_tool_href(tool)}">
<div class="card-kicker">Planning tool</div>
<h3>{tool['title']}</h3>
<p>{tool.get('summary', '')}</p>
<span class="cta">Open tool</span>
</a>
"""
        )

    usage_steps = "".join(f"<li>{step}</li>" for step in TOOL_USAGE_STEPS)

    return f"""
<section class="hero">
<span class="badge">Planning tools</span>
<h1>Planning Tools For Faster, Safer First Decisions</h1>
<p>Use these tools as one decision system: narrow the route quickly, spot what changes the answer and move into the right project guide, topic hub or local authority page before the wrong next step costs money.</p>
</section>

<section>
<span class="eyebrow">Tool-first route</span>
<h2>Choose The Tool That Matches The Doubt You Actually Have</h2>
<div class="answer-grid">
<div class="answer-card">
<h3>Best starting point</h3>
<p>Start with a tool when you need a fast first-pass answer before committing to deeper reading or local page comparisons.</p>
</div>
<div class="answer-card">
<h3>What to do after the result</h3>
<p>Move into the matching project guide, council page or rule hub rather than treating the tool output as a stopping point.</p>
</div>
<div class="answer-card">
<h3>When to escalate</h3>
<p>If the result feels borderline, assume the next step is a certificate, pre-app conversation or another formal check, not more guesswork.</p>
</div>
</div>
</section>

<section>
<span class="eyebrow">Tool library</span>
<h2>The Main Tools In The Decision System</h2>
<div class="card-grid">{''.join(cards)}</div>
</section>

<section>
<span class="eyebrow">Recommended sequence</span>
<h2>Best Way To Use Them</h2>
<ol>{usage_steps}</ol>
</section>
{build_personalised_guidance_cta(
    title="Need A More Tailored Steer Than A Quick Tool Can Give?",
    description="The tools are built to narrow the route quickly. If your case still feels too specific, too local or too borderline for a generic result, use the structured guidance form for a more tailored case-specific steer.",
    context_label="tools-index",
    email_context="tools page",
    compact=True,
)}
"""


def assemble_tool_page(blocks) -> str:
    return "\n".join(block for block in blocks if block)
