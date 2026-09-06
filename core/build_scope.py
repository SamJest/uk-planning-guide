from __future__ import annotations

import os
from pathlib import Path

from core.paths import OUTPUT_FOLDER
from utils.content_contracts import normalize_path
from utils.url_registry import load_canary_routes


VALID_BUILD_MODES = {"canary", "full"}


class BuildScopeError(RuntimeError):
    """Raised when a generator is invoked without an explicit safe scope."""


def build_mode() -> str:
    mode = str(os.environ.get("UKPG_BUILD_MODE") or "").strip().lower()
    if mode not in VALID_BUILD_MODES:
        shown = mode or "unset"
        raise BuildScopeError(
            f"Publication scope is {shown!r}; run build_site.py (canary by default) "
            "instead of invoking a generator directly."
        )
    return mode


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
    if build_mode() == "full":
        return True
    return normalize_path(route) in set(load_canary_routes()["render_routes"])


def should_publish_route(route: str) -> bool:
    if build_mode() == "full":
        return True
    return normalize_path(route) in set(load_canary_routes()["publish_routes"])
