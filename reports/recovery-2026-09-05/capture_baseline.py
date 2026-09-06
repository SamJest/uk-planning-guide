"""Read-only site/Git audit; writes only new files in a supplied audit directory."""
import csv
import hashlib
import json
import subprocess
import time
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent / "baseline"
BASE = "https://ukplanningguide.co.uk"
PACK = ROOT / "artifacts/recovery-pack-2026-09-04/UKPG_RECOVERY_PACK_2026-09-04"


class Head(HTMLParser):
    def __init__(self, html):
        super().__init__()
        self.canonicals = []
        self.robots = []
        self.refresh = []
        self.feed(html)

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "link" and "canonical" in a.get("rel", "").lower().split():
            self.canonicals.append(a.get("href", ""))
        if tag == "meta" and a.get("name", "").lower() in {"robots", "googlebot"}:
            self.robots.append(a.get("content", "").lower())
        if tag == "meta" and a.get("http-equiv", "").lower() == "refresh":
            self.refresh.append(a.get("content", ""))


def git(*args):
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True, encoding="utf-8")


def sitemaps(folder):
    index = ET.parse(folder / "sitemap.xml").getroot()
    members = []
    files = {}
    for child in index:
        loc = child.find("{*}loc").text
        path = folder / urlsplit(loc).path.lstrip("/")
        urls = [n.text for n in ET.parse(path).findall(".//{*}loc")]
        files[path.name] = len(urls)
        members.extend(urls)
    return members, files


def main():
    if OUT.exists():
        raise SystemExit("Baseline already exists; preserve it and choose a new dated capture.")
    OUT.mkdir(parents=True)
    started = time.monotonic()
    commands = {
        "status": ["status", "--short", "--untracked-files=all"],
        "branches": ["branch", "-avv"], "stashes": ["stash", "list"],
        "tags": ["tag", "-n"], "worktrees": ["worktree", "list", "--porcelain"],
        "remotes": ["remote", "-v"],
        "timeline": ["log", "--all", "--since=2026-06-20", "--date=iso-strict", "--format=%H|%P|%aI|%cI|%s"],
    }
    for name, command in commands.items():
        (OUT / f"git-{name}.txt").write_text(git(*command), encoding="utf-8")
    pack_files = {str(p.relative_to(PACK)): {"bytes": p.stat().st_size, "sha256": hashlib.sha256(p.read_bytes()).hexdigest()} for p in PACK.rglob("*") if p.is_file()}
    (OUT / "pack-manifest.json").write_text(json.dumps(pack_files, indent=2), encoding="utf-8")
    page_csv = next(PACK.rglob("Pages.csv"))
    with page_csv.open(encoding="utf-8-sig", newline="") as handle:
        traffic = {urlsplit(r["Top pages"]).path: r for r in csv.DictReader(handle)}
    production = ROOT / ".gh-pages-deploy"
    members, chunks = sitemaps(production)
    sitemap_set = set(members)
    files = {"/" + str(p.relative_to(production).parent).replace("\\", "/").strip(".").strip("/") + "/": p for p in production.rglob("index.html") if ".git" not in p.parts}
    if "//" in files:
        files["/"] = files.pop("//")
    counts = Counter()
    families = Counter()
    ledger = []
    local = ROOT / "output"
    for route, path in sorted(files.items()):
        content = path.read_bytes()
        html = content.decode("utf-8", errors="replace")
        head = Head(html.split("</head>", 1)[0])
        canonical = head.canonicals[0] if len(head.canonicals) == 1 else ""
        noindex = any("noindex" in v or "none" in v.split(",") for v in head.robots)
        url = BASE + route
        selfcanonical = canonical == url
        local_path = local / path.relative_to(production)
        old = local_path.read_bytes() if local_path.exists() else None
        row_traffic = traffic.get(route) or traffic.get(route.rstrip("/")) or {}
        clicks = int(row_traffic.get("Clicks", "0"))
        family = route.strip("/").split("/")[0] or "root"
        families[family] += 1
        issues = []
        if not selfcanonical:
            issues.append("nonself_or_missing_canonical")
        if noindex:
            issues.append("noindex")
        if head.refresh:
            issues.append("meta_refresh")
        for issue in issues:
            counts[issue] += 1
            if url in sitemap_set:
                counts["sitemap_" + issue] += 1
        # Technical eligibility is NOT editorial quality approval or an HTTP observation.
        classification = "protect_pending_review" if clicks else "retain_pending_review"
        if issues:
            classification += ";technical_review"
        counts["protected_click_urls"] += bool(clicks)
        counts["different_from_local_output"] += old != content
        ledger.append({"url": url, "family": family, "production_file": str(path.relative_to(production)).replace("\\", "/"), "sha256": hashlib.sha256(content).hexdigest(), "bytes": len(content), "canonical": canonical, "canonical_count": len(head.canonicals), "noindex": noindex, "meta_refresh": " | ".join(head.refresh), "sitemap": url in sitemap_set, "clicks": clicks, "impressions": row_traffic.get("Impressions", ""), "position": row_traffic.get("Position", ""), "classification": classification, "quality_approved": False, "live_status": "unverified", "issue_bucket": "unknown", "local_output_same": old == content})
    file_urls = {BASE + r for r in files}
    for url in sorted(sitemap_set - file_urls):
        counts["sitemap_missing_file"] += 1
    with (OUT / "url-inventory.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(ledger[0]))
        writer.writeheader()
        writer.writerows(ledger)
    with (OUT / "protected-traffic-urls.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(next(iter(traffic.values()))))
        writer.writeheader()
        writer.writerows(traffic.values())
    local_members, local_chunks = sitemaps(local)
    summary = {"source_commit": git("rev-parse", "HEAD").strip(), "production_commit": "aa7d89ec029c70d5973b7d982fcbe5036316d9b2", "deploy_worktree_tree": git("rev-parse", "2e3a696^{tree}").strip(), "production_tree": git("rev-parse", "aa7d89e^{tree}").strip(), "production_html_index_files": len(files), "sitemap_entries": len(members), "sitemap_unique": len(sitemap_set), "sitemap_files": chunks, "sitemap_missing_urls": sorted(sitemap_set - file_urls), "counts": dict(counts), "families": dict(sorted(families.items())), "local_output_sitemap_entries": len(local_members), "local_output_sitemap_files": len(local_chunks), "traffic_export_rows": len(traffic), "traffic_urls_without_production_file": sorted(BASE + p for p in traffic if p not in files and p.rstrip("/") + "/" not in files), "git_skip_worktree_files": sum(x.startswith("S ") for x in git("ls-files", "-v").splitlines()), "elapsed_seconds": round(time.monotonic() - started, 2)}
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
