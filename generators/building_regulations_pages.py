from __future__ import annotations

from pathlib import Path

from components.building_regulations_pages import build_building_regulations_content
from core.files import write_file
from core.paths import OUTPUT_FOLDER
from core.render import inject_into_base
from data.building_regulations_pages import (
    BUILDING_REGULATIONS_PAGES,
    building_regulations_path,
)


BASE_URL = "https://ukplanningguide.co.uk"


def _folder_for_page(page: dict) -> Path:
    slug = str(page.get("slug", "")).strip()
    root = OUTPUT_FOLDER / "building-regulations"
    if slug == "index":
        return root
    return root / slug


def generate_building_regulations_pages() -> None:
    print("Generating building regulations pages")

    for page in BUILDING_REGULATIONS_PAGES:
        route = building_regulations_path(page)
        breadcrumbs = [("Home", "/"), ("Building Regulations", "/building-regulations/")]
        if page["slug"] != "index":
            breadcrumbs.append((page["title"], ""))
        else:
            breadcrumbs[-1] = ("Building Regulations", "")

        html = inject_into_base(
            title=page["meta_title"],
            content=build_building_regulations_content(page),
            options={"breadcrumbs": breadcrumbs},
            canonical_url=f"{BASE_URL}{route}",
            meta_description=page["meta_description"],
        )
        write_file(_folder_for_page(page), "index.html", html)

    print("Building regulations pages generated successfully")


if __name__ == "__main__":
    generate_building_regulations_pages()
