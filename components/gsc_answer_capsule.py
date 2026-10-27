from __future__ import annotations

from html import escape

from data.search_demand_priorities import gsc_cluster_for_path, gsc_target_for_path


def _items_html(items: tuple[str, ...] | list[str]) -> str:
    return "".join(f"<li>{escape(str(item))}</li>" for item in items if str(item).strip())


def _official_cue(path: str, target: dict) -> str:
    cluster = target.get("cluster") or gsc_cluster_for_path(path)
    if cluster == "hmo-article-4":
        return "Use the council Article 4 direction, map or HMO guidance before relying on a permitted-development answer."
    if cluster == "planning-portal":
        return "Start with the official council portal or validation source, then move into the project page that matches the work."
    if cluster == "conservation-map":
        return "Confirm the official conservation-area map or heritage source before applying the project rule."
    if cluster == "extension-drawings":
        return "Check the council validation list or application guidance before commissioning drawings or plans."
    if cluster == "dropped-kerb-highway":
        return "Check both the planning authority and the highway or access approval route before arranging works."
    if cluster == "porch-outbuilding-rules":
        return "Use the country-specific official source or council rule before relying on a generic UK summary."
    return "Use the relevant official council or country source before relying on a broad planning answer."


def build_gsc_answer_capsule(path: str) -> str:
    target = gsc_target_for_path(path)
    if not target:
        return ""

    title = target.get("title", "Start With The Check That Changes The Answer")
    answer = target.get("answer", "")
    checks = target.get("checks", ())
    next_step = target.get("next_step", "")
    primary_href = target.get("primary_href", path)
    primary_label = target.get("primary_label", "Open strongest next page")
    official_cue = target.get("official_cue") or _official_cue(path, target)
    growth_cohort = str(target.get("growth_cohort", ""))

    checks_html = _items_html(checks)
    checks_block = (
        f"""
<div class="answer-card">
<h3>Checks most likely to change it</h3>
<ul class="checklist">{checks_html}</ul>
</div>
"""
        if checks_html
        else ""
    )
    next_step_block = (
        f"""
<div class="answer-card">
<h3>Best next move</h3>
<p>{escape(next_step)}</p>
<a class="cta" href="{escape(primary_href, quote=True)}">{escape(primary_label)}</a>
</div>
"""
        if next_step
        else ""
    )
    growth_actions = (
        """
<div class="hero-ctas growth-answer-actions">
<a class="btn" href="/tools/planning-route-check/" data-growth-action="route_check_start">Check your likely route</a>
<a class="btn button-secondary" href="#official-sources" data-growth-action="official_source">Open official sources</a>
</div>
"""
        if growth_cohort
        else ""
    )

    return f"""
<section class="local-answer-box gsc-answer-capsule" data-growth-cohort="{escape(growth_cohort, quote=True)}">
<span class="eyebrow">Quick route check</span>
<h2>{escape(title)}</h2>
{growth_actions}
<div class="answer-grid">
<div class="answer-card">
<h3>Working answer</h3>
<p>{escape(answer)}</p>
</div>
{checks_block}
<div class="answer-card">
<h3>Official check cue</h3>
<p>{escape(official_cue)}</p>
</div>
{next_step_block}
</div>
</section>
"""
