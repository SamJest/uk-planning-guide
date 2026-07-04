from copy import deepcopy

from data.scenario_data import SCENARIO_LOOKUP


STATUS_COPY = {
    "clear": {
        "label": "Looks straightforward",
        "tone": "good",
        "summary": "Nothing in these answers points to the first obvious tripwires for this topic, but exact measurements and local controls still matter.",
    },
    "warn": {
        "label": "Needs a closer check",
        "tone": "warn",
        "summary": "These answers sit close to the point where the topic usually needs a more exact measurement or a local policy check.",
    },
    "danger": {
        "label": "Formal or specialist check likely",
        "tone": "danger",
        "summary": "These answers suggest the simpler route is no longer a safe assumption, so the detailed guidance or formal process is the safer next move.",
    },
}


TYPE_PROFILES = {
    "structural": {
        "intro": "Use this when the main uncertainty is whether the project still looks comfortably within the normal height or scale envelope.",
        "questions": [
            {
                "id": "threshold",
                "step_label": "Threshold",
                "label": "How close does the proposal feel to the usual limit?",
                "help": "Use the closest high-level description rather than a perfect measurement.",
                "options": [
                    {"value": "comfortable", "label": "Comfortably inside", "hint": "It still looks clearly under the common limit.", "impact": "clear"},
                    {"value": "close", "label": "Close to the limit", "hint": "A small measurement change could alter the answer.", "impact": "warn", "reason": "The proposal sounds close enough to a common threshold that exact measurement matters."},
                    {"value": "beyond", "label": "Probably beyond it", "hint": "It already feels larger or taller than the simple route allows.", "impact": "danger", "reason": "The project already sounds beyond the first structural limit this self-check is designed around."},
                ],
            },
            {
                "id": "boundary",
                "step_label": "Boundary",
                "label": "Does the taller or larger part sit close to a boundary?",
                "help": "Boundary position often tightens height and scale checks.",
                "options": [
                    {"value": "no", "label": "No, with clear space", "hint": "The sensitive edge has room around it.", "impact": "clear"},
                    {"value": "somewhat", "label": "Some parts are close", "hint": "The boundary relationship could still change the answer.", "impact": "warn", "reason": "Boundary proximity can make an otherwise simple height or scale answer more sensitive."},
                    {"value": "yes", "label": "Yes, very close", "hint": "The higher part is tight to the boundary.", "impact": "danger", "reason": "A taller element close to the boundary is one of the clearest reasons this topic needs a stricter check."},
                ],
            },
            {
                "id": "certainty",
                "step_label": "Certainty",
                "label": "How certain are you about the measurements?",
                "help": "A quick self-check is less reliable when the dimensions are still rough.",
                "options": [
                    {"value": "measured", "label": "Measured already", "hint": "You have drawings or reliable dimensions.", "impact": "clear"},
                    {"value": "estimated", "label": "Estimated only", "hint": "You know roughly where it lands but not precisely.", "impact": "warn", "reason": "Estimated dimensions are often enough to move a structural topic from simple to borderline."},
                    {"value": "unknown", "label": "Not measured yet", "hint": "You still need a proper measurement pass.", "impact": "warn", "reason": "Without proper dimensions, this topic should be treated as a closer check rather than a clean answer."},
                ],
            },
        ],
        "baseline_reason": "The project does not sound close to the first obvious height and scale tripwires this check is looking for.",
        "changes": [
            "Exact height measured from the correct ground level.",
            "How the project sits relative to the nearest boundary.",
            "Any conservation area, Article 4 or heritage control affecting the property.",
        ],
        "next_checks": [
            "Measure the relevant height or bulk from the correct reference point before relying on the result.",
            "Open the detailed topic page if the proposal is anywhere near a published threshold.",
            "Use the decision engine if the wider planning route still feels unclear.",
        ],
    },
    "scale": {
        "intro": "Use this when the main uncertainty is how far the project projects from the house or spreads across the plot before the simpler route stops looking safe.",
        "questions": [
            {
                "id": "threshold",
                "step_label": "Threshold",
                "label": "How close does the proposal feel to the usual projection or coverage limit?",
                "help": "Use the closest high-level description rather than a perfect measurement.",
                "options": [
                    {"value": "comfortable", "label": "Comfortably inside", "hint": "It still looks clearly under the common limit.", "impact": "clear"},
                    {"value": "close", "label": "Close to the limit", "hint": "A small measurement change could alter the answer.", "impact": "warn", "reason": "The proposal sounds close enough to a common depth or projection threshold that exact measurement matters."},
                    {"value": "beyond", "label": "Probably beyond it", "hint": "It already feels larger or deeper than the simple route allows.", "impact": "danger", "reason": "The project already sounds beyond the first depth or projection limit this self-check is designed around."},
                ],
            },
            {
                "id": "context",
                "step_label": "Context",
                "label": "Does the extra depth or spread create pressure on boundaries, garden space or frontage?",
                "help": "Depth questions often stop being simple when the proposal starts to dominate the plot.",
                "options": [
                    {"value": "no", "label": "No, still comfortable", "hint": "The layout still feels modest on the plot.", "impact": "clear"},
                    {"value": "somewhat", "label": "Some pressure", "hint": "The design starts to feel tight or more dominant.", "impact": "warn", "reason": "Once a proposal starts to squeeze the plot or frontage, depth limits usually need a closer check."},
                    {"value": "yes", "label": "Yes, clearly pushing it", "hint": "The projection or spread feels dominant already.", "impact": "danger", "reason": "A design that already feels dominant on the plot is one of the clearest signs this depth question needs the stricter route."},
                ],
            },
            {
                "id": "certainty",
                "step_label": "Certainty",
                "label": "How certain are you about the measurements?",
                "help": "A quick self-check is less reliable when the dimensions are still rough.",
                "options": [
                    {"value": "measured", "label": "Measured already", "hint": "You have drawings or reliable dimensions.", "impact": "clear"},
                    {"value": "estimated", "label": "Estimated only", "hint": "You know roughly where it lands but not precisely.", "impact": "warn", "reason": "Estimated dimensions are often enough to move a depth-limits topic from simple to borderline."},
                    {"value": "unknown", "label": "Not measured yet", "hint": "You still need a proper measurement pass.", "impact": "warn", "reason": "Without proper dimensions, a depth-limits question should be treated as a closer check rather than a clean answer."},
                ],
            },
        ],
        "baseline_reason": "The project does not sound close to the first obvious depth or projection tripwires this check is looking for.",
        "changes": [
            "Exact projection measured from the correct original wall or reference point.",
            "How the increased depth affects the plot, frontage or remaining garden space.",
            "Any local restriction or prior approval route that changes the normal baseline.",
        ],
        "next_checks": [
            "Measure the projection from the correct original building line before relying on the result.",
            "Check whether the wider site layout makes the extra depth feel tighter in practice.",
            "Use the decision engine if the wider planning route still feels unclear.",
        ],
    },
    "neighbour": {
        "intro": "Use this when the main issue is how close the work is to a neighbour boundary and whether bulk, overlooking or siting could change the answer.",
        "questions": [
            {
                "id": "position",
                "step_label": "Position",
                "label": "How close is the project to the boundary in the sensitive spot?",
                "help": "Pick the description that feels closest to the tightest edge.",
                "options": [
                    {"value": "clear_gap", "label": "Clear gap", "hint": "There is comfortable room away from the boundary.", "impact": "clear"},
                    {"value": "tight_gap", "label": "Quite tight", "hint": "The project starts to feel close in one or two places.", "impact": "warn", "reason": "A tighter boundary gap is often enough to push a neighbour-rule topic into closer review."},
                    {"value": "on_boundary", "label": "On or almost on it", "hint": "The proposal is right against the boundary line.", "impact": "danger", "reason": "A project on or almost on the boundary usually needs the stricter version of the neighbour-rule check."},
                ],
            },
            {
                "id": "impact",
                "step_label": "Impact",
                "label": "How much visual or privacy impact could the project create?",
                "help": "Think about height, bulk and whether windows or roof changes face neighbours.",
                "options": [
                    {"value": "low", "label": "Low impact", "hint": "Little change to privacy or outlook.", "impact": "clear"},
                    {"value": "medium", "label": "Some impact", "hint": "There could be overlooking, enclosure or bulk concerns.", "impact": "warn", "reason": "Neighbour impact is one of the most common reasons a boundary question stops being straightforward."},
                    {"value": "high", "label": "High impact", "hint": "It looks likely to affect outlook, daylight or privacy.", "impact": "danger", "reason": "The proposal sounds likely to trigger the stronger neighbour-impact checks rather than a simple rule-of-thumb answer."},
                ],
            },
            {
                "id": "certainty",
                "step_label": "Certainty",
                "label": "How exact is the siting information?",
                "help": "Boundary topics are very sensitive to a small measurement shift.",
                "options": [
                    {"value": "measured", "label": "Measured from plans", "hint": "You know the relevant distances.", "impact": "clear"},
                    {"value": "rough", "label": "Roughly known", "hint": "You know the siting only in broad terms.", "impact": "warn", "reason": "Boundary topics get risky quickly when the gap is only roughly known."},
                    {"value": "unknown", "label": "Not checked yet", "hint": "You still need a proper dimension check.", "impact": "warn", "reason": "Until the boundary distances are measured properly, this topic should be treated as borderline."},
                ],
            },
        ],
        "baseline_reason": "The proposal does not sound close to the first neighbour-impact or boundary-distance tripwires this check is looking for.",
        "changes": [
            "Exact distance from the boundary measured on the correct face of the building.",
            "Whether the higher or more visible part is the part nearest the boundary.",
            "Any overlooking, roof change or local constraint that tightens the normal position.",
        ],
        "next_checks": [
            "Measure the tightest boundary gap rather than the easiest one to estimate.",
            "Stress-test the higher or more visible part of the design, not just the footprint.",
            "Open the topic guide if neighbour impact is already the main concern.",
        ],
    },
    "heritage": {
        "intro": "Use this when the main uncertainty is whether heritage controls change the normal planning answer for visible work.",
        "questions": [
            {
                "id": "status",
                "step_label": "Status",
                "label": "What do you know about the heritage designation?",
                "help": "Pick the most reliable status you have today.",
                "options": [
                    {"value": "not_affected", "label": "No designation found", "hint": "You have checked and nothing special is flagged.", "impact": "clear"},
                    {"value": "unsure", "label": "Not sure yet", "hint": "You still need to confirm the designation.", "impact": "warn", "reason": "Until the heritage status is confirmed, the safer assumption is that the normal answer may change."},
                    {"value": "affected", "label": "Definitely affected", "hint": "The property or area is already known to be protected.", "impact": "danger", "reason": "A confirmed heritage designation usually means the standard householder answer is no longer enough on its own."},
                ],
            },
            {
                "id": "visibility",
                "step_label": "Visibility",
                "label": "How visible is the proposed external change?",
                "help": "Think about the street scene, main elevations and original features.",
                "options": [
                    {"value": "modest", "label": "Mostly modest or tucked away", "hint": "The change is limited or not very exposed.", "impact": "clear"},
                    {"value": "visible", "label": "Clearly visible", "hint": "The change will be noticeable from outside.", "impact": "warn", "reason": "Visible external work is where heritage controls start to matter much more."},
                    {"value": "major", "label": "Prominent or fabric-changing", "hint": "The work affects important visible parts or original character.", "impact": "danger", "reason": "Prominent change to visible elevations or original fabric is usually a specialist heritage question rather than a quick check."},
                ],
            },
            {
                "id": "certainty",
                "step_label": "Process",
                "label": "How far through the heritage checking process are you?",
                "help": "This helps the tool decide whether the next move is still basic triage or a formal route.",
                "options": [
                    {"value": "checked", "label": "Already checked the basics", "hint": "You have looked at the designation and the affected features.", "impact": "clear"},
                    {"value": "partial", "label": "Some checks done", "hint": "You know part of the context but not the whole picture.", "impact": "warn", "reason": "Partial heritage checks usually still leave enough uncertainty to need the detailed guide."},
                    {"value": "early", "label": "Still very early", "hint": "You have not yet checked the heritage layer in detail.", "impact": "warn", "reason": "Early-stage heritage questions should be treated cautiously until the designation and affected features are confirmed."},
                ],
            },
        ],
        "baseline_reason": "Nothing here points to an obvious heritage override on its own, though visible change still needs checking carefully.",
        "changes": [
            "Whether the property, building or wider area is formally protected.",
            "How visible the work is from public viewpoints or key elevations.",
            "Whether original materials or character-defining features are being altered.",
        ],
        "next_checks": [
            "Confirm the heritage designation before relying on the normal route.",
            "Open the detailed topic page if the change is visible or affects original features.",
            "Use the council pages when local character guidance may tighten the response.",
        ],
    },
    "policy": {
        "intro": "Use this when a local policy layer such as an Article 4 direction may override the usual national planning position.",
        "questions": [
            {
                "id": "status",
                "step_label": "Status",
                "label": "How certain are you that the local restriction applies?",
                "help": "Pick the most accurate status you have today.",
                "options": [
                    {"value": "no", "label": "It does not apply", "hint": "You have checked and the restriction is not in force.", "impact": "clear"},
                    {"value": "unsure", "label": "I am not sure yet", "hint": "You still need to confirm whether the restriction applies.", "impact": "warn", "reason": "Unclear local policy status is enough to stop this from being a clean self-check answer."},
                    {"value": "yes", "label": "It definitely applies", "hint": "The property or area is already covered.", "impact": "danger", "reason": "A confirmed local restriction usually removes the safer assumption that the normal national route still applies."},
                ],
            },
            {
                "id": "visibility",
                "step_label": "Change",
                "label": "How visible or externally significant is the work?",
                "help": "Local restrictions matter most on visible external changes.",
                "options": [
                    {"value": "small", "label": "Minor or internal", "hint": "Very limited visible change.", "impact": "clear"},
                    {"value": "noticeable", "label": "Noticeable external change", "hint": "The work is visible enough that local policy could bite.", "impact": "warn", "reason": "A noticeable external change is where Article 4 and similar local controls tend to matter most."},
                    {"value": "major", "label": "Major external change", "hint": "The work clearly changes the building from outside.", "impact": "danger", "reason": "A major visible change in a locally controlled area usually needs the full policy route rather than a simple self-check."},
                ],
            },
            {
                "id": "route",
                "step_label": "Route",
                "label": "How much does your plan rely on normal permitted development rights?",
                "help": "This is the main planning question Article 4-style controls tend to change.",
                "options": [
                    {"value": "not_much", "label": "Not much", "hint": "You already expected a fuller planning route.", "impact": "clear"},
                    {"value": "somewhat", "label": "Quite a bit", "hint": "The project looks simpler only if normal rights still exist.", "impact": "warn", "reason": "If the project relies on the normal PD route, local policy restrictions matter much more."},
                    {"value": "entirely", "label": "Almost entirely", "hint": "The idea depends on the usual national rights remaining in place.", "impact": "danger", "reason": "Where the project depends heavily on normal PD rights, a confirmed local restriction is usually a decisive issue."},
                ],
            },
        ],
        "baseline_reason": "Nothing here suggests the local policy layer is clearly overriding the normal route, though it still needs confirming.",
        "changes": [
            "Whether the local restriction actually covers the property or only nearby streets.",
            "How visible the external work is once the design is fixed.",
            "Whether the proposal depends on normal PD rights that the local policy may remove.",
        ],
        "next_checks": [
            "Confirm the local restriction on the council map or written guidance before relying on the answer.",
            "Open the detailed topic page if the change is externally visible.",
            "Use the decision engine if the wider planning route still feels uncertain after the policy check.",
        ],
    },
    "design": {
        "intro": "Use this when the main uncertainty is whether a visible design change such as roof work still looks like the simpler route or needs a fuller planning check.",
        "questions": [
            {
                "id": "visibility",
                "step_label": "Visibility",
                "label": "How prominent is the visible change?",
                "help": "Think about the street-facing side and the overall visual impact.",
                "options": [
                    {"value": "rear_minor", "label": "Minor or tucked away", "hint": "A modest change with limited visibility.", "impact": "clear"},
                    {"value": "noticeable", "label": "Noticeable but not dominant", "hint": "The change is visible enough that design detail matters.", "impact": "warn", "reason": "Once the design change is clearly visible, the simple rule-of-thumb answer becomes less reliable."},
                    {"value": "prominent", "label": "Prominent or front-facing", "hint": "The change is visually assertive or clearly faces the street.", "impact": "danger", "reason": "A prominent visible change is one of the clearest signs this topic needs the fuller design check rather than a quick answer."},
                ],
            },
            {
                "id": "scale",
                "step_label": "Scale",
                "label": "How large is the design change?",
                "help": "Keep this high-level and focus on overall impact.",
                "options": [
                    {"value": "modest", "label": "Modest", "hint": "The change still feels secondary to the building.", "impact": "clear"},
                    {"value": "borderline", "label": "Around the limit", "hint": "The change is substantial enough that exact detail matters.", "impact": "warn", "reason": "The scale sounds close enough to a common threshold that detailed design is likely to decide the answer."},
                    {"value": "major", "label": "Major reshaping", "hint": "The change feels large or dominant already.", "impact": "danger", "reason": "A major design change usually needs the fuller route and visual impact review rather than a simple self-check."},
                ],
            },
            {
                "id": "constraints",
                "step_label": "Context",
                "label": "What do you know about local sensitivity on the site?",
                "help": "Visible design changes are much more context-sensitive than hidden ones.",
                "options": [
                    {"value": "none", "label": "No known sensitivity", "hint": "No special local control is known.", "impact": "clear"},
                    {"value": "unsure", "label": "Still unsure", "hint": "You have not checked the local layer yet.", "impact": "warn", "reason": "Until the local sensitivity is checked, visible design changes should be treated more cautiously."},
                    {"value": "sensitive", "label": "Sensitive site", "hint": "You already know the area or building has tighter controls.", "impact": "danger", "reason": "Visible design changes on a sensitive site usually need the stricter local route rather than a quick rule-of-thumb answer."},
                ],
            },
        ],
        "baseline_reason": "The design change does not sound close to the first obvious visual or roof-design tripwires this check is looking for.",
        "changes": [
            "How prominent the change is from the street or main viewpoints.",
            "Whether the overall size still reads as secondary to the existing building.",
            "Any local heritage or policy layer that tightens visible design changes.",
        ],
        "next_checks": [
            "Check the visible elevation rather than only the hidden side of the project.",
            "Open the detailed topic page if the change is front-facing or visually dominant.",
            "Use the rejection-risk analyzer if the main concern is design character rather than route alone.",
        ],
    },
}


