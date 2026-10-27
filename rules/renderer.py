# ------------------------------------------------
# RULE RENDERING (FIXED)
# ------------------------------------------------

import html as html_lib


def render_rules(rule, scenario_slug=None):

    if not rule:
        return ""

    rules = rule.get("rules", {})
    restrictions = rule.get("restrictions", {})

    # --------------------------------
    # RULE EXPLANATIONS
    # --------------------------------

    rule_explanations = {

        "height_rules": """
<p>
Height limits exist to prevent extensions or roof alterations from
overpowering neighbouring properties or significantly changing the
character of the surrounding area. Planning officers typically assess
whether the proposed structure would appear dominant or intrusive
when viewed from neighbouring homes or public spaces.
</p>

<p>
Even where a development falls within permitted development limits,
larger structures may still require careful design to avoid overlooking
or overshadowing nearby properties.
</p>
""",

        "depth_rules": """
<p>
Depth limits restrict how far an extension can project from the
original rear wall of the property. These rules help ensure that
extensions remain proportionate to the original house and do not
create excessive loss of light or privacy for neighbouring homes.
</p>
""",

        "boundary_rules": """
<p>
Boundary distance rules help protect neighbouring properties from
overshadowing, overlooking, and overbearing development. Structures
built very close to boundaries are subject to stricter height limits
to minimise their visual impact.
</p>
""",

        "roof_rules": """
<p>
Roof alteration limits control the size of dormers and other roof
extensions to ensure that changes remain visually subordinate to the
original roof. Excessively large roof alterations may require planning
permission even if other elements of the development fall within
permitted development rights.
</p>
""",

        "materials_rules": """
<p>
Materials used in extensions or roof alterations should normally
match the appearance of the existing building. This helps maintain
a consistent streetscape and ensures new development blends with
the surrounding area.
</p>
"""
    }

    html_output = ""

    # --------------------------------
    # Helper: render paragraph or list
    # --------------------------------

    def render_text_block(text):

        if not text:
            return ""

        if isinstance(text, list):

            block = ""
            for paragraph in text:
                if paragraph and str(paragraph).strip():
                    block += f"<p>{html_lib.escape(str(paragraph))}</p>"
            return block

        else:
            return f"<p>{html_lib.escape(str(text))}</p>"

    # --------------------------------
    # Scenario specific ordering
    # --------------------------------

    if scenario_slug in ["height-limits", "maximum-height"]:

        sections = [
            ("Height Rules", rules.get("height_rules")),
            ("Boundary Rules", rules.get("boundary_rules")),
            ("Roof Alterations", rules.get("roof_rules")),
            ("Materials", rules.get("materials_rules"))
        ]

    elif scenario_slug in ["boundary-rules", "distance-from-boundary"]:

        sections = [
            ("Boundary Rules", rules.get("boundary_rules")),
            ("Height Rules", rules.get("height_rules")),
            ("Depth Rules", rules.get("depth_rules"))
        ]

    elif scenario_slug in ["roof-alterations", "roof-rules"]:

        sections = [
            ("Roof Alterations", rules.get("roof_rules")),
            ("Materials", rules.get("materials_rules"))
        ]

    else:

        sections = [
            ("Height Rules", rules.get("height_rules")),
            ("Depth Rules", rules.get("depth_rules")),
            ("Boundary Rules", rules.get("boundary_rules")),
            ("Roof Alterations", rules.get("roof_rules")),
            ("Materials", rules.get("materials_rules"))
        ]

    # --------------------------------
    # Render rule sections
    # --------------------------------

    for title, text in sections:

        if text and str(text).strip():

            rule_key = None

            if title == "Height Rules":
                rule_key = "height_rules"
            elif title == "Depth Rules":
                rule_key = "depth_rules"
            elif title == "Boundary Rules":
                rule_key = "boundary_rules"
            elif title == "Roof Alterations":
                rule_key = "roof_rules"
            elif title == "Materials":
                rule_key = "materials_rules"

            explanation = rule_explanations.get(rule_key, "")

            html_output += f"""

<div class="card">

<h2>{title}</h2>

{render_text_block(text)}

{explanation}

</div>
"""

    # --------------------------------
    # Local planning restrictions
    # --------------------------------

    restriction_html = ""

    conservation = restrictions.get("conservation_area")
    listed = restrictions.get("listed_building")
    article4 = restrictions.get("article4_applies")
    article4_note = restrictions.get("article4_notes")

    if conservation:
        restriction_html += render_text_block(conservation)

    if listed:
        restriction_html += render_text_block(listed)

    if article4:
        text = "Article 4 directions may remove permitted development rights in some areas."
        if article4_note:
            text += " " + str(article4_note)

        restriction_html += f"<p>{html_lib.escape(text)}</p>"

    if restriction_html:

        html_output += f"""

<div class="card">

<h2>Local Planning Restrictions</h2>

{restriction_html}

</div>
"""

    return html_output