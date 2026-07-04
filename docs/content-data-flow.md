# Content and Data Flow

1. Project, council and rule data are loaded from `data/` by `data/loaders.py` and related helpers.
2. Phase 0 validates `data/canary/page-records.json`, `data/source-registry.json` and redirect/route manifests before any generator runs.
3. Numbered scripts call family generators and shared components.
4. `core/render.inject_into_base` resolves the explicit page record, centralizes canonical/index/date metadata and renders the source/review panel.
5. `core.files.write_file` converts each output path to a route and enforces the canary render allowlist.
6. `generators/upgrade_pages.py` creates country-first aliases, data pages, the review-only update and static redirect bridges.
7. Sitemap generation includes only published, indexable canary routes and uses `content_updated_at` for `lastmod`.
8. `utils/phase0_validation.py` validates the rendered output and writes the review report/hash.

Claims and local facts reference stable source IDs. Source verification dates never substitute for substantive page-update dates. Missing evidence produces visible uncertainty and `noindex`.

