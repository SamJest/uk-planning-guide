import os
import shutil
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Dict, List

from utils.sitemap_config import *
from utils.indexation import load_indexation_manifest, should_include_in_sitemap
from utils.scenario_relevance import is_relevant_scenario
from utils.route_contracts import route_contract_for_country_path
from core.build_scope import should_publish_route
from utils.content_contracts import load_page_records, page_record_for_url


def classify_url(url: str) -> str:
    path = url.replace(BASE_URL, "").strip("/")

    if path == "":
        return "root"

    parts = path.split("/")
    depth = len(parts)

    country_contract = route_contract_for_country_path("/" + path + "/")
    if country_contract:
        if depth == 1:
            return f"{parts[0]}-root"
        if depth == 2:
            return f"{parts[0]}-{parts[1]}-hub"
        return f"{parts[0]}-{country_contract.intent_type}"

    if parts[0] == "find-help" and parts[-1] == "success":
        return "utility"

    if parts[0] == "planning-help" and parts[-1] == "thank-you":
        return "utility"

    if parts[0] == "personalised-planning-guidance" and (parts[-1] == "request" or parts[-1] == "success"):
        return "utility"

    if parts[0] in SCENARIO_HUBS and depth == 1:
        return "scenario-hubs"

    if parts[0] in SCENARIO_HUBS and depth == 2:
        return "scenario-pages"

    if parts[0] == "tools" and depth == 1:
        return "tools-hub"

    if parts[0] == "tools" and depth == 2:
        return "tools"

    if parts[0] == "workflows" and depth == 1:
        return "workflow-hub"

    if parts[0] == "workflows" and depth == 2:
        return "workflows"

    if parts[0] == "planning-faq" and depth == 1:
        return "faq-hub"

    if parts[0] == "planning-faq" and depth == 2:
        return "faq"

    if parts[0] == "building-regulations" and depth == 1:
        return "building-regulations-hub"

    if parts[0] == "building-regulations" and depth == 2:
        return "building-regulations"

    if parts[0] == "downloads" and depth == 1:
        return "downloads-hub"

    if parts[0] == "downloads" and depth == 2:
        return "download-assets"

    if parts[0] == "local-search" and depth == 1:
        return "local-search-hub"

    if parts[0] == "local-search" and depth == 2:
        return "local-search"

    if parts[0] in {"about", "methodology", "privacy", "editorial-policy", "planning-help", "my-planning-project"} and depth == 1:
        return "trust-pages"

    if parts[0] == "councils" and depth == 1:
        return "council-hubs"

    if parts[0] == "councils" and depth == 2:
        return "council"

    if parts[0] in PROJECT_HUBS and depth == 1:
        return "projects"

    if parts[0] in AREA_HUBS and depth == 1:
        return "area-hubs"

    if parts[0] in PROJECT_HUBS and depth == 2 and parts[1] in AREA_HUBS:
        return "county-projects"

    if parts[0] in PROJECT_HUBS and depth == 3 and parts[1] in AREA_HUBS:
        return "council-projects"

    if parts[0] in PROJECT_HUBS and depth == 4 and parts[1] in AREA_HUBS:
        if is_gsc_recovery_path(f"/{path}/"):
            return "gsc-recovery"
        if parts[3] in SCENARIO_HUBS:
            if is_relevant_scenario(parts[0], parts[3]):
                return "project-scenario-pages"
            return "supplemental-scenarios"
        return "scenario-combinations"

    if depth == 1:
        return "misc-hubs"

    if depth == 4:
        return "scenario-pages"

    return "misc"


def priority_for_url(url: str) -> str:
    path = url.replace(BASE_URL, "").strip("/")

    if path == "":
        return "1.0"

    parts = path.split("/")
    first = parts[0]
    depth = len(parts)

    if first in {"about", "methodology", "privacy", "editorial-policy", "planning-help", "my-planning-project"}:
        return "0.6"

    if first in {"tools", "planning-faq", "workflows", "building-regulations", "downloads"} and depth == 1:
        return "0.8"

    if first in {"tools", "planning-faq", "workflows", "building-regulations", "downloads"} and depth == 2:
        return "0.7"

    if classify_url(url) == "gsc-recovery":
        return "0.6"

    if first in AREA_HUBS and depth == 1:
        return "0.85"

    if depth == 1:
        return "0.9"

    if depth == 2:
        return "0.8"

    if depth == 3:
        return "0.7"

    if classify_url(url) == "supplemental-scenarios":
        return "0.5"

    return "0.6"


def changefreq_for_url(section: str) -> str:
    if section in ("root", "scenario-hubs", "projects", "area-hubs", "council-hubs", "tools-hub", "faq-hub", "workflow-hub", "building-regulations-hub", "downloads-hub"):
        return "weekly"

    if section in ("scenario-pages", "supplemental-scenarios", "tools", "workflows", "faq", "trust-pages", "building-regulations", "download-assets"):
        return "monthly"

    return "monthly"


