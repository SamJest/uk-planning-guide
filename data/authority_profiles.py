from __future__ import annotations


AUTHORITY_PLACEHOLDER_NOTE = (
    "Replace the placeholder author and reviewer details with real named expert profiles "
    "before these pages are treated as finished public guidance."
)

GUIDANCE_EMAIL = "guidance@ukplanningguide.co.uk"
GUIDANCE_FORM_PATH = "/personalised-planning-guidance/request/"
GUIDANCE_SUCCESS_PATH = "/personalised-planning-guidance/request/success/"
EDITORIAL_POLICY_PATH = "/editorial-policy/"

DEFAULT_AUTHOR_SLUG = "lead_author"
DEFAULT_REVIEWER_SLUG = "lead_reviewer"


SITE_ORGANIZATION = {
    "name": "UK Planning Guide",
    "legal_name": "UK Planning Guide",
    "url": "https://ukplanningguide.co.uk/",
    "logo": "https://ukplanningguide.co.uk/assets/images/logo-main.png",
    "contact_email": GUIDANCE_EMAIL,
    "description": (
        "Answer-first planning guidance for homeowners, small developers and property "
        "researchers who need to know what usually applies before they commit to "
        "drawings, consultants or applications."
    ),
    "same_as": (),
    "about_path": "/about/",
    "methodology_path": "/methodology/",
    "privacy_path": "/privacy/",
    "editorial_policy_path": EDITORIAL_POLICY_PATH,
}


AUTHORITY_PROFILES = {
    "lead_author": {
        "slug": "lead_author",
        "name": "Sam Jones",
        "role": "Founder and primary planning content author",
        "short_bio": (
            "Independent publisher behind UK Planning Guide, focused on turning planning "
            "rules, local authority sources and early-stage project risk into practical "
            "plain-English guidance."
        ),
        "credentials": (
            "Builds and maintains UK Planning Guide's planning content, local-authority "
            "coverage and decision-support tools with an emphasis on official sources, "
            "clear route guidance and honest escalation points."
        ),
        "expertise_scope": (
            "Domestic planning routes, permitted development interpretation, local-authority "
            "variation, and early-stage planning risk triage."
        ),
        "profile_slug": "sam-jones",
        "headshot_path": "/assets/images/logo-main.png",
        "contact_email": GUIDANCE_EMAIL,
        "proof_links": (),
        "is_placeholder": False,
    },
    "lead_reviewer": {
        "slug": "lead_reviewer",
        "name": "UK Planning Guide Editorial Review Desk",
        "role": "Editorial review and source checking",
        "short_bio": (
            "Review layer responsible for official-source context, escalation wording and checks "
            "that pages stay clear about what is national guidance, what is local context "
            "and what still needs formal confirmation."
        ),
        "credentials": (
            "Applies the site's editorial review checklist across official-source context, visible "
            "ownership, update signals and clarity around where broad guidance stops "
            "being enough on its own."
        ),
        "expertise_scope": (
            "Editorial review, source verification, escalation guidance, and borderline "
            "planning-risk wording."
        ),
        "profile_slug": "lead-reviewer",
        "headshot_path": "/assets/images/logo-main.png",
        "contact_email": GUIDANCE_EMAIL,
        "proof_links": (),
        "is_placeholder": False,
    },
}


def authority_profile(slug: str) -> dict:
    return dict(AUTHORITY_PROFILES.get(slug or "", AUTHORITY_PROFILES[DEFAULT_AUTHOR_SLUG]))


def site_organization_profile() -> dict:
    return dict(SITE_ORGANIZATION)
