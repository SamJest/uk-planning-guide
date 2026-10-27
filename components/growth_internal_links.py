from __future__ import annotations

from html import escape

from data.search_demand_priorities import gsc_cluster_hub_for_family
from utils.live_links import is_live_internal_href


BASE_DONOR_CLUSTERS = {
    "change-of-use": ("hmo-article-4", "planning-portal"),
    "driveways": ("dropped-kerb-highway",),
    "dropped-kerbs": ("dropped-kerb-highway",),
    "fences-and-walls": ("conservation-map",),
}


def _clusters_for_project(project_slug: str, county_slug: str) -> tuple[str, ...]:
    project_slug = str(project_slug or "").strip()
    county_slug = str(county_slug or "").strip()
    if project_slug in {"garden-rooms", "outbuildings"}:
        if county_slug in {"scotland", "wales"}:
            return ("porch-outbuilding-rules", "conservation-map")
        return ("conservation-map",)
    return BASE_DONOR_CLUSTERS.get(project_slug, ())


def build_growth_internal_link_boost(project_slug: str, county_slug: str, town_slug: str) -> str:
    clusters = _clusters_for_project(project_slug, county_slug)
    if not clusters:
        return ""

    cards: list[str] = []
    for cluster in clusters:
        hub = gsc_cluster_hub_for_family(cluster)
        if not hub:
            continue
        href = f"/local-search/{hub['slug']}/"
        if hub.get("publication_status") == "blocked" or not is_live_internal_href(href):
            continue
        cards.append(
            f"""
<a class="card" href="{escape(href, quote=True)}">
<div class="card-kicker">Related route check</div>
<h3>{escape(hub["title"])}</h3>
<p>{escape(hub["summary"])}</p>
<span class="cta">Open route hub</span>
</a>
"""
        )

    if not cards:
        return ""

    return f"""
<section class="growth-link-boost" data-growth-link-boost="true" data-project-slug="{escape(project_slug, quote=True)}" data-authority-slug="{escape(town_slug, quote=True)}">
<span class="eyebrow">Useful next checks</span>
<h2>Related Routes That Often Change The Answer</h2>
<p class="section-lead">These links stay focused on connected planning questions, so the next page should narrow the route rather than send you into a broad index.</p>
<div class="grid">
{''.join(cards)}
</div>
</section>
"""
