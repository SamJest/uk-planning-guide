from __future__ import annotations

from hashlib import sha256
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import xml.etree.ElementTree as ET

from core.paths import ROOT
from utils.content_contracts import BASE_URL, load_page_records, normalize_path, page_records_by_route
from utils.content_integrity import lint_rendered_html
from utils.url_registry import load_canary_routes, load_redirects
from utils.build_provenance import source_fingerprint


CANONICAL_PATTERN = re.compile(r'<link\s+rel="canonical"\s+href="([^"]+)"', re.IGNORECASE)
ROBOTS_PATTERN = re.compile(r'<meta\s+name="robots"\s+content="([^"]+)"', re.IGNORECASE)
JSON_LD_PATTERN = re.compile(r'<script\s+type="application/ld\+json">(.*?)</script>', re.IGNORECASE | re.DOTALL)


class _LinkParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.links: list[str] = []

    def handle_starttag(self, tag: str, attrs) -> None:
        if tag != "a":
            return
        href = dict(attrs).get("href")
        if href:
            self.links.append(href)


def output_file_for_route(output_dir: Path, route: str) -> Path:
    clean = normalize_path(route).strip("/")
    return output_dir / clean / "index.html" if clean else output_dir / "index.html"


def _sitemap_urls(output_dir: Path) -> set[str]:
    index_path = output_dir / "sitemap.xml"
    if not index_path.exists():
        return set()
    namespace = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    root = ET.parse(index_path).getroot()
    urls: set[str] = set()
    for sitemap in root.findall("sm:sitemap/sm:loc", namespace):
        filename = (sitemap.text or "").rstrip("/").split("/")[-1]
        child_path = output_dir / "sitemaps" / filename
        if not child_path.exists():
            continue
        child = ET.parse(child_path).getroot()
        urls.update((node.text or "").strip() for node in child.findall("sm:url/sm:loc", namespace))
    return urls


def _route_exists(route: str, output_dir: Path, baseline_dir: Path | None = None) -> bool:
    if output_file_for_route(output_dir, route).exists():
        return True
    return bool(baseline_dir and output_file_for_route(Path(baseline_dir), route).exists())


