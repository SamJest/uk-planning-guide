# Wave 2 decision cards — review only

No merge, retirement, URL rewrite or indexation change is authorized by this dossier. Current HTTP observations are timestamped GET captures, not a guarantee of future behavior. The ranked GSC sample has no supplied 6/12-month window, query cohort or backlink export. Absent rows are unknown, not zero.

## The 21 raw GSC spelling mismatches

All 21 have an existing normalized static page and were observed redirecting once with HTTP 301 to the trailing-slash URL, then HTTP 200. Preserve their existing behavior. These were never demonstrated missing pages by the static exact-spelling count.

| Sample path | Clicks / impressions | Observed response | Current canonical | Decision |
|---|---:|---|---|---|
| `/change-of-use/somerset/somerset/permitted-development` | 1 / 13 | 301 → 200 | `/change-of-use/somerset/somerset/permitted-development/` | Keep current behavior |
| `/councils/dacorum` | 1 / 43 | 301 → 200 | `/councils/dacorum/` | Keep current behavior |
| `/councils/pembrokeshire-coast-national-park` | 1 / 27 | 301 → 200 | `/councils/pembrokeshire-coast-national-park/` | Keep current behavior |
| `/councils/sunderland` | 1 / 33 | 301 → 200 | `/councils/sunderland/` | Keep current behavior |
| `/driveways/greater-london/barking-and-dagenham/permitted-development` | 1 / 1 | 301 → 200 | `/driveways/greater-london/barking-and-dagenham/permitted-development/` | Keep current behavior |
| `/fences-and-walls/shropshire/shropshire/maximum-height` | 1 / 5 | 301 → 200 | `/fences-and-walls/shropshire/shropshire/maximum-height/` | Keep current behavior |
| `/fences-and-walls/staffordshire/stafford/planning-permission` | 1 / 1 | 301 → 200 | `/fences-and-walls/staffordshire/stafford/planning-permission/` | Keep current behavior |
| `/fences-and-walls/wales/newport` | 1 / 2 | 301 → 200 | `/fences-and-walls/wales/newport/` | Keep current behavior |
| `/garage-conversions/east-sussex/eastbourne/planning-permission` | 1 / 1 | 301 → 200 | `/garage-conversions/east-sussex/eastbourne/planning-permission/` | Keep current behavior |
| `/garage-conversions/essex/braintree/permitted-development` | 1 / 1 | 301 → 200 | `/garage-conversions/essex/braintree/permitted-development/` | Keep current behavior |
| `/garage-conversions/shropshire/shropshire/planning-permission` | 1 / 25 | 301 → 200 | `/garage-conversions/shropshire/shropshire/planning-permission/` | Keep current behavior |
| `/garden-rooms/greater-london/haringey/height-limits` | 1 / 2 | 301 → 200 | `/garden-rooms/greater-london/haringey/height-limits/` | Keep current behavior |
| `/garden-rooms/hampshire/basingstoke-and-deane` | 1 / 4 | 301 → 200 | `/garden-rooms/hampshire/basingstoke-and-deane/` | Keep current behavior |
| `/garden-rooms/staffordshire/east-staffordshire` | 1 / 2 | 301 → 200 | `/garden-rooms/staffordshire/east-staffordshire/` | Keep current behavior |
| `/house-extensions/somerset/bath-and-north-east-somerset/permitted-development` | 1 / 2 | 301 → 200 | `/house-extensions/somerset/bath-and-north-east-somerset/permitted-development/` | Keep current behavior |
| `/outbuildings/hampshire/gosport` | 1 / 4 | 301 → 200 | `/outbuildings/hampshire/gosport/` | Keep current behavior |
| `/outbuildings/oxfordshire/west-oxfordshire/height-limits` | 1 / 1 | 301 → 200 | `/outbuildings/oxfordshire/west-oxfordshire/height-limits/` | Keep current behavior |
| `/permitted-development/huntingdonshire` | 1 / 3 | 301 → 200 | `/permitted-development/huntingdonshire/` | Keep current behavior |
| `/porches/staffordshire/stafford` | 1 / 1 | 301 → 200 | `/porches/staffordshire/stafford/` | Keep current behavior |
| `/single-storey-extensions/hampshire/east-hampshire/planning-permission` | 1 / 2 | 301 → 200 | `/single-storey-extensions/hampshire/east-hampshire/planning-permission/` | Keep current behavior |
| `/solar-panels/wales/monmouthshire` | 1 / 10 | 301 → 200 | `/solar-panels/wales/monmouthshire/` | Keep current behavior |

## Representative overlapping families

The six comparisons are hypotheses about user jobs. Text overlap, low clicks, headings and common place names do not establish duplicate legal facts or authorize consolidation. Detailed provenance, canonicals, robots, static inbound counts, metrics and text-difference samples are in `overlap-decisions.json`.

### local-search-vs-hmo-milton-keynes

