from __future__ import annotations

from dataclasses import dataclass
from datetime import date
import hashlib
import json
from pathlib import Path
from typing import Iterable

from core.paths import ROOT


CONFIG_PATH = ROOT / "data" / "monetisation-config.json"
PARTNER_PATH = ROOT / "data" / "partner-registry.json"


@dataclass(frozen=True)
class MonetisationContext:
    route: str
    page_family: str
    jurisdiction: str
    project_type: str | None = None
    quality_pass: bool = False
    indexable: bool = False
    consent_ready: bool = False
    sensitive_state: bool = False
    purchased_experience: bool = False


@dataclass(frozen=True)
class EligibilityDecision:
    eligible: bool
    reasons: tuple[str, ...]


def _load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def monetisation_config() -> dict:
    return _load(CONFIG_PATH)


def ad_eligibility(context: MonetisationContext, config: dict | None = None) -> EligibilityDecision:
    config = config or monetisation_config()
    ads = config.get("ads", {})
    reasons: list[str] = []
    if not config.get("global_enabled"):
        reasons.append("global_disabled")
    if not ads.get("enabled"):
        reasons.append("ads_disabled")
    if not config.get("consent_ready") or not context.consent_ready:
        reasons.append("consent_not_ready")
    if not context.quality_pass:
        reasons.append("quality_not_approved")
    if not context.indexable:
        reasons.append("not_indexable")
    if context.page_family not in set(ads.get("allowed_page_families", [])):
        reasons.append("template_not_allowed")
    if context.page_family in set(ads.get("excluded_page_families", [])):
        reasons.append("template_excluded")
    if any(context.route.startswith(prefix) for prefix in ads.get("excluded_path_prefixes", [])):
        reasons.append("path_excluded")
    if context.sensitive_state:
        reasons.append("sensitive_state")
    if context.purchased_experience:
        reasons.append("purchased_experience")
    if not ads.get("provider") or int(ads.get("rollout_percent", 0)) <= 0:
        reasons.append("provider_or_rollout_missing")
    return EligibilityDecision(not reasons, tuple(reasons))


def _in_window(partner: dict, today: date) -> bool:
    try:
        return date.fromisoformat(partner["active_from"]) <= today <= date.fromisoformat(partner["expires_at"])
    except (KeyError, TypeError, ValueError):
        return False


def select_partner(
    context: MonetisationContext,
    *,
    category: str,
    config: dict | None = None,
    registry: dict | None = None,
    today: date | None = None,
) -> dict | None:
    config = config or monetisation_config()
    referrals = config.get("referrals", {})
    if not config.get("global_enabled") or not referrals.get("enabled"):
        return None
    if not context.quality_pass or not context.indexable or not context.consent_ready:
        return None
    if context.sensitive_state or context.purchased_experience:
        return None
    registry = registry or _load(PARTNER_PATH)
    today = today or date.today()
    candidates: Iterable[dict] = registry.get("partners", [])
    candidates = (
        partner
        for partner in candidates
        if partner.get("category") == category
        and partner.get("owner_approved") is True
        and _in_window(partner, today)
        and context.jurisdiction in set(partner.get("jurisdictions", []))
        and (not context.project_type or context.project_type in set(partner.get("project_types", [])))
        and partner.get("disclosure_text")
        and partner.get("url_template")
    )
    ordered = sorted(candidates, key=lambda item: (-int(item.get("priority", 0)), item["partner_id"]))
    return ordered[0] if ordered else None


def rollout_bucket(route: str, surface: str) -> int:
    digest = hashlib.sha256(f"{surface}|{route}".encode("utf-8")).digest()
    return int.from_bytes(digest[:4], "big") % 100
