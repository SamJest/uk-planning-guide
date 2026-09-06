import importlib.util
from pathlib import Path
import tempfile
import unittest


SCRIPT_PATH = Path(__file__).resolve().parents[1] / "scripts" / "42_analyse_clicked_404s.py"
SPEC = importlib.util.spec_from_file_location("clicked_404_analysis", SCRIPT_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(MODULE)


class Clicked404AnalysisTests(unittest.TestCase):
    def test_maps_clicked_missing_url_to_existing_direct_parent_without_authorising_redirect(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            ledger = root / "ledger.csv"
            ledger.write_text(
                "url,family,http_status,clicks\n"
                "https://ukplanningguide.co.uk/garden-rooms/county/authority/article-4/,garden-rooms,404_verified,3\n",
                encoding="utf-8",
            )
            parent = root / "site" / "garden-rooms" / "county" / "authority"
            parent.mkdir(parents=True)
            (parent / "index.html").write_text("parent", encoding="utf-8")

            report = MODULE.analyse(ledger, root / "site")

        self.assertEqual(report["status"], "passed")
        self.assertEqual(report["clicked_404_count"], 1)
        self.assertEqual(report["clicked_404_clicks"], 3)
        self.assertEqual(report["redirects_authorised"], 0)
        self.assertEqual(report["restorations_authorised"], 0)
        self.assertEqual(report["findings"][0]["same_authority_parent"], "/garden-rooms/county/authority/")
        self.assertTrue(report["findings"][0]["parent_exists"])


if __name__ == "__main__":
    unittest.main()
