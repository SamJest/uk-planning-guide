from __future__ import annotations

import argparse
import json
from pathlib import Path
from urllib.parse import urlparse


def route_file(base: Path, route: str) -> Path:
    clean = route.strip("/")
    return base / clean / "index.html" if clean else base / "index.html"


def analyse(ledger_path: Path, base: Path) -> dict:
    import csv

    with ledger_path.open(newline="", encoding="utf-8-sig") as handle:
        rows = list(csv.DictReader(handle))

    findings = []
    for row in rows:
        try:
            clicks = int(float(row.get("clicks") or 0))
        except ValueError:
            clicks = 0
        if clicks <= 0 or "404" not in str(row.get("http_status") or ""):
            continue

        parsed = urlparse(row["url"])
        parts = [part for part in parsed.path.split("/") if part]
        if len(parts) < 2:
            parent_route = "/"
            intent = parts[-1] if parts else ""
        else:
            parent_route = "/" + "/".join(parts[:-1]) + "/"
            intent = parts[-1]
        parent_exists = route_file(base, parent_route).exists()
        findings.append(
            {
                "missing_url": row["url"],
                "clicks": clicks,
                "family": row.get("family") or parts[0],
                "missing_rule_intent": intent,
                "same_authority_parent": parent_route,
                "parent_exists": parent_exists,
                "classification": "manual-equivalence-review",
                "recommended_action": (
                    "Use the parent as a visible recovery link. Do not redirect unless review proves that "
                    "the broader parent satisfies the missing combined-rule intent; otherwise restore only "
                    "from an explicit content contract."
                ),
            }
        )

    return {
        "status": "passed" if findings and all(item["parent_exists"] for item in findings) else "needs-review",
        "ledger": str(ledger_path),
        "production_base": str(base),
        "clicked_404_count": len(findings),
        "clicked_404_clicks": sum(item["clicks"] for item in findings),
        "same_authority_parent_found": sum(1 for item in findings if item["parent_exists"]),
        "redirects_authorised": 0,
        "restorations_authorised": 0,
        "findings": findings,
    }


def write_markdown(report: dict, destination: Path) -> None:
    lines = [
        "# Clicked 404 recovery analysis",
        "",
        f"- Missing clicked URLs: {report['clicked_404_count']}",
        f"- Recorded clicks: {report['clicked_404_clicks']}",
        f"- Existing same-authority parent pages: {report['same_authority_parent_found']}",
        "- Redirects authorised: 0",
        "- Restorations authorised: 0",
        "",
        "Every missing URL adds a combined rule-intent segment beneath an existing project/county/authority page. The parent is a safe visible recovery destination, but it is broader than the missing intent and therefore is not automatically an equivalent redirect target.",
        "",
        "| Missing path | Clicks | Existing recovery page | Missing intent | Decision |",
        "|---|---:|---|---|---|",
    ]
    for item in report["findings"]:
        path = urlparse(item["missing_url"]).path
        lines.append(
            f"| `{path}` | {item['clicks']} | `{item['same_authority_parent']}` | "
            f"`{item['missing_rule_intent']}` | Manual equivalence/content-contract review |"
        )
    lines.extend(
        [
            "",
            "## Safe next decision",
            "",
            "For each row, choose one of two evidence-backed treatments: prove the parent is a true substitute and implement a real HTTP redirect on a supporting host, or restore the exact URL from a reviewed content contract with authority/rule sources. Until then, keep the genuine 404 response and offer the parent as navigation. Do not use a client-side meta-refresh bridge as a substitute for an HTTP redirect.",
            "",
        ]
    )
    destination.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Map clicked live 404s to evidence-only recovery candidates.")
    parser.add_argument("--ledger", type=Path, required=True)
    parser.add_argument("--base", type=Path, required=True)
    parser.add_argument("--json-report", type=Path, required=True)
    parser.add_argument("--markdown-report", type=Path, required=True)
    args = parser.parse_args()

    report = analyse(args.ledger, args.base)
    args.json_report.parent.mkdir(parents=True, exist_ok=True)
    args.json_report.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    write_markdown(report, args.markdown_report)
    print(json.dumps({key: report[key] for key in report if key != "findings"}, indent=2))
    if report["status"] != "passed":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
