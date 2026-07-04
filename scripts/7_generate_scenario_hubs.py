import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from generators.scenario_hubs import generate_scenario_hub_pages

if __name__ == "__main__":
    generate_scenario_hub_pages()