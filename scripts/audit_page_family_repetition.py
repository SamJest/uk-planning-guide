from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from validate import OUTPUT_DIR, validate_family_repetition  # noqa: E402


def main() -> None:
    pages = list(OUTPUT_DIR.rglob("index.html"))
    validate_family_repetition(pages)


if __name__ == "__main__":
    main()
