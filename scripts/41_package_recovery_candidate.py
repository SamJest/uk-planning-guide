"""Package a small, hash-bound recovery patch without touching production."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from utils.build_provenance import source_fingerprint
from utils.phase0_validation import output_file_for_route


PRODUCTION_COMMIT = "aa7d89ec029c70d5973b7d982fcbe5036316d9b2"
PRODUCTION_TREE = "9c640ff1b40473f2e025e9368ac008d41b1e5cc5"
PAGE_ROUTES = (
    "/permitted-development/north-yorkshire/",
    "/conservation-areas/glasgow-city/",
    "/councils/sheffield/",
    "/tools/",
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def copy_change(source: Path, before: Path, output: Path, relative: Path, change_type: str) -> dict:
    if not source.is_file() or not before.is_file():
        raise SystemExit(f"Candidate blocked: expected file missing for {relative.as_posix()}")
    target = output / relative
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, target)
    before_hash, after_hash = sha256(before), sha256(target)
    if before_hash == after_hash:
        raise SystemExit(f"Candidate blocked: declared change is byte-identical: {relative.as_posix()}")
    return {
        "path": relative.as_posix(),
        "type": change_type,
        "before_sha256": before_hash,
        "after_sha256": after_hash,
        "rollback": f"Restore {before_hash} through a normal revert commit.",
    }


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base", type=Path, required=True)
    parser.add_argument("--site", type=Path, required=True)
    parser.add_argument("--sitemap-candidate", type=Path, required=True)
    parser.add_argument("--semantic-report", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)
    base, site = args.base.resolve(), args.site.resolve()
    sitemap_candidate, output = args.sitemap_candidate.resolve(), args.output.resolve()
    if output.exists():
        raise SystemExit(f"Candidate blocked: output already exists and will not be overwritten: {output}")
    tree = subprocess.check_output(["git", "-C", str(base), "rev-parse", "HEAD^{tree}"], text=True).strip()
    if tree != PRODUCTION_TREE:
        raise SystemExit(f"Candidate blocked: base tree {tree} is not verified production tree {PRODUCTION_TREE}")
    build_manifest = json.loads((site / "BUILD-MANIFEST.json").read_text(encoding="utf-8"))
    current_fingerprint = source_fingerprint(ROOT)
    if build_manifest.get("source_fingerprint") != current_fingerprint:
        raise SystemExit("Candidate blocked: canary does not match current source fingerprint")
    if Path(build_manifest.get("validation_baseline", "")).resolve() != base:
        raise SystemExit("Candidate blocked: canary was not validated against the selected production baseline")
    semantic_report = json.loads(args.semantic_report.read_text(encoding="utf-8"))
    if semantic_report.get("status") != "passed":
        raise SystemExit("Candidate blocked: semantic recovery report is not passing")
    sitemap_manifest = json.loads((sitemap_candidate / "release-manifest.json").read_text(encoding="utf-8"))
    if sitemap_manifest.get("production_tree") != PRODUCTION_TREE or sitemap_manifest.get("url_count_delta") != -10:
        raise SystemExit("Candidate blocked: sitemap patch is not the audited technical-exclusion cohort")

    output.mkdir(parents=True)
    changes = []
    for route in PAGE_ROUTES:
        source = output_file_for_route(site, route)
        before = output_file_for_route(base, route)
        relative = before.relative_to(base)
        changes.append(copy_change(source, before, output, relative, "reviewed-page-replacement"))
    for sitemap_change in sitemap_manifest["changed_files"]:
        relative = Path(sitemap_change["path"])
        changes.append(copy_change(sitemap_candidate / relative, base / relative, output, relative, "technical-sitemap-exclusion"))

    manifest = {
        "status": "review-candidate-not-deployed",
        "production_commit": PRODUCTION_COMMIT,
        "production_tree": PRODUCTION_TREE,
        "source_fingerprint": current_fingerprint,
        "page_routes": list(PAGE_ROUTES),
        "page_count_before": 35219,
        "page_count_after": 35219,
        "page_count_delta": 0,
        "sitemap_url_count_before": 35218,
        "sitemap_url_count_after": 35208,
        "sitemap_url_count_delta": -10,
        "changed_file_count": len(changes),
        "changes": changes,
        "rollback": "Revert the single bounded deployment commit; no redirect, deletion, or generated-corpus replacement is included.",
    }
    (output / "release-manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()
