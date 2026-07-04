from __future__ import annotations

from html import escape

from components.building_regs_handoff import build_download_building_regs_handoff
from data.download_assets import DOWNLOAD_ASSETS, download_asset_path


def _link_cards(items: list[dict], *, cta: str) -> str:
    cards = []
    for item in items:
        cards.append(
            f"""
<a class="card" href="{escape(item['path'], quote=True)}">
<h3>{escape(item['label'])}</h3>
<p>Use this alongside the printable resource when the next step needs a deeper route check.</p>
<span class="cta">{escape(cta)}</span>
</a>
"""
        )
    return "".join(cards)


def _source_cards(items: list[dict]) -> str:
    cards = []
    for item in items:
        cards.append(
            f"""
<a class="official-source-link" href="{escape(item['url'], quote=True)}">
<strong>{escape(item['label'])}</strong>
<span>Official source</span>
<span>{escape(item.get('why', 'Useful for checking the current official route before relying on the checklist.'))}</span>
</a>
"""
        )
    return "".join(cards)


def _checklist_html(asset: dict) -> str:
    sections = []
    for section in asset["checklist_sections"]:
        items = "".join(f"<li>{escape(item)}</li>" for item in section["items"])
        sections.append(
            f"""
<div class="download-checklist-group">
<h3>{escape(section['heading'])}</h3>
<ul class="download-checklist-items">{items}</ul>
</div>
"""
        )
    return "".join(sections)


def _ordered(items: list[str]) -> str:
    return "".join(f"<li>{escape(item)}</li>" for item in items)


def _unordered(items: list[str]) -> str:
    return "".join(f"<li>{escape(item)}</li>" for item in items)


def _citation_text(asset: dict) -> str:
    return (
        f"UK Planning Guide, {asset['title']}, last checked {asset['last_checked']}, "
        f"https://ukplanningguide.co.uk{download_asset_path(asset)}"
    )


def render_download_asset_page(asset: dict) -> str:
    related_tools = _link_cards(asset.get("related_tools", []), cta="Open tool")
    related_guides = _link_cards(asset.get("related_guides", []), cta="Open guide")
    official_sources = _source_cards(asset.get("official_sources", []))
    citation = _citation_text(asset)

    return f"""
<main class="download-asset" data-download-asset="{escape(asset['slug'], quote=True)}" data-asset-type="{escape(asset['asset_type'], quote=True)}" data-project-family="{escape(asset['project_family'], quote=True)}">
<section class="hero download-hero">
<span class="badge">Free printable {escape(asset['asset_type'].replace('-', ' '))}</span>
<h1>{escape(asset['title'])}</h1>
<p>{escape(asset['summary'])}</p>
<div class="download-meta">
<span><strong>Last checked</strong>{escape(asset['last_checked'])}</span>
<span><strong>Use for</strong>{escape(asset['audience'])}</span>
<span><strong>Format</strong>Print-friendly HTML</span>
</div>
<div class="download-actions">
<button type="button" data-download-action="print" data-asset-slug="{escape(asset['slug'], quote=True)}">{escape(asset['download_label'])}</button>
<button class="button-secondary" type="button" data-download-action="copy-link" data-asset-slug="{escape(asset['slug'], quote=True)}">Copy link</button>
<button class="button-secondary" type="button" data-download-action="copy-text" data-asset-slug="{escape(asset['slug'], quote=True)}">Copy checklist text</button>
</div>
<p class="download-action-note" data-download-status aria-live="polite">Use the print button to save as PDF from your browser.</p>
</section>

<section class="download-intro">
<span class="eyebrow">What this helps with</span>
<h2>Use This Before The Project Becomes Expensive</h2>
<p>This resource is designed for early planning decisions. It helps you name the issue, record the obvious checks and avoid paying for drawings, applications or contractor commitments before the planning route is clear enough.</p>
<div class="answer-grid">
<div class="answer-card">
<h3>Good use</h3>
<p>Print it, mark it up, save the source links and use it as a short agenda for a council, designer, consultant or builder conversation.</p>
</div>
<div class="answer-card">
<h3>Not a decision</h3>
<p>It is not a formal certificate, approval, legal opinion or replacement for checking the exact property, council and design.</p>
</div>
<div class="answer-card">
<h3>Best next step</h3>
<p>{escape(asset['cta_next_step'])} when the checklist shows the route is still unclear or locally sensitive.</p>
</div>
</div>
</section>

<section class="download-route">
<span class="eyebrow">Quick route check</span>
<h2>Work Through These First</h2>
<ol class="download-route-list">{_ordered(asset['quick_route'])}</ol>
</section>

<section class="download-checklist" data-download-copy-source>
<span class="eyebrow">Homeowner checklist</span>
<h2>{escape(asset['title'])}</h2>
<p class="section-lead">Tick these off on paper or copy the text into your project notes. Keep any official links, screenshots and dates with the project record.</p>
{_checklist_html(asset)}
</section>

<section class="download-mistakes">
<span class="eyebrow">Common mistakes</span>
<h2>Things Worth Avoiding</h2>
<ul class="checklist">{_unordered(asset['common_mistakes'])}</ul>
</section>

<section class="download-questions">
<span class="eyebrow">Ask before spending money</span>
<h2>Questions To Put To The Council Or A Professional</h2>
<ul class="checklist">{_unordered(asset['questions_to_ask'])}</ul>
</section>

<section class="official-sources download-sources" id="official-sources" data-official-sources="true" data-download-official-sources="true">
<span class="eyebrow">Official sources checked</span>
<h2>Official Sources Worth Opening Next</h2>
<p class="section-lead">Use these as starting points and then check the relevant council page for the property. Rules, validation requirements and local controls can change by authority and site.</p>
<div class="official-sources-list">{official_sources}</div>
</section>

<section class="download-related">
<span class="eyebrow">Related UKPlanningGuide tools</span>
<h2>Use With These Tools</h2>
<div class="grid">{related_tools}</div>
</section>

<section class="download-related">
<span class="eyebrow">Related guides</span>
<h2>Read The Guide Behind The Checklist</h2>
<div class="grid">{related_guides}</div>
</section>

{build_download_building_regs_handoff(asset["slug"])}

<section class="download-citation">
<span class="eyebrow">Share or cite</span>
<h2>Clean Citation Text</h2>
<p>Use this when sharing the resource with a neighbour, designer, builder or adviser.</p>
<textarea class="download-citation-text" readonly rows="3">{escape(citation)}</textarea>
<button class="button-secondary" type="button" data-download-action="copy-citation" data-asset-slug="{escape(asset['slug'], quote=True)}">Copy citation</button>
</section>

<section class="download-disclaimer">
<span class="eyebrow">Important</span>
<h2>General Guidance Only</h2>
<p>{escape(asset['print_disclaimer'])}</p>
<p>Before relying on a borderline route, confirm the latest position with official sources, the local planning authority or a suitable professional.</p>
</section>
</main>
"""


