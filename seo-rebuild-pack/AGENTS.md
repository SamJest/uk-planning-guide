# Codex instructions: UK Planning Guide authority/relevance/indexation repair

Follow `CODEX_MASTER_PROMPT.md` and docs in this pack. This is an *existing production project*.

1. Read repo, generator, CI, routing, data and last successful deploy first. Do not replace existing architecture or start a blank app.
2. Preserve functioning pages/tools, URLs, historical page identity and inbound links. Make a **before** URL inventory and document all modifications. Maintain protected page list from GSC.
3. Produce implementation, not just advice. Work in reviewable phases; run tests/build and include actual counts and diffs after each phase.
4. Distinguish **officially verified fact** from **general national rule** from **unverified local unknown**. No invented facts, maps, licence decisions, prices, article 4 coverage, dates or credentials. No false editorial review badges.
5. Maintain separate legal knowledge sources/logic for England, Wales, Scotland and Northern Ireland. Prefer source citations to unsupported estimates.
6. For every indexable page, demand distinct intent + answer-first content + verified relevant information + actual useful action. Generic navigation funnels and keyword combinations are not enough.
7. Only choose canonical/redirect/noindex based on evidence for specific URLs. GitHub Pages doesn't offer arbitrary server-side 301 configuration on its own; detect actual host/platform before recommending a redirect implementation.
8. Sitemap `lastmod` only when page materially changes; publish canonical 200 URLs only. Don't assume every URL Google knows should be included.
9. Don't create artificial indexed location pages, repetitive FAQs, schema spam, fake reviews or misleading author/editorial claims.
10. Do not send, publish or store visitor personal information in logs, SEO reports, test fixtures or prompts. Avoid new paid dependencies.
11. Document unresolved issues and source research with statuses; never silently replace uncertainty with confident assertions.
12. If the user can't review while on mobile, finish a safe independently useful PR and show exact changed URL counts, tests and remaining risks.

13. OWNER REQUIREMENT: no duplicate unindexed page bloat. Follow `docs/00_DUPLICATES_ARE_NOT_ALLOWED.md`: stop redundant URLs at generator level, not mass `noindex`; protect traffic/backlinks and only migrate with valid statuses.
