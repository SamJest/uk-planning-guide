# Search Traffic Incident — 5 July 2026

## Impact

- Average daily clicks fell from 117.3 on 24–30 June to 2.0 on 1–3 July: a 98.3% decline.
- Average daily impressions fell from 7,400.6 to 298.3: a 96.0% decline.
- Average position deteriorated from 12.3 to 51.8.

## What happened

Two separate changes were visible in Search Console:

1. The submitted-page coverage cohort changed from 10,096 URLs on 12 June to 1,193 URLs on 13 June. The indexed count therefore became a measurement of a much smaller sitemap cohort; it was not evidence that every omitted route had immediately been removed from Google's index.
2. Search performance collapsed on 1 July. This followed Google's June 2026 spam update, which ran from 24 to 26 June. Google's public status dashboard reported no crawling, indexing, ranking or serving outage on 1 July.

The Phase 0 inventory strengthens the quality diagnosis. Of the exported top 1,000 landing pages, 722 were classified `repair`, 236 `noindex`, six `keep`, one `merge`, and 35 were not present in the inventory. The site contains large groups of highly similar programmatic pages; some rule pages also contain unrelated project answers.

Official references:

- https://status.search.google.com/
- https://status.search.google.com/summary
- https://developers.google.com/search/docs/essentials/spam-policies
- https://developers.google.com/search/docs/crawling-indexing/sitemaps/build-sitemap

## Immediate repair deployed

Production commit `6b7fb75e8c0637cabb6e5b52abd4b9e9f039bf79` adds a screened recovery sitemap.

- 724 historically performing URLs restored to the submitted sitemap cohort.
- Every restored URL exists, is self-canonical, is indexable, and is not marked `noindex`, `redirect`, or `410` by the inventory.
- 236 unsafe top-page URLs were deliberately excluded.
- Unsupported build-date `lastmod` values were not added.
- The live sitemap set now contains 1,917 unique URLs with no duplicates.

## Required follow-up

1. In Search Console, confirm that Manual Actions and Security Issues are empty.
2. Resubmit `https://ukplanningguide.co.uk/sitemap.xml` and inspect the new recovery sitemap.
3. Repair the highest-impression `repair` cohort first, replacing repeated/local-filler sections with authority-specific facts and sources.
4. Quarantine the 236 unsafe top-page URLs only after reviewing their replacement or consolidation route.
5. Track clicks, impressions and position daily, but judge recovery over at least seven complete days rather than incomplete recent data.

Do not restore the entire 35,000-page corpus to sitemaps. That would increase exposure to the scaled-content quality problem that likely contributed to the incident.
