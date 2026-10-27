import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from generators.local_search_pages import generate_local_search_pages

if __name__ == "__main__":
    generate_local_search_pages()
