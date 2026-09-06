"""Validate a sparse recovery patch as an overlay on the audited production tree."""
from __future__ import annotations

import argparse
import csv
import hashlib
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import subprocess
from urllib.parse import urlsplit
import xml.etree.ElementTree as ET


PRODUCTION_TREE = "9c640ff1b40473f2e025e9368ac008d41b1e5cc5"
CANONICAL = re.compile(r'<link\s+rel=["\']canonical["\']\s+href=["\']([^"\']+)', re.I)
ROBOTS = re.compile(r'<meta\s+name=["\'](?:robots|googlebot)["\']\s+content=["\']([^"\']+)', re.I)


class Links(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.hrefs: set[str] = set()

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag != "a":
            return
        href = dict(attrs).get("href") or ""
        if href.startswith("/") and not href.startswith("//"):
            self.hrefs.add(href)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def route_file(root: Path, url_or_path: str) -> Path:
    route = urlsplit(url_or_path).path.strip("/")
    return root / route / "index.html" if route else root / "index.html"


def urls(path: Path) -> list[str]:
    return [(node.text or "").strip() for node in ET.parse(path).findall(".//{*}loc")]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base", type=Path, required=True)
    parser.add_argument("--patch", type=Path, required=True)
    parser.add_argument("--inventory", type=Path, required=True)
    parser.add_argument("--report", type=Path, required=True)
    args = parser.parse_args()
    base, patch = args.base.resolve(), args.patch.resolve()
    errors: list[dict[str, str]] = []
    tree = subprocess.check_output(["git", "-C", str(base), "rev-parse", "HEAD^{tree}"], text=True).strip()
    if tree != PRODUCTION_TREE:
        errors.append({"code": "production-tree-drift", "detail": tree})
    manifest = json.loads((patch / "release-manifest.json").read_text(encoding="utf-8"))
    for change in manifest["changes"]:
        target = patch / change["path"]
        if not target.is_file() or sha256(target) != change["after_sha256"]:
            errors.append({"code": "patch-hash-mismatch", "path": change["path"]})

    with args.inventory.open(newline="", encoding="utf-8-sig") as handle:
        inventory = {row["url"]: row for row in csv.DictReader(handle)}
    changed_sitemaps = {change["path"] for change in manifest["changes"] if change["type"] == "technical-sitemap-exclusion"}
    child_urls = urls(base / "sitemap.xml")
    sitemap_urls: list[str] = []
    for child_url in child_urls:
        relative = urlsplit(child_url).path.lstrip("/")
        sitemap_urls.extend(urls((patch if relative in changed_sitemaps else base) / relative))
    if len(sitemap_urls) != len(set(sitemap_urls)):
        errors.append({"code": "duplicate-sitemap-url"})
    if len(sitemap_urls) != manifest["sitemap_url_count_after"]:
        errors.append({"code": "sitemap-count", "detail": str(len(sitemap_urls))})

    changed_routes = set(manifest["page_routes"])
    for url in sitemap_urls:
        route = urlsplit(url).path or "/"
        if route in changed_routes:
            page = route_file(patch, route)
            head = page.read_text(encoding="utf-8", errors="ignore").split("</head>", 1)[0]
            canonical = CANONICAL.search(head)
            if not canonical or canonical.group(1) != url or "noindex" in " ".join(ROBOTS.findall(head)).lower():
                errors.append({"code": "changed-sitemap-page-ineligible", "url": url})
        else:
            row = inventory.get(url)
            if not row or row["canonical"] != url or row["noindex"].lower() == "true" or not row["production_file"]:
                errors.append({"code": "baseline-sitemap-page-ineligible", "url": url})

    broken_links: list[dict[str, str]] = []
    checked_links = 0
    for route in sorted(changed_routes):
        page = route_file(patch, route)
        parser_instance = Links()
        parser_instance.feed(page.read_text(encoding="utf-8", errors="ignore"))
        for href in parser_instance.hrefs:
            path = urlsplit(href).path
            if "." in Path(path).name:
                continue
            checked_links += 1
            if not route_file(patch, path).is_file() and not route_file(base, path).is_file():
                broken_links.append({"route": route, "href": href})
    errors.extend({"code": "broken-candidate-link", **item} for item in broken_links)
    report = {
        "status": "passed" if not errors else "failed",
        "production_tree": tree,
        "changed_file_count": len(manifest["changes"]),
        "page_count_before": manifest["page_count_before"],
        "page_count_after": manifest["page_count_after"],
        "sitemap_url_count_before": manifest["sitemap_url_count_before"],
        "sitemap_url_count_after": len(sitemap_urls),
        "sitemap_unique_count": len(set(sitemap_urls)),
        "sitemap_urls_validated": len(sitemap_urls),
        "changed_page_links_checked": checked_links,
        "broken_candidate_links": broken_links,
        "errors": errors[:100],
    }
    args.report.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))
    raise SystemExit(0 if not errors else 1)


if __name__ == "__main__":
    main()
