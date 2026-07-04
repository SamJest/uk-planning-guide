from __future__ import annotations

from data.organic_growth import growth_target_for_path


HMO_ARTICLE_4_PRIORITY_ROUTES = {
    ("staffordshire", "tamworth"): {
        "query": "tamworth hmo planning permitted development article 4",
        "local_search_slug": "hmo-article-4-tamworth",
        "impressions": 14902,
        "position": 4.12,
    },
    ("staffordshire", "stafford"): {
        "query": "stafford hmo article 4 direction staffordshire 2024 2025",
        "local_search_slug": "hmo-article-4-stafford",
        "impressions": 1562,
        "position": 9.54,
    },
    ("buckinghamshire", "milton-keynes"): {
        "query": "milton keynes article 4 direction hmo areas not covered",
        "local_search_slug": "hmo-article-4-milton-keynes",
        "impressions": 702,
        "position": 10.81,
    },
    ("northamptonshire", "west-northamptonshire"): {
        "query": "northampton hmo article 4 west northamptonshire council",
        "local_search_slug": "hmo-article-4-west-northamptonshire",
        "impressions": 459,
        "position": 9.32,
    },
    ("leicestershire", "charnwood"): {
        "query": "article 4 hmo charnwood loughborough blaby oadby wigston",
        "local_search_slug": "hmo-article-4-charnwood",
        "impressions": 422,
        "position": 9.65,
    },
    ("leicestershire", "blaby"): {
        "query": "article 4 hmo blaby",
        "local_search_slug": "hmo-article-4-blaby",
    },
    ("leicestershire", "harborough"): {
        "query": "article 4 hmo harborough",
        "local_search_slug": "hmo-article-4-harborough",
    },
    ("leicestershire", "oadby-and-wigston"): {
        "query": "article 4 hmo oadby and wigston",
        "local_search_slug": "hmo-article-4-oadby-and-wigston",
    },
    ("warwickshire", "nuneaton-and-bedworth"): {
        "query": "article 4 hmo nuneaton bedworth stratford daventry 2024 2025",
        "local_search_slug": "hmo-article-4-nuneaton-bedworth-warwickshire",
        "impressions": 338,
        "position": 8.17,
    },
}


GSC_EXPANSION_RELEASE_LIMITS = {
    "release": "second-stage-gsc-expansion-2026-06-08",
    "min_pages": 60,
    "max_pages": 80,
    "source_export": JUNE_8_2026_GSC_BASELINE["export"] if "JUNE_8_2026_GSC_BASELINE" in globals() else "https___ukplanningguide.co.uk_-Performance-on-Search-2026-06-08.zip",
    "keep_generated_local_search_disabled": True,
}


_CLUSTER_DEFAULTS = {
    "hmo-article-4": {
        "hub_slug": "hmo-article-4-checker",
        "hub_title": "HMO Article 4 Checker By Council",
        "capsule_title": "Settle Article 4 Coverage Before The HMO Route",
        "checks": (
            "Check the exact property against the Article 4 area or direction wording.",
            "Confirm whether the proposal is a change of use to an HMO.",
            "Treat permitted development as unsafe until the local coverage and use-class position are clear.",
        ),
        "next_step": "Open the local HMO or Article 4 page first, then verify the official council source if the route depends on coverage.",
    },
    "planning-portal": {
        "hub_slug": "planning-portal-council-checker",
        "hub_title": "Planning Portal And Council Route Checker",
        "capsule_title": "Use The Official Portal, Then Pick The Project Route",
        "checks": (
            "Start with the official council portal or validation source.",
            "Move into the project guide as soon as the build type is clear.",
            "Check conservation, Article 4, HMO or validation controls before relying on a broad council result.",
        ),
        "next_step": "Use the council route for orientation, then move into the project or topic page that decides the issue.",
    },
    "conservation-map": {
        "hub_slug": "conservation-area-map-checker",
        "hub_title": "Conservation Area Map And Planning Checker",
        "capsule_title": "Check The Official Conservation Area Position First",
        "checks": (
            "Open the official map, heritage source or conservation-area page before relying on a general rule.",
            "Check whether visibility, materials, demolition or frontage change is doing the real planning work.",
            "Use the project guide only after the heritage position is clear.",
        ),
        "next_step": "Confirm the designation first, then use the project route if the proposal still looks sensitive.",
    },
    "extension-drawings": {
        "hub_slug": "extension-drawings-validation-checker",
        "hub_title": "Extension Drawings And Validation Checker",
        "capsule_title": "Check The Drawing And Validation Route Before Spending",
        "checks": (
            "Confirm whether the project is still a simple householder route or already application-led.",
            "Check the drawings, site-plan and validation expectations before commissioning the wrong pack.",
            "Use the local extension guide once the council and project type are clear.",
        ),
        "next_step": "Open the local extension route first, then use drawing-readiness or validation checks before spend.",
    },
    "dropped-kerb-highway": {
        "hub_slug": "dropped-kerb-highway-checker",
        "hub_title": "Dropped Kerb And Highway Approval Checker",
        "capsule_title": "Separate Planning Permission From Highway Approval",
        "checks": (
            "Check whether planning permission, highway approval or both are needed.",
            "Confirm frontage visibility, access safety, drainage and hardstanding details.",
            "Use the dropped-kerb route before treating a driveway answer as complete.",
        ),
        "next_step": "Open the local dropped-kerb or driveway route, then verify the official highway source before works.",
    },
    "porch-outbuilding-rules": {
        "hub_slug": "porch-outbuilding-country-rules",
        "hub_title": "Porch And Outbuilding Rules In Scotland And Wales",
        "capsule_title": "Use The Country-Specific Rule Before The Generic UK Answer",
        "checks": (
            "Check whether Scotland or Wales has the controlling householder rule for the project.",
            "Confirm footprint, height, siting and relationship to a highway or boundary.",
            "Use official country or council sources where the project is close to a limit.",
        ),
        "next_step": "Open the country-specific porch or outbuilding route before relying on an England-led summary.",
    },
}


def _clean_text(value: str) -> str:
    return " ".join(str(value or "").split()).strip()


def _label_from_slug(slug: str) -> str:
    return str(slug or "").replace("-", " ").title()


def _expansion_candidate(
    *,
    slug: str,
    title: str,
    query: str,
    cluster: str,
    priority: int,
    authority_slug: str,
    county_slug: str,
    project_slug: str,
    target_scope: str = "council",
    project_scope: str = "council",
    council_slug: str | None = None,
    scenario_slug: str = "planning-permission",
    scenario_authority_slug: str | None = None,
    impressions: int | None = None,
    position: float | None = None,
    meta_title: str = "",
    meta_description: str = "",
    capsule_title: str = "",
    capsule_answer: str = "",
    capsule_checks: tuple[str, ...] | None = None,
    capsule_next_step: str = "",
    next_step_href: str = "",
    summary: str = "",
) -> dict:
    defaults = _CLUSTER_DEFAULTS[cluster]
    authority_label = _label_from_slug(authority_slug)
    local_council_slug = council_slug or (authority_slug if target_scope != "county" else "")
    local_scenario_authority_slug = scenario_authority_slug
    if local_scenario_authority_slug is None and target_scope != "county":
        local_scenario_authority_slug = local_council_slug or authority_slug
    if not next_step_href:
        if project_scope == "county":
            next_step_href = f"/{project_slug}/{county_slug}/"
        else:
            next_step_href = f"/{project_slug}/{county_slug}/{local_council_slug or authority_slug}/"
    if not meta_title:
        meta_title = f"{title}: planning route and official checks"
    if not meta_description:
        meta_description = (
            f"Check {title.lower()}, official sources, local restrictions and the next planning route "
            "before spending on drawings, applications or works."
        )
    if not capsule_answer:
        capsule_answer = (
            f"This query is best treated as a {defaults['hub_title'].lower()} route for {authority_label}, "
            "not as a broad planning search. The safer answer comes from the local route, official source "
            "and the project page that matches the work."
        )
    if not summary:
        summary = (
            f"A second-stage GSC expansion page for {query} searches that need a focused local route, "
            "the official source and the strongest next project or topic page."
        )

    return {
        "slug": slug,
        "title": title,
        "query": query,
        "cluster": cluster,
        "priority": priority,
        "impressions": impressions,
        "position": position,
        "target_route": next_step_href,
        "target_scope": target_scope,
        "authority_slug": authority_slug,
        "county_slug": county_slug,
        "council_slug": local_council_slug,
        "project_slug": project_slug,
        "project_scope": project_scope,
        "scenario_slug": scenario_slug,
        "scenario_authority_slug": local_scenario_authority_slug or "",
        "meta_title": _clean_text(meta_title),
        "meta_description": _clean_text(meta_description),
        "capsule_title": capsule_title or defaults["capsule_title"],
        "capsule_answer": _clean_text(capsule_answer),
        "capsule_checks": tuple(capsule_checks or defaults["checks"]),
        "capsule_next_step": capsule_next_step or defaults["next_step"],
        "next_step_href": next_step_href,
        "hub_slug": defaults["hub_slug"],
        "query_bucket": cluster,
        "summary": _clean_text(summary),
    }


