from __future__ import annotations

from dataclasses import asdict, dataclass
from functools import lru_cache
from pathlib import Path

from data.faq_data import FAQS
from data.loaders import load_councils, load_projects
from data.scenario_data import SCENARIOS
from data.tools_data import load_tools
from utils.country_utils import get_country_slug


BASE_URL = "https://ukplanningguide.co.uk"
COUNTRY_SLUGS = {"england", "scotland", "wales", "northern-ireland"}
INDEXABLE = "index"
NOINDEX = "noindex"
LEGACY_BRIDGE = "legacy-bridge"


@dataclass(frozen=True)
class RouteContract:
    country: str
    intent_type: str
    canonical_path: str
    legacy_paths: tuple[str, ...] = ()
    indexability: str = INDEXABLE
    project_slug: str = ""
    process_slug: str = ""
    rule_slug: str = ""
    authority_slug: str = ""
    source_path: str = ""

    @property
    def canonical_url(self) -> str:
        return BASE_URL.rstrip("/") + self.canonical_path

    def to_dict(self) -> dict[str, object]:
        payload = asdict(self)
        payload["canonical_url"] = self.canonical_url
        return payload


def normalize_path(path: str) -> str:
    clean = str(path or "").split("?", 1)[0].split("#", 1)[0].strip()
    if not clean:
        return "/"
    if not clean.startswith("/"):
        clean = "/" + clean
    clean = clean.rstrip("/")
    return clean + "/" if clean != "/" else "/"


def output_path_for_route(route_path: str, output_root: Path) -> Path:
    clean = normalize_path(route_path).strip("/")
    if not clean:
        return output_root / "index.html"
    return output_root / clean / "index.html"


@lru_cache(maxsize=1)
def project_slugs() -> frozenset[str]:
    return frozenset(project["slug"] for project in load_projects() if project.get("slug"))


@lru_cache(maxsize=1)
def scenario_slugs() -> frozenset[str]:
    return frozenset(scenario["slug"] for scenario in SCENARIOS if scenario.get("slug"))


@lru_cache(maxsize=1)
def tool_slugs() -> frozenset[str]:
    return frozenset(tool["slug"] for tool in load_tools() if tool.get("slug"))


@lru_cache(maxsize=1)
def faq_process_map() -> dict[str, str]:
    known = {
        "lawful-development-certificate": "lawful-development-certificates",
        "lawful-development-certificate-vs-planning-permission": "lawful-development-certificates",
        "prior-approval-vs-planning-permission": "prior-approval-vs-planning-permission",
        "is-pre-application-advice-worth-it": "pre-application-advice",
        "what-happens-if-planning-permission-is-refused": "planning-refused-and-appeals",
        "what-happens-after-planning-permission-is-approved": "after-planning-approval",
    }
    faq_slugs = {faq["slug"] for faq in FAQS if faq.get("slug")}
    return {key: value for key, value in known.items() if key in faq_slugs}


@lru_cache(maxsize=1)
def authority_lookup() -> dict[str, dict[str, str]]:
    lookup: dict[str, dict[str, str]] = {}
    for county_slug, councils in load_councils().items():
        country = get_country_slug(county_slug)
        for council in councils:
            town_slug = council.get("town_slug")
            if not town_slug:
                continue
            lookup[town_slug] = {
                "country": council.get("country_slug") or country,
                "county_slug": county_slug,
                "town_name": council.get("town_name", town_slug.replace("-", " ").title()),
            }
    return lookup


def country_for_county(county_slug: str) -> str:
    return get_country_slug(county_slug)


def country_for_authority(authority_slug: str, fallback_county_slug: str = "") -> str:
    authority = authority_lookup().get(str(authority_slug or "").strip())
    if authority:
        return authority["country"]
    return country_for_county(fallback_county_slug) if fallback_county_slug else "england"


