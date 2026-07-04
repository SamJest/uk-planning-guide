# Phase 0 Known Limitations

- The restored Git history is a deployment snapshot; the generator source had no tracked historical baseline.
- The in-app browser could not start because its filesystem permission parser rejected the literal `]` in this workspace path. No manual browser result or screenshot is represented as completed.
- Playwright discovered all 44 desktop/mobile checks, but the available Edge WebView executable is not a compatible browser binary and Chromium download did not complete. The suites are supplied; their first successful visual baselines still require review.
- Shared inline CSS and JavaScript remain in the base template pending visual-baseline approval. Deterministic HTML size checks remain active.
- The Colchester Article 4 local page remains noindex because an authoritative, area-specific designation source has not been established.
- GitHub Pages cannot guarantee HTTP 301 responses; the legacy bridge is canonical/noindex HTML plus a redirect registry entry.
