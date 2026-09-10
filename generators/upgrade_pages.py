from __future__ import annotations

import csv
import json
import re
import shutil
from html import escape
from pathlib import Path

from components.upgrade_components import (
    build_save_export_cta,
    build_upgrade_summary_panel,
    dataset_schema,
    item_list_schema,
    service_schema,
)
from core.files import write_file
from core.paths import BASE_URL, OUTPUT_FOLDER, ROOT
from core.render import inject_into_base
from data.data_assets import DATA_ASSETS, MONETISATION_SURFACES
from utils.route_contracts import (
    RouteContract,
    normalize_path,
    output_path_for_route,
    route_contract_for_legacy_path,
)
from utils.content_contracts import page_records_by_route
from utils.url_registry import load_redirects


ARTIFACT_DIR = ROOT / "artifacts" / "upgrade"
ROUTE_INVENTORY_CSV = ARTIFACT_DIR / "route-inventory.csv"
ROUTE_INVENTORY_JSON = ARTIFACT_DIR / "route-inventory.json"
REDIRECT_MAP_CSV = ARTIFACT_DIR / "redirect-map.csv"
REDIRECT_MAP_JSON = ARTIFACT_DIR / "redirect-map.json"
MAX_COUNTRY_ALIASES = 900
PRIORITY_PROJECT_ALIASES = {
    "house-extensions",
    "garden-rooms",
    "dropped-kerbs",
    "hmos",
    "outbuildings",
    "loft-conversions",
}

CANONICAL_PATTERN = re.compile(r'(<link rel="canonical" href=")[^"]*(")', re.IGNORECASE)
OG_URL_PATTERN = re.compile(r'(<meta property="og:url" content=")[^"]*(")', re.IGNORECASE)
SCHEMA_URL_PATTERN = re.compile(r'https://ukplanningguide\.co\.uk/[^" <]+')
ROBOTS_META_PATTERN = re.compile(
    r'<meta\s+name=["\']robots["\']\s+content=["\'][^"\']*["\']\s*/?>\s*',
    re.IGNORECASE,
)


def _expected_url_for_page(page: Path) -> str:
    rel = str(page.relative_to(OUTPUT_FOLDER)).replace("\\", "/")
    if rel.endswith("index.html"):
        rel = rel[:-10]
    return normalize_path("/" + rel)


def _write_json(path: Path, payload) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")


def _rewrite_canonical_markers(html: str, old_url: str, new_url: str) -> str:
    updated = CANONICAL_PATTERN.sub(rf"\1{new_url}\2", html)
    updated = OG_URL_PATTERN.sub(rf"\1{new_url}\2", updated)
    updated = updated.replace(f'"url": "{old_url}"', f'"url": "{new_url}"')
    updated = updated.replace(f'"@id": "{old_url}"', f'"@id": "{new_url}"')
    updated = updated.replace(f'"item": "{old_url}"', f'"item": "{new_url}"')
    updated = SCHEMA_URL_PATTERN.sub(lambda match: new_url if match.group(0).rstrip("/") == old_url.rstrip("/") else match.group(0), updated)
    return updated


def _canonical_alias_html(source_page: Path, contract: RouteContract) -> str:
    html = source_page.read_text(encoding="utf-8", errors="ignore")
    old_url = BASE_URL.rstrip("/") + contract.source_path
    html = _rewrite_canonical_markers(html, old_url, contract.canonical_url)
    declared_record = page_records_by_route().get(contract.canonical_path)
    if declared_record and declared_record.get("index_status") == "index":
        # Incremental builds may read a legacy source after it has already been
        # converted into a noindex bridge. The reviewed canonical contract wins.
        html = ROBOTS_META_PATTERN.sub("", html)
    return html


