# Source-anchored known problem examples (not proof of whole-site prevalence)

2026-10-27 exports in `data/gsc/` and prior manual spot checks. **No full live crawl was executed in this package**; verify current repo output and actual headers before changing URL routing.

| URL/cohort | Observation | First action |
|---|---|---|
| `/councils/colchester/` and `/england/councils/colchester/` | old route displays moved message linking new route; may be duplicate 200 | check generated files/HTTP status/sitemap/canonical; choose winner with traffic/backlinks considered; redirect if available |
| `/local-search/hmo-article-4-nuneaton-bedworth-warwickshire/` vs `/hmos/warwickshire/nuneaton-and-bedworth/` | likely intent overlap | compare MAIN answers and actual query intent; enrich differentiated map search or merge |
| `/article-4/cardiff/`, `/article-4/milton-keynes/` | generic local caveat, unverified direction details | research council original direction/map; make true local answer or consolidate |
| `/planning-permission/flintshire/` | generic current shell; previously indexed snapshot erroneously used garden room rules | source generator topical leakage regression |
| `/maximum-height/lambeth/` | example of project-neutral height answered via garden-room specifics | require project-specific matrix or redirect to scoped topic |
| `/hmos/staffordshire/tamworth/article-4/` | conservation mentioned as default main constraint on HMO Article 4 topic | correct constraint model, check proper map/source |
| `/councils/sheffield/` | 1,184 impressions / 0 clicks in limited page export | check user question fit, real council detail, snippet |
| `/local-search/hmo-article-4-milton-keynes/` | 1,187 impressions / 0 clicks in limited export | overlap with definitive topic+HMO guide |
| successful fences, driveways, solar and garden rooms | existing sample traffic | preserve routes/behaviour, enrich carefully |

GSC indexing report: 10,840 indexed, 24,355 unindexed, of which 17,013 crawled-not-indexed, 6,737 discovered-not-indexed, 593 Google-selected different canonical on 23 Oct. These are GSC *aggregates*, not exhaustive per-URL examples. Get the example URL exports for indexed and excluded cohorts if access permits.

The performance CSV sample 1,000 pages and 1,000 queries does not reconcile with daily totals; don't extrapolate exact per-family click share.

`data/gsc/gsc_1000_page_triage_for_codex.csv` contains a conservative **RESEARCH_BEFORE_DECISION** action label on every one of the 1,000 exported GSC URLs. Labels are search-path heuristic investigation categories, not verified duplication judgments. Run `scripts/inspect_content_smells.py --root PATH_TO_BUILD` to flag likely generic placeholders or wrong-topic openings across the current built pages; **review** rather than auto-remove the matches.
