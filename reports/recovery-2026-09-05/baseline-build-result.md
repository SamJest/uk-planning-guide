# Isolated source reproduction — observed failure

Source4674306, bundled Python, unique `artifacts/recovery-source-baseline-2026-09-05` directory; no existing production/output files available to the build.

Initial archive command accidentally omitted the tracked `rules/` module. That packaging omission caused a ModuleNotFoundError after2 scripts; it is an audit setup error, NOT a repository defect. The original tracked rules module was then extracted into the same isolated source. The build resumed the two unchanged completed scripts and executed all11. No application code was edited. This was a fresh-output reproduction with an interrupted/resumed run, not an uninterrupted clean-build pass.

Observed generation:31 HTML routes;20 publish-route contracts. Sum of individual script times18.49seconds. Whole-run wall-clock time is not comparable because the extraction correction interrupted it.

Validation FAILED:1,067 `broken-internal-link` occurrences, no other error codes. Examples include `/tools/`, `/workflows/`, `/building-regulations/`, `/house-extensions/`, `/councils/`. Existing validation falls back to `ROOT/output`, so the user's previous complete output made a partial canary appear self-contained. These are absent dependencies in an isolated preview; they are not verified live404s.

Report: isolated `reports/phase-0/canary-test-report.json`, SHA256 `af45de102f5033b34cefc13b9c176ab50cb8643e6887d1260154175ce586bc39`. Existing16 unit tests had passed against old local artifacts. Browser and Lighthouse remain unverified. Do not deploy a canary as a standalone replacement site.

Required correction: distinguish standalone preview validation from a bounded overlay validated against an explicit, hash-bound production baseline. Never silently borrow arbitrary `output/`. A fresh build must not clean or overwrite prior outputs; checkpoint resumption must bind to source identity.
