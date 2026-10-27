from pathlib import Path

from data.scenario_data import SCENARIOS as SCENARIO_DATA


BASE_URL = "https://ukplanningguide.co.uk"

DATA_FOLDER = Path("data")
OUTPUT_FILE = DATA_FOLDER / "link_index.json"

MAX_NEARBY_COUNCILS = 8
MAX_NEARBY_COUNTIES = 8
MAX_RELATED_PROJECTS = 6
MAX_RELATED_SCENARIOS = 6
MAX_INTERNAL_RULE_LINKS = 8

SCENARIOS = [scenario["slug"] for scenario in SCENARIO_DATA]