def _apply_static_redirect_bridges() -> None:
    for redirect in load_redirects():
        if redirect["status_code"] == 410:
            continue
        bridge_page = output_path_for_route(redirect["source_path"], OUTPUT_FOLDER)
        if not bridge_page.exists():
            continue
        html = bridge_page.read_text(encoding="utf-8", errors="ignore")
        target_url = BASE_URL.rstrip("/") + redirect["target_path"]
        html = CANONICAL_PATTERN.sub(rf"\1{target_url}\2", html)
        html = OG_URL_PATTERN.sub(rf"\1{target_url}\2", html)
        if 'name="robots"' not in html.lower():
            html = html.replace("</head>", '<meta name="robots" content="noindex, follow">\n</head>', 1)
        elif "noindex" not in html.lower():
            html = re.sub(
                r'<meta\s+name="robots"\s+content="[^"]*">',
                '<meta name="robots" content="noindex, follow">',
                html,
                count=1,
                flags=re.IGNORECASE,
            )
        bridge_notice = (
            '<section class="notice" data-static-redirect-bridge="true">'
            '<h2>This page has moved</h2>'
            f'<p><a href="{escape(redirect["target_path"], quote=True)}">Open the current country-first page.</a></p>'
            "</section>"
        )
        html = html.replace('<main class="container" id="main-content"', bridge_notice + '<main class="container" id="main-content"', 1)
        write_file(bridge_page.parent, bridge_page.name, html)


def _write_contract_outputs(contracts: list[RouteContract]) -> None:
    rows = [contract.to_dict() for contract in contracts]
    ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)
    _write_json(ROUTE_INVENTORY_JSON, rows)
    with ROUTE_INVENTORY_CSV.open("w", newline="", encoding="utf-8") as handle:
        fieldnames = [
            "country",
            "intent_type",
            "canonical_path",
            "canonical_url",
            "legacy_paths",
            "indexability",
            "project_slug",
            "process_slug",
            "rule_slug",
            "authority_slug",
            "source_path",
        ]
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            row = dict(row)
            row["legacy_paths"] = ";".join(row.get("legacy_paths") or [])
            writer.writerow({key: row.get(key, "") for key in fieldnames})

    redirects = [
        {
            "old_url": legacy,
            "new_url": contract.canonical_path,
            "status": 301,
            "reason": "Country-first canonical migration target",
            "priority": "High" if contract.intent_type in {"projects", "rules", "councils"} else "Medium",
        }
        for contract in contracts
        for legacy in contract.legacy_paths
        if legacy != contract.canonical_path
    ]
    _write_json(REDIRECT_MAP_JSON, redirects)
    with REDIRECT_MAP_CSV.open("w", newline="", encoding="utf-8") as handle:
        fieldnames = ["old_url", "new_url", "status", "reason", "priority"]
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(redirects)


def _generate_country_hub(country: str, intent: str, title: str, summary: str, items: list[dict]) -> None:
    canonical_path = f"/{country}/{intent}/"
    canonical_url = BASE_URL.rstrip("/") + canonical_path
    cards = "\n".join(
        f"""<a class="card" href="{escape(item['href'], quote=True)}">
<h3>{escape(item['title'])}</h3>
<p>{escape(item.get('summary', 'Open the canonical country-first page.'))}</p>
</a>"""
        for item in items[:48]
    )
    content = f"""
<section class="hero">
<span class="eyebrow">Country-first architecture</span>
<h1>{escape(title)}</h1>
<p>{escape(summary)}</p>
</section>
{build_upgrade_summary_panel(
    page_type=f"{country.title()} {intent} hub",
    legal_scope=f"{country.title()} planning context unless a page says otherwise.",
    what_changes="Local authority restrictions, exact property status, project scale, planning history and special controls.",
    official_source_basis="Official source cards on the destination page should explain the national and local footing.",
    stop_point="Move from the hub into the specific project, rule, process or council page once a decision depends on exact facts.",
)}
<section>
<h2>Canonical Pages</h2>
<div class="card-grid">{cards}</div>
</section>
"""
    html = inject_into_base(
        title=title,
        content=content,
        options={
            "breadcrumbs": [("Home", "/"), (country.title(), f"/{country}/"), (intent.title(), "")],
            "schema": item_list_schema(title, canonical_url, [{"title": item["title"], "url": BASE_URL.rstrip("/") + item["href"]} for item in items[:48]]),
        },
        canonical_url=canonical_url,
        meta_description=summary,
    )
    write_file(OUTPUT_FOLDER / country / intent, "index.html", html)


def _should_generate_alias(contract: RouteContract) -> bool:
    parts = [part for part in contract.source_path.strip("/").split("/") if part]
    if contract.intent_type in {"tools", "process", "rules", "councils"}:
        return len(parts) <= 2
    if contract.intent_type == "projects":
        if len(parts) >= 4:
            return False
        if not contract.authority_slug:
            return len(parts) == 1 or contract.project_slug in PRIORITY_PROJECT_ALIASES
        return contract.project_slug in PRIORITY_PROJECT_ALIASES and not contract.rule_slug
    return False


