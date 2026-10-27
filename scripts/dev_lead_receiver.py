"""Local-only Planning Route Check lead receiver.

This script is for development testing only. It is not production storage,
does not authenticate requests, and must not contain private secrets.
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import re


DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 8787
DEFAULT_OUTPUT_DIR = ".lead_test_submissions"
MAX_BODY_BYTES = 128 * 1024


def _safe_slug(value: str) -> str:
    clean = re.sub(r"[^a-zA-Z0-9_-]+", "-", value.strip())
    return clean.strip("-")[:80] or "lead"


def _summary(payload: dict) -> str:
    return "\n".join(
        [
            "NEW UK PLANNING GUIDE TEST LEAD",
            f"Project: {payload.get('project_type', '')}",
            f"Location: {payload.get('postcode_or_town', '')}",
            f"Council: {payload.get('council', '')}",
            f"Likely route: {payload.get('route_result', '')}",
            f"Confidence: {payload.get('confidence', '')}",
            f"Name: {payload.get('name', '')}",
            f"Email: {payload.get('email', '')}",
            f"Consent contact: {payload.get('consent_contact', '')}",
            f"Consent share: {payload.get('consent_share', '')}",
        ]
    )


class LeadReceiver(BaseHTTPRequestHandler):
    output_dir: Path

    def _cors(self) -> None:
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")

    def do_OPTIONS(self) -> None:
        self.send_response(204)
        self._cors()
        self.end_headers()

    def do_POST(self) -> None:
        if self.path.rstrip("/") != "/leads":
            self.send_response(404)
            self._cors()
            self.end_headers()
            self.wfile.write(b'{"ok": false, "error": "Use /leads"}')
            return

        try:
            content_length = int(self.headers.get("Content-Length", "0"))
        except ValueError:
            content_length = 0

        if content_length <= 0 or content_length > MAX_BODY_BYTES:
            self.send_response(413)
            self._cors()
            self.end_headers()
            self.wfile.write(b'{"ok": false, "error": "Invalid body size"}')
            return

        raw = self.rfile.read(content_length)
        try:
            payload = json.loads(raw.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError):
            self.send_response(400)
            self._cors()
            self.end_headers()
            self.wfile.write(b'{"ok": false, "error": "Expected JSON"}')
            return

        if not isinstance(payload, dict):
            self.send_response(400)
            self._cors()
            self.end_headers()
            self.wfile.write(b'{"ok": false, "error": "Expected JSON object"}')
            return

        payload.setdefault("status", "New")
        received_at = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        project = _safe_slug(str(payload.get("project_type", "lead")))
        location = _safe_slug(str(payload.get("postcode_or_town", "unknown")))
        filename = f"{received_at}-{project}-{location}.json"
        self.output_dir.mkdir(parents=True, exist_ok=True)
        output_path = self.output_dir / filename
        output_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")

        print()
        print(_summary(payload))
        print(f"Saved: {output_path}")

        self.send_response(200)
        self._cors()
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.end_headers()
        self.wfile.write(json.dumps({"ok": True, "file": filename}).encode("utf-8"))

    def log_message(self, format: str, *args) -> None:
        print(f"{self.address_string()} - {format % args}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Local-only lead receiver for Planning Route Check testing.")
    parser.add_argument("--host", default=DEFAULT_HOST)
    parser.add_argument("--port", type=int, default=DEFAULT_PORT)
    parser.add_argument("--output-dir", default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()

    handler = type("ConfiguredLeadReceiver", (LeadReceiver,), {"output_dir": Path(args.output_dir)})
    server = ThreadingHTTPServer((args.host, args.port), handler)

    print("Local test receiver only. Do not use this as production storage.")
    print(f"Listening on http://{args.host}:{args.port}/leads")
    print(f"Saving JSON submissions to {Path(args.output_dir).resolve()}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping lead receiver")
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
