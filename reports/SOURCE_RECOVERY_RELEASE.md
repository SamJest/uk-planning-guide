# Source recovery and production correctness batch — 27 October 2026

This report supersedes the previous claim that the generator was unavailable.
It was found by enumerating remote branches, then fetching
`codex/production-repair-source-2026-09-12` at
`b1ad39ae328347209d99fb30350c2ceaf5dcb38c`.

## What changed

Recovered the original Python components, generators, council/rule data, source
registry, templates, build/validation scripts, backend tests and pinned npm
lockfile. Production assets were preserved. Source imports are retained from the
original architecture; the old source branch's historical approvals and source
check dates are historical records, not a new legal or release sign-off.

The scenario summary selected the first restriction (often conservation) before
considering the requested topic. Topic-specific hints now take precedence. HMO
Article 4 summaries use a dedicated evidence checklist instead of guessed risk
and permission likelihood derived from restriction counts. The generator and
307 existing HTML pages are corrected. The summary asks for lawful use,
occupation/households, applicable right, signed direction/map/effective date and
separate licensing enquiry. It does not assert that a local direction exists.

Four existing protected project guides — fences-and-walls, driveways,
solar-panels and garden-rooms — now contain specific survey/measurement tasks,
worked preparation examples and downloadable reusable text worksheets. The
source renderer and download generator retain them on future builds. There are
no new HTML landing pages. Those 311 pages have genuine editorial modification
dates; 310 existing sitemap records were updated accordingly. One changed route
was already absent from the sitemap; it was not bulk-added without eligibility
review. Source-verification dates were not refreshed.

Pre-generation content-contract validation now rejects repeated canonical
editorial intent keys. Different nations and legacy aliases are tested
separately. This guards contracted generation; it does not certify every old
uncontracted production page as distinct. Existing full-build safety gates remain.

## Reproduce

```
npm ci
python3 -m pip install lxml==6.1.1 beautifulsoup4==4.14.2
python3 build_site.py --validation-baseline .
python3 -m unittest discover -s tests -v
python3 scripts/repair_hmo_summaries.py --check
python3 scripts/check_release.py
UKPG_OUTPUT_DIR=. node scripts/tool_smoke_test.js
node --test tests/planning_route_jurisdiction.test.cjs tests/static_preview.test.cjs backend/planning-lead-worker/test/worker.test.js
```

The default build writes an isolated `artifacts/phase-0-canary-site` candidate,
not the production tree. It generated and validated 39 pages with no content or
contract errors. Never deploy the complete source checkout as a replacement
static artifact: it now contains templates, tests and source data. Deploy only
reviewed static output through the existing publication workflow after the
release gates pass. Do not upload the isolated 39-page canary as the full site.

Narrow output refresh commands, if needed after a source edit:

```
python3 scripts/repair_hmo_summaries.py
python3 scripts/refresh_project_checklists.py
python3 scripts/refresh_correction_dates.py
```

## Validation evidence

* Final recovered Python suite plus new regressions: 74 tests passed, zero
  failures and zero skipped, after rebuilding against the final source fingerprint.
  Exact output is in `phase-0/source-recovery-python-tests.txt`.
* Node jurisdiction, static-preview and lead-worker suite: 4 tests passed. The
  notification-webhook failure text is an intentional failure-path test.
* Tool VM smoke suite: all 28 tool pages passed.
* Real desktop/mobile Chromium production journeys: 16 passed, zero skipped.
  Includes all four nation choices, calculator validation, enquiry draft/reset,
  local-storage saving and downloadable project summary.
* New Chromium survey/HMO checks: 10 passed, zero skipped; each new panel passed
  the scoped axe accessibility check and project pages had no horizontal overflow.
  This is not a claim of complete sitewide WCAG conformance.

The static scan in `source-recovery/summary.json` reports 35,220 production
HTML pages, 35,195 sitemap URLs, zero sitemap conflicts, zero broken local
anchor targets and zero remaining HMO conservation-default flags (248 at the
original baseline). The 3,986 local-evidence placeholders remain unresolved.
There are 311 changed existing public HTML files in this batch; none was added
or removed. These numbers do not count source templates as production URLs.

The browser tests use a local static server, not public HTTP. No visitor data was
submitted: the tested enquiry route prepares a local email draft. Source report
and browser outputs are current-run artifacts; historical screenshot fixtures
were not regenerated to force a pass.

## Remaining release blockers

The environment's restricted network policy allowed package registries/GitHub
but no custom official-source destinations. Government, legislation, council and
production requests returned proxy CONNECT 403, including an elevated retry.
Specific production/official research domains have now been saved to the cloud
configuration draft for review. Saving a draft does not apply runtime networking.
Review and save those settings, then publish the environment as required by the
product; retry access before claiming any research is verified.

Local source enrichment, address-level direction verification and source-freshness
review remain incomplete. The recovered source registry is useful prior evidence,
not evidence of a fresh check on 27 October. Production redirects remain untested.
GitHub API access also returned Forbidden; native Git read access works. Do not
request a token simply because the API route is blocked.

Nuneaton's local-search page was inspected against its HMO parent: it contains
generic routing rather than a checked direction/map result and even creator-facing
wording. It remains a consolidation candidate, not an implemented merge. Preserve
its traffic/backlinks while establishing the correct owner and real redirect
capability. Colchester remains an HTML canonical bridge, not a verified 301.
No mass pruning, blanket noindex, hosting migration or deployment was performed.

This batch is a substantive generator/content/functionality correction. It is not
completion of the source-research, deduplication and enrichment programme. The
23 October GSC baseline and 7/28/56-day post-publication measurement plan remain
in `RELEASE_REVIEW.md`.
