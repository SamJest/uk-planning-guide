from core.files import write_file
from core.paths import BASE_URL, OUTPUT_FOLDER
from core.render import inject_into_base
from components.editorial_authority import build_editorial_authority_block
from components.building_regs_handoff import build_project_building_regs_handoff
from components.gsc_answer_capsule import build_gsc_answer_capsule
from components.gsc_cluster_links import build_gsc_cluster_links
from components.official_sources import build_official_sources_block
from components.planning_helpers import scenario_rule_excerpt, useful_local_restrictions
from components.personalised_guidance import build_personalised_guidance_cta
from components.retention_cta import build_workspace_retention_cta
from components.seo import build_local_search_metadata
from data.loaders import load_rule
from data.local_search_pages import LOCAL_SEARCH_PAGES
from utils.country_utils import get_country_slug
from utils.local_search_strategy import (
    local_search_authority_href,
    local_search_focus_signal,
    local_search_owner,
    local_search_project_href,
    local_search_scenario_href,
    local_search_topic_phrase,
)
from utils.live_links import is_live_internal_href, normalize_internal_href
from utils.random_tools import get_month_year


def _label_from_slug(slug: str) -> str:
    return slug.replace("-", " ").title()


def _authority_title(page: dict) -> str:
    if page["authority_slug"] in {"scotland", "wales"}:
        return f"{_label_from_slug(page['authority_slug'])} planning guide"
    if page["target_scope"] == "county":
        return f"{_label_from_slug(page['authority_slug'])} county planning guide"
    return f"{_label_from_slug(page['authority_slug'])} council guide"


def _project_title(page: dict) -> str | None:
    project_slug = page.get("project_slug")
    if not project_slug:
        return None

    if page.get("project_scope") == "county":
        return f"{_label_from_slug(project_slug)} in {_label_from_slug(page['county_slug'])}"

    return f"{_label_from_slug(project_slug)} in {_label_from_slug(page.get('council_slug') or page['authority_slug'])}"


def _scenario_title(page: dict) -> str | None:
    scenario_slug = page.get("scenario_slug")
    if not scenario_slug:
        return None

    authority_slug = page.get("scenario_authority_slug")
    if authority_slug:
        return f"{_label_from_slug(scenario_slug)} in {_label_from_slug(authority_slug)}"

    return _label_from_slug(scenario_slug)


def _faq_href(page: dict) -> str:
    if page.get("faq_href"):
        return page["faq_href"]
    project_slug = page.get("project_slug", "")
    query = page.get("query", "")
    if page.get("scenario_slug") == "conservation-areas":
        return "/planning-faq/conservation-area-planning-rules/"
    if project_slug == "hmos" and "article 4" in query.lower():
        return "/planning-faq/planning-permission-vs-permitted-development/"
    if "dropped-kerb" in project_slug or "dropped kerb" in query:
        return "/planning-faq/do-i-need-planning-permission/"
    if page.get("scenario_slug") == "planning-permission":
        return "/planning-faq/planning-permission-vs-permitted-development/"
    return "/planning-faq/do-i-need-planning-permission/"


def _faq_title(page: dict) -> str:
    if page.get("faq_title"):
        return page["faq_title"]
    project_slug = page.get("project_slug", "")
    query = page.get("query", "")
    if page.get("scenario_slug") == "conservation-areas":
        return "Planning Rules In Conservation Areas"
    if project_slug == "hmos" and "article 4" in query.lower():
        return "Planning Permission Vs Permitted Development"
    if "dropped-kerb" in project_slug or "dropped kerb" in query:
        return "Do I Need Planning Permission?"
    if page.get("scenario_slug") == "planning-permission":
        return "Planning Permission Vs Permitted Development"
    return "Do I Need Planning Permission?"


