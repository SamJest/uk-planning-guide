# Wave 1 — bounded claim evidence canary

Prepared 8 November 2026. **Not deployed.** Targets the recovery branch, not main.

## Publication boundary

Wave 0 PR #18 was merged into `codex/source-recovery-hmo-quality` at `d1332c69ccf76b7ff9b19e79b7724104b4777090`, following owner instruction to continue. Wave 1 starts at that commit. Production main remains `bb01d67fc58f21400dffbf449604ee05d561abbc`; GitHub Pages uses main, `/`. The original dirty workspace was left intact. The extracted upgrade pack and all candidate output remain outside the publishing tree.

This is a source and isolated-canary change. It does not approve the recovery branch's older commits for production, an URL migration, a full build or deployment. Full-site sign-off remains bound to its historical source fingerprint and cannot authorize this changed source.

## Problem and resulting behavior

Previously, a source URL and page date could produce a verified/high-confidence label without evidence binding the claim to the source's nation, authority, project or rule. Five existing records now bind their assertions to exact propositions inside the existing source registry. Evidence references carry scope, an exact locator, review date, separately nullable historical/effective dates, process attribution and a capture digest. No second source registry was introduced.

The five primary routes are North Yorkshire permitted development, Glasgow conservation areas, Cardiff dropped kerbs, Colchester's authority profile and its existing noindex Article 4 guide. `data/canary/wave1-corpus.json` lists them and the wider 20-route QA corpus, including dated traffic-sample clicks. Nineteen other records are frozen by canonical JSON fingerprints: new or changed records must adopt the evidence contract. Historical dates no longer certify their claims; their visible confidence becomes “not assessed.” The current local-source and local-fact minimums remain enforced.

The renderer distinguishes checked context, historical records and unresolved property questions. These shared labels affect 34 isolated HTML files, including legacy aliases; only five record bodies were migrated. There are still 39 candidate HTML files and 78 total candidate files, with no added or removed filenames. Four candidate sitemap files change metadata; their URL membership is protected by the existing validator. The complete changed-file list is in `WAVE_1_EVIDENCE.json`.

The Colchester bridge exposed a pre-existing validator mismatch: it renders the canonical record's content but the validator expected the alias record's old update date. Validation now checks the content owner's date while retaining the alias's canonical, indexation and sitemap requirements. A mutation regression proves removing the canonical content date still fails.

## Source review and limits

Official extracts were read on **7 November 2026**. This is a material-read date, not a legislative effective date or independent professional review. Effective dates remain null where not evidenced. The audit capture is a serialized web-read bundle, SHA-256 `66058c9085228baa88fd1ba42778939f721ee314b0ff4e84018b17db04761d91`; it is not a raw HTTP-body hash. Some retrieved extracts were cached. A direct HTTP attempt returned 403; no fresh successful HTTP status is claimed. The full extracts are retained locally and excluded from the shareable evidence archive.

- [North Yorkshire's local-plan information](https://www.northyorks.gov.uk/planning-and-conservation/planning-policy/north-yorkshire-local-plan) supports emerging-plan context, not an address-level authority or park-boundary determination. The [area-specific application service](https://www.northyorks.gov.uk/planning-and-conservation/find-out-if-you-need-planning-permission-and-apply/find-out-if-you-need-planning-permission-and-apply-your-area) replaces the unrelated minerals/waste advice citation.
- [Glasgow's 5 March 2024 committee report](https://onlineservices.glasgow.gov.uk/CouncillorsandCommittees/viewSelectedDocument.asp?c=P62AFQDN812U81NT81) is explicitly historical. Its 25-area figure is not presented as a current boundary/count check. Review priorities are dated proposals, not proof of completed work.
- [Cardiff's crossover service](https://www.cardiff.gov.uk/vehiclecrossovers) supports application and assessment steps. It does not verify permission at a particular property; no fee or dimensional threshold was introduced.
- Colchester's [validation](https://www.new.colchester.gov.uk/planning/apply/what-you-need), [pre-application](https://www.new.colchester.gov.uk/planning/apply/pre-application-advice) and [plan](https://www.new.colchester.gov.uk/colchester-local-plan) pages support authority-service context. [National Article 4 guidance](https://www.gov.uk/guidance/when-is-permission-required#article-4-directions) does not establish a Colchester direction, withdrawn rights, effective date or property match. That outcome stays unverified and the existing noindex flag is preserved.

Welsh national validation guidance and Scottish ePlanning were corrected to national sources rather than falsely belonging to Cardiff/Edinburgh. Local-source floors still pass. Northern Ireland is covered by an unsupported, unpublished negative fixture: no English fallback or invented numeric answer is emitted. No professional reviewer, site boundary or property-specific legal outcome was invented.

## Before versus after and checks

| Measure | Before | After |
|---|---:|---:|
| Claim-scoped migrated page records | 0 | 5 |
| Scoped propositions in the existing source registry | 0 | 26 |
| Candidate HTML / total files | 39 / 78 | 39 / 78 |
| Public URLs changed / migrated / newly noindexed | 0 | 0 |
| Clicked URLs / exact matches / unresolved variants | 975 / 954 / 21 | 975 / 954 / 21 |
| Main Python regression tests | 78 | 95 |
| Public HTML / sitemap URLs | 35,220 / 35,195 | 35,220 / 35,195 |

The full inventory's summary, pages, protected URLs, sitemap violations and broken-link reports are byte-identical to the Wave 0 after-inventory. The existing 3,986 local-evidence gaps remain unresolved outside this bounded source canary.

Local checks passed: fresh isolated build (11/11 stages); 95 Python tests with no skips; six pack tests; pilot/release/HMO checks; JavaScript syntax; four Node tests; 28 tool smokes; 26 production/research browser checks; all 64 canary browser checks. Full inventory and Linux CI results are recorded in the evidence JSON when complete. Windows sandbox permission failures were retried outside the sandbox; they are not successful test results. Performance thresholds remain unchanged, with Linux CI the established authoritative Lighthouse profile.

The [initial Linux run](https://github.com/SamJest/uk-planning-guide/actions/runs/42526414663) passed the build, evidence preservation, all Python/Node/tool gates and production browser checks. The new cohort browser step mistakenly reused the still-running production server on port 8765 and correctly failed its claim assertions; Lighthouse was therefore skipped. The workflow now explicitly serves the canary on port 8766. The failed run is retained as evidence, not represented as passing or fixed by weakening an assertion.

Six deliberately changed Windows desktop/mobile snapshot baselines were inspected before updating; the existing 1% tolerance was retained. The five source canaries have before/after screenshots at 360, 768 and 1440 pixels, plus automated 320-pixel reflow, keyboard and axe checks. No production screenshot baseline was regenerated. The PR diff contains the six reviewed snapshots; local review images and logs are in the evidence archive.

The preservation gate checks all 20 selected production pages, canonical paths, script sources, forms and candidate indexation. Hashes normalize Git checkout line endings; a separate Git-diff gate forbids any publishing-tree change. The full dated GSC input must match the baseline, and all 975 clicked URLs must retain the same 954 exact/21 unresolved disposition. Unresolved variants are preserved, not redirected or declared fixed.

## Rollback and next PR

Rollback is reverting this source-only PR on the recovery branch; no production rollback is necessary. Do not deploy the 39-page candidate as a full site. Owner review and successful gates precede any further wave. The next PR should be a bounded usability improvement using the accepted evidence model, with its own measurable cohort and preservation checks. High-risk publication, URL migrations, outside services and spending still require explicit owner approval.
