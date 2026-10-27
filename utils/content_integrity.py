from __future__ import annotations

from dataclasses import dataclass
from hashlib import blake2b
from html import unescape
import re


PROJECT_FINGERPRINTS = {
    "garden-rooms": ("garden room", "incidental secondary building", "outbuilding use"),
    "dropped-kerbs": ("dropped kerb", "vehicle crossing", "new vehicular access"),
    "extensions": ("rear extension", "extension depth", "original rear wall"),
    "hmos": ("hmo", "house in multiple occupation", "use class c4"),
    "trees": ("tree preservation order", "tpo"),
}
GENERIC_FAMILIES = {"national_guide", "rule_guide", "authority_profile", "local_rule"}
ENGLAND_ONLY_MARKERS = (
    "class a of part 1 of schedule 2",
    "general permitted development order 2015",
    "prior approval under the gpdo",
)
PLACEHOLDER_MARKERS = (
    "demo-ready",
    "placeholder advertisement",
    "connect this form",
    "fake partner",
    "partner placement",
)
NAVIGATION_REGION = re.compile(
    r"<(?P<tag>[a-z0-9]+)[^>]*data-purpose=[\"'](?:project-navigation|labelled-example)[\"'][^>]*>.*?</(?P=tag)>",
    re.IGNORECASE | re.DOTALL,
)
TAG_PATTERN = re.compile(r"<[^>]+>")


@dataclass(frozen=True)
class IntegrityFinding:
    code: str
    message: str
    severity: str = "error"

    def to_dict(self) -> dict[str, str]:
        return {"code": self.code, "message": self.message, "severity": self.severity}


def visible_text(html: str) -> str:
    without_script = re.sub(r"<(script|style)\b.*?</\1>", " ", html or "", flags=re.IGNORECASE | re.DOTALL)
    return " ".join(unescape(TAG_PATTERN.sub(" ", without_script)).split())


def _semantic_body(html: str) -> str:
    source = html or ""
    if "data-purpose=" in source.lower():
        source = NAVIGATION_REGION.sub(" ", source)
    return visible_text(source).lower()


def _contains_fingerprint(text: str, fingerprint: str) -> bool:
    """Match semantic phrases on token boundaries, avoiding place-name substrings."""
    return bool(re.search(rf"(?<![a-z0-9]){re.escape(fingerprint)}(?![a-z0-9])", text))


def lint_page_record(record: dict) -> list[IntegrityFinding]:
    findings: list[IntegrityFinding] = []
    family = record.get("page_family")
    if family in GENERIC_FAMILIES and record.get("project_id"):
        findings.append(IntegrityFinding("generic-project-assumption", "Generic page record carries a project ID."))
    if family == "authority_profile" and record.get("rule_id"):
        findings.append(IntegrityFinding("authority-rule-assumption", "Authority profile carries a selected rule."))
    if record.get("index_status") == "index" and record.get("review_status") == "draft":
        findings.append(IntegrityFinding("draft-indexable", "Draft records cannot be indexable."))
    return findings


def lint_rendered_html(record: dict, html: str) -> list[IntegrityFinding]:
    findings = lint_page_record(record)
    text = _semantic_body(html)
    family = record.get("page_family")
    project_id = record.get("project_id")
    rule_id = record.get("rule_id")

    scan_generic_project_language = family in {"rule_guide", "authority_profile", "local_rule"} or (
        family == "national_guide" and bool(record.get("rule_id"))
    )
    if scan_generic_project_language:
        allowed = {project_id} if project_id else set()
        for topic, fingerprints in PROJECT_FINGERPRINTS.items():
            if topic == "trees":
                continue
            if topic in allowed:
                continue
            matched = [fingerprint for fingerprint in fingerprints if _contains_fingerprint(text, fingerprint)]
            if matched:
                findings.append(
                    IntegrityFinding(
                        "cross-family-project-language",
                        f"Generic {family} contains unlabelled {topic} language: {', '.join(matched)}.",
                    )
                )
    if rule_id == "article-4" and not project_id:
        for marker in PROJECT_FINGERPRINTS["garden-rooms"]:
            if _contains_fingerprint(text, marker):
                findings.append(IntegrityFinding("article4-garden-room-leak", f"Generic Article 4 page contains {marker!r}."))
    if family in {"national_guide", "rule_guide", "authority_profile", "local_rule"} and "assumed setup" in text:
        findings.append(IntegrityFinding("generic-assumed-setup", "Generic page contains an assumed project setup."))
    if record.get("jurisdiction") in {"wales", "scotland", "northern-ireland"}:
        for marker in ENGLAND_ONLY_MARKERS:
            if marker in text and "england" not in text[max(0, text.find(marker) - 120): text.find(marker) + len(marker) + 120]:
                findings.append(IntegrityFinding("jurisdiction-leak", f"Unqualified England-only marker: {marker}."))
    for marker in PLACEHOLDER_MARKERS:
        if marker in text:
            findings.append(IntegrityFinding("live-placeholder", f"Live placeholder marker found: {marker}."))
    return findings


def simhash64(text: str) -> int:
    words = re.findall(r"[a-z0-9]+", text.lower())
    shingle_count = max(1, len(words) - 4)
    if shingle_count <= 64:
        indices = range(shingle_count)
    else:
        indices = [round(index * (shingle_count - 1) / 63) for index in range(64)]
    vector = [0] * 64
    for index in indices:
        shingle = " ".join(words[index:index + 5])
        digest = int.from_bytes(blake2b(shingle.encode("utf-8"), digest_size=8).digest(), "big")
        for bit in range(64):
            vector[bit] += 1 if digest & (1 << bit) else -1
    result = 0
    for bit, value in enumerate(vector):
        if value >= 0:
            result |= 1 << bit
    return result


def simhash_similarity(left: int, right: int) -> float:
    return 1.0 - ((left ^ right).bit_count() / 64.0)
