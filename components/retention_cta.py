from __future__ import annotations

from html import escape

from data.retention_journeys import infer_retention_key, retention_journey_for_key
from data.search_demand_priorities import gsc_cluster_for_path, gsc_target_for_path


def _format(template: str, **values: str) -> str:
    try:
        return str(template or "").format(**values)
    except (KeyError, ValueError):
        return str(template or "")


def _attr(name: str, value: str) -> str:
    clean = str(value or "").strip()
    if not clean:
        return ""
    return f' {escape(name, quote=True)}="{escape(clean, quote=True)}"'


def build_workspace_retention_cta(
    path: str,
    *,
    title: str = "",
    page_family: str = "",
    project_slug: str = "",
    authority_slug: str = "",
) -> str:
    target = gsc_target_for_path(path)
    if not target:
        return ""

    retention_key = gsc_cluster_for_path(path) or infer_retention_key(path, target)
    journey = retention_journey_for_key(retention_key)
    page_title = title or target.get("meta_title") or target.get("title") or "this planning route"
    task_title = _format(journey["task_title_template"], title=page_title)
    save_summary = _format(journey["save_summary_template"], title=page_title)
    page_family = page_family or retention_key or "gsc-target"

    attrs = "".join(
        (
            _attr("data-workspace-retention", "true"),
            _attr("data-retention-key", retention_key),
            _attr("data-page-family", page_family),
            _attr("data-project-slug", project_slug),
            _attr("data-authority-slug", authority_slug),
            _attr("data-workspace-title", page_title),
            _attr("data-workspace-summary", save_summary),
            _attr("data-workspace-task-title", task_title),
            _attr("data-workspace-task-summary", journey["task_summary"]),
            _attr("data-workspace-next-tool", journey["next_tool_href"]),
        )
    )

    guidance_route = f"retention-{retention_key}".strip("-")
    return f"""
<section class="workspace-retention-cta"{attrs}>
<span class="eyebrow">{escape(journey["eyebrow"])}</span>
<h2>{escape(journey["title"])}</h2>
<p class="section-lead">{escape(journey["description"])}</p>
<div class="answer-grid">
<div class="answer-card">
<h3>Save the current route</h3>
<p>{escape(save_summary)}</p>
<button type="button" class="btn" data-workspace-page-action="save-context">{escape(journey["workspace_action_label"])}</button>
</div>
<div class="answer-card">
<h3>Make it a task</h3>
<p>{escape(journey["task_summary"])}</p>
<button type="button" class="button-secondary" data-workspace-page-action="add-context-task">{escape(journey["task_action_label"])}</button>
</div>
<div class="answer-card">
<h3>Come back with context</h3>
<p>Open the local workspace or continue with the most useful next tool for this route.</p>
<div class="hero-ctas">
<a class="button-secondary" href="/my-planning-project/">Open workspace</a>
<a class="button-secondary" href="{escape(journey["next_tool_href"], quote=True)}">{escape(journey["next_tool_label"])}</a>
</div>
</div>
</div>
<div class="hero-ctas">
<a class="button-secondary" href="{escape(journey["lead_href"], quote=True)}" data-guidance-triage="{escape(guidance_route, quote=True)}">{escape(journey["lead_cta_label"])}</a>
</div>
<p class="result-capture-note" data-workspace-note="true" data-project-note="true">Stored only in this browser. Nothing is sent unless you submit a form.</p>
</section>
"""
