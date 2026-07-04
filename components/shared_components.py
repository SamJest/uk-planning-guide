from pathlib import Path


COMPONENTS_DIR = Path(__file__).resolve().parent

def _read_component(filename: str) -> str:
    return (COMPONENTS_DIR / filename).read_text(encoding="utf-8")


def _replace_tokens(template: str, replacements: dict[str, str]) -> str:
    markup = template
    for key, value in replacements.items():
        markup = markup.replace(f"{{{{{key}}}}}", value)
    return markup


def render_result_capture(capture_id: str = "result-capture-email") -> str:
    return _replace_tokens(
        _read_component("result_capture.html"),
        {
            "capture_id": capture_id,
        },
    )


def build_conversion_band(
    title: str,
    description: str,
    primary_href: str,
    primary_title: str,
    primary_description: str,
    primary_cta: str,
    secondary_href: str,
    secondary_title: str,
    secondary_description: str,
    secondary_cta: str,
    *,
    eyebrow: str = "Next step",
    capture_id: str = "result-capture-email",
) -> str:
    return f"""
<section class="conversion-hook">
<span class="eyebrow">{eyebrow}</span>
<h2>{title}</h2>
<p>{description}</p>
<div class="grid-tight">
<a class="card" href="{primary_href}">
<div class="card-kicker">Recommended next step</div>
<h3>{primary_title}</h3>
<p>{primary_description}</p>
<span class="cta">{primary_cta}</span>
</a>
<a class="card" href="{secondary_href}">
<div class="card-kicker">Useful second route</div>
<h3>{secondary_title}</h3>
<p>{secondary_description}</p>
<span class="cta">{secondary_cta}</span>
</a>
</div>
{render_result_capture(capture_id)}
</section>
"""


def render_tool_ui_templates() -> str:
    return (
        '<div class="tool-ui-templates" hidden aria-hidden="true">'
        f'<template id="ukpg-result-capture-template">{render_result_capture("__RESULT_CAPTURE_ID__")}</template>'
        "</div>"
    )
