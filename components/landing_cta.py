from html import escape

from components.personalised_guidance import build_guidance_request_href
from data.landing_cta_variants import (
    LANDING_CTA_VARIANTS,
    TARGET_PROJECT_SCENARIO_OVERRIDES,
    TARGET_PROJECT_SLUGS,
    TARGET_SCENARIO_SLUGS,
)
from utils.live_links import is_live_internal_href, normalize_internal_href


def _project_variant(project_slug: str) -> str:
    slug = str(project_slug or "").strip().lower()
    if slug in {"dropped-kerbs", "driveways", "hard-surfaces", "fences-and-walls", "porches"}:
        return "frontage"
    if slug in {"change-of-use", "hmos"}:
        return "use_policy"
    return "general_route"


def _scenario_variant(scenario_slug: str) -> str:
    slug = str(scenario_slug or "").strip().lower()
    if slug in {"conservation-areas", "listed-buildings"}:
        return "heritage"
    if slug in {"article-4"}:
        return "use_policy"
    return "general_route"


def _first_live_href(*hrefs: str, fallback: str = "") -> str:
    for href in hrefs:
        clean = normalize_internal_href(href)
        if clean and is_live_internal_href(clean):
            return clean
    return normalize_internal_href(fallback)


def _landing_card(href: str, kicker: str, title: str, description: str, cta: str, role: str) -> str:
    return f"""
<a class="card" href="{escape(href, quote=True)}" data-landing-cta-role="{escape(role, quote=True)}" data-landing-cta-target="{escape(href, quote=True)}">
<div class="card-kicker">{kicker}</div>
<h3>{title}</h3>
<p>{description}</p>
<span class="cta">{cta}</span>
</a>
"""


def build_landing_handoff_block(
    *,
    variant_id: str,
    page_family: str,
    authority_slug: str = "",
    project_slug: str = "",
    scenario_slug: str = "",
    primary_tool_href: str,
    primary_tool_title: str,
    primary_tool_description: str,
    guidance_href: str,
    guidance_title: str,
    guidance_description: str,
    secondary_href: str,
    secondary_title: str,
    secondary_description: str,
    section_title: str,
    section_description: str,
    section_id: str = "landing-next-step",
) -> str:
    return f"""
<section class="landing-handoff" id="{escape(section_id, quote=True)}" data-landing-cta="true" data-page-family="{escape(page_family, quote=True)}" data-authority-slug="{escape(authority_slug, quote=True)}" data-project-slug="{escape(project_slug, quote=True)}" data-scenario-slug="{escape(scenario_slug, quote=True)}" data-cta-variant="{escape(variant_id, quote=True)}">
<span class="eyebrow">Next move</span>
<h2>{section_title}</h2>
<p class="section-lead">{section_description}</p>
<div class="grid">
{_landing_card(primary_tool_href, "Primary tool", primary_tool_title, primary_tool_description, "Open tool", "tool")}
{_landing_card(guidance_href, "Primary guidance", guidance_title, guidance_description, "Start guidance", "guidance")}
{_landing_card(secondary_href, "Best local follow-up", secondary_title, secondary_description, "Open follow-up", "secondary")}
</div>
</section>
"""


def build_project_landing_handoff(project_slug: str, clean_project: str, county_slug: str, town_slug: str, town_name: str) -> str:
    if project_slug not in TARGET_PROJECT_SLUGS:
        return ""

    variant_id = _project_variant(project_slug)
    variant = LANDING_CTA_VARIANTS[variant_id]
    planning_href = _first_live_href(f"/planning-permission/{town_slug}/", f"/councils/{town_slug}/", fallback=f"/{project_slug}/{county_slug}/{town_slug}/")
    guidance_href = build_guidance_request_href(
        context_label=f"landing-{variant_id}",
        email_context=f"{clean_project} in {town_name}",
        prefill={
            "authority": town_name,
            "location": town_name,
            "project_stage": "Just exploring the route",
            "project_summary": f"{clean_project} in {town_name}",
            "main_worry": variant["guidance_description"],
        },
    )
    return build_landing_handoff_block(
        variant_id=variant_id,
        page_family="project",
        authority_slug=town_slug,
        project_slug=project_slug,
        primary_tool_href=variant["primary_tool_href"],
        primary_tool_title=variant["primary_tool_title"],
        primary_tool_description=variant["primary_tool_description"],
        guidance_href=guidance_href,
        guidance_title=variant["guidance_title"],
        guidance_description=variant["guidance_description"],
        secondary_href=planning_href,
        secondary_title=f"Open planning permission in {town_name}",
        secondary_description="Use the local planning-permission page if the broader route still matters more than this one project detail.",
        section_title=variant["section_title"],
        section_description=variant["section_description"],
    )


