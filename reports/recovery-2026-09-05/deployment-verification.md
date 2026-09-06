# Recovery batch deployment verification

Verified 6 September 2026 (UTC).

## Change path

- Audited production base: `aa7d89ec029c70d5973b7d982fcbe5036316d9b2`, tree `9c640ff1b40473f2e025e9368ac008d41b1e5cc5`.
- Exact generated branch: `codex/recovery-batch-2026-09-06`.
- Eight-file deployment commit: `f7a308662faa81ddc3cb2253f142ba6765e087d9`.
- Review: [PR 15](https://github.com/SamJest/uk-planning-guide/pull/15).
- Production merge: `7749cbba33bc06075424a82ec7f733822acfbc57`.
- Deployment: [GitHub Pages run 34022456093](https://github.com/SamJest/uk-planning-guide/actions/runs/34022456093), successful build/report/deploy jobs.

Remote `main` was still the audited base immediately before merge and the PR merge used the expected exact head SHA. No branch protection was bypassed and no deployment setting changed.

## Public verification

The four changed routes returned HTTP 200, their own canonical URL, and no `noindex`:

- `/permitted-development/north-yorkshire/`
- `/conservation-areas/glasgow-city/`
- `/councils/sheffield/`
- `/tools/`

GitHub's served files use LF while the reviewed Windows files use CRLF. After LF normalisation, each public response SHA-256 exactly matches its reviewed release file. Response `Last-Modified` values are from the successful September deployment.

All eight cache-bypassed public sitemap shards returned HTTP 200. Counts were `5,000 / 4,996 / 5,000 / 5,000 / 4,996 / 5,000 / 4,999 / 217`: 35,208 total and 35,208 unique. None of the ten proved noindex/noncanonical exclusions remained submitted. Static page count remains 35,219; no path, redirect or deletion changed.

## Rollback

If this batch causes a verified regression, create a normal reviewed revert of deployment commit `f7a308662faa81ddc3cb2253f142ba6765e087d9` against the latest production branch. That restores the four prior HTML files and four prior XML files, returns sitemap membership to 35,218, and leaves all pages and unrelated later work intact. Do not reset, force-push or regenerate the corpus.

## Non-blocking observation

The Pages build emitted a Node.js 20 deprecation warning for `actions/upload-artifact@v4` being forced to Node.js 24. The workflow completed successfully; this is maintenance evidence, not a failed release or an immediate content rollback trigger.
