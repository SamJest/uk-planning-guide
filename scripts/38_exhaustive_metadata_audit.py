"""Run the strict role and metadata audits across every rendered HTML page.

The normal validator deliberately samples very large generated families.  This
release-gate command loads the complete corpus concurrently, then delegates to
the same validation functions while serving page reads from memory.
"""

from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import validate


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output-dir",
        type=Path,
        required=True,
        help="Rendered site directory to audit.",
    )
    parser.add_argument("--workers", type=int, default=24)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    output_dir = args.output_dir.resolve()
    validate.OUTPUT_DIR = output_dir
    pages = sorted(
        page
        for page in output_dir.rglob("*.html")
        if page != output_dir / "404.html"
    )
    print(f"ALL_PAGE_AUDIT={len(pages)}", flush=True)

    original_read_text = Path.read_text

    def read_page(page: Path) -> tuple[Path, str]:
        return page, original_read_text(page, encoding="utf-8", errors="ignore")

    with ThreadPoolExecutor(max_workers=max(1, args.workers)) as pool:
        page_cache = dict(pool.map(read_page, pages))
    print(f"ALL_PAGE_CACHE_READY={len(page_cache)}", flush=True)

    def cached_read_text(path: Path, *call_args, **call_kwargs) -> str:
        cached = page_cache.get(path)
        if cached is not None:
            return cached
        return original_read_text(path, *call_args, **call_kwargs)

    Path.read_text = cached_read_text
    try:
        validate.validate_role_metadata(pages)
        validate.validate_metadata_quality(pages)
    finally:
        Path.read_text = original_read_text

    print("ALL_PAGE_AUDIT_PASSED", flush=True)


if __name__ == "__main__":
    main()
