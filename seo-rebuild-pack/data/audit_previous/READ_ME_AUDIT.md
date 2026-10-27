# UKPlanningGuide.co.uk: Search Console + live-page audit — 27 October 2026

## Audit scope and critical limitation

**Completed:** Parsed both supplied Search Console ZIP exports; analysed 92 daily search-performance observations, 87 indexing chart observations, six exclusion categories, 1,000 exported landing pages and 1,000 exported queries; manually sampled publicly retrievable live pages across local projects, authority pages, topic hubs, FAQs, rule pages and local-search pages. Cross-checked recommendations against Google's official documentation.

**Not completed:** A literal full-site HTTP crawl of all ~35,195 Google-known URLs. This working environment cannot resolve the site's hostname directly from its Python runtime and did not expose the live robots.txt, XML sitemap files, or HTTP response headers to inspect. Public indexed-page snapshots are not a substitute for the raw HTML/headers. Consequently, exact per-URL canonicals, redirect codes, schema, duplicate percentages, broken links, robots rules and sitemap contents are **not verified** here. The packaged rate-limited crawler is provided to run from an internet-enabled host, with a separate output directory.

## Measured results

- Search performance export: 2026-07-26 to 2026-10-25; **1,203 clicks**, **103,044 impressions** in the daily chart.
- Most recent 10 days (16–25 Oct): **406 clicks**, **34,698 impressions**, **1.17% CTR**.
- Previous 10 days (6–15 Oct): **40 clicks**, **4,784 impressions**. Recovery is visible but volatile; October had multiple low-traffic days.
- Page indexing as of **2026-10-23**: **10,840 indexed**, **24,355 not indexed**; 30.8% indexed among URLs known to Google in that report. Indexed was **16,856** on 2026-08-05.
- Exclusions: **17,013 crawled not indexed**, **6,737 discovered not indexed**, **593 Google-chosen different canonical**, **11 historical 404**, **1 server error (5xx)**, **0 noindex**. Counts are GSC group totals, not independently confirmed sitewide issues.

**Data quality limitation:** The 'Pages' and 'Queries' exports contain only 1,000 rows each and should not be used as the sitewide inventory. Sum of page-table clicks (1,218) differs from the daily chart (1,203); the 1,000-row query export sums to only 17 clicks. Treat family/query analyses as directional, not exact all-site shares.

## Priority 1: Confirmed content problems and high-confidence overlap risks

1. **Local-topic skeletons without local answers.** Examples: https://ukplanningguide.co.uk/article-4/cardiff/ , https://ukplanningguide.co.uk/article-4/milton-keynes/ and https://ukplanningguide.co.uk/planning-permission/flintshire/ show 'No property-specific local facts have been verified' and mostly generic steps plus links. An Article 4 query expects an answer about current local coverage, the relevant direction and the official map/source. Either add source-verified local value or stop treating it as a separate indexable search result. Keep useful navigation even if a page is noindexed.
2. **Template-to-topic leakage.** A previously crawled version of https://ukplanningguide.co.uk/planning-permission/flintshire/ gives a *garden room* quick answer; https://ukplanningguide.co.uk/maximum-height/lambeth/ uses garden-room height thresholds as a broad topic's main answer; https://ukplanningguide.co.uk/hmos/staffordshire/tamworth/article-4/ says the main constraint is usually conservation areas, despite the stated Article 4 intent. Investigate template defaults and type/jurisdiction mapping. The Flintshire URL's currently retrieved short version differs from an older indexed cached version, so check live output from the repository, not screenshots alone.
3. **Competing URLs for similar searches.** https://ukplanningguide.co.uk/local-search/hmo-article-4-nuneaton-bedworth-warwickshire/ and https://ukplanningguide.co.uk/hmos/warwickshire/nuneaton-and-bedworth/ address heavily overlapping intent. Similar risk around Milton Keynes local-search vs HMO and Article 4 locality pages. Decide which page *answers* each user query. Where duplicates, choose a retained URL, preserve the best content, then use consistent link/canonical/sitemap signals and permanent redirects when available. A clear, distinct postcode/map answer can deserve its own page.
4. **Older /councils/ versus country-first architecture.** https://ukplanningguide.co.uk/councils/colchester/ includes a banner 'This page has moved' pointing to https://ukplanningguide.co.uk/england/councils/colchester/ . Both have been retrievable via public web views. Audit all cases of parallel council paths: actual 301/200 status, in-sitemap membership, rel=canonical, internal links, chosen canonical (in Search Console). Do not assume the 593 GSC disagreements are all from this cause.
5. **Thin council profiles.** Short versions of https://ukplanningguide.co.uk/councils/flintshire/ and https://ukplanningguide.co.uk/councils/barking-and-dagenham/ largely describe how to check an authority rather than provide meaningful checked local details. Link-dense pages with interchangeable copy may struggle to stand alone. Prefer specific local validation requirements, links, examples, effective-dated directions, local thresholds and source citations over repetitive boilerplate.

