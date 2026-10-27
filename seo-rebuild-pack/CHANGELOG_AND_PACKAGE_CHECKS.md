# Package completion and verification

Created 27 October 2026 from uploaded Google Search Console coverage + performance CSV/ZIPs and earlier sampled live-page audit.

The full-site generated repo and HTTP site crawl have NOT been run here (the project repository was not provided to this environment). Codex Cloud must run `scripts/audit_static_build.py`, `scripts/inspect_content_smells.py` and optional network `scripts/crawl_live_site.py` in the actual project, subject to access.

Included: primary task prompt; mobile task; owner anti-duplicate hard requirement; page type research blueprint; country-law fact verification; canonical/migration plan; technical CI gate; GSC prioritisation tables; source data; executable Python scripts and six unit tests.

Smoke tests executed against synthetic HTML pages; script compilation and `validate_evidence`, `validate_page_registry`, `check_migration_decisions` pass on included examples. Synthetic test data doesn't prove the current live site state.

Critical: don't delete everything with an exact-content flag. Assess intent, evidence, historic value and real canonical HTTP handling. The objective is more indexing of genuinely distinct canonical pages, not preserving 35k Google-known URLs at any cost.
