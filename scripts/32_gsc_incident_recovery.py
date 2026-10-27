"""Analyse the July 2026 GSC incident and build a screened recovery cohort."""

from __future__ import annotations

import argparse
import csv
from collections import Counter
from datetime import date
import json
from pathlib import Path
import re
from urllib.parse import urlparse
import xml.etree.ElementTree as ET


ROOT = Path(__file__).resolve().parents[1]
BASE_URL = "https://ukplanningguide.co.uk"
NS = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as stream:
        return list(csv.DictReader(stream))


def route_file(site_root: Path, url: str) -> Path:
    path = urlparse(url).path
    return site_root / ("index.html" if path == "/" else f"{path.strip('/')}/index.html")


def sitemap_urls(site_root: Path) -> set[str]:
    index = ET.parse(site_root / "sitemap.xml").getroot()
    urls: set[str] = set()
    for node in index.findall("sm:sitemap/sm:loc", NS):
        child = site_root / "sitemaps" / (node.text or "").rsplit("/", 1)[-1]
        if not child.exists():
            continue
        root = ET.parse(child).getroot()
        urls.update((loc.text or "").strip() for loc in root.findall("sm:url/sm:loc", NS))
    return urls


def average(rows: list[dict[str, str]], field: str) -> float:
    return sum(float(row[field].rstrip("%")) for row in rows) / len(rows)


def write_recovery_sitemap(site_root: Path, candidates: list[dict[str, object]]) -> Path:
    ET.register_namespace("", NS["sm"])
    filename = "sitemap-gsc-incident-recovery-1.xml"
    sitemap_path = site_root / "sitemaps" / filename
    urlset = ET.Element(f"{{{NS['sm']}}}urlset")
    for candidate in candidates:
        url = ET.SubElement(urlset, f"{{{NS['sm']}}}url")
        ET.SubElement(url, f"{{{NS['sm']}}}loc").text = str(candidate["url"])
    sitemap_path.parent.mkdir(parents=True, exist_ok=True)
    ET.ElementTree(urlset).write(sitemap_path, encoding="utf-8", xml_declaration=True)

    index_path = site_root / "sitemap.xml"
    index_tree = ET.parse(index_path)
    index_root = index_tree.getroot()
    public_url = f"{BASE_URL}/sitemaps/{filename}"
    existing = {
        (node.text or "").strip()
        for node in index_root.findall("sm:sitemap/sm:loc", NS)
    }
    if public_url not in existing:
        sitemap = ET.SubElement(index_root, f"{{{NS['sm']}}}sitemap")
        ET.SubElement(sitemap, f"{{{NS['sm']}}}loc").text = public_url
        index_tree.write(index_path, encoding="utf-8", xml_declaration=True)
    return sitemap_path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--site-root", type=Path, default=ROOT / ".gh-pages-deploy")
    parser.add_argument(
        "--incident-root",
        type=Path,
        default=ROOT / "reports" / "gsc-incident-2026-07-05",
    )
    parser.add_argument(
        "--write-sitemap",
        action="store_true",
        help="Write the screened recovery sitemap into --site-root and register it in sitemap.xml.",
    )
    args = parser.parse_args()
    site_root = args.site_root.resolve()
    incident_root = args.incident_root.resolve()

    performance = read_csv(incident_root / "performance" / "Chart.csv")
    coverage = read_csv(incident_root / "coverage" / "Chart.csv")
    page_rows = read_csv(incident_root / "performance" / "Pages.csv")
    inventory_rows = json.loads((ROOT / "reports" / "phase-0" / "page-inventory.json").read_text(encoding="utf-8"))
    inventory = {row["url"]: row for row in inventory_rows}
    submitted = sitemap_urls(site_root)

    before = [row for row in performance if "2026-06-24" <= row["Date"] <= "2026-06-30"]
    after = [row for row in performance if row["Date"] >= "2026-07-01"]
    coverage_before = next(row for row in coverage if row["Date"] == "2026-06-12")
    coverage_after = next(row for row in coverage if row["Date"] == "2026-06-13")

    exclusions: Counter[str] = Counter()
    action_counts: Counter[str] = Counter()
    candidates: list[dict[str, object]] = []
    for row in page_rows:
        url = row["Top pages"]
        inventory_row = inventory.get(url)
        action = (inventory_row or {}).get("proposed_action", "missing")
        action_counts[action] += 1
        if url in submitted:
            exclusions["already_in_sitemap"] += 1
            continue
        page_path = route_file(site_root, url)
        if not page_path.exists():
            exclusions["missing_file"] += 1
            continue
        html = page_path.read_text(encoding="utf-8", errors="ignore")
        canonical = re.search(r'<link\s+rel="canonical"\s+href="([^"]+)"', html, re.I)
        robots = re.search(r'<meta\s+name="robots"\s+content="([^"]+)"', html, re.I)
        if not canonical or canonical.group(1) != url:
            exclusions["canonical_mismatch"] += 1
            continue
        if robots and "noindex" in robots.group(1).lower():
            exclusions["noindex"] += 1
            continue
        if action in {"noindex", "redirect", "410"}:
            exclusions["unsafe_inventory_action"] += 1
            continue
        candidates.append(
            {
                "url": url,
                "clicks": int(row["Clicks"]),
                "impressions": int(row["Impressions"]),
                "ctr": row["CTR"],
                "position": float(row["Position"]),
                "inventory_action": action,
                "word_count": (inventory_row or {}).get("word_count", 0),
                "similarity": (inventory_row or {}).get("content_similarity_score", 0),
                "contamination": (inventory_row or {}).get("contamination_flags", ""),
            }
        )

    candidates.sort(key=lambda row: (-int(row["clicks"]), -int(row["impressions"])))
    result = {
        "analysed_at": date.today().isoformat(),
        "incident_start": "2026-07-01",
        "performance": {
            "before_period": "2026-06-24 to 2026-06-30",
            "after_period": "2026-07-01 to 2026-07-03",
            "before_daily_clicks": average(before, "Clicks"),
            "after_daily_clicks": average(after, "Clicks"),
            "before_daily_impressions": average(before, "Impressions"),
            "after_daily_impressions": average(after, "Impressions"),
            "before_position": average(before, "Position"),
            "after_position": average(after, "Position"),
        },
        "coverage_cohort_change": {
            "before_date": coverage_before["Date"],
            "before_total": int(coverage_before["Indexed"]) + int(coverage_before["Not indexed"]),
            "after_date": coverage_after["Date"],
            "after_total": int(coverage_after["Indexed"]) + int(coverage_after["Not indexed"]),
            "current_submitted_urls": len(submitted),
        },
        "top_page_inventory_actions": dict(action_counts),
        "candidate_count": len(candidates),
        "candidate_clicks": sum(int(row["clicks"]) for row in candidates),
        "candidate_impressions": sum(int(row["impressions"]) for row in candidates),
        "exclusions": dict(exclusions),
    }

    incident_root.mkdir(parents=True, exist_ok=True)
    (incident_root / "analysis.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    with (incident_root / "recovery-candidates.csv").open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(candidates[0]) if candidates else ["url"])
        writer.writeheader()
        writer.writerows(candidates)
    if args.write_sitemap:
        sitemap_path = write_recovery_sitemap(site_root, candidates)
        result["recovery_sitemap"] = str(sitemap_path)
        (incident_root / "analysis.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
