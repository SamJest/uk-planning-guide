import json


def build_tool_fallback(title: str, body: str, links: list[dict] | None = None) -> str:
    link_html = ""
    if links:
        cards = []
        for item in links:
            cards.append(
                f"""
<a class="tool-fallback-link" href="{item['href']}">
<strong>{item['title']}</strong>
<span>{item.get('description', 'Open the matching guidance.')}</span>
</a>
"""
            )
        link_html = f"<div class='tool-fallback-links'>{''.join(cards)}</div>"

    return f"""
<div class="tool-fallback" data-tool-fallback="true">
<h3>{title}</h3>
<p>{body}</p>
{link_html}
</div>
"""


def render_inline_tool(
    template: str,
    *,
    config: dict | None = None,
    styles: str = "",
    replacements: dict[str, str] | None = None,
) -> str:
    # Normalize doubled braces in the source template itself. Doing this before
    # we inject shared CSS/HTML replacements avoids corrupting valid `}}`
    # sequences that can appear inside minified style blocks.
    markup = template.replace("{{", "{").replace("}}", "}")
    markup = markup.replace("__STRUCTURED_TOOL_STYLES__", styles)

    if config is not None:
        markup = markup.replace("__CONFIG__", json.dumps(config))

    for key, value in (replacements or {}).items():
        markup = markup.replace(key, value)

    return markup