def build_scenario_landing_handoff(
    *,
    page_family: str,
    authority_slug: str,
    town_name: str,
    project_slug: str,
    clean_project: str,
    county_slug: str = "",
    scenario_slug: str,
) -> str:
    if scenario_slug not in TARGET_SCENARIO_SLUGS and project_slug not in TARGET_PROJECT_SCENARIO_OVERRIDES:
        return ""

    variant_id = _scenario_variant(scenario_slug)
    variant = LANDING_CTA_VARIANTS[variant_id]
    project_href = _first_live_href(f"/{project_slug}/{county_slug}/{authority_slug}/", fallback=f"/councils/{authority_slug}/")
    guidance_href = build_guidance_request_href(
        context_label=f"landing-{variant_id}",
        email_context=f"{clean_project} in {town_name}: {scenario_slug.replace('-', ' ')}",
        prefill={
            "authority": town_name,
            "location": town_name,
            "project_stage": "Comparing options and measurements",
            "project_summary": f"{clean_project} in {town_name}",
            "main_worry": variant["guidance_description"],
        },
    )
    return build_landing_handoff_block(
        variant_id=variant_id,
        page_family=page_family,
        authority_slug=authority_slug,
        project_slug=project_slug,
        scenario_slug=scenario_slug,
        primary_tool_href=variant["primary_tool_href"],
        primary_tool_title=variant["primary_tool_title"],
        primary_tool_description=variant["primary_tool_description"],
        guidance_href=guidance_href,
        guidance_title=variant["guidance_title"],
        guidance_description=variant["guidance_description"],
        secondary_href=project_href,
        secondary_title=f"Open {clean_project} in {town_name}",
        secondary_description="Use the matching local project page if the route now depends more on the build itself than on this one rule.",
        section_title=variant["section_title"],
        section_description=variant["section_description"],
    )


def build_council_landing_handoff(town_slug: str, town_name: str, lead_project_href: str, lead_project_title: str) -> str:
    variant = LANDING_CTA_VARIANTS["general_route"]
    guidance_href = build_guidance_request_href(
        context_label="landing-general_route",
        email_context=f"Planning permission in {town_name}",
        prefill={
            "authority": town_name,
            "location": town_name,
            "project_stage": "Just exploring the route",
            "project_summary": f"Planning permission route in {town_name}",
            "main_worry": variant["guidance_description"],
        },
    )
    secondary_href = _first_live_href(lead_project_href, f"/planning-permission/{town_slug}/", fallback=f"/councils/{town_slug}/")
    secondary_title = f"Open {lead_project_title} in {town_name}" if secondary_href == normalize_internal_href(lead_project_href) else f"Open planning permission in {town_name}"
    secondary_description = (
        "Use the strongest local project guide if the build type is already clear."
        if secondary_href == normalize_internal_href(lead_project_href)
        else "Use the local planning-permission page if the route question still matters more than the exact build type."
    )
    return build_landing_handoff_block(
        variant_id="general_route",
        page_family="council",
        authority_slug=town_slug,
        primary_tool_href=variant["primary_tool_href"],
        primary_tool_title=variant["primary_tool_title"],
        primary_tool_description=variant["primary_tool_description"],
        guidance_href=guidance_href,
        guidance_title="Get a clearer read on the local route",
        guidance_description="Use personalised guidance if the local authority layer is clearer than before, but the safest next page or formal check still is not.",
        secondary_href=secondary_href,
        secondary_title=secondary_title,
        secondary_description=secondary_description,
        section_title=variant["section_title"],
        section_description=variant["section_description"],
    )
