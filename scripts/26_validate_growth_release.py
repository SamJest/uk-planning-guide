from __future__ import annotations

import csv
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from html import unescape
import json
from pathlib import Path
import re
import sys
import xml.etree.ElementTree as ET
from urllib.parse import urlparse


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from core.paths import OUTPUT_FOLDER
from utils.indexation import INDEXATION_MANIFEST_CSV, normalize_path


TITLE_PATTERN = re.compile(r"<title>(.*?)</title>", re.IGNORECASE | re.DOTALL)
H1_PATTERN = re.compile(r"<h1(?:\s[^>]*)?>(.*?)</h1>", re.IGNORECASE | re.DOTALL)
CANONICAL_PATTERN = re.compile(
    r'<link\s+rel=["\']canonical["\']\s+href=["\']([^"\']+)["\']',
    re.IGNORECASE,
)
ROBOTS_PATTERN = re.compile(
    r'<meta\s+name=["\']robots["\']\s+content=["\']([^"\']+)["\']',
    re.IGNORECASE,
)
SCHEMA_PATTERN = re.compile(
    r'<script\s+type=["\']application/ld\+json["\']>(.*?)</script>',
    re.IGNORECASE | re.DOTALL,
)
TAG_PATTERN = re.compile(r"<[^>]+>")


def _output_file(path: str) -> Path:
    clean = normalize_path(path).strip("/")
    return OUTPUT_FOLDER / clean / "index.html" if clean else OUTPUT_FOLDER / "index.html"


def _read_through_h1(page: Path, limit: int = 524288) -> str:
    chunks = []
    size = 0
    with page.open("r", encoding="utf-8", errors="ignore") as handle:
        while size < limit:
            chunk = handle.read(min(65536, limit - size))
            if not chunk:
                break
            chunks.append(chunk)
            size += len(chunk)
            if "</h1>" in chunk.lower() or "</body>" in chunk.lower():
                break
    return "".join(chunks)


def _text(match: re.Match | None) -> str:
    if not match:
        return ""
    return " ".join(unescape(TAG_PATTERN.sub(" ", match.group(1))).split())


def _sitemap_paths() -> set[str]:
    paths = set()
    for sitemap in (OUTPUT_FOLDER / "sitemaps").glob("*.xml"):
        root = ET.parse(sitemap).getroot()
        for element in root.iter():
            if element.tag.endswith("loc") and element.text:
                paths.add(normalize_path(urlparse(element.text).path))
    return paths


def validate_release() -> dict[str, object]:
    with INDEXATION_MANIFEST_CSV.open("r", encoding="utf-8-sig", newline="") as handle:
        manifest = {normalize_path(row["path"]): row for row in csv.DictReader(handle)}
    generated = {
        normalize_path("/" + "/".join(page.relative_to(OUTPUT_FOLDER).parts[:-1])): page
        for page in OUTPUT_FOLDER.rglob("index.html")
    }
    sitemap_paths = _sitemap_paths()
    failures = []
    schema_blocks = 0
    titles = set()
    h1_count = 0

    missing_manifest = sorted(set(generated) - set(manifest))
    missing_files = sorted(set(manifest) - set(generated))
    if missing_manifest:
        failures.append(f"Generated pages missing from manifest: {missing_manifest[:10]}")
    if missing_files:
        failures.append(f"Manifest routes missing generated files: {missing_files[:10]}")

    def validate_page(item: tuple[str, dict[str, str]]) -> tuple[str, str, int, list[str]]:
        path, row = item
        page_failures = []
        page = generated.get(path) or _output_file(path)
        if not page.exists():
            return "", "", 0, [f"Generated file missing: {path}"]
        html = _read_through_h1(page)
        title = _text(TITLE_PATTERN.search(html))
        h1 = _text(H1_PATTERN.search(html))
        canonical_match = CANONICAL_PATTERN.search(html)
        canonical = normalize_path(canonical_match.group(1)) if canonical_match else ""
        robots_match = ROBOTS_PATTERN.search(html)
        robots = robots_match.group(1).lower() if robots_match else ""
        expected_canonical = normalize_path(row.get("canonical_target") or path)
        state = row.get("index_state", "")

        if not title:
            page_failures.append(f"Missing title: {path}")
        if not h1:
            page_failures.append(f"Missing H1: {path}")
        if canonical != expected_canonical:
            page_failures.append(f"Canonical mismatch: {path} -> {canonical or 'missing'} expected {expected_canonical}")
        if state == "noindex" and "noindex" not in robots:
            page_failures.append(f"Manifest noindex missing robots directive: {path}")
        if state == "index" and "noindex" in robots:
            page_failures.append(f"Manifest index conflicts with robots directive: {path}")
        if state == "index" and path not in sitemap_paths:
            page_failures.append(f"Indexable route missing from sitemap: {path}")
        if state != "index" and path in sitemap_paths:
            page_failures.append(f"Non-indexable route present in sitemap: {path}")

        page_schema_blocks = 0
        for payload in SCHEMA_PATTERN.findall(html):
            page_schema_blocks += 1
            try:
                json.loads(unescape(payload))
            except json.JSONDecodeError as exc:
                page_failures.append(f"Invalid JSON-LD: {path} ({exc})")
        return title.lower(), h1, page_schema_blocks, page_failures

    items = sorted(manifest.items())
    with ThreadPoolExecutor(max_workers=12) as executor:
        results = executor.map(validate_page, items, chunksize=64)
        for index, (title, h1, page_schema_blocks, page_failures) in enumerate(results, start=1):
            if title:
                titles.add(title)
            if h1:
                h1_count += 1
            schema_blocks += page_schema_blocks
            failures.extend(page_failures)
            if index % 5000 == 0:
                print(f"Validated growth release routes: {index}/{len(manifest)}", flush=True)
        if len(failures) >= 100:
            failures[:] = failures[:100]

    result = {
        "validated_at": datetime.now(timezone.utc).isoformat(),
        "generated_routes": len(generated),
        "manifest_routes": len(manifest),
        "sitemap_routes": len(sitemap_paths),
        "index_routes": sum(1 for row in manifest.values() if row.get("index_state") == "index"),
        "noindex_routes": sum(1 for row in manifest.values() if row.get("index_state") == "noindex"),
        "titles_found": len(titles),
        "h1_found": h1_count,
        "json_ld_blocks_parsed": schema_blocks,
        "failures": failures,
        "passed": not failures,
    }
    output = ROOT / "artifacts" / "growth" / "release-validation.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2), encoding="utf-8")
    if failures:
        for failure in failures[:25]:
            print(f"FAIL: {failure}")
        raise SystemExit(f"Growth release validation failed with {len(failures)} issue(s)")
    print(
        f"Growth release validation passed: {len(manifest)} routes, "
        f"{len(sitemap_paths)} sitemap URLs, {schema_blocks} JSON-LD blocks"
    )
    return result


if __name__ == "__main__":
    validate_release()
