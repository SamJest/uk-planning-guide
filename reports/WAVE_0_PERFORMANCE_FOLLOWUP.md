# Wave 0 performance follow-up — 4 November 2026

**NOT DEPLOYED.** [PR #18](https://github.com/SamJest/uk-planning-guide/pull/18), based on the recovery branch. Implementation commit: `9be4d2a793460671b501b99bbeffbc7574efc3ad`. The subsequent evidence commit adds reports and ensures hidden Lighthouse JSON artifacts are included in uploads.

## Outcome

The [Linux PR run 41893693679](https://github.com/SamJest/uk-planning-guide/actions/runs/41893693679) passed every step, including the five-page Lighthouse gate. The [push run 41893686120](https://github.com/SamJest/uk-planning-guide/actions/runs/41893686120) also passed. The gate uses the existing mobile Lighthouse configuration, five URLs and original thresholds: performance >=0.80, accessibility/best-practices/SEO >=0.90, LCP <=2500ms, CLS <=0.10, TBT <=300ms. `lighthouserc.cjs` has not changed.

The earlier Windows runs remain failing observations; they were not erased or relabelled as passing. Matched builds proved that Wave 0 had not changed rendered pages/assets, repeated controls exposed substantial timing variability, and the last Windows diagnostic produced explicit slow-host CPU warnings. Linux CI is now the declared repeatable platform for these lab budgets. These are lab results, not field Core Web Vitals or evidence of faster production pages.

## Concrete changes

- `scripts/serve_site.cjs` inserts the documented GA opt-out property into preview HTML before the analytics loader. This affects the loopback preview response only. It preserves the real external loader and leaves source HTML on disk unchanged. The original traces showed local test visits reaching analytics; the new guard prevents those visits from being sent to the production property.
- The existing Node preview test now checks opt-out order, preserved loader URL and unmodified disk bytes. The browser test checks that the flag is present when the loader executes and that no collection request is emitted. Its mock loader would send a request if the flag were absent.
- The workflow runs that browser regression on both desktop and mobile, runs the existing Lighthouse gate after functional checks, and uploads performance/provenance evidence even on failure, retaining it for seven days. There is no new service, dependency or recurring automation.
- No production template, runtime asset, rule, public HTML, download, sitemap, canonical, GSC input or source-review date changed. The analytics loading experiment described below was discarded.

The opt-out API is documented in [Google's tag privacy guide](https://developers.google.com/tag-platform/security/guides/privacy). Opt-out changes analytics initialization/collection work, so this is explicitly an **opted-out preview profile**, not a measurement of collection-enabled production. The loader still downloads and executes. No production tracking/consent policy was changed, and these tests do not certify that policy.

## Matched recovery and candidate comparison

The original recovery source at `36e47c3596b3d09ad2ede389a8bf4df7460ebfaa` was extracted into ignored artifacts and rebuilt with the same Python packages, same public validation baseline and isolated output as the candidate. Both emitted **39 HTML / 77 page-and-asset files, byte-identical**. The sole excluded file is `BUILD-MANIFEST.json`, which intentionally records different source fingerprints. Both content manifests hash to:

`b95f470ad731845aedef8978f6e4f49e1b6f1ee7b3006ef85c543a8869f892ba`

Both were served by the same preview code, with the same analytics opt-out, Lighthouse 12.6.1, Chromium 149, mobile emulation, URLs, default single run and unchanged assertions. Runs were sequential, without concurrent builds or test suites. Windows recovery failed four assertions; the identical candidate failed two. That difference is measurement variability, not a Wave 0 speed improvement.

| URL | Windows recovery LCP / TBT (ms) | Windows candidate LCP / TBT (ms) | Linux CI LCP / TBT (ms) | CI performance |
|---|---:|---:|---:|---:|
| `/` | 2241 / 2606 | 1673 / 80 | 1806 / 52 | 1.00 |
| `/england/councils/colchester/` | 3004 / 178 | 1855 / 105 | 1804 / 42 | 1.00 |
| `/wales/projects/dropped-kerbs/cardiff/` | 2970 / 230 | 2971 / 172 | 1958 / 48 | 0.99 |
| `/scotland/projects/garden-rooms/city-of-edinburgh/` | 1821 / 174 | 1810 / 144 | 1956 / 49 | 0.99 |
| `/england/tools/planning-route-check/` | 1822 / 160 | 3180 / 140 | 1955 / 50 | 0.99 |

All five Linux reports show zero `/g/collect` requests. Precise values, browser/environment metadata, collection counts and manifest hashes are in `WAVE_0_PERFORMANCE_EVIDENCE.json`; full reports are retained in the CI artifact and external local archive.

## Experiments retained, not shipped

An isolated prototype changed the Google loader from `async` to `defer`. It was compared with a fresh async control, three samples per page, on Cardiff and the route checker. Cardiff's median LCP was **1825ms async versus 1823ms defer**, effectively unchanged; the initial apparent gain against an earlier single sample was not reproducible. The route checker worsened from **3180ms to 3310ms**; median TBT rose from **145ms to 200ms**. The prototype was rejected. No template or production loader attribute changed.

A separate diagnostic blocked the Google loader to investigate first-party cost. It failed with much larger blocking-time values and slow-host CPU warnings, including benchmark indices of 544 and 753.5. It cannot establish first-party or Google causality and is not a passing release profile. The original loader was not blocked in the matched comparison or the passing Linux gate.

The original traces do show material Google-tag blocking work, but also large first-party/unattributed/instrumentation tasks. We therefore do not attribute every failure to Google, claim a production regression, or ship a speculative runtime change based on this Windows session.

## Regression and traffic evidence

Local final runs passed: isolated 39-page build; 78 Python tests with zero skips; 6 pack tests; 4 Node tests; 28 tool smoke checks; all asset JavaScript syntax checks; pilot, release and HMO checks; 26 production/research browser checks; and 54 canary keyboard/axe/contract/screenshot checks. Existing screenshot baselines were not updated. No layout change requires new design screenshots. The new analytics test is included in CI for both viewport projects, in addition to the 26 existing production/research checks.

Git diff checks confirm zero changes to the entire existing public HTML/XML, assets, downloads and GSC input corpus since the previous Wave 0 head. Counts therefore remain **35,220 HTML, 35,195 sitemap URLs, 975 clicked protection sample, 954 exact matches and the same 21 unresolved variants**. They are preserved corpus counts, not a claim of fresh live traffic measurements. The prior full inventory hashes and unresolved variants remain in `WAVE_0_EVIDENCE.json`.

## Review and rollback

**GO for owner review of Wave 0.** The previous performance-blocked status is superseded by the passing enforced Linux gate. No automatic merge, main update, publication or later wave is authorized by that result. Production source/artifact separation, the 3,986 evidence gaps, 21 clicked-URL variants and existing dependency advisories remain documented review items.

Reverting `9be4d2a793460671b501b99bbeffbc7574efc3ad` reverses the preview/CI follow-up, restores the previous browser test and stops enforcing Lighthouse in CI; it does not undo the historical baseline fix. No production rollback is needed because no release occurred.

After owner review, the next bounded PR is Wave 1: strengthen existing source/jurisdiction/intent contracts, first five high-risk canaries then a 20-URL validation corpus, with Wales/Scotland and an NI unsupported fixture, wrong-authority negative tests and the existing GSC protection. No new registry or broad generation, analytics policy change, URL retirement, service or spending is included. Wave 1 has not started.
