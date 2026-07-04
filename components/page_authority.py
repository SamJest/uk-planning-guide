from __future__ import annotations

from datetime import datetime
from html import escape
from urllib.parse import urlparse

from data.authority_profiles import (
    AUTHORITY_PLACEHOLDER_NOTE,
    DEFAULT_AUTHOR_SLUG,
    DEFAULT_REVIEWER_SLUG,
    EDITORIAL_POLICY_PATH,
    GUIDANCE_EMAIL,
    GUIDANCE_FORM_PATH,
    authority_profile,
    site_organization_profile,
)
from data.editorial_authority import editorial_authority_record
from data.editorial_authority import REVIEW_DATE as DEFAULT_REVIEW_DATE
from data.loaders import load_projects
from data.scenario_data import SCENARIOS
from utils.official_sources import OfficialSourceContext, relevant_official_sources
from utils.route_contracts import COUNTRY_SLUGS, route_contract_for_country_path


PROJECT_SLUGS = {project["slug"] for project in load_projects()}
SCENARIO_SLUGS = {scenario["slug"] for scenario in SCENARIOS}
SITE_URL = "https://ukplanningguide.co.uk/"
SLUG_LABELS = {
    "about": "About page",
    "methodology": "Methodology page",
    "privacy": "Privacy page",
    "editorial-policy": "Editorial policy page",
    "planning-permission": "Planning permission",
    "permitted-development": "Permitted development",
    "height-limits": "Height limits",
    "maximum-height": "Maximum height",
    "depth-limits": "Depth limits",
    "boundary-rules": "Boundary rules",
    "distance-from-boundary": "Distance from boundary",
    "roof-alterations": "Roof alterations",
    "conservation-areas": "Conservation areas",
    "listed-buildings": "Listed buildings",
    "article-4": "Article 4",
    "hmos": "HMOs",
    "dropped-kerbs": "Dropped kerbs",
    "house-extensions": "House extensions",
    "loft-conversions": "Loft conversions",
    "garden-rooms": "Garden rooms",
    "outbuildings": "Outbuildings",
    "building-regulations": "Building regulations",
}


def _format_review_date(value: str) -> str:
    clean = str(value or "").strip()
    if not clean:
        return ""
    for fmt in ("%Y-%m-%d", "%Y-%m"):
        try:
            parsed = datetime.strptime(clean, fmt)
        except ValueError:
            continue
        if fmt == "%Y-%m":
            return parsed.strftime("%B %Y")
        return f"{parsed.day} {parsed.strftime('%B %Y')}"
    return clean


def _path_from_canonical(canonical_url: str) -> str:
    clean = str(canonical_url or "").strip()
    if not clean:
        return "/"
    parsed = urlparse(clean)
    path = parsed.path or "/"
    return path if path.startswith("/") else "/" + path


def _label_from_slug(value: str) -> str:
    clean = str(value or "").strip().lower()
    if not clean:
        return ""
    if clean in SLUG_LABELS:
        return SLUG_LABELS[clean]

    words = []
    for token in clean.replace("/", " ").replace("-", " ").split():
        upper = token.upper()
        if upper in {"HMO", "HMOS", "PD", "UK"}:
            words.append("HMOs" if upper == "HMOS" else upper)
        else:
            words.append(token.capitalize())
    return " ".join(words)


def _page_descriptor(context: dict[str, str]) -> str:
    family = context.get("page_family", "")
    project_label = _label_from_slug(context.get("project_slug", ""))
    scenario_label = _label_from_slug(context.get("scenario_slug", ""))

    if family == "project" and project_label:
        return f"{project_label} local guide"
    if family == "scenario" and scenario_label:
        return f"{scenario_label} local page"
    if family == "hub" and project_label:
        return f"{project_label} hub"
    if family == "council":
        return "council guide"
    if family == "council-index":
        return "council index"
    if family == "local-search":
        return "local search route"
    if family == "faq":
        return "FAQ page"
    if family in {"building-regulations", "building-regulations-hub"}:
        return "building regulations guide"
    if family == "guidance":
        return "guidance page"
    if family == "editorial-policy":
        return "editorial policy page"
    if family:
        return family.replace("-", " ") + " page"
    return "page"


