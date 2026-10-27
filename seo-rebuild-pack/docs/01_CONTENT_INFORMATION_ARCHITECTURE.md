# Page quality specification: content as data, not spun prose

Every indexable page must answer a distinctive searcher question. Site-wide identical guidance can be shown in shared components, but must NOT be the page's only answer. For each field, use `verified` / `national_general` / `unverified` / `not_applicable` / `needs_review`. Do not invent local authority facts.

## Sitewide universal template components
- Clear question, short conditional answer first, jurisdiction named, applicability and key exception in first visible panel (no invented certainty).
- Clear category: permitted development vs planning permission vs building regulations vs listed building consent vs other separate permits. Never combine these statuses.
- Specific rule matrix with measurements, caveats and official legal/source citations; distinguish existing land/buildings, designated land, Article 4, and local conditions where applicable.
- Step-by-step eligibility or decision tool with assumptions, outcome labelled as guidance, postcode/authority lookup only if verified data exists.
- Worked fact patterns, what to measure/check, mistakes to avoid, next actions, quick checklist, direct **official** source links, dated relevant updates.
- Meaningful contextual links to other site pages, no automated 'related' links to wrong jurisdictions.
- Author/publisher identified accurately; website independent (not official council or solicitor); don't present automation as expert sign-off.
- Usable on mobile, accessible data tables, HTML crawlable content, performance budget and semantic navigation.
- Avoid generic repetitive FAQ blocks, fabricated user reviews, keyword-stuffed variants, invisible accordion-as-only-content and long prose without new information.

## Page-family contract

### 1. National project guides (outbuildings, fences, solar, driveways, loft conversions, extensions etc.)
- Exactly identify jurisdiction and specific project (not one set of England rules labelled UK).
- Standard requirements and **all key exceptions** with legal instrument official citation per claim; diagrams, measurement examples, relevant question flow, what triggers application.
- Distinguish PD rights from council restrictions and building regulations; note separate legislation for devolved nations.
- Change tracking for law changes, with verified dates; no invented current threshold.

### 2. Nation and cross-cutting rule guides (Article 4, conservation, listed, maximum height, planning-permission hubs)
- Topic-neutral pages must NOT display a specific project's threshold as if universal. Define which types of development rule applies to.
- England/Wales/Scotland/Northern Ireland rules must be separately selected. Include qualifying cases and official links.
- Where a height limit depends on project, show comparative table across relevant categories, don't pick 'garden rooms' by default.

### 3. Council profiles
- Official local planning application service, adopted policies, validation requirements/links, constraints map, conservation area information and directions, council contact service. Show last verified official source and avoid unsupported local-specific claims.
- Council identity stable across old/new names; account for reorganised authorities and Welsh/Scottish/NI planning structures.
- Real differentiating council facts, not just an auto-filled council name in an otherwise universal template.

### 4. Council × project
- If national rule is identical and **no verified local differentiation**, either enrich with useful local application pathway sourced from official council or consolidate into the council / national guide. No programmatic empty cross-product pages.
- Source-verified local validation form, relevant adopted policy, protected areas/directions, document checklist, examples pertinent to area. Unverified constraints must be described as property-dependent.

### 5. Article 4 × area and HMO × council
- Cite authority-issued direction/map link and coverage, relevant class of use and exactly what right was withdrawn if known; effective date only when supported; precise confidence (`confirmed_direction`, `no_direction_found` is NOT proof of none, `unverified`).
- Explicit boundary/address uncertainty and property-specific checks. Avoid claiming a town-wide designation from council-level existence.
- Link HMO licensing (separate regime) correctly, distinguish C3/C4/sui generis and nation applicability. Do not apply England HMO rules across nations.
- Exact-answer local-search helper pages must not compete with definitive guides. Keep only if substantively different map/postcode tool or intent, otherwise consolidate.

### 6. Conservation/listed/planning constraints
- Direct official register/maps and local design guides; identify consent types, not just generic generic 'restrictions may apply.' Avoid guessing designation coverage.

### 7. Planning tools/calculators/routes
- Published, understandable logic and assumptions; version, nation and sourced thresholds, input validation, edge cases, accessibility, disclosure that tool cannot determine property-level constraints without checked boundary data.
- Tools do not require thousands of boilerplate supporting landing pages. Canonicalise interface route appropriately.

### 8. FAQs/scenario pages
- Keep only a distinct real decision question, practical answer and exceptions. Consolidate same-answer scenario permutations into one canonical parent with anchors rather than issuing dozens of thin pages.

## Evidence architecture
One `claim_id` per substantive factual claim in a `sources/` registry containing publisher, official URL, exact proposition supported, nation, authority ID where appropriate, source issue/effective/check date, status, source location, and any supersession. Every project rule can have many precise claims; do not link to a planning home page as proof of an unrelated exact threshold. Store council-specific verified data once then render everywhere. Revision dates must reflect editorial revisions, not build timestamps.

## Information advantage opportunities
- Real source-backed planning matrices by jurisdiction and project; schematics explaining which measurement governs; council application steps; practical decision-tree answers; downloadable checklists; official map lookup links; evidence-linked local examples; real change logs.
- Do NOT mass-generate 30k identical 'in [town]' pages as a route to authority.
