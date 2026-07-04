from __future__ import annotations

import unittest

from core.paths import ROOT
from utils.phase0_validation import validate_phase0_canary


class PhaseZeroCanaryOutputTests(unittest.TestCase):
    def test_generated_canary_passes_contract_checks(self):
        output = ROOT / "artifacts" / "phase-0-canary-site"
        if not (output / "sitemap.xml").exists():
            self.skipTest("Run build_site.py to generate the Phase 0 canary first")
        report = validate_phase0_canary(output)
        self.assertEqual(report["errors"], [])


if __name__ == "__main__":
    unittest.main()

