"""Package the existing full site with the Phase 0 canary routes overlaid."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from zipfile import ZIP_STORED, ZipFile


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "output"
CANARY = ROOT / "artifacts" / "phase-0-canary-site"
ARCHIVE = ROOT / "artifacts" / "ukpg-full-site-phase0-candidate.zip"
CHECKSUM = ARCHIVE.with_suffix(ARCHIVE.suffix + ".sha256")
ROUTES_FILE = ROOT / "data" / "canary" / "routes.json"
REPORT = ROOT / "reports" / "phase-0" / "canary-test-report.json"


def route_relative_file(route: str) -> Path:
    return Path("index.html") if route == "/" else Path(route.strip("/")) / "index.html"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(8 * 1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def main() -> None:
    required = ["index.html", "CNAME", ".nojekyll", "sitemap.xml", "robots.txt"]
    missing_required = [name for name in required if not (BASE / name).is_file()]
    if missing_required:
        raise SystemExit(f"Full-site package blocked: output/ lacks {', '.join(missing_required)}")

    report = json.loads(REPORT.read_text(encoding="utf-8"))
    if report.get("status") != "passed":
        raise SystemExit("Full-site package blocked: deterministic canary report is not passing.")

    publish_routes = json.loads(ROUTES_FILE.read_text(encoding="utf-8"))["publish_routes"]
    overlay: dict[str, Path] = {}
    for route in publish_routes:
        relative = route_relative_file(route)
        source = CANARY / relative
        if not source.is_file():
            raise SystemExit(f"Full-site package blocked: missing canary route {route}")
        overlay[relative.as_posix()] = source

    canary_assets = CANARY / "assets"
    if canary_assets.is_dir():
        for source in canary_assets.rglob("*"):
            if source.is_file():
                relative = Path("assets") / source.relative_to(canary_assets)
                overlay[relative.as_posix()] = source

    base_files = sorted(path for path in BASE.rglob("*") if path.is_file())
    base_routes = sum(path.name == "index.html" for path in base_files)
    base_names = {path.relative_to(BASE).as_posix() for path in base_files}
    final_routes = base_routes + sum(name not in base_names for name in overlay if name.endswith("/index.html"))

    manifest = {
        "artifact": "UKPG full-site Phase 0 deployment candidate",
        "base_route_count": base_routes,
        "final_route_count": final_routes,
        "base_file_count": len(base_files),
        "overlaid_canary_routes": publish_routes,
        "canary_report_sha256": sha256(REPORT),
        "full_build_regenerated": False,
        "notes": "Existing full corpus with only the passing 20-route canary overlaid.",
    }

    ARCHIVE.parent.mkdir(parents=True, exist_ok=True)
    written: set[str] = set()
    # Storing is deliberate: compressing 35,000 separate HTML files can exceed
    # constrained build-runner timeouts, while the deployable bytes are unchanged.
    with ZipFile(ARCHIVE, "w", compression=ZIP_STORED, allowZip64=True) as archive:
        for index, base_source in enumerate(base_files, start=1):
            name = base_source.relative_to(BASE).as_posix()
            source = overlay.get(name, base_source)
            archive.write(source, name)
            written.add(name)
            if index % 5000 == 0:
                print(f"Packed {index:,}/{len(base_files):,} base files...")

        for name, source in sorted(overlay.items()):
            if name not in written:
                archive.write(source, name)

        archive.writestr(
            "_redirects",
            "/councils/colchester/ /england/councils/colchester/ 301\n",
        )
        archive.writestr("DEPLOYMENT-MANIFEST.json", json.dumps(manifest, indent=2) + "\n")

    archive_hash = sha256(ARCHIVE)
    CHECKSUM.write_text(f"{archive_hash}  {ARCHIVE.name}\n", encoding="ascii")
    print(f"Created: {ARCHIVE}")
    print(f"Routes: {final_routes:,} ({base_routes:,} existing + {final_routes - base_routes} new)")
    print(f"SHA-256: {archive_hash}")


if __name__ == "__main__":
    main()
