from __future__ import annotations

PROJECT_OWNER_PROJECT_SLUGS = frozenset(
    {
        "hmos",
        "dropped-kerbs",
        "driveways",
        "loft-conversions",
        "garage-conversions",
        "solar-panels",
        "heat-pumps",
        "porches",
        "garden-rooms",
        "outbuildings",
        "house-extensions",
        "rear-extensions",
        "side-extensions",
        "single-storey-extensions",
        "fences-and-walls",
        "windows-and-doors",
        "two-storey-extensions",
        "change-of-use",
    }
)
SCENARIO_OWNER_SCENARIO_SLUGS = frozenset({"conservation-areas"})
AUTHORITY_QUERY_PREFIXES = (
    "planning permission ",
    "permitted development ",
    "domestic alteration plans ",
)


def _query_text(page: dict) -> str:
    return str(page.get("query", "")).strip().lower()


def _authority_label(page: dict) -> str:
    return str(page.get("authority_slug", "")).replace("-", " ").title()


def _query_has_marker(query: str, marker: str) -> bool:
    normalized_query = f" {query.replace('-', ' ')} "
    normalized_marker = f" {marker.replace('-', ' ')} "
    return normalized_marker in normalized_query


def local_search_is_broad_authority_query(page: dict) -> bool:
    query = _query_text(page)
    slug = str(page.get("slug", "")).strip().lower()
    return (
        slug.startswith(("planning-permission-", "permitted-development-", "planning-", "planning-portal-", "domestic-alteration-plans-"))
        or query.startswith(AUTHORITY_QUERY_PREFIXES)
        or query.endswith(" planning")
    )


def local_search_owner(page: dict) -> str:
    scenario_slug = str(page.get("scenario_slug", "")).lower()
    project_slug = str(page.get("project_slug", "")).lower()
    query = _query_text(page)

    if scenario_slug in SCENARIO_OWNER_SCENARIO_SLUGS:
        return "scenario"
    if project_slug == "hmos" and "article 4" in query:
        return "project"
    if project_slug in PROJECT_OWNER_PROJECT_SLUGS and any(
        _query_has_marker(query, marker)
        for marker in (
            "extension",
            "extensions",
            "alteration",
            "alteration plans",
            "dropped kerb",
            "loft",
            "garage",
            "porch",
            "garden room",
            "outbuilding",
            "fence",
            "wall",
        )
    ):
        return "project"
    if local_search_is_broad_authority_query(page):
        return "authority"
    if project_slug in PROJECT_OWNER_PROJECT_SLUGS:
        return "project"
    return "authority"


def local_search_topic_phrase(page: dict, authority_label: str | None = None) -> str:
    authority = authority_label or _authority_label(page)
    query = _query_text(page)
    scenario_slug = str(page.get("scenario_slug", "")).lower()
    project_slug = str(page.get("project_slug", "")).lower()

    if project_slug == "hmos" and "article 4" in query:
        connector = "across" if page.get("target_scope") == "county" else "in"
        return f"HMO and Article 4 in {authority}" if connector == "in" else f"HMO and Article 4 across {authority}"
    if scenario_slug == "conservation-areas":
        return f"conservation area rules in {authority}"
    if scenario_slug == "article-4":
        return f"Article 4 rules in {authority}"
    if scenario_slug == "permitted-development":
        return f"permitted development in {authority}"
    if "industrial alteration" in query:
        return f"industrial alteration plans in {authority}"
    if "domestic alteration" in query:
        return f"domestic alteration plans in {authority}"
    if project_slug == "loft-conversions":
        return f"loft conversions in {authority}"
    if project_slug == "garage-conversions":
        return f"garage conversions in {authority}"
    if project_slug == "solar-panels":
        return f"solar panels in {authority}"
    if project_slug == "heat-pumps":
        return f"heat pumps in {authority}"
    if project_slug == "porches":
        return f"porch planning in {authority}"
    if project_slug == "garden-rooms":
        return f"garden rooms in {authority}"
    if project_slug == "outbuildings":
        return f"outbuildings in {authority}"
    if project_slug == "fences-and-walls":
        return f"fences and walls in {authority}"
    if project_slug == "windows-and-doors":
        return f"windows and doors in {authority}"
    if project_slug == "dropped-kerbs":
        return f"dropped kerbs in {authority}"
    if project_slug == "driveways":
        return f"driveway planning in {authority}"
    if project_slug == "two-storey-extensions":
        return f"two storey extensions in {authority}"
    if project_slug == "house-extensions":
        return f"house extensions in {authority}"
    if project_slug == "rear-extensions":
        return f"rear extensions in {authority}"
    if project_slug == "side-extensions":
        return f"side extensions in {authority}"
    if project_slug == "single-storey-extensions":
        return f"single storey extensions in {authority}"
    if project_slug == "change-of-use":
        return f"change of use in {authority}"
    if query.startswith("planning permission ") or query.endswith(" planning"):
        return f"planning permission in {authority}"
    return f"the local planning route in {authority}"


