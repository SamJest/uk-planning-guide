from __future__ import annotations


DATA_ASSETS = [
    {
        "slug": "council-profile-database",
        "title": "Council profile database",
        "summary": "A structured index of council planning links, planning-register routes, pre-application pages, validation sources and known local restrictions.",
        "source_basis": "Council websites, planning.data.gov.uk local planning authority data and the site's official source registry.",
        "phase": "Phase 5",
        "schema_name": "UK Planning Guide council profile database",
        "status": "Official-source directory. Coverage is limited to the sources listed below; check the council record for your address.",
    },
    {
        "slug": "pre-app-fees",
        "title": "Pre-application advice and fee sources",
        "summary": "Find official pre-application advice and fee pages. Read the current council fee schedule before choosing a service.",
        "source_basis": "Council fee pages, council pre-application advice pages and Planning Advisory Service material.",
        "phase": "Phase 5",
        "schema_name": "UK council pre-application advice fee comparator",
        "status": "Source links are provided; prices are not estimated or presented as a complete national comparison.",
    },
    {
        "slug": "validation-requirements",
        "title": "Validation requirement lookup",
        "summary": "A lookup for local validation list links, required document signposting and official submission routes.",
        "source_basis": "Council validation requirement pages and Planning Portal submission guidance.",
        "phase": "Phase 5",
        "schema_name": "UK council planning validation requirement lookup",
        "status": "Use the linked council validation list for the current document requirements.",
    },
    {
        "slug": "hmo-article-4-map",
        "title": "HMO Article 4 source finder",
        "summary": "Find official Article 4 sources and check the designation documents for the exact property and proposed use.",
        "source_basis": "Council Article 4 pages, local plan material and legislation context.",
        "phase": "Phase 5-6",
        "schema_name": "UK HMO Article 4 local authority lookup",
        "status": "This is a source directory, not a boundary map or a finding that any address is unrestricted.",
    },
    {
        "slug": "council-pack-export",
        "title": "Council pack export",
        "summary": "A printable or email-ready pack combining council official links, relevant rules, known restrictions, evidence checklists and next-step options.",
        "source_basis": "UK Planning Guide content, official source cards and council-specific source records.",
        "phase": "Phase 6-7",
        "schema_name": "UK Planning Guide council pack export",
        "status": "Save pages to My Planning Project, then export a text summary or print the pages as PDF.",
    },
]


MONETISATION_SURFACES = [
    {
        "slug": "reviewed-route-report",
        "title": "Reviewed planning route report",
        "summary": "Paid reviewed reports are not currently offered. Use the free route checker to prepare your own initial summary.",
        "service_type": "Planning route report",
    },
    {
        "slug": "premium-council-pack",
        "title": "Premium council pack",
        "summary": "Premium packs are not currently offered. Save official links and export your free project summary from My Planning Project.",
        "service_type": "Premium council planning pack",
    },
    {
        "slug": "professional-referral",
        "title": "Consent-led professional referral",
        "summary": "Professional matching is not currently offered. You can prepare an email enquiry or seek independent professional advice.",
        "service_type": "Professional referral",
    },
]
