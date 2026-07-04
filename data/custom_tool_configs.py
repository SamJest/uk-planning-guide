from copy import deepcopy

from utils.live_links import filter_live_dict_links


CUSTOM_TOOL_CONFIGS = {
    "building-control-route-checker": {
        "slug": "building-control-route-checker",
        "title": "Building Control Route Checker",
        "intro": "Work out which building regulations conversation is most useful next: full plans, building notice, competent person certification, regularisation, or a planning-first pause.",
        "analytics": {"start_event": "building_control_route_start", "result_event": "building_control_route_result"},
        "result_bands": {
            "clear": "light-building-control-route",
            "warn": "building-control-route-needed",
            "danger": "formal-or-sensitive-route",
        },
        "status_copy": {
            "clear": {
                "label": "Light route still plausible",
                "tone": "good",
                "summary": "The answers do not yet point to the heaviest building-control route, but you should still keep the evidence and official checks together.",
            },
            "warn": {
                "label": "Building control route needed",
                "tone": "warn",
                "summary": "The project has enough technical work that building control, installer certification or clearer inspection planning should be treated as a live next step.",
            },
            "danger": {
                "label": "Formal route or pause likely",
                "tone": "danger",
                "summary": "The answers point toward full plans, regularisation, higher-risk/sensitive checks or a planning-first pause before work should move ahead.",
            },
        },
        "section_labels": {
            "primary": "Likely route to discuss",
            "secondary": "Evidence to prepare",
            "next": "What to do before work starts",
        },
        "baseline_reason": "Nothing here clearly points to the heaviest route yet, but building regulations should still be kept separate from planning permission.",
        "primary_items": [
            "Confirm whether building regulations approval is needed before work starts.",
            "Keep planning permission and building regulations as separate checks.",
        ],
        "secondary_items": [
            "Project description, rough drawings or measurements, and any contractor specification.",
            "A note of whether the work is new, already started or already completed.",
        ],
        "next_checks": [
            "Open the matching building regulations guide before contacting building control.",
            "Ask who books inspections and what must not be covered up before inspection.",
            "Save certificates, installer records and completion evidence with the project file.",
        ],
        "links": [
            {"title": "Building Regulations Hub", "href": "/building-regulations/", "description": "Open the England-first guide for the wider approval split."},
            {"title": "Before You Start Checklist", "href": "/building-regulations/before-you-start-checklist/", "description": "Use this before contractor work begins."},
            {"title": "Planning Vs Building Regulations", "href": "/planning-faq/planning-permission-vs-building-regulations/", "description": "Use this if the two systems are still being mixed together."},
        ],
        "questions": [
            {
                "id": "project",
                "step_label": "Project",
                "label": "Which kind of work is closest?",
                "help": "Choose the nearest project type so the route checker can bias toward the right building-control conversation.",
                "options": [
                    {"value": "extension", "label": "Extension", "hint": "New floor space, structure, insulation, drainage or opening work.", "impact": "warn", "reason": "Extensions commonly need building control because structure, insulation, drainage and fire safety can all be involved.", "primary_add": ["Full plans or building notice should be discussed before work starts."], "links_add": [{"title": "Building Regulations For Extensions", "href": "/building-regulations/extensions/", "description": "Open the extension-specific route."}]},
                    {"value": "loft", "label": "Loft conversion", "hint": "New habitable room, roof changes, stairs or structural floor work.", "impact": "danger", "reason": "Loft conversions are often building-control-heavy because structure, escape and stairs need checking.", "primary_add": ["A fuller building-control route is likely to be sensible before construction starts."], "secondary_add": ["Early drawings showing stairs, head height, structure and escape route."], "links_add": [{"title": "Loft Conversion Building Regulations", "href": "/building-regulations/loft-conversions/", "description": "Use this when the project changes roof space into living accommodation."}]},
                    {"value": "garage", "label": "Garage conversion", "hint": "Turning a garage into habitable space.", "impact": "warn", "reason": "Garage conversions usually need technical checks for insulation, damp, ventilation and fire safety.", "primary_add": ["Building control should be part of the route before the garage is treated as finished living space."], "links_add": [{"title": "Garage Conversion Building Regulations", "href": "/building-regulations/garage-conversions/", "description": "Open the garage conversion route."}]},
                    {"value": "porch", "label": "Porch or small entrance", "hint": "Small porch, glazing, electrics or thermal separation question.", "impact": "clear", "primary_add": ["Check whether an exemption really applies and whether any electrical or glazing work still needs certification."], "links_add": [{"title": "Porch Building Regulations", "href": "/building-regulations/porches/", "description": "Use this before relying on a small-porch exemption."}]},
                    {"value": "services", "label": "Windows, electrics or heating", "hint": "Specialist work that may be installer-certified.", "impact": "warn", "reason": "Some specialist work may use a competent person scheme, but the installer must be registered for the exact work.", "primary_add": ["Competent person certification may be the route to discuss."], "secondary_add": ["Installer scheme details, warranty and certificate evidence."], "links_add": [{"title": "Competent Person Schemes", "href": "/building-regulations/competent-person-schemes/", "description": "Use this when certification may replace a direct application."}]},
                    {"value": "outbuilding", "label": "Outbuilding or temporary structure", "hint": "Detached building, services, sleeping use or regular occupation.", "impact": "warn", "reason": "Detached or temporary structures become more sensitive when they are occupied, serviced, close to boundaries or used for sleeping.", "primary_add": ["Ask building control whether size, use, services or boundary position change the route."], "links_add": [{"title": "Outbuilding Building Regulations", "href": "/building-regulations/outbuildings/", "description": "Open the detached-building route."}]},
                ],
            },
            {
                "id": "stage",
                "step_label": "Stage",
                "label": "What stage is the work at?",
                "help": "The right route changes sharply once work has already started or been completed.",
                "options": [
                    {"value": "idea", "label": "Idea or early quote", "hint": "No work started.", "impact": "clear"},
                    {"value": "drawings", "label": "Drawings or contractor ready", "hint": "You may soon commit spend.", "impact": "warn", "reason": "Once drawings or contractor dates are live, the approval route should be settled before work starts.", "next_add": ["Check whether drawings are enough for full plans or whether the project is still too uncertain."]},
                    {"value": "started", "label": "Work already started", "hint": "Some work is underway.", "impact": "danger", "reason": "Started work can create inspection and evidence gaps if building control was not involved early enough.", "primary_add": ["Contact building control before more work is covered up."], "secondary_add": ["Photos of exposed work and dated contractor records."]},
                    {"value": "completed", "label": "Work already completed", "hint": "You are trying to sort evidence after the event.", "impact": "danger", "reason": "Completed work without approval evidence may need a regularisation discussion rather than an ordinary pre-start route.", "primary_add": ["Regularisation may need to be discussed with local authority building control."], "links_add": [{"title": "Regularisation Certificates", "href": "/building-regulations/regularisation-certificates/", "description": "Use this for missing approval on past work."}]},
                ],
            },
            {
                "id": "planning",
                "step_label": "Planning",
                "label": "Is the planning route already settled?",
                "help": "Building control does not decide whether the development itself needs planning permission.",
                "options": [
                    {"value": "settled", "label": "Yes, planning is settled", "hint": "Permission, LDC or a clear route is in place.", "impact": "clear"},
                    {"value": "probably", "label": "Probably, but not proven", "hint": "You think it is permitted development or low risk.", "impact": "warn", "reason": "An unproven planning route should stay visible while building control is being prepared.", "secondary_add": ["Planning decision, lawful development certificate or written route note if certainty matters."]},
                    {"value": "unclear", "label": "No, still unclear", "hint": "Planning permission may still be needed.", "impact": "danger", "reason": "A live planning problem can make technical approval premature if the design may need to change.", "primary_add": ["Pause before committing construction spend until the planning route is credible."], "links_add": [{"title": "Planning Route Planner", "href": "/tools/planning-route-planner/", "description": "Map the planning route before building-control work is locked in."}]},
                ],
            },
            {
                "id": "risk",
                "step_label": "Risk",
                "label": "Which technical risk is most live?",
                "help": "Pick the issue that would be most expensive to discover late.",
                "options": [
                    {"value": "minor", "label": "Mostly minor finishes", "hint": "Little structure, fire, drainage or services change.", "impact": "clear"},
                    {"value": "services", "label": "Services or certification", "hint": "Electrics, heating, windows, drainage or plumbing.", "impact": "warn", "reason": "Services often need either building control involvement or competent person certification.", "secondary_add": ["Installer details and certification route."]},
                    {"value": "structure", "label": "Structure or fire safety", "hint": "Openings, beams, floors, stairs, escape or fire separation.", "impact": "danger", "reason": "Structural and fire-safety work is rarely a good place to rely on informal assurance.", "primary_add": ["Full plans or early building control discussion is likely to be the safer route."], "secondary_add": ["Structural calculations, specifications and inspection plan."]},
                    {"value": "higher_risk", "label": "Higher-risk or unusual building", "hint": "Flats, multi-unit, tall, commercial or complex use.", "impact": "danger", "reason": "Higher-risk or unusual buildings can move the route away from ordinary domestic assumptions.", "primary_add": ["Do not rely on a simple householder route without specialist or official confirmation."]},
                ],
            },
            {
                "id": "evidence",
                "step_label": "Evidence",
                "label": "How strong will your evidence be at the end?",
                "help": "The goal is not just doing compliant work; it is being able to prove the route later.",
                "options": [
                    {"value": "clear", "label": "Clear certificate route", "hint": "You know who will issue completion or compliance evidence.", "impact": "clear"},
                    {"value": "uncertain", "label": "Not sure yet", "hint": "You do not know what certificate or sign-off will exist.", "impact": "warn", "reason": "Unclear completion evidence often becomes a problem later during sale, remortgage or insurance checks.", "next_add": ["Ask exactly what evidence will be issued and when."]},
                    {"value": "missing", "label": "Likely missing evidence", "hint": "There may be no inspection or certificate trail.", "impact": "danger", "reason": "Missing evidence is a practical risk even where the work itself looks neat.", "primary_add": ["Build an evidence pack now rather than trying to reconstruct the route later."], "links_add": [{"title": "Completion Certificates", "href": "/building-regulations/completion-certificates/", "description": "Use this to understand what proof should exist."}]},
                ],
            },
        ],
    },
    "project-requirements-generator": {
        "slug": "project-requirements-generator",
        "title": "Project Requirements Generator",
        "intro": "Build a practical planning prep pack for the kind of project you are shaping. This tool turns a few structured answers into the requirements, documents and next checks most likely to matter.",
        "status_copy": {
            "clear": {
                "label": "Lean prep pack",
                "tone": "good",
                "summary": "Nothing here points to the heaviest planning admin route yet, but you still have a clear shortlist of checks and documents worth preparing.",
            },
            "warn": {
                "label": "Standard prep pack",
                "tone": "warn",
                "summary": "The project has enough moving parts that a fuller planning prep pack is worth pulling together before you rely on the simpler route.",
            },
            "danger": {
                "label": "Fuller prep pack needed",
                "tone": "danger",
                "summary": "The answers point toward a more formal or sensitive route, so the safest move is to prepare the stronger evidence and consent checks early.",
            },
        },
        "section_labels": {
            "primary": "Requirements likely to matter",
            "secondary": "Documents worth preparing",
            "next": "What to do next",
        },
        "baseline_reason": "The project does not yet show the strongest signals for a heavy planning pack, but a smaller prep pack is still worthwhile.",
        "primary_items": [
            "Check the matching project guide before you rely on the pack.",
            "Building regulations may still matter even where the planning route stays simpler.",
        ],
        "secondary_items": [
            "Basic dimensions of the existing property and the proposed work.",
            "Photos of the site, street scene and the most sensitive edges of the proposal.",
        ],
        "next_checks": [
            "Use this pack to tighten the planning question before you commission detailed drawings.",
            "Move into the exact project guide or local authority page once the design is less hypothetical.",
            "Treat borderline answers as a prompt for measured drawings, not more guessing.",
        ],
        "links": [
            {"title": "Planning FAQ", "href": "/planning-faq/", "description": "Useful if the process itself still feels unclear."},
            {"title": "Local Authorities", "href": "/councils/", "description": "Open the council layer if heritage, Article 4 or local policy may tighten the route."},
        ],
        "questions": [
            {
                "id": "project",
                "step_label": "Project",
                "label": "Which project pack do you need?",
                "help": "Choose the closest live project so the checklist points to the right tripwires and documents.",
                "options": [
                    {
                        "value": "extension",
                        "label": "Extension",
                        "hint": "Rear, side, wraparound or general extension work.",
                        "impact": "clear",
                        "primary_add": [
                            "Extension size, height, depth and boundary checks are likely to matter.",
                        ],
                        "secondary_add": [
                            "A sketch or measured note showing the original rear or side wall and the proposed projection.",
                        ],
                        "links_add": [
                            {"title": "House Extensions", "href": "/house-extensions/", "description": "Use the wider extension guide once the pack is assembled."},
                            {"title": "Depth Limits", "href": "/depth-limits/", "description": "Helpful when projection from the original house is the main question."},
                        ],
                    },
                    {
                        "value": "loft",
                        "label": "Loft or roof project",
                        "hint": "Loft conversions, dormers, rooflights or roof changes.",
                        "impact": "clear",
                        "primary_add": [
                            "Roof change visibility, volume and front-facing alterations are likely to matter.",
                        ],
                        "secondary_add": [
                            "Roof photos and a simple note of any front-facing roof change.",
                        ],
                        "links_add": [
                            {"title": "Loft Conversions", "href": "/loft-conversions/", "description": "Use this for the wider loft route and volume checks."},
                            {"title": "Roof Alterations", "href": "/roof-alterations/", "description": "Helpful when the roof treatment itself is the blocker."},
                        ],
                    },
                    {
                        "value": "outbuilding",
                        "label": "Garden room or outbuilding",
                        "hint": "Garden rooms, sheds, annexes or detached buildings.",
                        "impact": "clear",
                        "primary_add": [
                            "Height, incidental use and boundary position are likely to matter.",
                        ],
                        "secondary_add": [
                            "A note of the intended use and the distance to the nearest boundary.",
                        ],
                        "links_add": [
                            {"title": "Garden Rooms", "href": "/garden-rooms/", "description": "Useful for detached garden buildings and studios."},
                            {"title": "Outbuildings", "href": "/outbuildings/", "description": "Open the wider detached-building guide."},
                        ],
                    },
                    {
                        "value": "garage",
                        "label": "Garage conversion",
                        "hint": "Internal garage conversions or cases with visible frontage change.",
                        "impact": "warn",
                        "reason": "Garage conversions often stay simple only if the frontage, parking and planning history all line up.",
                        "primary_add": [
                            "Planning history and parking conditions are likely to matter.",
                        ],
                        "secondary_add": [
                            "The original approval history and a note on how parking still works after conversion.",
                        ],
                        "links_add": [
                            {"title": "Garage Conversions", "href": "/garage-conversions/", "description": "Use this when frontage treatment or parking is the main issue."},
                        ],
                    },
                    {
                        "value": "driveway",
                        "label": "Driveway or access change",
                        "hint": "Driveways, front garden parking or dropped-kerb style work.",
                        "impact": "warn",
                        "reason": "Driveway projects often combine planning, drainage and highway-access checks.",
                        "primary_add": [
                            "Drainage, frontage treatment and highway approval are likely to matter.",
                        ],
                        "secondary_add": [
                            "A simple frontage plan showing parking layout, boundary treatment and drainage approach.",
                        ],
                        "links_add": [
                            {"title": "Driveways", "href": "/driveways/", "description": "Helpful for drainage and frontage rules."},
                            {"title": "Dropped Kerbs", "href": "/dropped-kerbs/", "description": "Useful when access onto the highway is part of the job."},
                        ],
                    },
                ],
            },
            {
                "id": "property",
                "step_label": "Property",
                "label": "What kind of property is it?",
                "help": "Property type often decides whether the simpler householder route is even available.",
                "options": [
                    {"value": "house", "label": "House", "hint": "Detached, semi-detached, terraced or bungalow.", "impact": "clear"},
                    {"value": "flat", "label": "Flat or maisonette", "hint": "External changes often sit on a stricter route than houses.", "impact": "danger", "reason": "Flats and maisonettes often do not benefit from the same householder permitted development route used by houses.", "primary_add": ["A formal planning route is more likely than a simple householder shortcut."], "secondary_add": ["Any lease, freeholder or estate-control documents that may affect the work."]},
                    {"value": "other", "label": "Other or not sure", "hint": "Use this for mixed or unusual cases.", "impact": "warn", "reason": "Where the property type is unclear, the safer assumption is that the simpler route may not apply cleanly.", "primary_add": ["Clarify the property type before relying on a quicker planning answer."]},
                ],
            },
            {
                "id": "sensitivity",
                "step_label": "Sensitivity",
                "label": "What local sensitivity is already known?",
                "help": "Sensitive sites usually need a stronger pack earlier in the process.",
                "options": [
                    {"value": "none", "label": "No known sensitivity", "hint": "No heritage or special local control is known.", "impact": "clear"},
                    {"value": "unsure", "label": "Not checked yet", "hint": "You still need to confirm the local layer.", "impact": "warn", "reason": "Unclear local designation status is enough to justify a more careful prep pack.", "primary_add": ["Confirm conservation area, listed building or Article 4 status before you rely on the simpler route."], "secondary_add": ["A council designation search or written check for the address."]},
                    {"value": "heritage", "label": "Heritage control", "hint": "Listed building or strong conservation-area sensitivity is in play.", "impact": "danger", "reason": "Heritage controls often add a stricter route, stronger drawings and more careful evidence requirements.", "primary_add": ["Heritage controls may add listed building consent or a tighter planning route."], "secondary_add": ["Photos of the affected elevation and any original features that could be altered."], "links_add": [{"title": "Listed Buildings", "href": "/listed-buildings/", "description": "Use this when heritage consent may sit alongside planning."}, {"title": "Conservation Areas", "href": "/conservation-areas/", "description": "Helpful where area character controls could tighten the response."}]},
                    {"value": "article4", "label": "Article 4 or local restriction", "hint": "A local direction or policy overlay is already known.", "impact": "danger", "reason": "An Article 4 direction or similar local restriction can remove the simpler route and force a fuller planning pack.", "primary_add": ["A local policy restriction may remove the simpler permitted development route."], "secondary_add": ["A written note or map showing the exact area covered by the local restriction."], "links_add": [{"title": "Article 4 Restrictions", "href": "/article-4/", "description": "Open this when local policy may override the normal route."}]},
                ],
            },
            {
                "id": "change",
                "step_label": "Change",
                "label": "How visible or consequential is the change?",
                "help": "The more visible the external change, the stronger the planning pack usually needs to be.",
                "options": [
                    {"value": "internal", "label": "Mostly internal or modest", "hint": "Little visible external change.", "impact": "clear"},
                    {"value": "external", "label": "Noticeable external change", "hint": "Visible from outside but still moderate.", "impact": "warn", "reason": "Visible external change often means the planning route depends more on drawings and local context.", "secondary_add": ["Existing and proposed elevation sketches or annotated photos."]},
                    {"value": "major", "label": "Major external change", "hint": "A larger visible change or obvious reshaping.", "impact": "danger", "reason": "A major visible change usually needs the fuller route and stronger supporting evidence.", "primary_add": ["Treat a more formal planning route as realistic until the detailed checks say otherwise."], "secondary_add": ["Measured existing and proposed elevations, plus a clearer site or block plan."]},
                    {"value": "highway", "label": "Access or highway change", "hint": "A driveway entrance, dropped kerb or road-facing access issue.", "impact": "danger", "reason": "Highway-facing change often pulls in an extra approval route alongside planning.", "primary_add": ["Highway approval or access consent may sit alongside planning."], "secondary_add": ["A frontage plan showing visibility, boundary treatment and vehicle movement."]},
                ],
            },
            {
                "id": "certainty",
                "step_label": "Certainty",
                "label": "How advanced is the information you have?",
                "help": "The thinner the information, the more your pack should focus on basic verification.",
                "options": [
                    {"value": "measured", "label": "Measured already", "hint": "You have reliable dimensions or early drawings.", "impact": "clear"},
                    {"value": "rough", "label": "Roughly known", "hint": "You know the broad shape but not the exact dimensions.", "impact": "warn", "reason": "Rough dimensions are enough for ideas, but not enough for confident planning decisions.", "secondary_add": ["A measured sketch or simple survey note to replace rough estimates."]},
                    {"value": "idea", "label": "Still only an idea", "hint": "You need the planning pack to shape the brief itself.", "impact": "warn", "reason": "Early-stage ideas still need a clear pack so the first design pass does not drift into the wrong route.", "secondary_add": ["A one-page brief covering size, use, priorities and the main unknowns."]},
                ],
            },
        ],
    },
    "site-constraint-checker": {
        "slug": "site-constraint-checker",
        "title": "Site Constraint Checker",
        "intro": "Use this tool to isolate the constraint most likely to block progress on a home project. It is built to tell you which rule family is active, what usually tightens it, and where to click next.",
        "status_copy": {
            "clear": {"label": "Low constraint signal", "tone": "good", "summary": "Nothing here points to multiple strong blockers yet, though one rule family still deserves a proper check before you rely on it."},
            "warn": {"label": "Borderline constraints", "tone": "warn", "summary": "The project is close enough to one or two live constraints that a single broad answer is likely to be unreliable."},
            "danger": {"label": "Multiple constraint signals", "tone": "danger", "summary": "Several constraints are stacking up, so the safest route is to isolate the main blocker with the detailed guides rather than rely on a shortcut."},
        },
        "section_labels": {
            "primary": "Constraints now in play",
            "secondary": "What usually tightens them",
            "next": "What to do next",
        },
        "baseline_reason": "The answers do not yet show the strongest stack of planning constraints, but one focused rule check is still worthwhile.",
        "primary_items": ["Treat the biggest visible constraint as the first thing to verify, not the last."],
        "secondary_items": ["Small measurement shifts, previous additions and local controls can all make a borderline answer feel much less simple."],
        "next_checks": [
            "Open the first rule page that matches the active constraint rather than reading a generic guide from the top.",
            "Use measured dimensions if the project is anywhere near a threshold.",
            "Escalate to the wider local authority layer when special controls or sensitive context are in play.",
        ],
        "links": [
            {"title": "Planning Decision Engine", "href": "/tools/planning-decision-tool/", "description": "Use this if the overall route still feels uncertain after isolating the constraint."},
        ],
        "questions": [
            {
                "id": "project",
                "step_label": "Project",
                "label": "Which project family is closest?",
                "help": "This helps the checker prefer the right constraint links and examples.",
                "options": [
                    {"value": "extension", "label": "Extension", "hint": "Rear, side, wraparound or similar extension work.", "impact": "clear", "links_add": [{"title": "House Extensions", "href": "/house-extensions/", "description": "Use the wider extension guide if the scheme is still broad."}]},
                    {"value": "loft", "label": "Loft or roof project", "hint": "Dormers, loft conversions or rooflights.", "impact": "clear", "links_add": [{"title": "Loft Conversions", "href": "/loft-conversions/", "description": "Open this if roof volume or roof visibility is driving the issue."}]},
                    {"value": "outbuilding", "label": "Garden room or outbuilding", "hint": "Detached building in the garden or side plot.", "impact": "clear", "links_add": [{"title": "Outbuildings", "href": "/outbuildings/", "description": "Useful when detached-building use or siting is the bigger question."}]},
                    {"value": "frontage", "label": "Frontage or access project", "hint": "Driveway, dropped kerb, porch, wall or gate style work.", "impact": "warn", "reason": "Frontage projects often bring planning, highway and design sensitivity together in one question.", "links_add": [{"title": "Driveways", "href": "/driveways/", "description": "Helpful when frontage treatment, parking or drainage is live."}]},
                ],
            },
            {
                "id": "pressure",
                "step_label": "Pressure",
                "label": "Which rule pressure feels strongest right now?",
                "help": "Pick the one most likely to change the answer first.",
                "options": [
                    {"value": "depth", "label": "Depth or projection", "hint": "How far the project extends or spreads.", "impact": "warn", "reason": "Depth and projection questions often decide whether the scheme stays on the simpler route.", "primary_add": ["Depth limits and original-wall measurements are active constraints."], "secondary_add": ["Projection from the original house or the effective spread across the plot."], "links_add": [{"title": "Depth Limits", "href": "/depth-limits/", "description": "Open this when projection is the main tripwire."}]},
                    {"value": "height", "label": "Height or bulk", "hint": "Vertical scale, ridge height or overall mass.", "impact": "warn", "reason": "Height and bulk questions are often enough to move a project from simple to borderline.", "primary_add": ["Height and overall bulk are active constraints."], "secondary_add": ["Maximum height from the correct ground level and any taller edge near a boundary."], "links_add": [{"title": "Height Limits", "href": "/height-limits/", "description": "Use this for the main height check."}, {"title": "Maximum Height", "href": "/maximum-height/", "description": "Helpful when the exact threshold is the live issue."}]},
                    {"value": "boundary", "label": "Boundary relationship", "hint": "Distance to the boundary or neighbour impact.", "impact": "warn", "reason": "Boundary position is one of the quickest ways for a project to stop feeling straightforward.", "primary_add": ["Boundary distance and neighbour impact are active constraints."], "secondary_add": ["The tightest edge of the scheme, not just the easiest distance to estimate."], "links_add": [{"title": "Boundary Rules", "href": "/boundary-rules/", "description": "Open this when boundary position is the main blocker."}, {"title": "Distance From Boundary", "href": "/distance-from-boundary/", "description": "Helpful when the exact gap matters."}]},
                    {"value": "roof", "label": "Roof or visible design change", "hint": "Dormers, rooflights, prominent reshaping or visible alteration.", "impact": "warn", "reason": "Visible roof or design changes are often where the simple route becomes unreliable.", "primary_add": ["Roof treatment or visible design change is an active constraint."], "secondary_add": ["How prominent the change is from the street or main viewpoints."], "links_add": [{"title": "Roof Alterations", "href": "/roof-alterations/", "description": "Use this when the roof treatment is the main issue."}]},
                    {"value": "frontage", "label": "Front-facing or highway sensitivity", "hint": "Street-facing change, vehicle access or visibility splays.", "impact": "danger", "reason": "Front-facing change or highway sensitivity usually needs a stricter check than a hidden rear alteration.", "primary_add": ["Front-facing change, access or highway visibility is an active constraint."], "secondary_add": ["How the work affects the principal elevation, frontage character or road safety."], "links_add": [{"title": "Planning Permission", "href": "/planning-permission/", "description": "Helpful when the visible route itself is the main issue."}]},
                ],
            },
            {
                "id": "sensitivity",
                "step_label": "Sensitivity",
                "label": "How sensitive is the site or area?",
                "help": "This decides whether the constraint should be treated as routine or stricter.",
                "options": [
                    {"value": "none", "label": "No known sensitivity", "hint": "No special local control is known.", "impact": "clear"},
                    {"value": "unsure", "label": "Not sure yet", "hint": "The local layer still needs checking.", "impact": "warn", "reason": "An unclear local sensitivity check is enough to make a borderline constraint more serious.", "secondary_add": ["Conservation area, listed building and Article 4 status for the address."]},
                    {"value": "heritage", "label": "Heritage-sensitive", "hint": "Conservation area or listed building issues are already known.", "impact": "danger", "reason": "Heritage sensitivity often means the visible constraint is judged much more strictly.", "primary_add": ["Heritage controls are now part of the active constraint stack."], "links_add": [{"title": "Conservation Areas", "href": "/conservation-areas/", "description": "Helpful where area character changes the answer."}, {"title": "Listed Buildings", "href": "/listed-buildings/", "description": "Use this when listed-building consent may be part of the route."}]},
                    {"value": "article4", "label": "Article 4 or local policy restriction", "hint": "A local restriction is already known.", "impact": "danger", "reason": "A local policy restriction can make a manageable-looking constraint much harder to rely on.", "primary_add": ["A local policy restriction is part of the active constraint stack."], "links_add": [{"title": "Article 4 Restrictions", "href": "/article-4/", "description": "Open this when local policy may override the shortcut."}]},
                ],
            },
            {
                "id": "position",
                "step_label": "Position",
                "label": "How tight is the sensitive edge of the project?",
                "help": "Think about the highest, widest or most visible part rather than the easiest corner to measure.",
                "options": [
                    {"value": "comfortable", "label": "Comfortable clearance", "hint": "There is clear room from boundaries or the highway.", "impact": "clear"},
                    {"value": "tight", "label": "Quite tight", "hint": "The proposal feels close in one or two places.", "impact": "warn", "reason": "A tighter position is often enough to make a live constraint more important."},
                    {"value": "very_tight", "label": "Very tight or right on it", "hint": "The sensitive edge is close to a boundary or highway.", "impact": "danger", "reason": "A very tight edge usually triggers the stricter version of the live constraint, not the easier one."},
                ],
            },
            {
                "id": "history",
                "step_label": "History",
                "label": "What do you know about previous additions or site history?",
                "help": "Previous works can make otherwise familiar constraint answers much less reliable.",
                "options": [
                    {"value": "none", "label": "No known complication", "hint": "No major previous changes are known.", "impact": "clear"},
                    {"value": "some", "label": "Some previous work", "hint": "The property has already been altered or extended.", "impact": "warn", "reason": "Previous additions can use up allowances or make the current constraint harder to read."},
                    {"value": "unsure", "label": "Not sure", "hint": "You still need the planning history check.", "impact": "warn", "reason": "Without planning history, a live constraint should be treated more cautiously."},
                ],
            },
        ],
    },
    "planning-route-planner": {
        "slug": "planning-route-planner",
        "title": "Planning Route Planner",
        "intro": "Use this tool to map the approval route most likely to matter before you spend time on the wrong application path. It is built to show whether the live route looks like permitted development, a formal application, a parallel consent or a mixed route that still needs checking.",
        "status_copy": {
            "clear": {"label": "Simpler route still plausible", "tone": "good", "summary": "The answers still leave room for a simpler route, but the supporting checks are worth lining up before you rely on it."},
            "warn": {"label": "Mixed route signals", "tone": "warn", "summary": "The project is no longer an obvious one-route answer, so it is sensible to keep both the simpler and formal paths in view."},
            "danger": {"label": "Formal route likely", "tone": "danger", "summary": "The answers point toward a fuller application or parallel-consent path, so that should be treated as the safer baseline for planning."},
        },
        "section_labels": {
            "primary": "Likely approval routes",
            "secondary": "Checks that often sit alongside the route",
            "next": "What to do next",
        },
        "baseline_reason": "Nothing here clearly rules out the simpler route yet, but the route still needs the supporting checks below.",
        "primary_items": ["Start with the route that fits the project today, not the one you hope will fit later."],
        "secondary_items": ["Building regulations can still run alongside planning rather than replacing it."],
        "next_checks": [
            "Use the route output to decide which guide, consent or council check to open next.",
            "Treat mixed-route answers as a prompt for clearer measurements and planning history review.",
            "Use a lawful development certificate only when the underlying permitted-development case still looks credible.",
        ],
        "links": [
            {"title": "Planning Decision Engine", "href": "/tools/planning-decision-tool/", "description": "Helpful when the overall route still feels unclear even after this planner."},
            {"title": "Do I Need Planning Permission?", "href": "/planning-faq/do-i-need-planning-permission/", "description": "Useful when the process question is still the main blocker."},
        ],
        "questions": [
            {
                "id": "project",
                "step_label": "Project",
                "label": "What kind of route are you planning for?",
                "help": "Choose the nearest project so the planner can bias toward the usual route families for that work.",
                "options": [
                    {"value": "extension", "label": "Extension", "hint": "Rear, side or wraparound householder extension.", "impact": "clear", "primary_add": ["A householder or permitted-development route is usually the first route to test for a house extension."], "links_add": [{"title": "House Extensions", "href": "/house-extensions/", "description": "Use this once you know the route still revolves around an extension."}]},
                    {"value": "loft", "label": "Loft or roof project", "hint": "Loft conversion, dormer or rooflight style project.", "impact": "clear", "primary_add": ["A loft or roof-change route is usually the first route to test, with front-facing changes checked carefully."], "links_add": [{"title": "Loft Conversions", "href": "/loft-conversions/", "description": "Open this if the route still revolves around the roof change."}]},
                    {"value": "outbuilding", "label": "Garden room or outbuilding", "hint": "Detached building or annexe-style project.", "impact": "warn", "reason": "Detached-building routes often split quickly between incidental use, annexe questions and formal permission.", "primary_add": ["An outbuilding permitted-development route may be live, but use and height often decide it."], "links_add": [{"title": "Outbuildings", "href": "/outbuildings/", "description": "Useful for the detached-building route."}]},
                    {"value": "garage", "label": "Garage conversion", "hint": "Mostly internal conversion with possible frontage change.", "impact": "warn", "reason": "Garage conversions often look simple until parking history or frontage change becomes part of the route.", "primary_add": ["A simpler route may still be possible, but planning history and frontage treatment need checking."], "links_add": [{"title": "Garage Conversions", "href": "/garage-conversions/", "description": "Open this if parking and frontage treatment are the main route questions."}]},
                    {"value": "driveway", "label": "Driveway or dropped kerb", "hint": "Frontage parking, hardstanding or highway-access work.", "impact": "danger", "reason": "Driveway and access projects often involve planning, drainage and highways rather than a single simple route.", "primary_add": ["A mixed planning, drainage and highway-consent route is realistic for frontage access work."], "links_add": [{"title": "Driveways", "href": "/driveways/", "description": "Helpful when drainage and frontage rules are central."}, {"title": "Dropped Kerbs", "href": "/dropped-kerbs/", "description": "Use this when highway access is part of the route."}]},
                ],
            },
            {
                "id": "property",
                "step_label": "Property",
                "label": "What kind of property is involved?",
                "help": "This is often the first thing that changes the route from simple to formal.",
                "options": [
                    {"value": "house", "label": "House", "hint": "Detached, semi-detached, terraced or bungalow.", "impact": "clear"},
                    {"value": "flat", "label": "Flat or maisonette", "hint": "External work often follows a tighter route.", "impact": "danger", "reason": "Flats and maisonettes often move the route toward formal permission rather than the normal householder shortcut.", "primary_add": ["Treat a formal planning route as more likely than a simple householder shortcut."], "secondary_add": ["Any estate, lease or freeholder controls that could run alongside planning."]},
                    {"value": "other", "label": "Other or not sure", "hint": "Use this for mixed or unusual cases.", "impact": "warn", "reason": "Where the property type is unclear, the safer assumption is that the route needs more checking."},
                ],
            },
            {
                "id": "baseline",
                "step_label": "Baseline",
                "label": "How much does the proposal rely on normal permitted development rights?",
                "help": "This usually decides whether the route planner should lean simple or formal.",
                "options": [
                    {"value": "strong_pd", "label": "Quite heavily", "hint": "The proposal only works if the simpler route holds up.", "impact": "warn", "reason": "Where the project depends heavily on permitted development, the supporting checks become much more important.", "primary_add": ["A lawful development certificate may be worth considering if certainty matters later."], "secondary_add": ["The exact measurements and planning history that support the permitted-development case."], "links_add": [{"title": "Permitted Development", "href": "/permitted-development/", "description": "Open this for the baseline rights behind the simpler route."}]},
                    {"value": "mixed", "label": "It could go either way", "hint": "You are keeping both PD and application routes in view.", "impact": "warn", "reason": "A mixed-route answer is usually a sign to keep the formal path in view rather than over-commit to the shortcut.", "primary_add": ["Keep both the simpler route and a formal application route in view until measurements and constraints are clearer."]},
                    {"value": "formal", "label": "Not much", "hint": "You already expect a fuller or formal route.", "impact": "danger", "reason": "If the project already looks formal, the safer baseline is to plan for that route from the start.", "primary_add": ["Treat a formal planning route as the safer baseline rather than a fallback."], "secondary_add": ["A fuller design pack and supporting drawings for the likely application route."]},
                ],
            },
            {
                "id": "parallel",
                "step_label": "Parallel",
                "label": "Which extra approval or parallel consent feels most likely?",
                "help": "Pick the one most likely to run alongside the main planning route.",
                "options": [
                    {"value": "none", "label": "None obvious", "hint": "No extra consent route is known yet.", "impact": "clear"},
                    {"value": "listed", "label": "Listed building consent", "hint": "Historic fabric or listed-building status is involved.", "impact": "danger", "reason": "Listed building consent often sits alongside or above the normal planning route.", "primary_add": ["Listed building consent may sit alongside planning rather than being optional."], "secondary_add": ["A clearer description of the affected historic fabric and visible change."], "links_add": [{"title": "Listed Buildings", "href": "/listed-buildings/", "description": "Open this when listed-building consent may be part of the route."}]},
                    {"value": "highway", "label": "Highway or access approval", "hint": "A dropped kerb, access change or visibility issue is involved.", "impact": "danger", "reason": "A highway-access issue often means the route is not just planning permission on its own.", "primary_add": ["Highway approval may be part of the live route, not just planning."], "secondary_add": ["A frontage or access sketch showing visibility and vehicle movement."], "links_add": [{"title": "Dropped Kerbs", "href": "/dropped-kerbs/", "description": "Useful when highway approval is likely to matter."}]},
                    {"value": "prior_approval", "label": "Prior approval", "hint": "The project may sit on a prior-approval style route.", "impact": "warn", "reason": "Prior approval is a distinct route and should not be treated as the same thing as a clean PD answer.", "primary_add": ["A prior approval route may be the live process rather than a simple permitted-development answer."]},
                ],
            },
            {
                "id": "sensitivity",
                "step_label": "Sensitivity",
                "label": "How sensitive is the site context?",
                "help": "Sensitive sites usually move the route away from the simplest answer.",
                "options": [
                    {"value": "none", "label": "No known sensitivity", "hint": "No special local control is known.", "impact": "clear"},
                    {"value": "unsure", "label": "Not checked yet", "hint": "You still need the local layer.", "impact": "warn", "reason": "An unconfirmed local sensitivity check is enough to keep the formal route in view."},
                    {"value": "article4", "label": "Article 4 or local policy restriction", "hint": "A local restriction is already known.", "impact": "danger", "reason": "A local policy restriction can remove the simpler route entirely.", "primary_add": ["A local policy restriction may remove the simpler route and push the scheme toward formal permission."], "links_add": [{"title": "Article 4 Restrictions", "href": "/article-4/", "description": "Open this when local policy may override the shortcut."}]},
                    {"value": "heritage", "label": "Heritage-sensitive site", "hint": "Conservation area or listed-building issues are in play.", "impact": "danger", "reason": "Heritage sensitivity often means the formal route is the safer planning baseline.", "primary_add": ["Heritage sensitivity means the formal route should stay on the table even if the project looks modest."], "links_add": [{"title": "Conservation Areas", "href": "/conservation-areas/", "description": "Helpful when heritage context could tighten the route."}]},
                ],
            },
        ],
    },
}


