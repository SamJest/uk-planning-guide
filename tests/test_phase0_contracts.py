from __future__ import annotations

import json
import os
from pathlib import Path
import tempfile
import unittest

from core.paths import ROOT
from utils.content_contracts import ContractError, LOCAL_FAMILIES, load_page_records, page_records_by_route, validate_page_record
from utils.content_integrity import lint_rendered_html, simhash64, simhash_similarity
from utils.source_registry import load_source_registry, source_registry_by_id, validate_page_source_links
from utils.url_registry import load_canary_routes, load_redirects, validate_url_registry


class PhaseZeroContractTests(unittest.TestCase):
    def test_exact_canary_manifest_matches_records(self):
        routes = load_canary_routes()
        self.assertEqual(len(routes["publish_routes"]), 24)
        self.assertEqual(set(routes["publish_routes"]), set(page_records_by_route()))

    def test_generic_records_never_assume_a_project(self):
        generic = {"national_guide", "rule_guide", "authority_profile", "local_rule"}
        for record in load_page_records():
            if record["page_family"] in generic:
                self.assertIsNone(record["project_id"], record["route_path"])

    def test_indexable_local_records_have_evidence_floor(self):
        sources = source_registry_by_id()
        for record in load_page_records():
            if record["page_family"] not in LOCAL_FAMILIES or record["index_status"] != "index":
                continue
            active_local = {
                source_id
                for source_id in record["source_ids"]
                if sources[source_id]["status"] == "active" and sources[source_id]["authority_id"] == record["authority_id"]
            }
            self.assertGreaterEqual(len(active_local), 3, record["route_path"])
            self.assertGreaterEqual(len(record["unique_local_facts"]), 5, record["route_path"])

    def test_all_claim_and_fact_sources_exist_and_match(self):
        self.assertGreaterEqual(len(load_source_registry()), 12)
        validate_page_source_links()

    def test_redirects_have_no_chains_or_loops(self):
        redirects = load_redirects()
        sources = {item["source_path"] for item in redirects}
        targets = {item["target_path"] for item in redirects if item["status_code"] != 410}
        self.assertFalse(sources & targets)
        validate_url_registry()

    def test_phase_zero_signoff_blocks_full_build(self):
        signoff = json.loads((ROOT / "docs" / "phase-0-signoff.json").read_text(encoding="utf-8"))
        self.assertIs(signoff["approved"], False)
        self.assertIsNone(signoff["canary_report_sha256"])
        self.assertIsNone(signoff["source_fingerprint"])


class PhaseZeroIntegrityTests(unittest.TestCase):
    def test_multi_authority_local_record_is_rejected(self):
        record = dict(page_records_by_route()["/councils/sheffield/"])
        record["authority_id"] = "sheffield,rotherham"
        record["route_path"] = "/councils/sheffield-rotherham/"
        record["canonical_path"] = record["route_path"]
        with self.assertRaisesRegex(ContractError, "one normalized identifier"):
            validate_page_record(record)

    def test_authority_profile_cannot_select_a_rule(self):
        record = dict(page_records_by_route()["/councils/sheffield/"])
        record["rule_id"] = "article-4"
        with self.assertRaisesRegex(ContractError, "cannot carry a selected rule"):
            validate_page_record(record)

    def test_authority_profile_rejects_unlabelled_project_leakage(self):
        record = {
            "page_family": "authority_profile",
            "jurisdiction": "england",
            "authority_id": "example",
            "project_id": None,
            "rule_id": None,
            "review_status": "source_checked",
            "index_status": "index",
        }
        findings = lint_rendered_html(record, "<main><p>A garden room is the assumed setup.</p></main>")
        codes = {finding.code for finding in findings}
        self.assertIn("cross-family-project-language", codes)
        self.assertIn("generic-assumed-setup", codes)

    def test_labelled_navigation_is_not_treated_as_page_intent(self):
        record = {
            "page_family": "authority_profile",
            "jurisdiction": "england",
            "authority_id": "example",
            "project_id": None,
            "rule_id": None,
            "review_status": "source_checked",
            "index_status": "index",
        }
        html = '<section data-purpose="project-navigation"><a>Garden rooms</a><a>Dropped kerbs</a></section>'
        self.assertFalse(lint_rendered_html(record, html))

    def test_article_four_rejects_garden_room_context(self):
        record = {
            "page_family": "local_rule",
            "jurisdiction": "england",
            "authority_id": "example",
            "project_id": None,
            "rule_id": "article-4",
            "review_status": "source_checked",
            "index_status": "noindex",
        }
        codes = {finding.code for finding in lint_rendered_html(record, "<p>Check the garden room trigger.</p>")}
        self.assertIn("article4-garden-room-leak", codes)

    def test_devolved_page_rejects_unqualified_england_rule(self):
        record = {
            "page_family": "local_project",
            "jurisdiction": "wales",
            "authority_id": "cardiff",
            "project_id": "dropped-kerbs",
            "rule_id": None,
            "review_status": "source_checked",
            "index_status": "noindex",
        }
        codes = {finding.code for finding in lint_rendered_html(record, "<p>Use the General Permitted Development Order 2015.</p>")}
        self.assertIn("jurisdiction-leak", codes)

    def test_simhash_detects_repeated_copy(self):
        left = simhash64("the same planning guidance repeated across a local page")
        right = simhash64("the same planning guidance repeated across a local page")
        self.assertEqual(simhash_similarity(left, right), 1.0)


if __name__ == "__main__":
    unittest.main()
