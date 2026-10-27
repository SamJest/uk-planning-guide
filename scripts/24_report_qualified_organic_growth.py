from __future__ import annotations

import argparse
import csv
from dataclasses import dataclass
from datetime import date, datetime, timedelta
import io
import json
from pathlib import Path
import re
import sys
from urllib.parse import urlparse
import zipfile


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from data.organic_growth import CTR_TEST_TARGETS, INDEXATION_POLICY
from utils.indexation import INDEXATION_MANIFEST_CSV, normalize_path


CHART = "Chart.csv"
QUERIES = "Queries.csv"
PAGES = "Pages.csv"
COUNTRIES = "Countries.csv"
DEVICES = "Devices.csv"


@dataclass(frozen=True)
class PeriodMetrics:
    start: str
    end: str
    days: int
    clicks: int
    impressions: int
    ctr: float
    position: float

    def to_dict(self) -> dict[str, object]:
        return {
            "start": self.start,
            "end": self.end,
            "days": self.days,
            "clicks": self.clicks,
            "impressions": self.impressions,
            "ctr": self.ctr,
            "position": self.position,
        }


def _number(value: object) -> float:
    clean = str(value or "").replace(",", "").replace("%", "").strip()
    try:
        return float(clean)
    except ValueError:
        return 0.0


def _ctr(value: object) -> float:
    number = _number(value)
    return number / 100 if "%" in str(value) or number > 1 else number


def _first(row: dict[str, str], *names: str) -> str:
    lowered = {str(key).strip().lower(): value for key, value in row.items()}
    for name in names:
        value = lowered.get(name.lower())
        if value not in (None, ""):
            return str(value)
    return ""


def _read_zip_csv(archive: zipfile.ZipFile, name: str) -> list[dict[str, str]]:
    if name not in archive.namelist():
        return []
    text = archive.read(name).decode("utf-8-sig")
    return list(csv.DictReader(io.StringIO(text)))


def _export_date(path: Path, explicit: str | None) -> date:
    if explicit:
        return date.fromisoformat(explicit)
    match = re.search(r"(20\d{2}-\d{2}-\d{2})", path.name)
    if match:
        return date.fromisoformat(match.group(1))
    return date.today()


def _chart_rows(rows: list[dict[str, str]]) -> list[dict[str, object]]:
    result = []
    for row in rows:
        try:
            day = date.fromisoformat(_first(row, "date"))
        except ValueError:
            continue
        result.append(
            {
                "date": day,
                "clicks": int(_number(_first(row, "clicks"))),
                "impressions": int(_number(_first(row, "impressions"))),
                "position": _number(_first(row, "position", "average position")),
            }
        )
    return sorted(result, key=lambda item: item["date"])


def _period(rows: list[dict[str, object]]) -> PeriodMetrics:
    if not rows:
        return PeriodMetrics("", "", 0, 0, 0, 0.0, 0.0)
    clicks = sum(int(row["clicks"]) for row in rows)
    impressions = sum(int(row["impressions"]) for row in rows)
    weighted_position = (
        sum(float(row["position"]) * int(row["impressions"]) for row in rows) / impressions
        if impressions
        else 0.0
    )
    return PeriodMetrics(
        start=str(rows[0]["date"]),
        end=str(rows[-1]["date"]),
        days=len(rows),
        clicks=clicks,
        impressions=impressions,
        ctr=round(clicks / impressions, 5) if impressions else 0.0,
        position=round(weighted_position, 2),
    )


def _change(current: float, previous: float) -> float | None:
    if not previous:
        return None
    return round(current / previous - 1, 4)


