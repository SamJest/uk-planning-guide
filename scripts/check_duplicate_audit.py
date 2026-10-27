from pathlib import Path

from validate import OUTPUT_DIR, validate_duplicate_content


def main() -> None:
    pages = list(OUTPUT_DIR.rglob("*.html"))
    validate_duplicate_content(pages)


if __name__ == "__main__":
    main()
