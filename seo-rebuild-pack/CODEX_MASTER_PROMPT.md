# COPY EVERYTHING BELOW INTO CODEX CLOUD — UK PLANNING GUIDE FULL REBUILD

You are working in my EXISTING GitHub repository for https://ukplanningguide.co.uk. Operate as a senior technical SEO engineer, static-site architect, UK planning-information editor and QA engineer. **Implement substantive improvements in the repository**, not merely write a plan. I access Codex Cloud from mobile, so minimise questions and do the safe preparatory work autonomously. Avoid endless speculative upgrades; stay on this one site and its existing architecture.

## North-star outcome

Make UK Planning Guide the most practically useful UK planning research website: accurate project rules, local authority details, source-verified Article 4/conservation/HMO matters, decision tools, clear next actions, truthful provenance, quick mobile usability. **Aim for all legitimately distinct high-quality production pages to be indexable and, ultimately, indexed — while acknowledging that only Google chooses what it indexes.** Do not try to get every old/duplicate/invalid URL indexed just to hit a percentage.

### Current measurement baseline from my 27 Oct 2026 Search Console ZIPs

- GSC indexed (23 Oct): 10,840; not indexed 24,355; 17,013 crawled currently not indexed; 6,737 discovered currently not indexed; 593 Google chose a different canonical; 11 historical 404 and 1 5xx in aggregate report.
- Indexed was 16,856 on 5 Aug, so don't mistake recent traffic growth for full recovery.
- Last 10 days of performance chart 16–25 Oct: 406 clicks / 34,698 impressions, previous 10 days 6–15 Oct 40 / 4,784; 26 Jul–25 Oct 1,203 clicks / 103,044 impressions total.
- GSC Pages and Queries CSVs show only 1,000 rows each; page table clicks and queries do NOT reconcile with total chart. Treat sampled examples as directions, not population statistics.
- Traffic-protected topical families include fences-and-walls, driveways, solar-panels and garden-rooms. DO NOT casually rewrite their URLs/intent or lose functioning features.
- High-impression investigation URLs: `/hmos/staffordshire/tamworth/article-4/` (1,383 impressions / 0 clicks in exported table), `/local-search/hmo-article-4-milton-keynes/` (1,187 / 0), `/councils/sheffield/` (1,184 / 0), `/local-search/hmo-article-4-nuneaton-bedworth-warwickshire/` (1,064 / 0), `/planning-permission/flintshire/` (1,518 / 0). Do not overinterpret 0-click rows given export mismatch.

### Confirmed live-page quality concerns that must be traced to the generator

- `/article-4/cardiff/` and `/article-4/milton-keynes/` show “No property-specific local facts have been verified” and basic checklists, not actual local direction findings; these should not pretend to provide a verified local Article 4 answer.
- `/planning-permission/flintshire/` now uses a short generic template; an older indexed snapshot injected garden room guidance into this broad planning route. `/maximum-height/lambeth/` previously used garden-room heights to answer a project-neutral question. Treat content mixing as a generator-wide correctness risk: confirm CURRENT built output and add regression tests.
- `/hmos/staffordshire/tamworth/article-4/` currently says the key constraint is “usually conservation areas” despite its Article 4 planning intent. Investigate default constraint selection and add specific HMO/use class/Article 4 logic.
- `/local-search/hmo-article-4-nuneaton-bedworth-warwickshire/` largely funnels readers to `/hmos/warwickshire/nuneaton-and-bedworth/`; investigate duplicate/doorway intent and decide how to make each genuinely distinct or consolidate non-destructively.
- `/councils/colchester/` contains “This page has moved” and links to `/england/councils/colchester/`; test actual HTTP, canonicals and sitemap: host might not support true server-side 301 redirects. Do not declare a duplicate simply because both URLs exist; inspect.
- Site homepage observed 27 Oct says 28 project guides, 307 local authority paths and 28 tools; older project planning assumptions mention different counts. Inventory ACTUAL repository/build: don't use stale figures.

## Additional mandatory owner preference: NO duplicate URL bloat

The owner specifically does not want a vast mass of **unindexed duplicate pages**. Treat that as a hard production requirement. See `docs/00_DUPLICATES_ARE_NOT_ALLOWED.md` if available.

