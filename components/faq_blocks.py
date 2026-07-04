from components.planning_helpers import faq_schema


def build_faq_section(
    items,
    *,
    section_id: str = "faq",
    eyebrow: str = "Quick questions",
    title: str = "Questions people usually ask next",
    intro: str = "",
    class_name: str = "faq-section",
) -> str:
    if not items:
        return ""

    intro_html = f"<p class='section-lead'>{intro}</p>" if intro else ""
    faq_html = "".join(
        f"""
<div class="faq-item">
<h3>{question}</h3>
<p>{answer}</p>
</div>
"""
        for question, answer in items
    )

    return f"""
<section class="{class_name}" id="{section_id}">
<span class="eyebrow">{eyebrow}</span>
<h2>{title}</h2>
{intro_html}
{faq_html}
<script type="application/ld+json">{faq_schema(items)}</script>
</section>
"""