- Source: `/local-search/hmo-article-4-milton-keynes/` — 0 clicks / 1187 impressions.
- Comparison: `/hmos/buckinghamshire/milton-keynes/article-4/` — unknown (not present in supplied ranked sample).
- Hypothesis: HMO/Article 4 search landing versus HMO rule guide. Query coverage, authority evidence and unique value need review.
- Token-sequence overlap: 0.2043; candidate signal only.
- Decision: **unknown**. Approval: none. Both sampled URLs currently returned HTTP 200; no content-migration redirect was observed.
- Unique factual value: not independently established. Backlinks and 6/12-month query/landing cohorts: unknown.
- Rollback: retain both exact files and their current canonical/robots/sitemap state; no migration map is activated.

### hmo-vs-general-article4-milton-keynes

- Source: `/hmos/buckinghamshire/milton-keynes/article-4/` — unknown (not present in supplied ranked sample).
- Comparison: `/article-4/milton-keynes/` — unknown (not present in supplied ranked sample).
- Hypothesis: HMO change-of-use question and general permitted-development restrictions may differ; shared keywords do not prove equivalence.
- Token-sequence overlap: 0.1418; candidate signal only.
- Decision: **unknown**. Approval: none. Both sampled URLs currently returned HTTP 200; no content-migration redirect was observed.
- Unique factual value: not independently established. Backlinks and 6/12-month query/landing cohorts: unknown.
- Rollback: retain both exact files and their current canonical/robots/sitemap state; no migration map is activated.

### authority-vs-rule-milton-keynes

- Source: `/councils/milton-keynes/` — unknown (not present in supplied ranked sample).
- Comparison: `/article-4/milton-keynes/` — unknown (not present in supplied ranked sample).
- Hypothesis: Authority services and an Article 4 question have different roles. No consolidation on the basis of common place names.
- Token-sequence overlap: 0.4424; candidate signal only.
- Decision: **keep**. Approval: none. Both sampled URLs currently returned HTTP 200; no content-migration redirect was observed.
- Unique factual value: not independently established. Backlinks and 6/12-month query/landing cohorts: unknown.
- Rollback: retain both exact files and their current canonical/robots/sitemap state; no migration map is activated.

### council-country-alias-colchester

- Source: `/councils/colchester/` — unknown (not present in supplied ranked sample).
- Comparison: `/england/councils/colchester/` — 1 clicks / 103 impressions.
- Hypothesis: Retain the existing bridge behavior pending a separately approved hosting/migration decision; a canonical hint is not an HTTP 301.
- Token-sequence overlap: 1.0; candidate signal only.
- Decision: **keep**. Approval: none. Both sampled URLs currently returned HTTP 200; no content-migration redirect was observed.
- Unique factual value: not independently established. Backlinks and 6/12-month query/landing cohorts: unknown.
- Rollback: retain both exact files and their current canonical/robots/sitemap state; no migration map is activated.

### rule-country-alias-colchester

- Source: `/article-4/colchester/` — 2 clicks / 7 impressions.
- Comparison: `/england/rules/article-4/colchester/` — unknown (not present in supplied ranked sample).
- Hypothesis: Inspect existing canonical/noindex policy and query demand before any change. Neither equivalent HTTP redirects nor legal applicability are assumed.
- Token-sequence overlap: 1.0; candidate signal only.
- Decision: **unknown**. Approval: none. Both sampled URLs currently returned HTTP 200; no content-migration redirect was observed.
- Unique factual value: not independently established. Backlinks and 6/12-month query/landing cohorts: unknown.
- Rollback: retain both exact files and their current canonical/robots/sitemap state; no migration map is activated.

### hmo-vs-general-article4-tamworth

- Source: `/hmos/staffordshire/tamworth/article-4/` — 0 clicks / 1383 impressions.
- Comparison: `/article-4/tamworth/` — unknown (not present in supplied ranked sample).
- Hypothesis: HMO-specific decisions and the general rule page require distinct factual evidence before an equivalence decision.
- Token-sequence overlap: 0.1225; candidate signal only.
- Decision: **unknown**. Approval: none. Both sampled URLs currently returned HTTP 200; no content-migration redirect was observed.
- Unique factual value: not independently established. Backlinks and 6/12-month query/landing cohorts: unknown.
- Rollback: retain both exact files and their current canonical/robots/sitemap state; no migration map is activated.

## Owner review queue

Keep all 21 normalization routes. Review the six overlapping pairs using query/landing cohorts, backlinks and source-backed unique value before any consolidation. Any future retirement needs separate owner approval, an exact rollback map and verified HTTP migration capability. The existing Colchester council bridge returned HTTP 200; its planned 301 code is not represented as delivered.

The authoritative emitted-intent gate covers 24 contracted records / 21 self-canonical indexable intents. It does not certify semantic uniqueness across all 35,220 public pages. Closely related same-role/scope questions remain conservative collision failures until an explicit editorial distinction is implemented and evidenced.