def _alias_priority(contract: RouteContract) -> tuple[int, str]:
    parts = [part for part in contract.source_path.strip("/").split("/") if part]
    if contract.intent_type == "process":
        return (0, contract.source_path)
    if contract.intent_type == "tools":
        return (1, contract.source_path)
    if contract.intent_type == "projects" and len(parts) == 1:
        return (2, contract.source_path)
    if contract.intent_type == "rules" and len(parts) == 1:
        return (3, contract.source_path)
    if contract.intent_type == "councils" and contract.authority_slug:
        return (4, contract.source_path)
    if contract.intent_type == "projects" and contract.authority_slug:
        return (5, contract.source_path)
    if contract.intent_type == "rules" and contract.authority_slug:
        return (6, contract.source_path)
    return (9, contract.source_path)


def _select_alias_candidates(
    candidates: list[tuple[RouteContract, Path]],
    required_paths: set[str],
) -> list[tuple[RouteContract, Path]]:
    """Keep the capped cohort and append reviewed contracts that fall outside it."""
    ranked = sorted(candidates, key=lambda item: _alias_priority(item[0]))
    selected = list(ranked[:MAX_COUNTRY_ALIASES])
    selected_paths = {contract.canonical_path for contract, _ in selected}
    selected.extend(
        (contract, source_page)
        for contract, source_page in ranked[MAX_COUNTRY_ALIASES:]
        if contract.canonical_path in required_paths and contract.canonical_path not in selected_paths
    )
    return selected


def _generate_country_root(country: str, items_by_intent: dict[str, list[dict]]) -> None:
    canonical_path = f"/{country}/"
    canonical_url = BASE_URL.rstrip("/") + canonical_path
    links = []
    for intent, items in items_by_intent.items():
        if items:
            links.append({"title": intent.replace("-", " ").title(), "href": f"/{country}/{intent}/", "summary": f"Browse {country.title()} {intent.replace('-', ' ')}."})
    content = f"""
<section class="hero">
<span class="eyebrow">Planning system</span>
<h1>{escape(country.replace('-', ' ').title())} Planning Guide</h1>
<p>Country-first routing keeps planning guidance legally clearer and prevents one generic UK answer being reused where local systems differ.</p>
</section>
<section>
<h2>Start With The Right Intent</h2>
<div class="card-grid">
{''.join(f'<a class="card" href="{escape(item["href"], quote=True)}"><h3>{escape(item["title"])}</h3><p>{escape(item["summary"])}</p></a>' for item in links)}
</div>
</section>
"""
    html = inject_into_base(
        title=f"{country.replace('-', ' ').title()} planning guide",
        content=content,
        options={
            "breadcrumbs": [("Home", "/"), (country.replace("-", " ").title(), "")],
            "schema": item_list_schema(f"{country.title()} planning guide sections", canonical_url, [{"title": item["title"], "url": BASE_URL.rstrip("/") + item["href"]} for item in links]),
        },
        canonical_url=canonical_url,
        meta_description=f"Browse country-first planning projects, rules, process guides, councils, data assets and tools for {country.replace('-', ' ').title()}.",
    )
    write_file(OUTPUT_FOLDER / country, "index.html", html)


def generate_country_aliases() -> None:
    print("Generating country-first canonical aliases and route inventory")
    contracts: list[RouteContract] = []
    by_intent: dict[str, dict[str, list[dict]]] = {}

    candidates: list[tuple[RouteContract, Path]] = []
    for source_page in sorted(OUTPUT_FOLDER.rglob("index.html")):
        rel_parts = source_page.relative_to(OUTPUT_FOLDER).parts
        if not rel_parts or rel_parts[0] in {"assets", "sitemaps"}:
            continue
        source_path = _expected_url_for_page(source_page)
        contract = route_contract_for_legacy_path(source_path)
        if not contract or contract.canonical_path == source_path:
            continue
        if not _should_generate_alias(contract):
            continue
        candidates.append((contract, source_page))

    required_paths = set(page_records_by_route())
    for contract, source_page in _select_alias_candidates(candidates, required_paths):

        target_page = output_path_for_route(contract.canonical_path, OUTPUT_FOLDER)
        if target_page == source_page:
            continue
        if not write_file(target_page.parent, target_page.name, _canonical_alias_html(source_page, contract)):
            continue
        contracts.append(contract)
        by_intent.setdefault(contract.country, {}).setdefault(contract.intent_type, []).append(
            {
                "title": contract.canonical_path.strip("/").replace("-", " ").replace("/", " / ").title(),
                "href": contract.canonical_path,
                "summary": "Country-first canonical alias generated from the current production page.",
            }
        )

    for country, intents in sorted(by_intent.items()):
        _generate_country_root(country, intents)
        for intent, items in sorted(intents.items()):
            _generate_country_hub(
                country,
                intent,
                f"{country.replace('-', ' ').title()} {intent.replace('-', ' ')}",
                f"Canonical {intent.replace('-', ' ')} pages for {country.replace('-', ' ').title()}, grouped under the country-first information architecture.",
                items,
            )

    _write_contract_outputs(contracts)
    _apply_static_redirect_bridges()
    print(f"Country-first aliases generated: {len(contracts)}")


