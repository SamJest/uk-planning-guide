from copy import deepcopy

from data.planning_decision_engine import DECISION_ENGINE_CONFIG


PROJECTS_BY_ID = {
    project["id"]: deepcopy(project)
    for project in DECISION_ENGINE_CONFIG["projects"]
}


RISK_FACTORS = {
    "baseline_detailing": {
        "title": "No major refusal trigger identified",
        "explanation": "These answers do not point to a strong refusal signal on their own, but drawing quality, materials, scale and neighbour impact still need to be handled well.",
        "reduction_tips": [
            "Use accurate drawings that clearly show the relationship to the existing house.",
            "Keep the design visually tidy and proportionate rather than relying on vague sketches.",
        ],
        "links": [
            {"title": "Planning Permission", "href": "/planning-permission/", "description": "Use the main planning hub if you want the wider application context."},
        ],
    },
    "scale_bulk": {
        "title": "Scale and bulk",
        "explanation": "Councils often resist schemes that look too deep, too wide or too dominant for the host property and plot.",
        "reduction_tips": [
            "Reduce the depth, width or visual mass before submitting.",
            "Break up the form so the extension reads as subordinate to the original building.",
        ],
        "links": [
            {"title": "House Extensions", "href": "/house-extensions/", "description": "Useful for wider guidance on keeping extensions proportionate."},
            {"title": "Planning Permission", "href": "/planning-permission/", "description": "Helpful when bulk is pushing the scheme into a formal application route."},
        ],
    },
    "height_mass": {
        "title": "Height and visual dominance",
        "explanation": "Excessive height can make a proposal look overbearing or out of scale, especially near neighbours or on visible elevations.",
        "reduction_tips": [
            "Lower the ridge or eaves height if the scheme feels dominant.",
            "Keep taller elements away from boundaries where possible.",
        ],
        "links": [
            {"title": "Height Limits", "href": "/height-limits/", "description": "Useful when vertical scale is the key issue."},
            {"title": "Maximum Height", "href": "/maximum-height/", "description": "Helpful if the project is close to a height threshold."},
        ],
    },
    "overshadowing_daylight": {
        "title": "Loss of light and overshadowing",
        "explanation": "Taller or deeper forms near a boundary can trigger neighbour objections around daylight, overshadowing and sense of enclosure.",
        "reduction_tips": [
            "Pull the proposal away from the boundary or reduce the higher parts.",
            "Use a lower eaves line or stepped form on the most sensitive edge.",
        ],
        "links": [
            {"title": "Boundary Rules", "href": "/boundary-rules/", "description": "A strong next read when the neighbour relationship is the key concern."},
            {"title": "Distance From Boundary", "href": "/distance-from-boundary/", "description": "Helpful when siting is driving the refusal risk."},
        ],
    },
    "overlooking_privacy": {
        "title": "Overlooking and privacy",
        "explanation": "Councils often scrutinise new windows, raised views and roof changes that could create direct overlooking into neighbouring homes or gardens.",
        "reduction_tips": [
            "Reposition or reduce windows on sensitive elevations.",
            "Consider obscure glazing or a revised layout where overlooking is obvious.",
        ],
        "links": [
            {"title": "Roof Alterations", "href": "/roof-alterations/", "description": "Useful when dormers or roof windows are creating privacy concerns."},
            {"title": "Planning Permission", "href": "/planning-permission/", "description": "Helpful for the wider planning balance around neighbour impact."},
        ],
    },
    "street_scene_character": {
        "title": "Street scene and character impact",
        "explanation": "Schemes that sit prominently on the front or side elevation can be refused if they look awkward, overly bulky or out of character with the street.",
        "reduction_tips": [
            "Keep additions visually subordinate to the original building.",
            "Use a form, roofline and material palette that fit the existing street pattern.",
        ],
        "links": [
            {"title": "Planning Permission", "href": "/planning-permission/", "description": "Useful when design character is the real application issue."},
            {"title": "House Extensions", "href": "/house-extensions/", "description": "Helpful for wider extension design context."},
        ],
    },
    "roof_design": {
        "title": "Roof design and visual impact",
        "explanation": "Large dormers, roof raises and front-facing roof changes often draw design objections if they look bulky or visually intrusive.",
        "reduction_tips": [
            "Reduce the size of the roof enlargement or keep it away from the front slope.",
            "Aim for a roof form that looks clearly secondary to the original house.",
        ],
        "links": [
            {"title": "Loft Conversions", "href": "/loft-conversions/", "description": "Main guide for roof enlargements and loft schemes."},
            {"title": "Roof Alterations", "href": "/roof-alterations/", "description": "Useful when the roof treatment is the refusal risk."},
        ],
    },
    "heritage_policy": {
        "title": "Heritage or local policy constraints",
        "explanation": "Conservation areas, listed buildings and Article 4 directions can make councils much less tolerant of visible change or loss of original character.",
        "reduction_tips": [
            "Check the heritage or local policy layer before finalising the design.",
            "Use a simpler, less visually assertive design in sensitive areas.",
        ],
        "links": [
            {"title": "Conservation Areas", "href": "/conservation-areas/", "description": "Helpful if the site is in a conservation area."},
            {"title": "Listed Buildings", "href": "/listed-buildings/", "description": "Open this when heritage controls are likely to dominate the decision."},
            {"title": "Article 4 Restrictions", "href": "/article-4/", "description": "Useful where local directions may tighten the route."},
        ],
    },
    "residential_intensity": {
        "title": "Use intensity and residential character",
        "explanation": "A building that starts to function as separate living space can trigger stronger policy scrutiny than a clearly incidental domestic structure.",
        "reduction_tips": [
            "Keep the use clearly incidental to the main house if that is the intended route.",
            "Avoid layouts and facilities that make the building read as separate accommodation unless the application is designed for that use.",
        ],
        "links": [
            {"title": "Garden Rooms", "href": "/garden-rooms/", "description": "Useful when a detached garden building is the project type."},
            {"title": "Outbuildings", "href": "/outbuildings/", "description": "Helpful for wider outbuilding policy context."},
        ],
    },
    "parking_access": {
        "title": "Parking and access pressure",
        "explanation": "Loss of parking or awkward vehicle access can become a refusal risk where local policy expects a practical parking arrangement to remain.",
        "reduction_tips": [
            "Show clearly how parking and manoeuvring will still work after the change.",
            "Check the planning history for conditions tied to parking or garage retention.",
        ],
        "links": [
            {"title": "Garage Conversions", "href": "/garage-conversions/", "description": "Useful where parking loss is tied to a garage conversion."},
            {"title": "Local Authorities", "href": "/councils/", "description": "Helpful when council parking expectations may vary locally."},
        ],
    },
    "drainage_surface": {
        "title": "Drainage and surfacing",
        "explanation": "Front garden surfacing can run into planning objections if drainage is unresolved or the design pushes water toward the road.",
        "reduction_tips": [
            "Use a permeable surface or a clear soakaway strategy within the site.",
            "Separate the drainage design from any dropped kerb or highway question and show both clearly.",
        ],
        "links": [
            {"title": "Driveways", "href": "/driveways/", "description": "Useful for front garden surfacing and drainage issues."},
            {"title": "Dropped Kerbs", "href": "/dropped-kerbs/", "description": "Open this if the project also needs a new highway crossover."},
        ],
    },
    "boundary_enclosure": {
        "title": "Boundary enclosure and visibility",
        "explanation": "Tall walls, fences and gates can be resisted where they create an overly enclosed frontage or harm visibility beside a road.",
        "reduction_tips": [
            "Lower the boundary treatment if it looks dominant from the street.",
            "Check carefully whether the boundary fronts a road, footpath or highway corner.",
        ],
        "links": [
            {"title": "Fences and Walls", "href": "/fences-and-walls/", "description": "Main guide for boundary structure proposals."},
            {"title": "Boundary Rules", "href": "/boundary-rules/", "description": "Helpful when siting and frontage position matter."},
        ],
    },
    "highway_safety": {
        "title": "Highway safety and visibility",
        "explanation": "Access changes near a road can be refused where visibility, frontage width or traffic conditions make the arrangement feel unsafe.",
        "reduction_tips": [
            "Check the highway context early rather than leaving visibility issues until late.",
            "Simplify the access arrangement if the frontage is tight or awkward.",
        ],
        "links": [
            {"title": "Dropped Kerbs", "href": "/dropped-kerbs/", "description": "Useful where the planning issue overlaps with highways approval."},
            {"title": "Local Authorities", "href": "/councils/", "description": "Helpful when the local highway or planning layer may change the answer."},
        ],
    },
    "property_policy_fit": {
        "title": "Property type and policy fit",
        "explanation": "Flats, maisonettes and unusual property types can face a tighter policy response than a straightforward householder proposal.",
        "reduction_tips": [
            "Check the policy route carefully before assuming a normal householder application will be judged in the same way.",
            "Use the decision tool if you still need to confirm the likely route first.",
        ],
        "links": [
            {"title": "Planning Decision Engine", "href": "/tools/planning-decision-tool/", "description": "Useful if you still need to confirm the likely planning route."},
            {"title": "Planning Permission", "href": "/planning-permission/", "description": "Helpful for the wider policy route around non-standard property types."},
        ],
    },
    "site_history": {
        "title": "Previous additions and cumulative impact",
        "explanation": "Existing extensions, roof changes and site history can make a fresh proposal feel more intensive than the new work looks in isolation.",
        "reduction_tips": [
            "Assess the new proposal against the whole existing site history, not just the latest change.",
            "Tone down scale or visual impact if the property is already heavily altered.",
        ],
        "links": [
            {"title": "Planning Decision Engine", "href": "/tools/planning-decision-tool/", "description": "Helpful when cumulative development may also affect the route."},
            {"title": "Planning Permission", "href": "/planning-permission/", "description": "Useful for wider application context where cumulative impact matters."},
        ],
    },
}


