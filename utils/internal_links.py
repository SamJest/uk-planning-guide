from data.loaders import load_councils, load_projects
from data.promoted_links import PROMOTED_LINKS
from data.scenario_data import SCENARIO_LOOKUP
from utils.live_links import filter_live_pairs
from utils.project_scenario_config import project_scenario_href


MAX_PROJECT_LINKS = 4
MAX_NEARBY_LINKS = 8
MAX_TOPIC_LINKS = 4
MAX_CROSS_COUNTY_LINKS = 6

PROJECTS = load_projects()
PROJECTS_BY_SLUG = {project["slug"]: project for project in PROJECTS}
COUNCILS_BY_COUNTY = load_councils()

PROJECT_GROUPS = {}
for project in PROJECTS:
    PROJECT_GROUPS.setdefault(project["type"], []).append(project)

for group in PROJECT_GROUPS.values():
    group.sort(key=lambda item: item["slug"])

PROJECT_TYPE_SCENARIOS = {
    "extension": ["planning-permission", "permitted-development", "height-limits", "boundary-rules"],
    "loft": ["permitted-development", "planning-permission", "height-limits", "conservation-areas"],
    "outbuilding": ["permitted-development", "boundary-rules", "height-limits", "planning-permission"],
    "conversion": ["planning-permission", "permitted-development", "boundary-rules", "conservation-areas"],
    "external": ["planning-permission", "boundary-rules", "height-limits", "conservation-areas"],
    "microgeneration": ["planning-permission", "permitted-development", "conservation-areas", "height-limits"],
    "change-of-use": ["planning-permission", "conservation-areas", "permitted-development", "boundary-rules"],
    "agricultural": ["planning-permission", "height-limits", "boundary-rules", "conservation-areas"],
    "temporary": ["planning-permission", "boundary-rules", "height-limits", "conservation-areas"],
    "demolition": ["planning-permission", "conservation-areas", "boundary-rules", "height-limits"],
}

SCENARIO_NEIGHBOURS = {
    "planning-permission": ["permitted-development", "height-limits", "boundary-rules", "conservation-areas"],
    "permitted-development": ["planning-permission", "height-limits", "boundary-rules", "conservation-areas"],
    "height-limits": ["boundary-rules", "planning-permission", "permitted-development", "conservation-areas"],
    "boundary-rules": ["height-limits", "planning-permission", "permitted-development", "conservation-areas"],
    "conservation-areas": ["planning-permission", "permitted-development", "boundary-rules", "height-limits"],
}


def _seed_value(*parts) -> int:
    return sum(ord(char) for part in parts for char in str(part))


def _rotate(items, *seed_parts):
    if not items:
        return []

    ordered = list(items)
    offset = _seed_value(*seed_parts) % len(ordered)
    return ordered[offset:] + ordered[:offset]


def generate_anchor(project_title, area_name):
    templates = [
        "Do you need planning permission for {project} in {area}?",
        "{project} planning rules in {area}",
        "{project} guide for {area}",
        "{project} local checks in {area}",
    ]
    template = templates[_seed_value(project_title, area_name) % len(templates)]
    return template.format(project=project_title, area=area_name)


def unique_links(links):
    seen = set()
    output = []

    for href, text in links:
        if href not in seen:
            seen.add(href)
            output.append((href, text))

    return output


def _consume_unique_links(links, seen_hrefs=None):
    if seen_hrefs is None:
        seen_hrefs = set()
    output = filter_live_pairs(unique_links(links), exclude=seen_hrefs)
    seen_hrefs.update(href for href, _ in output)
    return output


def _project_type(project_slug):
    return PROJECTS_BY_SLUG.get(project_slug, {}).get("type", "")


def _area_name(area_slug):
    return area_slug.replace("-", " ").title()


def _topic_slugs(project_slug, scenario_slug=None):
    project_type = _project_type(project_slug)
    ordered = []

    if scenario_slug:
        ordered.extend(SCENARIO_NEIGHBOURS.get(scenario_slug, []))

    ordered.extend(PROJECT_TYPE_SCENARIOS.get(project_type, PROJECT_TYPE_SCENARIOS["extension"]))

    deduped = []
    seen = {scenario_slug} if scenario_slug else set()
    for slug in ordered:
        if slug in seen or slug not in SCENARIO_LOOKUP:
            continue
        seen.add(slug)
        deduped.append(slug)

    return deduped[:MAX_TOPIC_LINKS]


