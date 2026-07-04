from __future__ import annotations

from pathlib import Path

from components.faq_pages import build_faq_index_content, build_faq_page_content
from components.seo import build_faq_index_metadata, build_faq_metadata
from core.files import write_file
from core.paths import OUTPUT_FOLDER
from core.render import inject_into_base
from data.faq_data import FAQS


BASE_URL = "https://ukplanningguide.co.uk"
OUTPUT_DIR = OUTPUT_FOLDER


def generate_faq_pages():
    faq_root = OUTPUT_DIR / "planning-faq"
    faq_root.mkdir(parents=True, exist_ok=True)

    for faq in FAQS:
        page_content = build_faq_page_content(faq)
        title, description = build_faq_metadata(faq)
        html = inject_into_base(
            title=title,
            content=page_content,
            options={"breadcrumbs": [("Home", "/"), ("Planning FAQ", "/planning-faq/"), (faq["title"], "")]},
            canonical_url=f"{BASE_URL}/planning-faq/{faq['slug']}/",
            meta_description=description,
        )
        write_file(faq_root / faq["slug"], "index.html", html)
    title, description = build_faq_index_metadata()

    faq_index_html = inject_into_base(
        title=title,
        content=build_faq_index_content(FAQS),
        options={"breadcrumbs": [("Home", "/"), ("Planning FAQ", "")]},
        canonical_url=f"{BASE_URL}/planning-faq/",
        meta_description=description,
    )
    write_file(faq_root, "index.html", faq_index_html)


if __name__ == "__main__":
    generate_faq_pages()
    print("FAQ pages generated successfully.")
