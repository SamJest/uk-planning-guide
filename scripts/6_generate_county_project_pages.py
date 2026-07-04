import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from generators.county_project_pages import generate_county_project_pages

if __name__ == "__main__":
    generate_county_project_pages()