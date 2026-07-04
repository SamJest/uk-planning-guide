import json

from utils.local_note_validation import is_planning_local_note, normalize_local_note


SCENARIO_RULE_MAP = {
    "planning-permission": "permitted_development",
    "permitted-development": "permitted_development",
    "height-limits": "height_rules",
    "maximum-height": "height_rules",
    "depth-limits": "depth_rules",
    "boundary-rules": "boundary_rules",
    "distance-from-boundary": "boundary_rules",
    "roof-alterations": "roof_rules",
}

RESTRICTION_FIELD_MAP = {
    "Conservation areas": "conservation_area",
    "Listed buildings": "listed_building",
    "Article 4 directions": "article4_notes",
}

WEAK_LOCAL_RULE_MARKERS = (
    "most householder development follows national permitted development rules",
    "householder development follows national permitted development rules",
    "development must comply with national permitted development",
    "extensions must comply with national permitted development",
    "roof alterations must comply with national permitted development",
    "development near boundaries must follow national permitted development rules",
    "materials should be similar in appearance",
)

WEAK_RESTRICTION_MARKERS = (
    "additional planning restrictions may apply in conservation areas",
    "listed building consent is required for works affecting listed buildings",
    "article 4 directions may remove permitted development rights in some locations",
)


def _dedupe_text_items(items):
    cleaned = []
    seen = set()

    for item in items:
        text = normalize_local_note(item)
        if not text:
            continue
        key = text.lower().rstrip(".")
        if key in seen:
            continue
        seen.add(key)
        cleaned.append(text)

    return cleaned


def is_meaningful_local_rule_signal(text: str, field_key: str = "") -> bool:
    clean = normalize_local_note(text)
    if not clean or not is_planning_local_note(clean, field_key):
        return False

    lowered = clean.lower()
    if any(marker in lowered for marker in WEAK_LOCAL_RULE_MARKERS):
        return False

    return True


def is_meaningful_local_restriction(label: str, text: str) -> bool:
    clean = normalize_local_note(text)
    field_key = RESTRICTION_FIELD_MAP.get(label, "")
    if not clean or not is_planning_local_note(clean, field_key):
        return False

    lowered = clean.lower()
    if any(marker in lowered for marker in WEAK_RESTRICTION_MARKERS):
        return False

    return True


def useful_local_rule_items(rule, keys=("height_rules", "boundary_rules", "roof_rules"), limit_per_key: int = 1):
    items = []

    for key in keys:
        for text in excerpt_text((rule or {}).get("rules", {}).get(key, ""), limit=limit_per_key):
            if is_meaningful_local_rule_signal(text, key):
                items.append(text)

    return _dedupe_text_items(items)


def useful_local_restrictions(rule):
    items = []

    for label, text in restriction_messages(rule):
        if is_meaningful_local_restriction(label, text):
            items.append((label, normalize_local_note(text)))

    deduped = []
    seen = set()
    for label, text in items:
        key = (label.lower(), text.lower().rstrip("."))
        if key in seen:
            continue
        seen.add(key)
        deduped.append((label, text))

    return deduped

def _is_clean_excerpt(text: str) -> bool:
    return is_planning_local_note(text)


def first_text(value, fallback=""):
    if isinstance(value, list):
        for item in value:
            text = str(item).strip()
            if text:
                return text
        return fallback

    text = str(value or "").strip()
    return text or fallback


def excerpt_text(value, limit=2):
    if isinstance(value, list):
        items = [str(item).strip() for item in value if str(item).strip()]
        return items[:limit]

    text = str(value or "").strip()
    return [text] if text else []


def restriction_messages(rule):
    restrictions = (rule or {}).get("restrictions", {})
    messages = []

    conservation = str(restrictions.get("conservation_area", "")).strip()
    listed = str(restrictions.get("listed_building", "")).strip()
    article4_note = str(restrictions.get("article4_notes", "")).strip()
    article4_applies = bool(restrictions.get("article4_applies"))

    if conservation:
        messages.append(("Conservation areas", conservation))
    if listed:
        messages.append(("Listed buildings", listed))
    if article4_applies or article4_note:
        note = article4_note or "Article 4 directions may remove permitted development rights in some locations."
        messages.append(("Article 4 directions", note))

    return messages


def scenario_rule_excerpt(rule, scenario_slug):
    if not isinstance(rule, dict):
        return ""

    if scenario_slug == "conservation-areas":
        text = first_text(rule.get("restrictions", {}).get("conservation_area", ""))
        return text if _is_clean_excerpt(text) else ""
    if scenario_slug == "listed-buildings":
        text = first_text(rule.get("restrictions", {}).get("listed_building", ""))
        return text if _is_clean_excerpt(text) else ""
    if scenario_slug == "article-4":
        restrictions = rule.get("restrictions", {})
        if restrictions.get("article4_applies") or restrictions.get("article4_notes"):
            text = first_text(restrictions.get("article4_notes", ""))
            if _is_clean_excerpt(text):
                return text
            return "Article 4 directions can remove permitted development rights, so the council may expect a formal planning application."
        return ""

    key = SCENARIO_RULE_MAP.get(scenario_slug)
    if key == "permitted_development":
        text = first_text(rule.get("permitted_development", ""))
        return text if _is_clean_excerpt(text) else ""
    if key:
        text = first_text(rule.get("rules", {}).get(key, ""))
        return text if _is_clean_excerpt(text) else ""
    return ""


def faq_schema(faqs):
    payload = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {
                "@type": "Question",
                "name": question,
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": answer,
                },
            }
            for question, answer in faqs
        ],
    }
    return json.dumps(payload)
