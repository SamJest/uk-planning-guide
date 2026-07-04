# Phase 0 Canary Deployment

The canary is a self-contained static preview, not a replacement for the live 35,216-route site.

## Build and package

```powershell
python build_site.py
python scripts/29_package_canary.py
```

This creates `artifacts/ukpg-phase-0-canary-deploy.zip`. The packager refuses to run unless the deterministic canary report passes and all 20 published routes exist. It excludes `CNAME`, so a preview cannot claim the production domain, and includes a Netlify-compatible redirect for the legacy Colchester bridge.

## Preview deployment

Upload the ZIP to a static host at the domain root, such as a Netlify deploy preview or Cloudflare Pages Direct Upload. Do not deploy it over the production site: it deliberately contains only the 20-page canary and required internal dependencies.

After deployment, run the Playwright, axe and Lighthouse jobs against the preview URL. Human approval of those results is required before populating `docs/phase-0-signoff.json` or allowing a full build.
