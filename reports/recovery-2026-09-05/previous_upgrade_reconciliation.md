# Previous upgrade reconciliation

Initial audit, before implementation. The September brief replaces earlier expansion ambitions but does not authorize discarding useful deployed work.

| Initiative / exact evidence | Live evidence | State | Decision and risk |
|---|---|---|---|
| Source contracts: `utils/content_contracts.py`, `utils/source_registry.py`, data/canary; `b1f03491d89`, `d588f5ddb8d` | Only scoped July4 output overlaid | partly complete | Retain schema and tests; extend carefully. Existing 18-source registry checked July4 needs renewed verification. |
| Canary-only default: build_site.py + docs/phase-0-signoff.json | Production later bypassed it | partly complete | Complete fail-closed standalone and release controls. Do not change approved=false. |
| `core/build_scope.py` unrestricted fallback | Legacy generic pages remain | conflicting | Replace permissive unknown/default mode behavior; local isolated builds remain possible. |
| Scripts30/31 packaging and overlay | Subsequent HomeProof/repairs absent from their stale base | obsolete | Block legacy release packaging; retain source/history for reference, use exact production-base manifest. |
| July4 country-first 20-page canary | Generated deployment c37cee | complete (deployment), partly complete (QA) | Retain useful output, do not republish whole canary. `_route_exists` fallback hides missing preview links. |
| July5 screened1,917 sitemap / reports | Replaced July10 | obsolete | Retain analytical evidence, not mechanically revert to1,917. |
| Untracked script34; July10 +33,300 sitemap | Eight full-corpus shards live | conflicting | Reject future blanket restores. Diagnose and fix evidenced technical exclusions in small batches, preserve valid memberships while quality review proceeds. |
| Untracked35/36/37; July10/13 HTML repair batches | Many corrected dropped-kerb/solar/fence pages | partly complete | Preserve exact corrected live HTML. Reject blanket string replacement/verification-date refresh and obsolete recovery-note validation. |
| Generic scenario `_best_rule_for_scenario` | PD NorthYork and Glasgow conservation infer Garden Room | conflicting | Remove project inference from generic rule intent; unsupported combinations fail. Do not regenerate all pages. |
| Council priority-project sections | Sheffield still mixes project prompts | partly complete | Audit generic authority path independently; preserve official links. |
| July22 HomeProof `aab585de49b` | Live and absent from source generator | complete (deployment), unknown (usage) | Retain URLs, JS and saved-data keys. Treat as secondary until usage supports change. No second redesign. |
| July22 language cleanup `2e3a696` | Sampled hashes match aa7d89e | complete | Preserve; prohibit reintroducing fictional editorial desk or recovery/process copy. |
| Existing user project storage/tools | Deployed browser assets | unknown (complete data flow) | Preserve keys and payload shapes; inspect before migration or monetisation. |
| Untracked backend lead worker / lead docs | Account configuration not verified | unknown | Preserve; do not activate or send personal data while inspecting. |
| QA workflow / existing16 tests | Not a production required gate; old browser44 cases failed launch | partly complete | Retain deterministic tests, add regression and negative release tests; do not count launch failures as UI/a11y passes. |
| Previous rollback docs saying not deployed | July4 onward deployment history contradicts | obsolete | Supersede operational guidance with this audit; preserve originals. |
| Growth/noindex inventory recommendations | 1,425keep/29,682repair/93merge/4,016noindex in old report | unknown | Recommendations only, not current URL decisions or permission to mass-noindex. |

## Boundaries

No conflicting uncommitted tracked edits exist. Untracked scripts/docs/backend belong to the owner and are left untouched. New source work branches from4674306; deployment changes must be an independently reviewed patch on aa7d89e or its verified successor, never a source-branch merge into main. Reconciliation updates and exact commit/test/count/deploy records accompany each completed phase.

## Reconciliation update — 6 September 2026

| Previous work | Updated state | Recovery decision |
|---|---|---|
| Phase0 build scope and sign-off | completed for containment | Missing/unknown scope fails closed; full build still requires exact report and source fingerprints. Stale package/overlay entry points are disabled. |
| Scenario and council inferred-project templates | repaired for reviewed cohorts; blocked elsewhere | North Yorkshire, Glasgow and Sheffield now use explicit records. Uncontracted local-rule/authority generation raises `ContractError` instead of borrowing project copy. No full corpus regeneration. |
| July corrected dropped-kerb, solar, HMO and Durham fence pages | retained | Semantic validation reads these from the production baseline; the release candidate does not alter them. |
| 28-tool library and HomeProof/My Planning Project | retained and reorganised | Existing URLs/storage remain. `/tools/` now leads with four capabilities and keeps the specialist library behind a secondary disclosure. |
| Monetisation service scaffolds | modified, still inactive | Added one fail-closed eligibility service, empty owner-approved partner registry, event/privacy dictionary and paid-pack input schema. No provider, partner, checkout or third-party script is active. |
| Eight opaque sitemap shards | first technical defect cohort deployed | First recovery batch removes only ten proved technical exclusions. Family-level partitioning remains a later sitemap-only cohort; no quality-unreviewed URL is removed. |
| GitHub default 404 and 30 clicked missing URLs | custom recovery deployed; URL decisions pending | Add one noindex custom error document while retaining true 404 status. Map every clicked URL to an existing same-authority parent, but authorise no redirect/restoration without equivalence or content-contract evidence. |

Validation: 36 tests pass with no skips; 24-route clean canary plus special 404 passes; three semantic repairs plus the four-capability journey pass; 27/27 registered official source URLs are reachable; browser QA passes 54/54. Production deployments: PR15 merged as `7749cbba33bc` and PR16 as `9e9db289561`; both Pages runs succeeded; live repaired pages, custom 404 and the unchanged 35,208-URL sitemap passed verification.
