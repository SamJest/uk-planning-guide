# Recovery cohort Lighthouse summary

Run: 6 September 2026, Lighthouse 12.6.1, mobile emulation, local static canary `artifacts/builds/recovery-semantic-5`.

| Route | Performance | Accessibility | Best practices | SEO | LCP ms | CLS | TBT ms | Budget |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| `/permitted-development/north-yorkshire/` | 0.96 | 1.00 | 1.00 | 1.00 | 2,130.8 | 0 | 186.5 | pass |
| `/conservation-areas/glasgow-city/` | 0.96 | 1.00 | 1.00 | 1.00 | 2,113.9 | 0 | 185.0 | pass |
| `/councils/sheffield/` | 0.94 | 1.00 | 1.00 | 1.00 | 2,122.6 | 0 | 250.0 | pass |
| `/tools/` | 0.95 | 1.00 | 1.00 | 1.00 | 2,116.2 | 0 | 232.0 | pass |

Enforced budgets are performance ≥0.80, accessibility/best-practices/SEO ≥0.90, LCP ≤2,500ms, CLS ≤0.1 and TBT ≤300ms. All four changed pages pass.

The direct Lighthouse process returned non-zero after writing each valid JSON report because Edge exited before `chrome-launcher` could remove its temporary Windows profile (`EPERM`). This is a runner-cleanup defect after result generation, not an audit failure; the raw reports are retained alongside this summary. The earlier configured autorun was stopped after the same cleanup issue and is not counted as a passing run.
