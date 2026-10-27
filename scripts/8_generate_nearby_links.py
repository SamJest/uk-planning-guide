import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from generators.link_graph import generate_links

if __name__ == "__main__":
    generate_links()