COMMERCIAL_TOOL_CONFIGS = {
    "lawful-development-certificate-checker": {
        "slug": "lawful-development-certificate-checker",
        "title": "Lawful Development Certificate Checker",
        "intro": "Check whether a lawful development certificate looks unnecessary, worth considering, or strongly worth a formal look before you rely on permitted development.",
        "analytics": {"start_event": "ldc_checker_start", "result_event": "ldc_checker_result"},
        "result_bands": {
            "clear": "probably-not-needed",
            "warn": "worth-considering",
            "danger": "strongly-consider-formal-check",
        },
        "status_copy": {
            "clear": {"label": "Probably not needed", "tone": "good", "summary": "The answers do not show a strong certificate signal yet. Keep the evidence together, but a certificate may be more than this stage needs."},
            "warn": {"label": "Worth considering", "tone": "warn", "summary": "There is enough uncertainty or future value in proof that an LDC is worth weighing before you spend much more."},
            "danger": {"label": "Strongly consider a formal check", "tone": "danger", "summary": "The project has enough risk, sensitivity or cost consequence that written confirmation may be the safer next move."},
        },
        "section_labels": {
            "primary": "Certificate signal",
            "secondary": "Evidence to gather",
            "next": "Best next checks",
        },
        "baseline_reason": "The project still looks like it may sit on the simpler route, but the evidence should be kept together in case certainty becomes useful later.",
        "primary_items": [
            "Keep the permitted-development route and measurements together.",
            "Do not use an LDC to rescue a proposal that already looks like it needs planning permission.",
        ],
        "secondary_items": [
            "Photos, rough dimensions and any planning-history notes.",
            "A clear note of the exact work you want written confirmation for.",
        ],
        "next_checks": [
            "Check whether local restrictions, property type or planning history change the normal route.",
            "Estimate the cost trade-off before choosing formal proof.",
        ],
        "links": [
            {"title": "Planning Cost Calculator", "href": "/tools/planning-cost-calculator/", "description": "Estimate the cost trade-off before choosing formal proof."},
            {"title": "Drawing Readiness Checker", "href": "/tools/drawings-cost-readiness-checker/", "description": "Check whether drawings are worth preparing yet."},
            {"title": "Permitted Development", "href": "/permitted-development/", "description": "Open the baseline route behind the certificate question."},
        ],
        "questions": [
            {
                "id": "project",
                "step_label": "Project",
                "label": "What kind of project are you checking?",
                "help": "An LDC is most useful when the project may be lawful without a full planning application but the evidence still matters.",
                "options": [
                    {"value": "extension", "label": "Extension", "hint": "Rear, side or wraparound style work.", "impact": "clear", "links_add": [{"title": "House Extensions", "href": "/house-extensions/", "description": "Use this for the extension baseline."}]},
                    {"value": "loft", "label": "Loft or roof work", "hint": "Dormer, rooflight or loft enlargement.", "impact": "clear", "links_add": [{"title": "Loft Conversions", "href": "/loft-conversions/", "description": "Use this for loft and roof checks."}]},
                    {"value": "outbuilding", "label": "Outbuilding or garden room", "hint": "Detached garden structure or studio.", "impact": "warn", "reason": "Outbuildings often turn on use, height and siting, so proof may be useful where money is being committed.", "primary_add": ["Use and siting evidence matter for an outbuilding LDC."], "links_add": [{"title": "Outbuildings", "href": "/outbuildings/", "description": "Use this for detached building checks."}]},
                    {"value": "change_of_use", "label": "Use or HMO question", "hint": "Change of use, HMO, annexe or mixed-use concern.", "impact": "danger", "reason": "Use and HMO questions are often too consequential to rely on a broad answer alone.", "primary_add": ["A formal route or certificate check may be important before relying on the use."], "links_add": [{"title": "Article 4 Restrictions", "href": "/article-4/", "description": "Check local restrictions where use or HMO status is live."}]},
                ],
            },
            {
                "id": "property",
                "step_label": "Property",
                "label": "What kind of property is involved?",
                "help": "Property type can decide whether normal householder permitted development rights are available.",
                "options": [
                    {"value": "house", "label": "House", "hint": "Detached, semi-detached, terraced or bungalow.", "impact": "clear"},
                    {"value": "flat", "label": "Flat or maisonette", "hint": "External work is usually stricter.", "impact": "danger", "reason": "Flats and maisonettes often do not use the same householder permitted development route as houses.", "primary_add": ["Do not assume the normal householder shortcut applies to external flat or maisonette work."]},
                    {"value": "unclear", "label": "Not sure", "hint": "The property status or planning unit is unclear.", "impact": "warn", "reason": "Unclear property status makes written confirmation more useful if the project moves ahead."},
                ],
            },
            {
                "id": "restrictions",
                "step_label": "Restrictions",
                "label": "Are any local or site restrictions known?",
                "help": "Local controls are one of the main reasons broad permitted-development answers become unreliable.",
                "options": [
                    {"value": "none", "label": "No known restrictions", "hint": "No conservation, listed or Article 4 issue known.", "impact": "clear"},
                    {"value": "not_checked", "label": "Not checked yet", "hint": "You have not checked the local layer.", "impact": "warn", "reason": "The local restriction layer should be checked before relying on a certificate decision.", "secondary_add": ["A council designation or Article 4 check for the address."]},
                    {"value": "conservation", "label": "Conservation area or heritage", "hint": "Heritage sensitivity may narrow the route.", "impact": "danger", "reason": "Heritage sensitivity can make simple-looking work need a stricter check.", "links_add": [{"title": "Conservation Areas", "href": "/conservation-areas/", "description": "Use this when heritage context may change the answer."}]},
                    {"value": "article4", "label": "Article 4 or local direction", "hint": "A local direction may remove rights.", "impact": "danger", "reason": "An Article 4 direction can remove the permitted-development footing an LDC would rely on.", "links_add": [{"title": "Article 4 Restrictions", "href": "/article-4/", "description": "Open this when local policy may override the shortcut."}]},
                ],
            },
            {
                "id": "certainty",
                "step_label": "Certainty",
                "label": "Why do you want certainty?",
                "help": "The certificate is usually more attractive when the cost of being wrong is meaningful.",
                "options": [
                    {"value": "curiosity", "label": "Mainly curiosity", "hint": "You are still exploring and not spending yet.", "impact": "clear"},
                    {"value": "before_spend", "label": "Before drawings or works", "hint": "You may spend soon if the route holds.", "impact": "warn", "reason": "Upcoming spend makes written certainty more useful than broad guidance alone.", "primary_add": ["Consider whether certificate cost is cheaper than wasted drawings or redesign."]},
                    {"value": "sale_or_lender", "label": "Sale, lender or future proof", "hint": "You may need evidence for someone else.", "impact": "danger", "reason": "Sale, lender or future-proofing needs are a strong reason to consider written evidence.", "primary_add": ["Formal proof can be more valuable where a future buyer, lender or conveyancer may ask for it."]},
                ],
            },
        ],
    },
    "planning-cost-calculator": {
        "slug": "planning-cost-calculator",
        "title": "Planning Cost Calculator",
        "intro": "Estimate a cautious planning cost band from the route, project and readiness signals before you commit to the next spend.",
        "analytics": {"start_event": "cost_calculator_start", "result_event": "cost_calculator_result"},
        "status_copy": {
            "clear": {"label": "Lean cost band", "tone": "good", "summary": "This still looks like an early, lower-admin route. Keep spending light until the route is confirmed."},
            "warn": {"label": "Standard cost band", "tone": "warn", "summary": "The route has enough moving parts that drawings, certificates or application preparation may become realistic costs."},
            "danger": {"label": "Higher prep cost likely", "tone": "danger", "summary": "The project is leaning toward a fuller formal route or specialist preparation, so budget should be treated more cautiously."},
        },
        "section_labels": {"primary": "Likely cost drivers", "secondary": "Budget notes", "next": "Spend in this order"},
        "baseline_reason": "The answers do not yet show the strongest formal route, so avoid heavy spend until the route is clearer.",
        "primary_items": ["Use this as a directional budget check, not a quote."],
        "secondary_items": ["Local fees, drawings, surveys and specialist reports can change the real cost."],
        "next_checks": ["Clarify the route before commissioning detailed drawings.", "Keep formal applications, LDCs and pre-app advice separate in the budget."],
        "links": [
            {"title": "Drawing Readiness Checker", "href": "/tools/drawings-cost-readiness-checker/", "description": "Check whether drawings should be the next spend."},
            {"title": "Planning Application Readiness Checker", "href": "/tools/planning-application-readiness-checker/", "description": "Use this if the formal route is likely."},
            {"title": "Planning Help", "href": "/planning-help/", "description": "Use this when the next spend needs professional support."},
        ],
        "questions": [
            {
                "id": "project",
                "step_label": "Project",
                "label": "Which project are you budgeting for?",
                "help": "Different projects bring different drawing, evidence and consent costs.",
                "options": [
                    {"value": "extension", "label": "Extension", "hint": "Rear, side or wraparound extension.", "impact": "warn", "reason": "Extensions often need drawings even when the route stays straightforward.", "links_add": [{"title": "House Extensions", "href": "/house-extensions/", "description": "Open the extension baseline."}]},
                    {"value": "loft", "label": "Loft or roof work", "hint": "Loft conversion, dormer or roof change.", "impact": "warn", "reason": "Loft and roof work often needs measured drawings before the route is comfortable.", "links_add": [{"title": "Loft Conversions", "href": "/loft-conversions/", "description": "Open the loft baseline."}]},
                    {"value": "outbuilding", "label": "Outbuilding or garden room", "hint": "Detached garden building.", "impact": "clear", "links_add": [{"title": "Outbuildings", "href": "/outbuildings/", "description": "Open the outbuilding baseline."}]},
                    {"value": "driveway", "label": "Driveway or access", "hint": "Hardstanding, drainage or dropped kerb.", "impact": "danger", "reason": "Access projects can combine planning, drainage and highway costs.", "links_add": [{"title": "Dropped Kerbs", "href": "/dropped-kerbs/", "description": "Use this when highway approval may matter."}]},
                ],
            },
            {
                "id": "route",
                "step_label": "Route",
                "label": "Which route looks most likely?",
                "help": "The route is usually the biggest cost driver.",
                "options": [
                    {"value": "reading", "label": "Still researching", "hint": "No drawings or application path yet.", "impact": "clear"},
                    {"value": "ldc", "label": "LDC or certificate", "hint": "Permitted development may work but proof may matter.", "impact": "warn", "reason": "Certificate routes usually need enough drawings and evidence to prove the point.", "links_add": [{"title": "LDC Checker", "href": "/tools/lawful-development-certificate-checker/", "description": "Check whether proof is worth it."}]},
                    {"value": "application", "label": "Planning application", "hint": "A formal application is realistic.", "impact": "danger", "reason": "Formal applications usually bring the strongest drawing and preparation costs.", "primary_add": ["Budget for application preparation rather than only a quick rule check."]},
                    {"value": "preapp", "label": "Pre-app or specialist input", "hint": "Risk, design or policy judgement is live.", "impact": "danger", "reason": "Pre-app or specialist support usually means the project is already beyond a lean route."},
                ],
            },
            {
                "id": "drawings",
                "step_label": "Drawings",
                "label": "What drawing stage are you at?",
                "help": "The less measured the project is, the more likely the next cost is basic evidence rather than submission work.",
                "options": [
                    {"value": "none", "label": "No drawings yet", "hint": "Only an idea or rough sketch.", "impact": "clear"},
                    {"value": "rough", "label": "Rough sketches", "hint": "Enough to explain, not enough to submit.", "impact": "warn", "reason": "Rough sketches can help triage, but may not be enough for a formal route."},
                    {"value": "measured", "label": "Measured drawings", "hint": "Drawings are already being prepared.", "impact": "warn"},
                    {"value": "specialist", "label": "Likely specialist drawings", "hint": "Heritage, highway or complex design evidence.", "impact": "danger", "reason": "Specialist evidence is a strong cost signal."},
                ],
            },
            {
                "id": "sensitivity",
                "step_label": "Sensitivity",
                "label": "How sensitive is the site?",
                "help": "Sensitive sites often add evidence and professional-preparation costs.",
                "options": [
                    {"value": "low", "label": "No known sensitivity", "hint": "No local restriction known.", "impact": "clear"},
                    {"value": "unsure", "label": "Not checked", "hint": "The local layer is still unknown.", "impact": "warn", "reason": "Unknown local sensitivity should be checked before budget confidence rises."},
                    {"value": "heritage", "label": "Heritage or Article 4", "hint": "Conservation, listed or local direction.", "impact": "danger", "reason": "Heritage and Article 4 issues can add drawings, statements or specialist judgement."},
                ],
            },
        ],
    },
    "drawings-cost-readiness-checker": {
        "slug": "drawings-cost-readiness-checker",
        "title": "Drawings Cost Readiness Checker",
        "intro": "Check whether paid drawings look premature, useful, or urgent for the route you are moving toward.",
        "analytics": {"start_event": "cost_calculator_start", "result_event": "cost_calculator_result"},
        "status_copy": {
            "clear": {"label": "Do not rush drawings yet", "tone": "good", "summary": "The project still has route or brief uncertainty. Keep drawings light until the core planning question is clearer."},
            "warn": {"label": "Drawings may be useful", "tone": "warn", "summary": "A measured sketch or early drawing pack could now help remove uncertainty and avoid circular research."},
            "danger": {"label": "Drawings likely needed", "tone": "danger", "summary": "The route or risk now depends on proper drawings, evidence or a professional brief rather than broad guidance alone."},
        },
        "section_labels": {"primary": "Drawing readiness", "secondary": "Brief gaps", "next": "Prepare before paying"},
        "baseline_reason": "The project still looks early enough that route clarity should come before full drawings.",
        "primary_items": ["Start with the lightest drawing package that answers the planning question."],
        "secondary_items": ["Photos, dimensions, site sensitivity and planning history help stop the brief drifting."],
        "next_checks": ["Check route and cost before commissioning detailed drawings.", "Use measured drawings when thresholds or formal submissions matter."],
        "links": [
            {"title": "Planning Cost Calculator", "href": "/tools/planning-cost-calculator/", "description": "Estimate the next spend."},
            {"title": "Project Requirements Generator", "href": "/tools/project-requirements-generator/", "description": "Turn the route into a prep pack."},
            {"title": "Planning Help", "href": "/planning-help/", "description": "Use this when professional support is likely."},
        ],
        "questions": [
            {
                "id": "project",
                "step_label": "Project",
                "label": "What are the drawings for?",
                "help": "The project type decides whether drawings are mostly explanatory or route-critical.",
                "options": [
                    {"value": "small", "label": "Small or internal change", "hint": "Mostly simple or exploratory.", "impact": "clear"},
                    {"value": "extension", "label": "Extension or loft", "hint": "Measured drawings may decide the route.", "impact": "warn", "reason": "Extensions and lofts often need measured drawings once thresholds matter."},
                    {"value": "formal", "label": "Formal application project", "hint": "Drawings are likely part of submission prep.", "impact": "danger", "reason": "A formal application usually needs a clearer drawing pack."},
                ],
            },
            {
                "id": "route",
                "step_label": "Route",
                "label": "How clear is the planning route?",
                "help": "Unclear routes are where drawings can either help or become premature spend.",
                "options": [
                    {"value": "unclear", "label": "Still unclear", "hint": "You do not know which route to design for.", "impact": "clear", "reason": "Route clarity should come before detailed drawings."},
                    {"value": "probably_pd", "label": "Probably permitted development", "hint": "Needs measurement support.", "impact": "warn", "reason": "Drawings may help prove the permitted-development case.", "links_add": [{"title": "LDC Checker", "href": "/tools/lawful-development-certificate-checker/", "description": "Check whether formal proof is worth it."}]},
                    {"value": "formal", "label": "Likely formal application", "hint": "A planning submission may be next.", "impact": "danger", "reason": "Formal routes usually need drawings that explain the design clearly."},
                ],
            },
            {
                "id": "measurements",
                "step_label": "Measurements",
                "label": "How reliable are the current measurements?",
                "help": "Drawing readiness depends on whether the measurements can carry the planning decision.",
                "options": [
                    {"value": "rough", "label": "Rough estimate only", "hint": "Enough for ideas, not decisions.", "impact": "clear"},
                    {"value": "some", "label": "Some measured notes", "hint": "Basic sizes are known.", "impact": "warn"},
                    {"value": "tight", "label": "Close to a limit", "hint": "One threshold decides the answer.", "impact": "danger", "reason": "Close thresholds usually need measured drawings before anyone should rely on the route."},
                ],
            },
            {
                "id": "sensitivity",
                "step_label": "Sensitivity",
                "label": "Is the site sensitive?",
                "help": "Sensitive sites often need drawings earlier because design judgement matters.",
                "options": [
                    {"value": "low", "label": "No known sensitivity", "hint": "No special local issue known.", "impact": "clear"},
                    {"value": "unknown", "label": "Not checked yet", "hint": "The local layer is unknown.", "impact": "warn", "reason": "Check local sensitivity before briefing drawings too tightly."},
                    {"value": "sensitive", "label": "Heritage, Article 4 or highway issue", "hint": "Design judgement or extra approval is live.", "impact": "danger", "reason": "Sensitive sites often need stronger drawings and evidence."},
                ],
            },
        ],
    },
    "planning-application-readiness-checker": {
        "slug": "planning-application-readiness-checker",
        "title": "Planning Application Readiness Checker",
        "intro": "Check whether a formal planning application looks ready to prepare or whether route, evidence and drawing gaps still need work.",
        "analytics": {"start_event": "application_readiness_start", "result_event": "application_readiness_result"},
        "status_copy": {
            "clear": {"label": "Not application-ready yet", "tone": "good", "summary": "The project still needs route clarity or basic evidence before it should be treated as an application pack."},
            "warn": {"label": "Partly ready", "tone": "warn", "summary": "The formal route may be realistic, but the pack still has gaps that could weaken the next stage."},
            "danger": {"label": "Prepare a fuller pack", "tone": "danger", "summary": "The project is close enough to submission-level decisions that drawings, evidence and professional preparation should be tightened."},
        },
        "section_labels": {"primary": "Readiness signal", "secondary": "Pack gaps", "next": "Before submission prep"},
        "baseline_reason": "The project does not yet show a strong application-readiness signal, so clarify the route before preparing a formal pack.",
        "primary_items": ["Treat a formal application as a preparation route, not just a form."],
        "secondary_items": ["Drawings, local context and design reasons should match the main risk."],
        "next_checks": ["Use refusal-risk and cost checks before committing to a weak application.", "Check local validation and evidence needs before submission."],
        "links": [
            {"title": "Planning Rejection Risk Analyzer", "href": "/tools/planning-rejection-risk-analyzer/", "description": "Pressure-test refusal risk before preparing the pack."},
            {"title": "Planning Cost Calculator", "href": "/tools/planning-cost-calculator/", "description": "Estimate the likely preparation spend."},
            {"title": "Planning Permission", "href": "/planning-permission/", "description": "Open the formal route baseline."},
        ],
        "questions": [
            {
                "id": "project",
                "step_label": "Project",
                "label": "What kind of application might this become?",
                "help": "The project type shapes the evidence and drawing pack.",
                "options": [
                    {"value": "householder", "label": "Householder project", "hint": "Extension, loft, outbuilding or similar.", "impact": "warn", "reason": "Householder applications still need clear drawings and local context."},
                    {"value": "access", "label": "Access or frontage", "hint": "Dropped kerb, driveway or highway-facing change.", "impact": "danger", "reason": "Access and frontage applications often need stronger highway and design evidence.", "links_add": [{"title": "Dropped Kerbs", "href": "/dropped-kerbs/", "description": "Use this for highway-facing routes."}]},
                    {"value": "heritage", "label": "Heritage-sensitive project", "hint": "Listed, conservation or prominent design issue.", "impact": "danger", "reason": "Heritage-sensitive projects usually need a stronger explanation of design impact.", "links_add": [{"title": "Conservation Areas", "href": "/conservation-areas/", "description": "Use this for heritage context."}]},
                ],
            },
            {
                "id": "route",
                "step_label": "Route",
                "label": "How settled is the formal route?",
                "help": "If the route is still mixed, the application pack may be premature.",
                "options": [
                    {"value": "mixed", "label": "Still mixed", "hint": "Could be PD, LDC, prior approval or application.", "impact": "clear", "reason": "Clarify the route before preparing a full application."},
                    {"value": "likely_application", "label": "Likely application", "hint": "A planning application is the working route.", "impact": "warn"},
                    {"value": "application_needed", "label": "Application needed", "hint": "You are preparing for submission.", "impact": "danger", "reason": "Once an application is likely, the pack needs to be built around evidence rather than broad guidance."},
                ],
            },
            {
                "id": "drawings",
                "step_label": "Drawings",
                "label": "What drawing evidence exists?",
                "help": "Application readiness usually fails when drawings are too thin for the decision being asked.",
                "options": [
                    {"value": "none", "label": "No drawings", "hint": "Only a concept or photos.", "impact": "clear"},
                    {"value": "early", "label": "Early sketches", "hint": "Enough to discuss, not enough to submit.", "impact": "warn", "reason": "Early sketches may need converting into a proper existing/proposed set."},
                    {"value": "measured", "label": "Measured existing and proposed", "hint": "A submission-style pack is possible.", "impact": "danger", "primary_add": ["Check whether the drawings answer the main local risk, not only the dimensions."]},
                ],
            },
            {
                "id": "evidence",
                "step_label": "Evidence",
                "label": "What evidence problem still feels weakest?",
                "help": "The weakest evidence point is usually what determines the next preparation step.",
                "options": [
                    {"value": "unknown", "label": "Not sure yet", "hint": "You have not isolated the weak point.", "impact": "clear"},
                    {"value": "neighbour", "label": "Neighbour or amenity impact", "hint": "Privacy, outlook, overbearing or noise.", "impact": "warn", "reason": "Amenity concerns should be addressed before application prep is treated as ready."},
                    {"value": "design_policy", "label": "Design, heritage or policy", "hint": "The decision may depend on judgement.", "impact": "danger", "reason": "Design, heritage and policy judgement usually need stronger explanation before submission."},
                    {"value": "highway", "label": "Highway or access", "hint": "Parking, visibility or access safety.", "impact": "danger", "reason": "Highway evidence can decide whether the application is credible."},
                ],
            },
        ],
    },
}