GLOBAL_RULES = [
    {
        "factor": "property_policy_fit",
        "severity": "moderate",
        "conditions": {"property": ["flat", "other"]},
        "because": "The property type points toward a tighter planning and policy response than a straightforward householder case.",
    },
    {
        "factor": "heritage_policy",
        "severity": "high",
        "constraints_any": ["listed"],
        "because": "Listed building controls can dominate the planning balance and make design harm much harder to justify.",
    },
    {
        "factor": "heritage_policy",
        "severity": "moderate",
        "constraints_any": ["conservation", "article4", "unsure"],
        "because": "Local heritage or policy constraints may make visible change harder to support than the national baseline suggests.",
    },
    {
        "factor": "site_history",
        "severity": "moderate",
        "conditions": {"previous_work": ["yes"]},
        "because": "Previous additions can make the overall scheme feel more intensive or visually dominant.",
    },
]


def _project(project_id: str, description: str, risk_rules: list[dict]):
    project = deepcopy(PROJECTS_BY_ID[project_id])
    project["description"] = description
    project["risk_rules"] = risk_rules
    return project


PROJECTS = [
    _project(
        "rear-extension",
        "Use the same core project questions as the decision tool, but here the output focuses on the refusal risks councils often raise in a planning application.",
        [
            {"factor": "scale_bulk", "severity": "moderate", "conditions": {"size_band": ["borderline"]}, "because": "The extension depth looks close to the point where scale and bulk objections become more likely."},
            {"factor": "scale_bulk", "severity": "high", "conditions": {"size_band": ["large"]}, "because": "The extension depth looks well beyond a comfortable rear scale for many house plots."},
            {"factor": "height_mass", "severity": "moderate", "conditions": {"form_band": ["single-tall"]}, "because": "A taller single-storey form can still look visually dominant if the roof is bulky or high."},
            {"factor": "height_mass", "severity": "high", "conditions": {"form_band": ["two-storey"]}, "because": "A two-storey rear form can look dominant and materially change neighbour outlook."},
            {"factor": "overshadowing_daylight", "severity": "moderate", "conditions": {"near_boundary": ["yes"], "form_band": ["single-tall", "two-storey"]}, "because": "A taller rear extension near the boundary raises a stronger daylight and overshadowing risk."},
            {"factor": "overlooking_privacy", "severity": "moderate", "conditions": {"form_band": ["two-storey"]}, "because": "A two-storey rear extension often triggers more scrutiny around overlooking and neighbour privacy."},
        ],
    ),
    _project(
        "side-extension",
        "This version looks at the design and neighbour issues most likely to cause refusal if the scheme goes in as a planning application.",
        [
            {"factor": "scale_bulk", "severity": "moderate", "conditions": {"size_band": ["borderline"]}, "because": "The width is close to the point where the extension can look too bulky alongside the original house."},
            {"factor": "scale_bulk", "severity": "high", "conditions": {"size_band": ["wide"]}, "because": "A wide side extension often looks too dominant rather than subordinate to the original house."},
            {"factor": "street_scene_character", "severity": "high", "conditions": {"forward_of_house": ["yes"]}, "because": "Projecting forward of the main front wall can make the side addition look intrusive in the street scene."},
            {"factor": "height_mass", "severity": "moderate", "conditions": {"form_band": ["single-tall"]}, "because": "The height makes the side addition more visually assertive than a low, clearly secondary form."},
            {"factor": "height_mass", "severity": "high", "conditions": {"form_band": ["two-storey"]}, "because": "A two-storey side extension often creates a much stronger visual and neighbour impact."},
            {"factor": "overshadowing_daylight", "severity": "moderate", "conditions": {"near_boundary": ["yes"], "form_band": ["single-tall", "two-storey"]}, "because": "A taller edge close to the boundary can trigger daylight and enclosure concerns."},
        ],
    ),
    _project(
        "loft-conversion",
        "The tool focuses on the roof design, neighbour privacy and visual impact points that often drive loft refusal decisions.",
        [
            {"factor": "roof_design", "severity": "moderate", "conditions": {"roof_change": ["moderate"]}, "because": "A noticeable roof enlargement needs to look proportionate rather than bulky."},
            {"factor": "roof_design", "severity": "high", "conditions": {"roof_change": ["major"]}, "because": "A major roof reshaping project can look too dominant or out of keeping with the host roof."},
            {"factor": "roof_design", "severity": "high", "conditions": {"front_facing": ["yes"]}, "because": "A front-facing dormer or major front roof change often raises a stronger character objection."},
            {"factor": "overlooking_privacy", "severity": "moderate", "conditions": {"roof_change": ["moderate", "major"]}, "because": "Larger roof alterations often bring new windows and privacy questions into play."},
        ],
    ),
    _project(
        "garden-room",
        "This version highlights the neighbour, use and siting issues that often matter when a detached garden building needs planning permission.",
        [
            {"factor": "height_mass", "severity": "moderate", "conditions": {"height_band": ["medium"]}, "because": "The building height looks close to the point where a garden structure can feel too dominant."},
            {"factor": "height_mass", "severity": "high", "conditions": {"height_band": ["high"]}, "because": "The building height looks likely to draw stronger visual impact objections."},
            {"factor": "overshadowing_daylight", "severity": "moderate", "conditions": {"near_boundary": ["yes"], "height_band": ["medium", "high"]}, "because": "A taller outbuilding near the boundary can affect neighbour outlook and daylight."},
            {"factor": "street_scene_character", "severity": "high", "conditions": {"forward_of_house": ["yes"]}, "because": "A garden building in front of the house is much more exposed to street scene objections."},
            {"factor": "residential_intensity", "severity": "high", "conditions": {"use_band": ["sleeping"]}, "because": "A building designed for sleeping or day-to-day living will be judged more like accommodation than an incidental outbuilding."},
        ],
    ),
    _project(
        "porch",
        "The porch questions are the same shape as the decision tool, but the output here focuses on appearance and highway-related refusal risk.",
        [
            {"factor": "scale_bulk", "severity": "moderate", "conditions": {"footprint_band": ["medium"]}, "because": "The porch footprint is close to the point where it can start to feel too bulky on the front elevation."},
            {"factor": "scale_bulk", "severity": "high", "conditions": {"footprint_band": ["large"]}, "because": "A larger porch can look over-dominant rather than like a modest entrance feature."},
            {"factor": "height_mass", "severity": "high", "conditions": {"height_band": ["high"]}, "because": "The porch height risks making the addition look too dominant on the front of the house."},
            {"factor": "street_scene_character", "severity": "moderate", "conditions": {"within_two_metres_highway": ["yes"]}, "because": "A porch close to the front boundary or highway is more exposed in the street scene."},
            {"factor": "highway_safety", "severity": "moderate", "conditions": {"within_two_metres_highway": ["yes"]}, "because": "A porch close to the highway can raise visibility and frontage concerns."},
        ],
    ),
    _project(
        "garage-conversion",
        "This version looks at the design, parking and frontage issues most likely to create refusal risk on a garage conversion application.",
        [
            {"factor": "street_scene_character", "severity": "moderate", "conditions": {"change_band": ["minor"]}, "because": "Even a modest front elevation change needs to look well integrated rather than patched in."},
            {"factor": "street_scene_character", "severity": "high", "conditions": {"change_band": ["major"]}, "because": "A major frontage redesign can look out of character with the host house and street."},
            {"factor": "parking_access", "severity": "moderate", "conditions": {"parking_band": ["affected"]}, "because": "The proposal appears to put more pressure on parking or access than a simple internal change."},
            {"factor": "scale_bulk", "severity": "high", "conditions": {"change_band": ["major"]}, "because": "Once a garage conversion adds major external change or extra footprint, scale objections become more likely."},
        ],
    ),
    _project(
        "driveway",
        "This version focuses on drainage, frontage treatment and highway-related refusal risks for hard surfacing and front parking schemes.",
        [
            {"factor": "drainage_surface", "severity": "moderate", "conditions": {"surface_band": ["mixed"]}, "because": "Drainage is not fully resolved yet, which is a common weak point on front garden surfacing proposals."},
            {"factor": "drainage_surface", "severity": "moderate", "conditions": {"surface_band": ["sealed"], "front_garden": ["yes"]}, "because": "An impermeable front garden surface raises a stronger drainage objection risk."},
            {"factor": "drainage_surface", "severity": "high", "conditions": {"surface_band": ["sealed"], "front_garden": ["yes"], "area_band": ["large"]}, "because": "A larger impermeable front garden surface can look weak on drainage and design grounds if runoff is not dealt with properly."},
            {"factor": "street_scene_character", "severity": "moderate", "conditions": {"front_garden": ["yes"], "area_band": ["large"]}, "because": "A larger front parking area can change the character of the frontage more than a modest hardstanding."},
        ],
    ),
    _project(
        "fences-walls",
        "The refusal-risk version of this tool looks at enclosure, street scene and highway visibility concerns for boundary structures.",
        [
            {"factor": "boundary_enclosure", "severity": "moderate", "conditions": {"location_band": ["road"], "height_band": ["medium"]}, "because": "A medium-height boundary treatment beside the road can still feel visually enclosing."},
            {"factor": "boundary_enclosure", "severity": "high", "conditions": {"location_band": ["road"], "height_band": ["high"]}, "because": "A tall boundary beside the road is likely to look visually heavy and over-enclosing."},
            {"factor": "boundary_enclosure", "severity": "high", "conditions": {"location_band": ["side-rear"], "height_band": ["high"]}, "because": "A very tall side or rear boundary treatment can still look overbearing on the plot."},
            {"factor": "highway_safety", "severity": "moderate", "conditions": {"location_band": ["road"], "height_band": ["medium", "high"]}, "because": "A higher frontage wall or fence can also affect visibility beside a road or footpath."},
        ],
    ),
    _project(
        "dropped-kerb",
        "This version focuses on the highway safety and frontage issues most likely to cause a planning or highways refusal.",
        [
            {"factor": "highway_safety", "severity": "moderate", "conditions": {"road_band": ["uncertain"]}, "because": "Until the road status is confirmed, the visibility and planning position remain harder to support with confidence."},
            {"factor": "highway_safety", "severity": "high", "conditions": {"road_band": ["classified"]}, "because": "A busier or classified road tends to trigger a stronger highway safety test."},
            {"factor": "highway_safety", "severity": "moderate", "conditions": {"access_band": ["awkward"]}, "because": "A tight or awkward frontage can make access and visibility objections more likely."},
            {"factor": "street_scene_character", "severity": "moderate", "conditions": {"access_band": ["awkward"]}, "because": "An awkward frontage can also make the access arrangement look forced in the street scene."},
        ],
    ),
]