def _cluster_hub(
    *,
    cluster: str,
    priority: int,
    query: str,
    authority_slug: str,
    county_slug: str,
    project_slug: str,
    target_scope: str = "county",
    project_scope: str = "county",
    scenario_slug: str = "planning-permission",
    scenario_authority_slug: str = "",
    summary: str,
    meta_description: str,
) -> dict:
    defaults = _CLUSTER_DEFAULTS[cluster]
    return _expansion_candidate(
        slug=defaults["hub_slug"],
        title=defaults["hub_title"],
        query=query,
        cluster=cluster,
        priority=priority,
        authority_slug=authority_slug,
        county_slug=county_slug,
        project_slug=project_slug,
        target_scope=target_scope,
        project_scope=project_scope,
        scenario_slug=scenario_slug,
        scenario_authority_slug=scenario_authority_slug,
        meta_title=f"{defaults['hub_title']}: local route checks",
        meta_description=meta_description,
        capsule_answer=summary,
        next_step_href=f"/{project_slug}/{county_slug}/",
        summary=summary,
    )


GSC_CLUSTER_HUBS = {
    "hmo-article-4": _cluster_hub(
        cluster="hmo-article-4",
        priority=1,
        query="hmo article 4 checker by council",
        authority_slug="staffordshire",
        county_slug="staffordshire",
        project_slug="hmos",
        summary="Use this hub to compare HMO Article 4 searches by council before assuming permitted development is still available for a change of use.",
        meta_description="Compare HMO Article 4 routes by council, including coverage, change of use, permitted-development risk and official local checks.",
    ),
    "planning-portal": _cluster_hub(
        cluster="planning-portal",
        priority=2,
        query="planning portal council checker",
        authority_slug="yorkshire",
        county_slug="yorkshire",
        project_slug="house-extensions",
        summary="Use this hub when a planning portal search needs to become an official council source check and then a project-specific planning route.",
        meta_description="Find the right council planning portal route, official source, project page and validation check before relying on a broad authority search.",
    ),
    "conservation-map": _cluster_hub(
        cluster="conservation-map",
        priority=3,
        query="conservation area map planning checker",
        authority_slug="greater-london",
        county_slug="greater-london",
        project_slug="house-extensions",
        scenario_slug="conservation-areas",
        scenario_authority_slug="westminster",
        summary="Use this hub when the decisive search intent is whether a property is inside a conservation area or another heritage-sensitive local control.",
        meta_description="Check conservation area maps, heritage controls, official sources and local project routes before relying on a broad planning answer.",
    ),
    "dropped-kerb-highway": _cluster_hub(
        cluster="dropped-kerb-highway",
        priority=4,
        query="dropped kerb highway approval planning checker",
        authority_slug="staffordshire",
        county_slug="staffordshire",
        project_slug="dropped-kerbs",
        summary="Use this hub to separate dropped-kerb planning permission from the highway, access, visibility, drainage and hardstanding checks.",
        meta_description="Check dropped kerb planning, highway approval, access visibility, drainage and official local routes before driveway or kerb works.",
    ),
    "extension-drawings": _cluster_hub(
        cluster="extension-drawings",
        priority=5,
        query="extension drawings planning validation checker",
        authority_slug="kent",
        county_slug="kent",
        project_slug="house-extensions",
        summary="Use this hub when extension searches have moved from broad permission questions into drawings, plans, validation and spend-order decisions.",
        meta_description="Check extension drawings, planning validation, local project routes and the safest next step before commissioning the wrong drawing pack.",
    ),
    "porch-outbuilding-rules": _cluster_hub(
        cluster="porch-outbuilding-rules",
        priority=6,
        query="porch outbuilding scotland wales official rules",
        authority_slug="scotland",
        county_slug="scotland",
        project_slug="porches",
        summary="Use this hub when porch, garden-room or outbuilding searches need Scotland or Wales rule wording before a generic UK answer.",
        meta_description="Check Scotland and Wales porch, garden-room and outbuilding rules, official sources and local routes before relying on a generic UK summary.",
    ),
}


