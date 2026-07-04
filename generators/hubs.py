from pathlib import Path

from components.hub_sections import build_councils_hub_content, build_project_hub_content
from components.seo import build_councils_hub_metadata, build_project_hub_metadata
from core.files import write_file
from core.paths import OUTPUT_FOLDER
from core.render import inject_into_base
from utils.location_utils import build_master_town_index


BASE_URL = "https://ukplanningguide.co.uk"


def generate_councils_hub(councils_by_county):
    towns = build_master_town_index(councils_by_county)
    content = build_councils_hub_content(councils_by_county, towns)
    title, description = build_councils_hub_metadata(len(councils_by_county))

    html = inject_into_base(
        title=title,
        content=content,
        options={"breadcrumbs": [("Home", "/"), ("Councils", "/councils/")]},
        canonical_url=f"{BASE_URL}/councils/",
        meta_description=description,
    )

    folder = OUTPUT_FOLDER / "councils"
    folder.mkdir(parents=True, exist_ok=True)
    write_file(folder, "index.html", html)


def generate_project_hubs(projects, councils_by_county):
    towns = build_master_town_index(councils_by_county)

    for project in projects:
        content = build_project_hub_content(project, councils_by_county, towns)
        title, description = build_project_hub_metadata(project)

        html = inject_into_base(
            title=title,
            content=content,
            options={"breadcrumbs": [("Home", "/"), (project["title"], f"/{project['slug']}/")]},
            canonical_url=f"{BASE_URL}/{project['slug']}/",
            meta_description=description,
        )

        folder = OUTPUT_FOLDER / project["slug"]
        folder.mkdir(parents=True, exist_ok=True)
        write_file(folder, "index.html", html)