def _incident_status(rows: list[dict[str, object]]) -> dict[str, object]:
    required = int(INDEXATION_POLICY["incident_consecutive_days"])
    threshold = 1 - float(INDEXATION_POLICY["incident_drop_threshold"])
    checks = []
    for row in rows[-required:]:
        history = [
            prior
            for prior in rows
            if prior["date"] < row["date"]
            and prior["date"].weekday() == row["date"].weekday()
            and prior["date"] >= row["date"] - timedelta(days=28)
        ][-4:]
        baseline_clicks = sum(int(item["clicks"]) for item in history) / len(history) if history else 0
        baseline_impressions = sum(int(item["impressions"]) for item in history) / len(history) if history else 0
        drop = bool(
            history
            and int(row["clicks"]) < baseline_clicks * threshold
            and int(row["impressions"]) < baseline_impressions * threshold
        )
        checks.append(
            {
                "date": str(row["date"]),
                "clicks": row["clicks"],
                "impressions": row["impressions"],
                "weekday_baseline_clicks": round(baseline_clicks, 1),
                "weekday_baseline_impressions": round(baseline_impressions, 1),
                "material_drop": drop,
            }
        )
    return {
        "alert": len(checks) == required and all(item["material_drop"] for item in checks),
        "rule": f"{required} complete days with clicks and impressions at least 40% below their 28-day weekday baseline",
        "checks": checks,
    }


def _dimension_summary(rows: list[dict[str, str]], key: str) -> list[dict[str, object]]:
    result = []
    for row in rows:
        impressions = int(_number(_first(row, "impressions")))
        clicks = int(_number(_first(row, "clicks")))
        result.append(
            {
                "name": _first(row, key),
                "clicks": clicks,
                "impressions": impressions,
                "ctr": round(clicks / impressions, 5) if impressions else 0.0,
                "position": round(_number(_first(row, "position", "average position")), 2),
            }
        )
    return sorted(result, key=lambda item: item["impressions"], reverse=True)


def _page_opportunities(rows: list[dict[str, str]]) -> list[dict[str, object]]:
    opportunities = []
    for row in rows:
        impressions = int(_number(_first(row, "impressions")))
        clicks = int(_number(_first(row, "clicks")))
        position = _number(_first(row, "position", "average position"))
        ctr = _ctr(_first(row, "ctr"))
        if impressions < 100 or not 4 <= position <= 20 or ctr >= 0.02:
            continue
        page = _first(row, "top pages", "page")
        opportunities.append(
            {
                "page": page,
                "clicks": clicks,
                "impressions": impressions,
                "ctr": round(ctr, 5),
                "position": round(position, 2),
                "opportunity_score": round(impressions * max(0.02 - ctr, 0) / max(position, 1), 2),
            }
        )
    return sorted(opportunities, key=lambda item: item["opportunity_score"], reverse=True)


def _load_csv(path: Path | None) -> list[dict[str, str]]:
    if not path or not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def _combined_page_query_analysis(rows: list[dict[str, str]]) -> tuple[list[dict[str, object]], list[dict[str, object]]]:
    opportunities = []
    query_pages: dict[str, dict[str, dict[str, float]]] = {}
    for row in rows:
        country = _first(row, "country").lower()
        if country and country not in {"gbr", "united kingdom", "uk"}:
            continue
        page = _first(row, "page", "top pages")
        query = _first(row, "query", "top queries")
        if not page or not query:
            continue
        clicks = _number(_first(row, "clicks"))
        impressions = _number(_first(row, "impressions"))
        position = _number(_first(row, "position", "average position"))
        ctr = clicks / impressions if impressions else 0.0
        if impressions >= 20 and 4 <= position <= 20 and ctr < 0.02:
            opportunities.append(
                {
                    "page": page,
                    "query": query,
                    "clicks": int(clicks),
                    "impressions": int(impressions),
                    "ctr": round(ctr, 5),
                    "position": round(position, 2),
                }
            )
        page_totals = query_pages.setdefault(query, {}).setdefault(
            normalize_path(page),
            {"clicks": 0.0, "impressions": 0.0},
        )
        page_totals["clicks"] += clicks
        page_totals["impressions"] += impressions

    cannibalisation = []
    for query, pages in query_pages.items():
        material = {page: values for page, values in pages.items() if values["impressions"] >= 10}
        if len(material) < 2:
            continue
        ranked = sorted(
            material.items(),
            key=lambda item: (item[1]["clicks"], item[1]["impressions"]),
            reverse=True,
        )
        cannibalisation.append(
            {
                "query": query,
                "search_owner": ranked[0][0],
                "competing_pages": len(ranked),
                "total_impressions": int(sum(item[1]["impressions"] for item in ranked)),
                "pages": [item[0] for item in ranked],
            }
        )
    opportunities.sort(key=lambda item: item["impressions"], reverse=True)
    cannibalisation.sort(key=lambda item: item["total_impressions"], reverse=True)
    return opportunities, cannibalisation


