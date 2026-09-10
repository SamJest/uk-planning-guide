# Recovery phase delivery report

Status at 6 September 2026: source phases committed; bounded recovery batch deployed and live-verified.

| Phase | Source commit | Retained | Completed / changed | Rejected / deferred |
|---|---|---|---|---|
| Audit and baseline | `7bd8903ff82` | All prior branches, worktrees, untracked owner work and production HTML | Six mandatory audits, Git/deployment timeline, complete static baseline and rollback anchor | No reset, cleanup, history rewrite or source/production merge |
| Publication, sitemap and semantics | `8c15712f4a1` | July repaired dropped-kerb, solar, HMO and fence pages; existing URLs | Fail-closed scope/build provenance; 35,249-URL ledger; ten technical sitemap exclusions; explicit North Yorkshire/Glasgow/Sheffield contracts; uncontracted generator failure | Bulk sitemap restore, full-corpus regeneration, mass redirects/deletes and inferred project copy |
| Product and monetisation foundation | `7ca568c5ce7` | All specialist tool routes, My Planning Project and storage behavior | Four-capability tools presentation; central default-off eligibility; empty approved-partner registry; event/privacy dictionary; paid-pack input schema | Commercial activation, invented partners, unconsented scripts and unconfigured checkout |
| Release validation | `43d8164846f` | Production anchor and protected URL families | Source-bound build, semantic cohort checks, exact release manifest and validation evidence | Any untested or full-corpus output |
| Browser quality gates | `1cac028184f` | Existing component styling and tool behaviour | 52 desktop/mobile browser, accessibility, keyboard and visual checks plus four Lighthouse cases | Treating stale browser inputs or a post-result Windows cleanup warning as content QA |
| Generated deployment | `f7a308662fa`, merged by `7749cbba33b` | All other 35,215 HTML files and four unchanged sitemap shards | Exact four-page/four-shard patch through PR15 and successful Pages run | Merging the divergent source branch wholesale into production |
| Missing-URL recovery | `604da40abb9`, deployment `a1ec577bcd6`, merged by `9e9db289561` | Genuine HTTP 404 status and every existing content URL | Accessible noindex custom error document through PR16 and successful Pages run | Soft-404 redirects, canonicalising missing URLs or changing sitemap membership |
| Clicked-404 classification | `05773442d3c` | All 30 missing URLs and 91 clicks as protected demand evidence | Maps every missing combined-rule URL to its existing same-authority parent for visible recovery | No redirect or restoration without equivalence/content-contract evidence |

## Validation

- Final source fingerprint: `5dae6496f1752bf34b150a3b5faa22ffc7aa313ffd368e837dd9bfc7a3d76644`.
- Clean scoped canary: `artifacts/builds/recovery-404-2`; 24 publish routes plus the special 404 document; 11 generators; 15.1 seconds; zero Phase0 errors/warnings.
- Unit/contract/regression tests: 36 passed, zero skipped.
- Semantic cohort: three repaired pages pass; `/tools/` contains all four capability markers; four protected production pages retain exact canonical/local checks.
- Official sources: 27 active, zero unavailable/blocking after replacing the obsolete Colchester validation URL.
- Browser QA: 54/54 desktop/mobile tests pass, including keyboard, axe accessibility, tool operation and scoped visual baselines. The two new custom-404 screenshots were visually reviewed.
- Lighthouse: all four changed pages pass the configured performance, accessibility, best-practice, SEO, LCP, CLS and TBT budgets; raw reports and `lighthouse-summary.md` retained. Edge reports a post-result Windows temporary-profile cleanup error.
- Release candidate: `artifacts/releases/recovery-batch-3`; eight files; four HTML plus four XML; production tree-bound. Overlay validation checks all 35,208 submitted URLs and 139 candidate links with zero errors.
- Counts: production pages 35,219 → 35,219; submitted sitemap URLs 35,218 → 35,208; no redirect or deletion delta.
- Custom-404 release: `artifacts/releases/recovery-404-2`; one new special HTML file; existing page and sitemap counts unchanged; redirects remain zero.

## Deployment

