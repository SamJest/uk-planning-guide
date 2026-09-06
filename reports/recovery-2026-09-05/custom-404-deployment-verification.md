# Custom 404 deployment verification

Verified 6 September 2026 (UTC).

## Change path

- Production base: `7749cbba33bc06075424a82ec7f733822acfbc57`, tree `bd141850da7f1fceeb208c4e52b5b22296547d01`.
- Source implementation: `604da40abb9`.
- Clicked-404 evidence classification: `05773442d3c`.
- Exact generated deployment commit: `a1ec577bcd65bac1eb81c13349e36eb71c9d1d9f`.
- Review: [PR 16](https://github.com/SamJest/uk-planning-guide/pull/16), computed merge state clean with no required check run present.
- Production merge: `9e9db28956159587c57d88c7efebe22843f635ed`.
- Deployment: [GitHub Pages run 34042563042](https://github.com/SamJest/uk-planning-guide/actions/runs/34042563042), successful build/report/deploy jobs, completed 15:35:04 UTC.

## Counts and live result

- Existing `index.html` pages: 35,219 → 35,219.
- Special error documents: 0 → 1.
- Submitted sitemap URLs: 35,208 → 35,208, all unique.
- Redirects/restorations/deletions: zero.

A new cache-bypassed random path returned HTTP 404 and the reviewed custom recovery document. It contains `noindex, follow`, no canonical, no meta refresh and clear links into tools, councils, workflows and saved projects. GitHub serves LF while the reviewed Windows file uses CRLF; the served LF-normalised SHA-256 `b3f4009289667f7cef7c4821b8dde70f4b3537819c7f7bf4e4222ed92492887d` exactly matches the release.

## Validation

- Final source fingerprint: `5dae6496f1752bf34b150a3b5faa22ffc7aa313ffd368e837dd9bfc7a3d76644`.
- Clean canary: `artifacts/builds/recovery-404-2`, zero errors/warnings.
- Python: 36/36 passed, no skips.
- Browser: 54/54 passed across desktop/mobile, including keyboard, axe and reviewed custom-404 screenshots.
- Lighthouse: performance 0.99, accessibility 1.00, best practices 0.96, LCP 2,118 ms, CLS 0, TBT 0. Crawlability is deliberately disabled for the error document.
- Clicked missing URLs: 30/30 mapped to existing same-authority parents, covering all 91 recorded clicks; zero redirects or restorations authorised.

## Rollback

Revert deployment commit `a1ec577bcd65bac1eb81c13349e36eb71c9d1d9f` through a normal reviewed PR on latest production. This removes only `404.html`; no existing route, sitemap entry, redirect or user data is involved.
