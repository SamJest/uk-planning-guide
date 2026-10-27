import os
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

DATA_FOLDER = ROOT / "data"
TEMPLATES_FOLDER = ROOT / "templates"
_configured_output = str(os.environ.get("UKPG_OUTPUT_DIR") or "").strip()
OUTPUT_FOLDER = Path(_configured_output).resolve() if _configured_output else ROOT / "output"

BASE_URL = "https://ukplanningguide.co.uk"
FORCE_REBUILD = True
