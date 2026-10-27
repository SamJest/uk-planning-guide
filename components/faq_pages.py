from components.editorial_authority import build_editorial_authority_block
from components.building_regs_handoff import build_generic_building_regs_handoff
from components.download_assets import render_download_asset_cards_for_path
from components.find_help_pages import build_find_help_cta, should_show_find_help_faq_cta
from components.faq_blocks import build_faq_section
from components.personalised_guidance import build_personalised_guidance_cta
from data.download_assets import assets_for_source_path
from data.promoted_links import FAQ_INDEX_NEXT_STEP_KEYS, PROMOTED_LINKS
from utils.live_links import filter_live_card_links


def _render_list(items):
    return "".join(f"<li>{item}</li>" for item in items)


def _render_related_links(links):
    cards = []
    for title, href, description in links:
        cards.append(
            f"""
<a class="card" href="{href}">
<div class="card-kicker">Related guidance</div>
<h3>{title}</h3>
<p>{description}</p>
<span class="cta">Open page</span>
</a>
"""
        )
    return "<div class='grid'>" + "".join(cards) + "</div>"


def _render_priority_routes(links):
    if not links:
        return ""

    return f"""
<section id="faq-routes">
<span class="eyebrow">Best next routes</span>
<h2>Open One Of These Next If The Question Has Narrowed</h2>
<p class="section-lead">These are the follow-up pages most likely to settle the next decision without sending you into another broad explainer.</p>
{_render_related_links(links)}
</section>
"""


ROUTING_LED_OPENERS = (
    "use this page when",
    "start here when",
    "read this when",
    "open this when",
    "use this when",
)


def _is_routing_led(text: str) -> bool:
    return str(text or "").strip().lower().startswith(ROUTING_LED_OPENERS)


def _opening_answer(faq):
    summary = str(faq.get("summary", "")).strip()
    if summary and not _is_routing_led(summary):
        return summary

    for section in faq.get("sections", []):
        for paragraph in section.get("paragraphs", []):
            clean = str(paragraph).strip()
            if clean:
                parts = [part.strip() for part in clean.split(". ") if part.strip()]
                if parts:
                    sentence = parts[0]
                    return sentence if sentence.endswith((".", "?", "!")) else sentence + "."
                return clean

    return summary


def _opening_qualification(faq, opening):
    paragraphs = faq.get("sections", [{}])[0].get("paragraphs", [])
    opening_key = str(opening or "").strip().lower().rstrip(".")
    for paragraph in paragraphs:
        clean = str(paragraph).strip()
        clean_key = clean.lower().rstrip(".")
        if (
            clean
            and clean != opening
            and not _is_routing_led(clean)
            and clean_key != opening_key
            and not clean_key.startswith(opening_key + ".")
        ):
            return clean
    return ""


def _safest_next_step(faq):
    related_links = filter_live_card_links(faq.get("related_links", []))
    if related_links:
        title, _href, _description = related_links[0]
        return f"Open {title} next if the question has now narrowed into something more specific."
    return "Use the qualifier above, then move to a project guide, local page or formal check if the answer now depends on your exact site."


def _render_guidance_cta(faq):
    return build_personalised_guidance_cta(
        title="Need A More Case-Specific Steer?",
        description="If this FAQ answers the broad process question but your own case still turns on the details of the project, the property or the local authority area, use the structured guidance form for a more tailored case-specific steer.",
        context_label="faq-page",
        email_context=faq["title"],
        compact=True,
    )


def _render_find_help_cta(faq):
    if not should_show_find_help_faq_cta(faq["slug"]):
        return ""
    return build_find_help_cta()


def _render_building_regs_handoff(faq):
    text = " ".join(
        [
            str(faq.get("title", "")),
            str(faq.get("summary", "")),
            " ".join(
                " ".join(section.get("paragraphs", []))
                for section in faq.get("sections", [])
            ),
        ]
    ).lower()
    if "building regulation" not in text and "building control" not in text:
        return ""
    return build_generic_building_regs_handoff(
        title="Planning Answer Here, Building Regulations Detail On BuildingRegsGuide",
        destination_key="planning-vs-regs",
    )


def _render_faq_trust_section(faq, opening: str) -> str:
    key_checks = faq.get("key_checks", [])
    if key_checks:
        qualifier_html = f"<ul class='checklist'>{_render_list(key_checks[:3])}</ul>"
    else:
        qualifier_html = (
            "<p>Exact measurements, local controls, planning history and any formally sensitive site detail "
            "are the checks most likely to move the answer away from the broad position.</p>"
        )

    return f"""
<section id="faq-trust">
<span class="eyebrow">Trust and caveats</span>
<h2>Keep The Direct Answer, But Verify The Borderline Cases</h2>
<div class="answer-grid">
<div class="answer-card">
<h3>How to use this answer</h3>
<p>{opening}</p>
<p>Use this page as a practical briefing note for the broad route, not as a final permission decision for one exact site.</p>
</div>
<div class="answer-card">
<h3>What most often moves the answer</h3>
{qualifier_html}
</div>
<div class="answer-card">
<h3>When to stop reading and verify</h3>
<p>Stop relying on the FAQ alone when the answer now depends on one address, one exact drawing, one local control or a decision that would be expensive to get wrong.</p>
</div>
</div>
</section>
"""


