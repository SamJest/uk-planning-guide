import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from generators.planning_tools import generate_tools

if __name__ == "__main__":
    generate_tools()