GSC_EXPANSION_CANDIDATES_2026_06_08 = (
    _expansion_candidate(slug="hmo-article-4-loughborough", title="Loughborough HMO Article 4", query="loughborough hmo planning article 4 direction charnwood", cluster="hmo-article-4", priority=1, impressions=447, position=10.21, authority_slug="charnwood", county_slug="leicestershire", council_slug="charnwood", project_slug="hmos", next_step_href="/hmos/leicestershire/charnwood/article-4/"),
    _expansion_candidate(slug="hmo-article-4-daventry", title="Daventry HMO Article 4", query="daventry hmo article 4 west northamptonshire", cluster="hmo-article-4", priority=2, authority_slug="west-northamptonshire", county_slug="northamptonshire", council_slug="west-northamptonshire", project_slug="hmos", next_step_href="/hmos/northamptonshire/west-northamptonshire/article-4/"),
    _expansion_candidate(slug="hmo-article-4-stratford-on-avon", title="Stratford-on-Avon HMO Article 4", query="stratford on avon hmo article 4 direction", cluster="hmo-article-4", priority=3, authority_slug="stratford-on-avon", county_slug="warwickshire", council_slug="stratford-on-avon", project_slug="hmos", next_step_href="/hmos/warwickshire/stratford-on-avon/article-4/"),
    _expansion_candidate(slug="hmo-article-4-rugby", title="Rugby HMO Article 4", query="rugby hmo article 4 planning permission", cluster="hmo-article-4", priority=4, authority_slug="rugby", county_slug="warwickshire", council_slug="rugby", project_slug="hmos", next_step_href="/hmos/warwickshire/rugby/article-4/"),
    _expansion_candidate(slug="hmo-article-4-northampton", title="Northampton HMO Article 4", query="northampton hmo article 4 west northamptonshire council", cluster="hmo-article-4", priority=5, impressions=462, position=9.32, authority_slug="west-northamptonshire", county_slug="northamptonshire", council_slug="west-northamptonshire", project_slug="hmos", next_step_href="/hmos/northamptonshire/west-northamptonshire/article-4/"),
    _expansion_candidate(slug="hmo-article-4-kettering", title="Kettering HMO Article 4", query="kettering hmo article 4 north northamptonshire", cluster="hmo-article-4", priority=6, authority_slug="north-northamptonshire", county_slug="northamptonshire", council_slug="north-northamptonshire", project_slug="hmos", next_step_href="/hmos/northamptonshire/north-northamptonshire/article-4/"),
    _expansion_candidate(slug="hmo-article-4-corby", title="Corby HMO Article 4", query="corby hmo article 4 north northamptonshire", cluster="hmo-article-4", priority=7, authority_slug="north-northamptonshire", county_slug="northamptonshire", council_slug="north-northamptonshire", project_slug="hmos", next_step_href="/hmos/northamptonshire/north-northamptonshire/article-4/"),
    _expansion_candidate(slug="hmo-article-4-wellingborough", title="Wellingborough HMO Article 4", query="wellingborough hmo article 4 north northamptonshire", cluster="hmo-article-4", priority=8, authority_slug="north-northamptonshire", county_slug="northamptonshire", council_slug="north-northamptonshire", project_slug="hmos", next_step_href="/hmos/northamptonshire/north-northamptonshire/article-4/"),
    _expansion_candidate(slug="hmo-article-4-nottingham", title="Nottingham HMO Article 4", query="nottingham hmo article 4 direction", cluster="hmo-article-4", priority=9, authority_slug="nottingham", county_slug="nottinghamshire", council_slug="nottingham", project_slug="hmos", next_step_href="/hmos/nottinghamshire/nottingham/article-4/"),
    _expansion_candidate(slug="hmo-article-4-brent", title="Brent HMO Article 4", query="brent hmo article 4 planning", cluster="hmo-article-4", priority=10, authority_slug="brent", county_slug="greater-london", council_slug="brent", project_slug="hmos", next_step_href="/hmos/greater-london/brent/article-4/"),
    _expansion_candidate(slug="hmo-article-4-harrow", title="Harrow HMO Article 4", query="harrow hmo article 4 planning", cluster="hmo-article-4", priority=11, authority_slug="harrow", county_slug="greater-london", council_slug="harrow", project_slug="hmos", next_step_href="/hmos/greater-london/harrow/article-4/"),
    _expansion_candidate(slug="hmo-article-4-portsmouth", title="Portsmouth HMO Article 4", query="portsmouth hmo article 4 planning", cluster="hmo-article-4", priority=12, authority_slug="portsmouth", county_slug="hampshire", council_slug="portsmouth", project_slug="hmos", next_step_href="/hmos/hampshire/portsmouth/article-4/"),
    _expansion_candidate(slug="hmo-article-4-southampton", title="Southampton HMO Article 4", query="southampton hmo article 4 planning", cluster="hmo-article-4", priority=13, authority_slug="southampton", county_slug="hampshire", council_slug="southampton", project_slug="hmos", next_step_href="/hmos/hampshire/southampton/article-4/"),
    _expansion_candidate(slug="hmo-article-4-north-northamptonshire", title="North Northamptonshire HMO Article 4", query="north northamptonshire hmo article 4", cluster="hmo-article-4", priority=14, authority_slug="north-northamptonshire", county_slug="northamptonshire", council_slug="north-northamptonshire", project_slug="hmos", next_step_href="/hmos/northamptonshire/north-northamptonshire/article-4/"),
    _expansion_candidate(slug="hmo-article-4-warwickshire", title="Warwickshire HMO Article 4", query="warwickshire hmo article 4 nuneaton bedworth stratford rugby", cluster="hmo-article-4", priority=15, authority_slug="warwickshire", county_slug="warwickshire", project_slug="hmos", target_scope="county", project_scope="county", next_step_href="/hmos/warwickshire/"),
    _expansion_candidate(slug="planning-portal-cornwall", title="Cornwall Planning Portal", query="cornwall planning portal", cluster="planning-portal", priority=16, impressions=275, position=16.87, authority_slug="cornwall", county_slug="cornwall", council_slug="cornwall", project_slug="house-extensions", next_step_href="/councils/cornwall/"),
    _expansion_candidate(slug="planning-portal-croydon", title="Croydon Planning Portal", query="croydon planning portal", cluster="planning-portal", priority=17, authority_slug="croydon", county_slug="greater-london", council_slug="croydon", project_slug="house-extensions", next_step_href="/councils/croydon/"),
    _expansion_candidate(slug="planning-portal-leeds", title="Leeds Planning Portal", query="leeds planning portal", cluster="planning-portal", priority=18, authority_slug="leeds", county_slug="yorkshire", council_slug="leeds", project_slug="house-extensions", next_step_href="/councils/leeds/"),
    _expansion_candidate(slug="planning-portal-york", title="York Planning Portal", query="york planning portal", cluster="planning-portal", priority=19, authority_slug="york", county_slug="yorkshire", council_slug="york", project_slug="house-extensions", next_step_href="/councils/york/"),
    _expansion_candidate(slug="planning-portal-bradford", title="Bradford Planning Portal", query="bradford planning portal", cluster="planning-portal", priority=20, authority_slug="bradford", county_slug="yorkshire", council_slug="bradford", project_slug="house-extensions", next_step_href="/councils/bradford/"),
    _expansion_candidate(slug="planning-portal-wakefield", title="Wakefield Planning Portal", query="wakefield planning portal", cluster="planning-portal", priority=21, authority_slug="wakefield", county_slug="yorkshire", council_slug="wakefield", project_slug="house-extensions", next_step_href="/councils/wakefield/"),
    _expansion_candidate(slug="planning-portal-camden", title="Camden Planning Portal", query="camden planning portal", cluster="planning-portal", priority=22, authority_slug="camden", county_slug="greater-london", council_slug="camden", project_slug="house-extensions", next_step_href="/councils/camden/"),
    _expansion_candidate(slug="planning-portal-glasgow-city", title="Glasgow City Planning Portal", query="glasgow city planning portal", cluster="planning-portal", priority=23, authority_slug="glasgow-city", county_slug="scotland", council_slug="glasgow-city", project_slug="house-extensions", next_step_href="/councils/glasgow-city/"),
    _expansion_candidate(slug="planning-portal-aberdeen-city", title="Aberdeen City Planning Portal", query="aberdeen city planning portal", cluster="planning-portal", priority=24, authority_slug="aberdeen-city", county_slug="scotland", council_slug="aberdeen-city", project_slug="house-extensions", next_step_href="/councils/aberdeen-city/"),
    _expansion_candidate(slug="planning-portal-durham", title="Durham Planning Portal", query="county durham planning portal", cluster="planning-portal", priority=25, authority_slug="durham", county_slug="county-durham", council_slug="durham", project_slug="house-extensions", next_step_href="/councils/durham/"),
    _expansion_candidate(slug="planning-portal-east-riding-of-yorkshire", title="East Riding Planning Portal", query="east riding of yorkshire planning portal", cluster="planning-portal", priority=26, authority_slug="east-riding-of-yorkshire", county_slug="yorkshire", council_slug="east-riding-of-yorkshire", project_slug="house-extensions", next_step_href="/councils/east-riding-of-yorkshire/"),
    _expansion_candidate(slug="planning-portal-richmond-upon-thames", title="Richmond upon Thames Planning Portal", query="richmond upon thames planning portal", cluster="planning-portal", priority=27, authority_slug="richmond-upon-thames", county_slug="greater-london", council_slug="richmond-upon-thames", project_slug="house-extensions", next_step_href="/councils/richmond-upon-thames/"),
    _expansion_candidate(slug="planning-portal-hammersmith-and-fulham", title="Hammersmith and Fulham Planning Portal", query="hammersmith fulham planning portal", cluster="planning-portal", priority=28, authority_slug="hammersmith-and-fulham", county_slug="greater-london", council_slug="hammersmith-and-fulham", project_slug="house-extensions", next_step_href="/councils/hammersmith-and-fulham/"),
    _expansion_candidate(slug="planning-portal-westminster", title="Westminster Planning Portal", query="westminster planning portal", cluster="planning-portal", priority=29, authority_slug="westminster", county_slug="greater-london", council_slug="westminster", project_slug="house-extensions", next_step_href="/councils/westminster/"),
    _expansion_candidate(slug="planning-portal-north-yorkshire", title="North Yorkshire Planning Portal", query="north yorkshire planning portal", cluster="planning-portal", priority=30, authority_slug="north-yorkshire", county_slug="yorkshire", council_slug="north-yorkshire", project_slug="house-extensions", next_step_href="/councils/north-yorkshire/"),
    _expansion_candidate(slug="extension-drawings-folkestone", title="Extension Drawings In Folkestone", query="extension drawings folkestone planning", cluster="extension-drawings", priority=31, authority_slug="folkestone-and-hythe", county_slug="kent", council_slug="folkestone-and-hythe", project_slug="house-extensions", next_step_href="/house-extensions/kent/folkestone-and-hythe/"),
    _expansion_candidate(slug="planning-drawings-bromsgrove", title="Planning Drawings In Bromsgrove", query="planning drawings bromsgrove", cluster="extension-drawings", priority=32, impressions=271, position=5.10, authority_slug="bromsgrove", county_slug="worcestershire", council_slug="bromsgrove", project_slug="house-extensions", next_step_href="/house-extensions/worcestershire/bromsgrove/"),
    _expansion_candidate(slug="house-extension-drawings-hagley", title="House Extension Drawings In Hagley", query="house extension drawings hagley bromsgrove", cluster="extension-drawings", priority=33, authority_slug="bromsgrove", county_slug="worcestershire", council_slug="bromsgrove", project_slug="house-extensions", next_step_href="/house-extensions/worcestershire/bromsgrove/"),
    _expansion_candidate(slug="extension-plans-merton", title="Extension Plans In Merton", query="extension plans merton park planning", cluster="extension-drawings", priority=34, authority_slug="merton", county_slug="greater-london", council_slug="merton", project_slug="house-extensions", next_step_href="/house-extensions/greater-london/merton/"),
    _expansion_candidate(slug="extension-plans-uttlesford", title="Extension Plans In Uttlesford", query="extension plans uttlesford planning", cluster="extension-drawings", priority=35, authority_slug="uttlesford", county_slug="essex", council_slug="uttlesford", project_slug="house-extensions", next_step_href="/house-extensions/essex/uttlesford/"),
    _expansion_candidate(slug="extension-plans-norfolk", title="Extension Plans In Norfolk", query="extension plans norfolk planning", cluster="extension-drawings", priority=36, authority_slug="norfolk", county_slug="norfolk", project_slug="house-extensions", target_scope="county", project_scope="county", next_step_href="/house-extensions/norfolk/"),
    _expansion_candidate(slug="extension-plans-surrey", title="Extension Plans In Surrey", query="extension plans surrey planning", cluster="extension-drawings", priority=37, authority_slug="surrey", county_slug="surrey", project_slug="house-extensions", target_scope="county", project_scope="county", next_step_href="/house-extensions/surrey/"),
    _expansion_candidate(slug="extension-plans-croydon", title="Extension Plans In Croydon", query="extension plans croydon planning", cluster="extension-drawings", priority=38, authority_slug="croydon", county_slug="greater-london", council_slug="croydon", project_slug="house-extensions", next_step_href="/house-extensions/greater-london/croydon/"),
    _expansion_candidate(slug="extension-plans-richmond-upon-thames", title="Extension Plans In Richmond upon Thames", query="extension plans richmond upon thames", cluster="extension-drawings", priority=39, authority_slug="richmond-upon-thames", county_slug="greater-london", council_slug="richmond-upon-thames", project_slug="house-extensions", next_step_href="/house-extensions/greater-london/richmond-upon-thames/"),
    _expansion_candidate(slug="extension-plans-wandsworth", title="Extension Plans In Wandsworth", query="extension plans wandsworth planning", cluster="extension-drawings", priority=40, authority_slug="wandsworth", county_slug="greater-london", council_slug="wandsworth", project_slug="house-extensions", next_step_href="/house-extensions/greater-london/wandsworth/"),
    _expansion_candidate(slug="planning-drawings-cambridge", title="Planning Drawings In Cambridge", query="planning drawings cambridge extension", cluster="extension-drawings", priority=41, authority_slug="cambridge", county_slug="cambridgeshire", council_slug="cambridge", project_slug="house-extensions", next_step_href="/house-extensions/cambridgeshire/cambridge/"),
    _expansion_candidate(slug="planning-drawings-st-albans", title="Planning Drawings In St Albans", query="planning drawings st albans extension", cluster="extension-drawings", priority=42, authority_slug="st-albans", county_slug="hertfordshire", council_slug="st-albans", project_slug="house-extensions", next_step_href="/house-extensions/hertfordshire/st-albans/"),
    _expansion_candidate(slug="planning-drawings-eastleigh", title="Planning Drawings In Eastleigh", query="planning drawings eastleigh extension", cluster="extension-drawings", priority=43, authority_slug="eastleigh", county_slug="hampshire", council_slug="eastleigh", project_slug="house-extensions", next_step_href="/house-extensions/hampshire/eastleigh/"),
    _expansion_candidate(slug="planning-drawings-babergh", title="Planning Drawings In Babergh", query="planning drawings babergh extension", cluster="extension-drawings", priority=44, authority_slug="babergh", county_slug="suffolk", council_slug="babergh", project_slug="house-extensions", next_step_href="/house-extensions/suffolk/babergh/"),
    _expansion_candidate(slug="planning-drawings-south-hams", title="Planning Drawings In South Hams", query="planning drawings south hams extension", cluster="extension-drawings", priority=45, authority_slug="south-hams", county_slug="devon", council_slug="south-hams", project_slug="house-extensions", next_step_href="/house-extensions/devon/south-hams/"),
    _expansion_candidate(slug="porch-planning-permission-scotland", title="Porch Planning Permission In Scotland", query="scotland porch planning permission 3 square metres official", cluster="porch-outbuilding-rules", priority=46, impressions=306, position=7.82, authority_slug="scotland", county_slug="scotland", project_slug="porches", target_scope="county", project_scope="county", next_step_href="/porches/scotland/"),
    _expansion_candidate(slug="porch-planning-permission-city-of-edinburgh", title="Porch Planning Permission In Edinburgh", query="edinburgh porch planning permission", cluster="porch-outbuilding-rules", priority=47, authority_slug="city-of-edinburgh", county_slug="scotland", council_slug="city-of-edinburgh", project_slug="porches", next_step_href="/porches/scotland/city-of-edinburgh/"),
    _expansion_candidate(slug="porch-planning-permission-glasgow-city", title="Porch Planning Permission In Glasgow City", query="glasgow porch planning permission", cluster="porch-outbuilding-rules", priority=48, authority_slug="glasgow-city", county_slug="scotland", council_slug="glasgow-city", project_slug="porches", next_step_href="/porches/scotland/glasgow-city/"),
    _expansion_candidate(slug="porch-planning-permission-aberdeen-city", title="Porch Planning Permission In Aberdeen City", query="aberdeen porch planning permission", cluster="porch-outbuilding-rules", priority=49, authority_slug="aberdeen-city", county_slug="scotland", council_slug="aberdeen-city", project_slug="porches", next_step_href="/porches/scotland/aberdeen-city/"),
    _expansion_candidate(slug="porch-planning-permission-wales", title="Porch Planning Permission In Wales", query="wales porch planning permission 3 square metres", cluster="porch-outbuilding-rules", priority=50, authority_slug="wales", county_slug="wales", project_slug="porches", target_scope="county", project_scope="county", next_step_href="/porches/wales/"),
    _expansion_candidate(slug="porch-planning-permission-swansea", title="Porch Planning Permission In Swansea", query="swansea porch planning permission", cluster="porch-outbuilding-rules", priority=51, authority_slug="swansea", county_slug="wales", council_slug="swansea", project_slug="porches", next_step_href="/porches/wales/swansea/"),
    _expansion_candidate(slug="porch-planning-permission-gwynedd", title="Porch Planning Permission In Gwynedd", query="gwynedd porch planning permission", cluster="porch-outbuilding-rules", priority=52, authority_slug="gwynedd", county_slug="wales", council_slug="gwynedd", project_slug="porches", next_step_href="/porches/wales/gwynedd/"),
    _expansion_candidate(slug="outbuildings-wales-permitted-development", title="Outbuildings In Wales", query="outbuildings wales permitted development", cluster="porch-outbuilding-rules", priority=53, authority_slug="wales", county_slug="wales", project_slug="outbuildings", target_scope="county", project_scope="county", scenario_slug="permitted-development", next_step_href="/outbuildings/wales/"),
    _expansion_candidate(slug="outbuildings-scotland-official-rules", title="Outbuildings In Scotland", query="outbuildings scotland official planning rules", cluster="porch-outbuilding-rules", priority=54, authority_slug="scotland", county_slug="scotland", project_slug="outbuildings", target_scope="county", project_scope="county", next_step_href="/outbuildings/scotland/"),
    _expansion_candidate(slug="garden-room-scotland-planning", title="Garden Rooms In Scotland", query="garden room scotland planning permission", cluster="porch-outbuilding-rules", priority=55, authority_slug="scotland", county_slug="scotland", project_slug="garden-rooms", target_scope="county", project_scope="county", next_step_href="/garden-rooms/scotland/"),
    _expansion_candidate(slug="dropped-kerb-plymouth", title="Dropped Kerbs In Plymouth", query="dropped kerb plymouth planning highway approval", cluster="dropped-kerb-highway", priority=56, authority_slug="plymouth", county_slug="devon", council_slug="plymouth", project_slug="dropped-kerbs", next_step_href="/dropped-kerbs/devon/plymouth/"),
    _expansion_candidate(slug="dropped-kerb-devon", title="Dropped Kerbs In Devon", query="dropped kerb devon highway planning", cluster="dropped-kerb-highway", priority=57, authority_slug="devon", county_slug="devon", project_slug="dropped-kerbs", target_scope="county", project_scope="county", next_step_href="/dropped-kerbs/devon/"),
    _expansion_candidate(slug="dropped-kerb-cornwall", title="Dropped Kerbs In Cornwall", query="dropped kerb cornwall planning highway", cluster="dropped-kerb-highway", priority=58, authority_slug="cornwall", county_slug="cornwall", council_slug="cornwall", project_slug="dropped-kerbs", next_step_href="/dropped-kerbs/cornwall/cornwall/"),
    _expansion_candidate(slug="dropped-kerb-leeds", title="Dropped Kerbs In Leeds", query="dropped kerb leeds planning highway", cluster="dropped-kerb-highway", priority=59, authority_slug="leeds", county_slug="yorkshire", council_slug="leeds", project_slug="dropped-kerbs", next_step_href="/dropped-kerbs/yorkshire/leeds/"),
    _expansion_candidate(slug="dropped-kerb-croydon", title="Dropped Kerbs In Croydon", query="dropped kerb croydon planning highway", cluster="dropped-kerb-highway", priority=60, authority_slug="croydon", county_slug="greater-london", council_slug="croydon", project_slug="dropped-kerbs", next_step_href="/dropped-kerbs/greater-london/croydon/"),
    _expansion_candidate(slug="dropped-kerb-merton", title="Dropped Kerbs In Merton", query="dropped kerb merton planning highway", cluster="dropped-kerb-highway", priority=61, authority_slug="merton", county_slug="greater-london", council_slug="merton", project_slug="dropped-kerbs", next_step_href="/dropped-kerbs/greater-london/merton/"),
    _expansion_candidate(slug="dropped-kerb-richmond-upon-thames", title="Dropped Kerbs In Richmond upon Thames", query="dropped kerb richmond upon thames planning", cluster="dropped-kerb-highway", priority=62, authority_slug="richmond-upon-thames", county_slug="greater-london", council_slug="richmond-upon-thames", project_slug="dropped-kerbs", next_step_href="/dropped-kerbs/greater-london/richmond-upon-thames/"),
    _expansion_candidate(slug="dropped-kerb-westminster", title="Dropped Kerbs In Westminster", query="dropped kerb westminster planning highway", cluster="dropped-kerb-highway", priority=63, authority_slug="westminster", county_slug="greater-london", council_slug="westminster", project_slug="dropped-kerbs", next_step_href="/dropped-kerbs/greater-london/westminster/"),
    _expansion_candidate(slug="driveway-dropped-kerb-barking", title="Driveway And Dropped Kerb In Barking", query="driveway dropped kerb barking planning", cluster="dropped-kerb-highway", priority=64, authority_slug="barking-and-dagenham", county_slug="greater-london", council_slug="barking-and-dagenham", project_slug="driveways", next_step_href="/driveways/greater-london/barking-and-dagenham/"),
    _expansion_candidate(slug="driveway-planning-croydon", title="Driveway Planning In Croydon", query="driveway planning croydon dropped kerb", cluster="dropped-kerb-highway", priority=65, authority_slug="croydon", county_slug="greater-london", council_slug="croydon", project_slug="driveways", next_step_href="/driveways/greater-london/croydon/"),
    _expansion_candidate(slug="highway-dropped-kerb-staffordshire", title="Highway Dropped Kerb Checks In Staffordshire", query="dropped kerb staffordshire highway approval", cluster="dropped-kerb-highway", priority=66, impressions=249, position=19.28, authority_slug="staffordshire", county_slug="staffordshire", project_slug="dropped-kerbs", target_scope="county", project_scope="county", next_step_href="/dropped-kerbs/staffordshire/"),
    _expansion_candidate(slug="dropped-kerb-northampton", title="Dropped Kerbs In Northampton", query="dropped kerb northampton planning highway", cluster="dropped-kerb-highway", priority=67, authority_slug="west-northamptonshire", county_slug="northamptonshire", council_slug="west-northamptonshire", project_slug="dropped-kerbs", next_step_href="/dropped-kerbs/northamptonshire/west-northamptonshire/"),
    _expansion_candidate(slug="conservation-area-map-westminster", title="Westminster Conservation Area Map", query="westminster conservation areas map", cluster="conservation-map", priority=68, impressions=167, position=8.32, authority_slug="westminster", county_slug="greater-london", council_slug="westminster", project_slug="house-extensions", scenario_slug="conservation-areas", next_step_href="/conservation-areas/westminster/"),
    _expansion_candidate(slug="conservation-area-map-glasgow-city", title="Glasgow City Conservation Area Map", query="glasgow city conservation area map", cluster="conservation-map", priority=69, authority_slug="glasgow-city", county_slug="scotland", council_slug="glasgow-city", project_slug="house-extensions", scenario_slug="conservation-areas", next_step_href="/conservation-areas/glasgow-city/"),
    _expansion_candidate(slug="conservation-area-map-portsmouth", title="Portsmouth Conservation Area Map", query="portsmouth conservation area map", cluster="conservation-map", priority=70, authority_slug="portsmouth", county_slug="hampshire", council_slug="portsmouth", project_slug="house-extensions", scenario_slug="conservation-areas", next_step_href="/conservation-areas/portsmouth/"),
    _expansion_candidate(slug="conservation-area-map-southwark", title="Southwark Conservation Area Map", query="southwark conservation area map", cluster="conservation-map", priority=71, authority_slug="southwark", county_slug="greater-london", council_slug="southwark", project_slug="house-extensions", scenario_slug="conservation-areas", next_step_href="/conservation-areas/southwark/"),
    _expansion_candidate(slug="conservation-area-map-buckinghamshire", title="Buckinghamshire Conservation Area Map", query="buckinghamshire conservation areas map", cluster="conservation-map", priority=72, authority_slug="buckinghamshire", county_slug="buckinghamshire", council_slug="buckinghamshire", project_slug="house-extensions", scenario_slug="conservation-areas", next_step_href="/conservation-areas/buckinghamshire/"),
)


