"""Create a host-neutral Phase 0 canary deployment archive."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile


ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "artifacts" / "phase-0-canary-site"
ARCHIVE = ROOT / "artifacts" / "ukpg-phase-0-canary-deploy.zip"
ROUTES = ROOT / "data" / "canary" / "routes.json"
REPORT = ROOT / "reports" / "phase-0" / "canary-test-report.json"


def route_file(route: str) -> Path:
    return SITE / "index.html" if route == "/" else SITE / route.strip("/") / "index.html"


def main() -> None:
    report = json.loads(REPORT.read_text(encoding="utf-8"))
    if report.get("status") != "passed":
        raise SystemExit("Canary package blocked: deterministic report is not passing.")

    routes = json.loads(ROUTES.read_text(encoding="utf-8"))["publish_routes"]
    missing = [route for route in routes if not route_file(route).is_file()]
    if missing:
        raise SystemExit(f"Canary package blocked: missing routes: {', '.join(missing)}")

    report_hash = hashlib.sha256(REPORT.read_bytes()).hexdigest()
    manifest = {
        "artifact": "UKPG Phase 0 canary",
        "route_count": len(routes),
        "routes": routes,
        "canary_report_sha256": report_hash,
        "production_deployment": False,
        "notes": "Preview/review artifact. A full-site deployment remains sign-off gated.",
    }

    ARCHIVE.parent.mkdir(parents=True, exist_ok=True)
    with ZipFile(ARCHIVE, "w", compression=ZIP_DEFLATED, compresslevel=9) as archive:
        for source in sorted(SITE.rglob("*")):
            if source.is_file() and source.name != "CNAME":
                archive.write(source, source.relative_to(SITE).as_posix())
        archive.writestr(
            "_redirects",
            "/councils/colchester/ /england/councils/colchester/ 301\n",
        )
        archive.writestr(
            "DEPLOYMENT-MANIFEST.json",
            json.dumps(manifest, indent=2) + "\n",
        )

    archive_hash = hashlib.sha256(ARCHIVE.read_bytes()).hexdigest()
    print(f"Created: {ARCHIVE}")
    print(f"Routes: {len(routes)}")
    print(f"SHA-256: {archive_hash}")


if __name__ == "__main__":
    main()
