import argparse
import shutil
import subprocess
import sys
import time
import os
import json
import hashlib
from pathlib import Path

from core.files import copy_assets
from utils.build_provenance import source_fingerprint


SCRIPT_DIR = Path(__file__).resolve().parent
LIVE_OUTPUT_DIR = SCRIPT_DIR / "output"
CANARY_OUTPUT_DIR = SCRIPT_DIR / "artifacts" / "phase-0-canary-site"
SIGNOFF_PATH = SCRIPT_DIR / "docs" / "phase-0-signoff.json"
OUTPUT_DIR = CANARY_OUTPUT_DIR
BUILD_STATE_PATH = SCRIPT_DIR / "artifacts" / "build-progress-canary.json"

BASE_SCRIPTS = [
    "1_generate_site_core.py",
    "2_generate_homepage_and_indexes.py",
    "3_generate_scenario_pages.py",
    "3b_generate_project_scenario_pages.py",
    "4_generate_council_pages.py",
    "5_generate_county_pages.py",
    "6_generate_county_project_pages.py",
    "7_generate_scenario_hubs.py",
    "10_generate_local_search_pages.py",
    "18_generate_gsc_recovery_pages.py",
    "12_generate_planning_tools.py",
    "19_generate_building_regulations_pages.py",
    "8_generate_nearby_links.py",
    "11_generate_faq_pages.py",
    "20_generate_upgrade_pages.py",
    "21_generate_download_assets.py",
    "23_generate_growth_indexation_manifest.py",
    "9_generate_sitemaps.py",
]

CANARY_SCRIPTS = [
    "1_generate_site_core.py",
    "2_generate_homepage_and_indexes.py",
    "3_generate_scenario_pages.py",
    "4_generate_council_pages.py",
    "7_generate_scenario_hubs.py",
    "12_generate_planning_tools.py",
    "11_generate_faq_pages.py",
    "20_generate_upgrade_pages.py",
    "21_generate_download_assets.py",
    "23_generate_growth_indexation_manifest.py",
    "9_generate_sitemaps.py",
]

def get_scripts(mode: str = "full") -> list[str]:
    return list(CANARY_SCRIPTS if mode == "canary" else BASE_SCRIPTS)


def _load_build_state() -> dict:
    if not BUILD_STATE_PATH.exists():
        return {}
    try:
        return json.loads(BUILD_STATE_PATH.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}


def _save_build_state(state: dict) -> None:
    BUILD_STATE_PATH.parent.mkdir(parents=True, exist_ok=True)
    BUILD_STATE_PATH.write_text(json.dumps(state, indent=2), encoding="utf-8")


def _clear_build_state() -> None:
    if BUILD_STATE_PATH.exists():
        BUILD_STATE_PATH.unlink()


def _normalized_completed_scripts(state: dict, scripts: list[str], fingerprint: str) -> list[str]:
    if state.get("source_fingerprint") != fingerprint:
        return []
    completed = state.get("completed_scripts", [])
    if not isinstance(completed, list):
        return []
    allowed = set(scripts)
    return [script for script in completed if script in allowed]


def clean_output() -> None:
    if not OUTPUT_DIR.exists():
        return

    print("\nCleaning output folder...\n")

    for item in OUTPUT_DIR.iterdir():
        if item.name == ".git":
            continue

        try:
            if item.is_dir():
                shutil.rmtree(item)
            else:
                item.unlink()
        except OSError as exc:
            print(f"Warning: could not delete {item}: {exc}")


def run_script(script_name: str) -> bool:
    script_path = SCRIPT_DIR / "scripts" / script_name

    if not script_path.exists():
        print(f"Warning: skipping missing script {script_name}")
        return False

    print("\n--------------------------------------")
    print(f"Running: {script_name}")
    print("--------------------------------------")

    start = time.time()
    subprocess.run(
        [sys.executable, str(script_path)],
        cwd=str(SCRIPT_DIR),
        check=True,
    )
    duration = round(time.time() - start, 2)

    print(f"Completed: {script_name} ({duration}s)")
    return True