def _faq_description(page: dict) -> str:
    if page.get("faq_description"):
        return page["faq_description"]
    project_slug = page.get("project_slug", "")
    query = page.get("query", "")
    if page.get("scenario_slug") == "conservation-areas":
        return "Useful when the local heritage issue is broader than one authority page and you need the conservation-area route explained clearly."
    if project_slug == "hmos" and "article 4" in query.lower():
        return "Useful when the real issue is HMO change of use, Article 4 coverage, or whether the property has lost the easier fallback route."
    if "dropped-kerb" in project_slug or "dropped kerb" in query:
        return "Useful when the search is really about separating planning permission from the wider highways route."
    if page.get("scenario_slug") == "planning-permission":
        return "Useful when the question is still split between normal householder work and a fuller planning application."
    return "Useful when one project page or one rule page is not enough to settle the search."


def _search_intro(page: dict, authority_label: str) -> str:
    query = str(page.get("query", "")).lower()
    project_slug = str(page.get("project_slug", "")).lower()
    scenario_slug = str(page.get("scenario_slug", "")).lower()
    topic_phrase = local_search_topic_phrase(page, authority_label)

    if project_slug == "hmos" and "article 4" in query:
        if "not covered" in query or "areas" in query:
            return (
                f"For HMO Article 4 searches in {authority_label}, answer the coverage question first: whether the exact property, use and area are inside the direction is what decides whether the simpler route can still be relied on."
            )
        return (
            f"In {authority_label}, this usually comes down to whether HMO change of use, Article 4 or permitted development is the real blocker, and whether the exact property can still use the simpler route."
        )
    if "dropped kerb" in query or "dropped-kerb" in project_slug:
        return (
            f"For dropped kerbs in {authority_label}, the important question is usually whether planning permission, highway approval or both are doing the real work."
        )
    if scenario_slug == "article-4":
        return (
            f"The live issue in {authority_label} is whether Article 4 removes the fallback people were expecting and changes which detailed page matters next."
        )
    if scenario_slug == "conservation-areas":
        return (
            f"In {authority_label}, heritage coverage and conservation-area controls are often the reason the answer stops looking straightforward."
        )
    if scenario_slug == "permitted-development":
        return (
            f"In {authority_label}, the real question is usually whether permitted development survives once local controls, site history and the exact property position are checked properly."
        )
    return (
            f"This page is built for searches about {topic_phrase}. It gives you the local reading first, then sends you to the guide most likely to answer the remaining question."
    )


def _search_best_depth_path(page: dict, authority_kind: str) -> str:
    owner = local_search_owner(page)
    scenario_slug = str(page.get("scenario_slug", "")).lower()
    query = str(page.get("query", "")).lower()
    project_slug = str(page.get("project_slug", "")).lower()
    if project_slug == "hmos" and "article 4" in query:
        return "Start with the HMO guide, then widen out to the authority page if local policy or Article 4 coverage still needs a broader check."
    if "dropped kerb" in query or "dropped-kerb" in str(page.get("project_slug", "")).lower():
        return "Separate planning permission from the wider access, drainage and highway route before you commit to the wrong detailed guide."
    if scenario_slug == "article-4":
        return "Confirm whether Article 4 is what removes the simpler route, then move into the authority or project page that answers the remaining doubt."
    if scenario_slug == "conservation-areas":
        return "Confirm whether heritage controls are the real blocker, then move into the authority and project pages that explain the local answer more clearly."
    if owner == "project":
        return "Go to the project guide first, then use the council or rule page only if local policy changes the answer."
    return f"Treat this as a short route map: {authority_kind} guide first, then the strongest project or local rule page, then a process FAQ or tool if the answer still needs tightening."


def _best_next_move(page: dict, authority_kind: str) -> str:
    owner = local_search_owner(page)
    if owner == "project":
        return f"Start with the project guide if the build type is already clear, then widen out to the {authority_kind} page only if local policy, restrictions or council behaviour still need a broader check."
    if owner == "scenario":
        return f"Start with the local topic page if the rule itself is the blocker, then use the {authority_kind} page or project guide if the property context still changes the answer."
    return f"Start with the {authority_kind} page if the search is still broad, then move into the strongest project or planning topic page as soon as the real blocker is clearer."


