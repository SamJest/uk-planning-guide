from html import escape

from data.next_step_cards import recommend_next_step_cards


def _attrs(attrs: dict[str, str]) -> str:
    pairs = []
    for key, value in attrs.items():
        if value is None:
            continue
        pairs.append(f'{key}="{escape(str(value), quote=True)}"')
    return " ".join(pairs)


def _render_card(card: dict, common_attrs: dict[str, str]) -> str:
    attrs = {
        **common_attrs,
        "data-next-step-card": card["id"],
        "data-next-step-event": card.get("event_name", "next_step_card_click"),
    }
    title = escape(card["title"])
    description = escape(card["description"])
    label = escape(card.get("action_label", "Open"))

    if card.get("kind") == "button":
        return f"""
<button class="next-step-card next-step-card-button" type="button" data-project-action="save-page" {_attrs(attrs)}>
<span class="card-kicker">Next move</span>
<strong>{title}</strong>
<span>{description}</span>
<em>{label}</em>
</button>
"""

    return f"""
<a class="next-step-card" href="{escape(card.get('href', '#'), quote=True)}" {_attrs(attrs)}>
<span class="card-kicker">Next move</span>
<strong>{title}</strong>
<span>{description}</span>
<em>{label}</em>
</a>
"""


def build_next_step_cards(
    *,
    page_family: str = "",
    project_slug: str = "",
    tool_slug: str = "",
    context_text: str = "",
    title: str = "Choose The Next Useful Step",
    intro: str = "Start with the action that gives you progress without asking for more detail than needed: save the project, check whether formal proof is worth it, or test cost and readiness before using the longer form.",
    max_cards: int = 4,
) -> str:
    cards = recommend_next_step_cards(
        page_family=page_family,
        project_slug=project_slug,
        tool_slug=tool_slug,
        context_text=context_text,
        max_cards=max_cards,
    )
    if not cards:
        return ""

    common_attrs = {
        "data-page-family": page_family,
        "data-project-slug": project_slug,
        "data-tool-slug": tool_slug,
    }
    cards_html = "".join(_render_card(card, common_attrs) for card in cards)

    return f"""
<section class="next-step-module" data-next-step-module="{escape(page_family or tool_slug or 'general', quote=True)}">
<span class="eyebrow">Next step</span>
<h2>{escape(title)}</h2>
<p class="section-lead">{escape(intro)}</p>
<div class="next-step-grid">
{cards_html}
</div>
</section>
"""


def build_project_tracker_prompt(*, page_family: str = "", tool_slug: str = "", project_slug: str = "") -> str:
    return f"""
<section class="project-tracker-prompt" data-project-tracker-prompt="true" data-page-family="{escape(page_family, quote=True)}" data-tool-slug="{escape(tool_slug, quote=True)}" data-project-slug="{escape(project_slug, quote=True)}">
<span class="eyebrow">My Planning Project</span>
<h2>Keep A Clean Project Pack On This Device</h2>
<p class="section-lead">Save the current page, print a simple pack, or copy a short summary for someone helping you decide the next move. Nothing is sent anywhere unless you choose to submit a form.</p>
<div class="hero-ctas">
<button class="btn" type="button" data-project-action="save-page">Save current page</button>
<button class="btn button-secondary" type="button" data-project-action="print-pack">Print pack</button>
<button class="btn button-secondary" type="button" data-project-action="copy-summary">Copy summary</button>
</div>
<p class="result-capture-note" data-project-note="true">Stored in this browser only. Clear it any time from the project panel.</p>
</section>
"""