## Priority 2: Protect pages already earning traffic

The first 1,000 GSC page rows show: fences-and-walls (195 clicks / 2,908 impressions), driveways (97 / 1,803), solar-panels (88 / 1,159), garden-rooms (75 / 1,184), and outbuildings (87 / 2,061). These are *sample totals*, not overall site totals. Improve their helpfulness, source details and contextual internal links **without wholesale URL changes**.

Low conversion in sampled page groups: councils (17 clicks / 4,993 impressions), HMO (40 / 4,525), local-search (4 / 3,006) and planning-faq (1 / 2,501). Investigate whether the page fails the actual search, rather than just revising the title. GSC contains many unusually long Article 4 queries with 0 clicks, so cross-check actual search impressions and manual SERPs before building more exact-match pages.

## Technical audit pending raw full crawl

- Audit `robots.txt`, XML sitemap index and shards, absolute canonical URLs, and accurate `<lastmod>` only when content materially changed. Keep canonical, indexable 200 pages in sitemap; split sitemaps by content family for diagnostics and within Google's 50,000 URLs / 50 MB per-sitemap limit.
- Confirm `www`/non-`www`, HTTP/HTTPS, trailing slash, `/index.html`, legacy `/councils/`, country-first council URLs, and `/local-search/` destinations all resolve consistently. Note a GitHub Pages deployment may require host-level/edge redirects rather than HTML-only redirects.
- Flag title/H1 repetition, meta duplication, wrong project type in a topic page, empty/short main text, duplicated text, canonical mismatch, noindex, failed page, orphan or low-inlink URL.
- Fix GSC's single remaining 5xx and investigate any 404s still linked or sitemapped; do not redirect truly gone URLs to the homepage.
- Add build-time automated checks: no locally named page may cite an unrelated default project in its first answer; no England-only rule must render as universal in Wales or Scotland; local indexable topic pages need a source/coverage answer; every indexable page has one canonical and distinct H1; sitemap inclusion agrees with canonical/indexability.

## Safer 30-day change order

**Days 1–3:** Run raw full crawler; export GSC example URLs under the 'Crawled – currently not indexed' and 'Google chose different canonical' categories; inspect 30–50 examples in each high-volume family. Capture baseline before deployment.

**Days 4–10:** Repair wrong cross-topic answers; standardise council URL canonical architecture; repair remaining 5xx; correct sitemap/internal links. Make changes first on a controlled batch of URLs, not the whole 35k in one switch.

**Days 11–20:** Consolidate near-identical local-search/authority/topic pages selectively; add substantive official-source local evidence to high-opportunity local topics, with honest 'unverified' treatment where evidence is absent. Keep working pages intact.

**Days 21–30:** Measure organic clicks, UK CTR, affected group indexing, chosen canonicals and index coverage against the 16–25 Oct baseline. Avoid interpreting daily volatility as proof of an algorithmic penalty or a guaranteed recovery.

## Public references

- Google Search Central — canonicalization: https://developers.google.com/search/docs/crawling-indexing/consolidate-duplicate-urls
- Google Search Central — indexing status meanings: https://support.google.com/webmasters/answer/7440203
- Google Search Central — sitemap technical specification: https://developers.google.com/search/docs/crawling-indexing/sitemaps/build-sitemap
- Google Search Central — scaled content quality policy: https://developers.google.com/search/docs/essentials/spam-policies

## Package contents

- `search_console_1000_pages_ranked.csv`: full exported page sample with priority score; the score is only a triage aid.
- `search_console_page_families.csv`: per-family statistics from the limited page sample.
- `search_console_300_queries_by_impressions.csv`: query inspection sample; not a complete query tally.
- `prioritised_fix_plan.csv`: implementation tasks, scope and risk controls.
- `measured_metrics.json`: metrics directly computed from uploaded exports.
- `full_site_crawler.py`: a working, smoke-tested **separate full crawler**; requires external network access.
- `requirements.txt`: Python dependencies.

### Running the crawler

From the folder, with Python 3.10+: `pip install -r requirements.txt`, then `python full_site_crawler.py --site https://ukplanningguide.co.uk --output full_crawl --max-pages 50000 --rps 2 --workers 3`. It follows sitemap index entries and discovered internal links, honours robots.txt when available, and writes `pages.csv`, `sitemaps.csv`, `exact_duplicates.csv`, `near_duplicate_candidates.csv`, `broken_internal_links.csv`, `query_parameter_links.csv`, `summary.json`. At 2 HTTP requests/sec, full discovery and crawling of tens of thousands of pages can run for hours. Near duplicates are *candidates*, not proof; verify manually before canonicalising or redirecting.
