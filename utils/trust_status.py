"""One trust model for contract records and legacy page components."""
from dataclasses import dataclass


@dataclass(frozen=True)
class TrustStatus:
    verification: str
    confidence: str | None


def trust_status(record):
    verified = bool(record.get("verified_at") and record.get("source_ids"))
    historical = verified and record.get('evidence_version') != 1
    if record.get('evidence_version') == 1:
        from utils.claim_evidence import validate_record_evidence
        from utils.source_registry import source_registry_by_id
        validate_record_evidence(record, source_registry_by_id())
        assertions = record.get('claims', []) + record.get('unique_local_facts', [])
        verified = bool(verified and assertions and all(a['evidence_status'] == 'verified' for a in assertions))
    route = str(record.get("route_path", ""))
    utility = (record.get("page_family") in {"tool", "workflow", "home", "utility"}
               or route in {"/downloads/", "/about/", "/methodology/", "/editorial-policy/", "/privacy/"}
               or route.startswith("/downloads/"))
    confidence = None if utility else (record.get("confidence", "low") if verified and not historical else "not assessed")
    return TrustStatus("historical" if historical else "verified" if verified else "unverified", confidence)


def validate_trust_status(record):
    state = trust_status(record)
    if record.get("confidence") == "high" and state.verification == "unverified":
        raise ValueError("High confidence requires a verified source set")
