# Current Architecture

## Build and deployment

UK Planning Guide is a Python static-site generator. `build_site.py` runs numbered scripts in `scripts/`, which call renderers in `generators/` and shared HTML builders in `components/`. Source records live under `data/`; templates and shared browser assets live under `templates/` and `assets/`.

The live build historically wrote directly to `output/`, then generated `CNAME`, `.nojekyll`, segmented sitemaps and validation reports. Phase 0 changes the default to an isolated canary at `artifacts/phase-0-canary-site/`. A full build is blocked until `docs/phase-0-signoff.json` records approval and a passing report hash.

The supplied GitHub repository, `SamJest/uk-planning-guide`, is deployment-only history: its 24 commits contain generated HTML, not this generator source. The recovered history is 1.87 GiB and tracks roughly 35,000 generated files. Generator files in this workspace therefore have no historical source baseline; Phase 0 commits must stage only intentional files.

## Main entry points

- `build_site.py`: build orchestration, output cleaning, script execution and validation.
- `scripts/1_generate_site_core.py` through `scripts/23_generate_growth_indexation_manifest.py`: ordered build stages.
- `validate.py`: existing full-output validation.
- `utils/phase0_validation.py`: isolated 20-route canary validation.
- `scripts/27_phase0_inventory.py`: read-only quality inventory of the existing live output.
- `scripts/28_source_health.py`: explicit network source-health report.

## Rendering and assets

`core/render.py` injects page content into `templates/base.html`, adds metadata and schema, and now applies the matching page contract. `core/files.py` is the common write gate. In canary mode it rejects HTML routes outside the render manifest. Most shared CSS and JavaScript remain inline in `templates/base.html`; their extraction is tracked as a Phase 0 limitation because it requires visual regression approval.

## Analytics and workspace

GA4 property `G-GXRZWRNWD7` is loaded by the base template. Existing event names and browser workspace/local-storage behaviour are preserved. Phase 0 does not add accounts, sync or alerts.

## Test and runtime state

The repository uses Python `unittest`; no Python dependency manifest was present. Browser smoke scripts exist under `scripts/`, but no tracked Node package manifest or CI workflow existed before Phase 0.

