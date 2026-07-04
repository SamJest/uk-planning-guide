from __future__ import annotations


DATA_ASSETS = [
    {
        "slug": "council-profile-database",
        "title": "Council profile database",
        "summary": "A structured index of council planning links, planning-register routes, pre-application pages, validation sources and known local restrictions.",
        "source_basis": "Council websites, planning.data.gov.uk local planning authority data and the site's official source registry.",
        "phase": "Phase 5",
        "schema_name": "UK Planning Guide council profile database",
        "status": "Scaffolded; source-backed fields should be expanded council by council before scale indexing.",
    },
    {
        "slug": "pre-app-fees",
        "title": "Pre-application fee comparator",
        "summary": "A council-by-council comparator for pre-application advice links, fee pages and service notes.",
        "source_basis": "Council fee pages, council pre-application advice pages and Planning Advisory Service material.",
        "phase": "Phase 5",
        "schema_name": "UK council pre-application advice fee comparator",
        "status": "Scaffolded; individual fee values require council-source verification before publication at scale.",
    },
    {
        "slug": "validation-requirements",
        "title": "Validation requirement lookup",
        "summary": "A lookup for local validation list links, required document signposting and official submission routes.",
        "source_basis": "Council validation requirement pages and Planning Portal submission guidance.",
        "phase": "Phase 5",
        "schema_name": "UK council planning validation requirement lookup",
        "status": "Scaffolded; local validation notes must stay tied to council source URLs and update dates.",
    },
    {
        "slug": "hmo-article-4-map",
        "title": "HMO Article 4 map",
        "summary": "A council-level lookup for HMO Article 4 risk, source links and the exact-property checks investors still need to make.",
        "source_basis": "Council Article 4 pages, local plan material and legislation context.",
        "phase": "Phase 5-6",
        "schema_name": "UK HMO Article 4 local authority lookup",
        "status": "Scaffolded; treat unverified authorities as check-needed rather than clear or restricted.",
    },
    {
        "slug": "council-pack-export",
        "title": "Council pack export",
        "summary": "A printable or email-ready pack combining council official links, relevant rules, known restrictions, evidence checklists and next-step options.",
        "source_basis": "UK Planning Guide content, official source cards and council-specific source records.",
        "phase": "Phase 6-7",
        "schema_name": "UK Planning Guide council pack export",
        "status": "Scaffolded; premium delivery remains disabled until the launch gate is passed.",
    },
]


MONETISATION_SURFACES = [
    {
        "slug": "reviewed-route-report",
        "title": "Reviewed planning route report",
        "summary": "A launch-gated paid report covering likely route, key risks, evidence, official sources, council-specific links and recommended next step.",
        "service_type": "Planning route report",
    },
    {
        "slug": "premium-council-pack",
        "title": "Premium council pack",
        "summary": "A launch-gated pack for homeowners, architects, agents and researchers who want council links, restrictions and checklist exports in one place.",
        "service_type": "Premium council planning pack",
    },
    {
        "slug": "professional-referral",
        "title": "Consent-led professional referral",
        "summary": "A disabled-by-default referral path for users who explicitly ask for an introduction to a planner, architect, technologist, conservation specialist or HMO specialist.",
        "service_type": "Professional referral",
    },
]
