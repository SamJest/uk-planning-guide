# Phase 0 Canary Deployment

The canary is a self-contained static preview, not a replacement for the live 35,216-route site.

## Build and package

```powershell
python build_site.py --output-dir artifacts/builds/phase-0-canary --validation-baseline .gh-pages-deploy
python scripts/29_package_canary.py
```

This creates `artifacts/ukpg-phase-0-canary-deploy.zip`. The packager refuses to run unless the deterministic canary report passes and all 20 published routes exist. It excludes `CNAME`, so a preview cannot claim the production domain, and includes a Netlify-compatible redirect for the legacy Colchester bridge.

## Preview deployment

Upload the ZIP to a static host at the domain root, such as a Netlify deploy preview or Cloudflare Pages Direct Upload. Do not deploy it over the production site: it deliberately contains only the 20-page canary and required internal dependencies.

After deployment, run the Playwright, axe and Lighthouse jobs against the preview URL. Human approval of those results is required before populating `docs/phase-0-signoff.json` or allowing a full build.

## Full-site deployment candidate (retired)

The September 2026 recovery audit disabled `scripts/30_package_full_site_candidate.py` and `scripts/31_apply_canary_to_full_output.py`. Their passing-report check was not bound to the current source or production commit, and their base output predates later production repairs and HomeProof. Keep them for history only.

Any new production candidate must name the exact production base commit, list every changed file with before/after hashes and URL-count delta, and include a normal-commit rollback map. Build/preview approval does not itself authorize publication.
