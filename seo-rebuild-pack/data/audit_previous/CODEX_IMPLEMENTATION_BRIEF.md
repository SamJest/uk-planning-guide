# Codex implementation brief — UK Planning Guide SEO recovery

Work in the existing website repository; do not rebuild or migrate hosting. This is a quality-and-indexing repair, not a new pSEO rollout. Read `READ_ME_AUDIT.md`, `prioritised_fix_plan.csv` and `search_console_1000_pages_ranked.csv` from this package first.

## Phase 1: inventory and non-destructive QA

1. Find the site generator and all sources of project, local-authority, rule, FAQ and local-search pages. Count actual generated HTML URLs and map every generated URL to type, title, canonical, content source and indexability rule.
2. Check the deployed `robots.txt` plus all sitemaps. Confirm valid XML, exact URL counts, sitemap `lastmod` truthfulness, HTTP codes, redirect targets, canonical targets, noindex tags and homepage/internal link reachability. Use `full_site_crawler.py` as an independent cross-check on an internet-connected machine, not as a substitute for repository inspection.
3. Create `seo-qa-report.csv` with one row per emitted page: source template, URL, canonical, title, H1, jurisdiction, project/rule topic, local evidence status, body word count, sitemap inclusion, indexability, duplicate fingerprint, suspected topic-leak flags. Do not equate similar boilerplate to confirmed duplicate content.
4. Export or request GSC's URL examples for 'Duplicate, Google chose different canonical than user' (593), 'Crawled – currently not indexed' (17,013), and 'Discovered – currently not indexed' (6,737); classification must be based on examples, not on guessed causes.

## Phase 2: correctness first

5. Trace why old indexed output for `/planning-permission/flintshire/` described garden-room rules, why `/maximum-height/lambeth/` defaults to garden-room heights, and why `/hmos/staffordshire/tamworth/article-4/` prioritises conservation areas as the main constraint. Audit all template defaults. Add tests that catch an unrelated project or country jurisdiction in the prominent quick answer.
6. For council-specific local-rule pages that say no local source facts have been verified, add exact live official sources, directions and applicable mapped areas where evidence actually supports it. If there is no unique answer, prepare for selective consolidation/noindex, retaining clear navigation. Never fabricate local legal facts or pretend a generic source list settles a local property-specific question.
7. Trace two council URL architectures (`/councils/<slug>/` and `/<country>/councils/<slug>/`). Produce a **proposed** canonical and redirect mapping with GSC impressions/clicks and external-link risks; do not bulk-apply or deindex indexed pages until the mapping is reviewed.
8. Identify local-search vs HMO authority vs Article 4 overlaps for Nuneaton and Bedworth, Milton Keynes, Tamworth, Loughborough and Harborough. For each, state genuinely distinct search intent or recommend a primary page and route for the redundant page. No blanket deletion.
9. Ensure every indexable page has correct `lang`, unique descriptive title and H1, canonical in source HTML, correct source links, actual material revision date and consistent in-site links. Review claims like 'editorially checked' against a real auditable process.

## Phase 3: staging and rollout

10. Put changes behind a small staged sample (one English authority, one Welsh authority, one Scottish authority, and a few HMO/Article 4 pages). Build and rerun QA. Publish only after generated output validates and canonical links are consistent.
11. Produce an exact diff list: newly redirected URLs, canonical changes, changed indexability, sitemap additions/removals, user-facing content changes, tests performed.
12. Do not change working URLs or replace strong pages merely to increase the percentage indexed. Monitor affected pages' rankings/clicks and GSC canonical decisions 2–4 weeks after each deployment.

## Acceptance criteria

- No generated page contains a quick answer about an unrelated project type or another jurisdiction.
- No intentional canonical page declares contradictory canonical, internal-link and sitemap signals.
- A local indexable Article 4 page answers a source-verified local question; a purely generic source-navigation page is not presented as a local legal determination.
- Redirect rules are implementable on the **actual existing host**; don't assume GitHub Pages supports arbitrary HTTP 301 rules.
- All release notes say exactly how many URLs were affected, which were protected and which await manual review.
