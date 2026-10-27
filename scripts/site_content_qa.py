import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from utils.production_content import audit_output
from utils.content_contracts import load_page_records
from utils.jurisdiction_rules import validate_rule_module
import json


def audit_rule_data():
    root = Path(__file__).resolve().parents[1] / "data"
    for path in list((root / "rules").glob("*/national*.json")) + list((root / "rule_modules").glob("*/*.json")):
        record = json.loads(path.read_text(encoding="utf-8"))
        validate_rule_module(record, record.get("jurisdiction"))
    load_page_records()


if __name__ == "__main__":
    audit_rule_data()
    audit_output(sys.argv[1] if len(sys.argv) > 1 else "output")
