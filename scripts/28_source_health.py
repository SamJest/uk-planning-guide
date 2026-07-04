from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import ssl
import sys
import urllib.error
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from core.paths import ROOT
from utils.source_registry import load_source_registry


REPORT_PATH = ROOT / "reports" / "phase-0" / "source-health.json"


def _check(source: dict, timeout: int) -> dict:
    request = urllib.request.Request(
        source["url"],
        headers={"User-Agent": "UKPlanningGuide-SourceHealth/1.0 (+https://ukplanningguide.co.uk/methodology/)"},
        method="HEAD",
    )
    context = ssl.create_default_context()
    try:
        try:
            response = urllib.request.urlopen(request, timeout=timeout, context=context)
        except urllib.error.HTTPError as exc:
            if exc.code not in {403, 405, 429}:
                raise
            request = urllib.request.Request(source["url"], headers=dict(request.header_items()), method="GET")
            response = urllib.request.urlopen(request, timeout=timeout, context=context)
        with response:
            status = int(response.status)
            final_url = response.geturl()
        health = "redirected" if final_url.rstrip("/") != source["url"].rstrip("/") else "active"
        return {
            "source_id": source["source_id"],
            "requested_url": source["url"],
            "final_url": final_url,
            "http_status": status,
            "health": health,
            "error": "",
        }
    except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, OSError) as exc:
        return {
            "source_id": source["source_id"],
            "requested_url": source["url"],
            "final_url": "",
            "http_status": getattr(exc, "code", 0) or 0,
            "health": "unavailable",
            "error": str(exc),
        }


def run_source_health(*, timeout: int = 20, strict: bool = False) -> dict:
    results = [_check(source, timeout) for source in load_source_registry()]
    active_ids = {source["source_id"] for source in load_source_registry() if source["status"] == "active"}
    blocking = [result for result in results if result["source_id"] in active_ids and result["health"] == "unavailable"]
    report = {
        "checked_at": datetime.now(timezone.utc).isoformat(),
        "source_count": len(results),
        "active": sum(result["health"] == "active" for result in results),
        "redirected": sum(result["health"] == "redirected" for result in results),
        "unavailable": sum(result["health"] == "unavailable" for result in results),
        "blocking_count": len(blocking),
        "results": results,
    }
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({key: report[key] for key in ("source_count", "active", "redirected", "unavailable", "blocking_count")}, indent=2))
    if strict and blocking:
        raise SystemExit(1)
    return report


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Check Phase 0 source URLs without mutating the registry.")
    parser.add_argument("--timeout", type=int, default=20)
    parser.add_argument("--strict", action="store_true")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    run_source_health(timeout=args.timeout, strict=args.strict)
