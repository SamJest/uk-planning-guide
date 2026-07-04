def slug_to_title(slug):
    if not slug:
        return ""
    return slug.replace("-", " ").title()


def article(word):
    if not word:
        return "a"
    return "an" if word[0].lower() in "aeiou" else "a"