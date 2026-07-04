from __future__ import annotations

from functools import lru_cache

from utils.content_contracts import (
    ContractError,
    REDIRECTS_PATH,
    ROUTES_PATH,
    _load_json,
    absolute_url,
    load_page_records,
    normalize_path,
)


@lru_cache(maxsize=1)
def load_canary_routes() -> dict[str, tuple[str, ...]]:
    payload = _load_json(ROUTES_PATH)
    if not isinstance(payload, dict):
        raise ContractError("data/canary/routes.json must contain an object")
    result = {}
    for key in ("publish_routes", "render_routes"):
        values = payload.get(key)
        if not isinstance(values, list):
            raise ContractError(f"Canary route manifest needs {key}")
        normalized = tuple(normalize_path(value) for value in values)
        if len(normalized) != len(set(normalized)):
            raise ContractError(f"Canary route manifest contains duplicate {key}")
        result[key] = normalized
    if not set(result["publish_routes"]).issubset(set(result["render_routes"])):
        raise ContractError("Every published canary route must also be rendered")
    return result


@lru_cache(maxsize=1)
def load_redirects() -> tuple[dict, ...]:
    payload = _load_json(REDIRECTS_PATH)
    if not isinstance(payload, list):
        raise ContractError("data/canary/redirects.json must contain a list")
    sources: set[str] = set()
    for record in payload:
        required = {"source_path", "target_path", "status_code", "reason"}
        if not isinstance(record, dict) or required - set(record):
            raise ContractError("Invalid redirect record")
        source = normalize_path(record["source_path"])
        target = normalize_path(record["target_path"])
        if source == target:
            raise ContractError(f"Self-redirect is not allowed: {source}")
        if source in sources:
            raise ContractError(f"Duplicate redirect source: {source}")
        if record["status_code"] not in {301, 308, 410}:
            raise ContractError(f"Unsupported redirect status on {source}")
        record["source_path"] = source
        record["target_path"] = target
        sources.add(source)
    targets = {record["target_path"] for record in payload if record["status_code"] != 410}
    chained = sources & targets
    if chained:
        raise ContractError(f"Redirect chains are not allowed: {', '.join(sorted(chained))}")
    return tuple(payload)


@lru_cache(maxsize=1)
def url_registry() -> dict[str, dict]:
    registry: dict[str, dict] = {}
    for record in load_page_records():
        registry[record["route_path"]] = {
            "route_path": record["route_path"],
            "canonical_path": record["canonical_path"],
            "canonical_url": absolute_url(record["canonical_path"]),
            "index_status": record["index_status"],
            "content_updated_at": record["content_updated_at"],
            "page_family": record["page_family"],
        }
    for redirect in load_redirects():
        if redirect["source_path"] not in registry:
            registry[redirect["source_path"]] = {
                "route_path": redirect["source_path"],
                "canonical_path": redirect["target_path"],
                "canonical_url": absolute_url(redirect["target_path"]),
                "index_status": "noindex",
                "content_updated_at": None,
                "page_family": "redirect",
            }
    return registry


def validate_url_registry() -> None:
    routes = load_canary_routes()
    records = {record["route_path"] for record in load_page_records()}
    missing = sorted(set(routes["publish_routes"]) - records)
    if missing:
        raise ContractError(f"Published canary routes without page records: {', '.join(missing)}")
    load_redirects()
    url_registry()


def clear_url_caches() -> None:
    load_canary_routes.cache_clear()
    load_redirects.cache_clear()
    url_registry.cache_clear()

