from __future__ import annotations


GROWTH_RELEASE = "qualified-organic-growth-2026-07-03"
CTR_TEST_ID = "ctr-cohort-01-2026-07-03"
CTR_TEST_START = "2026-07-03"
CTR_TEST_MIN_DAYS = 28
CTR_TEST_BATCH_SIZE = 20


CTR_TEST_TARGETS = {
    "/councils/sheffield/": {
        "meta_title": "Sheffield planning portal: official links and local checks",
        "meta_description": "Open Sheffield's official planning links, then use the local project and rule checks that help identify the right permission route.",
        "title": "Open The Official Sheffield Route, Then Narrow The Project",
        "answer": "For a Sheffield planning search, start with the official council portal or application source. Then move to the local project or rule guide that matches the proposed work rather than relying on one broad council answer.",
        "checks": (
            "Open the official application, validation or planning-record source first.",
            "Choose the local project guide once the build type is clear.",
            "Check conservation, Article 4 or HMO controls where special restrictions may apply.",
        ),
        "next_step": "Check the official Sheffield sources below, or run the route check if the project type is not settled yet.",
        "primary_href": "/tools/planning-route-check/",
        "primary_label": "Check your likely planning route",
        "cluster": "planning-portal",
        "growth_cohort": CTR_TEST_ID,
        "search_owner": "/councils/sheffield/",
        "baseline_impressions": 2841,
        "baseline_clicks": 9,
        "baseline_ctr": 0.0032,
        "baseline_position": 11.83,
    },
    "/conservation-areas/glasgow-city/": {
        "meta_title": "Glasgow conservation areas: official map and local checks",
        "meta_description": "Check the official Glasgow conservation-area source, heritage controls and the local planning route before relying on a general project rule.",
        "title": "Check The Official Glasgow Conservation Area First",
        "answer": "For Glasgow, first confirm whether the property sits inside a conservation area using the official heritage source. That location check determines how cautiously to treat alterations, demolition, materials and the project-specific planning route.",
        "checks": (
            "Confirm the property's position against the official conservation-area information.",
            "Check whether materials, demolition, frontage or visibility make the proposal more sensitive.",
            "Apply the relevant project rule only after the heritage position is clear.",
        ),
        "next_step": "Use the official Glasgow sources below, then open the relevant project guide or route check.",
        "primary_href": "/tools/planning-route-check/",
        "primary_label": "Check your likely planning route",
        "cluster": "conservation-map",
        "growth_cohort": CTR_TEST_ID,
        "search_owner": "/conservation-areas/glasgow-city/",
        "baseline_impressions": 2700,
        "baseline_clicks": 4,
        "baseline_ctr": 0.0015,
        "baseline_position": 8.05,
    },
    "/hmos/northamptonshire/north-northamptonshire/": {
        "meta_title": "North Northamptonshire HMO Article 4: areas and checks",
        "meta_description": "Check North Northamptonshire HMO Article 4 coverage, change-of-use risk and official local sources before relying on permitted development.",
        "title": "Settle Article 4 Coverage Before Relying On The HMO Route",
        "answer": "For an HMO in North Northamptonshire, the first question is whether the exact property is affected by Article 4 or another local change-of-use restriction. Confirm that position before treating permitted development as available.",
        "checks": (
            "Confirm the exact property and council area.",
            "Check current Article 4 coverage and HMO change-of-use guidance.",
            "Review concentration, parking, refuse and neighbour-impact policy before committing.",
        ),
        "next_step": "Check the official local sources below, then run the route check if the proposed use is still uncertain.",
        "primary_href": "/tools/planning-route-check/",
        "primary_label": "Check your likely planning route",
        "cluster": "hmo-article-4",
        "growth_cohort": CTR_TEST_ID,
        "search_owner": "/hmos/northamptonshire/north-northamptonshire/",
        "baseline_impressions": 2378,
        "baseline_clicks": 2,
        "baseline_ctr": 0.0008,
        "baseline_position": 9.17,
    },
    "/hmos/leicestershire/oadby-and-wigston/": {
        "meta_title": "Oadby and Wigston HMO Article 4: areas and checks",
        "meta_description": "Check Oadby and Wigston HMO Article 4 coverage, change-of-use risk and official council sources before relying on permitted development.",
        "title": "Check Article 4 Coverage And HMO Change Of Use First",
        "answer": "For an HMO in Oadby and Wigston, confirm whether Article 4 or local change-of-use policy affects the exact property before relying on permitted development. Local concentration and amenity policy can matter even when the broad route looks simple.",
        "checks": (
            "Confirm the exact property position and current Article 4 coverage.",
            "Check the proposed HMO use class and whether a change of use is involved.",
            "Review local concentration, parking, refuse and neighbour-impact policy.",
        ),
        "next_step": "Check the official council sources below, then use the route checker if the use-class position remains unclear.",
        "primary_href": "/tools/planning-route-check/",
        "primary_label": "Check your likely planning route",
        "cluster": "hmo-article-4",
        "growth_cohort": CTR_TEST_ID,
        "search_owner": "/hmos/leicestershire/oadby-and-wigston/",
        "baseline_impressions": 2263,
        "baseline_clicks": 3,
        "baseline_ctr": 0.0013,
        "baseline_position": 6.77,
    },
}


PROTECTED_SEARCH_FAMILIES = frozenset(
    {
        "fences-and-walls",
        "heat-pumps",
        "permitted-development",
        "solar-panels",
    }
)


INDEXATION_POLICY = {
    "fresh_data_hours": 72,
    "zero_impression_windows_before_noindex": 2,
    "window_days": 28,
    "incident_drop_threshold": 0.40,
    "incident_consecutive_days": 3,
    "ctr_test_revert_click_drop": 0.15,
    "qualified_user_growth_target": 0.20,
    "ctr_relative_growth_target": 0.25,
    "maximum_click_loss_during_consolidation": 0.05,
}


def growth_target_for_path(path: str) -> dict:
    clean = "/" + str(path or "").strip("/")
    if clean != "/":
        clean += "/"
    return CTR_TEST_TARGETS.get(clean, {})


def growth_cohort_for_path(path: str) -> str:
    return str(growth_target_for_path(path).get("growth_cohort", ""))