def generate_data_asset_pages() -> None:
    print("Generating data-asset scaffolding")
    index_items = [
        {"title": asset["title"], "slug": asset["slug"], "url": f"{BASE_URL}/england/data/{asset['slug']}/"}
        for asset in DATA_ASSETS
    ]
    index_url = f"{BASE_URL}/england/data/"
    index_content = f"""
<section class="hero">
<span class="eyebrow">Planning data</span>
<h1>Planning Data Assets</h1>
<p>Source-backed council data resources for repeat visits, local checks and future downloadable packs. Incomplete datasets stay clearly labelled until verified.</p>
</section>
<section>
<h2>Available Data Resources</h2>
<div class="card-grid">
{''.join(f'<a class="card" href="/england/data/{escape(asset["slug"], quote=True)}/"><h3>{escape(asset["title"])}</h3><p>{escape(asset["summary"])}</p></a>' for asset in DATA_ASSETS)}
</div>
</section>
"""
    html = inject_into_base(
        title="Planning data assets: council links, fees and restrictions",
        content=index_content,
        options={
            "breadcrumbs": [("Home", "/"), ("England", "/england/"), ("Data", "")],
            "schema": item_list_schema("Planning data assets", index_url, index_items),
        },
        canonical_url=index_url,
        meta_description="Browse source-backed planning data assets for council profiles, pre-app fees, validation requirements, HMO Article 4 and council packs.",
    )
    write_file(OUTPUT_FOLDER / "england" / "data", "index.html", html)

    for asset in DATA_ASSETS:
        canonical_url = f"{BASE_URL}/england/data/{asset['slug']}/"
        content = f"""
<section class="hero">
<span class="eyebrow">Data asset</span>
<h1>{escape(asset['title'])}</h1>
<p>{escape(asset['summary'])}</p>
</section>
{build_upgrade_summary_panel(
    page_type="Data/tool landing page",
    legal_scope="England-first scaffold unless a record states a devolved-country source.",
    what_changes="The page should only become fully indexable where source URLs, update dates and methodology are present.",
    official_source_basis=asset["source_basis"],
    stop_point="Do not rely on this scaffold as a complete local answer until the individual council row has been source-checked.",
)}
<section>
<h2>Source And Update Method</h2>
<p><strong>Launch phase:</strong> {escape(asset['phase'])}</p>
<p><strong>Status:</strong> {escape(asset['status'])}</p>
<p><strong>Source basis:</strong> {escape(asset['source_basis'])}</p>
</section>
{build_save_export_cta(page_family="data", country="england", primary_label="Check my route", secondary_label="Save data summary")}
"""
        html = inject_into_base(
            title=asset["title"],
            content=content,
            options={
                "breadcrumbs": [("Home", "/"), ("England", "/england/"), ("Data", "/england/data/"), (asset["title"], "")],
                "schema": dataset_schema(asset, canonical_url),
            },
            canonical_url=canonical_url,
            meta_description=asset["summary"],
        )
        write_file(OUTPUT_FOLDER / "england" / "data" / asset["slug"], "index.html", html)


