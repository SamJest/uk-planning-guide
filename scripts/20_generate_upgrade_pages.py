import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from generators.upgrade_pages import generate_upgrade_pages


if __name__ == "__main__":
    generate_upgrade_pages()
