from __future__ import annotations

import unittest

from components.official_sources import build_official_sources_block
from data.scenario_data import SCENARIOS
from utils.official_sources import COUNCIL_LOOKUP, OfficialSourceContext, relevant_official_sources


class SourceBackedGenericPageTests(unittest.TestCase):
    def test_authority_source_cards_are_explicit_local_facts(self):
        authority_slug, council = next(iter(COUNCIL_LOOKUP.items()))
        html = build_official_sources_block(
            page_family="council",
            authority_slug=authority_slug,
            country_slug=council.get("country_slug", ""),
        )
        self.assertIn('data-purpose="labelled-example"', html)
        self.assertGreaterEqual(html.count('data-local-fact="true"'), 3)

    def test_every_authority_profile_has_an_official_source_floor(self):
        for authority_slug, council in COUNCIL_LOOKUP.items():
            sources = relevant_official_sources(
                OfficialSourceContext(
                    page_family="council",
                    authority_slug=authority_slug,
                    country_slug=council.get("country_slug", ""),
                    max_links=5,
                )
            )
            self.assertGreaterEqual(len(sources), 3, authority_slug)

    def test_every_local_rule_route_has_an_official_source_floor(self):
        for authority_slug, council in COUNCIL_LOOKUP.items():
            for scenario in SCENARIOS:
                sources = relevant_official_sources(
                    OfficialSourceContext(
                        page_family="scenario",
                        authority_slug=authority_slug,
                        country_slug=council.get("country_slug", ""),
                        scenario_slug=scenario["slug"],
                        max_links=5,
                    )
                )
                self.assertGreaterEqual(
                    len(sources),
                    3,
                    f"{scenario['slug']}/{authority_slug}",
                )


if __name__ == "__main__":
    unittest.main()
