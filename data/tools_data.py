from data.scenario_data import SCENARIOS


STANDALONE_TOOLS = [
    {
        "slug": "planning-decision-tool",
        "title": "Do I Need Planning Permission?",
        "summary": "Work through a structured project check to see whether the scheme looks likely permitted development, may need planning permission, or depends on local constraints.",
        "component": "planning_decision_tool",
        "meta_title": "Do I Need Planning Permission? Decision Engine",
        "meta_description": "Use the Planning Decision Engine to check whether a home project looks likely permitted development, needs planning permission, or depends on local constraints.",
        "hero_intro": "Use the Planning Decision Engine to sense-check the route for a home project before you spend money on drawings, applications or contractor quotes. It weighs the project type, property type, scale and local constraints, then points you to the most useful next page.",
        "hero_badges": [
            "Structured inputs only",
            "Static rule-based result",
            "Best for early project triage",
        ],
        "search_intents": [
            "Do I need planning permission for this project?",
            "Could this still be permitted development?",
            "Is this a borderline scheme worth checking formally?",
            "Could local constraints change the normal answer?",
        ],
        "calculator_heading": "Run The Planning Decision Engine",
        "calculator_intro": "Work through the steps, review the answers, then let the tool check the most common planning triggers for your project.",
        "explanation_cards": [
            {
                "title": "What it answers well",
                "body": "It gives a practical first steer on whether a project still looks comfortably inside the simpler route or whether planning permission is becoming more likely.",
            },
            {
                "title": "What usually changes the answer",
                "body": "Property type, local designations, previous additions and measurements close to a threshold are the factors most likely to move the result.",
            },
            {
                "title": "What to do with the result",
                "body": "Treat the answer as structured triage, then open the matching project guide, planning topic or local authority page before you rely on it.",
            },
        ],
        "guidance_links": [
            {
                "title": "Planning Permission",
                "href": "/planning-permission/",
                "description": "Open this when the engine points toward a formal route or a borderline answer.",
            },
            {
                "title": "Permitted Development",
                "href": "/permitted-development/",
                "description": "Use this to understand the baseline rights the engine is checking against.",
            },
            {
                "title": "House Extensions",
                "href": "/house-extensions/",
                "description": "Helpful when the project is an extension and the dimensions are driving the uncertainty.",
            },
            {
                "title": "Loft Conversions",
                "href": "/loft-conversions/",
                "description": "A strong next read for roof changes, dormers and loft enlargements.",
            },
            {
                "title": "Outbuildings",
                "href": "/outbuildings/",
                "description": "Use this for garden rooms, sheds and other detached buildings in the garden.",
            },
            {
                "title": "Local Authorities",
                "href": "/councils/",
                "description": "Best when conservation areas, Article 4 or heritage controls may change the normal answer.",
            },
        ],
        "faq_links": [
            {
                "title": "Planning Permission Vs Permitted Development",
                "href": "/planning-faq/planning-permission-vs-permitted-development/",
                "description": "Read this when the route still sits between the simpler householder answer and a formal application.",
            },
            {
                "title": "Lawful Development Certificate Vs Planning Permission",
                "href": "/planning-faq/lawful-development-certificate-vs-planning-permission/",
                "description": "Useful when the route looks simpler on paper but formal written proof may still be worth it.",
            },
            {
                "title": "Do I Need Planning Permission?",
                "href": "/planning-faq/do-i-need-planning-permission/",
                "description": "Read the broader route guide if you want the same decision explained in plainer language.",
            },
        ],
    },
    {
        "slug": "planning-route-check",
        "title": "Planning Route Check",
        "summary": "Answer a short set of homeowner questions and get a cautious first-pass route for permitted development, planning permission, council approvals and professional review.",
        "component": "planning_route_check_tool",
        "meta_title": "Planning Route Check | UK Planning Guide",
        "meta_description": "Answer a few project questions and get a simple planning route check for permission, permitted development, conservation areas and dropped kerbs.",
        "hero_intro": "Use the Planning Route Check when you want a calm first steer before spending money on drawings, applications or contractor conversations. It gives an instant result without asking for contact details, then offers an optional help request only after the guidance has been shown.",
        "hero_badges": [
            "No contact details needed",
            "Static rule-based result",
            "Optional help request after the result",
        ],
        "search_intents": [
            "Planning route check",
            "Do I need planning permission?",
            "Permitted development checker",
            "Planning permission checker UK",
            "Garden room planning permission checker",
            "Dropped kerb planning permission",
            "Extension planning permission checker",
        ],
        "calculator_heading": "Run The Planning Route Check",
        "calculator_intro": "Answer the project, property, location and restriction questions. The result is general guidance only and should be checked with your council or a suitable professional where the project is restricted or borderline.",
        "explanation_cards": [
            {
                "title": "What it gives you",
                "body": "A likely planning route, confidence level, reasons, watch-outs and next steps based on the answers you provide.",
            },
            {
                "title": "What it does not do",
                "body": "It does not make a legal decision or guarantee that permission is or is not required for one exact property.",
            },
            {
                "title": "When to ask for help",
                "body": "Use the optional help request when the result points toward restrictions, drawings, a formal application, highways approval or professional review.",
            },
        ],
        "guidance_links": [
            {
                "title": "Planning Permission",
                "href": "/planning-permission/",
                "description": "Useful when the route check points toward a formal application or a more cautious council check.",
            },
            {
                "title": "Permitted Development",
                "href": "/permitted-development/",
                "description": "Use this when the route check says permitted development may be possible but still needs limits checked.",
            },
            {
                "title": "Conservation Areas",
                "href": "/conservation-areas/",
                "description": "Open this if the property is in a conservation area or the result highlights heritage sensitivity.",
            },
            {
                "title": "Listed Buildings",
                "href": "/listed-buildings/",
                "description": "Use this when listed status may create a separate consent route.",
            },
            {
                "title": "Dropped Kerbs",
                "href": "/dropped-kerbs/",
                "description": "A strong follow-up where the route check points to highway or vehicle-access approval.",
            },
            {
                "title": "Planning Help",
                "href": "/planning-help/",
                "description": "Read the honest help route if you want to understand optional enquiry support without a guaranteed match claim.",
            },
        ],
        "faq_links": [
            {
                "title": "Planning Permission Vs Permitted Development",
                "href": "/planning-faq/planning-permission-vs-permitted-development/",
                "description": "Read this when the result sits between the simpler route and a formal application.",
            },
            {
                "title": "Lawful Development Certificate Vs Planning Permission",
                "href": "/planning-faq/lawful-development-certificate-vs-planning-permission/",
                "description": "Useful when permitted development may be possible but formal proof would reduce risk.",
            },
            {
                "title": "Do I Need Planning Permission?",
                "href": "/planning-faq/do-i-need-planning-permission/",
                "description": "A broader plain-English guide to the core route question.",
            },
        ],
    },
    {
        "slug": "building-control-route-checker",
        "title": "Building Control Route Checker",
        "summary": "Choose the next building regulations route to discuss: full plans, building notice, competent person certification, regularisation or a planning-first pause.",
        "component": "custom_planning_tool",
        "meta_title": "Building Control Route Checker | Building regulations tool",
        "meta_description": "Check whether a home project in England should ask about full plans, building notice, competent person schemes, regularisation or planning first.",
        "hero_intro": "Use this when planning and building regulations are starting to blur together. It gives a practical route steer before you contact building control, book a contractor, or assume an installer certificate will be enough.",
        "hero_badges": [
            "England-first",
            "Building control triage",
            "No login",
        ],
        "search_intents": [
            "Building control route checker",
            "Building notice or full plans?",
            "Do I need building regulations approval?",
            "Competent person scheme or building control?",
            "Regularisation certificate checker",
        ],
        "calculator_heading": "Check The Building Control Route",
        "calculator_intro": "Answer the project, work stage, planning status and evidence questions. The result points to the building-control conversation most worth having next.",
        "explanation_cards": [
            {
                "title": "What it answers well",
                "body": "It helps separate ordinary pre-start building control, competent person certification, regularisation and planning-first situations.",
            },
            {
                "title": "What it does not decide",
                "body": "It does not approve the work, replace your building control body, or prove that planning permission is unnecessary.",
            },
            {
                "title": "Best next move",
                "body": "Open the matching building regulations guide, then ask building control or the registered installer exactly what evidence will exist at completion.",
            },
        ],
        "guidance_links": [
            {"title": "Building Regulations Hub", "href": "/building-regulations/", "description": "Start here if you need the wider planning-versus-building-regulations split."},
            {"title": "Before You Start Checklist", "href": "/building-regulations/before-you-start-checklist/", "description": "Use this before construction work begins."},
            {"title": "Building Notice Vs Full Plans", "href": "/building-regulations/building-notice-vs-full-plans/", "description": "Compare the two common pre-start building-control routes."},
            {"title": "Competent Person Schemes", "href": "/building-regulations/competent-person-schemes/", "description": "Use this when installer self-certification may be the right route."},
            {"title": "Regularisation Certificates", "href": "/building-regulations/regularisation-certificates/", "description": "Use this when work has already been done without clear evidence."},
            {"title": "Completion Certificates", "href": "/building-regulations/completion-certificates/", "description": "Understand what evidence should be kept after completion."},
        ],
        "faq_links": [
            {"title": "Planning Permission Vs Building Regulations", "href": "/planning-faq/planning-permission-vs-building-regulations/", "description": "Use this if the two approval systems are still being mixed together."},
            {"title": "Building Regulations For Extensions", "href": "/planning-faq/building-regulations-for-extensions/", "description": "Useful when an extension is the live project."},
            {"title": "Temporary Buildings Building Regulations", "href": "/planning-faq/temporary-buildings-building-regulations/", "description": "Useful when temporary use or occupation is the question."},
        ],
    },
    {
        "slug": "what-can-i-build-explorer",
        "title": "What Can I Build? Explorer",
        "summary": "Explore the home project types that are most likely to fit your property before you dive into detailed planning checks.",
        "component": "what_can_i_build_explorer_tool",
        "meta_title": "What Can I Build? Explorer",
        "meta_description": "Use the What Can I Build? Explorer to see which home project types are most likely to fit your property under broad planning and permitted development rules.",
        "hero_intro": "Use this tool when you are still exploring possibilities rather than validating one measured scheme. It helps you move from a simple property setup into a shortlist of project types that are worth checking next, without drowning you in legal detail.",
        "hero_badges": [
            "Exploratory, not technical",
            "Structured rule-based shortlist",
            "Built to feed into the decision tool",
        ],
        "search_intents": [
            "What can I build on this property?",
            "What project type looks most realistic here?",
            "Should I start with an extension, loft or outbuilding?",
            "Which home improvement options are worth checking next?",
        ],
        "calculator_heading": "Explore What Could Fit",
        "calculator_intro": "Choose the property type, describe the amount of space, add any obvious features or local sensitivity, then explore the most likely project options.",
        "explanation_cards": [
            {
                "title": "What it answers well",
                "body": "It helps you move from a vague idea like 'what could we do with this house?' into a shortlist of project types that usually make sense for this setup.",
            },
            {
                "title": "What it does not try to do",
                "body": "It does not replace measured project checks, local verification or the stricter route-based logic in the decision engine.",
            },
            {
                "title": "Best next move",
                "body": "Pick the project option that feels closest to your goal, then open the guide or run that option through the Planning Decision Engine for a deeper check.",
            },
        ],
        "guidance_links": [
            {
                "title": "Planning Decision Engine",
                "href": "/tools/planning-decision-tool/",
                "description": "Use this once one of the explorer options starts to look serious and you want a stricter route check.",
            },
            {
                "title": "Planning Rejection Risk Analyzer",
                "href": "/tools/planning-rejection-risk-analyzer/",
                "description": "A strong follow-on if you are already leaning toward a particular scheme and want to stress-test refusal risks.",
            },
            {
                "title": "House Extensions",
                "href": "/house-extensions/",
                "description": "Useful when your shortlist is pointing toward extensions rather than roof or outbuilding options.",
            },
            {
                "title": "Loft Conversions",
                "href": "/loft-conversions/",
                "description": "Open this if roof space is one of the clearest opportunities the explorer is surfacing.",
            },
            {
                "title": "Outbuildings",
                "href": "/outbuildings/",
                "description": "Helpful when the result is pointing toward garden rooms and detached structures.",
            },
            {
                "title": "Permitted Development",
                "href": "/permitted-development/",
                "description": "Use this for the baseline rules behind the broad exploratory result.",
            },
        ],
        "faq_links": [
            {
                "title": "Planning Permission Vs Permitted Development",
                "href": "/planning-faq/planning-permission-vs-permitted-development/",
                "description": "Open this when the shortlist is narrowing but the approval route still feels mixed.",
            },
            {
                "title": "What Counts As The Original House?",
                "href": "/planning-faq/what-counts-as-the-original-house/",
                "description": "Useful when site history and previous additions may change what is still realistic.",
            },
            {
                "title": "Is Pre-Application Advice Worth It?",
                "href": "/planning-faq/is-pre-application-advice-worth-it/",
                "description": "Useful when one option is starting to look serious enough that early council feedback may be worth the time.",
            },
        ],
    },
    {
        "slug": "extension-value-estimator",
        "title": "Extension Value Estimator",
        "summary": "Estimate likely property value uplift from extension-led projects using project type, size, finish level and planning confidence.",
        "component": "extension_value_estimator_tool",
        "meta_title": "Extension Value Estimator: planning-aware uplift tool",
        "meta_description": "Use the Extension Value Estimator to estimate likely property value uplift from common extension-led projects with planning-aware confidence bands.",
        "hero_intro": "Use this tool when the planning route and likely value uplift need to be looked at together. It gives a cautious range for value added based on project type, added space, finish and planning confidence, then points you to the pages most worth opening next.",
        "hero_badges": [
            "Planning-aware value guide",
            "Static rule-based range",
            "Not a formal valuation",
        ],
        "search_intents": [
            "How much value does an extension add?",
            "Is this extension worth it?",
            "How much value does a loft conversion add?",
            "Does planning permission affect value uplift?",
            "How much value does a side extension add?",
            "Which extension adds the most value?",
        ],
        "calculator_heading": "Estimate The Likely Value Uplift",
        "calculator_intro": "Enter the current property value, choose the project type, add the likely floor area and finish level, then let the tool estimate a guided uplift range.",
        "explanation_cards": [
            {
                "title": "What it answers well",
                "body": "It gives a practical value-added range for common extension-led projects before you rely on rough one-line rules or salesy ROI claims.",
            },
            {
                "title": "What changes the estimate most",
                "body": "Project type, added area, bedroom gain, finish level and planning certainty do most of the work in the range this tool produces.",
            },
            {
                "title": "What it does not do",
                "body": "It does not model postcode-level market conditions or replace a valuation survey, estate-agent opinion or lender valuation.",
            },
        ],
        "guidance_links": [
            {
                "title": "House Extensions",
                "href": "/house-extensions/",
                "description": "Useful when the value question still depends on the extension route itself.",
            },
            {
                "title": "Loft Conversions",
                "href": "/loft-conversions/",
                "description": "Helpful for loft projects, bedroom gain and upper-floor value questions.",
            },
            {
                "title": "Planning Permission",
                "href": "/planning-permission/",
                "description": "Open this when planning certainty is still the main thing affecting how realistic the value upside feels.",
            },
            {
                "title": "Permitted Development",
                "href": "/permitted-development/",
                "description": "Useful when the simpler route still looks plausible and confidence is part of the value equation.",
            },
            {
                "title": "Two Storey Extensions",
                "href": "/two-storey-extensions/",
                "description": "A strong next read where added floor area and bedroom gain are the main sources of uplift.",
            },
            {
                "title": "Rear Extensions",
                "href": "/rear-extensions/",
                "description": "Helpful when the likely uplift depends on a more mainstream rear extension route.",
            },
        ],
        "faq_links": [
            {
                "title": "Does An Extension Add Value To A House?",
                "href": "/planning-faq/does-an-extension-add-value-to-a-house/",
                "description": "Read the broader guide if you want the value question explained in plainer language first.",
            },
            {
                "title": "Extension Cost Vs Value Added",
                "href": "/planning-faq/extension-cost-vs-value-added/",
                "description": "Useful when the real question is whether the likely uplift justifies the spend rather than just whether value rises at all.",
            },
            {
                "title": "Which Extension Adds The Most Value?",
                "href": "/planning-faq/which-extension-adds-the-most-value/",
                "description": "Useful when you are comparing several project routes before committing to one.",
            },
        ],
    },
    {
        "slug": "permitted-development-calculator",
        "title": "Permitted Development Calculator",
        "summary": "Estimate whether a common home project may fit within permitted development rules.",
        "component": "pd_calculator",
        "search_intents": [
            "Could this project be permitted development?",
            "Does this proposal still fit the simpler planning route?",
            "What usually pushes a scheme out of PD?",
        ],
        "faq_links": [
            {
                "title": "When A Lawful Development Certificate Is Worth It",
                "href": "/planning-faq/lawful-development-certificate/",
                "description": "Useful when the scheme may be permitted development but you want formal proof before building.",
            },
            {
                "title": "What Counts As The Original House?",
                "href": "/planning-faq/what-counts-as-the-original-house/",
                "description": "Helpful when previous additions may affect how much allowance is left.",
            },
        ],
    },
    {
        "slug": "planning-rejection-risk-analyzer",
        "title": "Planning Rejection Risk Analyzer",
        "summary": "Analyse the main refusal risks for a home project, including scale, neighbour impact, design character and local policy constraints.",
        "component": "planning_rejection_risk_tool",
        "meta_title": "Planning Rejection Risk Analyzer",
        "meta_description": "Use a structured planning rejection risk analyzer to see the main refusal risks for a home project and what could reduce them before submission.",
        "hero_intro": "Use this tool once the project route is starting to look real and you want to understand the objections most likely to derail a planning application. It uses the same structured project model as the Planning Decision Engine, but focuses on refusal risks, not permission route.",
        "hero_badges": [
            "Refusal-risk focused",
            "Structured rule analysis",
            "Built on the decision engine pattern",
        ],
        "search_intents": [
            "Could this application be refused?",
            "What are the main planning objections here?",
            "Will neighbour impact or design character be a problem?",
            "Which part of the proposal is most likely to trigger resistance?",
        ],
        "calculator_heading": "Run The Rejection Risk Analysis",
        "calculator_intro": "Work through the same style of project questions, then let the tool surface the refusal risks that are most likely to matter.",
        "explanation_cards": [
            {
                "title": "What it answers well",
                "body": "It helps you spot the planning objections a council is most likely to raise, such as bulk, privacy, design character, parking or heritage impact.",
            },
            {
                "title": "Why it is useful early",
                "body": "You can use it before drawings are final to see which design choices are most likely to need rethinking before an application goes in.",
            },
            {
                "title": "Best next move",
                "body": "Use the output to reduce the weak points in the proposal, then open the matching project guide, local authority layer or decision tool if the route still needs checking.",
            },
        ],
        "guidance_links": [
            {
                "title": "Planning Decision Engine",
                "href": "/tools/planning-decision-tool/",
                "description": "Use this first if you still need to confirm whether planning permission is probably required.",
            },
            {
                "title": "Planning Permission",
                "href": "/planning-permission/",
                "description": "Helpful when refusal risk is clearly pushing the project toward a formal application route.",
            },
            {
                "title": "Boundary Rules",
                "href": "/boundary-rules/",
                "description": "Useful where neighbour impact or boundary siting is driving the risk profile.",
            },
            {
                "title": "Conservation Areas",
                "href": "/conservation-areas/",
                "description": "A strong next read when heritage or local character controls may tighten the planning response.",
            },
            {
                "title": "House Extensions",
                "href": "/house-extensions/",
                "description": "Useful for broader extension design context where scale and appearance are the main issues.",
            },
            {
                "title": "Local Authorities",
                "href": "/councils/",
                "description": "Best when local policy or council context could change how the risks are judged.",
            },
        ],
        "faq_links": [
            {
                "title": "Can Neighbours Stop Planning Permission?",
                "href": "/planning-faq/can-neighbours-stop-planning-permission/",
                "description": "Read this when neighbour objections are the risk you are most worried about.",
            },
            {
                "title": "What Happens If Planning Permission Is Refused?",
                "href": "/planning-faq/what-happens-if-planning-permission-is-refused/",
                "description": "Useful when the next move after a weak design or risky application may be redesign rather than appeal.",
            },
            {
                "title": "How Long Does Planning Permission Usually Take?",
                "href": "/planning-faq/how-long-planning-permission-takes/",
                "description": "Useful when refusal risk and timing are both affecting the design strategy.",
            },
        ],
    },
    {
        "slug": "project-requirements-generator",
        "title": "Project Requirements Generator",
        "summary": "Build a practical planning prep pack covering requirements, documents and next checks for a home project.",
        "component": "custom_planning_tool",
        "meta_title": "Project Requirements Generator: planning prep tool",
        "meta_description": "Use the Project Requirements Generator to build a practical planning prep pack covering requirements, documents and next checks for a home project.",
        "hero_intro": "Use this tool when you know the broad project direction but want a clearer preparation pack before you spend more time on drawings or applications. It turns a few structured answers into the requirements, documents and next steps most likely to matter.",
        "hero_badges": [
            "Checklist-driven output",
            "Static structured logic",
            "Built for early planning prep",
        ],
        "search_intents": [
            "What do I need before applying for planning permission?",
            "Which documents and checks matter first?",
            "How do I build a planning prep pack?",
        ],
        "calculator_heading": "Build Your Planning Prep Pack",
        "calculator_intro": "Answer the short prompts, then generate a practical pack of requirements, documents and next checks.",
        "explanation_cards": [
            {
                "title": "What it answers well",
                "body": "It helps you turn a vague planning to-do list into a more concrete prep pack tied to the project, property and site sensitivity.",
            },
            {
                "title": "Why it saves time",
                "body": "It reduces the risk of commissioning drawings or checking the wrong route before the basic planning pack is in place.",
            },
            {
                "title": "Best next move",
                "body": "Use the output to prepare the right information, then move into the matching project guide, local authority layer or route tool.",
            },
        ],
        "guidance_links": [
            {"title": "Building Regulations", "href": "/building-regulations/", "description": "Use this when the prep pack should also keep building control, inspections and completion evidence in view."},
            {"title": "House Extensions", "href": "/house-extensions/", "description": "Useful when the prep pack is being built around extension work."},
            {"title": "Loft Conversions", "href": "/loft-conversions/", "description": "Helpful when roof volume or roof visibility is part of the prep pack."},
            {"title": "Outbuildings", "href": "/outbuildings/", "description": "Open this for detached building, annexe or garden-room questions."},
            {"title": "Local Authorities", "href": "/councils/", "description": "Best when the prep pack depends on local constraints or special controls."},
            {"title": "Planning Route Planner", "href": "/tools/planning-route-planner/", "description": "Use this next if the live route still needs mapping."},
            {"title": "Planning Decision Engine", "href": "/tools/planning-decision-tool/", "description": "Helpful when you still need a route-level answer first."},
        ],
        "faq_links": [
            {
                "title": "What Drawings Do I Need For Planning Permission?",
                "href": "/planning-faq/what-drawings-do-i-need-for-planning-permission/",
                "description": "Useful when the prep pack needs to turn into a concrete drawing and document list.",
            },
            {
                "title": "Is Pre-Application Advice Worth It?",
                "href": "/planning-faq/is-pre-application-advice-worth-it/",
                "description": "Helpful when one preparation decision is whether early council feedback could reduce redesign later.",
            },
            {
                "title": "What Happens After Planning Permission Is Approved?",
                "href": "/planning-faq/what-happens-after-planning-permission-is-approved/",
                "description": "Useful when the prep pack needs to stay aligned with conditions, decision notices and post-approval checks.",
            },
        ],
    },
    {
        "slug": "site-constraint-checker",
        "title": "Site Constraint Checker",
        "summary": "Identify the planning constraint most likely to block progress, then jump to the right rule page or tool.",
        "component": "custom_planning_tool",
        "meta_title": "Site Constraint Checker: planning rule tool",
        "meta_description": "Use the Site Constraint Checker to identify the planning constraint most likely to block progress and see which rule page to open next.",
        "hero_intro": "Use this when the project is not the real problem and you need to isolate the live planning constraint instead. It identifies the blocker, shows what usually tightens it, and points you to the next page worth opening.",
        "hero_badges": [
            "Constraint-first tool",
            "Fast rule isolation",
            "Designed for follow-up clicks",
        ],
        "search_intents": [
            "What is the real planning blocker here?",
            "Is height, depth or boundary position the main issue?",
            "Which rule should I check next?",
        ],
        "calculator_heading": "Check The Live Constraint",
        "calculator_intro": "Work through the prompts, then let the tool show which planning constraint is most active and where to go next.",
        "explanation_cards": [
            {
                "title": "What it answers well",
                "body": "It helps when the project is already known but the real blocker is height, depth, boundary position, roof change, frontage sensitivity or local control.",
            },
            {
                "title": "What it improves",
                "body": "Instead of sending you into a generic guide, it narrows the rule family that deserves the next check.",
            },
            {
                "title": "Best next move",
                "body": "Use the result to open the first rule page that matches the blocker, then use the wider route tools if the answer is still mixed.",
            },
        ],
        "guidance_links": [
            {"title": "Depth Limits", "href": "/depth-limits/", "description": "Useful when projection or site spread is the first blocker."},
            {"title": "Height Limits", "href": "/height-limits/", "description": "Open this when vertical scale is the main constraint."},
            {"title": "Boundary Rules", "href": "/boundary-rules/", "description": "Helpful when neighbour relationship or siting is the live issue."},
            {"title": "Roof Alterations", "href": "/roof-alterations/", "description": "Use this when visible roof change is the blocker."},
            {"title": "Planning Decision Engine", "href": "/tools/planning-decision-tool/", "description": "Helpful when the overall route still feels unresolved."},
            {"title": "Planning Route Planner", "href": "/tools/planning-route-planner/", "description": "Use this next when the blocker is known but the approval path is still fuzzy."},
        ],
        "faq_links": [
            {
                "title": "How To Measure Height For Planning Permission",
                "href": "/planning-faq/how-to-measure-height-for-planning-permission/",
                "description": "Useful when height is the controlling issue and the measurement method matters as much as the design.",
            },
            {
                "title": "How To Measure Distance From Boundary",
                "href": "/planning-faq/how-to-measure-distance-from-boundary/",
                "description": "Helpful when siting and neighbour relationship are the practical issues that keep changing the answer.",
            },
        ],
    },
    {
        "slug": "planning-route-planner",
        "title": "Planning Route Planner",
        "summary": "Map the approval route most likely to matter, including mixed routes such as planning, listed building or highway approvals.",
        "component": "custom_planning_tool",
        "meta_title": "Planning Route Planner: approval route tool",
        "meta_description": "Use the Planning Route Planner to map the approval route most likely to matter, including mixed routes such as planning, listed building or highway approvals.",
        "hero_intro": "Use this tool when you need to decide which approval path to prepare for before you sink time into the wrong route. It is designed to map whether the live answer still looks like permitted development, a formal application, a parallel consent or a mixed path that needs checking.",
        "hero_badges": [
            "Route-first output",
            "Static rule logic",
            "Built for early approval planning",
        ],
        "search_intents": [
            "What approval route do I need?",
            "Is this planning permission, prior approval or another consent?",
            "Could this project need mixed approvals?",
        ],
        "calculator_heading": "Plan The Approval Route",
        "calculator_intro": "Answer the structured questions, then let the tool map the approval route and supporting checks most likely to matter.",
        "explanation_cards": [
            {
                "title": "What it answers well",
                "body": "It helps you stop treating every project as a one-route question when the real answer may involve planning plus listed building consent, highways approval or a mixed fallback path.",
            },
            {
                "title": "Why it is useful early",
                "body": "It gives you a stronger steer on which route to prepare for before you invest in the wrong evidence or application assumptions.",
            },
            {
                "title": "Best next move",
                "body": "Use the route output to choose the right guide or council check, then confirm the detail with measured drawings and planning history where needed.",
            },
        ],
        "guidance_links": [
            {"title": "Permitted Development", "href": "/permitted-development/", "description": "Helpful when the simpler route still looks plausible."},
            {"title": "Planning Permission", "href": "/planning-permission/", "description": "Open this when the route is leaning more formal."},
            {"title": "Article 4 Restrictions", "href": "/article-4/", "description": "Useful when local policy could override the shortcut."},
            {"title": "Listed Buildings", "href": "/listed-buildings/", "description": "Helpful when listed building consent may run alongside planning."},
            {"title": "Dropped Kerbs", "href": "/dropped-kerbs/", "description": "Open this when highway approval may be part of the route."},
            {"title": "Project Requirements Generator", "href": "/tools/project-requirements-generator/", "description": "Use this next to turn the route into a practical prep pack."},
        ],
        "faq_links": [
            {
                "title": "Prior Approval Vs Planning Permission",
                "href": "/planning-faq/prior-approval-vs-planning-permission/",
                "description": "Useful when the route is not cleanly one thing or the other and the distinction matters before you prepare evidence.",
            },
            {
                "title": "Article 4 Directions Explained",
                "href": "/planning-faq/article-4-directions/",
                "description": "Helpful when local policy might be the reason the route is stricter than expected.",
            },
        ],
    },
    {
        "slug": "lawful-development-certificate-checker",
        "title": "Lawful Development Certificate Checker",
        "summary": "Check whether an LDC looks unnecessary, worth considering, or strongly worth a formal look before you spend more.",
        "component": "custom_planning_tool",
        "meta_title": "Lawful Development Certificate Checker | UK Planning Guide",
        "meta_description": "Use the LDC checker to decide whether a lawful development certificate may be worth it for a permitted development project.",
        "hero_intro": "Use this when the project may be permitted development, but you need to decide whether written proof is worth the fee, delay and drawing effort.",
        "hero_badges": ["Certificate triage", "No contact details", "Best before drawings or sales risk"],
        "search_intents": [
            "Is a lawful development certificate worth it?",
            "Do I need an LDC for permitted development?",
            "Lawful development certificate or planning permission?",
        ],
        "calculator_heading": "Check Whether An LDC Is Worth It",
        "calculator_intro": "Answer the project, property, restriction and certainty questions. The result helps you decide whether to rely on broad guidance, gather stronger evidence, or consider a formal certificate.",
        "explanation_cards": [
            {"title": "Best use case", "body": "Projects that still look like permitted development but carry enough uncertainty that written proof might prevent wasted spend later."},
            {"title": "What changes the answer", "body": "Article 4, conservation areas, flats, planning history, tight dimensions and future sale or remortgage risk all push the result toward a stronger formal check."},
            {"title": "What to do next", "body": "Use the result to decide whether to tighten drawings, estimate costs, or move toward a formal lawful development certificate."},
        ],
        "guidance_links": [
            {"title": "Permitted Development", "href": "/permitted-development/", "description": "Use this for the baseline route behind an LDC."},
            {"title": "Planning Permission", "href": "/planning-permission/", "description": "Open this if the project may need a formal planning application instead."},
            {"title": "Planning Cost Calculator", "href": "/tools/planning-cost-calculator/", "description": "Estimate the cost trade-off before choosing the route."},
            {"title": "Drawing Readiness Checker", "href": "/tools/drawings-cost-readiness-checker/", "description": "Check whether drawings are worth commissioning yet."},
            {"title": "Local Authorities", "href": "/councils/", "description": "Use this when local designations may change the normal answer."},
        ],
        "faq_links": [
            {"title": "Lawful Development Certificate Vs Planning Permission", "href": "/planning-faq/lawful-development-certificate-vs-planning-permission/", "description": "Useful when you need the difference explained before choosing the route."},
            {"title": "Planning Permission Vs Permitted Development", "href": "/planning-faq/planning-permission-vs-permitted-development/", "description": "Helpful when the basic route still feels mixed."},
        ],
    },
    {
        "slug": "planning-cost-calculator",
        "title": "Planning Cost Calculator",
        "summary": "Estimate the likely planning-route cost band before choosing between more reading, drawings, an LDC, pre-app advice or a full application.",
        "component": "custom_planning_tool",
        "meta_title": "Planning Cost Calculator | UK Planning Guide",
        "meta_description": "Estimate likely planning, certificate, pre-application and drawing cost bands before you decide the next planning step.",
        "hero_intro": "Use this before you commit to the next planning spend. It is not a quote, but it helps you compare the route, drawing and application costs that usually shape the decision.",
        "hero_badges": ["Cost triage", "Static estimate bands", "Best before commissioning work"],
        "search_intents": [
            "How much does planning permission cost?",
            "How much does a lawful development certificate cost?",
            "How much should I budget before planning drawings?",
        ],
        "calculator_heading": "Estimate The Planning Cost Band",
        "calculator_intro": "Choose the project type, route, drawing stage and urgency. The result gives a cautious cost-readiness band and the next check worth doing.",
        "explanation_cards": [
            {"title": "What it estimates", "body": "Typical planning-route spend bands, including application-style fees, certificate routes, drawings and professional preparation."},
            {"title": "What it cannot know", "body": "Exact local fees, consultant pricing, surveys and specialist reports still need checking once the route is clearer."},
            {"title": "Best next move", "body": "Use the estimate to decide whether to tighten the route, prepare drawings, or ask for a more case-specific steer."},
        ],
        "guidance_links": [
            {"title": "Planning Application Readiness Checker", "href": "/tools/planning-application-readiness-checker/", "description": "Use this if the result points toward a formal application."},
            {"title": "Drawing Readiness Checker", "href": "/tools/drawings-cost-readiness-checker/", "description": "Use this before commissioning drawings."},
            {"title": "Planning Permission", "href": "/planning-permission/", "description": "Open this for the formal route baseline."},
            {"title": "Planning Help", "href": "/planning-help/", "description": "Use this when the next spend needs a professional route."},
        ],
        "faq_links": [
            {"title": "Is Pre-Application Advice Worth It?", "href": "/planning-faq/is-pre-application-advice-worth-it/", "description": "Useful when pre-app advice may be part of the spend."},
            {"title": "Do I Need Planning Permission?", "href": "/planning-faq/do-i-need-planning-permission/", "description": "Helpful if the cost depends on the route."},
        ],
    },
    {
        "slug": "drawings-cost-readiness-checker",
        "title": "Drawings Cost Readiness Checker",
        "summary": "Check whether a project is ready for paid drawings or whether route, site and measurement issues should be tightened first.",
        "component": "custom_planning_tool",
        "meta_title": "Drawings Cost Readiness Checker | UK Planning Guide",
        "meta_description": "Check whether your project is ready for planning drawings, measured sketches or stronger route checks before paying for design work.",
        "hero_intro": "Use this when you are close to commissioning drawings but want to avoid paying for the wrong route, weak brief or missing site checks.",
        "hero_badges": ["Drawings readiness", "Spend order check", "Best before design fees"],
        "search_intents": [
            "When should I pay for planning drawings?",
            "Do I need drawings for planning permission?",
            "Am I ready to commission planning drawings?",
        ],
        "calculator_heading": "Check Drawing Readiness",
        "calculator_intro": "Answer the route, site, dimensions and evidence questions. The result tells you whether drawings look premature, useful, or urgent.",
        "explanation_cards": [
            {"title": "What it protects against", "body": "Commissioning drawings before the route, local constraints or core measurements are clear enough to brief properly."},
            {"title": "What it expects", "body": "A rough project idea, basic property facts, known restrictions and at least enough measurements to know where the uncertainty sits."},
            {"title": "Best next move", "body": "Use the result to tighten the brief, run a cost estimate, or move into application readiness if the formal route is likely."},
        ],
        "guidance_links": [
            {"title": "Building Regulations", "href": "/building-regulations/", "description": "Use this when drawings also need to support building control or completion evidence."},
            {"title": "Planning Cost Calculator", "href": "/tools/planning-cost-calculator/", "description": "Estimate the likely spend before moving ahead."},
            {"title": "Planning Application Readiness Checker", "href": "/tools/planning-application-readiness-checker/", "description": "Use this if a formal application is becoming realistic."},
            {"title": "Project Requirements Generator", "href": "/tools/project-requirements-generator/", "description": "Build a practical planning prep pack."},
            {"title": "Planning Help", "href": "/planning-help/", "description": "Use this when drawings or professional input are likely."},
        ],
        "faq_links": [
            {"title": "Do I Need Planning Permission?", "href": "/planning-faq/do-i-need-planning-permission/", "description": "Helpful when the route is still the main uncertainty."},
            {"title": "How To Measure Height For Planning Permission", "href": "/planning-faq/how-to-measure-height-for-planning-permission/", "description": "Useful when measured drawings depend on height checks."},
        ],
    },
    {
        "slug": "planning-application-readiness-checker",
        "title": "Planning Application Readiness Checker",
        "summary": "Check whether a formal planning application looks ready enough to prepare, or whether evidence, drawings and route checks are still thin.",
        "component": "custom_planning_tool",
        "meta_title": "Planning Application Readiness Checker | UK Planning Guide",
        "meta_description": "Check whether your planning application looks ready to prepare, or whether drawings, evidence, route certainty and local checks need work first.",
        "hero_intro": "Use this once the route is leaning formal. It helps you spot weak evidence, missing drawings and local-context gaps before a submission is prepared.",
        "hero_badges": ["Application readiness", "Evidence-first", "Best before submission prep"],
        "search_intents": [
            "Am I ready to submit a planning application?",
            "What do I need before a planning application?",
            "Planning application checklist UK",
        ],
        "calculator_heading": "Check Application Readiness",
        "calculator_intro": "Work through the route, drawings, local sensitivity and evidence questions. The result shows whether the application pack looks lean, standard or underprepared.",
        "explanation_cards": [
            {"title": "What it answers well", "body": "Whether a formal application route is ready to prepare or whether key decisions still need checking before spend increases."},
            {"title": "What usually blocks readiness", "body": "Thin drawings, unclear site constraints, missing heritage or highway context, and a weak explanation of why the design should be acceptable."},
            {"title": "Best next move", "body": "Use the output as a preparation checklist before moving into drawings, professional help or formal council advice."},
        ],
        "guidance_links": [
            {"title": "Planning Permission", "href": "/planning-permission/", "description": "Open this for the formal application baseline."},
            {"title": "Planning Cost Calculator", "href": "/tools/planning-cost-calculator/", "description": "Estimate route and preparation costs."},
            {"title": "Planning Rejection Risk Analyzer", "href": "/tools/planning-rejection-risk-analyzer/", "description": "Pressure-test the refusal risks before preparing the pack."},
            {"title": "Planning Help", "href": "/planning-help/", "description": "Use this when application support or drawings are likely."},
        ],
        "faq_links": [
            {"title": "Is Pre-Application Advice Worth It?", "href": "/planning-faq/is-pre-application-advice-worth-it/", "description": "Useful when the application is possible but risk still feels high."},
            {"title": "Prior Approval Vs Planning Permission", "href": "/planning-faq/prior-approval-vs-planning-permission/", "description": "Helpful if the route still may not be a standard application."},
        ],
    },
    {
        "slug": "project-roadmap-builder",
        "title": "Project Roadmap Builder",
        "summary": "Turn a project, property and local-risk setup into a practical staged planning route you can save and come back to.",
        "component": "custom_planning_tool",
        "meta_title": "Project Roadmap Builder | Planning workflow tool",
        "meta_description": "Build a staged planning roadmap for extensions, lofts, garden rooms, dropped kerbs, HMOs and sensitive sites before spending on drawings.",
        "hero_intro": "Use this when the next move is unclear and you need a route, not another isolated answer. The roadmap turns your project setup into a staged sequence: rule check, local check, proof route, drawings, application prep and help if needed.",
        "hero_badges": ["Saveable workflow", "No account needed", "Best before project spend"],
        "search_intents": [
            "Planning project roadmap",
            "What order should I check planning permission?",
            "Planning workflow for home project",
        ],
        "calculator_heading": "Build The Project Roadmap",
        "calculator_intro": "Choose the project, property setup, local sensitivity and confidence level. The result gives a staged route and next tasks to save in My Planning Project.",
        "explanation_cards": [
            {"title": "What it gives you", "body": "A practical sequence for checking rules, local constraints, formal proof, drawings and application readiness."},
            {"title": "Why it helps retention", "body": "The output is useful over several visits because it behaves like a project route rather than a one-off article."},
            {"title": "Best next move", "body": "Save the roadmap to My Planning Project, then complete one task at a time before moving to paid preparation."},
        ],
        "guidance_links": [
            {"title": "Building Regulations", "href": "/building-regulations/", "description": "Add this when the roadmap needs a separate building control and completion evidence track."},
            {"title": "My Planning Project", "href": "/my-planning-project/", "description": "Open the local workspace after saving your roadmap."},
            {"title": "Planning Route Planner", "href": "/tools/planning-route-planner/", "description": "Compare the approval route if the roadmap still feels mixed."},
            {"title": "Project Requirements Generator", "href": "/tools/project-requirements-generator/", "description": "Turn the route into a preparation pack."},
            {"title": "Planning Help", "href": "/planning-help/", "description": "Use this when the next step needs more than a broad guide."},
        ],
        "faq_links": [
            {"title": "Do I Need Planning Permission?", "href": "/planning-faq/do-i-need-planning-permission/", "description": "Useful when the first route question still needs plain-English context."},
            {"title": "Lawful Development Certificate Vs Planning Permission", "href": "/planning-faq/lawful-development-certificate-vs-planning-permission/", "description": "Use this when the roadmap points toward formal proof."},
        ],
    },
    {
        "slug": "planning-task-checklist-builder",
        "title": "Planning Task Checklist Builder",
        "summary": "Create a saveable planning task list for the project type, constraints and route you are working through.",
        "component": "custom_planning_tool",
        "meta_title": "Planning Task Checklist Builder | Home project checklist",
        "meta_description": "Create a planning task checklist for extensions, lofts, garden rooms, dropped kerbs, HMOs, conservation areas and listed buildings.",
        "hero_intro": "Use this when you want a clean action list instead of a long reading list. It builds a task sequence for checking the route, gathering evidence, deciding whether proof is needed and preparing the next conversation.",
        "hero_badges": ["Printable checklist", "Saveable tasks", "No login"],
        "search_intents": [
            "Planning permission checklist",
            "Home project planning checklist",
            "What do I need to check before planning application?",
        ],
        "calculator_heading": "Build The Checklist",
        "calculator_intro": "Pick the project and route pressure, then save the result into the local project workspace.",
        "explanation_cards": [
            {"title": "What it answers well", "body": "It turns a planning question into concrete tasks you can work through across several visits."},
            {"title": "What it avoids", "body": "It does not imply the route is settled. Borderline tasks still point users back to official checks and formal routes."},
            {"title": "Best next move", "body": "Save the checklist, mark tasks complete, and return through the My Planning Project panel."},
        ],
        "guidance_links": [
            {"title": "My Planning Project", "href": "/my-planning-project/", "description": "Review saved tasks and completed checks."},
            {"title": "Planning Application Readiness Checker", "href": "/tools/planning-application-readiness-checker/", "description": "Use this when the checklist points toward a formal application."},
            {"title": "Drawing Readiness Checker", "href": "/tools/drawings-cost-readiness-checker/", "description": "Use this before paying for drawings."},
            {"title": "Planning FAQ", "href": "/planning-faq/", "description": "Use the FAQ layer for process questions."},
        ],
        "faq_links": [
            {"title": "What Drawings Do I Need For Planning Permission?", "href": "/planning-faq/what-drawings-do-i-need-for-planning-permission/", "description": "Useful when the checklist reaches drawings."},
            {"title": "Is Pre-Application Advice Worth It?", "href": "/planning-faq/is-pre-application-advice-worth-it/", "description": "Useful when the task list points toward council feedback."},
        ],
    },
    {
        "slug": "evidence-pack-builder",
        "title": "Evidence Pack Builder",
        "summary": "Build a practical list of photos, measurements, drawings, official checks and planning-history notes to gather before spending more.",
        "component": "custom_planning_tool",
        "meta_title": "Evidence Pack Builder | Planning photos and drawings checklist",
        "meta_description": "Build a planning evidence pack covering photos, measurements, drawings, local constraints and official checks before a formal route.",
        "hero_intro": "Use this before commissioning drawings or asking for help. It tells you what evidence is likely to reduce uncertainty for the project and which gaps still need checking officially.",
        "hero_badges": ["Evidence-first", "Good before drawings", "Saveable pack"],
        "search_intents": [
            "What evidence do I need for planning permission?",
            "Planning photos and measurements checklist",
            "Planning drawings evidence pack",
        ],
        "calculator_heading": "Build The Evidence Pack",
        "calculator_intro": "Choose the project, site sensitivity and current evidence stage. The output becomes a saveable prep pack.",
        "explanation_cards": [
            {"title": "What it gives you", "body": "A practical evidence list for the project, including photos, dimensions, drawings and official checks."},
            {"title": "Why it matters", "body": "Better evidence helps users avoid paying for the wrong next step or asking a professional an under-specified question."},
            {"title": "Best next move", "body": "Gather the pack, then run the readiness or roadmap tool with fewer unknowns."},
        ],
        "guidance_links": [
            {"title": "Building Regulations Completion Certificates", "href": "/building-regulations/completion-certificates/", "description": "Use this when the evidence pack should include building control sign-off and compliance records."},
            {"title": "Drawing Readiness Checker", "href": "/tools/drawings-cost-readiness-checker/", "description": "Check whether drawings are the next useful spend."},
            {"title": "Project Requirements Generator", "href": "/tools/project-requirements-generator/", "description": "Turn evidence needs into a wider preparation pack."},
            {"title": "Local Authorities", "href": "/councils/", "description": "Use official local sources for designation and planning-history checks."},
            {"title": "My Planning Project", "href": "/my-planning-project/", "description": "Save and revisit the evidence tasks."},
        ],
        "faq_links": [
            {"title": "How To Measure Height For Planning Permission", "href": "/planning-faq/how-to-measure-height-for-planning-permission/", "description": "Useful when evidence depends on height."},
            {"title": "How To Measure Distance From Boundary", "href": "/planning-faq/how-to-measure-distance-from-boundary/", "description": "Useful when siting evidence matters."},
        ],
    },
    {
        "slug": "local-constraint-finder",
        "title": "Local Constraint Finder",
        "summary": "Find the local planning constraints most likely to change the route for a project before relying on the national baseline.",
        "component": "custom_planning_tool",
        "meta_title": "Local Constraint Finder | Article 4, conservation and council checks",
        "meta_description": "Find local planning constraints such as Article 4, conservation areas, listed buildings, highway issues and council checks for a project.",
        "hero_intro": "Use this when the national rule sounds simple but the property might be locally restricted. It highlights the constraint families that deserve a council or official-source check first.",
        "hero_badges": ["Local risk triage", "Official checks next", "Good for return visits"],
        "search_intents": [
            "Local planning constraints checker",
            "Article 4 conservation area planning check",
            "Council planning restrictions for home project",
        ],
        "calculator_heading": "Find The Local Constraint",
        "calculator_intro": "Choose the project, authority confidence and known designations. The result points to the local checks most likely to change the answer.",
        "explanation_cards": [
            {"title": "What it narrows", "body": "Article 4, conservation areas, listed buildings, planning history, highways and local policy pressure."},
            {"title": "What it does not do", "body": "It does not perform a live address lookup or replace official council maps and planning records."},
            {"title": "Best next move", "body": "Open the authority guide and save the constraint tasks before relying on the broad route."},
        ],
        "guidance_links": [
            {"title": "Local Authorities", "href": "/councils/", "description": "Open the official-source layer for your council."},
            {"title": "Article 4 Restrictions", "href": "/article-4/", "description": "Use this when a local direction may remove the shortcut."},
            {"title": "Conservation Areas", "href": "/conservation-areas/", "description": "Use this when heritage area controls may change the route."},
            {"title": "Listed Buildings", "href": "/listed-buildings/", "description": "Use this when listed building consent may be separate."},
        ],
        "faq_links": [
            {"title": "Article 4 Directions Explained", "href": "/planning-faq/article-4-directions/", "description": "Useful when local policy may override the usual route."},
            {"title": "Conservation Area Planning Rules", "href": "/planning-faq/conservation-area-planning-rules/", "description": "Useful when heritage context is the live issue."},
        ],
    },
    {
        "slug": "planning-timeline-planner",
        "title": "Planning Timeline Planner",
        "summary": "Estimate the practical sequence and timing bands for checks, drawings, LDCs, applications, pre-app advice and highway-style approvals.",
        "component": "custom_planning_tool",
        "meta_title": "Planning Timeline Planner | Route and timing workflow",
        "meta_description": "Plan the timing sequence for planning permission, lawful development certificates, drawings, pre-app advice and highway approvals.",
        "hero_intro": "Use this once you know the project but not the order of the next steps. It gives a cautious timing route so you can avoid commissioning work before the planning question is clear.",
        "hero_badges": ["Timing bands", "Spend-order check", "Return later"],
        "search_intents": [
            "Planning permission timeline",
            "How long should planning checks take?",
            "Planning application and drawings sequence",
        ],
        "calculator_heading": "Plan The Timeline",
        "calculator_intro": "Choose the likely route, evidence stage and sensitivity. The result gives an order of checks and timing bands to save.",
        "explanation_cards": [
            {"title": "What it estimates", "body": "The likely order of route checks, evidence gathering, drawings, proof routes, applications and help conversations."},
            {"title": "What it cannot know", "body": "Exact council processing times, consultant availability and specialist reports still need checking."},
            {"title": "Best next move", "body": "Save the timeline and use it to decide the next lightest useful action."},
        ],
        "guidance_links": [
            {"title": "Planning Cost Calculator", "href": "/tools/planning-cost-calculator/", "description": "Estimate route and preparation costs."},
            {"title": "Planning Application Readiness Checker", "href": "/tools/planning-application-readiness-checker/", "description": "Use this before treating the project as submission-ready."},
            {"title": "Lawful Development Certificate Checker", "href": "/tools/lawful-development-certificate-checker/", "description": "Use this when written proof may be worthwhile."},
            {"title": "My Planning Project", "href": "/my-planning-project/", "description": "Return to the saved timeline later."},
        ],
        "faq_links": [
            {"title": "How Long Planning Permission Takes", "href": "/planning-faq/how-long-planning-permission-takes/", "description": "Useful for broader timing context."},
            {"title": "Prior Approval Vs Planning Permission", "href": "/planning-faq/prior-approval-vs-planning-permission/", "description": "Useful when the route is not a standard application."},
        ],
    },
]

