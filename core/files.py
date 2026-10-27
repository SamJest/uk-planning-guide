import os
import shutil
from pathlib import Path

from core.build_scope import BuildScopeError, route_for_output_path, should_render_route


def ensure_dir(path):
    os.makedirs(path, exist_ok=True)


def write_file(folder, filename, content):
    path = Path(folder) / filename
    route = route_for_output_path(path)
    if filename == "index.html" and not route:
        raise BuildScopeError(f"Refusing to write a page outside the configured build output: {path}")
    if route and not should_render_route(route):
        return False

    os.makedirs(folder, exist_ok=True)

    with open(path, "w", encoding="utf-8") as handle:
        handle.write(content)
    return True


def copy_assets(src="assets", dest="output/assets"):
    if not os.path.exists(src):
        print("No assets folder found, skipping asset copy.")
        return

    if os.path.exists(dest):
        shutil.rmtree(dest)

    shutil.copytree(src, dest)
    print(f"Assets copied to {dest}")
