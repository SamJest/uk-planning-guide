# 27 October 2026: inventory and correctness pilot — NOT a full-site release approval

## Repository and reproducibility

Baseline commit: `bb01d67fc58f21400dffbf449604ee05d561abbc`.
The root is the published static tree: `.nojekyll`, `CNAME`, HTML directories,
`assets/`, `sitemap.xml`, `sitemaps/`, `robots.txt`. No original page generator,
template source, council feed, package/build manifest or deployment workflow was
present. `workflows/` contains public user journeys, not deployment configuration.
The original generator and its default-selection implementation cannot be traced
from this checkout. Do not present the repair layer as recovery of that source.
GitHub Pages is indicated by the tree, but the actual serving infrastructure and
deployment settings have not been independently confirmed.

Commands (Python 3.12, lxml 6.1.1):

```
python3 scripts/inventory.py --revision bb01d67fc58f21400dffbf449604ee05d561abbc --output reports/baseline
python3 scripts/repair_pilot.py
python3 scripts/inventory.py --output reports/after
python3 scripts/compare_inventory.py
python3 scripts/repair_pilot.py --check
python3 -m unittest discover -s tests -v
python3 scripts/check_release.py
```

Large CSV artifacts are gzip-compressed after comparison. Decompress them before
rerunning comparison. Baseline is explicitly read from Git for changed HTML;
the final audit reads current files. No original build command exists to run.

## Baseline and final outcome

35,220 emitted HTML files; 35,195 unique sitemap entries. Before and after:
zero missing-file/noncanonical/noindex sitemap violations, zero oversized shards,
zero unresolved local anchor targets, zero incoming-link orphans under this
scanner's graph. These are filesystem checks, not HTTP, robots-header or legal
verification. Existing title, H1 and main-text hash clusters are candidates only.

Every emitted URL has a manifest row and disposition: 14 NONINDEX_UTILITY,
10 LEGACY_CANONICAL_TEMP and 35,196 RESEARCH_BEFORE_DECISION. The latter is a
conservative review queue, not a finding that all those pages are duplicates or
adequate indexables. No route was added, removed, redirected or newly noindexed.
3,986 pages contain the local-evidence placeholder; these remain a research
backlog, not completed enrichment. HMO Article 4 default flags: 248 before,
247 after; only Tamworth was repaired in this batch.

The GSC sample contains 975 URLs with clicks; 954 exactly match current routes.
The 21 unmatched sampled URLs need variant/historical investigation. Unknown
backlinks are not zero backlinks. The full protected sample is retained in CSV.

## Five changed public pages

* `/planning-permission/flintshire/`: Welsh, project-neutral enquiry pathway;
  no imported garden-room numerical answer.
* `/maximum-height/lambeth/`: project and measurement selection before thresholds;
  no universal garden-building height claim.
* `/article-4/cardiff/`: explicitly unresolved direction, rights, boundary and dates;
  Welsh rather than assumed English route.
* `/article-4/milton-keynes/`: address/direction evidence request, separated from
  licensing and generic conservation designation.
* `/hmos/staffordshire/tamworth/article-4/`: replaces the conservation default with
  use classification/direction checks; separates licensing and planning.

The common renderer consumes explicit jurisdiction, intent, answer and steps. It
does not invent local substance or emit new URLs. Existing imported source-review
dates in these five pages are relabelled as unevidenced; the correction date is
explicitly distinguished from local source verification. Existing other dates
and claims have not all been authenticated. No new verified badge is used.

## Tests and release limits

PASS: three pilot tests (including idempotence, 60 jurisdiction/project/topic
render cases without inherited numerical thresholds, preserved script/form
connections and canonicals); six supplied-pack tests (including duplicate-intent
and unverified-doorway rejection fixtures); JavaScript syntax for all five assets;
pilot canonical/link/asset gate; representative local HTTP 200 responses for all
five changed pages, fences-and-walls, the planning-route tool, Scotland and Wales.
CI now repeats these checks. Fixture tests do not validate substantive planning
rules across every project/nation: that evidence model still needs upstream data.

NOT VERIFIED: production HTTP, real permanent redirects, official local source
research, mobile visual/accessibility review and interactive form/calculator
results. Production robots/sitemap/Colchester requests received proxy CONNECT
403, including an elevated retry. Chromium was attempted with a writable profile
but did not produce a completed screenshot; no visual pass is claimed.
Scripts and lead-capture configuration are unchanged; preservation is not an
end-to-end functional test. No Northern Ireland output directory exists.

Colchester old/new: old HTML is a canonical bridge to the England council page;
this is not proof of an HTTP redirect. Retained pending host and backlink checks.
Nuneaton local-search/HMO overlap: retained for review, no similarity-based merge.
No sitemap rewrite is warranted by the objective baseline. Canonical eligibility
is not a finding of distinctness, quality or indexing.

## Next bounded batches and blockers

1. Recover the original generator and council/rule data from the publishing
   project or prior source repository. Integrate the repair contract there before
   regenerating; otherwise upstream output may overwrite these corrections.
2. Make official council/legislation sources reachable, then research Cardiff,
   Milton Keynes and Tamworth directions with proposition, map, effective date,
   retrieval date and stable evidence ID. No authoritative check date was invented.
3. Review Nuneaton and Colchester pairs with primary content, traffic, backlinks
   and actual serving capabilities. Keep migration decisions reversible and
   eliminate confirmed redundant source records only after that review.
4. Expand the corrected HMO default by nation, with legal evidence and regression
   coverage, then general-topic and council families. Preserve protected families.
5. Complete the protected project/tool/Scottish content pilot and real mobile/tool
   interaction checks before release. Broad sitewide enrichment is not complete.

## Measurement

Comparison anchor: GSC coverage 23 October (10,840 indexed; 24,355 excluded;
17,013 crawled-not-indexed; 6,737 discovered-not-indexed; 593 alternate canonicals).
Performance windows remain 16–25 versus 6–15 October, with export sampling caveat.
At 7/28/56 days after any actual publication, compare submitted eligible canonical
URLs by family, chosen canonical, exclusions, clicks and impressions using fixed
windows. Historical known URLs are not the emitted-site denominator. No deployment,
sitemap submission, indexing improvement or Google acceptance is claimed here.