- Prioritise **fewer genuinely distinct and richer canonical pages**, not keeping every old generated URL. Do not regenerate thin city/keyword permutations when their answer repeats an existing guide.
- Distinguish previously known Google URLs (historical; may persist in GSC) from URLs currently emitted by the generator.
- Eliminate duplicates at generator/source: consolidate the true content, stop emitting redundant new routes, remove legacy routes from sitemaps and internal links, set consistent preferred canonicals and use actual permanent redirects when available.
- Keep legacy URL protection for users/backlinks. If GitHub Pages cannot issue true 301s, report residual 200 pages frankly and provide a deliberate migration path. `noindex` of every duplicate is NOT the fix; neither is blocking them with robots.txt.
- Each URL must be dispositioned `KEEP_ENRICH`, `KEEP_DISTINCT`, `MERGE_REDIRECT`, `LEGACY_CANONICAL_TEMP`, `RETIRE_404_410`, `RESEARCH_BEFORE_DECISION` or `NONINDEX_UTILITY`. Never bulk redirect based on cosine/simhash similarity alone.
- Gate future generation: **zero newly generated confirmed redundant URL pages** and **zero noncanonical entries in sitemaps**. Preserve useful distinct pages even if they share legal boilerplate. Protect high-value pages and all tools.

## Autonomy / release safety

Start work immediately; first inspect repo and current generator. If this pack is present at `/seo-rebuild-pack/`, use all its data, docs and scripts. If it is absent, **this prompt is standalone**: do not block; implement repository inventory, baseline, QA systems, template fixes and pilot using these instructions, then ask for GSC data only when necessary to decide high-risk existing URLs. Do not migrate hosting or add subscriptions. Preserve original behaviour for tools and lead-capture forms. Never fake official research, sources, review dates, credentials, costs, local boundaries or legal outcomes. Prefer “not verified — check the official source” over a misleading assertion, BUT do not count a generic disclaimer as standalone unique content.

**MANDATORY WORK SEQUENCE (make actual commits/PR with checks):**

### A. Baseline and complete inventory — do before content rewrite

1. Identify framework, generators, data feeds, template families, emitted page count, output directory, sitemap generator, robots, meta tags, canonicals, internal links, current hosting/router, deployed build workflow.
2. Build repository-derived **one row per emitted HTML URL** manifest: URL, page type, local authority ID, nation, project, planning topic, title, H1, canonical, indexability, cited source IDs, outgoing/incoming internal links, important content hashes and tokens, last genuine updated date. Include output statuses if live crawl is available.
3. Compare all sitemap URLs against built indexable canonical 200 pages; identify orphans, unreachable pages, duplicate title/H1/content, wrong-topic text, missing source evidence, broken internal links, legacy paths, redirect/hreflang/robots conflicts, leading/trailing slash conflicts.
4. Produce cohort report of indexable vs intentionally excluded vs duplicate candidates vs invalid vs needing evidence. Do not pretend the GSC 35,195 known URLs are all in current build.
5. If internet access is available, use official host robots + sitemap and rate-limited crawl. If not, state it and complete static-output/repo audit anyway. DO NOT label unrun checks completed.
6. Preserve a before/after diff of canonical URL inventory and a protected list for clicked URLs.

### B. Fix critical content correctness at GENERATOR level

7. Trace rule selection and defaults that cause garden room/height/HMO/conservation mismatches. Separate nation-specific planning rule models, projects, general topics and site-context overlays. A project-neutral topic page must not silently become an answer about a single project.
8. Write automated assertions for each project × 4 nations × topic where valid. Catch incompatible height/area/depth claims, false “permission not needed,” inappropriate project details, authority/nation bleed, stale dated claims, source claims without evidence.
9. Make the top “quick answer” responsive to the actual page intent; distinguish known general rule, known confirmed local overlay, unverified property detail, and next step. Avoid declaring “Article 4 applies” without exact direction/map/effective date.
10. Fix dates/provenance: `datePublished`, `dateModified` and visible “last reviewed” must reflect genuine changes/checks, not regenerated build time. Declare who authored/published and that this is independent information, not official council advice or expert certification.

### C. Substantive useful content for ALL existing page TYPES, without mass fluff

11. Define and implement rich reusable content data model: jurisdiction, project facts, qualified legal rule with exceptions, official source + exact proposition/source location + check date + published/effective date where available, evidence status, exact authority/council service links, relevant local direction/area, local plan/design/validation routes, eligibility decision tree, examples, definitions, diagrams where genuinely useful, accessibility, uncertainty, next action.
12. Build specific templates for:
  - national project guides: answer first, law scope, thresholds with exceptions, what triggers permission, edge cases, real worked examples, measurements, flowchart, downloadable checklist, official sources;
  - nation-specific planning/rule hubs: England, Wales, Scotland, Northern Ireland clearly separated;
  - local council profiles: official services, application portal, local validation, planning policies, constraint maps, adopted local guidance, current directions, selected project pointers;
  - project × council pages: national baseline + **sourced meaningful local differences**, exact checks and worked scenarios, not just inserted place names;
  - HMO/Article 4: distinguish planning use class from licensing, C3→C4 from sui generis, whether the PD right exists, local direction scope/date/map and uncertainty, avoid claiming a direction without source;
  - rule × council pages (Article 4, conservation, listed building, height, boundary etc.): verified topic-specific local material or deliberately merged into stronger useful page;
  - local-search/search-intent pages: only if they uniquely answer a real query beyond routing; otherwise propose specific consolidation mapping;
  - FAQs, tools, workflows and downloads: genuinely solve a user task; tools show input assumptions, calculation basis, jurisdiction, exclusions, uncertainty and printable/reusable result.