def _render_topic_links(project_slug, county_slug, town_slug, scenario_slug=None, seen_hrefs=None):
    project = PROJECTS_BY_SLUG.get(project_slug, {})
    project_name = project.get("short_name", project.get("title", "this project"))
    area_name = town_slug.replace("-", " ").title() if town_slug else ""
    current_scenario = SCENARIO_LOOKUP.get(scenario_slug, {})
    links = []

    for slug in _topic_slugs(project_slug, scenario_slug):
        if county_slug and town_slug:
            href = project_scenario_href(project_slug, county_slug, town_slug, slug) or f"/{slug}/{town_slug}/"
        else:
            href = f"/{slug}/"
        links.append((href, SCENARIO_LOOKUP[slug]["title"]))

    links = _consume_unique_links(links, seen_hrefs)
    if not links:
        return ""

    html = "".join(f'<a href="{href}">{title}</a>' for href, title in links)
    if scenario_slug and current_scenario:
        heading = f"What to Check Next for {project_name} in {area_name}"
        intro = (
            f"If {current_scenario['seo_angle']} is the current blocker, these are the next rules "
            "most likely to change the answer."
        )
    elif area_name:
        heading = f"What to Check Next for {project_name} in {area_name}"
        intro = (
            "These are usually the next same-project rule checks worth opening before you jump out to a broader rule hub."
        )
    else:
        heading = "What to Check Next"
        intro = "These are usually the next planning checks worth opening before you rely on the first answer."

    return f"""
<div class="card">
<div class="card-kicker">People also check</div>
<h2>{heading}</h2>
<p>{intro}</p>
<div class="link-grid">
{html}
</div>
</div>
"""


def _render_related_projects(project_slug, county_slug, town_slug, area_name, seen_hrefs=None):
    project = PROJECTS_BY_SLUG.get(project_slug, {})
    project_type = project.get("type")
    related = [item for item in PROJECT_GROUPS.get(project_type, []) if item["slug"] != project_slug]
    related = _rotate(related, project_slug, county_slug, town_slug)

    links = []
    for item in related[:MAX_PROJECT_LINKS]:
        href = f"/{item['slug']}/{county_slug}/{town_slug}/"
        links.append((href, generate_anchor(item["short_name"], area_name)))

    links = _consume_unique_links(links, seen_hrefs)
    if not links:
        return ""

    html = "".join(f'<a href="{href}">{text}</a>' for href, text in links)
    return f"""
<div class="card">
<div class="card-kicker">Related projects</div>
<h2>People Also Check Similar Project Types</h2>
<div class="link-grid">
{html}
</div>
</div>
"""


def _render_hierarchy_links(project_slug, county_slug, town_slug, area_name, seen_hrefs=None):
    project = PROJECTS_BY_SLUG.get(project_slug, {})
    project_name = project.get("short_name", project.get("title", "this project"))
    county_name = _area_name(county_slug) if county_slug else "this area"
    links = [
        (f"/{project_slug}/", f"{project_name} planning guide"),
        (f"/{project_slug}/{county_slug}/", f"{project_name} across {county_name}" if county_slug else "Area comparison"),
        (f"/councils/{town_slug}/", f"{area_name} planning authority guide" if town_slug else "Local authority guide"),
        (f"/{county_slug}/", f"{county_name} planning area guide" if county_slug else "Browse planning areas"),
    ]
    filtered = _consume_unique_links(links, seen_hrefs)
    if not filtered:
        return ""
    html = "".join(f'<a href="{href}">{text}</a>' for href, text in filtered)
    return f"""
<div class="card">
<div class="card-kicker">Broader and narrower pages</div>
<h2>Move Up Or Down The Planning Hierarchy</h2>
<div class="link-grid">
{html}
</div>
</div>
"""


def _render_same_project_area_links(project_slug, county_slug, town_slug, seen_hrefs=None):
    project = PROJECTS_BY_SLUG.get(project_slug, {})
    project_name = project.get("short_name", project.get("title", "this project"))
    county_slugs = [slug for slug in sorted(COUNCILS_BY_COUNTY.keys()) if slug != county_slug]
    county_slugs = _rotate(county_slugs, project_slug, county_slug, town_slug)

    links = []
    for slug in county_slugs[:MAX_CROSS_COUNTY_LINKS]:
        links.append((f"/{project_slug}/{slug}/", f"{project_name} across {_area_name(slug)}"))

    filtered = _consume_unique_links(links, seen_hrefs)
    if not filtered:
        return ""

    html = "".join(f'<a href="{href}">{text}</a>' for href, text in filtered)
    return f"""
<div class="card">
<div class="card-kicker">Same project elsewhere</div>
<h2>Compare This Project Across Other Planning Areas</h2>
<div class="link-grid">
{html}
</div>
</div>
"""