def render_download_assets_index() -> str:
    cards = []
    for asset in DOWNLOAD_ASSETS:
        cards.append(
            f"""
<a class="card" href="{download_asset_path(asset)}">
<div class="card-kicker">{escape(asset['asset_type'].replace('-', ' '))}</div>
<h3>{escape(asset['title'])}</h3>
<p>{escape(asset['summary'])}</p>
<span class="cta">Open printable resource</span>
</a>
"""
        )

    return f"""
<section class="hero">
<span class="badge">Free planning downloads</span>
<h1>Printable Planning Checklists And Worksheets</h1>
<p>Use these crawlable, printable resources before you spend money on drawings, applications, contractors or a route that still needs one obvious check.</p>
<div class="hero-ctas">
<a class="btn" href="/tools/">Use planning tools</a>
<a class="btn button-secondary" href="/my-planning-project/">Open My Planning Project</a>
</div>
</section>

<section>
<span class="eyebrow">Download library</span>
<h2>Pick The Checklist That Matches The Decision</h2>
<p class="section-lead">Each page can be printed, copied, cited and shared. The HTML page is the main resource; browser print is the PDF path when someone wants a saved copy.</p>
<div class="grid download-index-grid">{''.join(cards)}</div>
</section>
"""


def render_download_asset_cards_for_path(path: str, assets: list[dict]) -> str:
    if not assets:
        return ""

    cards = []
    for asset in assets:
        cards.append(
            f"""
<a class="card" href="{download_asset_path(asset)}">
<div class="card-kicker">Printable {escape(asset['asset_type'].replace('-', ' '))}</div>
<h3>{escape(asset['title'])}</h3>
<p>{escape(asset['summary'])}</p>
<span class="cta">Open checklist</span>
</a>
"""
        )

    return f"""
<section class="download-related-assets" data-download-internal-links="true">
<span class="eyebrow">Free printable resources</span>
<h2>Checklists To Use With This Page</h2>
<p class="section-lead">These printable resources turn the route into a short evidence and question list before the project moves into paid work.</p>
<div class="grid">{''.join(cards)}</div>
</section>
"""