def build_faq_page_content(faq):
    related_links = filter_live_card_links(faq.get("related_links", []))
    top_links = related_links[:3]
    secondary_links = related_links[3:]
    opening = _opening_answer(faq)
    qualification = _opening_qualification(faq, opening)
    downloadable_assets = render_download_asset_cards_for_path(
        f"/planning-faq/{faq['slug']}/",
        assets_for_source_path(f"/planning-faq/{faq['slug']}/"),
    )
    sections = []
    for section in faq["sections"]:
        paragraphs = "".join(f"<p>{paragraph}</p>" for paragraph in section.get("paragraphs", []))
        bullets = f"<ul class='checklist'>{_render_list(section['bullets'])}</ul>" if section.get("bullets") else ""
        sections.append(
            f"""
<section>
<h2>{section['heading']}</h2>
{paragraphs}
{bullets}
</section>
"""
        )

    return f"""
<section class="hero">
<span class="badge">{faq['category']}</span>
<h1>{faq['title']}</h1>
<p>{opening}</p>
{f'<p>{qualification}</p>' if qualification else ''}
</section>

<section id="faq-summary">
<span class="eyebrow">Working summary</span>
<h2>Short Answer, Main Qualifiers, Best Next Step</h2>
<div class="answer-grid">
<div class="answer-card">
<h3>Short answer</h3>
<p>{opening}</p>
</div>
<div class="answer-card">
<h3>What could change it</h3>
<ul class="checklist">{_render_list(faq['key_checks'][:3])}</ul>
</div>
<div class="answer-card">
<h3>Safest next step</h3>
<p>{_safest_next_step(faq)}</p>
</div>
</div>
</section>

{build_editorial_authority_block(
    f"/planning-faq/{faq['slug']}/",
    page_family="faq",
)}

{_render_priority_routes(top_links)}
{downloadable_assets}

<section id="faq-detail">
{''.join(sections)}
</section>
{build_faq_section(
    faq["questions"],
    section_id="faq-questions",
    eyebrow="Quick follow-up questions",
    title="Questions People Usually Ask Next",
)}
{_render_guidance_cta(faq)}
{_render_find_help_cta(faq)}
{_render_building_regs_handoff(faq)}

{f'''
<section class="support-stack">
<span class="eyebrow">Useful next pages</span>
<h2>Related Guidance</h2>
<p class="section-lead">Keep these as follow-ups after the main answer above. They are useful when the issue branches into a project, a local route or a more formal planning check.</p>
<details class="support-disclosure">
<summary>Show more related guidance and deeper follow-up pages</summary>
{_render_related_links(secondary_links)}
</details>
</section>
''' if secondary_links else ''}
{_render_faq_trust_section(faq, opening)}
"""


def build_faq_index_content(faqs):
    categories = {}
    for faq in faqs:
        categories.setdefault(faq["category"], []).append(faq)

    sections = []
    for category, items in categories.items():
        cards = []
        for faq in items:
            cards.append(
                f"""
<a class="card" href="/planning-faq/{faq['slug']}/">
<div class="card-kicker">{category}</div>
<h3>{faq['title']}</h3>
<p>{_opening_answer(faq)}</p>
<span class="cta">Read answer</span>
</a>
"""
            )

        sections.append(
            f"""
<section>
<h2>{category}</h2>
<div class="grid">{''.join(cards)}</div>
</section>
"""
        )

    next_step_links = filter_live_card_links(
        [
            (
                PROMOTED_LINKS[key]["title"],
                PROMOTED_LINKS[key]["href"],
                PROMOTED_LINKS[key]["description"],
            )
            for key in FAQ_INDEX_NEXT_STEP_KEYS
            if key in PROMOTED_LINKS
        ]
    )

    next_step_cards = "".join(
        f"""
<a class="card" href="{href}">
<div class="card-kicker">Useful next step</div>
<h3>{title}</h3>
<p>{description}</p>
<span class="cta">Open page</span>
</a>
"""
        for title, href, description in next_step_links
    )

    return f"""
<section class="hero">
<span class="badge">Planning FAQ</span>
<h1>Planning Permission Questions, Answered Clearly</h1>
<p>Use the FAQ library for broad planning questions about permission routes, restrictions, applications, timings and verification. If you already know the exact project or council area, the stronger next step is usually the matching guide rather than another general explainer.</p>
</section>

<section id="faq-library-summary">
<span class="eyebrow">Central answer library</span>
<h2>What This FAQ Hub Does Best</h2>
<div class="answer-grid">
<div class="answer-card">
<h3>Best fit</h3>
<p>Your question is about process, timing, permissions, restrictions or verification rather than one exact build type.</p>
</div>
<div class="answer-card">
<h3>What usually complicates it</h3>
<p>Local controls, listed status, conservation areas, Article 4 and borderline measurements often push a broad process question into a project or council page.</p>
</div>
<div class="answer-card">
<h3>Safest next step</h3>
<p>Start here when the question is still broad. Switch to the matching project, council or tool page as soon as the blocker is specific enough to name clearly.</p>
</div>
</div>
</section>

<section id="faq-library-categories">
{''.join(sections)}
</section>

<section id="faq-library-next-steps">
<span class="eyebrow">Good next steps</span>
<h2>Useful Next Steps</h2>
<div class="grid">{next_step_cards}</div>
</section>
{build_personalised_guidance_cta(
    title="Still Need A More Tailored Answer?",
    description="Use the FAQ library to narrow the issue first. If the real answer still depends on your exact property, project details or local context, the structured guidance form is the cleanest next step.",
    context_label="faq-index",
    email_context="FAQ library",
    compact=True,
)}
"""
