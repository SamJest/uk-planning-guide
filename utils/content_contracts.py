from __future__ import annotations

from datetime import date
from functools import lru_cache
import json
from pathlib import Path
import re
from urllib.parse import urlparse

from core.paths import BASE_URL, ROOT


PAGE_RECORDS_PATH = ROOT / "data" / "canary" / "page-records.json"
SOURCE_REGISTRY_PATH = ROOT / "data" / "source-registry.json"
REDIRECTS_PATH = ROOT / "data" / "canary" / "redirects.json"
ROUTES_PATH = ROOT / "data" / "canary" / "routes.json"

PAGE_FAMILIES = {
    "national_guide",
    "project_guide",
    "rule_guide",
    "authority_profile",
    "local_project",
    "local_rule",
    "tool",
    "workflow",
    "news",
    "data_report",
}
JURISDICTIONS = {"england", "wales", "scotland", "northern-ireland", "uk"}
REVIEW_STATUSES = {"draft", "source_checked", "editor_checked", "published"}
INDEX_STATUSES = {"noindex", "index"}
CONFIDENCE_LEVELS = {"low", "medium", "high"}
LOCAL_FAMILIES = {"authority_profile", "local_project", "local_rule"}
IDENTIFIER_PATTERN = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*")


class ContractError(ValueError):
    """Raised when a content record violates the Phase 0 contract."""


def normalize_path(value: str) -> str:
    clean = str(value or "").strip()
    if clean.startswith(("http://", "https://")):
        clean = urlparse(clean).path
    clean = clean.split("?", 1)[0].split("#", 1)[0]
    if not clean.startswith("/"):
        clean = "/" + clean
    clean = clean.rstrip("/")
    return clean + "/" if clean else "/"


def absolute_url(path: str) -> str:
    return BASE_URL.rstrip("/") + normalize_path(path)


