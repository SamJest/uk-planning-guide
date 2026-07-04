from components.planning_helpers import first_text, is_meaningful_local_rule_signal, restriction_messages, useful_local_rule_items


def render_national_rule_cards(rule_data):
    if not rule_data:
        return ""

    html_parts = []
    rules = rule_data.get("rules", {})
    if not isinstance(rules, dict):
        return ""

    baseline_label = rule_data.get("baseline_label", "National rule baseline")
    for _, section in rules.items():
        if not isinstance(section, dict):
            continue

        title = section.get("title", "")
        intro = section.get("intro", "")
        rules_list = section.get("rules", [])
        details = section.get("details", "")
        exceptions = section.get("exceptions", "")

        rule_items = "".join(f"<li>{item}</li>" for item in rules_list[:5]) if isinstance(rules_list, list) else ""
        details_block = (
            f"""
            <details class="rule-details">
                <summary>Why this rule matters</summary>
                <p>{details}</p>
            </details>
            """
            if details
            else ""
        )
        exception_block = (
            f"""
            <div class="rule-exceptions">
                <strong>When this usually needs a closer check:</strong> {exceptions}
            </div>
            """
            if exceptions
            else ""
        )

        html_parts.append(
            f"""
            <section class="rule-card national-rule">
                <span class="eyebrow">{baseline_label}</span>
                <h2>{title}</h2>
                <p>{intro}</p>
                <ul class="rule-list">{rule_items}</ul>
                {details_block}
                {exception_block}
            </section>
            """
        )

    restriction_items = restriction_messages(rule_data)
    if restriction_items:
        list_html = "".join(
            f"<li><strong>{label}:</strong> {text}</li>" for label, text in restriction_items
        )
        html_parts.append(
            f"""
            <section class="planning-restrictions">
                <span class="eyebrow">Local restriction signals</span>
                <h2>Important Planning Restrictions</h2>
                <ul>{list_html}</ul>
            </section>
            """
        )

    return "\n".join(html_parts)


def build_local_rule_highlight(rule) -> str:
    if not rule:
        return ""

    last_verified = rule.get("last_verified", "")
    householder_label = rule.get("householder_label", "relevant householder and permitted development rules")
    pd_note = first_text(
        rule.get("permitted_development", ""),
        f"This area may still allow some projects under the {householder_label}, subject to the normal limits and any local restrictions.",
    )
    rule_snapshots = useful_local_rule_items(
        rule,
        keys=("depth_rules", "height_rules", "boundary_rules", "roof_rules"),
    )

    if not rule_snapshots and not is_meaningful_local_rule_signal(pd_note, "permitted_development"):
        return ""

    bullets = "".join(f"<li>{item}</li>" for item in rule_snapshots[:3])
    verified_line = f"<p class='rule-verification'>Last verified: {last_verified}</p>" if last_verified else ""
    intro = (
        pd_note
        if is_meaningful_local_rule_signal(pd_note, "permitted_development")
        else f"Start with the local route summary, then use the national rule cards below for the detail."
    )

    return f"""
<section class="local-rule-highlight">
<span class="eyebrow">Local rule snapshot</span>
<h2>The Most Useful Local Notes On One Screen</h2>
<p>{intro}</p>
{f"<ul class='checklist'>{bullets}</ul>" if bullets else ""}
{verified_line}
</section>
"""


def build_rule_comparison(project_title: str, town_name: str) -> str:
    return f"""
<section class="rule-comparison">
<span class="eyebrow">Decision comparison</span>
<h2>{project_title} In {town_name}: When The Route Usually Stays Simple And When It Does Not</h2>
<table class="rule-comparison-table">
<thead>
<tr>
<th>If the proposal stays within the usual envelope</th>
<th>If local controls, site history or design details complicate it</th>
<th>Best next step</th>
</tr>
</thead>
<tbody>
<tr>
<td>You may be able to rely on the simpler householder route that normally applies in this jurisdiction.</td>
<td>You may need a formal application, written council confirmation or a more cautious redesign.</td>
<td>Measure carefully, keep drawings ready and verify formally if the scheme is close to a threshold.</td>
</tr>
</tbody>
</table>
</section>
"""
