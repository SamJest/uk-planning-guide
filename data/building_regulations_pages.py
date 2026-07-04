from __future__ import annotations


OFFICIAL_BUILDING_REGULATIONS_SOURCES = {
    "approval_needed": {
        "title": "GOV.UK: Building regulations approval",
        "url": "https://www.gov.uk/building-regulations-approval",
        "category": "building_regulations",
        "notes": "Use this to check when building regulations approval may be needed and why it is separate from planning permission.",
    },
    "how_to_apply": {
        "title": "GOV.UK: How to apply for building regulations approval",
        "url": "https://www.gov.uk/building-regulations-approval/how-to-apply",
        "category": "building_control",
        "notes": "Use this to choose the building control route, including local authority building control or a registered approver.",
    },
    "application_information": {
        "title": "GOV.UK: Preparing information for a building control approval application",
        "url": "https://www.gov.uk/guidance/preparing-information-for-a-building-control-approval-application",
        "category": "building_control_application",
        "notes": "Use this when the next question is what information, drawings and declarations may be needed for building control.",
    },
    "approved_documents": {
        "title": "GOV.UK: Approved Documents",
        "url": "https://www.gov.uk/government/collections/approved-documents",
        "category": "approved_documents",
        "notes": "Use this for the statutory guidance documents that explain common ways to meet building regulations requirements in England.",
    },
    "competent_person": {
        "title": "GOV.UK: Use a competent person scheme",
        "url": "https://www.gov.uk/building-regulations-approval/use-a-competent-person-scheme",
        "category": "competent_person_scheme",
        "notes": "Use this where windows, boilers, electrics or similar work may be self-certified by a registered installer instead of a direct building-control application.",
    },
}