def infer_page_context(canonical_url: str) -> dict[str, str]:
    path = _path_from_canonical(canonical_url)
    parts = [part for part in path.strip("/").split("/") if part]
    context = {
        "path": path,
        "page_family": "",
        "project_slug": "",
        "scenario_slug": "",
        "authority_slug": "",
        "country_slug": "",
    }

    if not parts:
        context["page_family"] = "home"
        return context

    first = parts[0]
    if first in COUNTRY_SLUGS:
        contract = route_contract_for_country_path(path)
        if contract:
            context["country_slug"] = contract.country
            context["project_slug"] = contract.project_slug
            context["scenario_slug"] = contract.rule_slug
            context["authority_slug"] = contract.authority_slug
            if contract.intent_type == "projects":
                context["page_family"] = "project" if contract.authority_slug else "hub"
            elif contract.intent_type == "rules":
                context["page_family"] = "scenario" if contract.authority_slug else "hub"
            elif contract.intent_type == "councils":
                context["page_family"] = "council" if contract.authority_slug else "council-index"
            elif contract.intent_type == "process":
                context["page_family"] = "faq"
            elif contract.intent_type in {"tools", "data"}:
                context["page_family"] = contract.intent_type
            else:
                context["page_family"] = contract.intent_type or "hub"
            return context
    if path.startswith("/planning-faq/"):
        context["page_family"] = "faq"
        return context
    if first == "building-regulations":
        context["page_family"] = "building-regulations-hub" if len(parts) == 1 else "building-regulations"
        return context
    if first == "about":
        context["page_family"] = "about"
        return context
    if first == "methodology":
        context["page_family"] = "methodology"
        return context
    if first == "privacy":
        context["page_family"] = "privacy"
        return context
    if first == "editorial-policy":
        context["page_family"] = "editorial-policy"
        return context
    if first == "personalised-planning-guidance":
        context["page_family"] = "guidance"
        return context
    if first == "local-search":
        context["page_family"] = "local-search"
        return context
    if first == "councils":
        context["page_family"] = "council" if len(parts) > 1 else "council-index"
        if len(parts) > 1:
            context["authority_slug"] = parts[1]
        return context
    if first in PROJECT_SLUGS:
        context["project_slug"] = first
        if len(parts) == 1:
            context["page_family"] = "hub"
        elif len(parts) == 2:
            context["page_family"] = "county-project"
            context["country_slug"] = parts[1]
        elif len(parts) >= 3:
            context["page_family"] = "project"
            context["country_slug"] = parts[1]
            context["authority_slug"] = parts[2]
            if len(parts) >= 4 and parts[3] in SCENARIO_SLUGS:
                context["scenario_slug"] = parts[3]
        return context
    if first in SCENARIO_SLUGS:
        context["scenario_slug"] = first
        if len(parts) == 1:
            context["page_family"] = "hub"
        elif len(parts) >= 2:
            context["page_family"] = "scenario"
            context["authority_slug"] = parts[1]
        return context
    if len(parts) == 1:
        context["page_family"] = "county"
    return context


