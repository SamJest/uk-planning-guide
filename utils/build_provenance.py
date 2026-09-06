from __future__ import annotations

import hashlib
from pathlib import Path


INPUT_FILES = {
    "build_site.py",
    "validate.py",
    "package.json",
    "package-lock.json",
    "playwright.config.mjs",
    "lighthouserc.cjs",
}
INPUT_DIRS = (
    "assets",
    "components",
    "core",
    "data",
    "generators",
    "rules",
    "schemas",
    "scripts",
    "templates",
    "tests",
    "utils",
)
IGNORED_PARTS = {"__pycache__", "node_modules", ".git"}


def source_fingerprint(root: Path) -> str:
    """Hash build inputs by relative path and bytes, excluding generated state."""
    root = Path(root).resolve()
    paths = [root / name for name in sorted(INPUT_FILES) if (root / name).is_file()]
    for name in INPUT_DIRS:
        folder = root / name
        if not folder.is_dir():
            continue
        paths.extend(
            path
            for path in folder.rglob("*")
            if path.is_file() and not (set(path.relative_to(root).parts) & IGNORED_PARTS)
        )
    digest = hashlib.sha256()
    for path in sorted(set(paths), key=lambda item: item.relative_to(root).as_posix()):
        relative = path.relative_to(root).as_posix().encode("utf-8")
        digest.update(len(relative).to_bytes(4, "big"))
        digest.update(relative)
        content = path.read_bytes()
        digest.update(len(content).to_bytes(8, "big"))
        digest.update(content)
    return digest.hexdigest()
