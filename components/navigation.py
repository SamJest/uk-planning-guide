def build_navigation(data, generated_pages):
    nav = []

    for topic in data.get("topics", []):
        slug = topic.get("slug")

        if not slug:
            continue

        url = f"{slug}/"

        if url in generated_pages:
            nav.append({
                "name": topic.get("name", slug.replace("-", " ").title()),
                "url": url
            })

    return nav


def render_navigation(nav):
    html = ""

    for item in nav:
        html += f'<a href="{item["url"]}">{item["name"]}</a>\n'

    return html