GSC_CLUSTER_HUB_SLUGS = tuple(sorted(hub["slug"] for hub in GSC_CLUSTER_HUBS.values()))
GSC_EXPANSION_CANDIDATE_SLUGS = tuple(
    sorted(candidate["slug"] for candidate in GSC_EXPANSION_CANDIDATES_2026_06_08)
)
GSC_EXPANSION_LOCAL_SEARCH_SLUGS = tuple(sorted(GSC_CLUSTER_HUB_SLUGS + GSC_EXPANSION_CANDIDATE_SLUGS))


DATA_LED_LOCAL_SEARCH_SLUGS = tuple(
    sorted(
        {
            route["local_search_slug"]
            for route in HMO_ARTICLE_4_PRIORITY_ROUTES.values()
            if route.get("local_search_slug")
        }
        | {
            "hmo-article-4-leicestershire",
            "hmo-article-4-milton-keynes",
            "hmo-article-4-west-northamptonshire",
            "hmo-article-4-nuneaton-bedworth-warwickshire",
            "planning-permission-newham",
            "westminster-conservation-areas",
            "planning-permission-eastleigh",
            "outbuildings-glasgow-city",
            "property-extension-folkestone",
            "planning-portal-sheffield",
            "planning-permission-cornwall",
            "planning-torridge",
            "planning-dagenham",
            "planning-fulham",
            "planning-permission-bromsgrove",
            "garage-conversion-basildon",
            "loft-extension-planning-greenwich",
            "house-extension-flitwick",
            "solar-panels-teignbridge",
            "house-extension-windsor",
        }
        | set(GSC_EXPANSION_LOCAL_SEARCH_SLUGS)
    )
)


