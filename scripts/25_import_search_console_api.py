from __future__ import annotations

import argparse
import csv
from datetime import date, timedelta
import json
import os
from pathlib import Path
import sys
import urllib.error
import urllib.parse
import urllib.request


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SITE = "sc-domain:ukplanningguide.co.uk"
DEFAULT_DIMENSIONS = ("date", "page", "query", "country", "device")
ROW_LIMIT = 25000


def _request_page(
    *,
    site_url: str,
    access_token: str,
    start_date: str,
    end_date: str,
    start_row: int,
) -> list[dict]:
    endpoint = (
        "https://www.googleapis.com/webmasters/v3/sites/"
        + urllib.parse.quote(site_url, safe="")
        + "/searchAnalytics/query"
    )
    body = json.dumps(
        {
            "startDate": start_date,
            "endDate": end_date,
            "dimensions": list(DEFAULT_DIMENSIONS),
            "type": "web",
            "dataState": "final",
            "rowLimit": ROW_LIMIT,
            "startRow": start_row,
        }
    ).encode("utf-8")
    request = urllib.request.Request(
        endpoint,
        data=body,
        method="POST",
        headers={
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
        },
    )
    with urllib.request.urlopen(request, timeout=60) as response:
        payload = json.loads(response.read().decode("utf-8"))
    return list(payload.get("rows", []))


def import_rows(
    *,
    site_url: str,
    access_token: str,
    start_date: str,
    end_date: str,
) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    start_row = 0
    while True:
        batch = _request_page(
            site_url=site_url,
            access_token=access_token,
            start_date=start_date,
            end_date=end_date,
            start_row=start_row,
        )
        for row in batch:
            keys = list(row.get("keys", []))
            keys.extend([""] * (len(DEFAULT_DIMENSIONS) - len(keys)))
            rows.append(
                {
                    **dict(zip(DEFAULT_DIMENSIONS, keys)),
                    "clicks": int(round(float(row.get("clicks", 0)))),
                    "impressions": int(round(float(row.get("impressions", 0)))),
                    "ctr": round(float(row.get("ctr", 0)), 6),
                    "position": round(float(row.get("position", 0)), 3),
                }
            )
        if len(batch) < ROW_LIMIT:
            break
        start_row += ROW_LIMIT
    return rows


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Import final Search Console page-query-country-device rows for the growth report."
    )
    parser.add_argument("--site-url", default=DEFAULT_SITE)
    parser.add_argument("--start-date")
    parser.add_argument("--end-date")
    parser.add_argument("--days", type=int, default=28)
    parser.add_argument("--token-env", default="GSC_ACCESS_TOKEN")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    end_day = date.fromisoformat(args.end_date) if args.end_date else date.today() - timedelta(days=3)
    start_day = date.fromisoformat(args.start_date) if args.start_date else end_day - timedelta(days=args.days - 1)
    access_token = os.environ.get(args.token_env, "").strip()
    if not access_token:
        raise SystemExit(f"Missing OAuth access token in environment variable {args.token_env}")

    output = args.output or ROOT / "artifacts" / "growth" / str(end_day) / "gsc-page-query-country-device.csv"
    try:
        rows = import_rows(
            site_url=args.site_url,
            access_token=access_token,
            start_date=str(start_day),
            end_date=str(end_day),
        )
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise SystemExit(f"Search Console API returned HTTP {exc.code}: {detail[:600]}") from exc

    output.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [*DEFAULT_DIMENSIONS, "clicks", "impressions", "ctr", "position"]
    with output.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    metadata = {
        "site_url": args.site_url,
        "start_date": str(start_day),
        "end_date": str(end_day),
        "dimensions": list(DEFAULT_DIMENSIONS),
        "data_state": "final",
        "rows": len(rows),
    }
    output.with_suffix(".json").write_text(json.dumps(metadata, indent=2), encoding="utf-8")
    print(f"Imported {len(rows)} final Search Console rows to {output}")


if __name__ == "__main__":
    main()

