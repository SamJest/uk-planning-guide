DECISION_ENGINE_CONFIG = {
    "property_types": [
        {"value": "house", "label": "House", "hint": "Detached, semi-detached or terraced house."},
        {"value": "bungalow", "label": "Bungalow", "hint": "Single-storey house using the same householder route in many cases."},
        {"value": "flat", "label": "Flat or maisonette", "hint": "External changes are usually on a tighter planning route than houses."},
        {"value": "other", "label": "Other or not sure", "hint": "Use this when the building type is unusual or the rights are unclear."},
    ],
    "constraint_options": [
        {"value": "conservation", "label": "Conservation area", "hint": "Design and heritage controls can tighten the normal route."},
        {"value": "listed", "label": "Listed building", "hint": "Listed building consent and planning controls often change the answer."},
        {"value": "article4", "label": "Article 4 direction", "hint": "Some councils remove permitted development rights in specific areas."},
        {"value": "unsure", "label": "Not sure about local constraints", "hint": "Use this if you have not checked designations yet."},
    ],
    "previous_work_options": [
        {"value": "no", "label": "No major additions", "hint": "The original house has not already been extended or enlarged in a way that matters here."},
        {"value": "yes", "label": "Yes or not sure", "hint": "Previous additions can use up allowances that these quicker answers rely on."},
    ],
    "projects": [
        {
            "id": "rear-extension",
            "label": "Rear extension",
            "description": "Best for single-storey or two-storey rear additions to a house.",
            "guide_href": "/rear-extensions/",
            "guide_title": "Rear Extension Guide",
            "primary_question": {
                "id": "size_band",
                "label": "How deep is the extension roughly?",
                "options": [
                    {"value": "modest", "label": "Modest depth", "hint": "Up to about 3m on an attached house or 4m on a detached house."},
                    {"value": "borderline", "label": "Around the limit", "hint": "Close to the usual rear extension depth limit."},
                    {"value": "large", "label": "Clearly beyond it", "hint": "Pushing well past the normal depth used for a simple answer."},
                ],
            },
            "secondary_question": {
                "id": "form_band",
                "label": "How tall is it?",
                "options": [
                    {"value": "single-modest", "label": "Single-storey and modest", "hint": "Typical eaves and ridge height for a standard rear extension."},
                    {"value": "single-tall", "label": "Single-storey but tall", "hint": "A high roof, vaulted form or otherwise close to a height limit."},
                    {"value": "two-storey", "label": "Two-storey", "hint": "The extension includes a full upper floor."},
                ],
            },
            "binary_questions": [
                {"id": "near_boundary", "label": "Does any high part sit close to a boundary?", "help": "Being within about 2 metres of a boundary can make the height check much more important."},
            ],
            "common_changes": [
                "Exact depth from the original rear wall.",
                "Overall height and eaves height near a boundary.",
                "Previous extensions already added to the house.",
                "Conservation area, Article 4 or listed building controls.",
            ],
            "next_checks": [
                "Measure the extension from the original rear wall, not the latest addition.",
                "Check the overall height and whether any high section is within about 2 metres of a boundary.",
                "Open the rear extension guide if the scheme is close to a limit.",
            ],
            "related_pages": [
                {"title": "House Extensions", "href": "/house-extensions/", "description": "Broader guidance when the extension design is still changing."},
                {"title": "Boundary Rules", "href": "/boundary-rules/", "description": "Useful when the side gap or neighbour relationship is driving the uncertainty."},
            ],
        },
        {
            "id": "side-extension",
            "label": "Side extension",
            "description": "Useful for side additions where width, height and front position matter.",
            "guide_href": "/side-extensions/",
            "guide_title": "Side Extension Guide",
            "primary_question": {
                "id": "size_band",
                "label": "How wide is the extension compared with the original house?",
                "options": [
                    {"value": "narrow", "label": "Clearly narrow", "hint": "It looks comfortably less than half the width of the original house."},
                    {"value": "borderline", "label": "Around half width", "hint": "Close to the point where side extensions often become borderline."},
                    {"value": "wide", "label": "Quite wide", "hint": "It looks wider than half the original house."},
                ],
            },
            "secondary_question": {
                "id": "form_band",
                "label": "How tall is it?",
                "options": [
                    {"value": "single-modest", "label": "Single-storey and modest", "hint": "A conventional single-storey side extension."},
                    {"value": "single-tall", "label": "Single-storey but tall", "hint": "Height or roof form feels close to a limit."},
                    {"value": "two-storey", "label": "Two-storey", "hint": "A full two-storey side extension."},
                ],
            },
            "binary_questions": [
                {"id": "forward_of_house", "label": "Does it project in front of the main front wall?", "help": "Being forward of the principal elevation often changes the route."},
                {"id": "near_boundary", "label": "Is the taller edge close to a boundary?", "help": "This often makes the height and neighbour checks more sensitive."},
            ],
            "common_changes": [
                "Whether the extension stays behind the main front wall.",
                "Whether the width remains clearly under half the original house width.",
                "Height close to a boundary.",
                "Local constraints and previous additions.",
            ],
            "next_checks": [
                "Compare the width against the original house, not the latest altered version.",
                "Check whether any part projects forward of the principal elevation.",
                "Open the side extension guide if the design is not obviously narrow and low.",
            ],
            "related_pages": [
                {"title": "House Extensions", "href": "/house-extensions/", "description": "Helpful when you need the wider extension rules around the project."},
                {"title": "Boundary Rules", "href": "/boundary-rules/", "description": "A strong next read when boundary position is the tripwire."},
            ],
        },
        {
            "id": "loft-conversion",
            "label": "Loft conversion",
            "description": "Good for rooflights, dormers and other loft changes on a house.",
            "guide_href": "/loft-conversions/",
            "guide_title": "Loft Conversion Guide",
            "primary_question": {
                "id": "roof_change",
                "label": "How big is the roof change?",
                "options": [
                    {"value": "light", "label": "Light change", "hint": "Rooflights only or a very modest rear change."},
                    {"value": "moderate", "label": "Noticeable enlargement", "hint": "A rear dormer or similar roof enlargement."},
                    {"value": "major", "label": "Major reshaping", "hint": "A large roof raise, major dormer or dramatic roof alteration."},
                ],
            },
            "binary_questions": [
                {"id": "front_facing", "label": "Does a dormer or major roof change face the road?", "help": "Front-facing roof alterations often move the answer away from the simple route."},
            ],
            "common_changes": [
                "Whether the roof enlargement faces the highway.",
                "How much extra roof volume is being added.",
                "Previous roof additions already carried out.",
                "Conservation area, Article 4 or listed building controls.",
            ],
            "next_checks": [
                "Measure the extra roof volume rather than relying on a visual guess.",
                "Check whether any dormer or roof change sits on the front roof slope.",
                "Open the loft conversion guide for volume and roof alteration detail.",
            ],
            "related_pages": [
                {"title": "Roof Alterations", "href": "/roof-alterations/", "description": "Helpful when the question is really about how the roof is changing."},
                {"title": "Permitted Development", "href": "/permitted-development/", "description": "Useful for the underlying householder PD baseline."},
            ],
        },
        {
            "id": "garden-room",
            "label": "Garden room or outbuilding",
            "description": "Useful for garden rooms, sheds, studios and detached outbuildings.",
            "guide_href": "/garden-rooms/",
            "guide_title": "Garden Room Guide",
            "primary_question": {
                "id": "height_band",
                "label": "How tall is the building roughly?",
                "options": [
                    {"value": "low", "label": "Comfortably low", "hint": "Clearly below the usual outbuilding height thresholds."},
                    {"value": "medium", "label": "Around the limit", "hint": "Close to the height where a detailed check matters."},
                    {"value": "high", "label": "Quite tall", "hint": "Pushing beyond the usual outbuilding height envelope."},
                ],
            },
            "secondary_question": {
                "id": "use_band",
                "label": "What is it mainly for?",
                "options": [
                    {"value": "incidental", "label": "Incidental use", "hint": "Home office, hobbies, storage, gym or similar use alongside the house."},
                    {"value": "sleeping", "label": "Sleeping or living use", "hint": "Guest room, annexe or anything that starts to work as accommodation."},
                ],
            },
            "binary_questions": [
                {"id": "near_boundary", "label": "Is it within about 2 metres of a boundary?", "help": "The nearer it is to the boundary, the tighter the height question becomes."},
                {"id": "forward_of_house", "label": "Is any part in front of the main house wall?", "help": "Outbuildings in front of the principal elevation are usually a harder route."},
            ],
            "common_changes": [
                "Maximum height from natural ground level.",
                "Whether it is truly incidental to the main house.",
                "Distance to boundaries and position in front of the house.",
                "Local constraints and previous outbuildings or additions.",
            ],
            "next_checks": [
                "Measure the maximum height from the correct ground level.",
                "Check whether the intended use stays incidental rather than becoming accommodation.",
                "Open the garden room or outbuildings guide if the building is near a boundary or close to the height limit.",
            ],
            "related_pages": [
                {"title": "Outbuildings", "href": "/outbuildings/", "description": "Wider guidance for sheds, garages and other detached structures."},
                {"title": "Maximum Height", "href": "/maximum-height/", "description": "Helpful when height is the question that keeps changing the answer."},
            ],
        },
        {
            "id": "porch",
            "label": "Porch",
            "description": "Best for a new porch on the front or side of the house.",
            "guide_href": "/porches/",
            "guide_title": "Porch Guide",
            "primary_question": {
                "id": "footprint_band",
                "label": "How large is the porch footprint?",
                "options": [
                    {"value": "small", "label": "Up to about 3m²", "hint": "Comfortably within the usual small-porch size."},
                    {"value": "medium", "label": "Around 3 to 4m²", "hint": "Close to the point where a detailed check matters."},
                    {"value": "large", "label": "More than about 4m²", "hint": "Clearly larger than the simplest porch allowance."},
                ],
            },
            "secondary_question": {
                "id": "height_band",
                "label": "How tall is the porch?",
                "options": [
                    {"value": "low", "label": "Up to about 3m", "hint": "Typical porch height."},
                    {"value": "high", "label": "More than about 3m", "hint": "Height alone may move the project out of the simple route."},
                ],
            },
            "binary_questions": [
                {"id": "within_two_metres_highway", "label": "Is it within about 2 metres of a highway or front boundary?", "help": "That proximity often changes the answer for porches."},
            ],
            "common_changes": [
                "External ground-floor area rather than internal usable space.",
                "Overall height.",
                "Distance to a highway or boundary fronting the road.",
                "Local designations and heritage controls.",
            ],
            "next_checks": [
                "Measure the external footprint rather than estimating the internal floor area.",
                "Check the distance from any boundary that fronts a highway.",
                "Open the porch guide if the design is close to the usual size or height limits.",
            ],
            "related_pages": [
                {"title": "Planning Permission", "href": "/planning-permission/", "description": "Useful if the porch is larger, taller or in a sensitive location."},
                {"title": "Permitted Development", "href": "/permitted-development/", "description": "Helpful for the baseline householder route."},
            ],
        },
        {
            "id": "garage-conversion",
            "label": "Garage conversion",
            "description": "Useful for internal garage conversions and cases with external changes.",
            "guide_href": "/garage-conversions/",
            "guide_title": "Garage Conversion Guide",
            "primary_question": {
                "id": "change_band",
                "label": "How much does the outside change?",
                "options": [
                    {"value": "internal", "label": "Mostly internal", "hint": "No extra footprint and only very modest external alteration."},
                    {"value": "minor", "label": "Visible but modest", "hint": "New window or door arrangement, but no extension."},
                    {"value": "major", "label": "Major external change", "hint": "Extension, large new openings or major frontage redesign."},
                ],
            },
            "secondary_question": {
                "id": "parking_band",
                "label": "What happens to parking and access?",
                "options": [
                    {"value": "retained", "label": "Parking still works", "hint": "There is still practical off-street parking after the conversion."},
                    {"value": "affected", "label": "Parking becomes a planning issue", "hint": "The conversion may remove or compromise parking or access expectations."},
                ],
            },
            "common_changes": [
                "Whether the work is really internal only.",
                "Parking conditions tied to the original permission.",
                "How much the front elevation changes.",
                "Local constraints and previous planning conditions.",
            ],
            "next_checks": [
                "Review the original planning history for any parking or garage-retention conditions.",
                "Check whether the frontage change is modest or a bigger redesign.",
                "Open the garage conversion guide if parking or frontage treatment is the main issue.",
            ],
            "related_pages": [
                {"title": "Permitted Development", "href": "/permitted-development/", "description": "Helpful where the conversion is mostly internal."},
                {"title": "Local Authorities", "href": "/councils/", "description": "Useful when parking standards or local design expectations matter."},
            ],
        },
        {
            "id": "driveway",
            "label": "Driveway or hard surface",
            "description": "Useful for new or replacement driveways and front garden parking areas.",
            "guide_href": "/driveways/",
            "guide_title": "Driveway Guide",
            "primary_question": {
                "id": "surface_band",
                "label": "How will surface water drain?",
                "options": [
                    {"value": "permeable", "label": "Permeable or soakaway", "hint": "Water soaks away within the property."},
                    {"value": "mixed", "label": "Not fully confirmed", "hint": "Drainage solution is mixed or still unclear."},
                    {"value": "sealed", "label": "Impermeable to the road", "hint": "Water would run to the highway or public sewer without a soakaway solution."},
                ],
            },
            "secondary_question": {
                "id": "area_band",
                "label": "How large is the surfaced area?",
                "options": [
                    {"value": "small", "label": "Around 5m² or less", "hint": "A small patch or limited parking bay."},
                    {"value": "large", "label": "Larger than 5m²", "hint": "Most front garden parking projects fall into this category."},
                ],
            },
            "binary_questions": [
                {"id": "front_garden", "label": "Is it mainly on the front garden facing the road?", "help": "Front garden hard surfacing is where the drainage rule matters most."},
            ],
            "common_changes": [
                "Whether the surface is permeable or drains within the site.",
                "Whether the area is larger than around 5 square metres.",
                "Whether a new dropped kerb is also needed.",
                "Conservation area or Article 4 controls.",
            ],
            "next_checks": [
                "Confirm exactly where surface water will drain.",
                "Separate the driveway surface question from any dropped kerb or highway licence question.",
                "Open the driveway guide if the area is in the front garden or drainage is not yet clear.",
            ],
            "related_pages": [
                {"title": "Dropped Kerbs", "href": "/dropped-kerbs/", "description": "Use this if the project also needs a new vehicle access from the road."},
                {"title": "Planning Permission", "href": "/planning-permission/", "description": "Helpful where impermeable surfacing or local controls change the route."},
            ],
        },
        {
            "id": "fences-walls",
            "label": "Fence, gate or wall",
            "description": "Useful for boundary walls, fences and gates where height is the key issue.",
            "guide_href": "/fences-and-walls/",
            "guide_title": "Fences and Walls Guide",
            "primary_question": {
                "id": "height_band",
                "label": "How tall is the fence, wall or gate?",
                "options": [
                    {"value": "low", "label": "Low", "hint": "At or below about 1 metre."},
                    {"value": "medium", "label": "Medium", "hint": "Between about 1 and 2 metres."},
                    {"value": "high", "label": "High", "hint": "Over about 2 metres."},
                ],
            },
            "secondary_question": {
                "id": "location_band",
                "label": "Where is it mainly located?",
                "options": [
                    {"value": "road", "label": "Fronting a road or footpath", "hint": "This is the stricter height situation."},
                    {"value": "side-rear", "label": "Side or rear boundary", "hint": "Usually the simpler height threshold."},
                ],
            },
            "common_changes": [
                "Height measured from the right ground level.",
                "Whether the boundary fronts a highway used by vehicles or pedestrians.",
                "Whether the wall or gate sits at the front of the house.",
                "Conservation area, listed building or local design controls.",
            ],
            "next_checks": [
                "Measure height from the lowest adjoining ground level, not just from the garden side.",
                "Check whether the boundary fronts a highway or footpath.",
                "Open the fence and wall guide if the structure is near or above the common thresholds.",
            ],
            "related_pages": [
                {"title": "Boundary Rules", "href": "/boundary-rules/", "description": "Helpful if the boundary relationship itself is the blocker."},
                {"title": "Planning Permission", "href": "/planning-permission/", "description": "Use this when height or highway position pushes the project out of the simple route."},
            ],
        },
        {
            "id": "dropped-kerb",
            "label": "Dropped kerb",
            "description": "Best for a new vehicle crossover or access across the pavement.",
            "guide_href": "/dropped-kerbs/",
            "guide_title": "Dropped Kerb Guide",
            "primary_question": {
                "id": "road_band",
                "label": "What sort of road is it on?",
                "options": [
                    {"value": "local", "label": "Minor residential road", "hint": "A typical local street without obvious highway complications."},
                    {"value": "uncertain", "label": "Not sure", "hint": "Road status is not confirmed yet."},
                    {"value": "classified", "label": "Busier or classified road", "hint": "A road where visibility and planning control are more likely to matter."},
                ],
            },
            "secondary_question": {
                "id": "access_band",
                "label": "How straightforward is the frontage?",
                "options": [
                    {"value": "simple", "label": "Straightforward frontage", "hint": "Plenty of width and no obvious shared-access complication."},
                    {"value": "awkward", "label": "Shared, tight or awkward", "hint": "Visibility, width or the access arrangement already looks challenging."},
                ],
            },
            "common_changes": [
                "Road classification and visibility.",
                "Whether a new parking area or driveway is also part of the project.",
                "Highway approval requirements alongside planning.",
                "Conservation area or Article 4 controls.",
            ],
            "next_checks": [
                "Check the highways route as well as the planning route.",
                "Confirm the road classification and whether visibility standards are likely to bite.",
                "Open the dropped kerb guide before assuming the simpler route applies.",
            ],
            "related_pages": [
                {"title": "Driveways", "href": "/driveways/", "description": "Useful when the crossover is part of a wider front garden parking project."},
                {"title": "Local Authorities", "href": "/councils/", "description": "Helpful when local highways or planning expectations are the real blocker."},
            ],
        },
    ],
    "default_links": [
        {"title": "What Can I Build? Explorer", "href": "/tools/what-can-i-build-explorer/", "description": "Use this if you are still deciding which kind of project is worth checking in more detail."},
        {"title": "Planning Permission", "href": "/planning-permission/", "description": "The main hub when the answer points toward an application or a closer check."},
        {"title": "Permitted Development", "href": "/permitted-development/", "description": "Helpful for the baseline rights behind the simpler route."},
        {"title": "Planning Rejection Risk Analyzer", "href": "/tools/planning-rejection-risk-analyzer/", "description": "Use this if the likely route is already clear and you want to stress-test the main refusal risks."},
        {"title": "Local Authorities", "href": "/councils/", "description": "Best when local designations or council context could change the answer."},
        {"title": "Planning FAQ", "href": "/planning-faq/do-i-need-planning-permission/", "description": "A practical next read when the process itself still feels unclear."},
    ],
}
