import random


SCENARIO_RULE_KEYS = {
    "planning-permission": "permitted_development",
    "permitted-development": "permitted_development",
    "height-limits": "height_rules",
    "maximum-height": "height_rules",
    "depth-limits": "depth_rules",
    "boundary-rules": "boundary_rules",
    "distance-from-boundary": "boundary_rules",
    "roof-alterations": "roof_rules",
}


def _extract_description(rule, scenario_slug):
    if not isinstance(rule, dict):
        return ""

    if scenario_slug in {"conservation-areas", "listed-buildings", "article-4"}:
        restriction_key = {
            "conservation-areas": "conservation_area",
            "listed-buildings": "listed_building",
            "article-4": "article4_notes",
        }[scenario_slug]
        return str(rule.get("restrictions", {}).get(restriction_key, "")).strip()

    rule_key = SCENARIO_RULE_KEYS.get(scenario_slug)
    if rule_key == "permitted_development":
        return str(rule.get("permitted_development", "")).strip()

    value = rule.get("rules", {}).get(rule_key, "")
    if isinstance(value, list):
        return str(value[0]).strip() if value else ""
    return str(value).strip()


def build_rule_interpretation(rule, project_title=None, scenario_slug=None, town_name=None):
    project_title = project_title or "your project"
    scenario_slug = scenario_slug or "this-scenario"
    town_name = town_name or "your area"

    scenario_readable = scenario_slug.replace("-", " ")
    description = _extract_description(rule, scenario_slug)

    intro_variants = [
        f"How This Rule Usually Affects {project_title} In {town_name}",
        f"How To Read This Rule For {project_title} In {town_name}",
        f"What Usually Changes Once This Rule Matters In {town_name}",
    ]

    context_variants = [
        f"In practical terms, this is one of the rules that most often shifts the answer for {scenario_readable} questions in {town_name}.",
        f"For {scenario_readable} questions in {town_name}, this rule often decides whether the route stays simple or needs a closer check.",
        f"If you're planning work in {town_name}, this rule is often the point where a rough assumption stops being reliable.",
    ]

    nuance_variants = [
        "The exact effect still depends on the site, neighbouring context, previous alterations and how close the design is to a hard limit.",
        "Small changes in dimensions, siting or roof form can be enough to change the planning route.",
        "Local context and precise drawings matter more here than broad rules of thumb.",
    ]

    guidance_variants = [
        f"The safest approach in {town_name} is to compare your exact proposal with both the national baseline and any local restrictions before relying on the simpler answer.",
        f"For properties in {town_name}, treat this page as a practical briefing note, then verify formally if the proposal is borderline.",
        f"In {town_name}, this rule is most useful when it pushes you toward a clearer next step rather than a guess.",
    ]

    random.seed(f"{project_title}-{scenario_slug}-{town_name}")

    fallback = (
        f"This guide summarises how {scenario_readable} can affect "
        f"{project_title.lower()} proposals in {town_name}."
    )

    return f"""
<section class="rule-interpretation">
<span class="eyebrow">Interpretation</span>
<h2>{random.choice(intro_variants)}</h2>
<p>{description or fallback}</p>
<p>{random.choice(context_variants)}</p>
<p>{random.choice(nuance_variants)}</p>
<p>{random.choice(guidance_variants)}</p>
</section>
"""