def _render_next_step_links(project_slug, county_slug, town_slug, area_name, seen_hrefs=None):
    explorer_tool = PROMOTED_LINKS["what_can_i_build_explorer"]
    planning_tool = PROMOTED_LINKS["planning_decision_tool"]
    risk_tool = PROMOTED_LINKS["planning_rejection_risk_tool"]
    route_tool = PROMOTED_LINKS["planning_route_planner"]
    requirements_tool = PROMOTED_LINKS["project_requirements_generator"]
    value_tool = PROMOTED_LINKS["extension_value_estimator"]
    faq = PROMOTED_LINKS["faq_need_planning"]
    council_href = f"/councils/{town_slug}/" if town_slug else "/councils/"
    county_href = f"/{project_slug}/{county_slug}/" if county_slug else "/councils/"
    project_name = PROJECTS_BY_SLUG.get(project_slug, {}).get("short_name", "this project")

    links = [
        (planning_tool["href"], f"Run a first-pass planning check for {project_name.lower()}"),
        (route_tool["href"], "Map the most likely approval route before preparing the wrong path"),
        (requirements_tool["href"], "Build a practical prep pack for the checks and documents most likely to matter"),
        (council_href, f"See the wider {area_name} authority context" if area_name else "Browse local authorities"),
        (county_href, f"Compare {project_name.lower()} across the county" if county_slug else "Browse county comparisons"),
        (risk_tool["href"], "Check the likely refusal risks if the design is already taking shape"),
        (faq["href"], "Read the core planning permission answer"),
        (explorer_tool["href"], "Switch to the explorer if the project type is still uncertain"),
    ]
    if _project_type(project_slug) in {"extension", "loft"}:
        links.insert(1, (value_tool["href"], f"Estimate the likely value uplift for {project_name.lower()}"))

    filtered = _consume_unique_links(links, seen_hrefs)
    if not filtered:
        return ""
    html = "".join(f'<a href="{href}">{text}</a>' for href, text in filtered)
    return f"""
<div class="card">
<div class="card-kicker">Next steps</div>
<h2>Useful Next Moves If The Answer Still Feels Borderline</h2>
<p>These links are ordered to help you act on the result rather than wander into another generic index.</p>
<div class="link-grid">
{html}
</div>
</div>
"""


