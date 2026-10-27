# Primary-source research system for UK planning guidance

High-stakes local legal/planning information: inaccuracies cost users money. *Research before claiming.*

Primary evidence priority: legislation.gov.uk for statutory instruments (check amendment/consolidation and commencement); gov.uk guidance/Planning Portal with applicability context; devolved administration and relevant official planning bodies; council-issued adopted policies, validated application requirements, conservation maps and Article 4 directions; local authority interactive maps and direct Planning Inspectorate decisions where relevant. Third-party blogs can point to topics but aren't authoritative evidence.

England planning rules must never be copied into Wales, Scotland and Northern Ireland. Central policy and law differ; check source dates and effective changes. Planning decisions are property-specific and cannot be conclusively answered without site context. A local guide should link users to the actual official authority source and describe its relevance, not hallucinate map coverage.

Every supported fact record:
- stable `claim_id`, `jurisdiction`, `authority_id` or null, `project`, `topic`, `claim`, `qualification`, `source_url`, `source_title`, `source_publisher`, `source_location`, `source_published` when known, `source_effective` when relevant/known, `verified_at` and `evidence_status`.
- `evidence_status`: `verified_primary`, `verified_secondary`, `unverified`, `superseded`.
- Review dates may only update after an actual source recheck. Unknown data should be null, not inferred.
- Document source freshness change-monitoring as an optional later automation, not current unsupported claims.
- Keep links, avoid copying licensed maps/long government text verbatim; favour concise summaries and own diagrams.

Investigate authority restructuring and jurisdiction before outputting council pages; never assume administrative geography equals Article 4 coverage. HMO licensing and planning permission are distinct; local use classification/specific exceptions and licensing changes are separate.

Block publication of pages with unsupported confident legal absolutes (e.g. 'no permission ever required', 'all of [town] Article 4') with rule tests or editorial hold.