TYPE_LINKS = {
    "structural": [
        {"title": "Planning Decision Engine", "href": "/tools/planning-decision-tool/", "description": "Use the wider route checker if the project feels borderline overall."},
        {"title": "Permitted Development", "href": "/permitted-development/", "description": "Open the main permitted development guide for the wider rule context."},
    ],
    "scale": [
        {"title": "Planning Decision Engine", "href": "/tools/planning-decision-tool/", "description": "Use the wider route checker if the project feels borderline overall."},
        {"title": "Permitted Development", "href": "/permitted-development/", "description": "Open the main permitted development guide for the wider rule context."},
    ],
    "neighbour": [
        {"title": "Planning Rejection Risk Analyzer", "href": "/tools/planning-rejection-risk-analyzer/", "description": "Stress-test neighbour and bulk objections if that is now the main concern."},
        {"title": "Boundary Rules", "href": "/boundary-rules/", "description": "Open the wider guide when boundary position is the key issue."},
    ],
    "heritage": [
        {"title": "Planning Permission", "href": "/planning-permission/", "description": "Open the main planning route guide for protected sites and visible change."},
        {"title": "Local Authorities", "href": "/councils/", "description": "Use the council pages when local heritage context may change the answer."},
    ],
    "policy": [
        {"title": "Planning Decision Engine", "href": "/tools/planning-decision-tool/", "description": "Check the wider route once the local policy status is clearer."},
        {"title": "Local Authorities", "href": "/councils/", "description": "Use the council pages to confirm the local control in force."},
    ],
    "design": [
        {"title": "Planning Rejection Risk Analyzer", "href": "/tools/planning-rejection-risk-analyzer/", "description": "Use the risk analyzer if design character is already the main concern."},
        {"title": "Planning Permission", "href": "/planning-permission/", "description": "Open the wider planning guide when visible design change is pushing toward an application."},
    ],
}


def build_scenario_tool_config(scenario_slug: str) -> dict:
    scenario = SCENARIO_LOOKUP[scenario_slug]
    profile = deepcopy(TYPE_PROFILES[scenario["type"]])
    profile["slug"] = scenario_slug
    profile["title"] = scenario["title"]
    profile["status_copy"] = deepcopy(STATUS_COPY)
    profile["links"] = [
        {
            "title": scenario["title"],
            "href": f"/{scenario_slug}/",
            "description": f"Open the full {scenario['title'].lower()} guide for the detailed rules behind this self-check.",
        },
        *deepcopy(TYPE_LINKS[scenario["type"]]),
    ]
    return profile
