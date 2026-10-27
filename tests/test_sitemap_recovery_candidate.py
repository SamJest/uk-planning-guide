from __future__ import annotations

import importlib.util
from pathlib import Path
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "scripts" / "38_prepare_sitemap_exclusion_candidate.py"
SPEC = importlib.util.spec_from_file_location("sitemap_recovery_candidate", PATH)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)


class SitemapRecoveryCandidateTests(unittest.TestCase):
    def test_exact_line_removal_preserves_unrelated_bytes(self):
        remove = "https://ukplanningguide.co.uk/noindex/"
        keep = "https://ukplanningguide.co.uk/keep/"
        text = f"<urlset>\n  <url><loc>{remove}</loc></url>\n  <url><loc>{keep}</loc></url>\n</urlset>\n"
        filtered, removed = MODULE.remove_exact_url_lines(text, {remove})
        self.assertEqual(removed, {remove})
        self.assertNotIn(remove, filtered)
        self.assertIn(f"  <url><loc>{keep}</loc></url>\n", filtered)

    def test_duplicate_exact_url_is_rejected(self):
        url = "https://ukplanningguide.co.uk/duplicate/"
        text = f"<url><loc>{url}</loc></url>\n<url><loc>{url}</loc></url>\n"
        with self.assertRaisesRegex(ValueError, "Duplicate sitemap entry"):
            MODULE.remove_exact_url_lines(text, {url})


if __name__ == "__main__":
    unittest.main()
