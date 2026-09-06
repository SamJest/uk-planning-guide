from __future__ import annotations

import argparse
from hashlib import sha256
import json
from pathlib import Path
import re
import shutil
import subprocess
import xml.etree.ElementTree as ET


EXPECTED_PRODUCTION_COMMIT = "7749cbba33bc06075424a82ec7f733822acfbc57"
EXPECTED_PRODUCTION_TREE = "bd141850da7f1fceeb208c4e52b5b22296547d01"


def digest(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def git_value(worktree: Path, expression: str) -> str:
    return subprocess.check_output(
        ["git", "rev-parse", expression], cwd=worktree, text=True
    ).strip()


def sitemap_count(site: Path) -> int:
    namespace = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    total = 0
    for path in sorted((site / "sitemaps").glob("sitemap-full-corpus-*.xml")):
        root = ET.parse(path).getroot()
        total += len(root.findall("sm:url/sm:loc", namespace))
    return total


def main() -> None:
    parser = argparse.ArgumentParser(description="Package the bounded custom 404 release candidate.")
    parser.add_argument("--build", type=Path, required=True)
    parser.add_argument("--production", type=Path, required=True)
    parser.add_argument("--destination", type=Path, required=True)
    args = parser.parse_args()

    production_commit = git_value(args.production, "HEAD")
    production_tree = git_value(args.production, "HEAD^{tree}")
    if production_commit not in {EXPECTED_PRODUCTION_COMMIT, "f7a308662faa81ddc3cb2253f142ba6765e087d9"}:
        raise SystemExit(f"Unexpected production worktree commit: {production_commit}")
    if production_tree != EXPECTED_PRODUCTION_TREE:
        raise SystemExit(f"Unexpected production tree: {production_tree}")

    source = args.build / "404.html"
    if not source.exists():
        raise SystemExit("Build does not contain 404.html")
    if (args.production / "404.html").exists():
        raise SystemExit("Production already contains 404.html; this add-only candidate is stale")
    html = source.read_text(encoding="utf-8")
    checks = {
        "marker": 'data-not-found-page="true"' in html,
        "noindex": bool(re.search(r'<meta\s+name="robots"\s+content="[^"]*noindex', html, re.I)),
        "no_canonical": not bool(re.search(r'<link\s+rel="canonical"', html, re.I)),
        "no_meta_refresh": "http-equiv=\"refresh\"" not in html.lower(),
    }
    if not all(checks.values()):
        raise SystemExit(f"404 release checks failed: {checks}")

    args.destination.mkdir(parents=True, exist_ok=False)
    destination = args.destination / "404.html"
    shutil.copy2(source, destination)
    index_count = sum(1 for _ in args.production.rglob("index.html"))
    submitted = sitemap_count(args.production)
    manifest = {
        "status": "review-candidate-not-deployed",
        "production_commit": EXPECTED_PRODUCTION_COMMIT,
        "production_tree": EXPECTED_PRODUCTION_TREE,
        "changed_file_count": 1,
        "index_page_count_before": index_count,
        "index_page_count_after": index_count,
        "special_html_file_count_delta": 1,
        "sitemap_url_count_before": submitted,
        "sitemap_url_count_after": submitted,
        "redirect_count_delta": 0,
        "change": {
            "path": "404.html",
            "type": "new-custom-error-document",
            "before_sha256": None,
            "after_sha256": digest(destination),
            "checks": checks,
        },
        "rollback": "Revert the single deployment commit to remove 404.html; do not reset or alter any content URL.",
    }
    (args.destination / "release-manifest.json").write_text(
        json.dumps(manifest, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()
