# Monetisation controls and privacy notes

Status: implemented as a fail-closed foundation; no commercial surface is active.

`data/monetisation-config.json` is the single control plane. Global monetisation, ads, referrals and the paid Project Readiness Pack default to off. Ad eligibility is evaluated by `utils/monetisation.py`; uncertainty, missing consent, an unapproved template, a sensitive state, a purchased experience, a missing provider or a zero rollout all suppress the surface. No advertising or partner script is included in the site template.

The partner registry is intentionally empty. Offers require an owner-approved record, an active date window, compatible jurisdiction and project type, disclosure text and a verified URL. An expired, incomplete or unapproved record cannot be selected.

The event dictionary permits only coarse page family, jurisdiction, project category, cohort and consent state. Exact addresses, postcodes, coordinates, contact details and free text are prohibited from analytics. Transaction services may use opaque order IDs in their own secured records, not planning answers in analytics.

Before activation the owner must select a certified consent platform and vendors, obtain privacy/legal review, set retention periods, approve partners and commercial terms, choose hosted checkout/tax/receipt/refund handling, provide support routing, and approve a price. These are genuine launch dependencies, not code defaults.

Rollback is one configuration change: leave `global_enabled` false (or turn it false) and rebuild the bounded cohort. Because no provider script is embedded unconditionally, this removes all commercial eligibility without editing templates. Production activation also requires passing tests, performance budgets and a separate reviewed deployment batch.
