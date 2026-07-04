from __future__ import annotations


MOJIBAKE_MARKERS = (
    "Ã",
    "Â",
    "â€",
    "â€™",
    "â€œ",
    "â€",
    "â€“",
    "â€”",
    "â‚¬",
    "Ã¢",
    "Ãƒ",
)


def looks_mojibake(value: str) -> bool:
    text = str(value or "")
    return any(marker in text for marker in MOJIBAKE_MARKERS)


def repair_mojibake(value) -> str:
    text = str(value or "")
    if not text or not looks_mojibake(text):
        return text

    repaired = text
    for _ in range(8):
        if not looks_mojibake(repaired):
            break
        try:
            candidate = repaired.encode("cp1252").decode("utf-8")
        except UnicodeError:
            break
        if candidate == repaired:
            break
        repaired = candidate
    return repaired


def clean_display_text(value) -> str:
    return " ".join(repair_mojibake(value).split()).strip()
