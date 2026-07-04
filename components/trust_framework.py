from __future__ import annotations

from html import escape


def planning_system_label(county_name: str) -> str:
    lowered = str(county_name or "").strip().lower()
    if lowered == "wales":
        return "Welsh planning system"
    if lowered == "scotland":
        return "Scottish planning system"
    if lowered == "northern ireland":
        return "Northern Ireland planning system"
    return "English planning system"


def _render_links(links: list[tuple[str, str]] | None) -> str:
    items = []
    for label, href in links or []:
        if not label or not href:
            continue
        items.append(f'<p><a href="{escape(href, quote=True)}">{escape(label)}</a></p>')
    return "".join(items)


def build_trust_framework(
    *,
    title: str,
    purpose: str,
    not_replace: str,
    built_from: str,
    verify_when: str,
    safest_next_step: str,
    support_links: list[tuple[str, str]] | None = None,
    section_id: str = "",
    eyebrow: str = "Trust and method",
) -> str:
    section_attr = f' id="{escape(section_id, quote=True)}"' if section_id else ""
    support_html = _render_links(support_links)
    support_card = (
        f"""
<div class="answer-card">
<h3>Useful trust pages</h3>
{support_html}
</div>
"""
        if support_html
        else ""
    )
    return f"""
<section class="trust-framework"{section_attr}>
<span class="eyebrow">{eyebrow}</span>
<h2>{title}</h2>
<div class="answer-grid">
<div class="answer-card">
<h3>Rules vary by location</h3>
<p>Planning routes can change by council area, property history, designations and the exact proposal. Use this page as a structured guide to the next check, not as a blanket approval.</p>
</div>
<div class="answer-card">
<h3>What this page is for</h3>
<p>{purpose}</p>
</div>
<div class="answer-card">
<h3>What it does not replace</h3>
<p>{not_replace}</p>
</div>
<div class="answer-card">
<h3>How the guidance is built</h3>
<p>{built_from}</p>
</div>
<div class="answer-card">
<h3>When to stop relying on broad guidance</h3>
<p>{verify_when}</p>
</div>
<div class="answer-card">
<h3>Safest formal next step</h3>
<p>{safest_next_step}</p>
</div>
<div class="answer-card">
<h3>Official-source check</h3>
<p>Where this page shows official sources, use those links near the relevant answer to confirm the latest council or national wording before relying on a borderline route.</p>
</div>
{support_card}
</div>
</section>
"""
