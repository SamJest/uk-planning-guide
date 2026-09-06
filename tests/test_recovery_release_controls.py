from __future__ import annotations

import importlib.util
import os
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

from core.build_scope import BuildScopeError, build_mode, should_publish_route
from core.files import write_file
from core.paths import ROOT
from utils.build_provenance import source_fingerprint
from utils.content_contracts import ContractError


def load_script(name: str):
    path = ROOT / "scripts" / name
    spec = importlib.util.spec_from_file_location(name.replace(".py", ""), path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class PublicationContainmentTests(unittest.TestCase):
    def test_missing_scope_fails_closed(self):
        with patch.dict(os.environ, {}, clear=True):
            with self.assertRaises(BuildScopeError):
                build_mode()
            with self.assertRaises(BuildScopeError):
                should_publish_route("/")

    def test_unknown_scope_fails_closed(self):
        with patch.dict(os.environ, {"UKPG_BUILD_MODE": "preview"}, clear=True):
            with self.assertRaises(BuildScopeError):
                build_mode()

    def test_build_inputs_have_a_stable_fingerprint(self):
        first = source_fingerprint(ROOT)
        second = source_fingerprint(ROOT)
        self.assertEqual(first, second)
        self.assertRegex(first, r"^[0-9a-f]{64}$")

    def test_explicit_canary_scope_is_limited(self):
        with patch.dict(os.environ, {"UKPG_BUILD_MODE": "canary"}, clear=True):
            self.assertEqual(build_mode(), "canary")
            self.assertFalse(should_publish_route("/not-in-the-reviewed-canary/"))

    def test_page_write_outside_configured_output_is_rejected(self):
        with tempfile.TemporaryDirectory() as folder:
            with patch.dict(os.environ, {"UKPG_BUILD_MODE": "canary"}, clear=True):
                with self.assertRaises(BuildScopeError):
                    write_file(Path(folder), "index.html", "unsafe")

    def test_legacy_full_corpus_package_is_disabled(self):
        with self.assertRaisesRegex(SystemExit, "disabled by the 2026-09 recovery audit"):
            load_script("30_package_full_site_candidate.py").main()

    def test_legacy_full_output_overlay_is_disabled(self):
        with self.assertRaisesRegex(SystemExit, "disabled by the 2026-09 recovery audit"):
            load_script("31_apply_canary_to_full_output.py").main()

    def test_uncontracted_local_rule_generation_fails_closed(self):
        from generators import scenario_pages

        councils = {"example-county": [{"town_slug": "example", "town_name": "Example"}]}
        scenarios = [{"slug": "permitted-development", "title": "Permitted development"}]
        with (
            patch.object(scenario_pages, "load_councils", return_value=councils),
            patch.object(scenario_pages, "load_projects", return_value=[]),
            patch.object(scenario_pages, "load_scenarios", return_value=scenarios),
            patch.object(scenario_pages, "should_render_route", return_value=True),
            patch.object(scenario_pages, "_generate_contract_local_rule_page", return_value=False),
        ):
            with self.assertRaisesRegex(ContractError, "Refusing to synthesize a local-rule page"):
                scenario_pages.generate_scenario_pages()

    def test_uncontracted_authority_generation_fails_closed(self):
        from generators import council_pages

        councils = {"example-county": [{"town_slug": "example", "town_name": "Example"}]}
        with (
            patch.object(council_pages, "load_councils", return_value=councils),
            patch.object(council_pages, "load_projects", return_value=[]),
            patch.object(council_pages, "load_scenarios", return_value=[]),
            patch.object(council_pages, "should_render_route", return_value=True),
            patch.object(council_pages, "_generate_contract_authority_profile", return_value=False),
        ):
            with self.assertRaisesRegex(ContractError, "Refusing to synthesize an authority profile"):
                council_pages.generate_council_pages()



if __name__ == "__main__":
    unittest.main()
