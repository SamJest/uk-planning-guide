# Current state inventory — 5 September 2026

## Scope and evidence

Repository: `C:/Users/Jest/Desktop/projects]/UKPGV3`. Static Python generators, HTML/CSS/JavaScript, GitHub Pages. No application changes preceded this audit. The user explicitly adopts the September pack's `02_CODEX_MASTER_PROMPT.md`; earlier packs and CSV contents are evidence, not fresh instructions.

The 38-file September pack was extracted under `artifacts/recovery-pack-2026-09-04/UKPG_RECOVERY_PACK_2026-09-04`. Its Markdown, manifest and supporting data were inspected; full CSV inputs are processed, not assumed from previews. `baseline/pack-manifest.json` records every file's hash. Original files remain unchanged.

## Preserved state

- Initial source branch `feature/phase-0-integrity-trust`, HEAD `4674306f8c3a614a871c1b5c2dbf66829d264190`; tracked working tree clean.
- Existing deployment worktree `.gh-pages-deploy`, branch `codex/remove-search-recovery-language`, HEAD `2e3a69692e1ea3f469da1f869722e0a8f45f07d5`, clean. Its tree equals production `aa7d89ec029c70d5973b7d982fcbe5036316d9b2` (merge PR14).
- Root contains skip-worktree generated files: a clean status does NOT mean a complete materialized deployment. Do not clear those flags or merge production wholesale.
- No tags or stashes observed. Two worktrees. Exact branches, parents, dates, remotes and untracked paths are captured in `baseline/git-*.txt`.
- Local `main` is June8 `23349e4a16052eb319cec05c036faf1880341482`; cached `origin/main` was July22 `91893938269827aca9c3b06ad2ac25beff3e6e99`. A read of the real remote and fetch into FETCH_HEAD established `aa7d89e`. Source/production divergence: 9 source-only and 28 production-only commits.

Untracked earlier work retained: `.gh-pages-deploy/`, `backend/`, `build_tools.py`, ZIPs and build logs, `docs/{lead-capture-setup,qualified-organic-growth,upgrade-implementation-notes}.md`, July5/10/13 incident reports, content-quality/traffic reports, and `scripts/34_...` through `37_...`. Ignored `output/`, canary artifacts, node_modules and earlier browser reports are preserved. No reset, clean, deletion, stash application, force push or broad staging is authorized or planned.

## Build and deployment controls

`build_site.py` defaults to canary; `docs/phase-0-signoff.json` is unapproved. However `core/build_scope.py` defaults to FULL for standalone generators and accepts unknown modes as unrestricted. The full sign-off checks only a nonempty hash, not its relationship to current content. Scripts30/31 package/overlay stale output based on an old passing report. Untracked script34 restores every HTML URL to the sitemap without canonical/indexability/editorial gating.

Production is generated HTML on main, built by GitHub's dynamic Pages workflow. No source QA workflow is present in that deployment-only history. Source `.github/workflows/phase0-qa.yml` runs tests, canary, browser and Lighthouse checks, but is not the production publication gate. Existing authenticated GitHub access supported the bounded PR and workflow verification; no tokens were exposed or changed.

## Baseline

Production: 35,219 `index.html` files, 35,218 sitemap entries in eight opaque full-corpus shards. Exact technical inventory, family counts, hashes, local-output differences and sitemap defects: `baseline/summary.json` and `baseline/url-inventory.csv`. These are file-level observations, not 35,219 HTTP checks or editorial approvals.

Baseline live representative pages and robots/sitemaps were read; seven normalized page hashes matched the then-current production. A random missing URL returned genuine HTTP404. No current 5xx URL can be identified from aggregate September data. The recovery cohort later received browser, accessibility, Lighthouse and post-deployment live checks; an all-live-URL HTTP distribution and current Search Console examples remain unavailable.

Clean reproduction uses a new source-only archive `artifacts/recovery-source-baseline-2026-09-05`, never the user's existing output. See `live_vs_repo_diff.md` for its outcome. Initial existing-output unit baseline: 16 tests pass; this alone is not a clean-build approval.

## Evidence limitations

September coverage: 13,970 indexed / 21,248 not indexed; buckets 14,470 crawled-not-indexed, 4,755 404, 1,413 discovered-not-indexed, 607 alternate canonical, 2 noindex, 1 server error. No example URLs supplied. July's 1,000 404 examples are historical and must not be relabelled as September's issue set.

Performance: six months 9,570 clicks / 614,153 impressions. Exported top1,000 pages total 3,667 clicks / 123,336 impressions, all have clicks; protect them all plus 28 priority URLs and all fences-and-walls paths. Query export is truncated to 1,000 rows (55 clicks / 128,022 impressions), so it is not the total query population. Suspicious HMO/Article4 group: 27 queries, 45,345 impressions, zero clicks; no claim of fraudulent traffic is supported.

## Recovery implementation status — 6 September 2026

Work now runs on `codex/ukpg-recovery-2026-09-06`. The complete classification ledger contains 35,249 unique evidence URLs: 35,219 production files plus 30 clicked URLs verified as live 404s. Decisions are 35,237 `IMPROVE` (protected from path/deletion changes pending semantic review), 1 `KEEP` (the verified Durham fence page), and 11 `NOINDEX/UTILITY`. The first recovery batch removed the ten noindex/noncanonical URLs that were submitted; the eleventh was already absent from the sitemap.

The final source-bound canary `artifacts/builds/recovery-semantic-6` contains 24 approved publish routes and validates against the exact production worktree with zero errors. A bounded eight-file release changed four HTML files and four sitemap shards: page count 35,219 → 35,219; sitemap count 35,218 → 35,208. It was deployed through PR15 as merge `7749cbba33bc06075424a82ec7f733822acfbc57`; the Pages run succeeded and public HTML/sitemap checks match the reviewed release.

The follow-up `artifacts/builds/recovery-404-2` clean canary adds a separately validated special `404.html`. The one-file candidate was deployed through PR16 as merge `9e9db28956159587c57d88c7efebe22843f635ed`. A random missing public path now returns genuine HTTP 404 with custom recovery navigation, `noindex, follow`, no canonical and no refresh. Existing page count remains 35,219 and sitemap membership remains 35,208. Separate analysis maps all 30 clicked missing URLs (91 clicks) to existing same-authority parents but authorises zero redirects or restorations.
