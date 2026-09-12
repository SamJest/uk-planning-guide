# UKPlanningGuide production repair — 11 September 2026

## Root causes

1. `utils/data_loader.py` fell back from missing national files to England's `national.json`. `data/loaders.py` separately merged English fields under Welsh/Scottish overrides. Local scraped overrides could then replace national rules without traceable verification.
2. Three shared FAQ builders contained public-facing editorial instructions.
3. Page contracts allowed high confidence without a verified source set; the renderer printed the values independently. Downloads also used a legacy guide classification despite being a utility page.
4. The nominal Editorial Review Desk had no repository evidence of an independent review team and was emitted as a Person in structured data.
5. Local/project composition repeated decision advice and national summaries. National source links were also marked as local facts, with a regression test enforcing that incorrect behaviour. Some generic local pages synthesized council claims from source titles.
6. The route checker did not require an explicit nation and could assess Northern Ireland input using its general route logic.

## Implementation

- Added `utils/jurisdiction_rules.py` and separate England, Wales and Scotland extension modules under `data/rule_modules/`. Both rule loaders now use this boundary. Missing modules return an unavailable state; unknown geography and mismatched jurisdictions fail. Unverified legacy local overrides cannot modify the baseline.
- Migrated legacy national records to an explicit England jurisdiction with an unverified status and a legislation reference. This is metadata classification, not a claim that all historical text was newly verified.
- Checked the affected extension baselines against [GOV.UK technical guidance](https://www.gov.uk/government/publications/permitted-development-rights-for-householders-technical-guidance/permitted-development-rights-for-householders-technical-guidance), [Welsh Government extension guidance](https://www.gov.wales/planning-permission-extensions) and [Scottish Circular 1/2024](https://www.gov.scot/publications/circular-1-2024-householder-permitted-development-rights/pages/4/). Module source records carry the check date, 2026-09-11.
- Removed editorial instructions in `components/sections.py`, `tool_pages.py` and `personalised_guidance.py`.
- Added the shared `utils/trust_status.py` model; updated contract validation, schema, records and trust rendering. Unverified high confidence is invalid. Utility ratings are omitted, including Downloads. The route checker no longer presents an unsupported confidence rating.
- Replaced the review-desk identity with editorial-process language and removed its Person/reviewedBy schema. About explains the absence of an independent review service and states the England/Wales/Scotland coverage limit.
- Consolidated repeated project blocks and the editorial component. The Cardiff house-extension sample fell from 4,500 to 3,142 visible words (30.2%) before the final source-label shortening. Retained the rule baseline, official links, quick answer, distinct FAQs and next actions.
- Local source panels now attach source links and check dates to the actual structured facts. Source cards are links, not facts. Generic pages without verified facts remain short; canonical contracts are used consistently for the page body and trust component.
- Added an explicit nation choice inside the route checker's existing location step. Northern Ireland, BT postcodes and missing jurisdictions cannot receive a GB route. NI users receive [nidirect guidance](https://www.nidirect.gov.uk/articles/planning-permission-when-apply).
- Added the Somerset Council display label without changing its slugs. Clarified browser printing/Save as PDF on Downloads.

## Regression protection

- `config/jurisdiction_markers.json`, `utils/production_content.py` and `scripts/site_content_qa.py` block internal copy, known English rule leakage on Welsh/Scottish routes, contradictory trust displays and invalid publishable rule metadata. Both legacy and country-first URL forms are covered. The render boundary and build run the checks.
- Added `npm run qa:content -- <build-directory>` and a native Python CLI equivalent. Build validation passes the actual output directory explicitly.
- Added Python tests for all extension variants, missing/mismatched modules, unverified local overrides, targeted content linting, utility trust states and reviewer schema. Corrected the old test that treated source cards as local facts.
- Added two Node tests for Northern Ireland/missing-jurisdiction handling and supported route-check behaviour, wired into CI.
- Updated visual baselines for the intentional trust/source-copy changes after inspection.
- Added `scripts/refresh_source_components.py` for incremental regeneration of shared source components using the production builders, plus local-page regeneration. It only accepts isolated `artifacts/builds/` candidates and preserves existing alias targets.

## Validation

Completed checks (final candidate review completed 12 September 2026):

| Command/check | Result |
| --- | --- |
| `python -m unittest discover -s tests -v` | 65 tests: 64 passed, 1 existing skip |
| `node --test tests/planning_route_jurisdiction.test.cjs` | 2 passed |
| `python build_site.py --full --output-dir artifacts/builds/production-repair` | All 18 generation stages and the existing validation pipeline passed |
| Production content QA during the full build | All 35,218 HTML files passed; this scan is exhaustive, separate from the legacy health sampler |
| Final source-component refresh and production content QA | All 35,218 HTML files passed; 23,899 components refreshed in the resumed pass |
| Final rule metadata/page-record audit and source fingerprint | Passed; current sources match the final refresh fingerprint |
| Final representative-page review | 11 routes returned HTTP 200, one H1 each, and no horizontal overflow; mobile Cardiff also passed |
| `python build_site.py --output-dir artifacts/builds/repair-canary --validation-baseline output` | All 11 stages and 36-page canary validation passed |
| `node node_modules/@playwright/test/cli.js test --workers=2` against the candidate canary | All 54 desktop/mobile contract, keyboard, accessibility and visual tests passed |
| `git diff --check` | Passed |
| Lighthouse CLI | Browser-launch/connection failure on this Windows host |
| Controlled-browser Lighthouse API, same five routes and thresholds | All accessibility, best-practice and SEO targets passed. Performance/loading targets were not consistently green; see below |
| Idle-machine Lighthouse rerun, 12 September | Performance scores 94–98; all category, CLS and TBT thresholds passed. Two LCP thresholds remain above 2.5 seconds |

The initial controlled Lighthouse run measured performance 96–98, accessibility 98–100, best practices 96 and SEO 100. Three LCP measurements were 2.52–2.58 seconds against a 2.5-second threshold. A repeat while the disk-intensive source refresh was running varied: homepage performance 73 (LCP 2.74s, TBT 846ms), route-check LCP 2.60s, and other measured routes passed the configured thresholds. These are residual performance checks, not a claim of a fully green performance release. Raw results are in `artifacts/repair-review/lighthouse-*.json` and both `repair-lighthouse-controlled.log` and `repair-lighthouse-final.log`.

Full logs are in `artifacts/repair-*.log`.

The final idle rerun measured LCP at 2.37s (home), 2.43s (Colchester), 2.47s (Cardiff dropped kerbs), 2.52s (Edinburgh garden rooms) and 2.74s (route checker). The latter two still fail the 2.5s threshold. Accessibility was 98–100, best practices 96, SEO 100, TBT 9–149ms and CLS 0–0.034. The route checker's LCP element is its hero paragraph: the audit attributes approximately 954ms to server response and 1,786ms to render delay, and flags `assets/js/lead-config.js` as render-blocking. This is a concrete performance follow-up; local Python-server timings are not a production hosting benchmark. See `artifacts/repair-lighthouse-idle.log`; the JSON reports now contain this latest run.

Commands use the bundled Python runtime and Node CLI on this Windows machine because `python` and `npm` were not on PATH.

## Representative pages

The review covers:

- `/house-extensions/somerset/somerset/`
- `/house-extensions/wales/cardiff/`
- `/two-storey-extensions/wales/powys/`
- `/house-extensions/scotland/aberdeen-city/`
- `/two-storey-extensions/scotland/city-of-edinburgh/`
- `/my-planning-project/`
- `/downloads/`
- `/about/`
- `/methodology/`
- `/england/councils/colchester/` — structured local facts and dated sources
- `/councils/somerset/` — limited verified local data

Text, canonical, source, trust and viewport findings and screenshots are stored under `artifacts/repair-review/`.

The final review confirms separate Welsh and Scottish extension cards, no utility confidence rating on Downloads/My Planning Project, an explicit coverage statement on About, and the Somerset Council display label. Colchester has five structured local facts; the sparse Somerset page has none and remains 496 visible main-content words. Official-source cards are no longer counted as local facts. Final Cardiff main content is 2,690 words; the earlier like-for-like boilerplate measurement above excludes the subsequent source-label shortening.

Final refresh evidence: `artifacts/repair-source-refresh.json`, source fingerprint `b3676cdeea874025b797720faa7013452901bcedfebb35694ffbbf87bcf2b1e5`. The original full-build manifest predates the incremental source-component regeneration; the refresh evidence records the final source state. This does not renew production sign-off.

## Deliberately unresolved content

- Dedicated Welsh/Scottish national-card modules beyond the six extension project variants were absent. They remain unavailable pending authoritative project-specific data; they do not inherit English rules. Porches remain separate from the extension module.
- Northern Ireland remains unsupported as a rule jurisdiction, with an explicit safe handoff.
- Legacy scraped local rules lack the provenance needed for publication. They remain stored for review but cannot override the national module without explicit jurisdiction, source URL and check date.
- Existing local source-check dates were retained. This repair does not claim a fresh verification of every council policy or designation.

## URLs and release status

No new URL migrations, redirect destinations, or canonical policies were introduced. Existing alias/bridge behaviour is retained. The full candidate is `artifacts/builds/production-repair/`; the original `output/` and live deployment were not replaced. Production sign-off remains separate and has not been renewed automatically.

## Remaining polish

- Expand the unavailable national modules using verified official guidance.
- Review and reintroduce genuinely local facts with dated evidence.
- Improve source-register typography where long citations wrap tightly.
- Improve and remeasure the two remaining Lighthouse LCP failures; inspect hero text rendering, the blocking lead configuration script and actual production response timings.
- The existing CI job runs on Linux, but the repository currently contains only Windows visual baselines. Windows browser tests passed here; Linux visual baselines still need a separate reviewed capture. Content QA itself is wired into the platform-independent Python build.
