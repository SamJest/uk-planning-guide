from components.sitemap_builders import *


def generate_sitemaps():

    print("Generating sitemap structure")

    urls = collect_urls()

    validate_sitemap_urls(urls)

    grouped_urls = group_urls_by_section(urls)

    sitemap_files = generate_section_sitemaps(grouped_urls)

    generate_sitemap_index(sitemap_files)

    update_robots()

    print("Sitemaps generated successfully")