def write_cname() -> None:
    (OUTPUT_DIR / "CNAME").write_text("ukplanningguide.co.uk\n", encoding="utf-8")
    print("Created CNAME file")


def write_nojekyll() -> None:
    (OUTPUT_DIR / ".nojekyll").write_text("", encoding="utf-8")
    print("Created .nojekyll file")


def _configure_build(mode: str, output_override: Path | None = None) -> None:
    global OUTPUT_DIR, BUILD_STATE_PATH
    if output_override is not None:
        resolved = output_override.resolve()
        allowed_root = (SCRIPT_DIR / "artifacts" / "builds").resolve()
        try:
            resolved.relative_to(allowed_root)
        except ValueError as exc:
            raise SystemExit(f"Custom build output must be inside {allowed_root}") from exc
        OUTPUT_DIR = resolved
        BUILD_STATE_PATH = allowed_root / f"{resolved.name}.build-state.json"
    elif mode == "full":
        OUTPUT_DIR = LIVE_OUTPUT_DIR
        BUILD_STATE_PATH = SCRIPT_DIR / "artifacts" / "build-progress.json"
    else:
        OUTPUT_DIR = CANARY_OUTPUT_DIR
        BUILD_STATE_PATH = SCRIPT_DIR / "artifacts" / "build-progress-canary.json"
    os.environ["UKPG_BUILD_MODE"] = mode
    os.environ["UKPG_OUTPUT_DIR"] = str(OUTPUT_DIR)


