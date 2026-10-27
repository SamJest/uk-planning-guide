# Mandatory: eliminate redundant URL generation; keep only valuable canonical indexables

The owner specifically DOES NOT want tens of thousands of duplicate *unindexed* pages.
**This is a production architecture requirement, not simply a Search Console reporting issue.**

## Non-negotiable result

1. **One durable URL for each distinct user intent and subject.** A different slug, council label, postcode variation, boilerplate paragraph or swapped keyword is not sufficient to justify another indexable page.
2. **Fix at the source generator/data graph.** Do not generate redundant public 200 pages and merely slap `noindex` on all of them. Remove or merge duplicate records/routes, rewrite link creation and sitemap assembly to use canonical page IDs only. Existing obsolete URLs must receive an explicit migration/retirement strategy.
3. **Before merging:** establish intent, primary content, official evidence, backlinks/traffic, inbound internal links, canonicals and any valuable unique sections. Preserve relevant information and valid legacy traffic.
4. **When same purpose/same answer:** select the stronger stable URL; merge useful passages/evidence; remove the alternative from future main HTML generation, internal navigation and sitemaps; serve a **single-hop 301/308** to the winner if host supports it. Avoid redirect chains and all-to-home redirects.
5. **GitHub Pages limitation:** bare GitHub Pages does not provide arbitrary host-level 301 rules. DO NOT claim a meta refresh or JavaScript redirect is HTTP 301. If redirects cannot be configured, prefer appropriate legacy HTML page with clear visible move link + `rel=canonical` to intended page as a **temporary** migration step, or negotiate a deployment edge redirect rule if an existing edge layer is available. Document residual duplicate 200 response until resolved. Do not keep the duplicate in sitemap or link to it internally.
6. **If no meaningful alternative and no user value:** retire route properly with HTTP `404`/`410` where host actually supports it; do not point to a vaguely similar topic. If a directory of static build files is removed on GitHub Pages, verify 404 handling. No `noindex` band-aid for obsolete duplicates.
7. **If two pages target different tasks despite shared boilerplate:** keep both only when the primary answer and useful content are materially different, supported by their own evidence, and clear from title/H1 and internal links.
8. **Unverified thin pages:** don't blanket `noindex` or delete all missing-evidence council pages. Prioritise researching them; if still non-distinct, fold into a better hub where practical, with risk review and redirects. Keep useful public tools/search interfaces functioning, even if their interface pages are not separate landing pages.
9. **Canonicals:** canonical 200 pages should self-canonicalise; consolidated 200 legacy shells point canonical to winner; no conflicting canonical, sitemap, schema URL or hreflang signals. Canonical is a signal, not an assurance Google agrees.
10. **Robots:** don't use robots.txt to enforce canonicals; blocked crawlers might not see `rel=canonical`. Avoid broad robots blocks that stop Google recognising redirects, or block CSS/JS needed for rendering. Do not use the GSC temporary removal tool as a duplicate strategy.
11. **Not every Google-known URL is part of the current build.** Categorise old historical URLs separately from currently emitted routes. Excluded noncanonical variants are NOT an SEO failure; emitting new redundant variants is.
12. **Sitewide near-duplicate scores are candidate flags, never automatic proof.** Large boilerplate and fixed legal text naturally repeat; inspect the MAIN answer, local evidence, functionality and query intent. Ensure false positives from repeated headers, nav and accessibility links do not delete unique pages.

## Required per-URL disposition

`KEEP_ENRICH` | `KEEP_DISTINCT` | `MERGE_REDIRECT` | `LEGACY_CANONICAL_TEMP` | `RETIRE_404_410` | `RESEARCH_BEFORE_DECISION` | `NONINDEX_UTILITY`

Every decision row must contain:
`from_url, to_url, page_family, intent_key, current_status, current_canonical, is_in_sitemap, traffic_clicks, traffic_impressions, backlinks_known, distinct_information, evidence_status, proposed_action, confidence, risk, reason, reviewer, approved_at, actual_http_result, implemented_at`.

**High-risk protection:** any URL showing recent GSC clicks, valuable external links, genuine separate legal jurisdiction, actual planning map/actionable details or working calculator must be independently reviewed before a move. Unknown backlinks are not the same as zero backlinks. Do not implement a mass redirect table based only on string similarity.

## Duplicate signals to compute (separately)

- Exact normalised main-content hash (ignore nav/footer/boilerplate, but retain headings/answers).
- Near-duplicate similarity of main ANSWER + informational sections; pair candidates *within related families*, with a separate global pass for accidental cross-topic clones.
- Same intent key: `nation | authority_id | project | topic | specific-user-question` (some keys do not apply); do not equate council and nation.
- Same title/H1, titles differing only in locality, repeated snippet patterns.
- Link-and-answer-only doorway pages, pages with zero verified distinguishing facts, unsupported 'Article 4 applies' statements.
- Overlapping legacy `/councils/{slug}/` vs `/{nation}/councils/{slug}/`, `/local-search/` vs comprehensive `/hmos/...` or `/article-4/...`, combinations of slugs and trailing slash or index.html.
- Query strings, HTTP/HTTPS, www/non-www and capitalisation as representation variants, NOT new pages.

## Measurable acceptance gates

- `duplicate_emitted_count` (confirmed redundant current generated pages) is **zero for new generation** after consolidation; legitimate dual-intent variants explicitly reviewed. Existing legacy 200 shells counted separately and targeted for removal.
- `sitemap_noncanonical_count = 0`, `sitemap_noindex_count = 0`, `sitemap_missing_local_page_count = 0` for verified indexable URLs; no promise Google will index them.
- `canonical_conflict_count = 0` in tested outputs; `internal_links_to_deprecated_count = 0` in changed cohort and eventually whole site.
- Each merged source has a landing page capturing its unique truthful content or an intentional retirement reason; no page just discarded because it lacks clicks this month.
- Publish before/after `emitted_pages`, `eligible_unique_pages`, `retired_pages`, `legacy_200_shells`, `merges`, `redirects_verified`, `GSC crawled_not_indexed`, `GSC duplicates_google_other_canonical`, and indexation of **submitted canonical** URLs. Initial GSC exclusion counts may rise before stabilising.
- Regression: adding a duplicate page fixture or contradictory canonical must FAIL CI.

## References
https://developers.google.com/search/docs/crawling-indexing/consolidate-duplicate-urls
https://developers.google.com/crawling/docs/crawl-budget
https://developers.google.com/search/docs/essentials/spam-policies
