# UK Planning Guide — full Codex implementation pack (27 October 2026)

**Target:** https://ukplanningguide.co.uk  
**Host:** currently publicly appears to be a static site; **verify repository, deploy workflow and actual host** before changing routing.  
**Goal:** the UK's most useful, accurate, comprehensively sourced, project-first planning reference — and maximum **eligible, canonical, distinct** URL indexation, with no guarantee that Google will index any particular page.

## Mobile / Codex Cloud: fastest use

**No need to understand the build system.**

**Owner priority:** no thousands of unindexed duplicate URLs. Remove redundant page generation; merge intent duplicates into more useful canonical pages, and safeguard historical traffic. `docs/00_DUPLICATES_ARE_NOT_ALLOWED.md` is the controlling policy.

1. Open your existing website repository in Codex Cloud on mobile.
2. Copy the **complete** `CODEX_MASTER_PROMPT.md` into a new Codex task. It is standalone, with the baseline and requirements embedded. **It works even before the ZIP is added to the repo.**
3. For the fullest audit, add the contents of this ZIP into `/seo-rebuild-pack/` in the repository, **not** into the site's published HTML/output folder. Add as extracted files (do not commit only the ZIP: Codex cannot inspect files trapped in an archive without extracting them). GitHub's web interface may not extract a ZIP automatically; upload extracted files or have Codex create the scaffold from the master prompt.
4. Ask Codex to begin with the repository inventory, baseline and a **single small pilot**. Then let it work through the playbooks one at a time and create reviewable commits/PRs. Never approve a wholesale canonical/noindex/redirect rewrite without reviewing the mapping.
5. The live crawler (`scripts/crawl_live_site.py`) needs network access and can take a while on tens of thousands of pages; **it has not been run sitewide in this package**. The repository/build crawl is a prerequisite; the crawler is an additional verification, not a substitute.

## What's included

- `CODEX_MASTER_PROMPT.md` — comprehensive standalone task for Codex Cloud, including hard constraints and test gates.
- `AGENTS.md` — persistent Codex repository instructions (merge with any existing root AGENTS.md rather than replacing).
- `docs/` — evidence-led content specifications, UK-jurisdiction separation, URL decisions, technical SEO, research standards, measurement and go/no-go criteria.
- `playbooks/` — small mobile-friendly sequenced Codex prompts.
- `scripts/` — independently runnable static build audit, per-URL prioritiser, evidence registry checker, build comparison, and existing rate-limited live crawler.
- `schemas/` and `data/templates/` — machine-readable evidence format and illustrative unverified page record; no local legal facts invented.
- `data/gsc/` — both original Google Search Console exports + previously computed 1,000-page and query priorities.
- `data/audit_previous/` — first audit, with explicit limitations.
- `tests/` — built-in unit tests for tools.

## Baseline, not promises

Search performance 26 Jul–25 Oct 2026: 1,203 chart clicks / 103,044 chart impressions. Last 10 days (16–25 Oct): 406 clicks / 34,698 impressions vs previous 10 days 40 / 4,784. Indexing report at 23 Oct: 10,840 indexed, 24,355 excluded; 17,013 crawled-not-indexed, 6,737 discovered-not-indexed, 593 Google's different canonical. Reported indexed was 16,856 on 5 Aug.

GSC **Pages** and **Queries** exports each show only **1,000 rows** and do **not** reconcile perfectly with the daily chart (query export has only 17 clicks); don't mistake those subsets for all URLs/queries. Search Console indexing report aggregates are not an export of 35,195 URL examples. Obtain URL sample lists from GSC directly before attributing causes.

## Non-negotiable principles

- **Never invent local planning facts, exact Article 4 direction coverage, dates, maps, costs or approval outcomes.** If official evidence isn't found, mark unknown and place in research backlog.
- **Never copy England rules into Wales/Scotland/Northern Ireland.** UK-wide is not identical to England.
- **Never indiscriminately noindex, delete, redirect or change canonical on currently indexed/traffic-driving URLs.** Prioritise consolidation only for true duplicate intent; preserve value.
- **Don't make longer pages for length's sake.** Every section must answer an actual user decision. Treat near-duplicate scoring as an investigation trigger, not an automatic deletion rule.
- **Don't reset freshness timestamps without substantial genuine content modification.** Review dates require evidence of review.
- **This pack does not contain completed legal research for every authority.** The evidence pipeline is designed to carry out and audit that research within the repo over time; it cannot credibly verify tens of thousands of local claims automatically by writing new prose.
- **Static-first**: preserve existing GitHub Pages/build architecture and avoid new paid infrastructure unless the code proves it necessary and the user requests it.

## Local run (optional, Codex should do this)

```bash
python3 -m pip install -r scripts/crawl_requirements.txt
python3 -m unittest discover -s tests -v
python3 scripts/audit_static_build.py --root PATH_TO_GENERATED_SITE --output outputs/build_audit
python3 scripts/build_priority_queue.py --gsc data/gsc/search_console_1000_pages_ranked.csv --audit outputs/build_audit/pages.csv --output outputs/priority_queue.csv
python3 scripts/validate_evidence.py --input data/templates/evidence_registry_example.json
# After build and internet-enabled environment verification:
python3 scripts/crawl_live_site.py --site https://ukplanningguide.co.uk --output outputs/live_crawl --workers 2 --rps 1
```

If your generator outputs thousands of pages, run first on **existing built pages**. `audit_static_build.py` reads HTML files only; it does not modify the website.

## Official search guidance supporting this approach

- https://developers.google.com/search/docs/fundamentals/creating-helpful-content
- https://developers.google.com/search/docs/essentials/spam-policies
- https://developers.google.com/search/docs/crawling-indexing/consolidate-duplicate-urls
- https://developers.google.com/search/docs/crawling-indexing/sitemaps/build-sitemap
- https://developers.google.com/crawling/docs/crawl-budget

**Definition of success:** no incorrect rule/jurisdiction answers, reproducibly sourced local evidence, unique useful intent for every indexable page, clean crawl and canonical architecture, visible progress in Search Console against an unchanged baseline. A 100% indexation rate is **not** an acceptance criterion because Google controls indexing.

## New pages: prevent duplicate URL creation before publishing

Codex must adapt your actual generator to emit a **semantic intent registry** and run `scripts/validate_page_registry.py --input PATH_TO_GENERATOR_EXPORT.csv` as a pre-build or CI gate. See the `data/templates/page_registry_example.csv` for field names. A fresh route with the same intent as an existing route must fail rather than quietly produce a thin extra page. The example is illustrative; its two rows are not approval decisions for real routes.

For pre/post deployment audits, run `scripts/enforce_release_gate.py --before outputs/before_build_audit --after outputs/after_build_audit`. This flags newly added exact duplicates and sitemap conflicts. It **cannot** decide semantic equivalence on its own, so Codex must still review intent, source-backed facts and historical traffic.

Additional targeting: `data/gsc/gsc_1000_page_triage_for_codex.csv` provides the exported URL cohort with cautious investigation labels; `scripts/inspect_content_smells.py` looks for old move shells, unverified generic placeholders and wrong-topic headline answers in all generated HTML pages. These are flags, not automatic delete decisions.
