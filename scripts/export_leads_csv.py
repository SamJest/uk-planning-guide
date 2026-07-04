from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


DEFAULT_INPUT_DIR = ".lead_test_submissions"
DEFAULT_OUTPUT_FILE = "leads_export.csv"

CSV_COLUMNS = [
    "submitted_at",
    "source",
    "page_url",
    "project_type",
    "property_type",
    "postcode_or_town",
    "council",
    "restrictions",
    "timeframe",
    "desired_help",
    "route_result",
    "confidence",
    "name",
    "email",
    "phone",
    "consent_contact",
    "consent_share",
    "user_notes",
    "status",
]


def _read_json(path: Path) -> dict:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"Could not read {path}: {exc}") from exc
    if not isinstance(payload, dict):
        raise ValueError(f"{path} does not contain a JSON object")
    return payload


def _cell(payload: dict, key: str) -> str:
    if key == "status":
        return str(payload.get("status") or "New")
    if key == "restrictions":
        value = payload.get("restrictions", "")
        if not value and payload.get("restrictions_json"):
            try:
                value = json.loads(payload.get("restrictions_json") or "[]")
            except json.JSONDecodeError:
                value = payload.get("restrictions_json", "")
        if isinstance(value, list):
            return "; ".join(str(item) for item in value if str(item).strip())
        return str(value or "")
    if key == "user_notes":
        return str(payload.get("user_notes") or payload.get("notes") or "")
    value = payload.get(key, "")
    if isinstance(value, bool):
        return "yes" if value else "no"
    if key in {"consent_contact", "consent_share"} and str(value) in {"0", "1"}:
        return "yes" if str(value) == "1" else "no"
    if isinstance(value, (list, dict)):
        return json.dumps(value, ensure_ascii=False)
    return str(value or "")


def _iter_json_rows(input_dir: Path):
    for path in sorted(input_dir.glob("*.json")):
        yield _read_json(path)


def _iter_csv_rows(input_file: Path):
    with input_file.open("r", newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            yield dict(row)


def export_leads(input_path: Path, output_file: Path) -> int:
    if input_path.is_file() and input_path.suffix.lower() == ".csv":
        rows = _iter_csv_rows(input_path)
    else:
        rows = _iter_json_rows(input_path)

    output_file.parent.mkdir(parents=True, exist_ok=True)

    with output_file.open("w", newline="", encoding="utf-8-sig") as handle:
        writer = csv.DictWriter(handle, fieldnames=CSV_COLUMNS)
        writer.writeheader()
        count = 0
        for payload in rows:
            writer.writerow({column: _cell(payload, column) for column in CSV_COLUMNS})
            count += 1
    return count


def main() -> None:
    parser = argparse.ArgumentParser(description="Export saved Planning Route Check lead JSON files or a D1 CSV export to owner CSV.")
    parser.add_argument("--input", default=DEFAULT_INPUT_DIR, help="Folder containing saved JSON lead files, or a CSV export from D1.")
    parser.add_argument("--output", default=DEFAULT_OUTPUT_FILE, help="CSV output path.")
    args = parser.parse_args()

    input_dir = Path(args.input)
    output_file = Path(args.output)

    if not input_dir.exists():
        raise SystemExit(f"Input path does not exist: {input_dir}")

    count = export_leads(input_dir, output_file)
    print(f"Exported {count} lead(s) to {output_file}")


if __name__ == "__main__":
    main()
