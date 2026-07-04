import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from generators.project_scenario_pages import generate_project_scenario_pages

if __name__ == "__main__":
    generate_project_scenario_pages()