CTR_RESCUE_LOCAL_SEARCH_SLUGS = tuple(
    sorted(
        {
            "hmo-article-4-tamworth",
            "hmo-article-4-stafford",
            "hmo-article-4-milton-keynes",
            "hmo-article-4-west-northamptonshire",
            "hmo-article-4-charnwood",
            "hmo-article-4-leicestershire",
            "hmo-article-4-nuneaton-bedworth-warwickshire",
            "outbuildings-glasgow-city",
            "westminster-conservation-areas",
            "planning-permission-newham",
            "property-extension-folkestone",
            "planning-portal-sheffield",
            "planning-permission-cornwall",
            "planning-torridge",
            "planning-dagenham",
            "planning-fulham",
            "planning-permission-bromsgrove",
            "garage-conversion-basildon",
            "loft-extension-planning-greenwich",
            "house-extension-flitwick",
            "solar-panels-teignbridge",
            "house-extension-windsor",
        }
        | set(GSC_EXPANSION_LOCAL_SEARCH_SLUGS)
    )
)


LOW_CTR_PAGE_TARGETS = (
    "/conservation-areas/glasgow-city/",
    "/hmos/leicestershire/oadby-and-wigston/",
    "/councils/sheffield/",
    "/local-search/outbuildings-glasgow-city/",
    "/councils/aberdeen-city/",
    "/porches/wales/gwynedd/",
    "/councils/barking-and-dagenham/",
    "/outbuildings/scotland/east-lothian/",
    "/rear-extensions/greater-london/brent/conservation-areas/",
    "/local-search/westminster-conservation-areas/",
    "/councils/croydon/",
    "/dropped-kerbs/staffordshire/staffordshire-moorlands/",
    "/conservation-areas/portsmouth/",
    "/driveways/greater-london/barking-and-dagenham/",
    "/outbuildings/greater-london/brent/article-4/",
    "/planning-permission/carmarthenshire/",
    "/porches/scotland/south-lanarkshire/",
    "/porches/wales/cardiff/",
)