def collect_urls() -> List[str]:
    urls = []
    manifest = load_indexation_manifest()

    for root, dirs, files in os.walk(OUTPUT_FOLDER):
        if "index.html" in files:
            path = Path(root)
            relative = path.relative_to(OUTPUT_FOLDER)

            if str(relative) == ".":
                url = BASE_URL.rstrip("/") + "/"
            else:
                clean_path = str(relative).replace("\\", "/").strip().strip("/")
                url = BASE_URL.rstrip("/") + "/" + clean_path + "/"

            html_path = path / "index.html"
            route_path = "/" if str(relative) == "." else "/" + str(relative).replace("\\", "/").strip("/") + "/"
            if not should_publish_route(route_path):
                continue
            section = classify_url(url)
            if section in EXCLUDED_SITEMAP_SECTIONS:
                continue
            if route_path in manifest:
                html = ""
            else:
                with html_path.open("r", encoding="utf-8", errors="ignore") as handle:
                    html = handle.read(65536)
            if not should_include_in_sitemap(route_path, html):
                continue

            urls.append(url)

    return sorted(urls)


def validate_sitemap_urls(urls: List[str]):
    seen = set()

    for url in urls:
        if not url.startswith(BASE_URL):
            raise ValueError(f"Malformed URL: {url}")

        if url in seen:
            raise ValueError(f"Duplicate URL detected: {url}")

        seen.add(url)


def group_urls_by_section(urls: List[str]) -> Dict[str, List[str]]:
    grouped = {}

    for url in urls:
        section = classify_url(url)
        if section in EXCLUDED_SITEMAP_SECTIONS:
            continue
        grouped.setdefault(section, []).append(url)

    return grouped


def split_chunks(urls: List[str]) -> List[List[str]]:
    return [urls[i : i + CHUNK_SIZE] for i in range(0, len(urls), CHUNK_SIZE)]


def _validate_section_name(section: str) -> None:
    if not CHILD_SITEMAP_SECTION_PATTERN.fullmatch(section or ""):
        raise ValueError(f"Malformed sitemap section name: {section!r}")


def _child_sitemap_filename(section: str, index: int) -> str:
    _validate_section_name(section)
    if index < 1:
        raise ValueError(f"Malformed sitemap chunk index: {index}")

    filename = f"sitemap-{section}-{index}.xml"
    if not CHILD_SITEMAP_NAME_PATTERN.fullmatch(filename):
        raise ValueError(f"Malformed sitemap filename generated: {filename}")

    return filename


def _clear_existing_sitemap_outputs() -> None:
    if SITEMAP_FOLDER.exists():
        shutil.rmtree(SITEMAP_FOLDER)

    SITEMAP_FOLDER.mkdir(parents=True, exist_ok=True)

    if not OUTPUT_FOLDER.exists():
        return

    for item in OUTPUT_FOLDER.iterdir():
        if not item.is_file():
            continue
        if item.name == "sitemap.xml":
            continue
        if LEGACY_ROOT_SITEMAP_NAME_PATTERN.fullmatch(item.name):
            item.unlink()


def build_urlset(urls: List[str], section: str) -> ET.Element:
    urlset = ET.Element("urlset", xmlns=XML_NAMESPACE)

    for url in urls:
        node = ET.SubElement(urlset, "url")
        ET.SubElement(node, "loc").text = url
        record = page_record_for_url(url)
        ET.SubElement(node, "lastmod").text = record["content_updated_at"] if record else TODAY
        ET.SubElement(node, "changefreq").text = changefreq_for_url(section)
        ET.SubElement(node, "priority").text = priority_for_url(url)

    return urlset


def generate_section_sitemaps(grouped_urls: Dict[str, List[str]]):
    _clear_existing_sitemap_outputs()
    sitemap_files = []

    for section in sorted(grouped_urls):
        chunks = split_chunks(sorted(grouped_urls[section]))

        for index, chunk in enumerate(chunks, start=1):
            urlset = build_urlset(chunk, section)
            tree = ET.ElementTree(urlset)
            filename = _child_sitemap_filename(section, index)
            file_path = SITEMAP_FOLDER / filename
            tree.write(file_path, encoding="utf-8", xml_declaration=True)
            sitemap_files.append(file_path)

    return sorted(sitemap_files, key=lambda path: path.name)


def generate_sitemap_index(sitemap_files):
    root = ET.Element("sitemapindex", xmlns=XML_NAMESPACE)
    contract_dates = [record["content_updated_at"] for record in load_page_records() if record["index_status"] == "index"]
    index_lastmod = max(contract_dates) if contract_dates else TODAY

    for file_path in sorted(sitemap_files, key=lambda path: path.name):
        if file_path.parent != SITEMAP_FOLDER:
            raise ValueError(f"Sitemap file written outside sitemap folder: {file_path}")
        if not CHILD_SITEMAP_NAME_PATTERN.fullmatch(file_path.name):
            raise ValueError(f"Malformed sitemap file referenced in index: {file_path.name}")
        sitemap = ET.SubElement(root, "sitemap")
        ET.SubElement(sitemap, "loc").text = f"{BASE_URL}/sitemaps/{file_path.name}"
        ET.SubElement(sitemap, "lastmod").text = index_lastmod

    tree = ET.ElementTree(root)
    tree.write(OUTPUT_FOLDER / "sitemap.xml", encoding="utf-8", xml_declaration=True)


def update_robots():
    robots_file = OUTPUT_FOLDER / "robots.txt"
    sitemap_line = f"Sitemap: {BASE_URL}/sitemap.xml"

    if robots_file.exists():
        content = robots_file.read_text(encoding="utf-8")
        if sitemap_line not in content:
            content += "\n" + sitemap_line + "\n"
            robots_file.write_text(content, encoding="utf-8")
    else:
        robots_file.write_text(sitemap_line + "\n", encoding="utf-8")
