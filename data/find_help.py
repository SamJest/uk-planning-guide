"""Configuration for the early-stage Find Help system.

This keeps the initial static setup easy to extend into a future
manual-matching workflow without pretending live matching is already active.
"""

from __future__ import annotations

FIND_HELP_ENABLED = False


ROLL_OUT_NOTE = (
    "The vetted local network is still being assembled. Matching will launch in "
    "carefully limited categories and areas rather than as a live nationwide marketplace."
)

FORM_PRIVACY_NOTE = (
    "Your details are used to review this early-stage request and, where relevant, to "
    "contact you about coverage or follow-up. They are not published without permission "
    "and are not used to sign you up to marketing emails."
)

FORM_NOSCRIPT_NOTE = (
    "This temporary early-stage form uses a lightweight on-page redirect. If it does not "
    "work on your device, email guidance@ukplanningguide.co.uk with the same details."
)

HOMEOWNER_HELP_TYPES = [
    "Planning consultant support",
    "Drawings or package preparation",
    "Architectural design input",
    "Lawful development certificate support",
    "Planning application support",
    "Dropped kerb or access-related help",
    "Not sure yet",
]

HOMEOWNER_PROJECT_TYPES = [
    "House extension",
    "Loft conversion",
    "Garage conversion",
    "Garden room or outbuilding",
    "Dropped kerb or driveway change",
    "Windows, doors or frontage change",
    "Heat pump or solar project",
    "Change of use",
    "Something else",
]

HOMEOWNER_PROJECT_STAGES = [
    "Just exploring the idea",
    "Measuring up and comparing options",
    "Ready for drawings or a package",
    "Preparing for an application or certificate",
    "Trying to fix a stalled or awkward case",
]

HOMEOWNER_CONSTRAINT_OPTIONS = [
    "No known special constraints",
    "Conservation area",
    "Listed building",
    "Flat or maisonette",
    "Article 4 concerns",
    "Previous extensions or history concerns",
    "Not sure",
]

HOMEOWNER_BUDGET_BANDS = [
    "Prefer not to say",
    "Under GBP 5,000",
    "GBP 5,000 to GBP 15,000",
    "GBP 15,000 to GBP 40,000",
    "GBP 40,000 to GBP 100,000",
    "Over GBP 100,000",
]

HOMEOWNER_TIMING_OPTIONS = [
    "Just planning ahead",
    "Within the next 3 months",
    "Within 3 to 6 months",
    "Within 6 to 12 months",
    "More than 12 months away",
]

SPECIALIST_TYPES = [
    "Planning consultant",
    "Architectural technologist",
    "Residential architect",
    "Residential drawing or package provider",
]

YEARS_OPERATING_OPTIONS = [
    "Under 2 years",
    "2 to 5 years",
    "6 to 10 years",
    "11 to 20 years",
    "More than 20 years",
]

HOMEOWNER_REQUEST_FIELDS = [
    {"name": "name", "label": "Full name", "type": "text", "required": True, "autocomplete": "name"},
    {"name": "email", "label": "Email", "type": "email", "required": True, "autocomplete": "email"},
    {"name": "phone", "label": "Phone (optional)", "type": "tel", "required": False, "autocomplete": "tel"},
    {"name": "postcode", "label": "Postcode", "type": "text", "required": True, "autocomplete": "postal-code"},
    {"name": "town_or_city", "label": "Town or city", "type": "text", "required": True, "autocomplete": "address-level2"},
    {"name": "project_type", "label": "Project type", "type": "select", "required": True, "options": HOMEOWNER_PROJECT_TYPES},
    {"name": "project_stage", "label": "Project stage", "type": "select", "required": True, "options": HOMEOWNER_PROJECT_STAGES},
    {"name": "help_needed", "label": "Help needed", "type": "select", "required": True, "options": HOMEOWNER_HELP_TYPES},
    {
        "name": "planning_route",
        "label": "Likely planning permission needed?",
        "type": "select",
        "required": True,
        "options": ["Likely yes", "Likely no", "Not sure yet"],
    },
    {
        "name": "special_constraints",
        "label": "Special constraints",
        "type": "select",
        "required": False,
        "options": HOMEOWNER_CONSTRAINT_OPTIONS,
    },
    {"name": "budget_band", "label": "Budget band (optional)", "type": "select", "required": False, "options": HOMEOWNER_BUDGET_BANDS},
    {"name": "preferred_timing", "label": "Preferred timing", "type": "select", "required": True, "options": HOMEOWNER_TIMING_OPTIONS},
    {
        "name": "notes",
        "label": "Project notes",
        "type": "textarea",
        "required": True,
        "rows": 7,
        "help": "A short summary is enough. Include the property type, the change you want to make, and anything that feels locally sensitive or borderline.",
    },
]

