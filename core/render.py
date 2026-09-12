import re
from datetime import date, datetime
from html import escape

from components.page_authority import build_authority_schema_bundle, build_page_trust_strip
from components.seo import refine_metadata, render_schema_markup
from components.shared_components import render_tool_ui_templates
from components.upgrade_components import build_sticky_action_bar
from core.paths import TEMPLATES_FOLDER
from utils.copy_tone import polish_html_copy
from utils.content_contracts import absolute_url, render_record_for_url
from utils.source_registry import sources_for_page


def _normalize_href(href: str) -> str:
    clean = str(href or "").strip()
    if not clean or clean.startswith(("http://", "https://", "#", "/")):
        return clean
    return "/" + clean.lstrip("/")


def _render_breadcrumbs(breadcrumbs) -> str:
    if not breadcrumbs:
        return ""

    if isinstance(breadcrumbs, str):
        return breadcrumbs

    parts = []
    for label, href in breadcrumbs:
        text = escape(str(label))
        if href:
            parts.append(f'<a href="{escape(_normalize_href(href), quote=True)}">{text}</a>')
        else:
            parts.append(f"<span>{text}</span>")

    if not parts:
        return ""

    return '<nav class="breadcrumbs" aria-label="Breadcrumbs">' + "".join(parts) + "</nav>"


def _is_inner_page(canonical_url: str) -> bool:
    clean = str(canonical_url or "").strip().rstrip("/")
    if not clean:
        return False
    return clean != "https://ukplanningguide.co.uk"


def _render_trust_strip(year) -> str:
    month_year = datetime.now().strftime("%B %Y")
    return (
        '<div class="page-trust-strip" data-nosnippet>'
        '<div class="page-trust-strip-heading">'
        "<strong>Editorially checked</strong>"
        "<span>Visible ownership, review date and source footing for this page.</span>"
        "</div>"
        '<div class="page-trust-strip-items">'
        f"<span><strong>Last reviewed</strong>{month_year}</span>"
        "<span><strong>Source footing</strong>National planning guidance, local context and page-specific tripwires.</span>"
        "<span><strong>Verify before spending</strong>Use a formal check when the proposal is close to a limit or affected by special controls.</span>"
        "</div>"
        "</div>"
    )


def _display_date(value: str) -> str:
    try:
        parsed = date.fromisoformat(str(value or ""))
    except ValueError:
        return str(value or "Not yet verified")
    return f"{parsed.day} {parsed.strftime('%B %Y')}"


def _render_contract_trust_strip(record: dict) -> str:
    from utils.trust_status import trust_status
    state = trust_status(record)
    verified = _display_date(record.get("verified_at")) if state.verification == "verified" else "Not yet verified"
    confidence = f"<span><strong>Confidence</strong>{escape(state.confidence.title())}</span>" if state.confidence else ""
    return (
        '<div class="page-trust-strip" data-nosnippet data-contract-trust="true">'
        '<div class="page-trust-strip-heading">'
        "<strong>Prepared under the UK Planning Guide editorial process</strong>"
        '<span><a href="/methodology/">How the review works</a></span>'
        "</div>"
        '<div class="page-trust-strip-items">'
        f"<span><strong>Content updated</strong>{escape(_display_date(record['content_updated_at']))}</span>"
        f"<span><strong>Sources checked</strong>{escape(verified)}</span>"
        f"{confidence}"
        "<span><strong>Important</strong>General planning information, not legal advice or formal approval.</span>"
        "</div>"
        "</div>"
    )


def _render_contract_source_panel(record: dict) -> str:
    sources = sources_for_page(record)
    source_lookup = {source["source_id"]: source for source in sources}
    claim_items = []
    for claim in record.get("claims", []):
        links = []
        for source_id in claim.get("source_ids", []):
            source = source_lookup.get(source_id)
            if not source:
                continue
            links.append(
                f'<a href="{escape(source["url"], quote=True)}" data-source-id="{escape(source_id, quote=True)}">'
                f'{escape(source["title"])}</a>'
            )
        claim_items.append(
            '<li data-claim-id="{claim_id}"><span>{text}</span><span class="claim-sources">{sources}</span></li>'.format(
                claim_id=escape(claim["claim_id"], quote=True),
                text=escape(claim["text"]),
                sources="; ".join(links),
            )
        )

    source_items = []
    for source in sources:
        source_items.append(
            '<li><a href="{url}" data-source-id="{source_id}">{title}</a>'
            '<span>{publisher} · checked {checked} · {status}</span></li>'.format(
                url=escape(source["url"], quote=True),
                source_id=escape(source["source_id"], quote=True),
                title=escape(source["title"]),
                publisher=escape(source["publisher"]),
                checked=escape(_display_date(source["last_checked_at"])),
                status=escape(source["status"]),
            )
        )
    fact_items = []
    for fact in record.get("unique_local_facts", []):
        evidence = []
        for source_id in fact.get("source_ids", []):
            source = source_lookup.get(source_id)
            if source:
                evidence.append(f'<a href="{escape(source["url"], quote=True)}">{escape(source["title"])}</a> (checked {escape(_display_date(source["last_checked_at"]))})')
        fact_items.append(f'<li data-local-fact="true">{escape(fact["fact"])} <span>{"; ".join(evidence)}</span></li>')
    if not claim_items and not source_items and not fact_items:
        return ""
    claims = f'<h3>Traceable claims</h3><ul class="claim-list">{"".join(claim_items)}</ul>' if claim_items else ""
    facts = f'<h3>Authority-specific facts</h3><ul class="local-fact-list">{"".join(fact_items)}</ul>' if fact_items else ""
    source_list = f'<h3>Source register</h3><ul class="source-register-list">{"".join(source_items)}</ul>' if source_items else ""
    return (
        '<section class="contract-source-panel" id="page-sources" data-page-source-panel="true">'
        '<span class="eyebrow">Sources and review</span>'
        '<h2>What this page is based on</h2>'
        f"{claims}{facts}{source_list}"
        '<p class="section-lead">Source verification dates are separate from the page content-update date.</p>'
        "</section>"
    )


