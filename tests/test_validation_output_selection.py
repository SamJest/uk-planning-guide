from __future__ import annotations

import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]


class ValidationOutputSelectionTests(unittest.TestCase):
    def test_validation_honours_build_output_environment(self):
        with tempfile.TemporaryDirectory(dir=ROOT / "artifacts") as temporary:
            expected = Path(temporary).resolve()
            environment = dict(os.environ)
            environment["UKPG_OUTPUT_DIR"] = str(expected)
            completed = subprocess.run(
                [sys.executable, "-c", "import validate; print(validate.OUTPUT_DIR)"],
                cwd=ROOT,
                env=environment,
                capture_output=True,
                text=True,
                check=True,
            )
        self.assertEqual(Path(completed.stdout.strip()), expected)

    def test_duplicate_id_check_ignores_data_attributes(self):
        from validate import _duplicate_ids

        html = (
            '<a data-source-id="official-source">First citation</a>'
            '<a data-source-id="official-source">Second citation</a>'
            '<section id="unique-section"></section>'
        )
        self.assertEqual(_duplicate_ids(html), [])

    def test_duplicate_id_check_still_reports_real_ids(self):
        from validate import _duplicate_ids

        html = '<section id="repeated"></section><div id="repeated"></div>'
        self.assertEqual(_duplicate_ids(html), ["repeated"])

    def test_custom_404_is_not_treated_as_a_canonical_route(self):
        import validate

        pages = [validate.OUTPUT_DIR / "404.html", validate.OUTPUT_DIR / "index.html"]
        selected = validate.pages_for_health_scan(pages)
        self.assertNotIn(validate.OUTPUT_DIR / "404.html", selected)
        self.assertIn(validate.OUTPUT_DIR / "index.html", selected)

    def test_release_policy_allows_only_declared_operational_noindex_routes(self):
        from validate import _is_allowed_noindex

        self.assertTrue(_is_allowed_noindex("/england/services/", "england-services-hub"))
        self.assertTrue(_is_allowed_noindex("/updates/phase-0-integrity-repair/", "misc"))
        self.assertTrue(_is_allowed_noindex("/england/rules/article-4/colchester/", "country-rule-page"))
        self.assertFalse(_is_allowed_noindex("/planning-permission/bedford/", "scenario-pages"))


if __name__ == "__main__":
    unittest.main()
