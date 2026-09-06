# Custom 404 Lighthouse summary

Run 6 September 2026 against `artifacts/builds/recovery-404-1`; its `404.html` SHA-256 is byte-identical to the final `artifacts/builds/recovery-404-2` candidate (`97da6654fe52c486766dd5895ef7639800333183cd3bc5b4b0ca56ff890d39ac`).

| Metric | Result |
|---|---:|
| Performance | 0.99 |
| Accessibility | 1.00 |
| Best practices | 0.96 |
| SEO | 0.66 |
| Largest Contentful Paint | 2,118 ms |
| Cumulative Layout Shift | 0 |
| Total Blocking Time | 0 ms |

The SEO score is intentionally reduced by `noindex, follow`, which is required for an error document. Best practices is reduced by one local `ERR_NETWORK_ACCESS_DENIED` resource error while external analytics was unavailable in the test sandbox; no page-script exception was reported. Lighthouse wrote a complete valid report, then exited 1 while Edge's temporary profile cleanup returned Windows `EPERM`, the same post-result tooling condition recorded for the first recovery batch.

Raw result: `lighthouse-custom-404.json`.
