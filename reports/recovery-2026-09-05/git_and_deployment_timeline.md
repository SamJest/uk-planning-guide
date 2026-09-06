# Git and deployment timeline

All deployment timestamps below UTC, read from GitHub Actions on 5 September. Source and generated-output commits must not be confused. Full parents and authored/committed timestamps: `baseline/git-timeline.txt`.

| Production merge | Change | HTML routes / sitemap URLs after merge | Pages completed UTC |
|---|---|---|---|
| `23349e4a1605` | June8 generated site baseline | 35,215 / 1,193 | June8 16:10:06 |
| none observed June20–July3 | No production deployment in returned history | unchanged observed Git tree | none |
| `c37cee327a56` (change `b1e21b17e7d`) | July4 20-page canary overlay, +2 routes | 35,217 / 1,193 | July4 21:01:55 |
| `6b7fb75e8c06` (`62684c0d695`) | July5 screened sitemap +724 | 35,217 / 1,917 | July5 07:13:29 |
| `52b8a0bc6a67` (`d2cfa2fd9e9`) | July10 full sitemap restore +33,300 | 35,217 / 35,217 | July10 07:07:45 |
| `933320c38438` (`e9704f89fb7`) | Repair50 | 35,217 / 35,217 | July10 08:41:33 |
| `1929340c55f9` (`7f42d52c063`) | Repair100 | unchanged | July10 10:15:39 |
| `3f6a21d5a817` (`ffdcf7afba0`) | Repair100 | unchanged | July10 10:29:52 |
| `9904d747d70c` (`a4aef4335c6`) | Repair100 | unchanged | July10 10:39:21 |
| `534bb720e613` (`0f07ec2c8d4`) | Repair100 | unchanged | July10 10:52:32 |
| `141d44674904` (`c390f418aff`) | Repair100 | unchanged | July10 10:58:45 |
| `b1673330ef5f` (`c9d9d3498f5`) | Repair100 | unchanged | July10 11:26:10 |
| `c5e10a744a17` (`03623e74836`) | Repair68; July10 total718 HTML edits | unchanged | July10 11:32:45 |
| `f176b458ba4e` (`36ebbe19d9c`) | July13 current-impression repair35 | unchanged | July13 20:42:56 |
| `918939382698` (`aab585de49b`) | HomeProof: 5HTML, 2XML, 4assets; +2 routes, +1 sitemap URL | 35,219 / 35,218 | July22 15:12:48 |
| `aa7d89ec029c` (`2e3a69692e1e`) | Remove creator-facing recovery language: 830HTML +1JS | 35,219 / 35,218 | July22 17:01:26 |

Every listed Pages run concluded success, meaning deployment succeeded, NOT content semantics passed. Latest run: [29940291492](https://github.com/SamJest/uk-planning-guide/actions/runs/29940291492), started July22 16:57:42. No later production run appeared. GitHub Pages server headers and live normalized hashes agree with this commit. The full deployment worktree tree hash equals this merge's tree.

## Unmerged source work retained

Nine source-only commits July4–5: `eae1e549401` source recovery; `b1f03491d89` source/page/URL contracts; `740858c9309` inventory; `d588f5ddb8d` canary; `b42165f0630` QA/CI; `aac5688f3ab` canary packaging; `8e90edcec7a` full candidate packaging; `449b4a06fe4` isolated overlay; `4674306f8c3` July5 incident analysis. Packaging source is not a current release authorization.

## Search timeline interpretation

Coverage visible corpus changes from1,193 on June30 to35,217 on July1 while impressions fall7,176 to284 (~96%). Git already held ~35k HTML before July1 and deployment history shows no matching July1 deploy. July10 is the observed sitemap expansion. Reporting/discovery/reprocessing is a possible explanation, not a proven cause. Neither blaming the July4 canary for the earlier fall nor mass-deleting July1's apparent cohort is supported.

## Current recovery branch and deployment state

On 6 September 2026 the audited work moved from source commit `4674306f8c3` to a dedicated branch, `codex/ukpg-recovery-2026-09-06`. Production remains `aa7d89ec029c`; no Pages files, remote branches, pull requests or deployment settings have been changed by this recovery. The final source-bound proposed release is `artifacts/releases/recovery-batch-2/release-manifest.json`, status `review-candidate-not-deployed`, based on production tree `9c640ff1b40473f2e025e9368ac008d41b1e5cc5`.