def route_contract_for_legacy_path(path: str) -> RouteContract | None:
    clean = normalize_path(path)
    parts = [part for part in clean.strip("/").split("/") if part]
    if not parts:
        return None
    if parts[0] in COUNTRY_SLUGS:
        return None

    first = parts[0]
    if first == "tools":
        suffix = "/".join(parts[1:])
        canonical = "/england/tools/" + (suffix + "/" if suffix else "")
        return RouteContract(
            country="england",
            intent_type="tools",
            canonical_path=canonical,
            legacy_paths=(clean,),
            source_path=clean,
        )

    if first == "councils":
        if len(parts) == 1:
            return RouteContract("england", "councils", "/england/councils/", (clean,), source_path=clean)
        authority = parts[1]
        country = country_for_authority(authority)
        return RouteContract(
            country=country,
            intent_type="councils",
            canonical_path=f"/{country}/councils/{authority}/",
            legacy_paths=(clean,),
            authority_slug=authority,
            source_path=clean,
        )

    process_map = faq_process_map()
    if first == "planning-faq" and len(parts) >= 2 and parts[1] in process_map:
        process = process_map[parts[1]]
        return RouteContract(
            country="england",
            intent_type="process",
            canonical_path=f"/england/process/{process}/",
            legacy_paths=(clean,),
            process_slug=process,
            source_path=clean,
        )

    if first == "building-regulations":
        suffix = "/".join(parts[1:])
        canonical = "/england/process/building-regulations/" + (suffix + "/" if suffix else "")
        return RouteContract(
            country="england",
            intent_type="process",
            canonical_path=canonical,
            legacy_paths=(clean,),
            process_slug="building-regulations",
            source_path=clean,
        )

    if first in scenario_slugs():
        if len(parts) == 1:
            return RouteContract(
                country="england",
                intent_type="rules",
                canonical_path=f"/england/rules/{first}/",
                legacy_paths=(clean,),
                rule_slug=first,
                source_path=clean,
            )
        authority = parts[1]
        country = country_for_authority(authority)
        return RouteContract(
            country=country,
            intent_type="rules",
            canonical_path=f"/{country}/rules/{first}/{authority}/",
            legacy_paths=(clean,),
            rule_slug=first,
            authority_slug=authority,
            source_path=clean,
        )

    if first in project_slugs():
        project = first
        if len(parts) == 1:
            return RouteContract(
                country="england",
                intent_type="projects",
                canonical_path=f"/england/projects/{project}/",
                legacy_paths=(clean,),
                project_slug=project,
                source_path=clean,
            )
        county = parts[1]
        country = country_for_county(county)
        if len(parts) == 2:
            return RouteContract(
                country=country,
                intent_type="projects",
                canonical_path=f"/{country}/projects/{project}/{county}/",
                legacy_paths=(clean,),
                project_slug=project,
                source_path=clean,
            )
        authority = parts[2]
        if len(parts) == 3:
            return RouteContract(
                country=country,
                intent_type="projects",
                canonical_path=f"/{country}/projects/{project}/{authority}/",
                legacy_paths=(clean,),
                project_slug=project,
                authority_slug=authority,
                source_path=clean,
            )
        rule = parts[3]
        return RouteContract(
            country=country,
            intent_type="projects",
            canonical_path=f"/{country}/projects/{project}/{authority}/{rule}/",
            legacy_paths=(clean,),
            project_slug=project,
            rule_slug=rule if rule in scenario_slugs() else "",
            authority_slug=authority,
            source_path=clean,
        )

    return None


def is_legacy_country_bridge_path(path: str) -> bool:
    contract = route_contract_for_legacy_path(path)
    return bool(contract and contract.canonical_path != normalize_path(path))


def route_contract_for_country_path(path: str) -> RouteContract | None:
    clean = normalize_path(path)
    parts = [part for part in clean.strip("/").split("/") if part]
    if len(parts) < 2 or parts[0] not in COUNTRY_SLUGS:
        return None
    country = parts[0]
    intent = parts[1]
    payload = {
        "country": country,
        "intent_type": intent,
        "canonical_path": clean,
        "source_path": clean,
    }
    if intent == "projects" and len(parts) >= 3:
        payload["project_slug"] = parts[2]
        if len(parts) >= 4:
            payload["authority_slug"] = parts[3]
        if len(parts) >= 5:
            payload["rule_slug"] = parts[4]
    elif intent == "process" and len(parts) >= 3:
        payload["process_slug"] = parts[2]
    elif intent == "rules" and len(parts) >= 3:
        payload["rule_slug"] = parts[2]
        if len(parts) >= 4:
            payload["authority_slug"] = parts[3]
    elif intent == "councils" and len(parts) >= 3:
        payload["authority_slug"] = parts[2]
    return RouteContract(**payload)


def route_contract_for_path(path: str) -> RouteContract | None:
    return route_contract_for_country_path(path) or route_contract_for_legacy_path(path)