def _resolve_official_source(context: dict[str, str], record: dict) -> dict[str, str]:
    override = record.get("official_source") or {}
    if override.get("title") and override.get("url"):
        return {
            "title": str(override["title"]).strip(),
            "url": str(override["url"]).strip(),
            "date": _format_review_date(override.get("date") or record.get("last_reviewed", "")),
        }

    authority_slug = context.get("authority_slug", "")
    if authority_slug:
        sources = relevant_official_sources(
            OfficialSourceContext(
                page_family=context.get("page_family", "project") if context.get("page_family") in {"project", "scenario", "council", "local-search"} else "project",
                authority_slug=authority_slug,
                country_slug=context.get("country_slug", ""),
                project_slug=context.get("project_slug", ""),
                scenario_slug=context.get("scenario_slug", ""),
                max_links=1,
            )
        )
        if sources:
            source = sources[0]
            return {
                "title": source.title,
                "url": source.url,
                "date": _format_review_date(source.last_reviewed or record.get("last_reviewed", "")),
            }

    family = context.get("page_family", "")
    project_label = _label_from_slug(context.get("project_slug", ""))
    scenario_label = _label_from_slug(context.get("scenario_slug", ""))
    if family == "council":
        title = "Council planning, validation and pre-application pages"
    elif family == "project" and project_label:
        title = f"Council planning pages for {project_label}"
    elif family == "scenario" and scenario_label:
        title = f"Council sources for {scenario_label.lower()}"
    elif family == "hub" and project_label:
        title = f"National planning guidance for {project_label.lower()}"
    elif family == "faq":
        title = "National planning and application guidance"
    elif family in {"building-regulations", "building-regulations-hub"}:
        title = "GOV.UK building regulations and building control guidance"
    elif family in {"about", "methodology", "editorial-policy", "guidance", "privacy"}:
        title = "Visible methodology and editorial standards"
    else:
        title = "Planning route and official sources"

    return {
        "title": title,
        "url": "",
        "date": _format_review_date(record.get("last_reviewed", "")),
    }


def _default_source_basis(context: dict[str, str]) -> str:
    family = context.get("page_family", "")
    project_label = _label_from_slug(context.get("project_slug", ""))
    scenario_label = _label_from_slug(context.get("scenario_slug", ""))
    if family == "council":
        return "Council planning pages, validation requirements and the local project routes residents usually need next."
    if family == "local-search":
        return "The local search intent, the authority guide that should answer it, and the deeper project or rule page worth opening next."
    if family == "scenario":
        return f"The national {scenario_label.lower() if scenario_label else 'rule'} baseline, the council sources that change it locally, and the formal route to use if the answer tightens."
    if family == "project":
        if project_label:
            return f"The national {project_label.lower()} route, the local authority material that can narrow it, and the official checks most likely to settle the next move."
        return "The national project route, the local authority material that can narrow it, and the official checks most likely to settle the next move."
    if family == "hub":
        if project_label:
            return f"The national {project_label.lower()} baseline, the rule pages that usually change it, and the best local routes to open once the question stops being broad."
        return "The core planning routes, the national guidance behind them and the local pages most likely to settle the next decision."
    if family == "faq":
        return "The national planning-process baseline, the main qualifier that usually changes it and the deeper guide or formal check worth opening next."
    if family in {"building-regulations", "building-regulations-hub"}:
        return "England building regulations guidance, building control approval routes and the planning checks that still need to be kept separate."
    if family in {"about", "methodology", "editorial-policy", "guidance", "privacy"}:
        return "Visible ownership, review practice, source handling and the point where the site's guidance deliberately stops short of a formal decision."
    return "National planning baseline, local authority context and page-specific tripwires."


def _default_local_factor(context: dict[str, str]) -> str:
    project_slug = context.get("project_slug", "")
    scenario_slug = context.get("scenario_slug", "")
    family = context.get("page_family", "")
    if project_slug == "dropped-kerbs":
        return "Highway approval, frontage visibility and drainage usually settle more of the route than the planning headline on its own."
    if project_slug == "hmos" or scenario_slug == "article-4":
        return "The route often changes once Article 4 coverage, local policy pressure and the exact property position are checked together."
    if scenario_slug == "conservation-areas":
        return "Visibility, materials and heritage sensitivity usually do more work here than one headline measurement."
    if family == "council":
        return "This page matters most where local controls, planning history or one sensitive rule make the usual national answer less reliable."
    if family == "local-search":
        return "The page only earns its place if it turns a broad local query into the real blocker before the user opens the wrong detailed page."
    if family == "faq":
        return "The broad answer usually weakens once one local control, one exact measurement or one planning-history point starts doing the real work."
    if family in {"building-regulations", "building-regulations-hub"}:
        return "The answer usually changes once the work type, inspection route, competent person coverage or planning route is unclear."
    if family == "hub" and project_slug:
        label = _label_from_slug(project_slug).lower()
        return f"{label} queries usually stop being broad when scale, siting, use or a local control becomes the real risk."
    return "The answer usually changes once the proposal is borderline, visually sensitive or leaning on one assumption that still needs to hold up locally."


