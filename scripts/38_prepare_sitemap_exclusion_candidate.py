"""Prepare (never deploy) a hash-bound sitemap-only recovery candidate."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import subprocess
from pathlib import Path
from urllib.parse import urlsplit
import xml.etree.ElementTree as ET


PRODUCTION_COMMIT = "aa7d89ec029c70d5973b7d982fcbe5036316d9b2"
PRODUCTION_TREE = "9c640ff1b40473f2e025e9368ac008d41b1e5cc5"
EXCLUSIONS = {
    "https://ukplanningguide.co.uk/councils/colchester/": "noindex and canonical to the country-first URL",
    "https://ukplanningguide.co.uk/england/rules/article-4/colchester/": "noindex",
    "https://ukplanningguide.co.uk/england/services/premium-council-pack/": "noindex",
    "https://ukplanningguide.co.uk/england/services/professional-referral/": "noindex",
    "https://ukplanningguide.co.uk/england/services/reviewed-route-report/": "noindex",
    "https://ukplanningguide.co.uk/local-search/": "noindex",
    "https://ukplanningguide.co.uk/personalised-planning-guidance/request/": "noindex form",
    "https://ukplanningguide.co.uk/personalised-planning-guidance/request/success/": "noindex success page",
    "https://ukplanningguide.co.uk/planning-help/thank-you/": "noindex success page",
    "https://ukplanningguide.co.uk/updates/phase-0-integrity-repair/": "noindex operational page",
}
CANONICAL = re.compile(r'<link\s+rel=["\']canonical["\']\s+href=["\']([^"\']+)', re.I)
ROBOTS = re.compile(r'<meta\s+name=["\'](?:robots|googlebot)["\']\s+content=["\']([^"\']+)', re.I)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def sitemap_urls(path: Path) -> list[str]:
    return [(node.text or "").strip() for node in ET.parse(path).findall(".//{*}loc")]


def remove_exact_url_lines(text: str, urls: set[str]) -> tuple[str, set[str]]:
    removed: set[str] = set()
    output = []
    for line in text.splitlines(keepends=True):
        matched = next((url for url in urls if f"<loc>{url}</loc>" in line), None)
        if matched:
            if matched in removed:
                raise ValueError(f"Duplicate sitemap entry for {matched}")
            removed.add(matched)
            continue
        output.append(line)
    return "".join(output), removed


def assert_exclusion_is_technical(base: Path, url: str) -> None:
    route = urlsplit(url).path.strip("/")
    page = base / route / "index.html" if route else base / "index.html"
    if not page.is_file():
        raise SystemExit(f"Candidate blocked: production file is missing for {url}")
    head = page.read_text(encoding="utf-8", errors="ignore").split("</head>", 1)[0]
    robots = " ".join(ROBOTS.findall(head)).lower()
    canonical = (CANONICAL.search(head).group(1) if CANONICAL.search(head) else "")
    if "noindex" not in robots and canonical == url:
        raise SystemExit(f"Candidate blocked: {url} is not currently noindex/noncanonical")


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)
    base, output = args.base.resolve(), args.output.resolve()
    if output.exists():
        raise SystemExit(f"Candidate blocked: output already exists and will not be overwritten: {output}")
    tree = subprocess.check_output(
        ["git", "-C", str(base), "rev-parse", "HEAD^{tree}"], text=True, encoding="utf-8"
    ).strip()
    if tree != PRODUCTION_TREE:
        raise SystemExit(f"Candidate blocked: base tree {tree} is not verified production tree {PRODUCTION_TREE}")
    for url in EXCLUSIONS:
        assert_exclusion_is_technical(base, url)

    index = base / "sitemap.xml"
    child_urls = sitemap_urls(index)
    child_files = [base / urlsplit(url).path.lstrip("/") for url in child_urls]
    before_urls = [url for path in child_files for url in sitemap_urls(path)]
    if len(before_urls) != len(set(before_urls)):
        raise SystemExit("Candidate blocked: duplicate URLs already exist across submitted sitemaps")
    if not set(EXCLUSIONS).issubset(before_urls):
        missing = sorted(set(EXCLUSIONS) - set(before_urls))
        raise SystemExit(f"Candidate blocked: expected submitted exclusions missing: {missing}")

    output.mkdir(parents=True)
    shutil.copy2(index, output / "sitemap.xml")
    changes = []
    removed_all: set[str] = set()
    for source in child_files:
        relative = source.relative_to(base)
        target = output / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        text = source.read_text(encoding="utf-8")
        filtered, removed = remove_exact_url_lines(text, set(EXCLUSIONS))
        target.write_text(filtered, encoding="utf-8", newline="")
        removed_all.update(removed)
        if removed:
            changes.append({"path": relative.as_posix(), "before_sha256": sha256(source), "after_sha256": sha256(target), "removed_urls": sorted(removed)})
    if removed_all != set(EXCLUSIONS):
        raise SystemExit(f"Candidate blocked: exact removal mismatch: {sorted(set(EXCLUSIONS) - removed_all)}")
    after_files = [output / path.relative_to(base) for path in child_files]
    after_urls = [url for path in after_files for url in sitemap_urls(path)]
    if set(EXCLUSIONS) & set(after_urls) or len(after_urls) != len(before_urls) - len(EXCLUSIONS):
        raise SystemExit("Candidate blocked: post-filter sitemap count/membership mismatch")
    manifest = {
        "status": "review-candidate-not-deployed",
        "production_commit": PRODUCTION_COMMIT,
        "production_tree": PRODUCTION_TREE,
        "before_url_count": len(before_urls),
        "after_url_count": len(after_urls),
        "url_count_delta": -len(EXCLUSIONS),
        "changed_files": changes,
        "excluded_urls": [{"url": url, "reason": reason} for url, reason in sorted(EXCLUSIONS.items())],
        "unchanged_page_count": 35219,
        "rollback": "Restore the four before_sha256 XML blobs through a normal revert commit.",
    }
    (output / "release-manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()
