# Rollout QA and measurement

## Changeset gate
- Commit diff contains baseline inventory; proposed actions; affected routes; production build executed; static audit evidence.
- All changed indexable URLs have correct source-backed answer, nation, topic, relevant local facts and verified official sources; valid internal links and working calculators.
- 0 contradictory canonicals, 0 noncanonical/noindex sitemap entries, 0 new obsolete duplicate HTML route generation, 0 unreviewed protected URL migrations, 0 known broken changed internal links, 0 false factual claims.
- Sample rendered pages on desktop and mobile and compare title/H1/answer relevance and performance; check no JS-only content blocking indexing.
- Show code diff, tests and before/after counts, not just 'fixed SEO'. If a check was not run (e.g. public crawl blocked), label NOT RUN.

## Sitewide counts after each release
`emitted_html`, `eligible_canonical`, `utility_nonindexed`, `intent_dup_candidate`, `confirmed_duplicate`, `merged`, `redirected_real_http`, `legacy_200_shell`, `retired_404_410`, `missing_evidence`, `broken_inlinks`, `sitemap_canonical_mismatch`, `orphan_pages`, `official_claims_verified`, `uncertainty_hold`, `tool_regressions`.

## GSC monitored weekly with lag
`indexed canonicals / submitted unique canonical sitemap URLs` overall and by family; GSC `crawled-not-indexed`, `discovered-not-indexed`, `duplicate chosen other`, clicks/impressions/CTR by query group; traffic impact on previously clicked pages. Keep exact date windows fixed and compare after 7/28/56 days. Google may keep historic retired URLs listed for some time; that's not proof that generator still emits them.

## Release safety
Never deploy a sitewide URL prune in one pass without a protected URL map and rollback. Pilot one council old/new URL, one HMO local-search overlap, one Article 4 local page, one general topic leak, one national project guide across distinct jurisdictions, and at least one working tool. Stage content upgrades separately from route migration when feasible. Keep source evidence backlog distinct from technical QA backlog.

## Repo/Cloud report format
1. Previous state (actual numbers and command); 2. changed source files and output page cohort; 3. before/after indexable/duplicate/retired/legacy states; 4. tests run with PASS/FAIL/NOT RUN; 5. sample URLs; 6. source verification gaps; 7. next bounded PR batch.