JUNE_8_2026_GSC_BASELINE = {
    "export": "https___ukplanningguide.co.uk_-Performance-on-Search-2026-06-08.zip",
    "date_range": "last 3 months",
    "clicks": 6047,
    "impressions": 374727,
    "ctr": 1.61,
    "first_28_days_clicks": 1382,
    "first_28_days_impressions": 95401,
    "first_28_days_ctr": 1.45,
    "first_28_days_position": 23.08,
    "last_28_days_clicks": 2735,
    "last_28_days_impressions": 158038,
    "last_28_days_ctr": 1.73,
    "last_28_days_position": 9.98,
    "desktop_ctr": 1.01,
    "mobile_ctr": 2.71,
    "uk_ctr": 2.06,
    "search_appearance_rows": 0,
}


JUNE_2026_GSC_BASELINE = {
    **JUNE_8_2026_GSC_BASELINE,
}


JULY_3_2026_GSC_BASELINE = {
    "export": "https___ukplanningguide.co.uk_-Performance-on-Search-2026-07-03.zip",
    "date_range": "last 3 months",
    "data_start": "2026-04-02",
    "data_end": "2026-07-01",
    "complete_day_cutoff": "2026-06-30",
    "clicks": 7711,
    "impressions": 477637,
    "ctr": 1.61,
    "latest_complete_week_clicks": 821,
    "latest_complete_week_impressions": 51804,
    "latest_complete_week_ctr": 1.58,
    "previous_complete_week_clicks": 767,
    "previous_complete_week_impressions": 64914,
    "previous_complete_week_ctr": 1.18,
    "post_release_clicks": 2654,
    "post_release_impressions": 174419,
    "post_release_ctr": 1.52,
    "post_release_position": 11.27,
    "pre_release_equal_clicks": 2429,
    "pre_release_equal_impressions": 134290,
    "pre_release_equal_ctr": 1.81,
    "pre_release_equal_position": 10.25,
    "uk_clicks": 7500,
    "uk_impressions": 352542,
    "uk_ctr": 2.13,
    "desktop_ctr": 1.01,
    "mobile_ctr": 2.71,
    "search_appearance_rows": 0,
    "preliminary_last_day": {
        "date": "2026-07-01",
        "clicks": 1,
        "impressions": 284,
        "position": 51.9,
    },
}


GSC_BASELINE_HISTORY = (
    JUNE_8_2026_GSC_BASELINE,
    JULY_3_2026_GSC_BASELINE,
)


LATEST_GSC_BASELINE = JULY_3_2026_GSC_BASELINE


