from __future__ import annotations

import json
from html import escape

from core.paths import BASE_URL


def build_upgrade_summary_panel(
    *,
    page_type: str,
    legal_scope: str,
    what_changes: str,
    official_source_basis: str,
    stop_point: str,
) -> str:
    return f"""
<section class="upgrade-summary-panel" data-upgrade-summary="true">
<span class="eyebrow">Route clarity</span>
<h2>What To Check Before You Rely On The Answer</h2>
<div class="answer-grid">
<div class="answer-card">
<h3>Page type</h3>
<p>{escape(page_type)}</p>
</div>
<div class="answer-card">
<h3>Legal scope</h3>
<p>{escape(legal_scope)}</p>
</div>
<div class="answer-card">
<h3>What changes the answer</h3>
<p>{escape(what_changes)}</p>
</div>
<div class="answer-card">
<h3>Official-source basis</h3>
<p>{escape(official_source_basis)}</p>
</div>
</div>
<div class="notice">
<strong>When broad guidance stops being enough</strong>
<p>{escape(stop_point)}</p>
</div>
</section>
"""


def build_save_export_cta(
    *,
    page_family: str,
    country: str = "",
    project_slug: str = "",
    authority_slug: str = "",
    primary_label: str = "Check the likely route",
    secondary_label: str = "Save or email summary",
) -> str:
    attrs = {
        "data-route-cta": "true",
        "data-page-family": page_family,
        "data-country": country,
        "data-project-slug": project_slug,
        "data-authority-slug": authority_slug,
    }
    attr_html = " ".join(f'{escape(key)}="{escape(value, quote=True)}"' for key, value in attrs.items())
    return f"""
<section class="route-retention-cta" {attr_html}>
<span class="eyebrow">Next step</span>
<h2>Keep This Planning Route With Your Project Notes</h2>
<p>Use the free route check first. If the answer depends on local restrictions, evidence or a borderline measurement, keep the summary and official links together before spending more money.</p>
<div class="hero-ctas">
<a class="cta" href="/tools/planning-route-check/" data-retention-action="route_started">{escape(primary_label)}</a>
<button class="button-secondary" type="button" data-retention-action="summary_saved">{escape(secondary_label)}</button>
<button class="button-secondary" type="button" data-retention-action="council_pack_downloaded">Export council pack</button>
</div>
<p class="guidance-consent-note">Summary and export actions are designed to use non-sensitive route context only. Do not put names, addresses or full project notes into analytics.</p>
</section>
"""


def build_sticky_action_bar() -> str:
    return """
<div class="sticky-action-bar" data-sticky-action-bar="true" data-nosnippet>
<a href="/tools/planning-route-check/" data-sticky-action="route_started">Check route</a>
<button type="button" data-sticky-action="summary_saved">Save</button>
<button type="button" data-sticky-action="council_pack_downloaded">Export</button>
<a href="/planning-help/" data-sticky-action="premium_report_viewed">Reviewed report</a>
</div>
"""


def dataset_schema(asset: dict, canonical_url: str) -> dict:
    return {
        "@type": "Dataset",
        "@id": canonical_url.rstrip("/") + "#dataset",
        "name": asset["schema_name"],
        "description": asset["summary"],
        "url": canonical_url,
        "creator": {"@id": BASE_URL.rstrip("/") + "/#organization"},
        "license": BASE_URL.rstrip("/") + "/editorial-policy/",
        "isAccessibleForFree": True,
        "dateModified": "2026-05-31",
        "variableMeasured": [
            "official source URL",
            "local planning route",
            "source freshness",
            "council-specific status",
        ],
    }


def service_schema(surface: dict, canonical_url: str, *, enabled: bool = False) -> dict:
    return {
        "@type": "Service",
        "@id": canonical_url.rstrip("/") + "#service",
        "name": surface["title"],
        "serviceType": surface["service_type"],
        "description": surface["summary"],
        "provider": {"@id": BASE_URL.rstrip("/") + "/#organization"},
        "areaServed": "United Kingdom",
        "url": canonical_url,
        "isRelatedTo": BASE_URL.rstrip("/") + "/planning-help/",
        "additionalProperty": {
            "@type": "PropertyValue",
            "name": "Launch status",
            "value": "Disabled until launch" if not enabled else "Available",
        },
    }


def item_list_schema(name: str, canonical_url: str, items: list[dict]) -> dict:
    return {
        "@type": "ItemList",
        "@id": canonical_url.rstrip("/") + "#item-list",
        "name": name,
        "url": canonical_url,
        "itemListElement": [
            {
                "@type": "ListItem",
                "position": index,
                "name": item.get("title") or item.get("name") or item.get("slug"),
                "url": item.get("url") or canonical_url.rstrip("/") + "/" + item.get("slug", "").strip("/") + "/",
            }
            for index, item in enumerate(items, start=1)
        ],
    }


def json_script(data: dict) -> str:
    return f'<script type="application/json" data-upgrade-contract="true">{escape(json.dumps(data, sort_keys=True), quote=False)}</script>'
