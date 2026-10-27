# Canonical URL architecture, migration discipline and hosting limits

1. Detect existing canonical URL policy using working URLs and GSC. Decide final routes *before* changing templates. Prefer keeping already successful stable URLs unless a demonstrable reason warrants moving.
2. Build explicit mapping CSV from OLD to NEW with traffic/backlink/intent/review fields and approval. Do not rename all project paths for neatness.
3. Normalisation policy: HTTPS, preferred host, predictable trailing slash, no index.html variants, no query-driven duplicate SEO landing pages. Record existing exceptions and handle them.
4. A canonical-eligible URL must return 200, self-canonical, be indexable and appear in exactly one sitemap, with crawlable HTML links and appropriate structured data identifiers.
5. Redirect deprecated alternatives using server or existing CDN edge 301/308 where configurable, test real status and single hop. GitHub Pages standalone does not expose general arbitrary server redirects. If not supported, retain temporary moved HTML shell that isn't in sitemap, canonical to winner, and linked out; explicitly report that residual 200 duplicate remains. This is a fallback, not finished migration.
6. Direct internal links/breadcrumbs/footer/sitemaps to preferred URL only; never link via a legacy path. Avoid redirect chains, loops and wholesale home redirects. Preserve useful unique content before consolidation.
7. Source and target should match actual intent; otherwise keep or properly return 404/410 (and fix internal links).
8. Keep redirects where possible for at least one year and ideally permanently for changed high-value URLs; monitor Search Console chosen canonicals, errors and traffic.
9. Excluded duplicate sources are *expected* in GSC during migration; do not aim to get them indexed. Judge eligible canonical denominator, not Google-known URLs denominator.
10. Sitemap shards <50k locs and <50MB uncompressed each. Only absolute canonical 200/indexable URLs; lastmod changes only when actually modified. Create family-level shards for diagnostics where useful, and put sitemap index in robots.txt. Verify HTTP status and XML with a live crawler when network is available.

**Migration sign-off requires** a recorded independent choice and dry-run diff for each protected URL; include `old_url,new_url,action,reason,protected,actual_http_status,internal_inlinks_after,sitemap_entries_after` in review.
