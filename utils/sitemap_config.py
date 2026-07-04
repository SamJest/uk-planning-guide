import re
from datetime import datetime

from data.loaders import load_councils, load_projects
from data.scenario_data import SCENARIOS as SCENARIO_DATA
from data.gsc_recovery_routes import is_gsc_recovery_path
from core.paths import OUTPUT_FOLDER


SITEMAP_FOLDER = OUTPUT_FOLDER / "sitemaps"

BASE_URL = "https://ukplanningguide.co.uk"
CHUNK_SIZE = 5000
TODAY = datetime.today().strftime("%Y-%m-%d")
XML_NAMESPACE = "http://www.sitemaps.org/schemas/sitemap/0.9"
CHILD_SITEMAP_NAME_PATTERN = re.compile(r"^sitemap-[a-z0-9-]+-[1-9][0-9]*\.xml$")
CHILD_SITEMAP_SECTION_PATTERN = re.compile(r"^[a-z0-9-]+$")
LEGACY_ROOT_SITEMAP_NAME_PATTERN = re.compile(r"^sitemap-[a-z0-9-]+(?:-[1-9][0-9]*)?\.xml$")

SCENARIO_HUBS = [scenario["slug"] for scenario in SCENARIO_DATA]
PROJECT_HUBS = {project["slug"] for project in load_projects()}
AREA_HUBS = set(load_councils().keys())
EXCLUDED_SITEMAP_SECTIONS = {
    "scenario-combinations",
    "supplemental-scenarios",
    "utility",
    "local-search-hub",
    "england-services",
    "england-services-hub",
}