def _default_stop_and_verify(context: dict[str, str]) -> str:
    project_slug = context.get("project_slug", "")
    scenario_slug = context.get("scenario_slug", "")
    if project_slug == "dropped-kerbs":
        return "Stop and verify when access safety, frontage width, drainage or highway approval is doing the real work."
    if project_slug in {"garden-rooms", "outbuildings", "annexes"}:
        return "Stop and verify when use, siting or scale pushes the structure beyond a clearly incidental secondary building."
    if project_slug == "house-extensions":
        return "Stop and verify when the scheme is close to a depth, width or height threshold or depends on the original-house baseline."
    if project_slug == "hmos" or scenario_slug == "article-4":
        return "Stop and verify when the simpler route only survives if Article 4 does not bite on the exact property."
    if scenario_slug == "conservation-areas":
        return "Stop and verify when the proposal changes a visible elevation, historic fabric or the wider street scene."
    if context.get("page_family") == "council":
        return "Stop and verify when the council layer, not the broad national answer, is carrying most of the risk."
    if context.get("page_family") == "faq":
        return "Stop and verify when the answer now depends on one exact address, one tight threshold or a decision that would be expensive to get wrong."
    if context.get("page_family") in {"building-regulations", "building-regulations-hub"}:
        return "Stop and verify when work starts, inspections are due, or completion evidence would matter for sale, lending or insurance."
    return "Stop and verify when the proposal is close to a limit, affected by special controls or expensive to get wrong."


def _default_what_checked(context: dict[str, str]) -> str:
    family = context.get("page_family", "")
    if family == "council":
        return "The main authority route, the local pages residents usually need first, and the council sources most likely to change the answer."
    if family == "local-search":
        return "The real local search intent, the best next page, and the formal check most worth doing next."
    if family == "scenario":
        return "The controlling rule, the local restriction layer and the official source most likely to ground the answer."
    if family == "project":
        return "The national route, the local tripwires and the official checks worth making before more money is spent."
    if family == "hub":
        return "The broad route question, the local tripwires that usually change it and the deeper page that should settle the next move."
    if family == "faq":
        return "The direct answer, the qualifier that most often changes it and the stronger next page or formal check if the issue is no longer broad."
    if family in {"building-regulations", "building-regulations-hub"}:
        return "The England-first building regulations route, the building control questions to ask and the planning route that still needs checking separately."
    return "The official sources, the practical route guidance and the point where a formal check becomes safer."


def _default_change_note(context: dict[str, str]) -> str:
    family = context.get("page_family", "")
    descriptor = _page_descriptor(context)
    if family == "project":
        return f"Updated this {descriptor} to show clearer official sources, a cleaner verification trigger and a tighter next-step route."
    if family == "scenario":
        return f"Updated this {descriptor} to tighten the rule summary, clarify the council sources and make the stop-and-verify point easier to spot."
    if family == "council":
        return "Updated this council guide so ownership, review status and the strongest local source are visible without slowing the answer."
    if family == "local-search":
        return "Updated this route page so the local context, official sources and safest next click are clearer."
    if family == "hub":
        return f"Updated this {descriptor} to tighten trust wording, clarify official sources and point faster to the page that usually settles the route."
    if family == "faq":
        return "Updated this FAQ to shorten the summary, clarify the official sources and make the formal-check trigger easier to scan."
    if family in {"building-regulations", "building-regulations-hub"}:
        return "Added England-first building regulations guidance with clearer official sources, building control questions and planning route handoffs."
    if family in {"about", "methodology", "editorial-policy", "guidance", "privacy"}:
        return f"Updated this {descriptor} to show clearer ownership, review wording and the practical limit of the site's guidance."
    return "Updated the trust wording, official-source links and route language so the next decision is clearer."