GSC_2026_06_08_PAGE_TARGETS = {
    "/conservation-areas/glasgow-city/": {
        "meta_title": "Glasgow City conservation areas: official map and planning checks",
        "meta_description": "Check Glasgow City conservation areas, official heritage sources, planning tripwires and the safest next local page before relying on a broad answer.",
        "title": "Check The Official Conservation Area First",
        "answer": "For Glasgow City, the winning answer needs to start with whether the property is inside a conservation area. Once that is settled, the project-specific planning route becomes much easier to judge.",
        "checks": (
            "Open the official conservation-area or heritage source before relying on a general rule.",
            "Check whether visibility, materials, demolition or frontage change is doing the real planning work.",
            "Use the project guide only after the heritage position is clear.",
        ),
        "next_step": "Start with official sources, then move into the local project or planning-permission route if the proposal still looks sensitive.",
        "primary_href": "/conservation-areas/glasgow-city/",
    },
    "/hmos/leicestershire/oadby-and-wigston/": {
        "meta_title": "Oadby and Wigston HMO Article 4: change of use and local checks",
        "meta_description": "Check HMO planning in Oadby and Wigston, including Article 4, change of use, local concentration and whether permitted development is safe.",
        "title": "Treat This As An HMO Change-Of-Use Check",
        "answer": "The live question in Oadby and Wigston is whether Article 4, concentration pressure or local amenity policy removes the simple HMO assumption. Do not treat it as a generic householder route.",
        "checks": (
            "Check Article 4 coverage for the exact property and proposed use.",
            "Look at local concentration, parking, refuse and neighbour amenity before assuming the change is low-risk.",
            "Use the HMO route first, then the authority page if policy wording is still unclear.",
        ),
        "next_step": "Open the Article 4 or local-search HMO route if the proposal depends on permitted development still being available.",
        "primary_href": "/local-search/hmo-article-4-oadby-and-wigston/",
    },
    "/councils/sheffield/": {
        "meta_title": "Sheffield planning portal, permission routes and council checks",
        "meta_description": "Use the Sheffield planning portal route, council sources, local project guides and permission checks before relying on a broad planning search.",
        "title": "Use This As The Sheffield Portal And Route Page",
        "answer": "Most Sheffield planning searches need a fast handoff to the official portal, then the right project or rule page. The council layer is the start point, not the whole answer.",
        "checks": (
            "Use the official Sheffield planning application and validation source first.",
            "Move into the project page once the build type is clear.",
            "Check conservation, Article 4 or HMO controls before relying on a simple route.",
        ),
        "next_step": "If the query is about the portal, open official sources first; if it is about a project, jump into the matching local project guide.",
        "primary_href": "/local-search/planning-portal-sheffield/",
    },
    "/councils/aberdeen-city/": {
        "meta_title": "Aberdeen City planning permission: council route and checks",
        "meta_description": "Use the Aberdeen City council page for planning permission routes, official sources, project guides and local checks before relying on a broad answer.",
        "title": "Start With The Aberdeen City Council Route",
        "answer": "For Aberdeen City, the broad council query should quickly become a project, rule or official-source check. The useful answer is the path to the right next page.",
        "checks": (
            "Confirm the official council source before using a generic planning answer.",
            "Open the local project page as soon as the build type is known.",
            "Check heritage or local restrictions if the project is close to a threshold.",
        ),
        "next_step": "Use the council route as orientation, then move into the project or topic page that decides the issue.",
        "primary_href": "/councils/aberdeen-city/",
    },
    "/outbuildings/scotland/east-lothian/": {
        "meta_title": "Outbuildings in East Lothian: Scottish planning and local checks",
        "meta_description": "Check outbuilding planning in East Lothian, including Scottish rules, height, use, local restrictions and official checks before relying on a shortcut.",
        "title": "Check The Scottish Outbuilding Route",
        "answer": "For East Lothian outbuildings, the first job is to confirm whether the structure still reads as a normal domestic outbuilding under the Scottish planning route.",
        "checks": (
            "Check height, siting and whether the use stays secondary to the main house.",
            "Slow down where conservation, listed-building or local design controls are involved.",
            "Use official sources before relying on a broad UK outbuilding answer.",
        ),
        "next_step": "Open the local outbuilding route first, then verify official Scottish or council sources if the proposal is close to a limit.",
        "primary_href": "/outbuildings/scotland/east-lothian/",
    },
    "/dropped-kerbs/devon/plymouth/": {
        "meta_title": "Dropped kerbs in Plymouth: planning, highway and access checks",
        "meta_description": "Check Plymouth dropped kerb planning, highway approval, access visibility, drainage and the official route before paying for the wrong work.",
        "title": "Separate Planning From Highway Approval",
        "answer": "For Plymouth dropped kerbs, the planning answer is only half the route if the access, highway or drainage approval is what actually decides the job.",
        "checks": (
            "Check whether planning permission and highway approval are both needed.",
            "Confirm frontage visibility and access safety before treating the route as simple.",
            "Check drainage or surfacing if a new driveway is part of the same job.",
        ),
        "next_step": "Use the dropped-kerb page first, then the official highway/access source before committing to works.",
        "primary_href": "/dropped-kerbs/devon/plymouth/",
    },
    "/driveways/greater-london/barking-and-dagenham/": {
        "meta_title": "Driveways in Barking and Dagenham: planning, drainage and kerb checks",
        "meta_description": "Check driveway planning in Barking and Dagenham, including drainage, frontage, dropped kerb and highway checks before relying on a broad answer.",
        "title": "Check Drainage, Frontage And Kerb Route Together",
        "answer": "For Barking and Dagenham driveways, the useful answer has to separate surface drainage, frontage layout and whether a dropped kerb or highway approval is part of the same route.",
        "checks": (
            "Check whether the driveway surface is permeable or needs drainage handling.",
            "Confirm whether a dropped kerb or highway approval is also needed.",
            "Use the council route if frontage visibility or access safety is unclear.",
        ),
        "next_step": "Open the driveway guide first, then the dropped-kerb route if the access point is changing.",
        "primary_href": "/driveways/greater-london/barking-and-dagenham/",
    },
}


GSC_2026_06_08_LOCAL_SEARCH_TARGETS = {
    "hmo-article-4-tamworth": {
        "meta_title": "Tamworth HMO Article 4: coverage, change of use and PD checks",
        "meta_description": "Check Tamworth HMO Article 4 coverage, change of use, permitted-development risk and the official local route before relying on an HMO answer.",
        "title": "Answer Article 4 Coverage Before The HMO Route",
        "answer": "This search is not just asking whether HMOs exist in Tamworth. It is asking whether Article 4 removes the simpler route and makes planning permission the safer baseline.",
        "checks": (
            "Check whether the exact property is inside the Article 4 area.",
            "Confirm whether the proposal is a change of use to an HMO.",
            "Treat permitted development as unsafe until the Article 4 and use-class position is verified.",
        ),
        "next_step": "Open the Tamworth HMO guide and the official council source before spending on drawings, valuations or tenancy planning.",
        "primary_href": "/hmos/staffordshire/tamworth/",
    },
    "hmo-article-4-leicestershire": {
        "meta_title": "Leicestershire HMO Article 4: Blaby, Harborough, Oadby and Wigston",
        "meta_description": "Compare Leicestershire HMO Article 4 checks for Blaby, Harborough, Charnwood, Oadby and Wigston before relying on permitted development.",
        "title": "Compare The Councils Before Assuming One HMO Answer",
        "answer": "This Leicestershire query is a comparison problem. Blaby, Harborough, Charnwood, Loughborough and Oadby and Wigston need council-specific Article 4 and change-of-use checks.",
        "checks": (
            "Pick the exact council before relying on county-level wording.",
            "Check Article 4 coverage and local concentration policy for that authority.",
            "Use the local HMO guide once the authority is clear.",
        ),
        "next_step": "Move from the comparison page into the council-specific HMO route that matches the property.",
        "primary_href": "/local-search/hmo-article-4-oadby-and-wigston/",
    },
    "hmo-article-4-stafford": {
        "meta_title": "Stafford HMO Article 4 direction: 2024-2025 planning checks",
        "meta_description": "Check Stafford HMO Article 4 direction wording, 2024-2025 search intent, change-of-use risk and the safest local planning route.",
        "title": "Check The Direction, Date Context And Exact Property",
        "answer": "Stafford HMO searches that mention 2024 or 2025 need current Article 4 direction wording and property-level coverage before a permitted-development assumption is safe.",
        "checks": (
            "Check the latest local Article 4 position rather than an old summary.",
            "Confirm whether the exact HMO proposal is a change-of-use case.",
            "Review local concentration, amenity and parking pressure before relying on the route.",
        ),
        "next_step": "Use the Stafford HMO route first, then verify the official council position if the proposal depends on Article 4 not applying.",
        "primary_href": "/hmos/staffordshire/stafford/",
    },
    "hmo-article-4-milton-keynes": {
        "meta_title": "Milton Keynes HMO Article 4 areas: covered and not covered checks",
        "meta_description": "Check Milton Keynes HMO Article 4 areas, whether a property is covered or not covered, and the planning route before relying on PD.",
        "title": "Settle Covered Or Not Covered First",
        "answer": "For Milton Keynes, the key search intent is whether the property is inside an Article 4 area. That coverage check decides whether the simple HMO route can still be relied on.",
        "checks": (
            "Check the exact Article 4 area or map position.",
            "Confirm the proposed use and whether a change of use is involved.",
            "Keep the council source visible before relying on any broad HMO answer.",
        ),
        "next_step": "Use the local HMO page once the coverage question is settled.",
        "primary_href": "/hmos/buckinghamshire/milton-keynes/",
    },
    "hmo-article-4-west-northamptonshire": {
        "meta_title": "Northampton HMO Article 4: West Northants route checks",
        "meta_description": "Check Northampton and West Northamptonshire HMO Article 4, change of use, council context and whether permitted development is safe.",
        "title": "Keep Northampton And West Northamptonshire Together",
        "answer": "This query needs both the Northampton wording and the West Northamptonshire council route. The decisive point is whether Article 4 or change-of-use policy removes the simple HMO fallback.",
        "checks": (
            "Confirm the exact authority and property position before using a broad Northampton answer.",
            "Check Article 4 coverage and HMO change-of-use risk.",
            "Review local amenity, parking and concentration pressure before relying on permitted development.",
        ),
        "next_step": "Open the West Northamptonshire HMO route, then verify the official council position if the answer depends on coverage.",
        "primary_href": "/hmos/northamptonshire/west-northamptonshire/",
    },
    "hmo-article-4-charnwood": {
        "meta_title": "Charnwood HMO Article 4: Loughborough and Leicestershire checks",
        "meta_description": "Check Charnwood and Loughborough HMO Article 4, permitted-development assumptions and the safest local planning route.",
        "title": "Answer The Loughborough And Charnwood Route Directly",
        "answer": "For Charnwood and Loughborough searches, the useful answer is whether Article 4, HMO concentration or local policy changes the route before a user trusts permitted development.",
        "checks": (
            "Check whether the property is in Charnwood and whether Loughborough wording is the real local intent.",
            "Confirm Article 4 and change-of-use status before relying on the shortcut route.",
            "Use the Leicestershire comparison only when the exact council is still uncertain.",
        ),
        "next_step": "Open the Charnwood HMO guide first, then the Leicestershire comparison if council boundaries are still unclear.",
        "primary_href": "/hmos/leicestershire/charnwood/",
    },
    "hmo-article-4-oadby-and-wigston": {
        "meta_title": "Oadby and Wigston HMO Article 4: planning and PD checks",
        "meta_description": "Check Oadby and Wigston HMO Article 4, change-of-use risk, local concentration and whether permitted development is still safe.",
        "title": "Check Article 4 And Local Concentration First",
        "answer": "For Oadby and Wigston HMO searches, Article 4 and local concentration are the checks most likely to make a simple permitted-development answer unsafe.",
        "checks": (
            "Check the exact property position and Article 4 status.",
            "Review HMO concentration, amenity, parking and refuse arrangements.",
            "Use the local HMO guide before relying on a broad Leicestershire comparison.",
        ),
        "next_step": "Open the Oadby and Wigston HMO page, then verify official council sources if the route is still borderline.",
        "primary_href": "/hmos/leicestershire/oadby-and-wigston/",
    },
    "hmo-article-4-nuneaton-bedworth-warwickshire": {
        "meta_title": "Nuneaton and Warwickshire HMO Article 4: 2024-2025 checks",
        "meta_description": "Check HMO Article 4 intent for Nuneaton, Bedworth and Warwickshire searches before relying on permitted development.",
        "title": "Use The Local HMO Route Before The Wider Warwickshire Context",
        "answer": "Nuneaton, Bedworth and Warwickshire searches mix authority names and date-aware Article 4 intent. The page needs to settle local coverage and change-of-use risk before widening out.",
        "checks": (
            "Check the exact council and whether Nuneaton and Bedworth is the right authority.",
            "Verify Article 4 coverage and any current local direction wording.",
            "Treat Stratford or Daventry wording as a comparison signal, not one shared answer.",
        ),
        "next_step": "Open the Nuneaton and Bedworth HMO guide first, then use broader council context only if the property is elsewhere.",
        "primary_href": "/hmos/warwickshire/nuneaton-and-bedworth/",
    },
    "planning-portal-sheffield": {
        "meta_title": "Sheffield planning portal: official source and permission route",
        "meta_description": "Open the Sheffield planning portal route, official council sources, local project guides and permission checks before relying on a broad search.",
        "title": "Use The Official Portal, Then Pick The Project Route",
        "answer": "A Sheffield planning portal search needs the official source first, then the strongest local project or planning-permission page. Do not leave users in a generic council summary.",
        "checks": (
            "Open the official application or validation source.",
            "Switch to the project guide if the build type is clear.",
            "Use HMO, Article 4 or conservation checks when special controls are the real blocker.",
        ),
        "next_step": "Open official sources, then move into the matching project or local planning-permission page.",
        "primary_href": "/councils/sheffield/",
    },
    "property-extension-folkestone": {
        "meta_title": "Property extensions in Folkestone: planning route and local checks",
        "meta_description": "Check property extension planning in Folkestone and Hythe, including local permission routes, drawings, validation and council checks.",
        "title": "Turn The Property Extension Query Into A Route Check",
        "answer": "For Folkestone property extension searches, the useful answer is whether the extension is still a simple householder route or already needs planning permission and drawings.",
        "checks": (
            "Check extension scale, neighbour relationship and previous additions.",
            "Use local validation and drawing guidance before commissioning the wrong pack.",
            "Move into the project page once the extension type is clear.",
        ),
        "next_step": "Open the local house-extension route, then the council source if drawings or validation are the live issue.",
        "primary_href": "/house-extensions/kent/folkestone-and-hythe/",
    },
}


