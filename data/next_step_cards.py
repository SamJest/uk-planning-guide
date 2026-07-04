NEXT_STEP_CARDS = {
    "save-project": {
        "id": "save-project",
        "title": "Save this project",
        "description": "Keep the current page, route and next checks together on this device so you can come back without redoing the research.",
        "action_label": "Save project",
        "kind": "button",
        "event_name": "project_save",
    },
    "ldc-worth-check": {
        "id": "ldc-worth-check",
        "title": "Check if an LDC is worth it",
        "description": "Use this when the work may be permitted development but you want to know whether written proof is sensible before spending more.",
        "action_label": "Run LDC check",
        "href": "/tools/lawful-development-certificate-checker/",
        "event_name": "next_step_card_click",
    },
    "drawings-readiness": {
        "id": "drawings-readiness",
        "title": "Check drawing readiness",
        "description": "See whether the project is ready for drawings, or whether route, site or measurement issues should be tightened first.",
        "action_label": "Check readiness",
        "href": "/tools/drawings-cost-readiness-checker/",
        "event_name": "next_step_card_click",
    },
    "planning-cost": {
        "id": "planning-cost",
        "title": "Estimate planning costs",
        "description": "Sense-check likely application, drawing and certificate costs before choosing the next route.",
        "action_label": "Estimate costs",
        "href": "/tools/planning-cost-calculator/",
        "event_name": "next_step_card_click",
    },
    "application-readiness": {
        "id": "application-readiness",
        "title": "Check application readiness",
        "description": "Use this when the route is leaning formal and you want to know what still needs preparing.",
        "action_label": "Check application",
        "href": "/tools/planning-application-readiness-checker/",
        "event_name": "next_step_card_click",
    },
    "professional-route": {
        "id": "professional-route",
        "title": "Find the right help route",
        "description": "Use this once the answer depends on drawings, a council decision, heritage sensitivity or a higher-risk spend.",
        "action_label": "See help options",
        "href": "/planning-help/",
        "event_name": "next_step_card_click",
    },
    "full-guidance-form": {
        "id": "full-guidance-form",
        "title": "Ask for case-specific guidance",
        "description": "Use the longer form only when the lighter checks have narrowed the question but your own property or design still decides the route.",
        "action_label": "Open form",
        "href": "/personalised-planning-guidance/request/",
        "event_name": "next_step_card_click",
    },
}


ROUTE_ORDER = {
    "tool": ["save-project", "ldc-worth-check", "drawings-readiness", "planning-cost"],
    "cost-tool": ["save-project", "drawings-readiness", "application-readiness", "professional-route"],
    "ldc-tool": ["save-project", "drawings-readiness", "planning-cost", "full-guidance-form"],
    "guidance": ["ldc-worth-check", "planning-cost", "drawings-readiness", "full-guidance-form"],
    "formal": ["save-project", "application-readiness", "planning-cost", "professional-route"],
    "sensitive": ["save-project", "ldc-worth-check", "professional-route", "full-guidance-form"],
    "default": ["save-project", "ldc-worth-check", "planning-cost", "drawings-readiness"],
}


SENSITIVE_TERMS = (
    "article-4",
    "article 4",
    "conservation",
    "listed",
    "hmo",
    "flat",
    "maisonette",
    "heritage",
)


FORMAL_TERMS = (
    "planning-permission",
    "application",
    "prior-approval",
    "rejection",
    "risk",
    "dropped-kerb",
    "driveway",
)


def recommend_next_step_cards(
    *,
    page_family: str = "",
    project_slug: str = "",
    tool_slug: str = "",
    context_text: str = "",
    max_cards: int = 4,
) -> list[dict]:
    signal = " ".join([page_family, project_slug, tool_slug, context_text]).lower()

    if tool_slug == "lawful-development-certificate-checker":
        order = ROUTE_ORDER["ldc-tool"]
    elif tool_slug in {
        "planning-cost-calculator",
        "drawings-cost-readiness-checker",
        "planning-application-readiness-checker",
    }:
        order = ROUTE_ORDER["cost-tool"]
    elif any(term in signal for term in SENSITIVE_TERMS):
        order = ROUTE_ORDER["sensitive"]
    elif any(term in signal for term in FORMAL_TERMS):
        order = ROUTE_ORDER["formal"]
    elif "guidance" in page_family:
        order = ROUTE_ORDER["guidance"]
    elif tool_slug:
        order = ROUTE_ORDER["tool"]
    else:
        order = ROUTE_ORDER["default"]

    cards = []
    seen = set()
    for card_id in order:
        card = NEXT_STEP_CARDS.get(card_id)
        if not card or card_id in seen:
            continue
        seen.add(card_id)
        cards.append(card.copy())
        if len(cards) >= max_cards:
            break
    return cards