BUILDING_REGULATIONS_PAGES = [
    {
        "slug": "index",
        "title": "Building Regulations For Home Projects",
        "meta_title": "Building regulations: home project approval guide",
        "meta_description": "Check building regulations for home projects in England, including approval routes, building control, certificates and planning links.",
        "intent": "building regulations hub",
        "jurisdiction": "England",
        "project_slug": "",
        "primary_questions": [
            ("Are building regulations the same as planning permission?", "No. Planning decides whether development is acceptable in planning terms. Building regulations deal with construction standards, safety, energy use, drainage and similar technical matters."),
            ("Can a project need both?", "Yes. Many domestic projects can need building regulations approval even when planning permission is not required."),
            ("What should I check first?", "Start with the planning route if the design itself may not be acceptable, then use building control to settle how compliant work should be carried out."),
        ],
        "answer_blocks": [
            {
                "title": "Short answer",
                "body": "For England, treat building regulations as a separate approval track from planning permission. Extensions, loft conversions, garage conversions and many structural or service changes commonly need building control input even where the planning route looks simple.",
                "checks": ["Identify the work type", "Check whether planning is also needed", "Choose local authority building control or a registered approver"],
            },
            {
                "title": "Why it matters",
                "body": "The practical risk is not only enforcement. Missing building control evidence can create problems when selling, remortgaging or proving that work was inspected properly.",
                "checks": ["Keep application records", "Keep inspection notes", "Keep completion certificates or equivalent compliance evidence"],
            },
        ],
        "official_sources": ["approval_needed", "how_to_apply", "application_information"],
        "related_routes": [
            {"title": "Building Control Route Checker", "href": "/tools/building-control-route-checker/", "description": "Choose whether the next conversation is full plans, building notice, competent person route, regularisation or planning-first."},
            {"title": "Planning Permission Vs Building Regulations", "href": "/planning-faq/planning-permission-vs-building-regulations/", "description": "Use this if the two approval systems are still being mixed together."},
            {"title": "Project Requirements Generator", "href": "/tools/project-requirements-generator/", "description": "Build a planning-side prep pack before you commission drawings or submit."},
            {"title": "Evidence Pack Builder", "href": "/tools/evidence-pack-builder/", "description": "Create a checklist of photos, measurements, drawings and records to keep together."},
        ],
    },
    {
        "slug": "extensions",
        "title": "Building Regulations For Extensions",
        "meta_title": "Building regulations for extensions in England",
        "meta_description": "Check extension building regulations in England, including structure, insulation, drainage, fire safety and planning route links.",
        "intent": "extension building regulations",
        "jurisdiction": "England",
        "project_slug": "house-extensions",
        "primary_questions": [
            ("Do extensions usually need building regulations approval?", "Yes. Most domestic extensions need building control because structure, insulation, drainage, ventilation and fire safety can all be involved."),
            ("Does permitted development avoid building regulations?", "No. A permitted development extension can still need building regulations approval."),
            ("What should be ready before applying?", "Measured drawings, structural assumptions, drainage position and the intended use of the new space usually matter early."),
        ],
        "answer_blocks": [
            {
                "title": "Main approval track",
                "body": "For an England extension, expect building control to matter unless the work is unusually minor. The planning question decides whether the extension can be built; building regulations decide whether the construction meets technical standards.",
                "checks": ["Structural support", "Thermal performance", "Drainage and ventilation"],
            },
            {
                "title": "Planning link",
                "body": "Settle the planning route before final technical design if the extension is close to a planning limit, near a boundary or affected by local controls.",
                "checks": ["Depth and height", "Neighbour impact", "Previous additions"],
            },
        ],
        "official_sources": ["approval_needed", "how_to_apply", "application_information"],
        "related_routes": [
            {"title": "Building Control Route Checker", "href": "/tools/building-control-route-checker/", "description": "Use this before choosing building notice or full plans for the extension."},
            {"title": "House Extensions", "href": "/house-extensions/", "description": "Check the planning route before the technical approval route is treated as settled."},
            {"title": "Building Regulations For Extensions FAQ", "href": "/planning-faq/building-regulations-for-extensions/", "description": "Read the shorter extension-focused answer."},
            {"title": "Drawings Cost Readiness Checker", "href": "/tools/drawings-cost-readiness-checker/", "description": "Use this before commissioning drawings too early."},
        ],
    },
    {
        "slug": "loft-conversions",
        "title": "Building Regulations For Loft Conversions",
        "meta_title": "Loft conversion building regulations in England",
        "meta_description": "Check loft conversion building regulations in England, including structure, stairs, fire safety, insulation and planning links.",
        "intent": "loft conversion building regulations",
        "jurisdiction": "England",
        "project_slug": "loft-conversions",
        "primary_questions": [
            ("Do loft conversions need building control?", "In most cases, yes. The route often involves structure, stairs, fire safety, insulation and ventilation."),
            ("Is planning permission separate?", "Yes. A loft may be permitted development in planning terms but still need building regulations approval."),
            ("What is the biggest early risk?", "Commissioning drawings before the head height, stairs and roof alteration route are understood can waste time."),
        ],
        "answer_blocks": [
            {
                "title": "Main approval track",
                "body": "A loft conversion is usually a building-control-heavy project because it changes how roof space is used and how people escape safely from the house.",
                "checks": ["Structural floor and roof changes", "Stairs and escape route", "Insulation and ventilation"],
            },
            {
                "title": "Planning link",
                "body": "Planning still matters if the loft includes dormers, visible roof changes or local restrictions such as conservation area controls.",
                "checks": ["Roof form", "Visible alterations", "Local restrictions"],
            },
        ],
        "official_sources": ["approval_needed", "how_to_apply", "application_information"],
        "related_routes": [
            {"title": "Building Control Route Checker", "href": "/tools/building-control-route-checker/", "description": "Use this to decide whether the loft route needs full plans before work starts."},
            {"title": "Loft Conversions", "href": "/loft-conversions/", "description": "Check the planning side of the loft route."},
            {"title": "Roof Alterations", "href": "/roof-alterations/", "description": "Use this when visible roof changes may alter the planning answer."},
            {"title": "Project Roadmap Builder", "href": "/tools/project-roadmap-builder/", "description": "Sequence planning, drawings and approval steps before committing spend."},
        ],
    },
    {
        "slug": "garage-conversions",
        "title": "Building Regulations For Garage Conversions",
        "meta_title": "Garage conversion building regulations in England",
        "meta_description": "Check garage conversion building regulations in England, including insulation, damp, fire safety, structure and planning checks.",
        "intent": "garage conversion building regulations",
        "jurisdiction": "England",
        "project_slug": "garage-conversions",
        "primary_questions": [
            ("Do garage conversions need building regulations approval?", "Usually yes, because the work changes a non-habitable space into living accommodation."),
            ("Does it always need planning permission?", "Not always, but planning can still matter if conditions, external changes or local restrictions apply."),
            ("What should be checked early?", "Insulation, damp proofing, ventilation, fire separation and any structural opening changes are common early checks."),
        ],
        "answer_blocks": [
            {
                "title": "Main approval track",
                "body": "Building control usually focuses on whether the converted garage can perform like proper living space, not just whether the door has been blocked up neatly.",
                "checks": ["Thermal upgrade", "Damp resistance", "Fire safety and ventilation"],
            },
            {
                "title": "Planning link",
                "body": "Planning becomes more important where the garage has restrictive conditions, the frontage changes noticeably or the council has local parking concerns.",
                "checks": ["Planning conditions", "Frontage changes", "Parking pressure"],
            },
        ],
        "official_sources": ["approval_needed", "how_to_apply", "application_information"],
        "related_routes": [
            {"title": "Building Control Route Checker", "href": "/tools/building-control-route-checker/", "description": "Work out whether building control, installer certification or regularisation is the next route."},
            {"title": "Garage Conversions", "href": "/garage-conversions/", "description": "Check the planning route for converting a garage."},
            {"title": "Planning Route Planner", "href": "/tools/planning-route-planner/", "description": "Build the order of checks before drawings and building control."},
            {"title": "Evidence Pack Builder", "href": "/tools/evidence-pack-builder/", "description": "Keep planning and building-control evidence in one place."},
        ],
    },
    {
        "slug": "porches",
        "title": "Building Regulations For Porches",
        "meta_title": "Porch building regulations in England",
        "meta_description": "Check porch building regulations in England, including glazing, electrics, thermal separation and planning permission links.",
        "intent": "porch building regulations",
        "jurisdiction": "England",
        "project_slug": "porches",
        "primary_questions": [
            ("Do porches need building regulations approval?", "Some small porches may be exempt, but the answer depends on size, glazing, electrics and whether the existing front door remains in place."),
            ("Does planning still matter?", "Yes. Porch planning limits are separate from building regulations exemptions."),
            ("What should I ask before building?", "Ask whether the porch is exempt and whether any electrical, glazing or thermal work must still comply."),
        ],
        "answer_blocks": [
            {
                "title": "Main approval track",
                "body": "The building regulations question for a porch is usually about whether an exemption really applies and whether specific work still needs competent handling.",
                "checks": ["Floor area", "Thermal separation", "Glazing and electrics"],
            },
            {
                "title": "Planning link",
                "body": "A porch can be small enough for one approval route and still fail another if it sits too close to a highway or exceeds a planning limit.",
                "checks": ["External size", "Highway-side position", "Height"],
            },
        ],
        "official_sources": ["approval_needed", "how_to_apply", "application_information"],
        "related_routes": [
            {"title": "Building Control Route Checker", "href": "/tools/building-control-route-checker/", "description": "Use this when you are unsure whether the porch is exempt or needs a compliance route."},
            {"title": "Porches", "href": "/porches/", "description": "Check the planning side of porch size and position."},
            {"title": "Planning Permission For Extensions", "href": "/planning-faq/planning-permission-for-extensions/", "description": "Use this when the porch is part of a wider extension route."},
            {"title": "Planning Task Checklist Builder", "href": "/tools/planning-task-checklist-builder/", "description": "Build a small project checklist before work starts."},
        ],
    },
    {
        "slug": "temporary-buildings",
        "title": "Building Regulations For Temporary Buildings",
        "meta_title": "Temporary building regulations in England",
        "meta_description": "Check temporary building regulations in England, including structure, use, services, safety and planning permission links.",
        "intent": "temporary building regulations",
        "jurisdiction": "England",
        "project_slug": "temporary-buildings",
        "primary_questions": [
            ("Can temporary buildings need building regulations approval?", "Yes. The word temporary does not automatically remove technical approval questions."),
            ("Does planning still matter?", "Yes. Planning looks at use, duration, siting and impact, while building regulations look at technical compliance."),
            ("What is the practical risk?", "A structure that is occupied, serviced or fixed in place can stop feeling temporary quickly."),
        ],
        "answer_blocks": [
            {
                "title": "Main approval track",
                "body": "Building control risk rises when a temporary building has services, regular occupation, structural complexity or a safety-critical use.",
                "checks": ["Structure and anchoring", "Fire safety", "Services and access"],
            },
            {
                "title": "Planning link",
                "body": "Planning risk rises when the temporary use is open-ended, visually prominent or effectively operating as a permanent building.",
                "checks": ["Duration", "Use", "Removal plan"],
            },
        ],
        "official_sources": ["approval_needed", "how_to_apply", "application_information"],
        "related_routes": [
            {"title": "Building Control Route Checker", "href": "/tools/building-control-route-checker/", "description": "Use this if temporary occupation, services or public use make the route unclear."},
            {"title": "Temporary Buildings", "href": "/temporary-buildings/", "description": "Check the planning route for temporary structures and site buildings."},
            {"title": "Temporary Buildings And Building Regulations", "href": "/planning-faq/temporary-buildings-building-regulations/", "description": "Read the shorter FAQ answer."},
            {"title": "Planning Timeline Planner", "href": "/tools/planning-timeline-planner/", "description": "Sequence checks before installation dates are fixed."},
        ],
    },
    {
        "slug": "outbuildings",
        "title": "Building Regulations For Outbuildings",
        "meta_title": "Outbuilding building regulations in England",
        "meta_description": "Check outbuilding building regulations in England, including size, sleeping use, services, fire safety and planning links.",
        "intent": "outbuilding building regulations",
        "jurisdiction": "England",
        "project_slug": "outbuildings",
        "primary_questions": [
            ("Do outbuildings need building regulations approval?", "Some small detached outbuildings may avoid approval, but size, sleeping accommodation, services and proximity to boundaries can change the answer."),
            ("Does garden room marketing settle it?", "No. How the building is used and built matters more than the label."),
            ("What should I check before ordering?", "Check size, use, electrics, heating, drainage, boundary position and whether anyone may sleep there."),
        ],
        "answer_blocks": [
            {
                "title": "Main approval track",
                "body": "An outbuilding becomes more building-control-sensitive when it is larger, closer to boundaries, fitted with services or capable of sleeping accommodation.",
                "checks": ["Use and occupation", "Size and boundary position", "Electrics, heating and drainage"],
            },
            {
                "title": "Planning link",
                "body": "Planning still controls whether the outbuilding is incidental, appropriately sited and within the permitted development envelope.",
                "checks": ["Incidental use", "Height", "Siting"],
            },
        ],
        "official_sources": ["approval_needed", "how_to_apply", "application_information"],
        "related_routes": [
            {"title": "Building Control Route Checker", "href": "/tools/building-control-route-checker/", "description": "Use this when services, sleeping use or boundary position make the building-control route unclear."},
            {"title": "Outbuildings", "href": "/outbuildings/", "description": "Check the planning side for sheds, garden rooms and detached structures."},
            {"title": "Garden Room Planning Permission", "href": "/planning-faq/garden-room-planning-permission/", "description": "Use this if the outbuilding is really a garden room."},
            {"title": "Site Constraint Checker", "href": "/tools/site-constraint-checker/", "description": "Check local and site constraints before relying on a broad answer."},
        ],
    },
    {
        "slug": "driveways",
        "title": "Building Regulations For Driveways",
        "meta_title": "Driveway building regulations in England",
        "meta_description": "Check driveway building regulations in England, including drainage, access, hard surfaces, dropped kerbs and planning links.",
        "intent": "driveway building regulations",
        "jurisdiction": "England",
        "project_slug": "driveways",
        "primary_questions": [
            ("Are driveways mainly a building regulations issue?", "Usually the bigger issues are planning, drainage and highway approval, but construction standards can still matter."),
            ("Does a driveway need planning permission?", "It can, especially for non-permeable front garden surfacing or where access changes are involved."),
            ("What should be separated?", "Separate surface drainage, planning permission, dropped kerb or highways approval, and any construction compliance questions."),
        ],
        "answer_blocks": [
            {
                "title": "Main approval track",
                "body": "For driveways, the useful check is often not one approval label but the split between drainage, vehicle access and planning restrictions.",
                "checks": ["Surface water", "Dropped kerb approval", "Frontage construction"],
            },
            {
                "title": "Planning link",
                "body": "Planning becomes important when a front garden is paved with non-permeable surfacing or when local restrictions affect frontage changes.",
                "checks": ["Permeable surfacing", "Highway access", "Local restrictions"],
            },
        ],
        "official_sources": ["approval_needed", "how_to_apply", "application_information"],
        "related_routes": [
            {"title": "Building Control Route Checker", "href": "/tools/building-control-route-checker/", "description": "Use this if the driveway search is really about drainage, highway access or technical compliance."},
            {"title": "Driveways", "href": "/driveways/", "description": "Check the planning and drainage route for driveways."},
            {"title": "Dropped Kerbs", "href": "/dropped-kerbs/", "description": "Use this when the route involves vehicle access over the pavement."},
            {"title": "Dropped Kerb Planning Vs Highways Approval", "href": "/planning-faq/dropped-kerb-planning-vs-highways-approval/", "description": "Separate planning from highway approval before applying."},
        ],
    },
    {
        "slug": "cornwall-extensions",
        "title": "Building Regulations For Home Extensions In Cornwall",
        "meta_title": "Building regulations for home extensions in Cornwall",
        "meta_description": "Check Cornwall home extension building regulations, building control route, planning permission links and evidence to keep.",
        "intent": "local extension building regulations",
        "jurisdiction": "England",
        "project_slug": "house-extensions",
        "primary_questions": [
            ("Is this a Cornwall-specific building regulations rule page?", "No. The technical baseline is England-focused. The local angle is which planning and council routes to open before committing drawings."),
            ("Why make a local page?", "Search demand shows people combine Cornwall with building regulations for home extensions, so this page turns that query into the right national and local next checks."),
            ("Where should I go next?", "Use the extension planning guide and Cornwall local planning pages if the design is still not settled."),
        ],
        "answer_blocks": [
            {
                "title": "Local read",
                "body": "For a Cornwall home extension, do not let building regulations hide the planning question. Building control can deal with technical compliance, while planning still deals with the acceptability of the extension itself.",
                "checks": ["Extension dimensions", "Planning route", "Building control application route"],
            },
            {
                "title": "Evidence to keep",
                "body": "Keep drawings, structural notes, approval correspondence and completion evidence together because the paperwork can matter later during sale or remortgage.",
                "checks": ["Drawings", "Approval record", "Completion evidence"],
            },
        ],
        "official_sources": ["approval_needed", "how_to_apply", "application_information"],
        "related_routes": [
            {"title": "Building Control Route Checker", "href": "/tools/building-control-route-checker/", "description": "Use this before choosing the technical approval route for the extension."},
            {"title": "House Extensions In Cornwall", "href": "/house-extensions/cornwall/", "description": "Compare local extension routes across Cornwall councils."},
            {"title": "Planning Permission In Cornwall", "href": "/cornwall/", "description": "Open the county entry page for local authority routes."},
            {"title": "Extensions Building Regulations", "href": "/building-regulations/extensions/", "description": "Read the national England-first extension guidance."},
        ],
    },
    {
        "slug": "porches-building-regulations",
        "title": "Porches Building Regulations",
        "meta_title": "Porches building regulations: England checks",
        "meta_description": "Check porch building regulations in England, including exemptions, glazing, electrics, thermal separation and planning limits.",
        "intent": "porch building regulations search",
        "jurisdiction": "England",
        "project_slug": "porches",
        "primary_questions": [
            ("Can a porch be exempt from building regulations?", "Some porches can be exempt, but only if the details support that reading."),
            ("What details usually matter?", "Size, external doors, glazing, electrics and whether the existing front entrance remains properly separated."),
            ("What else should be checked?", "Planning permission limits are separate, especially size, height and highway-side position."),
        ],
        "answer_blocks": [
            {
                "title": "Direct answer",
                "body": "Treat a porch as a small project with two separate questions: whether the porch is exempt from building regulations, and whether it stays inside the planning limits.",
                "checks": ["Exemption position", "Planning limits", "Competent electrical or glazing work"],
            },
            {
                "title": "Before ordering",
                "body": "Ask the installer or building control body which compliance route they are relying on, then keep that answer with the quote and drawings.",
                "checks": ["Installer basis", "Compliance route", "Records kept"],
            },
        ],
        "official_sources": ["approval_needed", "how_to_apply", "application_information"],
        "related_routes": [
            {"title": "Building Control Route Checker", "href": "/tools/building-control-route-checker/", "description": "Check whether the porch route looks exempt, installer-led or building-control-led."},
            {"title": "Porches", "href": "/porches/", "description": "Check the planning route for porch size and siting."},
            {"title": "Building Regulations For Porches", "href": "/building-regulations/porches/", "description": "Read the main porch building regulations guide."},
            {"title": "Planning Route Check", "href": "/tools/planning-route-check/", "description": "Get a quick first steer on the planning route."},
        ],
    },
    {
        "slug": "temporary-structures",
        "title": "Temporary Structure Building Regulations",
        "meta_title": "Temporary structure building regulations in England",
        "meta_description": "Check temporary structure building regulations in England, including safety, services, use, planning permission and approval routes.",
        "intent": "temporary structure building regulations",
        "jurisdiction": "England",
        "project_slug": "temporary-buildings",
        "primary_questions": [
            ("Does temporary mean no building regulations?", "No. Temporary status does not automatically remove technical safety or approval questions."),
            ("What makes the route more formal?", "Regular occupation, public use, services, structural complexity or a weak removal plan can all increase risk."),
            ("How should I sequence it?", "Check planning use and duration first, then check whether building control or another safety route is needed."),
        ],
        "answer_blocks": [
            {
                "title": "Direct answer",
                "body": "A temporary structure should be assessed by how it is used, fixed, serviced and occupied, not only by how long the owner says it will stay.",
                "checks": ["Use", "Services", "Removal date"],
            },
            {
                "title": "Before installation",
                "body": "Set out the planned use, duration, access and services before asking building control or the council for the next route.",
                "checks": ["Use statement", "Site plan", "Approval route"],
            },
        ],
        "official_sources": ["approval_needed", "how_to_apply", "application_information"],
        "related_routes": [
            {"title": "Building Control Route Checker", "href": "/tools/building-control-route-checker/", "description": "Use this when safety, occupation, services or regularisation questions are live."},
            {"title": "Temporary Buildings", "href": "/temporary-buildings/", "description": "Check when the planning route becomes formal."},
            {"title": "Building Regulations For Temporary Buildings", "href": "/building-regulations/temporary-buildings/", "description": "Read the project-specific building regulations guide."},
            {"title": "Planning Timeline Planner", "href": "/tools/planning-timeline-planner/", "description": "Sequence approvals before dates become tight."},
        ],
    },
    {
        "slug": "loft-conversion-building-regulations",
        "title": "Loft Conversion Building Regulations",
        "meta_title": "Loft conversion building regulations: England checks",
        "meta_description": "Check loft conversion building regulations in England, including structure, fire safety, stairs, insulation and planning links.",
        "intent": "loft conversion building regulations search",
        "jurisdiction": "England",
        "project_slug": "loft-conversions",
        "primary_questions": [
            ("What is the fastest answer?", "Most loft conversions need building control because they change habitable space, structure and escape routes."),
            ("Can planning be ignored?", "No. Planning may still matter for dormers, roof alterations, conservation areas and Article 4 controls."),
            ("What should I avoid?", "Avoid paying for full drawings before the stairs, head height, roof form and planning route are credible."),
        ],
        "answer_blocks": [
            {
                "title": "Direct answer",
                "body": "A loft conversion is usually one of the clearest cases where building control matters even when planning permission may not.",
                "checks": ["Structure", "Stairs", "Fire safety"],
            },
            {
                "title": "Planning trigger",
                "body": "Roof changes, dormers and sensitive areas can make the planning route just as important as technical compliance.",
                "checks": ["Dormer design", "Roof visibility", "Local controls"],
            },
        ],
        "official_sources": ["approval_needed", "how_to_apply", "application_information"],
        "related_routes": [
            {"title": "Building Control Route Checker", "href": "/tools/building-control-route-checker/", "description": "Use this before deciding whether full plans are the safer loft route."},
            {"title": "Building Regulations For Loft Conversions", "href": "/building-regulations/loft-conversions/", "description": "Read the full loft-specific guide."},
            {"title": "Loft Conversions", "href": "/loft-conversions/", "description": "Check planning permission and permitted development."},
            {"title": "Drawings Cost Readiness Checker", "href": "/tools/drawings-cost-readiness-checker/", "description": "Check whether drawings are the right next spend."},
        ],
    },
    {
        "slug": "driveway-building-regulations",
        "title": "Driveway Building Regulations",
        "meta_title": "Driveway building regulations: drainage and access checks",
        "meta_description": "Check driveway building regulations, drainage, planning permission, dropped kerb and highway approval routes in England.",
        "intent": "driveway building regulations search",
        "jurisdiction": "England",
        "project_slug": "driveways",
        "primary_questions": [
            ("Is a driveway mainly building control?", "Usually no. The bigger approval questions are drainage, planning and highway access, especially for front gardens."),
            ("What can still go wrong?", "Non-permeable surfacing, poor drainage and missing dropped kerb approval can all create problems."),
            ("What should I ask first?", "Ask whether the surface is permeable, whether access over the pavement is needed and whether local planning controls apply."),
        ],
        "answer_blocks": [
            {
                "title": "Direct answer",
                "body": "Driveway searches often use building regulations wording when the real decision is drainage, planning permission or highway approval.",
                "checks": ["Surface water", "Planning route", "Highway approval"],
            },
            {
                "title": "Proof to keep",
                "body": "Keep the drainage specification, dropped kerb approval and any planning confirmation together with contractor details.",
                "checks": ["Drainage record", "Highway consent", "Planning evidence"],
            },
        ],
        "official_sources": ["approval_needed", "how_to_apply", "application_information"],
        "related_routes": [
            {"title": "Building Control Route Checker", "href": "/tools/building-control-route-checker/", "description": "Separate building-control, drainage, highway and planning route questions."},
            {"title": "Building Regulations For Driveways", "href": "/building-regulations/driveways/", "description": "Read the main driveway approval split."},
            {"title": "Driveways", "href": "/driveways/", "description": "Check the planning and drainage route."},
            {"title": "Dropped Kerbs", "href": "/dropped-kerbs/", "description": "Open this if vehicle access crosses the pavement."},
        ],
    },
    {
        "slug": "building-notice-vs-full-plans",
        "title": "Building Notice Vs Full Plans",
        "meta_title": "Building notice vs full plans: approval route check",
        "meta_description": "Compare building notice and full plans routes in England before choosing building control for home project work.",
        "intent": "building control application route",
        "jurisdiction": "England",
        "project_slug": "",
        "primary_questions": [
            ("What is this page for?", "Use it when the project clearly needs building control and the next question is which application route to discuss."),
            ("Does it replace advice from building control?", "No. It helps you prepare the right questions before contacting the building control body."),
            ("What should I decide first?", "Decide whether the design is stable enough for plans to be checked before work starts or whether the route is still too uncertain."),
        ],
        "answer_blocks": [
            {
                "title": "Direct answer",
                "body": "A full plans route is usually stronger when you want technical checking before work starts. A building notice route can be simpler for some domestic work, but it leaves more to be checked as the job progresses.",
                "checks": ["Design certainty", "Risk level", "Inspection sequence"],
            },
            {
                "title": "Planning link",
                "body": "Do not choose a building control route before the planning route is credible if the design itself may need permission or redesign.",
                "checks": ["Planning permission", "Drawings readiness", "Project risk"],
            },
        ],
        "official_sources": ["how_to_apply", "application_information", "approval_needed"],
        "related_routes": [
            {"title": "Building Control Route Checker", "href": "/tools/building-control-route-checker/", "description": "Run the route check before deciding whether full plans or building notice is the next conversation."},
            {"title": "Planning Application Readiness Checker", "href": "/tools/planning-application-readiness-checker/", "description": "Use this if the planning pack is still uncertain."},
            {"title": "Drawings Cost Readiness Checker", "href": "/tools/drawings-cost-readiness-checker/", "description": "Check whether drawings should be commissioned yet."},
            {"title": "Building Regulations Hub", "href": "/building-regulations/", "description": "Return to the building regulations pilot hub."},
        ],
    },
    {
        "slug": "completion-certificates",
        "title": "Building Regulations Completion Certificates",
        "meta_title": "Building regulations completion certificates: what to keep",
        "meta_description": "Check why building regulations completion evidence matters for home projects, sale, remortgage and future proof in England.",
        "intent": "completion certificate evidence",
        "jurisdiction": "England",
        "project_slug": "",
        "primary_questions": [
            ("Why do certificates matter?", "They help prove that building control was involved and that the work reached the relevant sign-off point."),
            ("When does missing evidence hurt?", "It often becomes painful during a sale, remortgage, insurance question or later regularisation discussion."),
            ("What should I keep?", "Keep applications, plans, inspection records, certificates and installer compliance records together."),
        ],
        "answer_blocks": [
            {
                "title": "Direct answer",
                "body": "Completion evidence is the paper trail that stops technical approval from becoming a memory test years later.",
                "checks": ["Application reference", "Inspection history", "Completion certificate or compliance evidence"],
            },
            {
                "title": "Planning link",
                "body": "Keep planning and building-control evidence together because future buyers and advisers may need to understand both routes.",
                "checks": ["Planning decision or LDC", "Building control sign-off", "Installer certificates"],
            },
        ],
        "official_sources": ["approval_needed", "how_to_apply", "application_information"],
        "related_routes": [
            {"title": "Building Control Route Checker", "href": "/tools/building-control-route-checker/", "description": "Use this to decide what evidence route should exist before completion is treated as settled."},
            {"title": "Evidence Pack Builder", "href": "/tools/evidence-pack-builder/", "description": "Build a checklist of the records to keep."},
            {"title": "Lawful Development Certificate Checker", "href": "/tools/lawful-development-certificate-checker/", "description": "Use this when planning proof may also be useful."},
            {"title": "What Happens After Planning Permission Is Approved?", "href": "/planning-faq/what-happens-after-planning-permission-is-approved/", "description": "Check the post-decision sequence."},
        ],
    },
    {
        "slug": "competent-person-schemes",
        "title": "Competent Person Schemes And Building Regulations",
        "meta_title": "Competent person schemes for building regulations",
        "meta_description": "Check when competent person schemes can self-certify building regulations compliance for home work in England.",
        "intent": "competent person scheme building regulations",
        "jurisdiction": "England",
        "project_slug": "",
        "primary_questions": [
            ("What is a competent person scheme?", "It is a route where a registered installer can self-certify certain work as compliant, instead of you making a separate building regulations application yourself."),
            ("What kind of work can this affect?", "Common examples include windows, boilers, heating systems, electrics and similar specialist work where registered installers can notify or certify the work."),
            ("What should I keep?", "Keep the installer details, scheme name, certificate, warranty and any notice or completion evidence with the rest of the project file."),
        ],
        "answer_blocks": [
            {
                "title": "Direct answer",
                "body": "For some home work in England, the practical route may be installer certification rather than a building notice or full plans application. The important thing is to confirm the installer is registered for the exact work and to keep the certificate after completion.",
                "checks": ["Registered installer", "Correct work category", "Certificate kept"],
            },
            {
                "title": "Planning link",
                "body": "Installer certification does not answer the planning question. Windows, doors, boilers, roof works or external changes can still need planning or listed-building checks in sensitive cases.",
                "checks": ["External change", "Listed building", "Conservation or Article 4 control"],
            },
        ],
        "official_sources": ["competent_person", "approval_needed", "how_to_apply"],
        "related_routes": [
            {"title": "Building Control Route Checker", "href": "/tools/building-control-route-checker/", "description": "Check whether competent person certification is likely to be the right route."},
            {"title": "Building Regulations Completion Certificates", "href": "/building-regulations/completion-certificates/", "description": "Use this to understand why certification evidence matters later."},
            {"title": "Evidence Pack Builder", "href": "/tools/evidence-pack-builder/", "description": "Keep installer certificates with the wider project records."},
        ],
    },
    {
        "slug": "regularisation-certificates",
        "title": "Building Regulations Regularisation Certificates",
        "meta_title": "Building regulations regularisation certificates in England",
        "meta_description": "Check when regularisation may help for past work without building regulations approval in England.",
        "intent": "building regulations regularisation certificate",
        "jurisdiction": "England",
        "project_slug": "",
        "primary_questions": [
            ("What is regularisation?", "It is a retrospective route for some work already carried out without building regulations approval, handled through a local authority building control body."),
            ("Is it guaranteed?", "No. Building control may need evidence, opening-up works or alterations before it can decide whether the work complies."),
            ("When does it usually come up?", "It often appears during sale, remortgage, insurance, enforcement or when owners realise older work has no completion evidence."),
        ],
        "answer_blocks": [
            {
                "title": "Direct answer",
                "body": "Regularisation is not a shortcut for live work. It is a way to deal with some past work where approval evidence is missing, and it may still involve investigation, remedial work and cost.",
                "checks": ["Work date", "Local authority route", "Evidence available"],
            },
            {
                "title": "Before you apply",
                "body": "Gather drawings, invoices, photos, installer certificates and any old correspondence before asking building control what it will need to inspect or verify.",
                "checks": ["Photos and invoices", "Installer records", "Possible opening-up work"],
            },
        ],
        "official_sources": ["how_to_apply", "approval_needed", "application_information"],
        "related_routes": [
            {"title": "Building Control Route Checker", "href": "/tools/building-control-route-checker/", "description": "Use this if the issue is missing approval for work already done."},
            {"title": "Building Regulations Completion Certificates", "href": "/building-regulations/completion-certificates/", "description": "Understand what evidence should ideally exist."},
            {"title": "Evidence Pack Builder", "href": "/tools/evidence-pack-builder/", "description": "Build the missing-evidence pack before contacting building control."},
        ],
    },
    {
        "slug": "before-you-start-checklist",
        "title": "Building Regulations Before You Start Checklist",
        "meta_title": "Building regulations checklist before work starts",
        "meta_description": "Use a practical England building regulations checklist before home project work starts, including route, drawings and evidence.",
        "intent": "building regulations checklist before work starts",
        "jurisdiction": "England",
        "project_slug": "",
        "primary_questions": [
            ("What should be clear before work starts?", "Know whether the project needs building control, whether planning is settled, what drawings or specifications are needed, and who is responsible for inspections."),
            ("What is the biggest avoidable mistake?", "Covering up work before inspection or assuming a contractor's confidence is the same as written compliance evidence."),
            ("What should I save from day one?", "Save the route decision, drawings, specifications, inspection plan, contractor details and any official correspondence."),
        ],
        "answer_blocks": [
            {
                "title": "Direct answer",
                "body": "Before work starts, the useful building regulations checklist is simple: confirm the route, confirm the technical information needed, confirm inspection responsibility, and keep proof as the job progresses.",
                "checks": ["Route chosen", "Information ready", "Inspection plan"],
            },
            {
                "title": "Planning link",
                "body": "Do not let a tidy building-control checklist hide a live planning problem. If the design may need permission, settle that before construction commitments become hard to unwind.",
                "checks": ["Planning route", "Local constraints", "Project evidence"],
            },
        ],
        "official_sources": ["approval_needed", "how_to_apply", "application_information", "competent_person"],
        "related_routes": [
            {"title": "Building Control Route Checker", "href": "/tools/building-control-route-checker/", "description": "Run the quick route check before work starts."},
            {"title": "Project Roadmap Builder", "href": "/tools/project-roadmap-builder/", "description": "Sequence planning, building control, drawings and evidence."},
            {"title": "Evidence Pack Builder", "href": "/tools/evidence-pack-builder/", "description": "Create the practical record-keeping list."},
        ],
    },
    {
        "slug": "structural-calculations",
        "title": "Structural Calculations And Building Regulations",
        "meta_title": "Structural calculations for building regulations",
        "meta_description": "Check when structural calculations may be needed for building regulations approval in England.",
        "intent": "structural calculations building regulations",
        "jurisdiction": "England",
        "project_slug": "",
        "primary_questions": [
            ("When do structural calculations matter?", "They usually matter when work changes how loads are carried, such as beams, openings, loft floors, roof changes, extensions or removed walls."),
            ("Who decides whether they are enough?", "Building control or the registered building control approver will decide what technical information is needed for the route being used."),
            ("Can planning permission still matter?", "Yes. A structurally sound proposal can still need planning permission if the development itself is not permitted or locally acceptable."),
        ],
        "answer_blocks": [
            {
                "title": "Direct answer",
                "body": "Structural calculations are often the bridge between a nice drawing and a buildable building regulations submission. Use them when the work affects beams, walls, floors, roofs or foundations.",
                "checks": ["Load-bearing change", "Engineer input", "Building-control route"],
            },
            {
                "title": "Before you pay",
                "body": "Ask whether the engineer needs measured drawings, opening sizes, foundation assumptions, roof details or existing wall information before calculating anything.",
                "checks": ["Measured dimensions", "Existing structure", "Design assumptions"],
            },
        ],
        "official_sources": ["approved_documents", "application_information", "approval_needed"],
        "related_routes": [
            {"title": "Building Control Route Checker", "href": "/tools/building-control-route-checker/", "description": "Use this when structural work makes the approval route unclear."},
            {"title": "Building Notice Vs Full Plans", "href": "/building-regulations/building-notice-vs-full-plans/", "description": "Compare routes before relying on work being checked on site."},
            {"title": "Drawings Cost Readiness Checker", "href": "/tools/drawings-cost-readiness-checker/", "description": "Check whether drawings and calculations are the right next spend."},
        ],
    },
    {
        "slug": "building-control-inspections",
        "title": "Building Control Inspections",
        "meta_title": "Building control inspections: what to expect",
        "meta_description": "Check what building control inspections are for and what evidence to keep during home work in England.",
        "intent": "building control inspections",
        "jurisdiction": "England",
        "project_slug": "",
        "primary_questions": [
            ("What are inspections for?", "They let the building control body check important stages before work is covered up or treated as complete."),
            ("Who books them?", "That depends on the arrangement with your builder and building control body, so confirm responsibility before work starts."),
            ("What should I keep?", "Keep inspection dates, photos, notes, emails, certificates and any change instructions with the project file."),
        ],
        "answer_blocks": [
            {
                "title": "Direct answer",
                "body": "Inspections are not admin decoration. They are how hidden work, stage checks and completion evidence stay connected to the building regulations route.",
                "checks": ["Inspection stages", "Booking responsibility", "Completion evidence"],
            },
            {
                "title": "Practical risk",
                "body": "The common mistake is covering work up before the right inspection has happened, then trying to prove compliance later from memory.",
                "checks": ["Do not cover too early", "Take photos", "Save written advice"],
            },
        ],
        "official_sources": ["how_to_apply", "application_information", "approval_needed"],
        "related_routes": [
            {"title": "Before You Start Checklist", "href": "/building-regulations/before-you-start-checklist/", "description": "Use this to set inspection responsibilities before work starts."},
            {"title": "Completion Certificates", "href": "/building-regulations/completion-certificates/", "description": "Understand what the inspection trail should lead to."},
            {"title": "Evidence Pack Builder", "href": "/tools/evidence-pack-builder/", "description": "Create the record-keeping list before work is hidden."},
        ],
    },
    {
        "slug": "drawings-and-specifications",
        "title": "Building Regulations Drawings And Specifications",
        "meta_title": "Building regulations drawings and specifications",
        "meta_description": "Check what drawings and specifications may be needed for a building control application in England.",
        "intent": "building regulations drawings specifications",
        "jurisdiction": "England",
        "project_slug": "",
        "primary_questions": [
            ("Are planning drawings enough?", "Not always. Planning drawings show the proposal for planning judgement; building regulations drawings usually need more technical detail."),
            ("What extra detail may matter?", "Structure, insulation, ventilation, drainage, fire safety, materials, dimensions and specification notes can all be relevant."),
            ("When should I commission them?", "Commission technical drawings when the planning route and design are stable enough that the details are unlikely to be wasted."),
        ],
        "answer_blocks": [
            {
                "title": "Direct answer",
                "body": "Building regulations drawings should explain how the work will comply, not just what it will look like. That often means sections, notes, specifications and structural detail.",
                "checks": ["Technical sections", "Specification notes", "Compliance detail"],
            },
            {
                "title": "Spend-order check",
                "body": "If planning permission might still change the design, do not rush into full technical drawings before the route is credible.",
                "checks": ["Planning route", "Design stability", "Building-control route"],
            },
        ],
        "official_sources": ["application_information", "approved_documents", "how_to_apply"],
        "related_routes": [
            {"title": "Drawings Cost Readiness Checker", "href": "/tools/drawings-cost-readiness-checker/", "description": "Use this before paying for drawings too early."},
            {"title": "Project Requirements Generator", "href": "/tools/project-requirements-generator/", "description": "Build the wider preparation pack."},
            {"title": "Building Control Route Checker", "href": "/tools/building-control-route-checker/", "description": "Check which route the drawings need to support."},
        ],
    },
    {
        "slug": "drainage-and-waste",
        "title": "Drainage And Waste Building Regulations",
        "meta_title": "Drainage building regulations for home projects",
        "meta_description": "Check drainage and waste building regulations issues for extensions, bathrooms, driveways and home work in England.",
        "intent": "drainage building regulations",
        "jurisdiction": "England",
        "project_slug": "",
        "primary_questions": [
            ("When does drainage trigger building regulations?", "Drainage can matter when extensions, bathrooms, kitchens, utility rooms, hard surfaces or new connections affect waste or surface water."),
            ("Is it the same as planning permission?", "No. Drainage can sit alongside planning, highway, sewer or building control questions depending on the work."),
            ("What should be checked early?", "Check existing drain positions, surface water route, sewer ownership, connection points and whether work will be inspected."),
        ],
        "answer_blocks": [
            {
                "title": "Direct answer",
                "body": "Drainage is one of the quickest ways for a simple-looking project to become technical. Treat foul drainage, surface water and highway run-off as separate questions.",
                "checks": ["Foul drainage", "Surface water", "Inspection route"],
            },
            {
                "title": "Planning link",
                "body": "Driveways and front garden works often look like building-regulations searches, but the real issue may be drainage, planning permission or highway approval.",
                "checks": ["Permeable surface", "Sewer or drain route", "Highway access"],
            },
        ],
        "official_sources": ["approved_documents", "approval_needed", "application_information"],
        "related_routes": [
            {"title": "Driveway Building Regulations", "href": "/building-regulations/driveway-building-regulations/", "description": "Use this where drainage and hardstanding are being confused."},
            {"title": "Building Regulations For Extensions", "href": "/building-regulations/extensions/", "description": "Use this when extension drainage is part of the project."},
            {"title": "Driveways", "href": "/driveways/", "description": "Check the planning and drainage route for hard surfaces."},
        ],
    },
    {
        "slug": "windows-and-doors",
        "title": "Windows And Doors Building Regulations",
        "meta_title": "Windows and doors building regulations in England",
        "meta_description": "Check building regulations, competent person certification and planning links for replacing windows and doors in England.",
        "intent": "windows doors building regulations",
        "jurisdiction": "England",
        "project_slug": "windows-and-doors",
        "primary_questions": [
            ("Do replacement windows and doors need building regulations?", "They can. Many replacements are handled through competent person certification, but the route depends on the work and installer."),
            ("Does installer certification settle planning?", "No. Planning, conservation area and listed-building controls can still matter for external appearance or historic fabric."),
            ("What proof should I keep?", "Keep the installer certificate, guarantee, product details and any planning or listed-building evidence together."),
        ],
        "answer_blocks": [
            {
                "title": "Direct answer",
                "body": "For replacement windows and doors, the practical building regulations route is often competent person certification. Confirm the installer is registered for the exact work and keep the certificate.",
                "checks": ["Registered installer", "Correct certification", "Certificate kept"],
            },
            {
                "title": "Planning link",
                "body": "External appearance can still be controlled by planning permission, conservation area rules, Article 4 directions or listed-building consent.",
                "checks": ["External appearance", "Conservation area", "Listed building"],
            },
        ],
        "official_sources": ["competent_person", "approval_needed", "approved_documents"],
        "related_routes": [
            {"title": "Windows And Doors", "href": "/windows-and-doors/", "description": "Check the planning route for replacement or altered openings."},
            {"title": "Competent Person Schemes", "href": "/building-regulations/competent-person-schemes/", "description": "Use this where installer certification is the likely route."},
            {"title": "Completion Certificates", "href": "/building-regulations/completion-certificates/", "description": "Understand what proof to keep after completion."},
        ],
    },
    {
        "slug": "roof-lights",
        "title": "Roof Lights Building Regulations",
        "meta_title": "Roof light building regulations in England",
        "meta_description": "Check building regulations and planning links for roof lights, roof windows and related roof work in England.",
        "intent": "roof light building regulations",
        "jurisdiction": "England",
        "project_slug": "roof-lights",
        "primary_questions": [
            ("Do roof lights need building regulations approval?", "They can, especially where structure, thermal performance, weathering, fire safety or roof work is involved."),
            ("Is planning permission separate?", "Yes. Roof lights can still raise planning issues if they face the highway, alter the roof form, or sit in a sensitive area."),
            ("What should be checked before cutting the roof?", "Check structure, product specification, position, weathering, insulation and whether building control or installer certification applies."),
        ],
        "answer_blocks": [
            {
                "title": "Direct answer",
                "body": "A roof light is not just a window dropped into a roof. Cutting, weathering and insulating the opening can make building regulations relevant.",
                "checks": ["Roof structure", "Weathering", "Thermal performance"],
            },
            {
                "title": "Planning link",
                "body": "Planning can still matter where roof lights are prominent, front-facing, in a conservation area or part of a wider loft conversion.",
                "checks": ["Roof visibility", "Sensitive area", "Wider loft route"],
            },
        ],
        "official_sources": ["approved_documents", "approval_needed", "competent_person"],
        "related_routes": [
            {"title": "Roof Lights", "href": "/roof-lights/", "description": "Check the planning route for roof windows."},
            {"title": "Roof Alterations", "href": "/roof-alterations/", "description": "Use this when the roof change is more visible or extensive."},
            {"title": "Loft Conversion Building Regulations", "href": "/building-regulations/loft-conversions/", "description": "Open this if the roof light is part of a loft conversion."},
        ],
    },
    {
        "slug": "solar-panels",
        "title": "Solar Panel Building Regulations",
        "meta_title": "Solar panel building regulations in England",
        "meta_description": "Check building regulations, electrical certification, roof loading and planning links for solar panels in England.",
        "intent": "solar panel building regulations",
        "jurisdiction": "England",
        "project_slug": "solar-panels",
        "primary_questions": [
            ("Can solar panels involve building regulations?", "Yes. Electrical safety, roof loading, fixing, fire considerations and installer certification can all matter."),
            ("Does permitted development settle everything?", "No. Planning permission and building regulations are separate, and sensitive sites can still need closer checks."),
            ("What proof should I keep?", "Keep installer accreditation details, electrical certificates, product information, warranties and any planning evidence."),
        ],
        "answer_blocks": [
            {
                "title": "Direct answer",
                "body": "For solar panels, the practical route usually combines installer competence, electrical certification and roof suitability rather than a single yes-or-no approval label.",
                "checks": ["Installer competence", "Electrical certification", "Roof suitability"],
            },
            {
                "title": "Planning link",
                "body": "Planning can still matter for prominent panels, listed buildings, conservation areas and other sensitive settings.",
                "checks": ["Visual impact", "Heritage sensitivity", "Planning route"],
            },
        ],
        "official_sources": ["competent_person", "approved_documents", "approval_needed"],
        "related_routes": [
            {"title": "Solar Panels", "href": "/solar-panels/", "description": "Check the planning side of solar panel installation."},
            {"title": "Competent Person Schemes", "href": "/building-regulations/competent-person-schemes/", "description": "Use this when installer certification is part of the route."},
            {"title": "Evidence Pack Builder", "href": "/tools/evidence-pack-builder/", "description": "Keep the installation and compliance evidence together."},
        ],
    },
    {
        "slug": "heat-pumps",
        "title": "Heat Pump Building Regulations",
        "meta_title": "Heat pump building regulations in England",
        "meta_description": "Check heat pump building regulations, installer certification, electrics, noise and planning links in England.",
        "intent": "heat pump building regulations",
        "jurisdiction": "England",
        "project_slug": "heat-pumps",
        "primary_questions": [
            ("Can heat pumps involve building regulations?", "Yes. Heating systems, electrics, ventilation, energy performance and installer certification can all matter."),
            ("Is planning permission separate?", "Yes. Heat pumps can have planning conditions around siting, size, noise and sensitive locations."),
            ("What should be kept after installation?", "Keep installer certificates, commissioning records, product details, warranties and any planning evidence."),
        ],
        "answer_blocks": [
            {
                "title": "Direct answer",
                "body": "A heat pump is usually both a technical installation and a planning question. The building regulations side should cover safe, competent installation and the right compliance records.",
                "checks": ["Installer certification", "Electrical route", "Commissioning records"],
            },
            {
                "title": "Planning link",
                "body": "Planning can still matter where the unit is close to boundaries, visually prominent, noisy, or on a sensitive building or site.",
                "checks": ["Siting", "Noise", "Sensitive location"],
            },
        ],
        "official_sources": ["competent_person", "approved_documents", "approval_needed"],
        "related_routes": [
            {"title": "Heat Pumps", "href": "/heat-pumps/", "description": "Check the planning route for heat pump siting and restrictions."},
            {"title": "Competent Person Schemes", "href": "/building-regulations/competent-person-schemes/", "description": "Use this when registered installer certification is part of the route."},
            {"title": "Local Constraint Finder", "href": "/tools/local-constraint-finder/", "description": "Check whether local designations could affect the planning route."},
        ],
    },
]


BUILDING_REGULATIONS_PAGE_BY_SLUG = {
    page["slug"]: page for page in BUILDING_REGULATIONS_PAGES
}


def building_regulations_path(page: dict) -> str:
    slug = str(page.get("slug", "")).strip("/")
    if slug == "index":
        return "/building-regulations/"
    return f"/building-regulations/{slug}/"