def validate_phase0_canary(output_dir: Path, *, baseline_dir: Path | None = None) -> dict:
    output_dir = Path(output_dir)
    routes = load_canary_routes()["publish_routes"]
    records = page_records_by_route()
    redirects = {item["source_path"]: item for item in load_redirects()}
    sitemap_urls = _sitemap_urls(output_dir)
    errors: list[dict[str, str]] = []
    warnings: list[dict[str, str]] = []
    pages: list[dict] = []

    def add_error(route: str, code: str, message: str) -> None:
        errors.append({"route": route, "code": code, "message": message})

    def add_warning(route: str, code: str, message: str) -> None:
        warnings.append({"route": route, "code": code, "message": message})

    not_found_path = output_dir / "404.html"
    not_found_result = {"path": str(not_found_path), "checks": {}}
    if not not_found_path.exists():
        add_error("/404.html", "missing-page", "Custom GitHub Pages 404 document is missing.")
    else:
        not_found_html = not_found_path.read_text(encoding="utf-8", errors="ignore")
        not_found_robots = ROBOTS_PATTERN.search(not_found_html)
        robots_value = (not_found_robots.group(1) if not_found_robots else "").lower()
        checks = {
            "marker": 'data-not-found-page="true"' in not_found_html,
            "noindex": "noindex" in robots_value,
            "no_canonical": CANONICAL_PATTERN.search(not_found_html) is None,
            "no_meta_refresh": "http-equiv=\"refresh\"" not in not_found_html.lower(),
        }
        not_found_result["checks"] = checks
        for check, passed in checks.items():
            if not passed:
                add_error("/404.html", f"invalid-{check.replace('_', '-')}", f"Custom 404 check failed: {check}.")

        parser = _LinkParser()
        parser.feed(not_found_html)
        for href in parser.links:
            if href.startswith(("http://", "https://", "mailto:", "tel:", "#")):
                continue
            target_route = normalize_path(href)
            if not _route_exists(target_route, output_dir, baseline_dir):
                add_error("/404.html", "broken-internal-link", f"Internal target is missing: {target_route}")

    for route in routes:
        record = records[route]
        page_path = output_file_for_route(output_dir, route)
        page_result = {"route": route, "path": str(page_path), "checks": {}}
        pages.append(page_result)
        if not page_path.exists():
            add_error(route, "missing-page", "Canary output is missing.")
            continue
        html = page_path.read_text(encoding="utf-8", errors="ignore")
        expected_canonical = BASE_URL.rstrip("/") + record["canonical_path"]
        canonical_match = CANONICAL_PATTERN.search(html)
        canonical = canonical_match.group(1) if canonical_match else ""
        if canonical != expected_canonical:
            add_error(route, "canonical-mismatch", f"Expected {expected_canonical}, found {canonical or 'none'}.")
        page_result["checks"]["canonical"] = canonical == expected_canonical

        robots_match = ROBOTS_PATTERN.search(html)
        robots = (robots_match.group(1) if robots_match else "").lower()
        is_noindex = "noindex" in robots
        if is_noindex != (record["index_status"] == "noindex"):
            add_error(route, "index-status-mismatch", f"Record={record['index_status']}, rendered robots={robots or 'index'}.")
        absolute = BASE_URL.rstrip("/") + route
        if record["index_status"] == "index" and absolute not in sitemap_urls:
            add_error(route, "missing-from-sitemap", "Indexable canary route is absent from sitemaps.")
        if record["index_status"] == "noindex" and absolute in sitemap_urls:
            add_error(route, "noindex-in-sitemap", "Noindex canary route appears in a sitemap.")

        if record["content_updated_at"] not in html:
            add_error(route, "date-mismatch", "Substantive update date is absent from rendered metadata.")
        if record["source_ids"] and 'data-page-source-panel="true"' not in html:
            add_error(route, "missing-source-panel", "Source-linked record rendered without the source panel.")
        for source_id in record["source_ids"]:
            if f'data-source-id="{source_id}"' not in html:
                add_error(route, "missing-source-id", f"Rendered page does not expose source {source_id}.")
        for claim in record["claims"]:
            if f'data-claim-id="{claim["claim_id"]}"' not in html:
                add_error(route, "missing-claim-id", f"Rendered page does not expose claim {claim['claim_id']}.")
        if record["page_family"] in {"authority_profile", "local_project"} and record["index_status"] == "index":
            if html.count('data-local-fact="true"') < 5:
                add_error(route, "insufficient-local-facts", "Indexable local page renders fewer than five local facts.")

        for finding in lint_rendered_html(record, html):
            target = add_error if finding.severity == "error" else add_warning
            target(route, finding.code, finding.message)

        for payload in JSON_LD_PATTERN.findall(html):
            try:
                json.loads(payload)
            except json.JSONDecodeError as exc:
                add_error(route, "invalid-structured-data", str(exc))

        parser = _LinkParser()
        parser.feed(html)
        for href in parser.links:
            if href.startswith(("http://", "https://", "mailto:", "tel:", "#")):
                continue
            target_route = normalize_path(href)
            if not _route_exists(target_route, output_dir, baseline_dir):
                add_error(route, "broken-internal-link", f"Internal target is missing: {target_route}")

        if len(html.encode("utf-8")) > 175 * 1024:
            add_warning(route, "html-budget", f"HTML is {len(html.encode('utf-8'))} bytes; preferred budget is 179200.")
        if html.count("googletagmanager.com/gtag/js") > 1:
            add_error(route, "duplicate-analytics", "GA4 loader appears more than once.")
        if route in redirects and 'data-static-redirect-bridge="true"' not in html:
            add_error(route, "missing-static-bridge", "Redirect route lacks a visible static bridge marker.")

    return {
        "status": "passed" if not errors else "failed",
        "source_fingerprint": source_fingerprint(ROOT),
        "output_dir": str(output_dir),
        "validation_baseline": str(Path(baseline_dir).resolve()) if baseline_dir else None,
        "route_count": len(routes),
        "error_count": len(errors),
        "warning_count": len(warnings),
        "errors": errors,
        "warnings": warnings,
        "pages": pages,
        "special_pages": {"404": not_found_result},
    }


def _write_report(report: dict) -> tuple[Path, str]:
    report_dir = ROOT / "reports" / "phase-0"
    report_dir.mkdir(parents=True, exist_ok=True)
    json_path = report_dir / "canary-test-report.json"
    payload = json.dumps(report, indent=2, sort_keys=True) + "\n"
    json_path.write_text(payload, encoding="utf-8")
    digest = sha256(payload.encode("utf-8")).hexdigest()
    lines = [
        "# Phase 0 Canary Test Report",
        "",
        f"- Status: **{report['status']}**",
        f"- Routes: {report['route_count']}",
        f"- Errors: {report['error_count']}",
        f"- Warnings: {report['warning_count']}",
        f"- JSON SHA-256: `{digest}`",
        "",
    ]
    if report["errors"]:
        lines.extend(["## Errors", ""])
        lines.extend(f"- `{item['route']}` `{item['code']}` — {item['message']}" for item in report["errors"])
        lines.append("")
    if report["warnings"]:
        lines.extend(["## Warnings", ""])
        lines.extend(f"- `{item['route']}` `{item['code']}` — {item['message']}" for item in report["warnings"])
        lines.append("")
    (report_dir / "canary-test-report.md").write_text("\n".join(lines), encoding="utf-8")
    return json_path, digest


def run_phase0_canary_validation(output_dir: Path, *, baseline_dir: Path | None = None) -> dict:
    report = validate_phase0_canary(output_dir, baseline_dir=baseline_dir)
    report_path, digest = _write_report(report)
    print(f"Phase 0 report: {report_path}")
    print(f"Phase 0 report SHA-256: {digest}")
    if report["status"] != "passed":
        raise RuntimeError(f"Phase 0 canary failed with {report['error_count']} errors")
    return report
