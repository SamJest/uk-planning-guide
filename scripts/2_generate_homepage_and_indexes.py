import sys
from pathlib import Path


CURRENT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = CURRENT_DIR.parent
sys.path.append(str(PROJECT_ROOT))

from data.loaders import load_councils, load_projects
from generators.homepage import generate_homepage
from generators.hubs import generate_councils_hub, generate_project_hubs


def main():
    print("Starting homepage and index generation")

    generate_homepage()

    projects = load_projects()
    councils_by_county = load_councils()
    generate_project_hubs(projects, councils_by_county)
    generate_councils_hub(councils_by_county)

    print("Homepage and index generation complete")


if __name__ == "__main__":
    main()
