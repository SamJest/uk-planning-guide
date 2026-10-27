from __future__ import annotations

from datetime import date
from functools import lru_cache
from urllib.parse import urlparse

from utils.content_contracts import (
    ContractError,
    LOCAL_FAMILIES,
    SOURCE_REGISTRY_PATH,
    _load_json,
    load_page_records,
)


SOURCE_STATUSES = {"active", "redirected", "unavailable", "unverified"}
SOURCE_TYPES = {
    "article_4",
    "local_plan",
    "validation_list",
    "pre_app",
    "fees",
    "application_search",
    "conservation_map",
    "committee",
    "national_legislation",
    "official_guidance",
    "design_guide",
    "highways",
    "planning_portal",
    "editorial_method",
}


def validate_source_record(record: dict) -> None:
    required = {
        "source_id",
        "authority_id",
        "jurisdiction",
        "source_type",
        "title",
        "url",
        "publisher",
        "last_checked_at",
        "status",
        "page_families",
    }
    missing = sorted(required - set(record))
    if missing:
        raise ContractError(f"Source record is missing fields: {', '.join(missing)}")
    source_id = str(record["source_id"] or "")
    if not source_id or source_id.strip("abcdefghijklmnopqrstuvwxyz0123456789-"):
        raise ContractError(f"Invalid source_id: {source_id!r}")
    if record["source_type"] not in SOURCE_TYPES:
        raise ContractError(f"Unsupported source type for {source_id}: {record['source_type']}")
    if record["status"] not in SOURCE_STATUSES:
        raise ContractError(f"Unsupported source status for {source_id}: {record['status']}")
    parsed = urlparse(str(record["url"] or ""))
    if parsed.scheme != "https" or not parsed.netloc:
        raise ContractError(f"Source {source_id} must use an absolute HTTPS URL")
    try:
        date.fromisoformat(str(record["last_checked_at"]))
    except ValueError as exc:
        raise ContractError(f"Source {source_id} has invalid last_checked_at") from exc
    if not str(record["title"]).strip() or not str(record["publisher"]).strip():
        raise ContractError(f"Source {source_id} needs a title and publisher")
    if not isinstance(record["page_families"], list) or not record["page_families"]:
        raise ContractError(f"Source {source_id} needs supported page families")


@lru_cache(maxsize=1)
def load_source_registry() -> tuple[dict, ...]:
    payload = _load_json(SOURCE_REGISTRY_PATH)
    if not isinstance(payload, list):
        raise ContractError("data/source-registry.json must contain a list")
    seen_ids: set[str] = set()
    seen_urls: dict[str, str] = {}
    for record in payload:
        validate_source_record(record)
        source_id = record["source_id"]
        normalized_url = record["url"].rstrip("/").lower()
        if source_id in seen_ids:
            raise ContractError(f"Duplicate source_id: {source_id}")
        if normalized_url in seen_urls:
            raise ContractError(f"Duplicate source URL on {source_id} and {seen_urls[normalized_url]}")
        seen_ids.add(source_id)
        seen_urls[normalized_url] = source_id
    return tuple(payload)


@lru_cache(maxsize=1)
def source_registry_by_id() -> dict[str, dict]:
    return {record["source_id"]: record for record in load_source_registry()}


def sources_for_page(record: dict, *, active_only: bool = False) -> list[dict]:
    registry = source_registry_by_id()
    sources = [registry[source_id] for source_id in record.get("source_ids", []) if source_id in registry]
    return [source for source in sources if source["status"] == "active"] if active_only else sources


def validate_page_source_links() -> None:
    registry = source_registry_by_id()
    for page in load_page_records():
        route = page["route_path"]
        missing = sorted(set(page["source_ids"]) - set(registry))
        if missing:
            raise ContractError(f"{route} references missing sources: {', '.join(missing)}")
        for source_id in page["source_ids"]:
            source = registry[source_id]
            if page["page_family"] not in source["page_families"]:
                raise ContractError(f"{source_id} does not support {page['page_family']} on {route}")
            if source["jurisdiction"] not in {page["jurisdiction"], "uk"}:
                raise ContractError(f"{source_id} has the wrong jurisdiction for {route}")
            if source["authority_id"] and page["authority_id"] != source["authority_id"] and page["page_family"] != "data_report":
                raise ContractError(f"{source_id} belongs to the wrong authority for {route}")

        if page["index_status"] == "index" and page["page_family"] in LOCAL_FAMILIES:
            active_local = {
                source["source_id"]
                for source in sources_for_page(page, active_only=True)
                if source["authority_id"] == page["authority_id"]
            }
            if len(active_local) < 3:
                raise ContractError(f"Indexable local page needs three active local sources: {route}")
            if len(page["unique_local_facts"]) < 5:
                raise ContractError(f"Indexable local page needs five local facts: {route}")


def clear_source_caches() -> None:
    load_source_registry.cache_clear()
    source_registry_by_id.cache_clear()
