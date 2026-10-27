from __future__ import annotations

from utils.text_cleaning import clean_display_text


KNOWN_CONTAMINATED_SNIPPETS = (
    "we operate a rolling programme which we regularly review to ensure the remaining roads and residential streets in your neighbourhood are clean and safe",
    "the zoi identifies the distance within which new residents are likely to travel to",
    "if we decide to issue an order we will write to the owner of the tree",
    "find out about neighbourhood planning, planning reporting and local development plans",
)

NOISY_MARKERS = (
    "copyright acts",
    "customer services",
    "contact us",
    "make a comment",
    "report a breach",
    "planning breaches",
    "planning enforcements",
    "interactive map",
    "view and comment on planning applications",
    "current and past planning applications",
    "planning application information submitted",
    "downloaded and/or printed",
    "downloaded and or printed",
    "consultation purposes",
    "all comments on planning applications",
    "decision-making process",
    "community infrastructure levy",
    "local plan, cil",
    "these forms should be used",
    "neighbourhood planning",
    "planning appeals",
    "application form",
    "rolling programme",
    "remaining roads",
    "distance within which new residents are likely to travel",
    "write to the owner of the tree",
)

FIELD_KEYWORDS = {
    "permitted_development": ("permitted development", "planning permission", "prior approval", "application"),
    "height_rules": ("height", "eaves", "roof", "storey", "metre"),
    "depth_rules": ("depth", "rear", "projection", "project", "original wall", "garden", "metre"),
    "boundary_rules": ("boundary", "road", "front", "side", "neighbour", "highway", "distance"),
    "roof_rules": ("roof", "dormer", "rooflight", "ridge", "eaves", "alteration"),
    "materials_rules": ("material", "appearance", "match", "finish", "brick", "render", "cladding", "tile"),
    "conservation_area": ("conservation", "heritage", "area", "character", "appearance"),
    "listed_building": ("listed", "consent", "historic", "building"),
    "article4_notes": ("article 4", "permitted development", "direction"),
}


def normalize_local_note(value) -> str:
    return clean_display_text(value)


def is_known_contaminated_snippet(value) -> bool:
    text = normalize_local_note(value).lower()
    if not text:
        return False
    return any(snippet in text for snippet in KNOWN_CONTAMINATED_SNIPPETS)


def is_planning_local_note(value, field_key: str = "") -> bool:
    text = normalize_local_note(value).lower()
    if not text:
        return False

    if is_known_contaminated_snippet(text):
        return False

    if any(marker in text for marker in NOISY_MARKERS):
        return False

    keywords = FIELD_KEYWORDS.get(field_key, ())
    if keywords and not any(keyword in text for keyword in keywords):
        return False

    return True
