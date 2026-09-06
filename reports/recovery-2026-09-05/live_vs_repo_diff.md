# Live versus repository

Production `aa7d89ec029c70d5973b7d982fcbe5036316d9b2`; source `4674306f8c3a614a871c1b5c2dbf66829d264190`. Existing `.gh-pages-deploy` tree is byte-identical to production's Git tree. Root source/output is NOT deployment truth.

## Representative live checks (4–5 September)

Normalized HTML removes line-ending differences. Seven representative samples match production. Every listed page returned200 and self-canonical; this does not establish semantic quality.

| Route | Normalized SHA256 prefix | Observed defect / retention |
|---|---|---|
| `/` | FB246E362D390DAE | July/HomeProof product additions; retain |
| `/permitted-development/north-yorkshire/` | 8B2AD7B652954156 | 42 Garden Room occurrences,3 editorial-desk mentions; generic-project contamination |
| `/conservation-areas/glasgow-city/` | 67E8739266575EB5 | 32 Garden Room occurrences,3 desk mentions; Scotland-specific repair needed |
| `/councils/sheffield/` | 2A9798C58E6B4AAC | 5 Garden Room occurrences; inspect navigation versus assumed intent, not all mentions are defects |
| `/dropped-kerbs/devon/plymouth/` | A8BAD8CC2CAEB398 | No Garden Room or desk phrase; retain repaired page |
| `/solar-panels/devon/teignbridge/` | 999D3982E0B5D804 | No Garden Room or desk phrase; retain |
| `/fences-and-walls/county-durham/durham/` | D6B58DE7B0C25F47 | No Garden Room or desk phrase; protect sourced1m-highway/2m-elsewhere distinction |

`/404-probe-codex-recovery-20260904/` returned true404, GitHub default page. No custom404 observed. robots.txt advertises sitemap and does not block crawling. No server/CDN redirect configuration proven beyond GitHub Pages behavior; `_redirects` from prior ZIP packaging is NOT evidence of active HTTP301 support on Pages.

Live sitemap comprises8 shards:5,001 + six5,000 +217 =35,218. First shard lastmodJuly21, othersJuly10. Local output has49 sitemap files; exact membership/differences in baseline summary. Lastmod is not proof of source verification.

## Full file-level comparison

`capture_baseline.py` reads all production HTML, head canonicals/robots/refresh, full content hashes, local output hashes, sitemap members and traffic export. `baseline/url-inventory.csv` keeps technical eligibility separate from editorial approval and HTTP observations. Family counts in summary permit cohort review. No filename is treated as evidence of HTTP200. Unknown Google-selected canonical/conversion/backlink data stay unknown.

## Clean reproduction

Source-only Git archive from4674306 extracted into a newly created directory under artifacts; build runs there with bundled Python, isolated output and reports. Existing canary unit tests passed16 against old artifacts; clean reproduction outcome is recorded in `baseline-build-result.md` when complete. Until then, this audit does not authorize a page deployment or assert a clean-build pass.

Browser/Lighthouse baseline unavailable from successful current runs. No current Core Web Vitals export provided. These are explicit deployment validation gaps, not zeros or passes.

## Reviewed replacement delta

The release candidate changes only `/permitted-development/north-yorkshire/`, `/conservation-areas/glasgow-city/`, `/councils/sheffield/` and `/tools/`. The first three become explicit project-free local-rule/authority pages with self-canonicals and verified official sources. `/tools/` presents the four-capability journey while preserving every specialist tool URL. The candidate also removes ten already-noindex/noncanonical sitemap memberships across shards 1, 2, 5 and 7. Exact before/after SHA-256 values are in `artifacts/releases/recovery-batch-2/release-manifest.json`.

The resulting static candidate has no page additions or deletions. It has not been deployed, so no claim is made that live hashes have changed. A post-deployment live verification and performance run remain mandatory.
