COUNTRY_META = {
    "england": {
        "name": "England",
        "system_label": "English planning system",
        "baseline_label": "National rule baseline",
        "householder_label": "national householder rules",
        "notice_title": "Country context",
        "notice_body": "This page is written against the English planning baseline and local authority context.",
        "notice_checks": [
            "Use local authority pages when conservation areas, listed buildings or Article 4 could change the answer.",
            "Treat close-to-the-limit schemes as verification cases rather than summary-answer cases.",
        ],
    },
    "wales": {
        "name": "Wales",
        "system_label": "Welsh planning system",
        "baseline_label": "Welsh rule baseline",
        "householder_label": "Welsh householder rules",
        "notice_title": "Welsh planning context",
        "notice_body": "Wales has its own planning regime and householder guidance, so English assumptions should not be copied across without checking the Welsh route properly.",
        "notice_checks": [
            "Use this page as a route-finding guide, not as proof that English thresholds apply unchanged in Wales.",
            "Verify the local authority position if the project is close to a limit or the wording still feels generic.",
        ],
    },
    "scotland": {
        "name": "Scotland",
        "system_label": "Scottish planning system",
        "baseline_label": "Scottish rule baseline",
        "householder_label": "Scottish householder rules",
        "notice_title": "Scottish planning context",
        "notice_body": "Scotland has its own planning regime and householder guidance, so the safest route is to treat this as a Scotland-aware guide rather than a recycled England answer.",
        "notice_checks": [
            "Do not assume the English householder route applies unchanged in Scotland.",
            "Use the local authority page and verify exact thresholds where the proposal is close to a limit.",
        ],
    },
    "northern-ireland": {
        "name": "Northern Ireland",
        "system_label": "Northern Ireland planning system",
        "baseline_label": "Northern Ireland rule baseline",
        "householder_label": "Northern Ireland householder rules",
        "notice_title": "Northern Ireland planning context",
        "notice_body": "Northern Ireland planning coverage still needs dedicated data, so any future pages should launch only with NI-specific rules and terminology.",
        "notice_checks": [
            "Do not reuse English, Welsh or Scottish householder assumptions for Northern Ireland.",
            "Add dedicated Northern Ireland rule layers before publishing NI pages at scale.",
        ],
    },
}

SPECIAL_COUNTY_COUNTRIES = {
    "wales": "wales",
    "scotland": "scotland",
    "northern-ireland": "northern-ireland",
}


def get_country_slug(county_slug: str) -> str:
    return SPECIAL_COUNTY_COUNTRIES.get(str(county_slug or "").strip().lower(), "england")


def get_country_meta(county_slug: str) -> dict:
    return COUNTRY_META[get_country_slug(county_slug)]


def get_country_name(county_slug: str) -> str:
    return get_country_meta(county_slug)["name"]


def get_system_label(county_slug: str) -> str:
    return get_country_meta(county_slug)["system_label"]


def get_householder_label(county_slug: str) -> str:
    return get_country_meta(county_slug)["householder_label"]


def get_baseline_label(county_slug: str) -> str:
    return get_country_meta(county_slug)["baseline_label"]


def is_non_english_context(county_slug: str) -> bool:
    return get_country_slug(county_slug) != "england"