def generate_monetisation_pages() -> None:
    print("Generating launch-gated monetisation scaffolding")
    index_url = f"{BASE_URL}/england/services/"
    index_content = f"""
<section class="hero">
<span class="eyebrow">Future services</span>
<h1>Planning Service Options</h1>
<p>These service pages are prepared for future launch. The free guides, tools and official-source checks stay useful first; paid or referral routes will only open when fulfilment, consent and privacy workflows are ready.</p>
</section>
<section>
<h2>Service Scaffolds</h2>
<div class="card-grid">
{''.join(f'<a class="card" href="/england/services/{escape(surface["slug"], quote=True)}/"><h3>{escape(surface["title"])}</h3><p>{escape(surface["summary"])}</p></a>' for surface in MONETISATION_SURFACES)}
</div>
</section>
"""
    html = inject_into_base(
        title="Planning service options",
        content=index_content,
        options={
            "breadcrumbs": [("Home", "/"), ("England", "/england/"), ("Services", "")],
            "schema": item_list_schema(
                "Planning service options",
                index_url,
                [
                    {"title": surface["title"], "url": f"{BASE_URL}/england/services/{surface['slug']}/"}
                    for surface in MONETISATION_SURFACES
                ],
            ),
            "meta_robots": "noindex, follow",
        },
        canonical_url=index_url,
        meta_description="Browse future planning service options for reviewed route reports, council packs and professional referrals.",
    )
    write_file(OUTPUT_FOLDER / "england" / "services", "index.html", html)

    for surface in MONETISATION_SURFACES:
        canonical_url = f"{BASE_URL}/england/services/{surface['slug']}/"
        content = f"""
<section class="hero">
<span class="eyebrow">Future service</span>
<h1>{escape(surface['title'])}</h1>
<p>{escape(surface['summary'])}</p>
</section>
<section class="notice">
<h2>Coming Soon</h2>
<p>This service is not available yet. Free guidance, official sources and consent-led next steps remain the first route until the service is ready.</p>
</section>
{build_upgrade_summary_panel(
    page_type="Service landing page",
    legal_scope="United Kingdom service scaffold; page copy must stay clear about country-specific planning differences.",
    what_changes="Launch readiness, fulfilment process, partner availability, payment setup and privacy notice updates.",
    official_source_basis="The service must summarise official sources rather than replace formal council or professional decisions.",
    stop_point="Do not enable checkout or referrals until consent, disclosure, fulfilment and review workflow are ready.",
)}
"""
        html = inject_into_base(
            title=surface["title"],
            content=content,
            options={
                "breadcrumbs": [("Home", "/"), ("England", "/england/"), ("Services", "/england/services/"), (surface["title"], "")],
                "schema": service_schema(surface, canonical_url, enabled=False),
                "meta_robots": "noindex, follow",
            },
            canonical_url=canonical_url,
            meta_description=surface["summary"],
        )
        write_file(OUTPUT_FOLDER / "england" / "services" / surface["slug"], "index.html", html)


def generate_phase_zero_update() -> None:
    canonical_url = f"{BASE_URL}/updates/phase-0-integrity-repair/"
    content = """
<section class="hero">
<span class="eyebrow">Site update</span>
<h1>Phase 0 integrity repair</h1>
<p>UK Planning Guide is testing stricter page-family, source, jurisdiction and URL controls on a limited canary set before any wider regeneration.</p>
</section>
<section>
<h2>What this update covers</h2>
<ul class="checklist">
<li>Explicit page records instead of inferred project context.</li>
<li>Traceable source IDs and separate source-check dates.</li>
<li>Contamination checks for project, rule and jurisdiction leakage.</li>
<li>A twenty-route canary that remains isolated from the live output.</li>
</ul>
</section>
<section class="notice">
<h2>Review status</h2>
<p>This is a source-controlled release note for human review. It remains noindex and is excluded from sitemaps until Phase 0 is approved.</p>
</section>
"""
    html = inject_into_base(
        title="Phase 0 integrity repair | UK Planning Guide",
        content=content,
        options={
            "breadcrumbs": [("Home", "/"), ("Phase 0 integrity repair", "")],
            "meta_robots": "noindex, follow",
        },
        canonical_url=canonical_url,
        meta_description="A review-only update on UK Planning Guide's Phase 0 content integrity and source-control canary.",
    )
    write_file(OUTPUT_FOLDER / "updates" / "phase-0-integrity-repair", "index.html", html)


def generate_upgrade_pages() -> None:
    for country_dir in ("england", "scotland", "wales", "northern-ireland"):
        target = OUTPUT_FOLDER / country_dir
        if target.exists():
            shutil.rmtree(target)
    generate_country_aliases()
    generate_data_asset_pages()
    generate_monetisation_pages()
    generate_phase_zero_update()
