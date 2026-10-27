from __future__ import annotations

from html import escape

from components.page_authority import resolve_page_authority


def _block_intro(authority: dict) -> str:
    family = str(authority.get("page_family") or "")
    if family == "project":
        return "A quick note on the local route this page is using, the council source that matters most and the point where a formal check becomes the safer next move."
    if family == "scenario":
        return "A quick note on the rule this page is grounding, the local source behind it and the point where broad guidance stops being enough."
    if family == "council":
        return "A quick note on the documented review process, which council material this guide uses and when a local check should replace broad reading."
    if family == "hub":
        return "A quick note on the broad route this hub is using, what usually changes it and where to go when the question stops being broad."
    if family == "faq":
        return "A quick note on the answer this FAQ is grounding, the main qualifier behind it and when a formal check is safer than more reading."
    if family == "local-search":
        return "A quick note on why this route page exists, which official sources support it and where the user should go next."
    if family in {"building-regulations", "building-regulations-hub"}:
        return "A quick note on the England-first building regulations route, the official sources behind it and when building control should settle the next question."
    return "A quick note on what this page was checked against, what usually changes the answer and where a formal check becomes safer."


def build_editorial_authority_block(
    path: str,
    *,
    page_family: str,
    authority_slug: str = "",
    country_slug: str = "",
    project_slug: str = "",
    scenario_slug: str = "",
) -> str:
    authority = resolve_page_authority(
        path,
        page_family=page_family,
        authority_slug=authority_slug,
        country_slug=country_slug,
        project_slug=project_slug,
        scenario_slug=scenario_slug,
    )
    source = authority["official_source"]
    source_title = escape(source.get("title", "Visible official sources"))
    source_url = escape(source.get("url", ""), quote=True)
    source_date = escape(source.get("date", ""))
    source_reason = escape(str(authority.get("source_reason") or ""))
    change_note = escape(str(authority.get("change_note") or ""))

    official_link = (
        f'<a class="editorial-source-link" href="{source_url}">{source_title}</a>'
        if source_url
        else f"<strong>{source_title}</strong>"
    )
    source_reason_html = (
        f"<p>{source_reason}</p>"
        if source_reason
        else "<p>Use the linked official material to confirm the current wording before relying on a close or expensive route.</p>"
    )

    return f"""
<section class="editorial-authority" id="editorial-authority" data-editorial-authority="true" data-editorial-path="{escape(path, quote=True)}" data-editorial-family="{escape(str(authority.get('page_family') or page_family), quote=True)}">
<span class="eyebrow">Editorial authority</span>
<h2>Source context</h2>
<div class="editorial-trust-strip">
<span><strong>Content updated</strong> {escape(str(authority.get("last_reviewed_display") or ""))}</span>
<span><strong>Prepared under</strong> <a href="/methodology/">UK Planning Guide editorial process</a></span>
<span><strong>Review method</strong> Route, jurisdiction, local context and official-source checks</span>
</div>
<div class="editorial-proof-grid">
<div class="mini-card editorial-footing">
<h3>Official sources</h3>
<p>{official_link}</p>
<p class="quick-summary">{source_date}</p>
{source_reason_html}
</div>
</div>
</section>
"""
