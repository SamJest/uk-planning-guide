from components.county_sections import (
    build_county_decision_guide,
    build_county_decision_summary,
    build_county_jump_links,
    build_county_jurisdiction_notice,
    build_county_start_here_section,
    build_county_topic_links,
    build_trust_section,
    slug_to_name,
)
from components.seo import build_county_metadata
from core.files import write_file
from core.paths import BASE_URL, FORCE_REBUILD, OUTPUT_FOLDER
from core.render import inject_into_base
from data.loaders import load_councils, load_projects
from utils.county_config import load_scenarios
from utils.random_tools import get_month_year, page_rng


def generate_county_pages():
    print("Starting county page generation")

    projects = load_projects()
    councils_by_county = load_councils()
    county_slugs = list(councils_by_county.keys())
    scenarios = load_scenarios()

    for county_slug, councils in councils_by_county.items():
        county_name = slug_to_name(county_slug)
        page_rng("county", county_slug, "county")

        county_folder = OUTPUT_FOLDER / county_slug
        county_folder.mkdir(parents=True, exist_ok=True)
        file_path = county_folder / "index.html"

        if file_path.exists() and not FORCE_REBUILD:
            continue

        hero = f"""
<section class="hero">
<span class="badge">Area Planning Guidance</span>
<h1>Planning Permission In {county_name}</h1>
<p>Use this area hub when the search is really about planning permission in {county_name} and the next step depends on choosing the right council, project guide or planning topic first. It is built to turn a broad county-level query into the local route most likely to answer it properly.</p>
</section>
"""

        project_cards = "".join(
            f"""
<a class="card project-card" href="/{project['slug']}/{county_slug}/">
<div class="card-kicker">Area project hub</div>
<h3>{project['title']}</h3>
<p>Compare {project['short_name'].lower()} guidance across the councils in {county_name}.</p>
<span class="cta">Compare this project</span>
</a>
"""
            for project in projects
        )

        project_block = f"""
<section class="project-block" id="county-projects">
<h2>Project Guides People Usually Need First</h2>
<div class="card-grid">{project_cards}</div>
</section>
"""

        council_cards = "".join(
            f"""
<a class="card council-card" href="/councils/{council['town_slug']}/">
<div class="card-kicker">Local authority page</div>
<h3>{council['town_name']}</h3>
<p>Open the council guide, local restriction context and priority project checks.</p>
<span class="cta">View council guide</span>
</a>
"""
            for council in councils
        )

        council_block = f"""
<section class="council-cards" id="county-councils">
<h2>Choose the Right Local Planning Authority</h2>
<div class="card-grid">{council_cards}</div>
</section>
"""

        nearby_cards = []
        for other_county_slug in county_slugs:
            if other_county_slug == county_slug:
                continue

            nearby_cards.append(
                f"""
<a class="card county-card" href="/{other_county_slug}/">
<div class="card-kicker">Area comparison</div>
<h3>{slug_to_name(other_county_slug)}</h3>
<p>Compare nearby planning-area guidance when the local layer is still uncertain.</p>
<span class="cta">Compare area</span>
</a>
"""
            )

            if len(nearby_cards) >= 6:
                break

        nearby_counties = f"""
<section class="nearby-counties">
<h2>Nearby Planning Areas</h2>
<div class="card-grid">{''.join(nearby_cards)}</div>
</section>
"""

        content = "\n".join(
            [
                hero,
                build_county_jurisdiction_notice(county_slug, county_name),
                build_county_jump_links(county_name),
                build_county_decision_summary(county_name, len(councils)),
                build_county_start_here_section(county_slug, county_name, councils),
                build_county_decision_guide(county_name, len(councils)),
                project_block,
                build_county_topic_links(county_slug, scenarios),
                council_block,
                nearby_counties,
                build_trust_section("Planning Permission", county_name, "County"),
                f"<div class='last-updated'>Updated {get_month_year()}</div>",
            ]
        )
        title, description = build_county_metadata(county_name, len(councils), county_slug)

        html = inject_into_base(
            title=title,
            content=content,
            options={"breadcrumbs": [("Home", "/"), (county_name, f"/{county_slug}/")]},
            canonical_url=f"{BASE_URL}/{county_slug}/",
            meta_description=description,
        )

        write_file(county_folder, "index.html", html)

    print("County pages generated successfully")