def _hero_handoff(page: dict, authority_label: str, authority_kind: str) -> str:
    owner = local_search_owner(page)
    if owner == "project":
        return f"If the build type is already clear in {authority_label}, jump straight to the project guide below and use this page only to decide whether the {authority_kind} layer still changes the route."
    if owner == "scenario":
        return f"If one local rule in {authority_label} is doing most of the work, jump straight to the topic page below and use the {authority_kind} guide only if the wider local context still matters."
    return f"If the search is still broad in {authority_label}, open the {authority_kind} guide first, then follow the project or topic page that resolves the remaining doubt fastest."


def _clean_signal(text: str) -> str:
    clean = str(text or "").strip()
    lowered = clean.lower()
    if not clean:
        return ""
    if "most householder development follows national permitted development rules" in lowered:
        return ""
    if "use the linked authority, project and planning-topic pages" in lowered:
        return ""
    return clean


def _why_this_page_exists(page: dict, authority_label: str) -> str:
    owner = local_search_owner(page)
    topic_phrase = local_search_topic_phrase(page, authority_label)
    query = page["query"]

    if owner == "project":
        return (
            f"People search for {query} when the project type is already clear but the local route is not. "
            f"This page keeps {topic_phrase} readable, then hands you to the strongest project page before the wider local context."
        )
    if owner == "scenario":
        return (
            f"People search for {query} when one local rule is doing most of the work. "
            f"This page keeps the heritage or restriction issue visible first, then sends you to the deeper rule and project pages."
        )
    return (
        f"People search for {query} when the local route is still broad. "
            f"This page turns that broad query into a short list of authority, topic and project pages that are actually worth your time."
    )


def _tripwires(page: dict, authority_label: str, restrictions: list[tuple[str, str]]) -> list[str]:
    query = str(page.get("query", "")).lower()
    project_slug = str(page.get("project_slug", "")).lower()
    scenario_slug = str(page.get("scenario_slug", "")).lower()
    items = [f"{label} can change the answer faster than the broad search query suggests." for label, _ in restrictions[:2]]

    if project_slug == "heat-pumps":
        items.extend(
            [
                "Noise, siting and neighbour relationship usually matter more than the installer sales summary.",
                "Conservation-area or listed-building context can move a routine heat-pump answer into a closer local check.",
            ]
        )
    elif project_slug == "loft-conversions":
        items.extend(
            [
                "Roof volume, front-facing roof changes and visibility from the street are common reasons the route hardens.",
                "Previous roof additions and awkward roof form often matter before the wider design work is even finished.",
            ]
        )
    elif project_slug == "dropped-kerbs":
        items.extend(
            [
                "Highway approval, frontage visibility and drainage can become the real route even where the query only mentions planning permission.",
                "A planning-friendly answer is still weak if the access layout would not work safely on the highway.",
            ]
        )
    elif project_slug == "hmos" and "article 4" in query:
        items.extend(
            [
                "Article 4 coverage has to be checked for the exact property, not assumed from a broad district-level mention.",
                "Local concentration pressure and amenity concerns can make a borderline HMO proposal much less comfortable.",
            ]
        )
    elif scenario_slug == "conservation-areas":
        items.extend(
            [
                "Visibility, materials and any demolition element can turn a familiar project into a heritage-led decision.",
                "The local answer becomes less reliable if the proposal depends on visible change looking routine.",
            ]
        )
    elif scenario_slug == "article-4":
        items.extend(
            [
                "The important check is whether the direction removes rights for this proposal, not whether Article 4 exists somewhere nearby.",
                "A route that depends on the simpler fallback should be treated cautiously until the local control is verified.",
            ]
        )

    seen: set[str] = set()
    deduped: list[str] = []
    for item in items:
        clean = " ".join(item.split())
        if clean and clean not in seen:
            seen.add(clean)
            deduped.append(clean)
    return deduped[:4]


