# Search-friendly static-site generation and CI

**Repo detection:** First inspect package scripts, build output, GitHub Actions workflows, GitHub Pages config, CDN/proxy and generated page families. No host migrations, paid infrastructure, incompatible Node or Python dependencies by default.

### Crawl and indexing
- Usable `<main>` and crawlable `<a href>` navigation in initial HTML. Canonical absolute URL in `<head>`; head + sitemap + structured URL consistent. Appropriate indexable content not hidden solely behind client JS.
- One H1, unique information-scent title and description, breadcrumb as appropriate, meaningful HTML lists/tables with accessible headers.
- Only accurate JSON-LD: Organization/Website/BreadcrumbList where supported; do not use schema to imply governmental authority or reviews/FAQ eligibility that site doesn't have.
- Stable normalized preferred host and trailing slash. Sitemaps only canonical, live indexable pages. Don't create faceted/search/query route indexes accidentally.
- Distinguish historic redirects from live canonical pages and remain aware of unsupported GitHub Pages 301s.
- Optional caching/media optimization. Do not break lead capture, Cloudflare Worker D1, planning decision tools or their analytics without tests.

### Automated predeploy contract
- Read generated HTML and derive page-manifest + canonical status; compare with XML sitemap and all internal links.
- Produce `pages.csv`, `exact_duplicates.csv`, `near_duplicate_candidates.csv`, `repeated_titles.csv`, `internal_links.csv`, `broken_internal_links.csv`, `sitemap_violations.csv`, `summary.json`.
- Source-controlled approved exception/migration maps for intended duplicates and legacy routes; fail if unexpected duplicate routes enter indexable/sitemap.
- 100% of indexable pages are reachable via sitemap and/or site HTML navigation with a valid canonical; no orphan priority pages.
- Template correctness tests: no default garden room rule on generic permission/maximum-height; no wrong nation; HMO Article 4 output keyed to proper intent; no local verified claim lacking source ID.
- Tool regression tests to confirm calculators survive upgrades.
- Release in family batches and preserve rollback diff.

### Cautions
- XML sitemaps limited to 50,000 URLs and 50MB uncompressed per sitemap; use multiple shards if needed. Report actual HTTP status before claiming redirects.
- `lastmod` must be truthful and not rebuild timestamp. `meta robots noindex` on persistent low-value utility pages may be appropriate but not as default duplicate consolidation tactic.

### Duplicate prevention in new builds
Export a generator-source semantic-intent registry with stable keys, run `scripts/validate_page_registry.py` in CI **before** HTML generation, and fail if two indexable routes serve the same canonical intent or an indexable local route has no sourced local distinction (unless reviewed as a genuine tool). Run `scripts/enforce_release_gate.py` on pre/post HTML manifests. These are starter independent checks; integrate them with the actual site's generator; do not swap a proposed registry for the real build inventory.
