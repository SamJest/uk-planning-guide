import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from generators.council_pages import generate_council_pages

if __name__ == "__main__":
    generate_council_pages()