RISK_ANALYZER_CONFIG = {
    "property_types": deepcopy(DECISION_ENGINE_CONFIG["property_types"]),
    "constraint_options": deepcopy(DECISION_ENGINE_CONFIG["constraint_options"]),
    "previous_work_options": deepcopy(DECISION_ENGINE_CONFIG["previous_work_options"]),
    "risk_factors": deepcopy(RISK_FACTORS),
    "global_rules": deepcopy(GLOBAL_RULES),
    "projects": PROJECTS,
    "default_links": [
        {"title": "What Can I Build? Explorer", "href": "/tools/what-can-i-build-explorer/", "description": "Use the explorer if you are still weighing up which project type is the best fit for the property."},
        {"title": "Planning Decision Engine", "href": "/tools/planning-decision-tool/", "description": "Use the decision tool if you still need to confirm whether the project probably needs planning permission in the first place."},
        {"title": "Planning Permission", "href": "/planning-permission/", "description": "Open the main hub if the refusal risks are pointing toward a formal planning route."},
        {"title": "Local Authorities", "href": "/councils/", "description": "Helpful when local design policy or heritage context could change the risk picture."},
        {"title": "Planning FAQ", "href": "/planning-faq/do-i-need-planning-permission/", "description": "A useful next read when the application route still feels unclear."},
    ],
}
