import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from generators.building_regulations_pages import generate_building_regulations_pages


if __name__ == "__main__":
    generate_building_regulations_pages()
