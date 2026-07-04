from __future__ import annotations

from html import escape

from data.search_demand_priorities import (
    gsc_cluster_for_path,
    gsc_cluster_hub_for_path,
    gsc_expansion_candidates_for_family,
)


def _current_slug(path: str) -> str:
    clean = "/" + str(path or "").strip("/")
    if clean.startswith("/local-search/"):
        return clean.strip("/").split("/")[-1]
    return ""


def _card(href: str, kicker: str, title: str, body: str, cta: str) -> str:
    return f"""
<a class="card" href="{escape(href, quote=True)}">
<div class="card-kicker">{escape(kicker)}</div>
<h3>{escape(title)}</h3>
<p>{escape(body)}</p>
<span class="cta">{escape(cta)}</span>
</a>
"""


def build_gsc_cluster_links(path: str, *, limit: int = 4) -> str:
    cluster = gsc_cluster_for_path(path)
    if not cluster:
        return ""

    current = _current_slug(path)
    hub = gsc_cluster_hub_for_path(path)
    cards: list[str] = []

    if hub and hub.get("slug") != current:
        cards.append(
            _card(
                f"/local-search/{hub['slug']}/",
                "Cluster hub",
                hub["title"],
                "Use this first when the search belongs to a wider group of related local routes.",
                "Open hub",
            )
        )

    for item in gsc_expansion_candidates_for_family(cluster):
        if item["slug"] == current:
            continue
        cards.append(
            _card(
                f"/local-search/{item['slug']}/",
                "Related GSC route",
                item["title"],
                item["summary"],
                "Open related route",
            )
        )
        if len(cards) >= limit:
            break

    if not cards:
        return ""

    heading = hub.get("title", "Related GSC Routes") if hub else "Related GSC Routes"
    return f"""
<section class="local-search-routes gsc-cluster-links" data-gsc-cluster-links="true" data-gsc-cluster="{escape(cluster, quote=True)}">
<span class="eyebrow">GSC opportunity cluster</span>
<h2>{escape(heading)}</h2>
<p class="section-lead">These routes group similar June 2026 Search Console queries so visitors can move sideways when the exact authority, project or official-source check is slightly different.</p>
<div class="grid">
{''.join(cards)}
</div>
</section>
"""
