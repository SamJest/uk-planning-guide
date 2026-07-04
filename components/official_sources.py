from __future__ import annotations

from datetime import datetime
from html import escape

from utils.official_sources import (
    OfficialSourceContext,
    relevant_official_sources,
    source_category_label,
)


SOURCE_BLOCK_INTROS = {
    "council": "These are the council pages most likely to settle the next local check without turning the page into a directory.",
    "project": "These are the official pages most likely to settle this local project route once the broad answer has been narrowed.",
    "scenario": "These are the official pages most likely to settle this local rule question once the blocker is clear.",
    "local-search": "These are the official pages most likely to confirm the route once you know which deeper page to open next.",
    "building-regulations": "These are the official pages most likely to settle the building regulations and building control route before work starts.",
}


def _format_last_reviewed(value: str) -> str:
    clean = str(value or "").strip()
    if not clean:
        return ""

    for fmt in ("%Y-%m-%d", "%Y-%m"):
        try:
            parsed = datetime.strptime(clean, fmt)
        except ValueError:
            continue
        if fmt == "%Y-%m":
            return parsed.strftime("%B %Y")
        return f"{parsed.day} {parsed.strftime('%B %Y')}"
    return clean


def _label_from_slug(value: str) -> str:
    clean = str(value or "").strip()
    if not clean:
        return ""
    special = {
        "hmos": "HMOs",
        "article-4": "Article 4",
        "planning-permission": "planning permission",
        "permitted-development": "permitted development",
        "conservation-areas": "conservation areas",
        "listed-buildings": "listed buildings",
        "height-limits": "height limits",
        "boundary-rules": "boundary rules",
        "maximum-height": "maximum height",
        "building-regulations": "building regulations",
    }
    lowered = clean.lower()
    if lowered in special:
        return special[lowered]
    return clean.replace("-", " ")


def _source_intro(*, page_family: str, authority_slug: str, project_slug: str, scenario_slug: str) -> str:
    authority = _label_from_slug(authority_slug).title()
    project = _label_from_slug(project_slug)
    scenario = _label_from_slug(scenario_slug)
    if page_family == "project" and project and authority:
        return f"These are the official pages most likely to settle the {project} route in {authority}."
    if page_family == "scenario" and scenario and authority:
        return f"These are the official pages most likely to settle the {scenario} position in {authority}."
    if page_family == "council" and authority:
        return f"These are the council pages most likely to settle the next planning check in {authority}."
    if page_family == "local-search" and authority:
        return f"These are the official pages most likely to confirm the route behind this {authority} search."
    if page_family == "building-regulations":
        return "These are the official pages most likely to confirm the England building regulations and building control route."
    return SOURCE_BLOCK_INTROS.get(page_family, SOURCE_BLOCK_INTROS["council"])


def _source_reason(source, *, page_family: str, authority_slug: str, project_slug: str, scenario_slug: str) -> str:
    if source.notes:
        return source.notes

    authority = _label_from_slug(authority_slug).title()
    project = _label_from_slug(project_slug)
    scenario = _label_from_slug(scenario_slug)
    category = source.category

    if category == "planning_portal":
        if page_family == "project" and project and authority:
            return f"Useful for the official application route and national planning paperwork behind {project} in {authority}."
        if page_family == "scenario" and scenario and authority:
            return f"Useful for the official application route when {scenario} in {authority} is pushing the page toward a formal check."
        return f"Useful for the official application route and submission next step in {authority}."
    if category == "validation_requirements":
        return f"Useful because it sets out the document and checklist requirements that matter if {authority} is the next formal stop."
    if category == "pre_application_advice":
        return f"Useful when the broad answer is no longer enough and a local pre-application view in {authority} is the safer next step."
    if category == "householder_guidance":
        return f"Useful because it shows how {authority} explains common domestic projects before the page leans too hard on a national rule of thumb."
    if category == "permitted_development_guidance":
        return f"Useful because it helps test whether the simpler fallback still holds once {authority}'s local context is added back in."
    if category == "article_4":
        return f"Useful because Article 4 can remove the fallback route the page would otherwise be relying on in {authority}."
    if category in {"conservation_area", "heritage", "listed_buildings"}:
        return f"Useful because heritage controls often do more work than the headline measurement once the site is in a sensitive part of {authority}."
    if category in {"highways", "dropped_kerb_or_vehicle_access"}:
        return f"Useful because the decisive issue may be access, visibility or highway approval in {authority}, not planning wording alone."
    if category == "design_guide":
        return f"Useful when the route depends on how {authority} is likely to read visibility, materials or street-facing design."
    if category == "local_plan":
        return f"Useful because the local plan often settles the policy position once the route stops being a broad national question."
    if category == "trees":
        return f"Useful because tree constraints can change what looks like a routine project in {authority}."
    if category == "enforcement":
        return f"Useful when the risk sits in how the council may treat an existing or proposed breach rather than in the broad route summary."
    if category in {"building_regulations", "building_control", "building_control_application", "approved_documents", "competent_person_scheme"}:
        return "Useful because building regulations approval is separate from planning permission and should be checked before work starts."
    return f"Useful as a direct council source for the next check this page is pointing you toward in {authority}."


def build_official_sources_block(
    *,
    page_family: str,
    authority_slug: str,
    country_slug: str = "",
    project_slug: str = "",
    scenario_slug: str = "",
    section_id: str = "official-sources",
    max_links: int = 5,
) -> str:
    context = OfficialSourceContext(
        page_family=page_family,
        authority_slug=authority_slug,
        country_slug=country_slug,
        project_slug=project_slug,
        scenario_slug=scenario_slug,
        max_links=max_links,
    )
    sources = relevant_official_sources(context)
    if not sources:
        return ""

    intro = _source_intro(
        page_family=page_family,
        authority_slug=authority_slug,
        project_slug=project_slug,
        scenario_slug=scenario_slug,
    )
    items = []
    for source in sources:
        meta_bits = [source_category_label(source.category)]
        if source.last_reviewed:
            meta_bits.append(f"Last reviewed {_format_last_reviewed(source.last_reviewed)}")
        reason = _source_reason(
            source,
            page_family=page_family,
            authority_slug=authority_slug,
            project_slug=project_slug,
            scenario_slug=scenario_slug,
        )
        items.append(
            f"""
<a class="official-source-link" href="{escape(source.url, quote=True)}">
<strong>{escape(source.title)}</strong>
<span>{escape(" | ".join(meta_bits))}</span>
<span>{escape(reason)}</span>
</a>
"""
        )

    return f"""
<section class="official-sources" id="{escape(section_id, quote=True)}" data-official-sources="true" data-official-sources-family="{escape(page_family, quote=True)}" data-official-sources-authority="{escape(authority_slug, quote=True)}" data-official-sources-count="{len(sources)}">
<span class="eyebrow">Official sources</span>
<h2>Official Sources Worth Checking</h2>
<p class="section-lead">{escape(intro)}</p>
<p class="section-lead">Rules, validation requirements and local designations can change by location. Use these links to confirm the latest official position before relying on a close or expensive planning route.</p>
<div class="official-sources-list">
{''.join(items)}
</div>
</section>
"""
