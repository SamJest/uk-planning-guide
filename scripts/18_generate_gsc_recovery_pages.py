import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from generators.gsc_recovery_pages import generate_gsc_recovery_pages


if __name__ == "__main__":
    generate_gsc_recovery_pages()