_GSC_EXPANSION_BY_SLUG = {
    item["slug"]: item
    for item in (
        *GSC_EXPANSION_CANDIDATES_2026_06_08,
        *GSC_CLUSTER_HUBS.values(),
    )
}


def _target_from_expansion_item(item: dict) -> dict:
    if not item:
        return {}
    return {
        "meta_title": item.get("meta_title", ""),
        "meta_description": item.get("meta_description", ""),
        "title": item.get("capsule_title", ""),
        "answer": item.get("capsule_answer", ""),
        "checks": tuple(item.get("capsule_checks") or ()),
        "next_step": item.get("capsule_next_step", ""),
        "primary_href": item.get("next_step_href") or item.get("target_route") or f"/local-search/{item['slug']}/",
        "primary_label": "Open strongest route",
        "cluster": item.get("cluster", ""),
        "hub_slug": item.get("hub_slug", ""),
    }


def gsc_expansion_candidate_for_slug(slug: str) -> dict:
    return _GSC_EXPANSION_BY_SLUG.get(str(slug or "").strip(), {})


def gsc_expansion_candidates_for_family(cluster: str) -> tuple[dict, ...]:
    clean = str(cluster or "").strip()
    return tuple(
        sorted(
            (
                item
                for item in GSC_EXPANSION_CANDIDATES_2026_06_08
                if item.get("cluster") == clean
            ),
            key=lambda item: (int(item.get("priority") or 9999), item["slug"]),
        )
    )


def gsc_cluster_hub_for_family(cluster: str) -> dict:
    return GSC_CLUSTER_HUBS.get(str(cluster or "").strip(), {})


def _normalize_path(path: str) -> str:
    clean = "/" + str(path or "").strip("/")
    if clean != "/":
        clean += "/"
    return clean


def gsc_target_for_path(path: str) -> dict:
    clean = _normalize_path(path)
    target = growth_target_for_path(clean)
    if target:
        return target
    target = GSC_2026_06_08_PAGE_TARGETS.get(clean)
    if target:
        return target
    if clean.startswith("/local-search/"):
        slug = clean.strip("/").split("/")[-1]
        return gsc_target_for_local_search_slug(slug)
    return {}


def gsc_target_for_local_search_slug(slug: str) -> dict:
    clean = str(slug or "").strip()
    target = GSC_2026_06_08_LOCAL_SEARCH_TARGETS.get(clean)
    if target:
        return target
    return _target_from_expansion_item(gsc_expansion_candidate_for_slug(clean))


def gsc_cluster_for_path(path: str) -> str:
    clean = _normalize_path(path)
    target = gsc_target_for_path(clean)
    if target.get("cluster"):
        return str(target["cluster"])
    if clean.startswith("/local-search/"):
        slug = clean.strip("/").split("/")[-1]
        item = gsc_expansion_candidate_for_slug(slug)
        return str(item.get("cluster", ""))
    return ""


def gsc_cluster_hub_for_path(path: str) -> dict:
    return gsc_cluster_hub_for_family(gsc_cluster_for_path(path))


def metadata_override_for_path(path: str) -> tuple[str, str] | None:
    target = gsc_target_for_path(path)
    title = target.get("meta_title")
    description = target.get("meta_description")
    if title and description:
        return title, description
    return None


def metadata_override_for_local_search_slug(slug: str) -> tuple[str, str] | None:
    target = gsc_target_for_local_search_slug(slug)
    title = target.get("meta_title")
    description = target.get("meta_description")
    if title and description:
        return title, description
    return None



CONTROLLED_EXPANSION_GATE = {
    "max_pages": 3000,
    "preferred_range": (1500, 3000),
    "priority_families": (
        "hmos",
        "planning-permission",
        "conservation-areas",
        "dropped-kerbs",
        "porches",
        "driveways",
        "outbuildings",
        "extension-plans",
        "building-regs-bridges",
    ),
    "required_gates": (
        "metadata uniqueness",
        "local-search quality",
        "duplicate and family-repetition review",
        "sitemap count reconciliation",
        "canonical and internal link checks",
    ),
}


def hmo_article_4_priority_for(county_slug: str, town_slug: str) -> dict:
    return HMO_ARTICLE_4_PRIORITY_ROUTES.get((county_slug, town_slug), {})
