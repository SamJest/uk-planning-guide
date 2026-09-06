from __future__ import annotations

import json
from pathlib import Path
import unittest

from core.paths import ROOT
from utils.build_provenance import source_fingerprint
from utils.phase0_validation import validate_phase0_canary


class PhaseZeroCanaryOutputTests(unittest.TestCase):
    def test_generated_canary_passes_contract_checks(self):
        expected_fingerprint = source_fingerprint(ROOT)
        candidates = [ROOT / "artifacts" / "phase-0-canary-site"]
        builds_root = ROOT / "artifacts" / "builds"
        if builds_root.exists():
            candidates.extend(
                sorted(
                    (path for path in builds_root.iterdir() if path.is_dir()),
                    key=lambda path: path.stat().st_mtime,
                    reverse=True,
                )
            )
        output = next(
            (
                path
                for path in candidates
                if (path / "sitemap.xml").exists()
                and (path / "BUILD-MANIFEST.json").exists()
                and json.loads((path / "BUILD-MANIFEST.json").read_text(encoding="utf-8")).get("source_fingerprint")
                == expected_fingerprint
            ),
            None,
        )
        if output is None:
            self.skipTest("Run build_site.py to generate the Phase 0 canary first")
        manifest_path = output / "BUILD-MANIFEST.json"
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        baseline = manifest.get("validation_baseline")
        report = validate_phase0_canary(output, baseline_dir=Path(baseline) if baseline else None)
        self.assertEqual(report["errors"], [])


if __name__ == "__main__":
    unittest.main()
