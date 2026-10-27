from __future__ import annotations

from html import escape

from data.building_regs_sister import (
    BUILDING_REGS_DESTINATIONS,
    destination_by_key,
    destination_for_download,
    destination_for_project,
)


def _external_card(destination: dict, *, kicker: str = "BuildingRegsGuide") -> str:
    if not destination:
        return ""
    return f"""
<a class="card" href="{escape(destination['url'], quote=True)}">
<div class="card-kicker">{escape(kicker)}</div>
<h3>{escape(destination['title'])}</h3>
<p>{escape(destination['description'])}</p>
<span class="cta">Open sister guide</span>
</a>
"""


def build_project_building_regs_handoff(project_slug: str, project_title: str, town_name: str = "") -> str:
    destination = destination_for_project(project_slug)
    if not destination:
        return ""

    place_phrase = f" in {town_name}" if town_name else ""
    project_label = str(project_title or "this project").replace("Planning Permission", "").strip() or "this project"
    return f"""
<section class="building-regs-handoff" data-nosnippet>
<span class="eyebrow">Planning here, building regs next</span>
<h2>Keep Planning Permission Separate From Building Regulations</h2>
<p class="section-lead">UK Planning Guide keeps the planning route for {escape(project_label.lower())}{escape(place_phrase)} clear. BuildingRegsGuide owns the technical approval route, evidence, inspections and certificate questions once the design is moving toward construction.</p>
<div class="grid">
{_external_card(destination)}
{_external_card(BUILDING_REGS_DESTINATIONS["route-checker"], kicker="BuildingRegsGuide tool")}
</div>
</section>
"""


def build_generic_building_regs_handoff(*, title: str = "Building regulations next steps", destination_key: str = "planning-vs-regs") -> str:
    destination = destination_by_key(destination_key)
    if not destination:
        return ""
    return f"""
<section class="building-regs-handoff" data-nosnippet>
<span class="eyebrow">Sister-site handoff</span>
<h2>{escape(title)}</h2>
<p class="section-lead">Use UK Planning Guide for the planning-permission question. Use BuildingRegsGuide when the next issue is building control, inspections, competent person certification, completion evidence or approved-document guidance.</p>
<div class="grid">
{_external_card(destination)}
{_external_card(BUILDING_REGS_DESTINATIONS["route-checker"], kicker="BuildingRegsGuide tool")}
</div>
</section>
"""


def build_download_building_regs_handoff(asset_slug: str) -> str:
    destination = destination_for_download(asset_slug)
    if not destination:
        return ""
    return f"""
<section class="building-regs-handoff" data-nosnippet>
<span class="eyebrow">Planning here, building regs next</span>
<h2>Pair This Planning Checklist With The Technical Evidence Route</h2>
<p class="section-lead">This download helps with the planning-side decision. BuildingRegsGuide covers the building-control conversation, inspection stages and certificate evidence to keep once the project moves toward work.</p>
<div class="grid">
{_external_card(destination)}
{_external_card(BUILDING_REGS_DESTINATIONS["completion-certificate"], kicker="Evidence guide")}
</div>
</section>
"""
