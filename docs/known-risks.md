# Known Risks

- **No tracked source history:** the supplied Git remote contains deployment output only. Source-level rollback is limited to commits created from this Phase 0 branch.
- **Repository bloat:** recovered Git objects occupy about 1.87 GiB because generated HTML is committed. History rewriting is excluded pending separate approval.
- **Large legacy corpus:** the current output has 35,216 routes. Inventory decisions are recommendations only; no mass deindexing or deletion occurs in Phase 0.
- **Generator inference:** legacy council and local-rule generators historically selected a priority/first project. Contract-specific authority and local-rule renderers bypass that behaviour for the canary.
- **Source freshness:** all 18 canary registry links passed the 4 July 2026 network health check. Future network failure is kept separate from deterministic builds and blocks canary release in the strict health job.
- **Static redirects:** GitHub Pages cannot return configured 301/410 responses. Phase 0 can only emit canonical/noindex bridge pages and a deployment redirect registry.
- **Inline asset weight:** the base template still contains substantial shared inline CSS and JavaScript. It is reported as a performance warning until extraction has visual-regression approval.
- **Browser tooling:** browser/a11y/performance tests require a supported Playwright browser installation. The local Edge WebView executable cannot substitute for Chromium; the supplied CI job installs Chromium explicitly.