def _before_spend_money(page: dict, authority_label: str, authority_kind: str) -> str:
    owner = local_search_owner(page)
    query = str(page.get("query", "")).lower()
    project_slug = str(page.get("project_slug", "")).lower()
    if project_slug == "hmos" and "article 4" in query:
        return (
            f"Do not rely on the HMO permitted-development assumption in {authority_label} until Article 4 coverage, the exact use class and the local concentration or amenity position have been checked. "
            "If the proposal only works because Article 4 is assumed not to bite, verify that point before spending on drawings, valuations or tenancy planning."
        )
    if owner == "project":
        return (
            f"Do not spend money on a full drawing pack until the project guide and the {authority_kind} layer agree on the likely route. "
            "If they do not line up cleanly, treat that as a signal to verify formally rather than to keep reading broad summaries."
        )
    if owner == "scenario":
        return (
            f"If the issue in {authority_label} is really heritage, Article 4 or another control-led topic, settle that point before paying for design work that depends on the simpler route surviving."
        )
    return (
        f"Use this page to narrow the question first, then spend time on the main guide that resolves it. Broad local queries are useful for orientation, but they are a weak basis for drawings, quotes or an application strategy on their own."
    )


def _verification_warning(page: dict, authority_label: str) -> str:
    scenario_slug = str(page.get("scenario_slug", "")).lower()
    project_slug = str(page.get("project_slug", "")).lower()
    query = str(page.get("query", "")).lower()
    if project_slug == "hmos" and "article 4" in query:
        return (
            f"If the route depends on Article 4 coverage in {authority_label}, verify the exact property and proposed HMO use before treating permitted development as safe. "
            "That is often the point where council records, a certificate route or tailored advice saves more than another broad search."
        )
    if scenario_slug in {"conservation-areas", "article-4"}:
        return (
            f"If the route depends on heritage controls or Article 4 coverage in {authority_label}, verify the exact property position before treating the simpler route as safe. "
            "That is often the point where pre-application advice or a formal council check saves more money than another round of generic reading."
        )
    if project_slug in {"loft-conversions", "two-storey-extensions", "garden-rooms", "outbuildings"}:
        return (
            "If the design is close to a size, height or use threshold, prepare measured drawings and decide whether a lawful development certificate is worth securing before work starts."
        )
    return (
        "If the proposal is borderline, affected by special controls or financially sensitive, use the linked pages to narrow the issue and then move to a lawful development certificate, pre-application advice or another formal check before relying on assumptions."
    )


def _broad_answer(page: dict, authority_label: str, authority_kind: str) -> str:
    owner = local_search_owner(page)
    topic_phrase = local_search_topic_phrase(page, authority_label)
    query = str(page.get("query", "")).lower()
    project_slug = str(page.get("project_slug", "")).lower()
    if project_slug == "hmos" and "article 4" in query:
        return (
            f"Treat this as an Article 4 coverage and HMO change-of-use question first. If the property is covered, the safer baseline is usually that planning permission may be needed before the HMO route can be relied on."
        )
    if owner == "project":
        return (
            f"The quickest safe reading is to treat this as a {topic_phrase.lower()} question first, then use the {authority_kind} page to see whether local restrictions or policy make the usual route less reliable."
        )
    if owner == "scenario":
        return (
            f"The search phrase is only the entry point. The live answer turns on {topic_phrase.lower()}, then on whether that issue changes the wider planning route in {authority_label}."
        )
    return (
        f"This search is usually a starting query rather than a final answer. Use it to reach the {authority_kind} guide first, then the strongest project or planning-topic page once the real blocker is clearer."
    )


