from __future__ import annotations

from datetime import date
import unittest

from utils.monetisation import MonetisationContext, ad_eligibility, select_partner


class MonetisationControlTests(unittest.TestCase):
    def test_monetisation_defaults_to_ineligible(self):
        context = MonetisationContext(
            route="/garden-rooms/",
            page_family="project_guide",
            jurisdiction="england",
            quality_pass=True,
            indexable=True,
            consent_ready=True,
        )
        decision = ad_eligibility(context)
        self.assertFalse(decision.eligible)
        self.assertIn("global_disabled", decision.reasons)
        self.assertIn("ads_disabled", decision.reasons)

    def test_ads_are_never_eligible_on_tools(self):
        config = {
            "global_enabled": True,
            "consent_ready": True,
            "ads": {
                "enabled": True,
                "provider": "reviewed-provider",
                "rollout_percent": 10,
                "allowed_page_families": ["project_guide"],
                "excluded_page_families": ["tool"],
                "excluded_path_prefixes": ["/tools/"],
            },
        }
        context = MonetisationContext(
            route="/tools/planning-route-check/",
            page_family="tool",
            jurisdiction="uk",
            quality_pass=True,
            indexable=True,
            consent_ready=True,
        )
        self.assertFalse(ad_eligibility(context, config).eligible)

    def test_unapproved_or_expired_partner_is_suppressed(self):
        config = {"global_enabled": True, "referrals": {"enabled": True}}
        context = MonetisationContext(
            route="/garden-rooms/essex/colchester/",
            page_family="local_project",
            jurisdiction="england",
            project_type="garden-rooms",
            quality_pass=True,
            indexable=True,
            consent_ready=True,
        )
        base = {
            "partner_id": "example",
            "name": "Example",
            "category": "planning-drawings",
            "jurisdictions": ["england"],
            "project_types": ["garden-rooms"],
            "url_template": "https://example.invalid/",
            "commercial_model": "cpa",
            "disclosure_text": "Commercial link",
            "active_from": "2026-01-01",
            "expires_at": "2026-12-31",
            "priority": 1,
            "fallback": "/tools/planning-application-readiness-checker/",
            "last_verified": "2026-09-06",
        }
        for owner_approved, expiry in ((False, "2026-12-31"), (True, "2026-01-02")):
            partner = dict(base, owner_approved=owner_approved, expires_at=expiry)
            selected = select_partner(
                context,
                category="planning-drawings",
                config=config,
                registry={"partners": [partner]},
                today=date(2026, 9, 6),
            )
            self.assertIsNone(selected)


if __name__ == "__main__":
    unittest.main()