SPECIALIST_APPLICATION_FIELDS = [
    {"name": "full_name", "label": "Full name", "type": "text", "required": True, "autocomplete": "name"},
    {"name": "company_name", "label": "Company name", "type": "text", "required": True, "autocomplete": "organization"},
    {"name": "email", "label": "Email", "type": "email", "required": True, "autocomplete": "email"},
    {"name": "phone", "label": "Phone", "type": "tel", "required": True, "autocomplete": "tel"},
    {"name": "website", "label": "Website", "type": "url", "required": False, "autocomplete": "url"},
    {"name": "specialist_type", "label": "Specialist type", "type": "select", "required": True, "options": SPECIALIST_TYPES},
    {
        "name": "areas_covered",
        "label": "Areas covered",
        "type": "textarea",
        "required": True,
        "rows": 4,
        "help": "List the towns, counties or regions you genuinely cover for homeowner work.",
    },
    {"name": "years_operating", "label": "Years operating", "type": "select", "required": True, "options": YEARS_OPERATING_OPTIONS},
    {
        "name": "services_offered",
        "label": "Services offered",
        "type": "textarea",
        "required": True,
        "rows": 4,
    },
    {
        "name": "project_types_handled",
        "label": "Project types handled",
        "type": "textarea",
        "required": True,
        "rows": 4,
    },
    {
        "name": "recent_examples",
        "label": "Recent relevant examples",
        "type": "textarea",
        "required": True,
        "rows": 5,
        "help": "Keep this concise. A few strong, homeowner-relevant examples are more useful than a long list.",
    },
    {
        "name": "insurance_confirmation",
        "label": "Insurance confirmation",
        "type": "select",
        "required": True,
        "options": [
            "Yes, appropriate cover is in place",
            "Cover is being renewed or updated",
            "Prefer to explain in notes",
        ],
    },
    {
        "name": "pricing_approach",
        "label": "Pricing approach",
        "type": "textarea",
        "required": True,
        "rows": 4,
        "help": "Explain how you usually price homeowner work, for example fixed-fee stages, hourly input or packaged deliverables.",
    },
    {
        "name": "fit_statement",
        "label": "Why you are a good fit",
        "type": "textarea",
        "required": True,
        "rows": 5,
    },
]

FIND_HELP_DRAFT_ROUTES = [
    "/find-help/",
    "/find-help/homeowners/",
    "/find-help/homeowners/request/",
    "/find-help/homeowners/request/success/",
    "/find-help/specialists/",
    "/find-help/specialists/apply/",
    "/find-help/specialists/apply/success/",
    "/find-help/how-it-works/",
    "/find-help/trust/",
]

FIND_HELP_ROUTES = FIND_HELP_DRAFT_ROUTES if FIND_HELP_ENABLED else []

FIND_HELP_CTA_PROJECT_SLUGS = {
    "house-extensions",
    "single-storey-extensions",
    "rear-extensions",
    "side-extensions",
    "two-storey-extensions",
    "wraparound-extensions",
    "loft-conversions",
    "dropped-kerbs",
}

FIND_HELP_CTA_FAQ_SLUGS = {
    "lawful-development-certificate",
    "lawful-development-certificate-vs-planning-permission",
    "is-pre-application-advice-worth-it",
}

# Future backend shape notes for the manual-matching phase.
HOMEOWNER_REQUEST_MODEL = {
    "entity": "homeowner_request",
    "version": "prelaunch-v1",
    "status_flow": ["received", "coverage_pending", "reviewed", "matched", "closed"],
    "primary_fields": [field["name"] for field in HOMEOWNER_REQUEST_FIELDS],
}

SPECIALIST_APPLICATION_MODEL = {
    "entity": "specialist_application",
    "version": "prelaunch-v1",
    "status_flow": ["received", "screening", "shortlisted", "approved", "declined"],
    "primary_fields": [field["name"] for field in SPECIALIST_APPLICATION_FIELDS],
}