def _load_json(path: Path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise ContractError(f"Missing contract file: {path.relative_to(ROOT)}") from exc
    except json.JSONDecodeError as exc:
        raise ContractError(f"Invalid JSON in {path.relative_to(ROOT)}: {exc}") from exc


def _require_iso_date(value, label: str, *, nullable: bool = False) -> None:
    if value is None and nullable:
        return
    if not isinstance(value, str):
        raise ContractError(f"{label} must be an ISO date")
    try:
        date.fromisoformat(value)
    except ValueError as exc:
        raise ContractError(f"{label} must be an ISO date, got {value!r}") from exc


def _require_keys(record: dict, keys: set[str], label: str) -> None:
    missing = sorted(keys - set(record))
    if missing:
        raise ContractError(f"{label} is missing required fields: {', '.join(missing)}")


def validate_page_record(record: dict) -> None:
    required = {
        "route_path",
        "canonical_path",
        "page_family",
        "jurisdiction",
        "authority_id",
        "project_id",
        "rule_id",
        "source_ids",
        "claims",
        "verified_at",
        "content_updated_at",
        "review_status",
        "index_status",
        "confidence",
        "unique_local_facts",
    }
    _require_keys(record, required, "Page record")
    route = normalize_path(record["route_path"])
    canonical = normalize_path(record["canonical_path"])
    if record["route_path"] != route or record["canonical_path"] != canonical:
        raise ContractError(f"Page paths must be normalized with trailing slashes: {route}")
    if record["page_family"] not in PAGE_FAMILIES:
        raise ContractError(f"Unsupported page family on {route}: {record['page_family']!r}")
    if record["jurisdiction"] not in JURISDICTIONS:
        raise ContractError(f"Unsupported jurisdiction on {route}: {record['jurisdiction']!r}")
    if record["review_status"] not in REVIEW_STATUSES:
        raise ContractError(f"Unsupported review status on {route}")
    if record["index_status"] not in INDEX_STATUSES:
        raise ContractError(f"Unsupported index status on {route}")
    if record["confidence"] not in CONFIDENCE_LEVELS:
        raise ContractError(f"Unsupported confidence on {route}")
    _require_iso_date(record["verified_at"], f"{route} verified_at", nullable=True)
    _require_iso_date(record["content_updated_at"], f"{route} content_updated_at")

    for field in ("authority_id", "project_id", "rule_id"):
        if record[field] is not None and not isinstance(record[field], str):
            raise ContractError(f"{route} {field} must be a string or null")
        if isinstance(record[field], str) and not IDENTIFIER_PATTERN.fullmatch(record[field]):
            raise ContractError(f"{route} {field} must contain one normalized identifier")
    for field in ("source_ids", "claims", "unique_local_facts"):
        if not isinstance(record[field], list):
            raise ContractError(f"{route} {field} must be a list")
    if len(record["source_ids"]) != len(set(record["source_ids"])):
        raise ContractError(f"{route} contains duplicate source IDs")

    if record["page_family"] == "authority_profile" and record["project_id"] is not None:
        raise ContractError(f"Generic authority profile cannot carry a project ID: {route}")
    if record["page_family"] in {"national_guide", "rule_guide", "authority_profile", "local_rule"} and record["project_id"] is not None:
        raise ContractError(f"Generic rule/authority record cannot assume a project: {route}")
    if record["page_family"] in LOCAL_FAMILIES and not record["authority_id"]:
        raise ContractError(f"Local page requires authority_id: {route}")
    if record["page_family"] in LOCAL_FAMILIES and route.strip("/").split("/")[-1] != record["authority_id"]:
        raise ContractError(f"Local page route must end with its single authority_id: {route}")
    if record["page_family"] == "authority_profile" and record["rule_id"] is not None:
        raise ContractError(f"Authority profile cannot carry a selected rule: {route}")
    if record["page_family"] == "local_project" and not record["project_id"]:
        raise ContractError(f"Local project requires project_id: {route}")
    if record["page_family"] == "local_rule" and not record["rule_id"]:
        raise ContractError(f"Local rule requires rule_id: {route}")

    known_claim_ids: set[str] = set()
    for claim in record["claims"]:
        if not isinstance(claim, dict):
            raise ContractError(f"{route} claim must be an object")
        _require_keys(claim, {"claim_id", "text", "source_ids"}, f"Claim on {route}")
        if not claim["claim_id"] or claim["claim_id"] in known_claim_ids:
            raise ContractError(f"{route} has an empty or duplicate claim_id")
        known_claim_ids.add(claim["claim_id"])
        if not str(claim["text"]).strip() or not claim["source_ids"]:
            raise ContractError(f"{route} claim {claim['claim_id']} needs text and sources")
        if not set(claim["source_ids"]).issubset(set(record["source_ids"])):
            raise ContractError(f"{route} claim {claim['claim_id']} references undeclared sources")

    for fact in record["unique_local_facts"]:
        if not isinstance(fact, dict):
            raise ContractError(f"{route} local fact must be an object")
        _require_keys(fact, {"fact", "source_ids"}, f"Local fact on {route}")
        if not str(fact["fact"]).strip() or not fact["source_ids"]:
            raise ContractError(f"{route} local facts need text and sources")
        if not set(fact["source_ids"]).issubset(set(record["source_ids"])):
            raise ContractError(f"{route} local fact references undeclared sources")


@lru_cache(maxsize=1)
def load_page_records() -> tuple[dict, ...]:
    payload = _load_json(PAGE_RECORDS_PATH)
    if not isinstance(payload, list):
        raise ContractError("data/canary/page-records.json must contain a list")
    seen: set[str] = set()
    for record in payload:
        if not isinstance(record, dict):
            raise ContractError("Every page record must be an object")
        validate_page_record(record)
        route = record["route_path"]
        if route in seen:
            raise ContractError(f"Duplicate page route: {route}")
        seen.add(route)
    return tuple(payload)


@lru_cache(maxsize=1)
def page_records_by_route() -> dict[str, dict]:
    return {record["route_path"]: record for record in load_page_records()}


def page_record_for_path(path: str) -> dict | None:
    clean = normalize_path(path)
    direct = page_records_by_route().get(clean)
    if direct:
        return direct
    try:
        from utils.route_contracts import route_contract_for_legacy_path

        contract = route_contract_for_legacy_path(clean)
    except (ImportError, ValueError):
        contract = None
    return page_records_by_route().get(contract.canonical_path) if contract else None


def page_record_for_url(url: str) -> dict | None:
    return page_record_for_path(urlparse(str(url or "")).path or "/")


def render_record_for_path(path: str) -> dict | None:
    clean = normalize_path(path)
    direct = page_records_by_route().get(clean)
    if direct and direct["canonical_path"] != clean:
        return page_records_by_route().get(direct["canonical_path"]) or direct
    return page_record_for_path(clean)


def render_record_for_url(url: str) -> dict | None:
    return render_record_for_path(urlparse(str(url or "")).path or "/")


def clear_contract_caches() -> None:
    load_page_records.cache_clear()
    page_records_by_route.cache_clear()
