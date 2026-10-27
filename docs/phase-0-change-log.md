# Phase 0 Change Log

## 4 July 2026

- Restored the supplied deployment-only Git history and created `feature/phase-0-integrity-trust` without overwriting workspace files.
- Added strict page, source and redirect schemas plus a fixed 20-route canary manifest.
- Added normalized source records for national guidance, Colchester, Cardiff and City of Edinburgh.
- Made canary output the default build target and blocked full builds behind an explicit sign-off file.
- Added a shared route write gate, contract-driven canonical/index/date/source rendering, and static redirect-bridge handling.
- Added safe authority-profile and local-rule rendering paths that do not infer a priority project.
- Added contamination, jurisdiction, source, URL, redirect, inventory and canary validation utilities.
- Added read-only page-inventory and source-health report commands.
- Audited all 35,216 existing routes without changing the live corpus: 1,425 keep, 29,682 repair, 93 merge and 4,016 noindex recommendations.
- Verified all 18 registered sources as reachable in the separate network health job.
- Added Playwright, axe, Lighthouse and CI definitions for the exact canary, with visual-baseline approval retained as a human gate.
- Passed the deterministic 20-route canary validator and 16 Python unit tests. Passing report SHA-256: `3d741804c0baea51094fd2fb189c9248c46dbecb73bd1e02cc64ab1c705c210d`.

No full-site regeneration, deployment, URL deletion, mass noindex change or history rewrite was performed.