13. No fake length targets, spun introductions, copied council text, templated FAQs on every page or excessive footers full of project links. Short pages are acceptable when they answer their question completely. Content is authored from an evidence model; never ask AI to invent the local substance.
14. For every existing page, generate a content QA finding and improvements. Record blockers per page. Do NOT represent research backlog as completed factual enrichment. Actual verified enrichment must be source-driven, ideally scheduled council batches, with audit trail.

### D. Indexability / canonical architecture

15. Make exactly one preferred indexable canonical per **distinct user intent**, not per randomly generated keyword combination. Preserve strong historical URLs where sensible; map duplicate/legacy candidates with clicks, links, intended replacement, reason, redirect viability and confidence. Escalate uncertain mappings for review; never execute destructive redirects blindly.
16. Fix sitemap root/index/sharding (<=50,000 URLs and <=50MB uncompressed per file); include only intended indexable canonical successful URLs; truthful `lastmod`; consistent internal links, HTTPS/www/trailing slash and appropriate redirect behaviour on the ACTUAL host.
17. Handle missing pages appropriately: restore valuable moved content or equivalent, real 404/410 for gone content where supported; avoid “soft 404” moved-content shells. Do not block needed pages via robots.txt or misuse noindex for canonicalization.
18. Ensure descriptive non-duplicated titles/H1/meta descriptions, breadcrumbs and relevant schema (only truthful supported types; do not chase FAQ rich-result hacks). Check mobile rendering, JS-free crawlable body and links, accessible tools and fast initial load.
19. Expand indexability **only as earned**: source-complete unique pages, not bulk toggling index/noindex. Maintain a review backlog for source-deficient local pages. This is a quality-first programme, not an artificial 100% indexation trick.

### E. Pilot, validate and release

20. Implement pilot covering England, Wales, Scotland, and NI where the site has pages; at minimum: a currently clicked fences/walls, driveways or solar page; one general topic × locality; one council old/new path; one HMO Article 4; one local-search overlap; one tool. Include Flintshire/Cardiff/Milton Keynes/Tamworth/Nuneaton where present.
21. Compare before vs after rendered pages; tests for topic, jurisdiction, accuracy-evidence linkage, canonical/sitemap reconciliation, navigation, mobile/accessibility and functionality. CI must fail on objective errors. Keep subjective quality review separate.
22. No destructive deployment until release gate: zero broken internal links in changed cohort, zero canonical contradictions, zero sitemap invalid URLs, zero false verified badges, zero wrong-jurisdiction legal statements, no loss of protected URLs/tools. On GitHub Pages, do NOT assume host-level 301 redirects are possible; implement safely or report a host constraint with alternatives.
23. Generate summary for mobile: exact files changed, URLs affected, before/after counts by category, tests passing/failing, content quality improved, unresolved official source needs, SEO/GSC comparison date and next sensible batch.
24. Roll out by family and council research batches, not a simultaneous rewrite of tens of thousands of URLs. Codex may automate truthful template/data improvements sitewide where testable, but location-specific fact verification needs explicit primary evidence.

## Acceptance tests / definition of done

- Every existing generated URL is inventoried, categorised, and given an explicit indexability/content/evidence disposition.
- Every indexable URL has unique purpose, correct nation and topic, accurate answer first, relevant useful local/national content, provenance, appropriate 200/canonical/link/sitemap signals.
- Every legal/local assertion has evidence provenance or is clearly qualified, with no unsupported “verified” badge.
- No obsolete duplicate public URLs remain as misleading 200 moved shells **without a justified migration decision**; no indexable near-doorways.
- All existing high-performing page families and functioning tools remain accessible and improved rather than lost.
- Reproducible generator-level QA, release report, complete backlog and risk-reviewed rollout.
- The plan for measuring indexed eligible URLs, not “index every known URL,” uses Search Console on 7/28/56-day time frames; the site isn't called fixed solely because sitemap submission succeeded.

**Start now:** show repo topology/generator and produce an actual baseline artifact. Then commit Phase A + safe Phase B fixes and a representative content pilot; continue according to gated playbooks. Don't stop after writing a nice plan. If repository checkout lacks rights or an external source is unavailable, execute the portions you can, then identify exactly what prevented the remainder. Only ask a question when a genuinely irreversible/paid action requires consent.
