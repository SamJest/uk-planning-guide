from __future__ import annotations

from datetime import date, timedelta
import importlib.util
from pathlib import Path
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]

from data.organic_growth import CTR_TEST_ID, CTR_TEST_TARGETS, growth_target_for_path
from utils.indexation import (
    CANONICAL,
    INDEXABLE,
    NOINDEX,
    derive_indexation_decision,
    search_owner_for_path,
)


def _load_report_module():
    path = ROOT / "scripts" / "24_report_qualified_organic_growth.py"
    spec = importlib.util.spec_from_file_location("qualified_growth_report", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class QualifiedOrganicGrowthTests(unittest.TestCase):
    def test_ctr_cohort_is_decision_complete(self):
        self.assertEqual(len(CTR_TEST_TARGETS), 4)
        for path, target in CTR_TEST_TARGETS.items():
            self.assertEqual(target["growth_cohort"], CTR_TEST_ID)
            self.assertTrue(target["meta_title"])
            self.assertTrue(target["meta_description"])
            self.assertTrue(target["search_owner"])
            self.assertEqual(growth_target_for_path(path), target)

    def test_indexation_states_follow_html_contract(self):
        indexed = derive_indexation_decision(
            "/councils/sheffield/",
            '<link rel="canonical" href="https://ukplanningguide.co.uk/councils/sheffield/">',
        )
        self.assertEqual(indexed.index_state, INDEXABLE)
        self.assertEqual(indexed.cohort, CTR_TEST_ID)

        noindex = derive_indexation_decision(
            "/local-search/",
            '<meta name="robots" content="noindex, follow"><link rel="canonical" href="https://ukplanningguide.co.uk/local-search/">',
        )
        self.assertEqual(noindex.index_state, NOINDEX)

        canonical = derive_indexation_decision(
            "/old-page/",
            '<link rel="canonical" href="https://ukplanningguide.co.uk/new-page/">',
        )
        self.assertEqual(canonical.index_state, CANONICAL)
        self.assertEqual(canonical.canonical_target, "/new-page/")

    def test_local_search_bridge_resolves_to_search_owner(self):
        self.assertEqual(
            search_owner_for_path("/local-search/planning-portal-sheffield/"),
            "/councils/sheffield/",
        )

    def test_incident_requires_three_complete_material_drops(self):
        report = _load_report_module()
        start = date(2026, 5, 1)
        rows = []
        for index in range(42):
            rows.append(
                {
                    "date": start + timedelta(days=index),
                    "clicks": 100,
                    "impressions": 5000,
                    "position": 10.0,
                }
            )
        rows[-1]["clicks"] = 1
        rows[-1]["impressions"] = 50
        self.assertFalse(report._incident_status(rows)["alert"])
        for row in rows[-3:]:
            row["clicks"] = 1
            row["impressions"] = 50
        self.assertTrue(report._incident_status(rows)["alert"])


if __name__ == "__main__":
    unittest.main()