The exact eight-file patch was committed as `f7a308662faa81ddc3cb2253f142ba6765e087d9` on `codex/recovery-batch-2026-09-06`, reviewed in [PR 15](https://github.com/SamJest/uk-planning-guide/pull/15), and merged without base drift as production commit `7749cbba33bc06075424a82ec7f733822acfbc57`. [Pages run 34022456093](https://github.com/SamJest/uk-planning-guide/actions/runs/34022456093) completed successfully. Public verification found all four changed pages HTTP 200, self-canonical and indexable; their LF-normalised SHA-256 values exactly match the reviewed files. The eight live shards contain 35,208 unique URLs and none of the ten exclusions. Rollback remains a normal revert of the single generated deployment commit/merge, not a reset.

The add-only custom 404 was committed as `a1ec577bcd65bac1eb81c13349e36eb71c9d1d9f`, reviewed in [PR 16](https://github.com/SamJest/uk-planning-guide/pull/16), and merged as current production `9e9db28956159587c57d88c7efebe22843f635ed`. [Pages run 34042563042](https://github.com/SamJest/uk-planning-guide/actions/runs/34042563042) completed successfully. A new random missing path returns HTTP 404 with the reviewed custom content, `noindex, follow`, no canonical and no refresh; its LF-normalised hash matches the release. The public sitemap remains 35,208 unique URLs.

## Owner decisions still required

Current Search Console example URLs for the September 5xx, 404, alternate-canonical and crawled/discovered buckets; equivalence or content-contract decisions for the 30 mapped clicked 404s; advertising/CMP/vendor/legal approval; partner identities and commercial terms; analytics retention; hosted checkout/tax/receipt/refund/support providers; paid-pack price and launch approval. These decisions do not block the completed technical recovery, but they do block redirects/restorations, commercial activation and evidence-specific treatment of the remaining Search Console cohorts.

## Full-corpus recovery gate — 10 September 2026

- Retained: the current production tree, the July repaired families, all 1,000 protected traffic URLs, the genuine custom 404, every specialist tool URL, My Planning Project storage behaviour, and the two production-only HomeProof routes.
- Completed: source-backed generic rule and authority rendering; zero cross-template contamination; declared noindex enforcement; noindex-aware sitemap generation; blocked-hub suppression; deterministic internal-link generation; and preservation of reviewed country-first routes outside the optional 900-alias cap.
- Rejected: mass deletion, blanket redirects, full-corpus indexation by filename, unverified local claims, commercial activation, and overwriting HomeProof.
- Clean source fingerprint: `087646aab86244673bde62c165493a3bae4cb7184bd4b83c3cd5df4028165aae`.
- Source-bound canary: passed with zero errors/warnings; finalized report SHA-256 `6cc6caa327f1aeaa7b09985aa4e9ddfa47568976e1b89b0b516b0bab36545536`.
- Clean full build: 18/18 generators; 1,792.78 seconds; 35,218 HTML files including `404.html`; 35,217 routes; 49 sitemap files; 35,195 submitted URLs; overall `HEALTHY`.
- Tests: 53 Python contract/regression tests passed; 54/54 Edge desktop/mobile contract, keyboard, accessibility, functional, 404 and visual checks passed. Six intentionally expanded recovery-page baselines were visually reviewed and updated.
- Exhaustive metadata release gate: all 35,219 deployment routes passed page-role/title assignment and metadata-quality checks, including title/description presence and length, truncation, bland-template detection, duplicate-family detection and unexpected `noindex` detection.
- Full semantic inventory before the restored reviewed alias: 35,216 routes, 34,168 keep, 1,036 similarity-only merge recommendations retained for evidence review, 12 intentional canonical bridges, and zero repair/noindex/410 recommendations, contamination, source-family mismatch or local-evidence-floor gaps. The additional Colchester Article 4 route was separately canary/browser validated and remains declared `noindex` pending authority-specific evidence.
- Pre-deployment route reconciliation: candidate 35,217 versus production 35,219; the only candidate omissions are `/homeproof/` and `/homeproof/workspace/`, which the deployment overlay must retain. No candidate-only route exists.
- Deployment: generated commit `4dcd42073dad03487a8e111d0d4651d2c2fa2538` was reviewed and merged through [PR 17](https://github.com/SamJest/uk-planning-guide/pull/17) as production commit `708e972d7bff967ed6b99a4cdc821983b34c4a55`. [Pages run 34535683965](https://github.com/SamJest/uk-planning-guide/actions/runs/34535683965) completed successfully. The combined live tree has 35,219 routes: all 35,217 candidate routes plus the two retained HomeProof routes. No HTML page was deleted; nine obsolete XML shards were removed and remain recoverable from Git.
- Live verification: the homepage, North Yorkshire permitted-development, Glasgow conservation-area, Sheffield council, Colchester council, restored Colchester Article 4, HomeProof landing and HomeProof workspace routes return HTTP 200 with the reviewed titles and canonicals. The Colchester Article 4 route and HomeProof workspace retain their intentional `noindex`; a random missing path returns a genuine HTTP 404. The live sitemap index returns HTTP 200 and references 49 successful shards containing 35,195 unique submitted URLs, zero duplicates and zero obsolete full-corpus or incident-recovery shard references.
- Deployment warning: GitHub Pages reported the platform action's Node.js 20 deprecation while forcing that action to Node.js 24. The build and deploy jobs both succeeded; this warning does not affect the rendered site but should be watched as routine workflow maintenance.