def local_search_focus_signal(page: dict, authority_label: str | None = None) -> str:
    authority = authority_label or _authority_label(page)
    query = _query_text(page)
    scenario_slug = str(page.get("scenario_slug", "")).lower()
    project_slug = str(page.get("project_slug", "")).lower()

    if project_slug == "hmos" and "article 4" in query:
        return (
            f"In {authority}, the live issue is usually whether Article 4 has removed the simpler HMO route "
            "and forced the project back into a fuller change-of-use decision."
        )
    if scenario_slug == "conservation-areas":
        return (
            f"In {authority}, conservation-area answers become more cautious when visibility, materials, demolition "
            "risk or harm to character stop the proposal looking routine."
        )
    if scenario_slug == "article-4":
        return (
            f"In {authority}, Article 4 questions are really about whether the direction bites on this exact property "
            "and proposal, not whether Article 4 exists somewhere in the wider authority."
        )
    if scenario_slug == "permitted-development":
        return (
            f"In {authority}, permitted development only stays dependable when the site history, local designations "
            "and measured design all support the same answer."
        )
    if query.startswith("planning permission ") or query.endswith(" planning"):
        return (
            f"In {authority}, broad planning searches usually stop being broad once the proposal is measured against "
            "restrictions, site history and the actual design rather than the headline idea."
        )
    if project_slug == "loft-conversions":
        return (
            f"In {authority}, loft conversions stay on the easier route only while roof shape, added volume and street "
            "visibility still read as subordinate to the existing house."
        )
    if project_slug == "garage-conversions":
        return (
            f"In {authority}, garage conversions usually become harder when parking loss, frontage treatment or highway "
            "issues matter more than the internal building work itself."
        )
    if project_slug == "solar-panels":
        return (
            f"In {authority}, solar-panel proposals are usually straightforward only while the panels stay visually "
            "subordinate and heritage controls are not the real issue."
        )
    if project_slug == "heat-pumps":
        return (
            f"In {authority}, heat-pump answers tighten up when siting, noise and neighbour impact are weakly explained "
            "or local restrictions add another layer of sensitivity."
        )
    if project_slug == "porches":
        return (
            f"In {authority}, porch proposals stay simpler when footprint, height and the relationship to a highway or "
            "boundary keep the scheme comfortably within the smaller householder route."
        )
    if project_slug == "garden-rooms":
        return (
            f"In {authority}, garden-room questions usually turn on whether the height, siting and intended use still "
            "read as genuinely incidental to the main house."
        )
    if project_slug == "outbuildings":
        return (
            f"In {authority}, outbuildings remain the easier case only while height, siting and use still read as "
            "secondary to the house rather than a separate living space."
        )
    if project_slug == "fences-and-walls":
        return (
            f"In {authority}, fence and wall proposals stop being routine when highway-side height or ground-level "
            "changes push the visible structure past the usual limits."
        )
    if project_slug == "windows-and-doors":
        return (
            f"In {authority}, window and door changes usually stay simple only if the property is not listed and local "
            "design controls do not make visible alterations materially more sensitive."
        )
    if project_slug == "dropped-kerbs":
        return (
            f"In {authority}, dropped-kerb answers often depend as much on highway approval, frontage visibility and "
            "drainage as on planning permission itself."
        )
    if project_slug == "driveways":
        return (
            f"In {authority}, driveway searches usually need a tighter answer on drainage, frontage treatment and "
            "whether the real route also includes a dropped kerb or other highway approval."
        )
    if project_slug == "two-storey-extensions":
        return (
            f"In {authority}, two-storey extensions usually become the formal-route case once depth, height and "
            "neighbour impact stop looking routine against the existing house."
        )
    return f"In {authority}, the local planning route usually changes once the exact site, restrictions and design details are checked together."


def local_search_entry_lead(page: dict, authority_label: str) -> str:
    scope_label = "county" if page.get("target_scope") == "county" else "council"
    topic_phrase = local_search_topic_phrase(page, authority_label)

    if local_search_owner(page) == "authority":
        if local_search_is_broad_authority_query(page):
            return f"Check planning permission in {authority_label} against the council route and matching project page."
        return f"Check the local planning route in {authority_label} against the strongest {scope_label} or project page."
    return f"Check {topic_phrase} against the best matching project or local-rule page."


def local_search_next_step_phrase(page: dict) -> str:
    return {
        "authority": "Use the authority guide, then the matching project check.",
        "scenario": "Use the topic page, then check the authority or project context.",
        "project": "Use the project guide first, then the authority or topic check.",
    }[local_search_owner(page)]


def local_search_authority_href(page: dict) -> str:
    if page["target_scope"] == "county":
        return f"/{page['authority_slug']}/"
    return f"/councils/{page['authority_slug']}/"


def local_search_project_href(page: dict) -> str | None:
    project_slug = page.get("project_slug")
    if not project_slug:
        return None

    if page.get("project_scope") == "county":
        return f"/{project_slug}/{page['county_slug']}/"

    council_slug = page.get("council_slug") or page["authority_slug"]
    return f"/{project_slug}/{page['county_slug']}/{council_slug}/"


def local_search_scenario_href(page: dict) -> str | None:
    scenario_slug = page.get("scenario_slug")
    if not scenario_slug:
        return None

    authority_slug = page.get("scenario_authority_slug")
    if authority_slug:
        return f"/{scenario_slug}/{authority_slug}/"

    return f"/{scenario_slug}/"