def resolve_page_authority(
    path: str,
    *,
    page_family: str = "",
    authority_slug: str = "",
    country_slug: str = "",
    project_slug: str = "",
    scenario_slug: str = "",
) -> dict[str, object]:
    record = editorial_authority_record(path) or {}
    context = {
        "path": path,
        "page_family": page_family or str(record.get("family", "")) or "",
        "authority_slug": authority_slug,
        "country_slug": country_slug,
        "project_slug": project_slug,
        "scenario_slug": scenario_slug,
    }
    source = _resolve_official_source(context, record)
    author = authority_profile(record.get("author_slug") or DEFAULT_AUTHOR_SLUG)
    reviewer = authority_profile(record.get("reviewer_slug") or DEFAULT_REVIEWER_SLUG)
    organization = site_organization_profile()
    last_reviewed = str(record.get("last_reviewed") or DEFAULT_REVIEW_DATE)
    return {
        "path": path,
        "page_family": context["page_family"],
        "organization": organization,
        "author": author,
        "reviewer": reviewer,
        "reviewer_credentials": str(record.get("reviewer_credentials") or reviewer.get("credentials") or reviewer.get("role") or ""),
        "last_reviewed": last_reviewed,
        "last_reviewed_display": _format_review_date(last_reviewed),
        "source_basis": str(record.get("source_basis") or _default_source_basis(context)),
        "source_list": list(record.get("source_list") or []),
        "what_checked": str(record.get("what_checked") or _default_what_checked(context)),
        "local_factor": str(record.get("local_factor") or _default_local_factor(context)),
        "stop_and_verify": str(record.get("stop_and_verify") or _default_stop_and_verify(context)),
        "change_note": str(record.get("change_note") or _default_change_note(context)),
        "legal_scope_note": str(record.get("legal_scope_note") or _default_source_basis(context)),
        "local_uniqueness_note": str(record.get("local_uniqueness_note") or _default_local_factor(context)),
        "indexability_status": str(record.get("indexability_status") or "index"),
        "redirect_from_urls": list(record.get("redirect_from_urls") or []),
        "source_reason": str(record.get("official_footing_reason") or ""),
        "official_source": source,
        "notes": str(record.get("notes") or ""),
    }


def build_page_authority_from_canonical(canonical_url: str) -> dict[str, object]:
    context = infer_page_context(canonical_url)
    return resolve_page_authority(
        context["path"],
        page_family=context["page_family"],
        authority_slug=context["authority_slug"],
        country_slug=context["country_slug"],
        project_slug=context["project_slug"],
        scenario_slug=context["scenario_slug"],
    )


def build_page_trust_strip(canonical_url: str) -> str:
    context = build_page_authority_from_canonical(canonical_url)
    if context.get("page_family") == "home":
        return ""

    source_basis = escape(str(context["source_basis"]))
    stop_and_verify = escape(str(context["stop_and_verify"]))
    author_name = escape(str(context["author"]["name"]))
    reviewer_name = escape(str(context["reviewer"]["name"]))
    reviewed = escape(str(context["last_reviewed_display"] or _format_review_date(DEFAULT_REVIEW_DATE)))

    return (
        '<div class="page-trust-strip" data-page-authority="true" data-nosnippet>'
        '<div class="page-trust-strip-heading">'
        "<strong>Editorially checked</strong>"
        "<span>Visible ownership, review date and official-source context for this page.</span>"
        "</div>"
        '<div class="page-trust-strip-items">'
        f"<span><strong>Written by</strong> {author_name}</span>"
        f"<span><strong>Reviewed by</strong> {reviewer_name}</span>"
        f"<span><strong>Last reviewed</strong> {reviewed}</span>"
        f"<span><strong>Official-source context</strong> {source_basis}</span>"
        f"<span><strong>Verify before spending</strong> {stop_and_verify}</span>"
        "</div>"
        "</div>"
    )


