def seed_value(*parts) -> int:
    return sum(ord(char) for part in parts for char in str(part))


def rotate(items, *seed_parts):
    ordered = [item for item in items if item]
    if not ordered:
        return []
    offset = seed_value(*seed_parts) % len(ordered)
    return ordered[offset:] + ordered[:offset]


def town_size_bucket(county_slug: str, town_name: str) -> str:
    clean_county = str(county_slug or "").strip().lower()
    clean_town = str(town_name or "").strip().lower()
    if clean_county == "greater-london":
        return "large"
    if "city" in clean_town or len(clean_town.split()) >= 3:
        return "large"
    if clean_county in {"cornwall", "cumbria", "herefordshire", "lincolnshire", "northumberland", "somerset", "wales"}:
        return "small"
    return "medium"


def vary_paragraph(
    base_sentences,
    *,
    seed_key="",
    sentence_count=2,
    conditional_inserts=None,
    project_type="",
    town_size="",
    scenario_slug="",
    town_name="",
):
    ordered = rotate(base_sentences, seed_key, project_type, town_size, scenario_slug, town_name)
    if conditional_inserts:
        if conditional_inserts.get(project_type):
            ordered.append(conditional_inserts[project_type])
        if conditional_inserts.get(town_size):
            ordered.append(conditional_inserts[town_size])
        if conditional_inserts.get(scenario_slug):
            ordered.append(conditional_inserts[scenario_slug])
    final_sentences = rotate(ordered, "final", seed_key, project_type, town_size, scenario_slug, town_name)
    return " ".join(final_sentences[: max(1, min(sentence_count, len(final_sentences)))])
