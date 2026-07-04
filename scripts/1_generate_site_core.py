import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from generators.site_core import generate_site_core

if __name__ == "__main__":
    generate_site_core()