def build_authority_summary_section(
    *,
    section_id: str,
    title: str,
    intro: str,
    include_placeholder_note: bool = True,
) -> str:
    author = authority_profile(DEFAULT_AUTHOR_SLUG)
    reviewer = authority_profile(DEFAULT_REVIEWER_SLUG)
    organization = site_organization_profile()
    note_html = (
        f"<p class='section-lead'>{escape(AUTHORITY_PLACEHOLDER_NOTE)}</p>"
        if include_placeholder_note and (author.get('is_placeholder') or reviewer.get('is_placeholder'))
        else ""
    )
    return f"""
<section id="{escape(section_id, quote=True)}" class="authority-summary">
<span class="eyebrow">Authority and accountability</span>
<h2>{title}</h2>
<p class="section-lead">{escape(intro)}</p>
{note_html}
<div class="answer-grid">
<div class="answer-card">
<h3>Written by</h3>
<p><strong>{escape(author['name'])}</strong><br>{escape(author['role'])}</p>
<p>{escape(author['short_bio'])}</p>
</div>
<div class="answer-card">
<h3>Reviewed by</h3>
<p><strong>{escape(reviewer['name'])}</strong><br>{escape(reviewer['role'])}</p>
<p>{escape(reviewer['short_bio'])}</p>
</div>
<div class="answer-card">
<h3>Official sources</h3>
<p>Pages are published under {escape(organization['name'])} with a visible methodology, review date, privacy notice and editorial policy.</p>
<p><a href="{EDITORIAL_POLICY_PATH}">Read the editorial policy</a></p>
</div>
<div class="answer-card">
<h3>Contact route</h3>
<p>Use the structured guidance form when the route still depends on the project details, the property itself or the local authority context.</p>
<p><a href="{GUIDANCE_FORM_PATH}">Open the guidance form</a><br><a href="mailto:{escape(GUIDANCE_EMAIL, quote=True)}">{escape(GUIDANCE_EMAIL)}</a></p>
</div>
</div>
</section>
"""


def _person_schema(profile: dict, canonical_url: str) -> dict | None:
    if profile.get("is_placeholder"):
        return None
    payload = {
        "@type": "Person",
        "name": profile["name"],
        "description": profile["short_bio"],
        "url": canonical_url.rstrip("/") + f"#{profile['profile_slug']}",
        "email": profile["contact_email"],
    }
    if profile.get("proof_links"):
        payload["sameAs"] = list(profile["proof_links"])
    return payload


def build_authority_schema_bundle(canonical_url: str, title: str, meta_description: str) -> list[dict]:
    authority = build_page_authority_from_canonical(canonical_url)
    organization = authority["organization"]
    org_schema = {
        "@type": "Organization",
        "@id": SITE_URL.rstrip("/") + "/#organization",
        "name": organization["name"],
        "url": organization["url"],
        "email": organization["contact_email"],
        "logo": {
            "@type": "ImageObject",
            "url": organization["logo"],
        },
        "description": organization["description"],
    }
    if organization.get("same_as"):
        org_schema["sameAs"] = list(organization["same_as"])

    family = str(authority.get("page_family") or "")
    if family in {"home", "hub", "council-index", "county", "county-project", "local-search", "building-regulations-hub"}:
        schema_type = "CollectionPage"
    else:
        schema_type = "Article"
    page_schema = {
        "@type": schema_type,
        "headline": title,
        "description": meta_description,
        "url": canonical_url,
        "mainEntityOfPage": {"@type": "WebPage", "@id": canonical_url},
        "dateModified": authority.get("last_reviewed") or DEFAULT_REVIEW_DATE,
        "publisher": {"@id": org_schema["@id"]},
    }

    author_schema = _person_schema(authority["author"], canonical_url)
    reviewer_schema = _person_schema(authority["reviewer"], canonical_url)
    if author_schema:
        page_schema["author"] = author_schema
    else:
        page_schema["author"] = {"@id": org_schema["@id"]}
    if reviewer_schema:
        page_schema["reviewedBy"] = reviewer_schema

    return [org_schema, page_schema]
