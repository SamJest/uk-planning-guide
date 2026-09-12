# UKPlanningGuide repair and release — 12 September 2026

This report supersedes the outstanding-work section of `production-repair-2026-09-11.md`. The user explicitly authorised completing the repairs and redeploying the site. Deployment details are recorded below when publication is verified.

## Root causes and repairs

1. Two independent loaders could inherit England's rules when Welsh or Scottish data was missing. Both now use `utils/jurisdiction_rules.py`, require explicit jurisdiction and official sources, and reject unverified local overrides. Six extension variants use separate England/Wales/Scotland modules. The other 22 published project types now have separate Welsh and Scottish records. Where a numerical rule cannot be justified, the record provides scoped official guidance and questions instead of invented thresholds. Porches do not inherit extension rules.
2. Internal editorial instructions and repeated decision advice leaked through shared components. Templates and generators now publish visitor-facing wording; blocking whole-output checks cover forbidden phrases and nation leakage. Cardiff's measured main content fell from approximately 4,500 to 2,690 words through removal of repetition and misleading source descriptions.
3. Separate trust implementations allowed unverified sources with high confidence and implied named human review. A shared trust model prevents invalid combinations, omits confidence for utility pages and describes the editorial process accurately. Source-check dates remain separate from content-update dates.
4. Source-link titles had been expanded into apparent council facts. Source cards now describe links neutrally; actual structured local facts retain source URLs and check dates. Sparse pages stay short. Somerset uses the visible Council label without changing its URLs.
5. Calculators presented England-only measurements as UK-wide rules, treated blank values as zero, and confused total height with eaves height. Both numerical decision tools now require a nation. The measurement tool validates inputs and restricts its numerical check to an initial England single-storey rear-extension check; other nations and project types receive appropriate official guidance.
6. Sticky Export saved a bookmark, and enquiry forms could redirect to a success message without delivering anything. Export now downloads a real project summary. Save persists the page in My Planning Project. Enquiry forms prepare a reviewable email addressed to the existing public guidance address, explicitly stating that nothing has been sent. Optional sharing consent is optional. Northern Ireland does not receive the Great Britain enquiry flow.
7. Data-page and service copy implied comparators, paid reports or matching services that were not available. Source directories now link to actual official sources and describe their scope. Paid services and professional matching are not advertised as operational. Downloads accurately explains browser Print / Save as PDF.
8. A blocking configuration script and an uncompressed development server distorted loading performance. The route-check configuration and script now defer in order. The local production-style preview supports gzip and real HTTP 404s. Browser CI uses the platform of the reviewed Windows baselines; performance remains a separate job.

## Changed implementation

Core changes are in `utils/jurisdiction_rules.py`, `utils/trust_status.py`, `utils/production_content.py`, both data loaders, `core/render.py`, `components/rules.py`, authority/source/editorial components, `templates/base.html`, project-tracker and route-check JavaScript, calculator/decision/form components, and the council/scenario/site/upgrade generators. Data changes include nation-specific rule modules, trust contracts, Somerset metadata, and honest data-directory descriptions.

Build and release tooling includes `build_site.py`, `scripts/site_content_qa.py`, `scripts/prepare_production_repair.py`, `scripts/refresh_tool_pages.py`, `scripts/audit_site_links.py`, `scripts/package_production_repair.py`, `scripts/serve_site.cjs`, and the canary CI workflow. The release packager checks every HTML file, records before/after hashes, retains production-only files and requires the expected production base.

## Validation

Commands use the bundled Python runtime and Node CLI on this host.

| Check | Result |
| --- | --- |
| Full isolated build, `python build_site.py --full --output-dir artifacts/builds/production-repair` | All 18 generation stages and full content checks passed; 35,218 HTML files |
| Production generator/component refreshes | Shared repairs propagated across the corpus; 44 additional nation records rendered |
| Final canary build, `python build_site.py --output-dir artifacts/builds/repair-canary --validation-baseline artifacts/builds/production-repair` | All 11 stages and contract validation passed |
| `python -m unittest discover -s tests -v` | 65 passed, one generated-canary check skipped while the concurrent build was incomplete |
| Separate final `test_phase0_canary_output.py` run | Passed against the completed, fingerprint-matching canary; all 66 tests therefore exercised successfully |
| Native Node tests | 4 passed, including jurisdiction isolation, static preview and receiver validation |
| `node scripts/tool_smoke_test.js` with the full candidate output | All tool checks passed |
| Final Playwright run, `test --workers=1` | 70 passed in 3.7 minutes; desktop/mobile contracts, keyboard, accessibility, visual checks and functional journeys |
| Whole-site link and sitemap audit | 35,218 HTML files; zero broken internal links and zero missing, noindex or noncanonical sitemap members |
| `git diff --check` | Passed |

The earlier screenshot-review run had 69 passes and one accessibility-scan timeout under concurrent load. The complete final run passed without updating screenshots. Performance results and exact release hashes are appended after the final gates finish.

## Representative inspection

Reviewed generated pages include `/house-extensions/somerset/somerset/`, `/house-extensions/wales/cardiff/`, `/two-storey-extensions/wales/powys/`, `/house-extensions/scotland/aberdeen-city/`, `/two-storey-extensions/scotland/city-of-edinburgh/`, `/my-planning-project/`, `/downloads/`, `/about/`, `/methodology/`, `/england/councils/colchester/`, and `/councils/somerset/`. The review checked one H1, canonical, source/trust presentation, mobile overflow and concise sparse content. Browser regressions additionally exercise all four nation choices, invalid calculator inputs, saving, downloading and email draft preparation without sending messages.

## Deliberate scope and remaining maintenance

Northern Ireland remains a separately signposted official-guidance handoff, not a supported rule engine. Unproven scraped local rules remain quarantined; council restrictions and property-specific rights still require current official evidence. Legacy England modules with no fresh verification remain labelled accordingly. This repair does not claim that every council policy has been freshly rechecked.

Enquiries use an explicit email draft that the visitor reviews and sends in their email application. There is no claim of automatic delivery, an operational professional network or a paid report service. These are product capabilities that require an actual operated service, not hidden form-success messages.

No URL migrations, new redirect policies or canonical changes were introduced for cosmetic reasons. Routine future work is refreshing dated council sources and improving long-source typography; neither should be replaced by fabricated local detail.

## Deployment evidence

Pending final packaging and publication verification. The production base is `708e972d7bff967ed6b99a4cdc821983b34c4a55`; the isolated release checkout is `artifacts/production-release`. Rollback uses a normal revert of the release commit, never a reset or force push.
