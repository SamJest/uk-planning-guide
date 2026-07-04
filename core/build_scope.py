from __future__ import annotations

import os
from pathlib import Path

from core.paths import OUTPUT_FOLDER
from utils.content_contracts import normalize_path
from utils.url_registry import load_canary_routes


def build_mode() -> str:
    return str(os.environ.get("UKPG_BUILD_MODE") or "full").strip().lower()


def route_for_output_path(path: Path) -> str:
    try:
        relative = path.resolve().relative_to(OUTPUT_FOLDER.resolve())
    except ValueError:
        return ""
    parts = list(relative.parts)
    if parts and parts[-1] == "index.html":
        parts.pop()
    elif parts:
        return ""
    return normalize_path("/" + "/".join(parts))


def should_render_route(route: str) -> bool:
    if build_mode() != "canary":
        return True
    return normalize_path(route) in set(load_canary_routes()["render_routes"])


def should_publish_route(route: str) -> bool:
    if build_mode() != "canary":
        return True
    return normalize_path(route) in set(load_canary_routes()["publish_routes"])

