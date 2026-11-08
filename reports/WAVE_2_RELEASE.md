# Wave 2 — intent governance and protected URL diagnosis

Prepared 8 November 2026. **Not deployed.** Depends on unmerged Wave 1 PR #19. This is a separate, review-only source change; neither PR is merged automatically.

## Outcome

The 21 non-exact clicked URLs are not demonstrated missing pages. Read-only GET observations of all 21 exact GSC spellings found a single HTTP 301 to the trailing-slash version followed by HTTP 200; all 21 normalized static files already exist. The raw inventory remains 954 exact URL spellings plus 21 non-exact spellings. Normalized coverage is 975. The original sample is retained unchanged, and no recovery redirect or restoration was introduced.

The prior pack's instruction to investigate “missing” routes was a hypothesis to verify, not evidence of a production defect. The earlier exact-spelling report correctly preserved those variants without claiming a live 404; this wave supplies the missing HTTP observations. Old clicked-404 analysis remains available for genuinely observed historical 404 ledgers; it is not applied to these 21 current responses.

## Implemented source changes

- `utils/intent_registry.py` exposes a deterministic six-axis key: nation, authority, project, rule topic, user question and page role. The existing contracted generation validator uses it; keyword/URL changes cannot evade collisions for the same scoped guide. Distinct nations, authorities, projects, rules and roles remain separate. Existing functions receive stable task IDs; new functional pages must declare an ID, and a second tool URL for the same task is rejected. The exported registry covers **24 contracted records / 21 self-canonical indexable intents**, not all 35,220 public pages. Same-role/scope questions conservatively remain collisions until an editorial distinction is explicitly supported.
- Sitemap validation now reads actual emitted targets and rejects absent files, outside-output paths, spoofed hosts, query/fragment variants, duplicate URLs, multiple/wrong canonicals and robots/googlebot noindex/none. It fails before XML emission; it does not “fix” a URL by rewriting or removing it. Existing URL and lastmod output is unchanged.
- The Colchester redirect record explicitly distinguishes `legacy_200_bridge` delivery from its **planned** 301 code. The sampled legacy URL returned HTTP 200. Neither the record nor a canonical hint is presented as proof of a delivered content-migration redirect. Source/target paths, canonical/noindex flags and generated HTML remain unchanged.
- Offline CI gates validate the exported registry, 21 protected decisions, six comparison cards, body hashes of reviewed static pages, and actual emitted sitemap targets. The existing migration-decision validator checks all 27 review dispositions. No migration action, approval, backlink result or reviewer was fabricated.

## Review dossier and provenance

Start with [human-readable decision cards](wave-2/DECISION_CARDS.md). The associated JSON records contain exact URLs, sample clicks/impressions or unknown, canonical/robots state, static inbound/sitemap counts, timestamped GET status chains, body digests, intent hypotheses, text-difference samples, owners and rollback instructions. [Migration decisions](wave-2/migration-decisions.csv) retain current behavior or request research; every row remains unreviewed for migration approval.

The six comparisons cover `/local-search/` versus an HMO Article 4 guide in Milton Keynes, HMO-specific versus general Article 4 pages in Milton Keynes and Tamworth, council-service versus rule roles, and Colchester's council/rule country-first aliases. All ten representative pages returned HTTP 200 directly. Text similarity and unique-looking headings are candidate signals, not independently verified unique facts. Backlinks, query cohorts and 6/12-month landing-page data were not supplied and remain unknown. Low clicks or absent sample rows never authorize retirement.

Three of the ten sampled live response bodies differ from the unmerged recovery checkout: the Milton Keynes HMO/Article 4 pages and Tamworth's HMO Article 4 page. The cards keep live metadata/text samples and recovery-branch comparisons separate; unmerged source repairs are not treated as already deployed or used as proof that live content is redundant. All 21 normalization response bodies match their existing normalized static files (with Git line endings normalized).

Thirty-one exact read-only GET captures were made: 21 protected variants and ten representative pages. Their exact UTC timestamps and status/header chains are retained per record. These are historical observations, not promises of future delivery. No crawl, analytics event, paid service or data transfer to a new vendor was introduced. Raw public HTML/header captures remain in local evidence. [GitHub's documentation](https://docs.github.com/en/pages/getting-started-with-github-pages/what-is-github-pages) describes Pages as static hosting; the observed directory normalization is not evidence that arbitrary content migrations can be delivered as HTTP redirects. Any future host or redirect change needs its own approved and verified plan.

## Before versus after

| Measure | Before | After |
|---|---:|---:|
| Public HTML / sitemap URLs | 35,220 / 35,195 | unchanged |
| Candidate HTML / files | 39 / 78 | 39 / 78 |
| Candidate HTML, assets or sitemap bytes changed | — | 0 |
| Contracted records / self-canonical indexable intents | 24 / 21 | 24 / 21 |
| Raw clicked sample exact / non-exact spellings | 954 / 21 | 954 / 21 |
| Non-exact variants with current HTTP normalization evidence | 0 | 21 |
| Confirmed merges / approved retirements / new migrations | 0 / 0 / 0 | 0 / 0 / 0 |
| Python tests | 95 | 111 |

The full public-corpus baseline is the passing Wave 1 inventory; this wave's preservation gate forbids publishing-tree changes. All 77 candidate files other than `BUILD-MANIFEST.json` are byte-identical. No visible design change occurred, so no screenshot baseline was updated. The existing desktop/mobile keyboard/axe/screenshot suite remains a release gate.

## Validation and release boundary

See `WAVE_2_EVIDENCE.json` for actual check status, logs/SHAs and CI links. Local fresh build and all 111 Python tests passed with zero skips. Existing pack, Node, tool, browser, pilot/HMO/release and Lighthouse gates are retained without lowered thresholds. Review-only cards do not constitute approval to merge, deploy, retire a route, issue a new redirect, change canonicals or noindex pages.

Rollback is reverting this source-only governance PR; no production recovery is needed. Review Wave 1 before the dependent Wave 2 PR, then approve any later work separately. The next pack wave is the route-check → guide → local check → save/export journey, with five realistic mobile/desktop tasks. The previously proposed compact mobile trust/source presentation belongs with those UX improvements after this governance step, not ahead of it.