WORKFLOW_TOOL_CONFIGS = {
    "project-roadmap-builder": {
        "slug": "project-roadmap-builder",
        "title": "Project Roadmap Builder",
        "intro": "Build a staged route for the project so the next move is clear, saveable and easy to come back to.",
        "analytics": {"start_event": "workflow_start", "result_event": "workflow_completed"},
        "status_copy": {
            "clear": {"label": "Lean roadmap", "tone": "good", "summary": "The project can start with lighter checks before heavier preparation is useful."},
            "warn": {"label": "Standard roadmap", "tone": "warn", "summary": "The route has enough moving parts that saved tasks and evidence checks are worth using."},
            "danger": {"label": "Fuller roadmap", "tone": "danger", "summary": "The project is sensitive enough that local verification, evidence and formal-route decisions should come early."},
        },
        "section_labels": {"primary": "Roadmap stages", "secondary": "Evidence to gather", "next": "Next tasks"},
        "baseline_reason": "No single high-risk signal dominates yet, so the roadmap starts with route and local checks before paid preparation.",
        "primary_items": [
            "Start with the matching project guide and the rule most likely to decide the route.",
            "Check the council layer before relying on the national baseline.",
            "Decide whether proof, pre-app advice or a planning application is actually needed.",
        ],
        "secondary_items": [
            "Keep photos, rough dimensions and planning-history notes together.",
            "Save useful guide pages into My Planning Project as you work.",
        ],
        "next_checks": [
            "Save this roadmap to My Planning Project.",
            "Complete one local constraint check before commissioning drawings.",
            "Use the requirements generator once the route stops being hypothetical.",
        ],
        "links": [
            {"title": "My Planning Project", "href": "/my-planning-project/", "description": "Open the saved local workspace."},
            {"title": "Project Requirements Generator", "href": "/tools/project-requirements-generator/", "description": "Turn the route into a preparation pack."},
            {"title": "Local Authorities", "href": "/councils/", "description": "Check the local authority layer."},
        ],
        "questions": [
            {
                "id": "project",
                "step_label": "Project",
                "label": "What project needs a roadmap?",
                "help": "Choose the closest project so the roadmap can point to the right checks.",
                "options": [
                    {"value": "extension", "label": "Extension or loft", "hint": "House extension, side/rear extension or loft project.", "impact": "warn", "primary_add": ["Check depth, height, boundary and roof-change limits before drawings."], "links_add": [{"title": "House Extensions", "href": "/house-extensions/", "description": "Open the main extension route."}, {"title": "Loft Conversions", "href": "/loft-conversions/", "description": "Use this if roof space is the project."}]},
                    {"value": "garden", "label": "Garden room or outbuilding", "hint": "Detached structure, studio, shed or garden building.", "impact": "clear", "primary_add": ["Check height, siting, use and land coverage before assuming the route is simple."], "links_add": [{"title": "Garden Rooms", "href": "/garden-rooms/", "description": "Open the garden-room route."}]},
                    {"value": "access", "label": "Driveway or dropped kerb", "hint": "Access, hardstanding, frontage or highway-facing work.", "impact": "danger", "reason": "Access projects often involve highway approval alongside planning or drainage checks.", "primary_add": ["Separate the planning route from the highway or dropped-kerb route."], "links_add": [{"title": "Dropped Kerbs", "href": "/dropped-kerbs/", "description": "Open the highway-facing route."}]},
                    {"value": "hmo", "label": "HMO or change of use", "hint": "HMO, Article 4 or use-class uncertainty.", "impact": "danger", "reason": "HMO and change-of-use routes depend heavily on local policy and Article 4 coverage.", "primary_add": ["Check HMO, licensing and Article 4 sources for the exact authority."], "links_add": [{"title": "Article 4 And HMO By Council", "href": "/article-4-hmo-by-council/", "description": "Use the council reference route."}]},
                ],
            },
            {
                "id": "property",
                "step_label": "Property",
                "label": "Which property context applies?",
                "help": "Property type and sensitivity decide how cautious the roadmap should be.",
                "options": [
                    {"value": "ordinary_house", "label": "House, no known sensitivity", "hint": "No known local restriction yet.", "impact": "clear"},
                    {"value": "uncertain", "label": "Not checked yet", "hint": "You still need local designation or planning-history checks.", "impact": "warn", "reason": "Unknown local sensitivity should be checked before the route is trusted.", "secondary_add": ["Council designation and planning-history checks."]},
                    {"value": "sensitive", "label": "Sensitive or restricted", "hint": "Conservation, listed, Article 4, flat or condition risk.", "impact": "danger", "reason": "Sensitive context can remove shortcut assumptions and add consent routes.", "secondary_add": ["Official source check for each known restriction."]},
                ],
            },
            {
                "id": "stage",
                "step_label": "Stage",
                "label": "How far along is the project?",
                "help": "The roadmap changes depending on whether this is still an idea or already near paid preparation.",
                "options": [
                    {"value": "idea", "label": "Still an idea", "hint": "You need the route to shape the brief.", "impact": "clear", "next_add": ["Use the roadmap before commissioning any detailed drawings."]},
                    {"value": "rough", "label": "Rough design exists", "hint": "You have sketches or approximate dimensions.", "impact": "warn", "secondary_add": ["Measured notes for the limits most likely to decide the route."]},
                    {"value": "spend", "label": "About to spend", "hint": "Drawings, pre-app, LDC or application prep is close.", "impact": "danger", "reason": "Once spend is close, route uncertainty should be reduced before work is commissioned.", "next_add": ["Run the cost and readiness tools before committing to the next paid step."]},
                ],
            },
        ],
    },
    "planning-task-checklist-builder": {
        "slug": "planning-task-checklist-builder",
        "title": "Planning Task Checklist Builder",
        "intro": "Create a practical checklist of planning tasks that can be saved, printed and marked off later.",
        "analytics": {"start_event": "workflow_start", "result_event": "checklist_export"},
        "status_copy": {
            "clear": {"label": "Lean checklist", "tone": "good", "summary": "Start with route, local and measurement checks before heavier admin."},
            "warn": {"label": "Working checklist", "tone": "warn", "summary": "The project has enough uncertainty to benefit from a structured task list."},
            "danger": {"label": "Full checklist", "tone": "danger", "summary": "The answers point toward formal, sensitive or multi-consent tasks that should be tracked carefully."},
        },
        "section_labels": {"primary": "Tasks to add", "secondary": "Checks to record", "next": "How to use the checklist"},
        "baseline_reason": "The checklist begins with the basic route and local checks because no heavier trigger has dominated yet.",
        "primary_items": ["Identify the most relevant project guide.", "Check local council context.", "Record measurements and assumptions."],
        "secondary_items": ["Saved guide URLs, notes and project assumptions.", "Photos, measurements and official-source checks."],
        "next_checks": ["Save this checklist to My Planning Project.", "Mark one task complete before adding another paid step.", "Print or copy the checklist for a designer or adviser."],
        "links": [
            {"title": "My Planning Project", "href": "/my-planning-project/", "description": "Open saved tasks."},
            {"title": "Planning Application Readiness Checker", "href": "/tools/planning-application-readiness-checker/", "description": "Use this if the checklist points formal."},
        ],
        "questions": [
            {
                "id": "project",
                "step_label": "Project",
                "label": "Which checklist do you need?",
                "help": "Pick the closest project family.",
                "options": [
                    {"value": "extension", "label": "Extension or loft", "hint": "Extension, loft or roof work.", "impact": "warn", "primary_add": ["Measure depth, height, boundaries and roof changes."], "links_add": [{"title": "House Extensions", "href": "/house-extensions/", "description": "Use the extension guide."}]},
                    {"value": "garden", "label": "Garden room or outbuilding", "hint": "Garden room, shed, studio or outbuilding.", "impact": "clear", "primary_add": ["Record intended use, height and distance to boundary."], "links_add": [{"title": "Outbuildings", "href": "/outbuildings/", "description": "Use the detached building guide."}]},
                    {"value": "dropped", "label": "Dropped kerb or driveway", "hint": "Access, parking, frontage or hardstanding.", "impact": "danger", "reason": "Highway, drainage and planning tasks need separating.", "primary_add": ["Check highway process, drainage and frontage design separately."], "links_add": [{"title": "Dropped Kerbs", "href": "/dropped-kerbs/", "description": "Use the dropped-kerb guide."}]},
                    {"value": "hmo", "label": "HMO or conservation issue", "hint": "HMO, Article 4, conservation or listed context.", "impact": "danger", "reason": "Sensitive routes need official-source checks early.", "primary_add": ["Check Article 4, conservation or listed-building status before relying on the shortcut."], "links_add": [{"title": "Local Constraint Finder", "href": "/tools/local-constraint-finder/", "description": "Find the local constraint first."}]},
                ],
            },
            {
                "id": "route",
                "step_label": "Route",
                "label": "What route does it look like?",
                "help": "The route determines the next task type.",
                "options": [
                    {"value": "unknown", "label": "Unknown", "hint": "Still researching.", "impact": "clear"},
                    {"value": "pd", "label": "May be PD", "hint": "Permitted development might work.", "impact": "warn", "primary_add": ["Decide whether an LDC is worth considering."], "links_add": [{"title": "LDC Checker", "href": "/tools/lawful-development-certificate-checker/", "description": "Check if proof is worth it."}]},
                    {"value": "formal", "label": "Likely formal", "hint": "Application, pre-app or specialist help likely.", "impact": "danger", "reason": "Formal routes need drawings and evidence tasks earlier.", "primary_add": ["Prepare application readiness and evidence tasks."]},
                ],
            },
            {
                "id": "evidence",
                "step_label": "Evidence",
                "label": "How complete is the evidence?",
                "help": "This decides whether the checklist should focus on gathering facts or moving to preparation.",
                "options": [
                    {"value": "thin", "label": "Very thin", "hint": "Few measurements or photos.", "impact": "clear", "secondary_add": ["Photos and basic measured notes."]},
                    {"value": "some", "label": "Some evidence", "hint": "Rough notes or sketches exist.", "impact": "warn", "secondary_add": ["Convert rough assumptions into measured notes."]},
                    {"value": "ready", "label": "Nearly ready", "hint": "Drawings or formal prep may be next.", "impact": "danger", "reason": "Near-ready projects need a final readiness check before submission-style spend.", "links_add": [{"title": "Application Readiness Checker", "href": "/tools/planning-application-readiness-checker/", "description": "Check the formal pack."}]},
                ],
            },
        ],
    },
    "evidence-pack-builder": {
        "slug": "evidence-pack-builder",
        "title": "Evidence Pack Builder",
        "intro": "Build the evidence list most likely to reduce planning uncertainty before drawings, applications or help requests.",
        "analytics": {"start_event": "workflow_start", "result_event": "workflow_completed"},
        "status_copy": {
            "clear": {"label": "Basic evidence pack", "tone": "good", "summary": "A light evidence pack should be enough for the next research step."},
            "warn": {"label": "Measured evidence pack", "tone": "warn", "summary": "The project needs clearer measurements or official checks before confidence rises."},
            "danger": {"label": "Formal evidence pack", "tone": "danger", "summary": "The project is sensitive enough that stronger drawings, official checks or specialist notes may be needed."},
        },
        "section_labels": {"primary": "Evidence to gather", "secondary": "Official checks", "next": "Before spending more"},
        "baseline_reason": "The route is not yet showing the strongest evidence demand, so start with photos and dimensions.",
        "primary_items": ["Current photos from street, neighbour-facing and project-facing angles.", "Basic measured dimensions of the proposed change."],
        "secondary_items": ["Council designation check and planning-history note if uncertainty remains."],
        "next_checks": ["Save the pack and gather evidence before commissioning detailed drawings.", "Use readiness tools once the pack is no longer thin."],
        "links": [
            {"title": "Drawing Readiness Checker", "href": "/tools/drawings-cost-readiness-checker/", "description": "Check whether drawings are useful now."},
            {"title": "Local Authorities", "href": "/councils/", "description": "Use official local sources."},
        ],
        "questions": [
            {
                "id": "project",
                "step_label": "Project",
                "label": "What evidence pack is this for?",
                "help": "Different projects need different proof.",
                "options": [
                    {"value": "extension", "label": "Extension or loft", "hint": "Dimensions and drawings matter.", "impact": "warn", "primary_add": ["Existing and proposed depth, height, roof and boundary dimensions."]},
                    {"value": "garden", "label": "Garden building", "hint": "Use, height and siting matter.", "impact": "clear", "primary_add": ["Intended use note, eaves height, overall height and boundary distance."]},
                    {"value": "access", "label": "Driveway or access", "hint": "Highway and drainage matter.", "impact": "danger", "reason": "Access projects often need frontage, drainage and highway evidence.", "primary_add": ["Frontage photos, parking layout, drainage approach and highway-access notes."]},
                    {"value": "heritage", "label": "Heritage or HMO", "hint": "Official local checks matter.", "impact": "danger", "reason": "Sensitive or use-based projects need official-source evidence earlier.", "secondary_add": ["Article 4, conservation, listed building, HMO or licensing source notes."]},
                ],
            },
            {
                "id": "sensitivity",
                "step_label": "Sensitivity",
                "label": "What local issue is possible?",
                "help": "This controls how strong the evidence pack should be.",
                "options": [
                    {"value": "none", "label": "None known", "hint": "No special control identified.", "impact": "clear"},
                    {"value": "unknown", "label": "Not checked", "hint": "Local layer still unknown.", "impact": "warn", "reason": "Unknown local status should be checked before relying on the pack.", "secondary_add": ["Council map or designation search."]},
                    {"value": "sensitive", "label": "Known sensitivity", "hint": "Conservation, listed, Article 4, highway or HMO issue.", "impact": "danger", "reason": "Known sensitivity makes official evidence more important.", "secondary_add": ["Screenshots or notes from official source pages."]},
                ],
            },
            {
                "id": "stage",
                "step_label": "Stage",
                "label": "What evidence exists already?",
                "help": "Choose the current evidence strength.",
                "options": [
                    {"value": "none", "label": "Almost none", "hint": "Only an idea.", "impact": "clear"},
                    {"value": "rough", "label": "Rough notes", "hint": "Some photos or sketch dimensions.", "impact": "warn", "secondary_add": ["Replace estimates with measured notes."]},
                    {"value": "drawings", "label": "Drawings or application prep", "hint": "Formal preparation is close.", "impact": "danger", "reason": "Formal preparation should be checked against the main local risk.", "next_add": ["Run application readiness before submission-style work."]},
                ],
            },
        ],
    },
    "local-constraint-finder": {
        "slug": "local-constraint-finder",
        "title": "Local Constraint Finder",
        "intro": "Identify the local constraint families most likely to change the planning route before relying on a national rule.",
        "analytics": {"start_event": "workflow_start", "result_event": "workflow_completed"},
        "status_copy": {
            "clear": {"label": "Low local constraint signal", "tone": "good", "summary": "No strong local constraint is obvious yet, but council checks still matter before work starts."},
            "warn": {"label": "Constraint check needed", "tone": "warn", "summary": "One or more local checks could change the answer and should be verified."},
            "danger": {"label": "Strong local constraint signal", "tone": "danger", "summary": "The project may depend on local controls, so official source checks should come before route confidence."},
        },
        "section_labels": {"primary": "Constraints to check", "secondary": "Official-source notes", "next": "Next local moves"},
        "baseline_reason": "No strong local constraint has been selected, so start with the council guide and project page.",
        "primary_items": ["Check the council page for local planning context.", "Check whether any special designation applies to the exact property."],
        "secondary_items": ["Use official council maps, designation pages and planning records where possible."],
        "next_checks": ["Save the constraint list.", "Open the council page before relying on project guidance.", "Escalate if the shortcut depends on no local control applying."],
        "links": [
            {"title": "Local Authorities", "href": "/councils/", "description": "Find the council layer."},
            {"title": "Article 4", "href": "/article-4/", "description": "Check local direction risk."},
            {"title": "Conservation Areas", "href": "/conservation-areas/", "description": "Check heritage area risk."},
        ],
        "questions": [
            {
                "id": "project",
                "step_label": "Project",
                "label": "Which project is being checked?",
                "help": "The likely constraint depends on project type.",
                "options": [
                    {"value": "householder", "label": "Extension, loft or outbuilding", "hint": "Householder-style project.", "impact": "warn", "primary_add": ["Check conservation area, Article 4, listed status and previous conditions."]},
                    {"value": "frontage", "label": "Driveway, fence or dropped kerb", "hint": "Street-facing or highway-side project.", "impact": "danger", "reason": "Frontage projects can combine design, highway and drainage constraints.", "primary_add": ["Check highway, drainage, visibility and front-boundary controls."]},
                    {"value": "hmo", "label": "HMO or change of use", "hint": "Use class, licensing or Article 4 issue.", "impact": "danger", "reason": "HMO routes are strongly local and may depend on Article 4 coverage.", "primary_add": ["Check HMO licensing, Article 4 and local policy concentration."]},
                ],
            },
            {
                "id": "known",
                "step_label": "Known risk",
                "label": "What local risk is already known?",
                "help": "Select the strongest known risk.",
                "options": [
                    {"value": "none", "label": "None known", "hint": "No local issue identified.", "impact": "clear"},
                    {"value": "unknown", "label": "Not checked", "hint": "Local layer is still unknown.", "impact": "warn", "reason": "Unknown local designation status is itself a constraint to resolve."},
                    {"value": "heritage", "label": "Conservation or listed", "hint": "Heritage control may apply.", "impact": "danger", "reason": "Heritage controls can add consent or restrict visible change.", "links_add": [{"title": "Listed Buildings", "href": "/listed-buildings/", "description": "Check listed building consent."}]},
                    {"value": "article4", "label": "Article 4 or condition", "hint": "Local direction or planning condition possible.", "impact": "danger", "reason": "Article 4 or planning conditions can remove normal assumptions."},
                ],
            },
            {
                "id": "certainty",
                "step_label": "Certainty",
                "label": "How confident are you in the council source?",
                "help": "Use this to decide whether the next step is research or formal confirmation.",
                "options": [
                    {"value": "not_found", "label": "Not found yet", "hint": "No official source checked.", "impact": "warn", "secondary_add": ["Find the council designation page or planning record."]},
                    {"value": "seen", "label": "Source found", "hint": "Official page seen but not property-specific.", "impact": "warn", "secondary_add": ["Record the source URL and what it does not settle."]},
                    {"value": "property_specific", "label": "Property-specific check needed", "hint": "Exact address decides the answer.", "impact": "danger", "reason": "Property-specific uncertainty should not be settled by a broad guide."},
                ],
            },
        ],
    },
    "planning-timeline-planner": {
        "slug": "planning-timeline-planner",
        "title": "Planning Timeline Planner",
        "intro": "Plan the order of route checks, evidence gathering, drawings, certificates, applications and help conversations.",
        "analytics": {"start_event": "workflow_start", "result_event": "workflow_completed"},
        "status_copy": {
            "clear": {"label": "Light timeline", "tone": "good", "summary": "The next stage can stay light while route and local checks are clarified."},
            "warn": {"label": "Standard timeline", "tone": "warn", "summary": "The project may need measured evidence, proof or readiness checks before the next spend."},
            "danger": {"label": "Formal timeline", "tone": "danger", "summary": "The timeline should allow for stronger evidence, formal routes or specialist input."},
        },
        "section_labels": {"primary": "Likely sequence", "secondary": "Timing notes", "next": "Before the next step"},
        "baseline_reason": "The project still looks early enough that route clarity should come before a heavy timeline.",
        "primary_items": ["Confirm project route.", "Check local constraints.", "Gather evidence before paid preparation."],
        "secondary_items": ["Exact timing depends on council process, drawings and specialist evidence."],
        "next_checks": ["Save the timeline.", "Avoid paying for detailed drawings until the route and local risks are clearer."],
        "links": [
            {"title": "Planning Cost Calculator", "href": "/tools/planning-cost-calculator/", "description": "Estimate route spend."},
            {"title": "Planning Application Readiness Checker", "href": "/tools/planning-application-readiness-checker/", "description": "Check formal readiness."},
        ],
        "questions": [
            {
                "id": "route",
                "step_label": "Route",
                "label": "Which route seems most likely?",
                "help": "The route determines the timing sequence.",
                "options": [
                    {"value": "research", "label": "Still researching", "hint": "No clear route yet.", "impact": "clear"},
                    {"value": "ldc", "label": "May need LDC", "hint": "PD possible but proof may matter.", "impact": "warn", "primary_add": ["Allow time for measured drawings and formal proof if certainty matters."], "links_add": [{"title": "LDC Checker", "href": "/tools/lawful-development-certificate-checker/", "description": "Check whether proof is worth it."}]},
                    {"value": "application", "label": "Likely application", "hint": "Formal planning route realistic.", "impact": "danger", "reason": "Applications need stronger drawing and evidence sequencing.", "primary_add": ["Plan evidence, drawings, validation checks and possible design revisions."]},
                    {"value": "highway", "label": "Highway or mixed consent", "hint": "Dropped kerb, listed building, heritage or access route.", "impact": "danger", "reason": "Mixed routes often have parallel consent timelines.", "primary_add": ["Separate planning, highway, listed-building or specialist consent timing."]},
                ],
            },
            {
                "id": "evidence",
                "step_label": "Evidence",
                "label": "What stage is the evidence at?",
                "help": "Evidence strength decides what should happen before the clock starts.",
                "options": [
                    {"value": "idea", "label": "Idea only", "hint": "No proper evidence yet.", "impact": "clear"},
                    {"value": "rough", "label": "Rough evidence", "hint": "Photos, notes or sketches.", "impact": "warn", "secondary_add": ["Use measured notes before relying on close thresholds."]},
                    {"value": "drawings", "label": "Drawings underway", "hint": "Formal prep may be close.", "impact": "danger", "reason": "Once drawings are underway, route mistakes become more expensive."},
                ],
            },
            {
                "id": "sensitivity",
                "step_label": "Sensitivity",
                "label": "How sensitive is the project?",
                "help": "Sensitive projects usually need more time for checks and revisions.",
                "options": [
                    {"value": "low", "label": "Low sensitivity", "hint": "No known local issue.", "impact": "clear"},
                    {"value": "unknown", "label": "Unknown", "hint": "Local layer not checked.", "impact": "warn", "reason": "Unknown local sensitivity should be resolved before timing confidence rises."},
                    {"value": "high", "label": "High sensitivity", "hint": "Heritage, Article 4, HMO, highway or refusal risk.", "impact": "danger", "reason": "Sensitive routes may need pre-app, specialist evidence or redesign time."},
                ],
            },
        ],
    },
}

CUSTOM_TOOL_CONFIGS.update(COMMERCIAL_TOOL_CONFIGS)
CUSTOM_TOOL_CONFIGS.update(WORKFLOW_TOOL_CONFIGS)


def build_custom_tool_config(tool_slug: str) -> dict:
    config = deepcopy(CUSTOM_TOOL_CONFIGS[tool_slug])
    config["links"] = filter_live_dict_links(config.get("links", []))

    for question in config.get("questions", []):
        for option in question.get("options", []):
            option["links_add"] = filter_live_dict_links(option.get("links_add", []))

    return config
