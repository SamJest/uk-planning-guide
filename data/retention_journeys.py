from __future__ import annotations


DEFAULT_RETENTION_JOURNEY = {
    "eyebrow": "My Planning Project",
    "title": "Keep This Check With Your Project Notes",
    "description": "Save the route, add one next action, or open the workspace before the details get scattered across tabs and notes.",
    "workspace_action_label": "Save this check",
    "task_action_label": "Add next task",
    "task_title_template": "Follow up: {title}",
    "task_summary": "Turn this page into a concrete follow-up task you can come back to later.",
    "save_summary_template": "Saved route check from {title}.",
    "next_tool_href": "/tools/planning-route-check/",
    "next_tool_label": "Run route check",
    "lead_cta_label": "Ask for planning help",
    "lead_href": "/planning-help/",
}


RETENTION_JOURNEYS = {
    "hmo-article-4": {
        "title": "Save The HMO Coverage Check",
        "description": "Keep the Article 4, change-of-use and official-source checks together before you rely on a permitted-development assumption.",
        "workspace_action_label": "Save coverage check",
        "task_action_label": "Add coverage task",
        "task_title_template": "Check Article 4 coverage for {title}",
        "task_summary": "Add a task to verify the exact property against the local Article 4 or HMO source.",
        "save_summary_template": "Saved HMO Article 4 route from {title}.",
        "next_tool_href": "/article-4-hmo-by-council/",
        "next_tool_label": "Compare HMO routes",
    },
    "planning-portal": {
        "title": "Save The Council Route",
        "description": "Keep the official portal, local project route and next verification step in one workspace before opening more council pages.",
        "workspace_action_label": "Save council route",
        "task_action_label": "Add portal task",
        "task_title_template": "Check official council route for {title}",
        "task_summary": "Add a task to open the official portal and then move into the matching project guide.",
        "save_summary_template": "Saved council route from {title}.",
        "next_tool_href": "/tools/planning-decision-tool/",
        "next_tool_label": "Check likely route",
    },
    "conservation-map": {
        "title": "Save The Map And Source Check",
        "description": "Keep the heritage map/source check with the project route so the designation question does not get lost later.",
        "workspace_action_label": "Save map check",
        "task_action_label": "Add source task",
        "task_title_template": "Verify conservation-area source for {title}",
        "task_summary": "Add a task to confirm the official conservation-area position before using the project rule.",
        "save_summary_template": "Saved conservation-area source check from {title}.",
        "next_tool_href": "/conservation-areas/",
        "next_tool_label": "Open conservation hub",
    },
    "extension-drawings": {
        "title": "Save The Drawing-Readiness Check",
        "description": "Keep validation, drawings and spend-order notes together before paying for the wrong pack or application route.",
        "workspace_action_label": "Save drawing check",
        "task_action_label": "Add drawing task",
        "task_title_template": "Check drawing readiness for {title}",
        "task_summary": "Add a task to confirm drawings, validation and the local project route before spend.",
        "save_summary_template": "Saved extension drawing-readiness route from {title}.",
        "next_tool_href": "/tools/project-requirements-generator/",
        "next_tool_label": "Build requirements pack",
    },
    "dropped-kerb-highway": {
        "title": "Save The Planning Vs Highway Check",
        "description": "Keep planning permission, highway approval, drainage and access checks together before driveway or kerb work starts.",
        "workspace_action_label": "Save kerb checklist",
        "task_action_label": "Add highway task",
        "task_title_template": "Separate planning and highway checks for {title}",
        "task_summary": "Add a task to confirm whether planning, highway approval or both are needed.",
        "save_summary_template": "Saved planning versus highway route from {title}.",
        "next_tool_href": "/dropped-kerbs/",
        "next_tool_label": "Open dropped kerb hub",
    },
    "porch-outbuilding-rules": {
        "title": "Save The Country-Specific Rule Check",
        "description": "Keep Scotland or Wales rule notes with the local route before relying on an England-led summary.",
        "workspace_action_label": "Save rule check",
        "task_action_label": "Add official-rule task",
        "task_title_template": "Verify country-specific rule for {title}",
        "task_summary": "Add a task to confirm the official country or council source before relying on the route.",
        "save_summary_template": "Saved country-specific rule check from {title}.",
        "next_tool_href": "/tools/planning-decision-tool/",
        "next_tool_label": "Check likely route",
    },
}


def retention_journey_for_key(key: str) -> dict[str, str]:
    journey = dict(DEFAULT_RETENTION_JOURNEY)
    journey.update(RETENTION_JOURNEYS.get(str(key or "").strip(), {}))
    return journey


def infer_retention_key(path: str, target: dict | None = None) -> str:
    target = target or {}
    text = " ".join(
        str(part or "")
        for part in (
            path,
            target.get("meta_title", ""),
            target.get("title", ""),
            target.get("answer", ""),
            target.get("next_step", ""),
            target.get("primary_href", ""),
        )
    ).lower()

    if "hmo" in text or "article 4" in text:
        return "hmo-article-4"
    if "planning portal" in text or "/councils/" in text:
        return "planning-portal"
    if "conservation" in text or "heritage" in text:
        return "conservation-map"
    if "drawing" in text or "drawings" in text or "plans" in text or "validation" in text:
        return "extension-drawings"
    if "dropped kerb" in text or "dropped-kerb" in text or "driveway" in text or "highway" in text:
        return "dropped-kerb-highway"
    if "porch" in text or "outbuilding" in text or "scotland" in text or "wales" in text:
        return "porch-outbuilding-rules"
    return "default"
