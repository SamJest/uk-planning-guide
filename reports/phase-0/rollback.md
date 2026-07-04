# Phase 0 Rollback

Phase 0 has not been deployed, so rollback is currently branch-only:

1. Do not merge or deploy `feature/phase-0-integrity-trust`.
2. Continue serving the existing `main` deployment snapshot.
3. Remove `artifacts/phase-0-canary-site/` locally if the review build is no longer needed.

If Phase 0 is later merged, revert its five commits in reverse order. Do not rewrite the recovered repository history. Any future host-level redirect must be rolled back separately from the static HTML bridge.
