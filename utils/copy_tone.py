from __future__ import annotations


COPY_TONE_REPLACEMENTS: tuple[tuple[str, str], ...] = (
    ("Main Tripwires", "Main Checks"),
    ("Local Tripwires", "Local Checks"),
    ("Practical Tripwires", "Practical Checks"),
    ("Common Tripwires", "Common Checks"),
    ("Heritage Tripwires", "Heritage Checks"),
    ("Projection Tripwires", "Projection Checks"),
    ("Siting Tripwires", "Siting Checks"),
    ("Clearance Tripwires", "Clearance Checks"),
    ("Visibility Tripwires", "Visibility Checks"),
    ("Tripwires", "Risk Points"),
    ("main tripwires", "main checks"),
    ("local tripwires", "local checks"),
    ("practical tripwires", "practical checks"),
    ("common tripwires", "common checks"),
    ("heritage tripwires", "heritage checks"),
    ("projection tripwires", "projection checks"),
    ("siting tripwires", "siting checks"),
    ("clearance tripwires", "clearance checks"),
    ("visibility tripwires", "visibility checks"),
    ("consent triggers, heritage tripwires", "consent triggers, heritage checks"),
    ("the likely tripwires", "the likely checks"),
    ("the tripwires", "the checks"),
    ("tripwires", "risk points"),
    ("Broad answer", "Working answer"),
    ("broad answer", "general answer"),
    ("Broad guidance", "General guidance"),
    ("broad guidance", "general guidance"),
    ("Local Layer", "Local Context"),
    ("local layer", "local context"),
    ("Authority Layer", "Authority Context"),
    ("authority layer", "authority context"),
    ("live question", "active question"),
    ("Live question", "Active question"),
    ("worth opening next", "worth opening"),
    ("most worth opening next", "most worth opening"),
    ("route still feels", "answer still feels"),
    ("route still looks", "answer still looks"),
    ("route still sits", "answer still sits"),
    ("route still depends", "answer still depends"),
    ("route still needs", "answer still needs"),
    ("route still is not", "answer still is not"),
    ("before you spend more money", "before you pay for more work"),
    ("before you spend more", "before you pay for more work"),
    ("before you spend money", "before you pay for drawings or advice"),
    ("before more money is spent", "before more money goes into the project"),
    ("spend time on drawings", "pay for drawings"),
    ("another round of generic reading", "another round of general reading"),
)


def polish_html_copy(html: str) -> str:
    polished = html or ""
    for old, new in COPY_TONE_REPLACEMENTS:
        polished = polished.replace(old, new)
    return polished
