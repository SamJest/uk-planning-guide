"""Blocking publication checks, shared by rendering and the whole-output audit."""
import json
from pathlib import Path
import re
from utils.content_integrity import visible_text

CONFIG = json.loads((Path(__file__).resolve().parents[1] / "config/jurisdiction_markers.json").read_text(encoding="utf-8"))


def content_errors(html, path="/"):
    # Do not join separate headings/paragraphs into an apparent instruction,
    # e.g. "What it does not replace</h3><p>This site ...".
    text = visible_text(re.sub(r'</(?:h[1-6]|p|li|div|section)>', '. ', html, flags=re.I))
    errors = []
    for pattern in CONFIG["internal_patterns"]:
        if re.search(pattern, text, re.I):
            errors.append("internal instruction: " + pattern)
    # Paths cover both /wales/projects/... and legacy /project/wales/authority/.
    nations = {n for n in ("wales", "scotland", "northern-ireland") if n in path.strip("/").split("/")}
    nations.update(re.findall(r'data-jurisdiction=[\"\'](wales|scotland|northern-ireland)[\"\']', html))
    for nation in nations:
        for pattern in CONFIG["jurisdiction_patterns"][nation]:
            if re.search(pattern, text, re.I):
                errors.append(f"{nation} rule leakage: {pattern}")
    if re.search(r"Sources checked\s*:?\s*Not yet verified.{0,120}Confidence\s*:?\s*High\b", text, re.I):
        errors.append("unverified source set with high confidence")
    elif re.search(r"Confidence\s*:?\s*High\b.{0,120}Sources checked\s*:?\s*Not yet verified", text, re.I):
        errors.append("unverified source set with high confidence")
    return errors


def assert_publishable(html, path):
    errors = content_errors(html, path)
    if errors:
        raise ValueError(f"Content QA failed for {path}: {'; '.join(errors)}")


def audit_output(output):
    output = Path(output)
    files = list(output.rglob("*.html"))
    if not files:
        raise ValueError(f"No generated HTML to audit in {output}")
    failures = []
    for file in files:
        route = "/" + file.relative_to(output).as_posix()
        failures.extend(f"{route}: {e}" for e in content_errors(file.read_text(encoding="utf-8"), route))
    if failures:
        raise ValueError(f"{len(failures)} content QA failures:\n" + "\n".join(failures[:80]))
    print(f"Production content QA passed: {len(files)} HTML files")
    return len(files)