def build_internal_links(*args, **kwargs):
    scenario_slug = kwargs.get("scenario_slug")
    seen_hrefs: set[str] = set()

    if len(args) == 4 and isinstance(args[0], dict):
        project, town, all_projects, all_towns = args

        project_slug = project["slug"]
        project_title = project["short_name"]
        county_slug = town["county_slug"]
        town_slug = town["town_slug"]
        town_name = town["town_name"]

        same_type = [
            item for item in PROJECT_GROUPS.get(project.get("type"), [])
            if item["slug"] != project_slug
        ]
        other_projects = [
            item for item in sorted(all_projects, key=lambda item: item["slug"])
            if item["slug"] != project_slug and item["slug"] not in {entry["slug"] for entry in same_type}
        ]
        related_projects = _rotate(same_type + other_projects, project_slug, county_slug, town_slug)

        project_links = []
        for item in related_projects[:MAX_PROJECT_LINKS]:
            href = f"/{item['slug']}/{county_slug}/{town_slug}/"
            text = generate_anchor(item["short_name"], town_name)
            project_links.append((href, text))

        nearby = sorted(
            [item for item in all_towns if item["town_slug"] != town_slug],
            key=lambda item: (item["county_slug"], item["town_slug"]),
        )
        nearby = _rotate(nearby, town_slug, county_slug, project_slug)

        town_links = []
        for item in nearby[:MAX_NEARBY_LINKS]:
            href = f"/{project_slug}/{item['county_slug']}/{item['town_slug']}/"
            text = generate_anchor(project_title, item["town_name"])
            town_links.append((href, text))

        project_links = _consume_unique_links(project_links, seen_hrefs)
        project_html = "".join(
            f'<a href="{href}">{text}</a>'
            for href, text in project_links
        )
        project_section = ""
        if project_html:
            project_section = f"""
<div class="card">
<div class="card-kicker">Related projects</div>
<h2>Related Project Guides</h2>
<div class="link-grid">
{project_html}
</div>
</div>
"""

        town_links = _consume_unique_links(town_links, seen_hrefs)
        town_html = "".join(
            f'<a href="{href}">{text}</a>'
            for href, text in town_links
        )
        town_section = ""
        if town_html:
            town_section = f"""
<div class="card">
<div class="card-kicker">Compare by area</div>
<h2>Compare Nearby Areas</h2>
<div class="link-grid">
{town_html}
</div>
</div>
"""

        topic_section = _render_topic_links(project_slug, "", "", scenario_slug=None, seen_hrefs=seen_hrefs)
        area_section = _render_same_project_area_links(project_slug, county_slug, town_slug, seen_hrefs=seen_hrefs)
        return topic_section + project_section + town_section + area_section + _render_next_step_links(project_slug, county_slug, town_slug, town_name, seen_hrefs=seen_hrefs)

    if len(args) == 3:
        project_slug, county_slug, town_slug = args
        area_name = town_slug.replace("-", " ").title()
        return (
            _render_topic_links(project_slug, county_slug, town_slug, scenario_slug=scenario_slug, seen_hrefs=seen_hrefs)
            + _render_related_projects(project_slug, county_slug, town_slug, area_name, seen_hrefs=seen_hrefs)
            + _render_hierarchy_links(project_slug, county_slug, town_slug, area_name, seen_hrefs=seen_hrefs)
            + _render_same_project_area_links(project_slug, county_slug, town_slug, seen_hrefs=seen_hrefs)
            + _render_next_step_links(project_slug, county_slug, town_slug, area_name, seen_hrefs=seen_hrefs)
        )

    return ""


def build_cluster_links(project, town, all_projects, all_towns):
    project_slug = project["slug"]
    project_title = project["short_name"]
    county_slug = town["county_slug"]
    town_slug = town["town_slug"]
    town_name = town["town_name"]

    cluster_areas = sorted(all_towns, key=lambda item: (item["county_slug"], item["town_slug"]))
    cluster_areas = _rotate(cluster_areas, project_slug, county_slug, town_slug)

    area_links = "".join(
        f'<a href="/{project_slug}/{item["county_slug"]}/{item["town_slug"]}/">{generate_anchor(project_title, item["town_name"])}</a>'
        for item in cluster_areas[: MAX_PROJECT_LINKS + 1]
        if item["town_slug"] != town_slug
    )

    area_section = f"""
<div class="card">
<h2>{project_title} Across Nearby Areas</h2>
<div class="link-grid">
{area_links}
</div>
</div>
"""

    same_type = [
        item for item in PROJECT_GROUPS.get(project.get("type"), [])
        if item["slug"] != project_slug
    ]
    other_projects = [
        item for item in sorted(all_projects, key=lambda item: item["slug"])
        if item["slug"] != project_slug and item["slug"] not in {entry["slug"] for entry in same_type}
    ]
    cluster_projects = _rotate(same_type + other_projects, town_slug, county_slug, project_slug)

    project_links = "".join(
        f'<a href="/{item["slug"]}/{county_slug}/{town_slug}/">{generate_anchor(item["short_name"], town_name)}</a>'
        for item in cluster_projects[: MAX_PROJECT_LINKS + 1]
    )

    project_section = f"""
<div class="card">
<h2>Planning Projects in {town_name}</h2>
<div class="link-grid">
{project_links}
</div>
</div>
"""

    return area_section + project_section


def build_nearby_links(project_slug, county_slug, town_slug, councils_by_county):
    links = []
    project_name = PROJECTS_BY_SLUG.get(project_slug, {}).get("short_name", "This project")
    councils = sorted(
        councils_by_county.get(county_slug, []),
        key=lambda item: item.get("town_slug") or item.get("slug") or "",
    )

    for council in councils:
        slug = council.get("town_slug") or council.get("slug")
        name = council.get("town_name") or council.get("name")

        if not slug or not name or slug == town_slug:
            continue

        links.append(
            f'<a href="/{project_slug}/{county_slug}/{slug}/">{project_name} in {name}</a>'
        )

        if len(links) >= MAX_NEARBY_LINKS:
            break

    return "".join(links)