def _guidance_tracking_context(page: dict, owner: str) -> dict[str, str]:
    authority_slug = page.get("council_slug") or page.get("scenario_authority_slug") or page.get("authority_slug", "")
    return {
        "route_family": page.get("project_slug", ""),
        "query_bucket": page.get("gsc_query_bucket") or page.get("gsc_cluster") or owner,
        "authority_slug": authority_slug,
        "project_slug": page.get("project_slug", ""),
        "scenario_slug": page.get("scenario_slug", ""),
        "local_search_slug": page.get("slug", ""),
        "gsc_cluster": page.get("gsc_cluster", ""),
        "gsc_priority": str(page.get("gsc_priority", "")),
    }


def generate_local_search_pages():
    print("Generating local search pages")

    root = OUTPUT_FOLDER / "local-search"
    root.mkdir(parents=True, exist_ok=True)

    for page in LOCAL_SEARCH_PAGES:
        rule_council = page.get("council_slug") or page.get("scenario_authority_slug") or page["authority_slug"]
        rule = load_rule(page["project_slug"], page["county_slug"], rule_council) if page.get("project_slug") else {}
        permitted = _clean_signal(str(rule.get("permitted_development", "")))
        local_signal = _clean_signal(scenario_rule_excerpt(rule, page.get("scenario_slug") or "planning-permission"))
        restrictions = useful_local_restrictions(rule)
        local_title, local_description = build_local_search_metadata(page, rule)

        authority_label = _label_from_slug(page["authority_slug"])
        authority_kind = "county" if page["target_scope"] == "county" else "authority"
        authority_href = local_search_authority_href(page)
        project_href = local_search_project_href(page)
        project_title = _project_title(page)
        scenario_href = local_search_scenario_href(page)
        scenario_title = _scenario_title(page)
        faq_href = _faq_href(page)
        faq_title = _faq_title(page)
        faq_description = _faq_description(page)
        search_intro = _search_intro(page, authority_label)
        best_depth_path = _search_best_depth_path(page, authority_kind)
        primary_owner = local_search_owner(page)
        if not local_signal:
            local_signal = permitted or local_search_focus_signal(page, authority_label)

        cards = []
        seen_hrefs: set[str] = set()

        def add_card(href: str | None, kicker: str, title: str | None, description: str, cta: str) -> None:
            clean = normalize_internal_href(href or "")
            if not clean or not title or clean in seen_hrefs or not is_live_internal_href(clean):
                return
            seen_hrefs.add(clean)
            cards.append(
                f"""
<a class="card" href="{clean}">
<div class="card-kicker">{kicker}</div>
<h3>{title}</h3>
<p>{description}</p>
<span class="cta">{cta}</span>
</a>
"""
            )

        card_specs = {
            "authority": (
                authority_href,
                "Authority guide",
                _authority_title(page),
                f"Best if the main uncertainty is local policy, authority context or simply where to start in {authority_label}.",
                "Open authority page",
            ),
            "scenario": (
                scenario_href,
                "Planning topic",
                scenario_title,
                "Best when one planning issue is doing most of the work, rather than the whole project type.",
                "Open topic page",
            ),
            "project": (
                project_href,
                "Project guide",
                project_title,
                "Best when the build type is already clear and you want the practical route without reading generic authority guidance first.",
                "Open project guide",
            ),
            "faq": (
                faq_href,
                "FAQ follow-up",
                faq_title,
                faq_description,
                "Read answer",
            ),
            "tool": (
                "/tools/planning-decision-tool/",
                "Tool",
                "Check if your project is likely to need permission",
                "Helpful if this search is only part of the route question and you want a fast first-pass answer before opening multiple local pages.",
                "Check likely route",
            ),
        }
        if page.get("project_slug") == "hmos" and "article 4" in str(page.get("query", "")).lower():
            article_4_authority = page.get("council_slug") or page.get("scenario_authority_slug")
            if article_4_authority and page.get("target_scope") != "county":
                card_specs["hmo_article_4"] = (
                    f"/hmos/{page['county_slug']}/{article_4_authority}/article-4/",
                    "Exact Article 4 route",
                    f"HMO Article 4 in {_label_from_slug(article_4_authority)}",
                    "Best when the search is specifically about whether Article 4 removes the simpler HMO route for this authority.",
                    "Open Article 4 route",
                )
        card_order = {
            "authority": ["authority", "scenario", "project", "faq", "tool"],
            "scenario": ["scenario", "authority", "project", "faq", "tool"],
            "project": ["project", "authority", "scenario", "faq", "tool"],
        }.get(primary_owner, ["authority", "scenario", "project", "faq", "tool"])
        if "hmo_article_4" in card_specs:
            card_order = ["project", "hmo_article_4", "authority", "scenario", "faq", "tool"]

        for key in card_order:
            add_card(*card_specs[key])

        if primary_owner == "project":
            guidance_title = "Need The Local Project Route Narrowed Further?"
            guidance_description = f"If the answer in {authority_label} now depends on your exact design, site history or local sensitivity, use the structured guidance form after the quick checks."
        elif primary_owner == "scenario":
            guidance_title = "Need The Local Rule Question Narrowed Further?"
            guidance_description = f"If one rule, designation or local control is now deciding the answer in {authority_label}, use the structured guidance form after you have checked the quick tools."
        else:
            guidance_title = "Need A More Tailored Local Steer?"
            guidance_description = f"If the answer in {authority_label} is especially location-sensitive, use the structured guidance form only after the quicker route and proof checks are not enough."

        tripwires = _tripwires(page, authority_label, restrictions)
        tripwire_card = (
            f"""
<div class="answer-card">
<h3>Checks most likely to matter</h3>
<ul class="checklist">{''.join(f"<li>{item}</li>" for item in tripwires)}</ul>
</div>
"""
            if tripwires
            else ""
        )

        content = f"""
<section class="hero">
<span class="badge">Local search guide</span>
<h1>{page['title']}</h1>
<p>{search_intro}</p>
<p>{_hero_handoff(page, authority_label, authority_kind)}</p>
<div class="last-updated">Updated {get_month_year()}</div>
</section>

{build_gsc_answer_capsule(f"/local-search/{page['slug']}/")}

{build_workspace_retention_cta(
    f"/local-search/{page['slug']}/",
    title=page["title"],
    page_family="local-search",
    project_slug=page.get("project_slug", ""),
    authority_slug=page.get("council_slug") or page.get("scenario_authority_slug") or page["authority_slug"],
)}

{build_gsc_cluster_links(f"/local-search/{page['slug']}/")}

<section class="local-search-answer" id="local-search-answer">
<span class="eyebrow">Working read</span>
<h2>What This Search Usually Means In Practice</h2>
<div class="answer-grid">
<div class="answer-card">
<h3>Working answer</h3>
<p>{_broad_answer(page, authority_label, authority_kind)}</p>
</div>
<div class="answer-card">
<h3>Why this search exists</h3>
<p>{_why_this_page_exists(page, authority_label)}</p>
</div>
<div class="answer-card">
<h3>Best next step</h3>
<p>{_best_next_move(page, authority_kind)}</p>
</div>
</div>
</section>

{build_official_sources_block(
    page_family="local-search",
    authority_slug=page.get("council_slug") or page.get("scenario_authority_slug") or page["authority_slug"],
    country_slug=rule.get("country_slug", get_country_slug(page["county_slug"])),
    project_slug=page.get("project_slug", ""),
    scenario_slug=page.get("scenario_slug", ""),
)}

{build_editorial_authority_block(
    f"/local-search/{page['slug']}/",
    page_family="local-search",
    authority_slug=page.get("council_slug") or page.get("scenario_authority_slug") or page["authority_slug"],
    country_slug=rule.get("country_slug", get_country_slug(page["county_slug"])),
    project_slug=page.get("project_slug", ""),
    scenario_slug=page.get("scenario_slug", ""),
)}

<section class="local-search-sensitivity" id="local-search-sensitivity">
<span class="eyebrow">Where it usually tightens up</span>
<h2>The Checks Worth Making Before You Pay For More Work</h2>
<div class="answer-grid">
<div class="answer-card">
<h3>Main local signal</h3>
<p>{local_signal}</p>
</div>
{tripwire_card}
<div class="answer-card">
<h3>Before you spend money</h3>
<p>{_before_spend_money(page, authority_label, authority_kind)}</p>
</div>
</div>
</section>

<section class="local-search-routes" id="local-search-routes">
<span class="eyebrow">Deeper route options</span>
<h2>Open The Page Most Likely To Settle The Remaining Question</h2>
<p class="section-lead">{best_depth_path}</p>
<div class="grid">
{''.join(cards)}
</div>
</section>

{build_project_building_regs_handoff(page.get("project_slug", ""), project_title or page["title"], authority_label)}

{build_personalised_guidance_cta(
    title=guidance_title,
    description=guidance_description,
    context_label="local-search",
    email_context=page['title'],
    compact=True,
    prefill={
        "authority": page.get("council_slug") or page.get("scenario_authority_slug") or page["authority_slug"],
        "project": page.get("project_slug", ""),
        "query": page.get("query", ""),
        "route_family": page.get("gsc_cluster") or primary_owner,
    },
    tracking_context=_guidance_tracking_context(page, primary_owner),
)}

<section class="local-search-verify" id="local-search-verify">
<span class="eyebrow">Verification warning</span>
<h2>When A Broad Local Search Stops Being A Safe Stopping Point</h2>
<div class="answer-grid">
<div class="answer-card">
<h3>When to escalate</h3>
<p>{_verification_warning(page, authority_label)}</p>
</div>
<div class="answer-card">
<h3>Formal checks that often help</h3>
<ul class="checklist">
<li>Use a lawful development certificate when the project only works if the simpler route still holds up.</li>
<li>Use pre-application advice when the design is sensitive, locally constrained or already drifting toward a full application.</li>
<li>Keep measured drawings, site photos and planning-history notes together before you rely on any borderline answer.</li>
</ul>
</div>
<div class="answer-card">
<h3>How to use this page well</h3>
<p>Treat this as a starting point, not a stopping point. Its job is to get you to the authority, project, topic and tool pages that make the next real decision easier.</p>
</div>
</div>
</section>
"""

        html = inject_into_base(
            title=local_title,
            content=content,
            options={
                "breadcrumbs": [("Home", "/"), ("Local search", "/local-search/"), (page["title"], "")],
            },
            canonical_url=f"{BASE_URL}/local-search/{page['slug']}/",
            meta_description=local_description,
        )
        write_file(root / page["slug"], "index.html", html)

    index_cards = "".join(
        f"""
<a class="card" href="/local-search/{page['slug']}/">
<div class="card-kicker">Local search guide</div>
<h3>{page['title']}</h3>
<p>{_search_intro(page, _label_from_slug(page.get('council_slug') or page.get('scenario_authority_slug') or page['authority_slug']))}</p>
<span class="cta">Open page</span>
</a>
"""
        for page in LOCAL_SEARCH_PAGES
    )
    index_html = inject_into_base(
        title="Local Planning Search Guides",
        content=f"""
<section class="hero">
<span class="badge">Curated local search pages</span>
<h1>Local Planning Search Guides</h1>
<p>These compact pages stay available as query-specific starting points, but broader evergreen guides and stronger local planning guides carry the main search load.</p>
</section>
<section>
<h2>Curated local-intent pages</h2>
<div class="grid">{index_cards}</div>
</section>
""",
        options={"breadcrumbs": [("Home", "/"), ("Local search", "")], "meta_robots": "noindex, follow"},
        canonical_url=f"{BASE_URL}/local-search/",
        meta_description="Browse curated local planning search guides built for high-intent county, council, rule and project-location queries.",
    )
    write_file(root, "index.html", index_html)

    print("Local search pages generated successfully")
