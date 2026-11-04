# Wave 0 — historical CI baseline and preservation gates

3 November 2026. **NOT DEPLOYED.** [PR #18](https://github.com/SamJest/uk-planning-guide/pull/18).

## Branch reconciliation and publication boundary

- Observed remote main: `bb01d67fc58f21400dffbf449604ee05d561abbc`.
- Observed recovery / PR base: `codex/source-recovery-hmo-quality`, `36e47c3596b3d09ad2ede389a8bf4df7460ebfaa`, four commits ahead of main, zero behind. No open PR existed at initial inspection.
- Tested implementation: `25c6e0d3d483cb2555fec987aac494606b5910ed` on `codex/ukpg-next-level-wave-0-2026-11-03`. Subsequent evidence-only commit does not change tested implementation.
- GitHub Pages API reports legacy branch publication from **main, `/`**. Neither this source checkout nor the 39-page canary is an approved full-site deployment artifact.
- Existing dirty work on `codex/production-repair-source-2026-09-12` was left intact. Work took place in an isolated worktree. The November ZIP was extracted outside the repository and publishing tree; its master prompt, repository map, release gates and remaining specifications were read alongside the October recovery report and existing packs.
- This PR targets the recovery branch so the Wave 0 diff remains bounded. It does **not** merge the recovery branch into main or approve its four prior commits for publication.

## Diagnosis: the pack's missing-page assumption was false

[October run 40601842366](https://github.com/SamJest/uk-planning-guide/actions/runs/40601842366) ran 74 Python tests with one error, then skipped the downstream gates. Its checkout used `fetch-depth: 1`. The error reported Flintshire absent from the pinned baseline.

Direct GitHub Contents API verification found `planning-permission/flintshire/index.html` **at that exact main SHA**, blob `d7b7cf54e4cca338e9a175e002ab2b26ff3b1c9b`, 66,498 bytes. All five pilot paths exist there. The unchanged pilot suite passed all three tests locally with history available. A separate shallow no-checkout repository, with partial-clone lazy fetching disabled (`GIT_NO_LAZY_FETCH=1`), reproduced the missing-path error and exit 128. An initial partial-clone experiment automatically fetched the requested object and therefore passed; it was not treated as a reproduction.

The defect was unavailable historical Git objects in CI, not a legitimately new Flintshire route. Reclassifying Flintshire as new, skipping it, or moving the baseline would weaken the test.

## Implementation and exact public footprint

1. `.github/workflows/seo-qa.yml` fetches full history for the pinned historical comparisons.
2. `tests/test_seo_pilot.py` fails explicitly when the historical commit is unavailable, retains strict ordered script-source / form-action / canonical comparisons for **all five** real pages, and adds four regression tests:
   - missing history is an error, not a new-page classification;
   - nine changed/removed/added script, form and canonical mutations must fail the same preservation assertions;
   - a synthetic new-route fixture independently satisfies jurisdiction, unverified evidence, one-H1, canonical/script/form and idempotence contracts;
   - the four recovered guide panels and four text downloads exactly match their source renderers.
3. This report and `WAVE_0_EVIDENCE.json` record results, hashes, unresolved URLs and release limits.

**Public URLs changed, added, removed, redirected, canonicalized or newly noindexed: none.** No generator, rule, template, runtime asset, production HTML, sitemap, GSC input, source-review date or legal claim changed. The synthetic route is test data only. The 307 HMO summaries were checked against their source renderer without writing production output.

## Before versus after

Fresh `scripts/inventory.py` scans ran before and after, excluding source/templates/dependencies/candidates from public page counts. Their complete pages, protected, broken-link, sitemap-violation and summary files are **byte-identical**; SHA-256 values and all 21 non-exact protected URLs are in `WAVE_0_EVIDENCE.json`.

| Metric | Before | After |
|---|---:|---:|
| Emitted HTML | 35,220 | 35,220 |
| Unique sitemap URLs | 35,195 | 35,195 |
| Research-before-decision pages | 35,196 | 35,196 |
| Operational noindex utilities | 14 | 14 |
| Legacy canonical bridges | 10 | 10 |
| Sitemap violations / broken local links | 0 / 0 | 0 / 0 |
| Clicked GSC sample | 975 | 975 |
| Exact emitted matches / unresolved variants | 954 / 21 | 954 / 21 |
| Missing local-evidence placeholders | 3,986 | 3,986 |
| Wrong HMO conservation-default flags | 0 | 0 |
| Python tests (October CI versus candidate) | 73 passed, 1 error | 78 passed, 0 skipped |

The GSC input is the existing dated October export, not fresh live analytics or a complete backlink/traffic census. Protected CSV SHA-256 before and after: `59ce9c77eaa4a9dc58d931b012a137927af4255fecc8847ca6e1df971f47b8b9`. The 21 mismatches were retained, not erased or automatically migrated.

## Tests actually executed

Implementation SHA above; local Windows Python 3.12 with CI-pinned lxml 6.1.1 / BeautifulSoup 4.14.2, locked npm dependencies and Chromium. [GitHub PR CI run 41693594308](https://github.com/SamJest/uk-planning-guide/actions/runs/41693594308) and [push CI run 41689543115](https://github.com/SamJest/uk-planning-guide/actions/runs/41689543115) both succeeded. Every downstream step in PR CI executed successfully; no skipped test steps.

| Command / gate | Result |
|---|---|
| `python build_site.py --validation-baseline .` | PASS; isolated canary, 11 scripts, 39 HTML; zero contract errors/warnings |
| `python scripts/repair_pilot.py --check` | PASS; 5 pages, zero stale |
| `python -m unittest discover -s tests -v` | PASS; 78, zero failed/skipped locally and in CI |
| `python scripts/check_release.py` | PASS; pilot canonicals/assets/links and existing protected route presence |
| `python scripts/repair_hmo_summaries.py --check` | PASS; zero stale summaries across existing HMO outputs |
| `python -m unittest discover -s seo-rebuild-pack/tests -v` | PASS; 6, zero failed/skipped |
| `node --check` for every `assets/js/*.js` | PASS; zero syntax failures |
| `npm ci` | PASS; existing package-lock preserved |
| `node --test tests/planning_route_jurisdiction.test.cjs tests/static_preview.test.cjs backend/planning-lead-worker/test/worker.test.js` | PASS; 4, zero failed/skipped |
| `UKPG_OUTPUT_DIR=. node scripts/tool_smoke_test.js` | PASS; all 28 tools |
| Playwright `production-journeys.spec.mjs` + `research-improvements.spec.mjs`, 2 workers | PASS; 26 desktop/mobile tests locally and in CI |
| Playwright `phase0-canary.spec.mjs`, 2 workers, isolated canary | PASS; 54 keyboard/axe/contract/screenshot tests, zero skipped; no screenshot baselines updated |
| `scripts/inventory.py --root . --output ...` twice | PASS; complete before/after inventories byte-identical |
| `git diff --check` | PASS |

Initial sandbox Python/pack runs failed on Windows temporary-directory permissions and the Node preview check failed on denied loopback access. Unrestricted reruns passed. One intermediate Python run skipped the canary because a newly added test changed the input fingerprint; the canary was rebuilt, then the final **78-test run passed without skips**. These intermediate results are preserved in local logs, not hidden by test changes.

The isolated candidate's local source fingerprint is `8c4a245701d7f853282bca7fd520b97958acf0646e95c1cfff9352e4f0e73d05`. File blob IDs and fresh canary report hash are recorded in the evidence JSON. Fingerprints include checkout bytes and therefore may differ between Windows CRLF and Linux LF environments. Fresh machine-path reports remain in ignored QA artifacts; tracked historical reports were restored rather than committed as unrelated churn.

No visual change was implemented. The existing desktop/mobile screenshot baselines passed unchanged; before/after design screenshots are not applicable. Browser checks used local static output, test fixtures and email drafts, not real submissions. No production HTTP redirect, fresh official-source verification, field Core Web Vitals or new live GSC measurements are claimed.

## Supplemental performance gate and remaining risks

The existing `test:lighthouse` gate was also run, although it is not part of `seo-qa.yml`. Full Chromium could not launch because of the Windows side-by-side runtime configuration; the Playwright headless Chromium binary ran all five configured URLs with unchanged assertions. The first measurement, concurrent with the inventory scan, failed the 300ms total-blocking-time budget on the homepage (317ms), Cardiff (301.9095ms) and route checker (574.638ms). A second run after the inventory/browser suites finished also exited **1**, with 11 failed assertions across five URLs:

| Canary URL | Failed idle-run assertions |
|---|---|
| `/` | Performance 0.71 < 0.80; TBT 2891.5ms > 300ms |
| `/england/councils/colchester/` | Performance 0.79; LCP 4278.034ms > 2500ms; TBT 313ms |
| `/wales/projects/dropped-kerbs/cardiff/` | Performance 0.79; LCP 4069.9065ms; TBT 362ms |
| `/scotland/projects/garden-rooms/city-of-edinburgh/` | LCP 4056.2035ms; TBT 312ms |
| `/england/tools/planning-route-check/` | TBT 336.3565ms |

Accessibility, best-practices, SEO and CLS assertions did not fail. The variability prevents a confident cause assignment, but the gate is **failing, not waived**. This PR changes no rendering/runtime code; a regression relative to the recovery branch is not established by these measurements. No threshold or production asset was changed to force a pass. Raw Lighthouse reports and both successful collection runs' logs remain in the external evidence archive. **Publication and progression beyond Wave 0 remain blocked pending performance diagnosis.**

The dependency installer also reported 27 existing development-dependency advisories (2 low, 6 moderate, 18 high, 1 critical). No lockfile update or automatic audit fix was made in this baseline repair.

The 3,986 evidence gaps, 21 clicked-URL mismatches, unverified authority claims and static-source publication separation remain review items. Passing local/CI checks does not certify planning law or Google indexation.

## Rollback, release decision and next PR

No production rollback is required because no release occurred. To reverse the implementation on this review branch, revert `25c6e0d3d483cb2555fec987aac494606b5910ed` and rerun the gates; this reinstates the shallow-history CI defect. Do not reset or force-push shared history. The untouched recovery base is `36e47c3596b3d09ad2ede389a8bf4df7460ebfaa`; main remains the production baseline above.

**Decision: GO for review of the baseline fix; NO GO for publication or later waves.** PR #18 stays draft because the supplemental performance gate is unresolved. No approval to merge into main or deploy is implied. Owner review is required before publication, migrations, services, spending, new data collection or risky legal assertions. This Wave 0 PR remains isolated from those actions.

Next bounded work: resolve any reproducible Lighthouse budget failure on the unchanged recovery output versus candidate under the same idle runner before treating performance as green. Once Wave 0 gates and review permit, propose Wave 1 as a separate PR strengthening the existing source/jurisdiction/intent contracts, with five high-risk canary pages and a 20-URL validation corpus; include Wales, Scotland and an NI unsupported fixture, negative wrong-authority/source tests and the existing GSC protections. Use the existing source registry; do not start a second one. No later wave was implemented.