def _render_social_meta(title: str, meta_description: str, canonical_url: str) -> str:
    if not title and not meta_description and not canonical_url:
        return ""

    og_type = "website" if not _is_inner_page(canonical_url) else "article"
    tags = [
        ('property', 'og:site_name', "UK Planning Guide"),
        ('property', 'og:title', title),
        ('property', 'og:description', meta_description),
        ('property', 'og:url', canonical_url),
        ('property', 'og:type', og_type),
        ('name', 'twitter:card', "summary"),
        ('name', 'twitter:title', title),
        ('name', 'twitter:description', meta_description),
    ]

    lines = []
    for attr_name, attr_value, content in tags:
        if not content:
            continue
        lines.append(
            f'<meta {attr_name}="{escape(str(attr_value), quote=True)}" content="{escape(str(content), quote=True)}">'
        )

    return "\n".join(lines)


def inject_into_base(
    title,
    content,
    options=None,
    canonical_url="",
    meta_description="",
):
    template = (TEMPLATES_FOLDER / "base.html").read_text(encoding="utf-8")
    options = options or {}
    record = render_record_for_url(canonical_url or "/")
    if record:
        options = dict(options)
        canonical_url = absolute_url(record["canonical_path"])
        if record["index_status"] == "noindex":
            options["meta_robots"] = "noindex, follow"
    title, meta_description = refine_metadata(title or "", meta_description or "", canonical_url or "")
    content = content or ""
    if _is_inner_page(canonical_url):
        if record:
            content = _render_contract_trust_strip(record) + content
        else:
            content = (build_page_trust_strip(canonical_url) or _render_trust_strip(options.get("year"))) + content
    breadcrumbs = options.get("breadcrumbs")
    extra_schema = (
        options.get("schema")
        or options.get("structuredData")
        or options.get("structured_data")
    )
    authority_schema = build_authority_schema_bundle(canonical_url or "", title or "", meta_description or "")
    if record:
        contract_schema = {
            "@type": "WebPage",
            "@id": f"{canonical_url}#contract-page",
            "url": canonical_url,
            "dateModified": record["content_updated_at"],
        }
        if isinstance(extra_schema, list):
            extra_schema = extra_schema + [contract_schema]
        elif extra_schema:
            extra_schema = [extra_schema, contract_schema]
        else:
            extra_schema = [contract_schema]
    if extra_schema:
        if isinstance(extra_schema, list):
            extra_schema = authority_schema + extra_schema
        else:
            extra_schema = authority_schema + [extra_schema]
    else:
        extra_schema = authority_schema
    schema = render_schema_markup(
        title or "",
        canonical_url or "",
        meta_description or "",
        breadcrumbs=breadcrumbs,
        extra_schema=extra_schema,
    )

    replacements = {
        "title": escape(title or ""),
        "meta_description": escape(meta_description or ""),
        "social_meta_tags": _render_social_meta(title or "", meta_description or "", canonical_url or ""),
        "meta_robots_tag": (
            f'<meta name="robots" content="{escape(str(options.get("meta_robots") or ""), quote=True)}">'
            if options.get("meta_robots")
            else ""
        ),
        "canonical": escape(canonical_url or "", quote=True),
        "schema": schema,
        "breadcrumbs": _render_breadcrumbs(breadcrumbs),
        "navigation_links": options.get("navigation_links", "") or "",
        "content": (content or "") + (_render_contract_source_panel(record) if record else "") + (build_sticky_action_bar() if _is_inner_page(canonical_url) else ""),
        "year": str(options.get("year") or datetime.now().year),
        "tool_ui_components": render_tool_ui_templates(),
    }

    html = template
    for key, value in replacements.items():
        html = html.replace(f"{{{{{key}}}}}", value)

    if options.get("include_canonical") is False:
        html = re.sub(r'\s*<link\s+rel="canonical"\s+href="[^"]*">', "", html, count=1, flags=re.IGNORECASE)

    if record:
        html = html.replace(
            '<html lang="en">',
            '<html lang="en" data-page-family="{family}" data-jurisdiction="{jurisdiction}" data-review-status="{review}">'.format(
                family=escape(record["page_family"], quote=True),
                jurisdiction=escape(record["jurisdiction"], quote=True),
                review=escape(record["review_status"], quote=True),
            ),
            1,
        )

    html = polish_html_copy(re.sub(r"\{\{.*?\}\}", "", html))
    from utils.production_content import assert_publishable
    assert_publishable(html, canonical_url.replace("https://ukplanningguide.co.uk", ""))
    return html
