"""Overlay the passing Phase 0 canary onto the existing full output, with rollback files."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import shutil


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_FULL = ROOT / "output"
CANARY = ROOT / "artifacts" / "phase-0-canary-site"
BACKUP = ROOT / "artifacts" / "full-site-pre-phase0-overlay"
MANIFEST = ROOT / "artifacts" / "full-site-phase0-overlay-manifest.json"
ROUTES_FILE = ROOT / "data" / "canary" / "routes.json"
REPORT = ROOT / "reports" / "phase-0" / "canary-test-report.json"


def route_file(root: Path, route: str) -> Path:
    return root / "index.html" if route == "/" else root / route.strip("/") / "index.html"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--target",
        type=Path,
        default=DEFAULT_FULL,
        help="Full static-site directory to receive the canary overlay.",
    )
    args = parser.parse_args()
    full = args.target.resolve()

    report = json.loads(REPORT.read_text(encoding="utf-8"))
    if report.get("status") != "passed":
        raise SystemExit("Overlay blocked: deterministic canary report is not passing.")
    for required in ("index.html", "CNAME", ".nojekyll", "sitemap.xml", "robots.txt"):
        if not (full / required).is_file():
            raise SystemExit(f"Overlay blocked: {full / required} is missing.")

    routes = json.loads(ROUTES_FILE.read_text(encoding="utf-8"))["publish_routes"]
    changes: list[dict[str, object]] = []
    for route in routes:
        source = route_file(CANARY, route)
        destination = route_file(full, route)
        if not source.is_file():
            raise SystemExit(f"Overlay blocked: canary route is missing: {route}")
        existed = destination.is_file()
        if existed:
            relative = destination.relative_to(full)
            backup = BACKUP / relative
            backup.parent.mkdir(parents=True, exist_ok=True)
            if not backup.exists():
                shutil.copy2(destination, backup)
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)
        changes.append(
            {
                "route": route,
                "existed_before": existed,
                "deployed_sha256": digest(destination),
            }
        )

    legacy_url = "https://ukplanningguide.co.uk/councils/colchester/"
    sitemap_removals: list[str] = []
    for council_sitemap in (full / "sitemaps").glob("*.xml"):
        sitemap_text = council_sitemap.read_text(encoding="utf-8")
        if legacy_url not in sitemap_text:
            continue
        relative = council_sitemap.relative_to(full)
        sitemap_backup = BACKUP / relative
        sitemap_backup.parent.mkdir(parents=True, exist_ok=True)
        if not sitemap_backup.exists():
            shutil.copy2(council_sitemap, sitemap_backup)
        pattern = rf"<url><loc>{re.escape(legacy_url)}</loc>.*?</url>"
        sitemap_text, removed = re.subn(pattern, "", sitemap_text)
        if removed < 1:
            raise SystemExit("Overlay blocked: could not remove the legacy bridge from its sitemap.")
        council_sitemap.write_text(sitemap_text, encoding="utf-8")
        sitemap_removals.append(relative.as_posix())

    route_count = sum(path.name == "index.html" for path in full.rglob("index.html"))
    manifest = {
        "artifact": str(full),
        "status": "deployment-candidate",
        "route_count": route_count,
        "overlaid_routes": changes,
        "backup_directory": str(BACKUP),
        "sitemap_removals": sitemap_removals,
        "full_build_regenerated": False,
        "canary_report_sha256": hashlib.sha256(REPORT.read_bytes()).hexdigest(),
    }
    MANIFEST.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(f"Full deployment candidate: {full}")
    print(f"Routes: {route_count:,}")
    print(f"Overlaid: {len(changes)}")
    print(f"Manifest: {MANIFEST}")


if __name__ == "__main__":
    main()
