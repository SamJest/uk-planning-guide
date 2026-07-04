from pathlib import Path

from components.download_assets import render_download_asset_page, render_download_assets_index
from core.files import write_file
from core.paths import OUTPUT_FOLDER
from core.render import inject_into_base
from data.download_assets import DOWNLOAD_ASSETS, download_asset_path


BASE_URL = "https://ukplanningguide.co.uk"


def generate_download_assets() -> None:
    print("Generating download asset pages")

    index_html = inject_into_base(
        title="Printable Planning Checklists And Worksheets",
        content=render_download_assets_index(),
        options={"breadcrumbs": [("Home", "/"), ("Downloads", "")]},
        canonical_url=f"{BASE_URL}/downloads/",
        meta_description="Free printable planning checklists and worksheets for UK homeowners before applications, drawings, permissions or project spend.",
    )
    write_file(OUTPUT_FOLDER / "downloads", "index.html", index_html)

    for asset in DOWNLOAD_ASSETS:
        path = download_asset_path(asset).strip("/")
        html = inject_into_base(
            title=asset["meta_title"],
            content=render_download_asset_page(asset),
            options={
                "breadcrumbs": [
                    ("Home", "/"),
                    ("Downloads", "/downloads/"),
                    (asset["title"], ""),
                ],
                "structured_data": [
                    {
                        "@context": "https://schema.org",
                        "@type": "DigitalDocument",
                        "name": asset["title"],
                        "description": asset["summary"],
                        "url": f"{BASE_URL}{download_asset_path(asset)}",
                        "dateModified": asset["last_checked"],
                        "audience": asset["audience"],
                        "isAccessibleForFree": True,
                    }
                ],
            },
            canonical_url=f"{BASE_URL}{download_asset_path(asset)}",
            meta_description=asset["meta_description"],
        )
        write_file(OUTPUT_FOLDER / path, "index.html", html)

    print("Download asset pages generated successfully")
