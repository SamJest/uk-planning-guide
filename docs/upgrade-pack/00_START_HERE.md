# UK Planning Guide: Codex Upgrade Pack

**Primary objective:** turn `ukplanningguide.co.uk` into the most useful independent planning resource for UK homeowners and small property projects, with a long-term operating target of **400,000–500,000+ monthly visits**.

**Target horizon:** 18–24 months is the credible category-leadership window. This is an ambitious operating target, not a traffic guarantee.

## Executive diagnosis

The site is no longer a basic content site. It already has:

- a clear decision-first positioning;
- project guides and country/council paths;
- a substantial planning-tool library;
- workflows, downloads and a browser-based “My Planning Project” workspace;
- structured data, segmented sitemaps and event tracking.

That foundation is valuable. The main constraint is now **quality control and product depth**, not raw page count.

The current site should be treated as approximately **6.2/10 overall**:

| Area | Score | Diagnosis |
|---|---:|---|
| Positioning and value proposition | 8.0 | Clear “check the route before paying” promise |
| Visual design | 7.0 | Credible and consistent, though repetitive across long pages |
| Navigation and information architecture | 7.5 | Strong hubs, tools and project routes |
| National evergreen guidance | 7.0 | Useful, answer-first content with concrete rules |
| Local authority usefulness | 3.5 | Generic local pages contain project-template leakage and insufficient local evidence |
| Tools and interactive utility | 6.5 | Broad tool set, but several tools overlap and are not yet backed by a distinctive data layer |
| Retention | 5.5 | Good local-storage MVP; no cross-device sync, alerts, application tracking or recurring digests |
| Trust and editorial transparency | 5.0 | Strong intent, but source mismatches, placeholder UI, date inconsistencies and unclear review identities weaken trust |
| Technical SEO and build safety | 5.0 | Strong sitemap/schema intent, but prior stale URLs, duplicated inline assets and weak generator safeguards create risk |
| Competitive defensibility | 5.5 | Good independent proposition; no strong proprietary data or recurring workflow moat yet |

## The central strategy

Do **not** attempt to reach 500,000 visits by publishing tens of thousands of lightly differentiated council/project pages.

Build a **Planning Operating System for UK homeowners**:

1. **Plan** — identify the likely route.
2. **Check** — constraints, rules, local authority requirements and evidence.
3. **Prepare** — drawings, documents, costs, tasks and application readiness.
4. **Track** — applications, decisions, policy changes and deadlines.
5. **Act** — lawful development certificate, pre-application advice, full application or relevant professional.
6. **Learn** — authoritative guides, data reports, case studies and current planning updates.

The traffic target becomes plausible only when the site combines three engines:

- **Search acquisition:** definitive national, project, scenario and genuinely local pages.
- **Recurring utility:** saved projects, application watches, alerts, digests and task reminders.
- **Linkable data:** council comparisons, decision trends, policy trackers and annual reports.

## Non-negotiable first move

Freeze broad indexable page expansion until the content generator is safe.

Observed examples show generic “planning permission”, “permitted development”, “Article 4” and council pages inheriting garden-room or dropped-kerb assumptions. Codex must repair this at the source, quarantine affected output and introduce build-time validation before creating more URLs.

## The five highest-impact workstreams

1. **Generator integrity and index cleanup**
2. **Authority data registry and source verification**
3. **My Planning Project 2.0 with accounts, sync and return loops**
4. **National content and high-intent project cluster rebuild**
5. **Application/policy tracking and linkable planning data**

## Pack contents

- `01_CODEX_MASTER_PROMPT.md` — the exact implementation brief to give Codex.
- `02_SITE_AUDIT_AND_COMPETITOR_GAPS.md` — scorecard, defects and competitive position.
- `03_PRODUCT_AND_RETENTION_SPEC.md` — recurring-use product specification.
- `04_SEO_CONTENT_AND_DATA_STRATEGY.md` — traffic architecture and editorial system.
- `05_TECHNICAL_ARCHITECTURE_AND_QA.md` — build, data, testing and performance requirements.
- `06_24_MONTH_ROADMAP.md` — phased execution and measurable gates.
- `07_IMPLEMENTATION_BACKLOG.csv` — prioritized work items.
- `08_ACCEPTANCE_TESTS.md` — acceptance criteria Codex must satisfy.
- `09_TRAFFIC_MODEL.csv` — modeled route to 475,000 monthly visits.
- `10_SOURCE_AND_EVIDENCE_APPENDIX.md` — audited URLs and competitor references.

## How to use this pack

Give Codex the repository and `01_CODEX_MASTER_PROMPT.md`. Instruct it to work in a feature branch and complete **Phase 0 only first**. Do not allow a full-site regeneration until the 20-page canary set passes every integrity, source, link, schema and visual test in `08_ACCEPTANCE_TESTS.md`.