def _ga4_summary(rows: list[dict[str, str]]) -> dict[str, object]:
    totals = {"users": 0.0, "engaged_sessions": 0.0, "conversions": 0.0}
    for row in rows:
        country = _first(row, "country").lower()
        medium = _first(row, "session medium", "medium", "default channel group").lower()
        if country and country not in {"united kingdom", "uk", "gbr"}:
            continue
        if medium and "organic" not in medium:
            continue
        totals["users"] += _number(_first(row, "users", "active users"))
        totals["engaged_sessions"] += _number(_first(row, "engaged sessions"))
        totals["conversions"] += _number(_first(row, "conversions", "key events"))
    return {key: int(value) for key, value in totals.items()}


def _write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    fieldnames = list(rows[0])
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def _pct(value: float | None) -> str:
    return "n/a" if value is None else f"{value:+.1%}"


def build_report(
    gsc_zip: Path,
    output_dir: Path,
    *,
    as_of: str | None = None,
    page_query_csv: Path | None = None,
    ga4_csv: Path | None = None,
) -> dict[str, object]:
    export_day = _export_date(gsc_zip, as_of)
    cutoff = export_day - timedelta(days=int(INDEXATION_POLICY["fresh_data_hours"]) // 24)
    with zipfile.ZipFile(gsc_zip) as archive:
        chart = _chart_rows(_read_zip_csv(archive, CHART))
        query_rows = _read_zip_csv(archive, QUERIES)
        page_rows = _read_zip_csv(archive, PAGES)
        country_rows = _read_zip_csv(archive, COUNTRIES)
        device_rows = _read_zip_csv(archive, DEVICES)

    complete = [row for row in chart if row["date"] <= cutoff]
    preliminary = [row for row in chart if row["date"] > cutoff]
    latest7 = _period(complete[-7:])
    prior7 = _period(complete[-14:-7])
    latest28 = _period(complete[-28:])
    prior28 = _period(complete[-56:-28])
    countries = _dimension_summary(country_rows, "country")
    devices = _dimension_summary(device_rows, "device")
    uk = next((item for item in countries if item["name"] == "United Kingdom"), {})
    query_clicks = sum(int(_number(_first(row, "clicks"))) for row in query_rows)
    query_impressions = sum(int(_number(_first(row, "impressions"))) for row in query_rows)
    all_period = _period(chart)

    page_query_rows = _load_csv(page_query_csv)
    query_page_opportunities, cannibalisation = _combined_page_query_analysis(page_query_rows)
    page_opportunities = _page_opportunities(page_rows)
    ga4 = _ga4_summary(_load_csv(ga4_csv)) if ga4_csv else {}
    incident = _incident_status(complete)

    summary = {
        "source": str(gsc_zip),
        "export_date": str(export_day),
        "complete_day_cutoff": str(cutoff),
        "excluded_preliminary_days": [str(row["date"]) for row in preliminary],
        "all_exported": all_period.to_dict(),
        "latest_complete_7_days": latest7.to_dict(),
        "previous_complete_7_days": prior7.to_dict(),
        "latest_complete_28_days": latest28.to_dict(),
        "previous_complete_28_days": prior28.to_dict(),
        "changes": {
            "weekly_clicks": _change(latest7.clicks, prior7.clicks),
            "weekly_impressions": _change(latest7.impressions, prior7.impressions),
            "weekly_ctr": _change(latest7.ctr, prior7.ctr),
            "28d_clicks": _change(latest28.clicks, prior28.clicks),
            "28d_impressions": _change(latest28.impressions, prior28.impressions),
            "28d_ctr": _change(latest28.ctr, prior28.ctr),
        },
        "uk": uk,
        "countries": countries,
        "devices": devices,
        "query_privacy": {
            "visible_query_clicks": query_clicks,
            "all_clicks": all_period.clicks,
            "visible_click_share": round(query_clicks / all_period.clicks, 5) if all_period.clicks else 0,
            "visible_query_impressions": query_impressions,
            "note": "Do not use the visible query table alone for traffic totals; anonymised queries are omitted.",
        },
        "incident": incident,
        "ga4_uk_organic": ga4,
        "page_opportunity_count": len(page_opportunities),
        "page_query_opportunity_count": len(query_page_opportunities),
        "cannibalisation_group_count": len(cannibalisation),
        "ctr_test_paths": list(CTR_TEST_TARGETS),
        "indexation_manifest": str(INDEXATION_MANIFEST_CSV),
    }

    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    _write_csv(output_dir / "page-opportunities.csv", page_opportunities)
    _write_csv(output_dir / "page-query-opportunities.csv", query_page_opportunities)
    _write_csv(output_dir / "cannibalisation-groups.csv", cannibalisation)

    preliminary_note = (
        ", ".join(summary["excluded_preliminary_days"])
        if summary["excluded_preliminary_days"]
        else "none"
    )
    report = f"""# Qualified Organic Growth Report

Generated from `{gsc_zip.name}`. Export date: {export_day}. Complete-day cutoff: {cutoff}.

## Executive read

- Incident status: **{'ALERT' if incident['alert'] else 'no incident'}**.
- Preliminary rows excluded: {preliminary_note}.
- Latest complete week: **{latest7.clicks:,} clicks**, **{latest7.impressions:,} impressions**, **{latest7.ctr:.2%} CTR**, position **{latest7.position:.2f}**.
- Week-on-week: clicks {_pct(summary['changes']['weekly_clicks'])}, impressions {_pct(summary['changes']['weekly_impressions'])}, CTR {_pct(summary['changes']['weekly_ctr'])}.
- Latest complete 28 days: **{latest28.clicks:,} clicks**, {_pct(summary['changes']['28d_clicks'])} versus the prior 28 days.
- UK: **{int(uk.get('clicks', 0)):,} clicks** from **{int(uk.get('impressions', 0)):,} impressions** at **{float(uk.get('ctr', 0)):.2%} CTR**.
- Visible query rows account for only **{query_clicks:,}/{all_period.clicks:,} clicks ({summary['query_privacy']['visible_click_share']:.1%})**; use page-query API data before consolidation decisions.

## Opportunity queues

- Page-level CTR/ranking candidates: **{len(page_opportunities)}**.
- UK page-query candidates: **{len(query_page_opportunities)}**.
- Cannibalisation groups with two or more material pages: **{len(cannibalisation)}**.
- First CTR cohort: {', '.join(CTR_TEST_TARGETS)}.

## Decision rules

- Ignore the newest {INDEXATION_POLICY['fresh_data_hours']} hours.
- Alert only after {incident['rule']}.
- Do not noindex a bridge or generated route until two complete 28-day evidence windows and page-query-country mapping confirm the owner.
- Revert a CTR test after 28 complete days if normalised clicks decline more than {INDEXATION_POLICY['ctr_test_revert_click_drop']:.0%} while position is stable.

## Data gaps

- Add a Search Console API page-query-country-device export to populate owner and cannibalisation decisions.
- Add a GA4 landing-page export to report UK organic users, engaged sessions and planning enquiries.
"""
    (output_dir / "qualified-organic-growth-report.md").write_text(report, encoding="utf-8")
    return summary


def main() -> None:
    parser = argparse.ArgumentParser(description="Create the repeatable qualified-organic GSC/GA4 growth report.")
    parser.add_argument("gsc_zip", type=Path, help="Search Console Performance-on-Search ZIP export")
    parser.add_argument("--as-of", help="Export date override in YYYY-MM-DD format")
    parser.add_argument("--page-query-csv", type=Path, help="Optional Search Console API page-query-country-device CSV")
    parser.add_argument("--ga4-csv", type=Path, help="Optional GA4 UK organic landing-page export")
    parser.add_argument("--output-dir", type=Path, help="Output directory")
    args = parser.parse_args()
    export_day = _export_date(args.gsc_zip, args.as_of)
    output_dir = args.output_dir or ROOT / "artifacts" / "growth" / str(export_day)
    summary = build_report(
        args.gsc_zip,
        output_dir,
        as_of=args.as_of,
        page_query_csv=args.page_query_csv,
        ga4_csv=args.ga4_csv,
    )
    print(f"Qualified organic growth report written to {output_dir}")
    print(f"Incident alert: {summary['incident']['alert']}")


if __name__ == "__main__":
    main()
