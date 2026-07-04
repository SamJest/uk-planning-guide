import sys
from pathlib import Path


CURRENT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = CURRENT_DIR.parent
sys.path.append(str(PROJECT_ROOT))

from generators.download_assets import generate_download_assets


if __name__ == "__main__":
    generate_download_assets()
