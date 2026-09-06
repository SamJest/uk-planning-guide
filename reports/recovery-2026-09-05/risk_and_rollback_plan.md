# Risk and rollback plan

## Main risks and controls

1. Divergent source versus production: source branch is9 commits ahead/28 behind, with skip-worktree HTML. Never deploy source tree or stale output. Base deployment patch on verified production commit and expected file hashes; abort on drift.
2. Existing untracked work: record/preserve all; stage exact new/changed paths only. No reset/clean/pop/force push or deletion. Leave old deployment worktree clean.
3. SEO equity: protect traffic/priority/fences families; unknown performance is not zero equity. Technical exclusion from sitemap is distinct from noindex/deletion. No new redirect without exact evidence and supported host mechanism.
4. Wrong planning guidance: no inferred project for generic rules, no England rules silently applied to Scotland/Wales. Official sources and review dates before conclusions. No mass regeneration.
5. Stale build approval: old reports and old output cannot authorize changed bytes; hash-bound manifest, clean build, explicit cohort and rollback.
6. Privacy/revenue: no ads/affiliates/analytics before appropriate consent; no secrets in client; no personal project fields in events. All commercial flags off until owner/account/compliance decisions resolved.
7. Deployment access: gh token invalid, GitHub connector reads successful production workflow. Verify write capability only when ready; do not change credentials or host settings speculatively. Protected branch rules/Pages admin settings may need owner access.

## Rollback mechanics

Initial production anchor `aa7d89ec029c70d5973b7d982fcbe5036316d9b2`, tree `9c640ff1b40473f2e025e9368ac008d41b1e5cc5`. Existing clean deployment worktree contains the same tree. Initial source anchor `4674306f8c3a614a871c1b5c2dbf66829d264190`.

Each source/release phase is a small normal commit with exact paths and before/after hashes. Roll back a released patch with a new reviewed revert commit/PR on latest production, preserving unrelated later changes; no branch reset. Recheck hashes/counts before reverting. For additions, record that rollback removes only that phase's new files. For sitemap-only changes, retain prior XML blobs in Git; never regenerate old membership from filenames. Commercial emergency rollback is flags off plus prevention of provider injection; maintain paid-user receipts/delivery records.

Never run directory-wide cleanup against root, output, prior canary or .gh-pages-deploy. New build outputs use unique subdirectories; any removal must be separately scoped and validated. Source archive and audit evidence remain local/nonpublic; do not package ZIPs, raw GSC exports, backend credentials or reports into Pages.

## Deployment acceptance

Clean scoped build and relevant tests; semantic fixtures across jurisdictions; exact-file diff and no unexpected count explosion; sitemap members200/selfcanonical/indexable; link targets valid; no accidental retired URLs; no preconsent third-party scripts; visible disclosures; browser/a11y/performance checks; explicit production base and rollback. Unknown current5xx, missing GSC issue samples and unavailable commercial accounts are documented separately. Do not claim tests/deployment not performed.

## Batch1 rollback map

`artifacts/releases/recovery-batch-2/release-manifest.json` records SHA-256 values for all eight changed files. Rollback is a normal revert of that single generated deployment commit: it restores the four HTML blobs and four XML blobs, returns submitted sitemap membership from 35,208 to 35,218, and leaves all 35,219 pages in place. There are no redirects, deletions, payment records, partner state or user-data migrations to reverse. Source rollback is likewise by phase commit, never reset or force push.