# These scenario topics are already covered by the dedicated interactive tools above.
SCENARIO_TOOL_EXCLUSIONS = {
    "planning-permission",
    "permitted-development",
}


def _tool_href(slug: str) -> str:
    return f"/tools/{slug}/"


def _build_scenario_tool(scenario: dict) -> dict:
    title = scenario["title"]
    seo_angle = str(scenario.get("seo_angle", "")).strip() or title.lower()

    return {
        "slug": scenario["slug"],
        "title": f"{title} Self-Check",
        "summary": f"Use a quick self-check for {seo_angle} questions before you read the full guidance.",
        "href": _tool_href(scenario["slug"]),
        "source": "scenario",
    }


def _normalize_tool(tool: dict) -> dict:
    item = tool.copy()
    item.setdefault("href", _tool_href(item["slug"]))
    item.setdefault("source", "standalone")
    return item


def load_tools() -> list[dict]:
    tools = [_normalize_tool(tool) for tool in STANDALONE_TOOLS]

    for scenario in SCENARIOS:
        if scenario["slug"] in SCENARIO_TOOL_EXCLUSIONS:
            continue
        tools.append(_build_scenario_tool(scenario))

    seen = set()
    for tool in tools:
        slug = tool["slug"]
        if slug in seen:
            raise ValueError(f"Duplicate tool slug detected: {slug}")
        seen.add(slug)

    return [tool.copy() for tool in tools]
