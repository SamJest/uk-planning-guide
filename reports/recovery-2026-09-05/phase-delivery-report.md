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

## Validation

- Final source fingerprint: `845da6f2f44d9b69bd1d5cbf2ed81f09b2154715aa8885dc3b86cc99462da249`.
- Clean scoped canary: `artifacts/builds/recovery-semantic-6`; 24 publish routes; 11 generators; 18.42 seconds; zero Phase0 errors/warnings.
- Unit/contract/regression tests: 32 passed, zero skipped.
- Semantic cohort: three repaired pages pass; `/tools/` contains all four capability markers; four protected production pages retain exact canonical/local checks.
- Official sources: 27 active, zero unavailable/blocking after replacing the obsolete Colchester validation URL.
- Browser QA: 52/52 desktop/mobile tests pass, including keyboard, axe accessibility, tool operation and scoped visual baselines.
- Lighthouse: all four changed pages pass the configured performance, accessibility, best-practice, SEO, LCP, CLS and TBT budgets; raw reports and `lighthouse-summary.md` retained. Edge reports a post-result Windows temporary-profile cleanup error.
- Release candidate: `artifacts/releases/recovery-batch-3`; eight files; four HTML plus four XML; production tree-bound. Overlay validation checks all 35,208 submitted URLs and 139 candidate links with zero errors.
- Counts: production pages 35,219 → 35,219; submitted sitemap URLs 35,218 → 35,208; no redirect or deletion delta.

## Deployment

The exact eight-file patch was committed as `f7a308662faa81ddc3cb2253f142ba6765e087d9` on `codex/recovery-batch-2026-09-06`, reviewed in [PR 15](https://github.com/SamJest/uk-planning-guide/pull/15), and merged without base drift as production commit `7749cbba33bc06075424a82ec7f733822acfbc57`. [Pages run 34022456093](https://github.com/SamJest/uk-planning-guide/actions/runs/34022456093) completed successfully. Public verification found all four changed pages HTTP 200, self-canonical and indexable; their LF-normalised SHA-256 values exactly match the reviewed files. The eight live shards contain 35,208 unique URLs and none of the ten exclusions. Rollback remains a normal revert of the single generated deployment commit/merge, not a reset.

## Owner decisions still required

Current Search Console example URLs for the September 5xx, 404, alternate-canonical and crawled/discovered buckets; advertising/CMP/vendor/legal approval; partner identities and commercial terms; analytics retention; hosted checkout/tax/receipt/refund/support providers; paid-pack price and launch approval. These decisions do not block the current technical recovery candidate, but they do block commercial activation and evidence-specific treatment of the remaining Search Console cohorts.