def _assert_full_build_approved() -> None:
    try:
        signoff = json.loads(SIGNOFF_PATH.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise SystemExit(f"Full build blocked: unreadable {SIGNOFF_PATH.relative_to(SCRIPT_DIR)} ({exc})")
    if signoff.get("approved") is not True or not str(signoff.get("canary_report_sha256") or "").strip():
        raise SystemExit(
            "Full build blocked: Phase 0 sign-off must be approved and include the passing canary report SHA-256."
        )
    report_path = SCRIPT_DIR / "reports" / "phase-0" / "canary-test-report.json"
    try:
        report_bytes = report_path.read_bytes()
        report = json.loads(report_bytes)
    except (OSError, json.JSONDecodeError) as exc:
        raise SystemExit(f"Full build blocked: unreadable passing canary report ({exc})")
    actual_report_hash = hashlib.sha256(report_bytes).hexdigest()
    current_fingerprint = source_fingerprint(SCRIPT_DIR)
    if report.get("status") != "passed":
        raise SystemExit("Full build blocked: canary report is not passing.")
    if signoff.get("canary_report_sha256") != actual_report_hash:
        raise SystemExit("Full build blocked: approved canary report hash does not match the report on disk.")
    if signoff.get("source_fingerprint") != current_fingerprint:
        raise SystemExit("Full build blocked: approval is not bound to the current build inputs.")
    if report.get("source_fingerprint") != current_fingerprint:
        raise SystemExit("Full build blocked: canary report was produced from different build inputs.")


def write_build_manifest(mode: str, fingerprint: str, validation_baseline: Path | None) -> None:
    payload = {
        "mode": mode,
        "source_fingerprint": fingerprint,
        "validation_baseline": str(validation_baseline.resolve()) if validation_baseline else None,
        "production_deployment": False,
    }
    (OUTPUT_DIR / "BUILD-MANIFEST.json").write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def build_site(
    *,
    mode: str = "canary",
    output_override: Path | None = None,
    validation_baseline: Path | None = None,
) -> None:
    _configure_build(mode, output_override)
    if mode == "full":
        _assert_full_build_approved()

    from utils.content_contracts import load_page_records
    from utils.source_registry import load_source_registry, validate_page_source_links
    from utils.url_registry import validate_url_registry

    load_page_records()
    load_source_registry()
    validate_page_source_links()
    validate_url_registry()

    print("\n======================================")
    print(f"{mode.upper()} BUILD STARTED")
    print("======================================")
    print(f"Output: {OUTPUT_DIR}")

    scripts = get_scripts(mode)
    fingerprint = source_fingerprint(SCRIPT_DIR)
    prior_state = _load_build_state()
    completed_scripts = _normalized_completed_scripts(prior_state, scripts, fingerprint)
    resuming = bool(completed_scripts)
    build_started_at = (
        prior_state.get("started_at")
        if resuming
        else time.strftime("%Y-%m-%dT%H:%M:%S")
    )

    start_time = time.time()
    if resuming:
        print("\nResuming previous build from saved progress...\n")
        print(f"Completed scripts already recorded: {len(completed_scripts)}/{len(scripts)}")
        if len(completed_scripts) == len(scripts):
            print("Generator scripts are already complete; rerunning validation from the saved checkpoint.")
    else:
        clean_output()
        _save_build_state(
            {
                "started_at": build_started_at,
                "completed_scripts": [],
                "scripts": scripts,
                "source_fingerprint": fingerprint,
            }
        )

    completed = len(completed_scripts)
    for script in scripts:
        if script in completed_scripts:
            continue
        try:
            if run_script(script):
                completed += 1
                completed_scripts.append(script)
                _save_build_state(
                    {
                        "started_at": build_started_at,
                        "completed_scripts": completed_scripts,
                        "scripts": scripts,
                        "source_fingerprint": fingerprint,
                    }
                )
        except subprocess.CalledProcessError:
            print(f"\nBuild failed while running {script}")
            raise SystemExit(1)

    copy_assets(src=SCRIPT_DIR / "assets", dest=OUTPUT_DIR / "assets")
    if mode == "full":
        write_cname()
    write_nojekyll()
    write_build_manifest(mode, fingerprint, validation_baseline)

    _save_build_state(
        {
            "started_at": build_started_at,
            "completed_scripts": completed_scripts,
            "scripts": scripts,
            "source_fingerprint": fingerprint,
            "validation_mode": "local",
            "validation_status": "running",
            "validation_started_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
        }
    )

    try:
        if mode == "canary":
            from utils.phase0_validation import run_phase0_canary_validation

            print("\nRunning Phase 0 canary validation...\n")
            run_phase0_canary_validation(OUTPUT_DIR, baseline_dir=validation_baseline)
        else:
            from validate import run_validation

            print("\nRunning validation (local mode)...\n")
            run_validation(mode="local")
    except Exception as exc:
        _save_build_state(
            {
                "started_at": build_started_at,
                "completed_scripts": completed_scripts,
                "scripts": scripts,
                "source_fingerprint": fingerprint,
                "validation_mode": "local",
                "validation_status": "failed",
                "validation_started_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
                "validation_error": str(exc),
                "failed_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
            }
        )
        print(f"\nValidation failed: {exc}")
        raise SystemExit(1)

    total_time = round(time.time() - start_time, 2)
    _clear_build_state()

    print("\n======================================")
    print("BUILD COMPLETE")
    print("======================================")
    print(f"\nScripts executed: {completed}/{len(scripts)}")
    print(f"Total build time: {total_time} seconds\n")


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build the UK Planning Guide site.")
    parser.add_argument(
        "--full",
        action="store_true",
        help="Run the full build only after docs/phase-0-signoff.json is approved.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        help="Fresh canary output below artifacts/builds/. Full production output remains fixed and gated.",
    )
    parser.add_argument(
        "--validation-baseline",
        type=Path,
        help="Explicit static-site baseline used to resolve links outside the scoped canary.",
    )
    return parser.parse_args(argv)


if __name__ == "__main__":
    arguments = parse_args()
    build_site(
        mode="full" if arguments.full else "canary",
        output_override=arguments.output_dir,
        validation_baseline=arguments.validation_baseline,
    )
