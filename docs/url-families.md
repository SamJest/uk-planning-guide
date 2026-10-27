# URL Families

The existing output contains 35,216 `index.html` routes. The largest legacy families are project-first paths such as `/garden-rooms/{county}/{authority}/`, plus rule suffixes and combination routes. Country-first aliases under `/england/`, `/wales/` and `/scotland/` were added later and are capped by the alias generator.

Phase 0 contracts use these families:

- `national_guide`: homepage, hubs, downloads and FAQ guidance.
- `project_guide`: one project with no selected authority.
- `rule_guide`: one planning rule with no selected project or authority.
- `authority_profile`: one authority with no selected project or rule.
- `local_project`: an explicit authority and project.
- `local_rule`: an explicit authority and rule, without an inferred project.
- `tool`, `workflow`, `news`, `data_report`.

The canonical route is stored in each `PageRecord`. Legacy routes are explicit `RedirectRecord` entries. Navigation, canonicals, sitemap inclusion and redirect checks consume the same registry.

The Phase 0 canary is fixed in `data/canary/routes.json`. `/councils/colchester/` is retained as a noindex static bridge to `/england/councils/colchester/`; GitHub Pages cannot guarantee a true HTTP 301.

