from __future__ import annotations

from datetime import date, timedelta
import importlib.util
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]

from components.gsc_cluster_links import build_gsc_cluster_links
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


def _load_indexation_builder_module():
    path = ROOT / "scripts" / "23_generate_growth_indexation_manifest.py"
    spec = importlib.util.spec_from_file_location("growth_indexation_builder", path)
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

    def test_full_manifest_reads_rendered_noindex_state(self):
        builder = _load_indexation_builder_module()
        with tempfile.TemporaryDirectory(dir=ROOT / "artifacts") as temporary:
            output = Path(temporary)
            page = output / "updates" / "review-only" / "index.html"
            page.parent.mkdir(parents=True)
            page.write_text(
                '<meta name="robots" content="noindex, follow">'
                '<link rel="canonical" href="https://ukplanningguide.co.uk/updates/review-only/">',
                encoding="utf-8",
            )
            captured = []
            with (
                patch.object(builder, "OUTPUT_FOLDER", output),
                patch.object(builder, "write_indexation_manifest", side_effect=lambda rows: captured.extend(rows)),
            ):
                builder.build_manifest()
        self.assertEqual(len(captured), 1)
        self.assertEqual(captured[0].index_state, NOINDEX)

    def test_blocked_cluster_hub_is_not_linked(self):
        html = build_gsc_cluster_links("/local-search/garden-room-scotland-planning/")
        self.assertNotIn("/local-search/porch-outbuilding-country-rules/", html)

    def test_blocked_cluster_hub_is_not_a_required_release_target(self):
        from data.search_demand_priorities import (
            DATA_LED_LOCAL_SEARCH_SLUGS,
            GSC_CLUSTER_HUB_SLUGS,
            GSC_EXPANSION_LOCAL_SEARCH_SLUGS,
        )

        blocked_slug = "porch-outbuilding-country-rules"
        self.assertNotIn(blocked_slug, GSC_CLUSTER_HUB_SLUGS)
        self.assertNotIn(blocked_slug, GSC_EXPANSION_LOCAL_SEARCH_SLUGS)
        self.assertNotIn(blocked_slug, DATA_LED_LOCAL_SEARCH_SLUGS)

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
