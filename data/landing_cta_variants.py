LANDING_CTA_VARIANTS = {
    "frontage": {
        "variant_id": "frontage",
        "primary_tool_href": "/tools/site-constraint-checker/",
        "primary_tool_title": "Check the planning and frontage constraints",
        "primary_tool_description": "Use the constraint checker when planning permission, highway approval, visibility or drainage may all be active at once.",
        "guidance_title": "Get a clearer read on planning vs highway issues",
        "guidance_description": "Use personalised guidance if the route depends on frontage layout, crossover approval, visibility, drainage or a sensitive edge-of-site detail.",
        "section_title": "The Fastest Next Step If Frontage Details Are Doing Most Of The Work",
        "section_description": "Use one of these next moves while the route question is still fresh. This is where planning, highway and local-detail questions usually separate.",
    },
    "use_policy": {
        "variant_id": "use_policy",
        "primary_tool_href": "/tools/planning-route-planner/",
        "primary_tool_title": "Map the policy and permission route",
        "primary_tool_description": "Use the route planner when use class, Article 4, local policy, parking or amenity pressure are driving the answer.",
        "guidance_title": "Get a clearer read on policy and use-class risk",
        "guidance_description": "Use personalised guidance if the route depends on Article 4, use class, local policy, concentration pressure, parking or neighbour impact.",
        "section_title": "The Fastest Next Step If Policy Or Use Class Is The Real Blocker",
        "section_description": "Use one of these next moves while the route still depends on the policy layer more than on one simple building measurement.",
    },
    "heritage": {
        "variant_id": "heritage",
        "primary_tool_href": "/tools/planning-decision-tool/",
        "primary_tool_title": "Run the planning decision tool",
        "primary_tool_description": "Use the planning decision tool when heritage, local controls and the broader route still need separating cleanly.",
        "guidance_title": "Get a clearer read on heritage risk",
        "guidance_description": "Use personalised guidance if conservation area, listed-building or heritage sensitivity is the reason the normal answer no longer feels safe.",
        "section_title": "The Fastest Next Step If Heritage Controls Are The Real Issue",
        "section_description": "Use one of these next moves while the heritage layer is still the main reason the route feels uncertain.",
    },
    "general_route": {
        "variant_id": "general_route",
        "primary_tool_href": "/tools/planning-decision-tool/",
        "primary_tool_title": "Run the planning decision tool",
        "primary_tool_description": "Use the planning decision tool when you want the fastest route-level answer before opening more local pages.",
        "guidance_title": "Get a clearer read on the local route",
        "guidance_description": "Use personalised guidance if the general route is clearer than before, but the local checks and safest formal step still are not.",
        "section_title": "The Fastest Next Step If You Want A More Useful Answer Quickly",
        "section_description": "Use one of these next moves while the route question is still broad enough to benefit from a clearer next step.",
    },
}

TARGET_PROJECT_SLUGS = {
    "fences-and-walls",
    "dropped-kerbs",
    "change-of-use",
    "porches",
    "outbuildings",
}

TARGET_PROJECT_SCENARIO_OVERRIDES = {
    "house-extensions",
    "annexes",
}

TARGET_SCENARIO_SLUGS = {
    "planning-permission",
    "permitted-development",
    "conservation-areas",
    "article-4",
    "listed-buildings",
}
