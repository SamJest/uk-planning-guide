# Codex Master Prompt: UK Planning Guide Category-Leader Upgrade

You are working on the existing repository for `https://ukplanningguide.co.uk/`.

Your job is to evolve the site into the strongest independent UK homeowner planning resource and a credible route toward 400,000–500,000+ monthly visits. This is not a request for superficial redesign, indiscriminate page generation or generic SEO text.

## Operating rules

1. Work on a new feature branch. Never commit directly to `main`.
2. Inspect and document the existing generator, templates, data sources, URL registry, deployment process and tests before changing code.
3. Preserve current working URLs, useful content, GA4 identifiers and established event names unless a migration explicitly requires changes.
4. Make small, reviewable commits grouped by workstream.
5. Do not regenerate the whole site until a representative 20-URL canary set passes all required tests.
6. Do not invent planning facts, council rules, professional reviewers, statistics, application data or source citations.
7. A missing local fact must be represented as “not yet verified” or cause a page to remain non-indexable. It must never be filled with generic or unrelated copy.
8. Keep free route checks useful without requiring contact details. Ask for an account or email only after value has been delivered and only with explicit consent.
9. Treat planning guidance as general information, not legal advice. Clearly identify uncertainty and escalation routes.
10. Prefer improving the existing static architecture progressively over an unnecessary full framework rewrite.
11. Record every changed URL, redirect and noindex decision.
12. Stop and report rather than silently weakening a requirement.

# Product direction

The target product is a **Planning Operating System for UK homeowners and small projects**:

- Plan the likely route.
- Check national and local constraints.
- Prepare documents, costs and tasks.
- Track applications, policies and deadlines.
- Act through the correct application/certificate/advice/professional route.
- Return for updates, project progress and local planning activity.

# Phase 0: mandatory integrity and trust repair

Complete this phase before expanding content or building major new features.

## 0.1 Map the current system

Create:

- `docs/current-architecture.md`
- `docs/url-families.md`
- `docs/content-data-flow.md`
- `docs/known-risks.md`
- `docs/phase-0-change-log.md`

Document:

- generator entry points;
- source data files;
- template and partial hierarchy;
- all page families;
- URL creation rules;
- canonical and sitemap generation;
- shared CSS/JS handling;
- current tests and deployment;
- analytics events;
- workspace/local-storage model;
- current repository size and large-file sources.

## 0.2 Introduce typed page-family contracts

Every generated page must have an explicit, validated record containing at least:

```json
{
  "page_family": "national_guide|project_guide|rule_guide|authority_profile|local_project|local_rule|tool|workflow|news|data_report",
  "jurisdiction": "england|wales|scotland|northern-ireland|uk",
  "authority_id": null,
  "project_id": null,
  "rule_id": null,
  "source_ids": [],
  "verified_at": null,
  "review_status": "draft|source_checked|editor_checked|published",
  "index_status": "noindex|index",
  "confidence": "low|medium|high",
  "unique_local_facts": []
}
```

Implement JSON Schema or an equivalent strict typed schema.

No template may infer a project or rule from whichever record happens to rank first in a collection.

## 0.3 Eliminate cross-family content leakage

Build a contamination linter and fail the build when:

- a generic council profile is dominated by one project type;
- a generic planning-permission page assumes a garden room or another project;
- an Article 4 page contains garden-room “incidental secondary building” wording unless context explicitly requires it;
- a council-wide page promotes dropped kerbs as the main planning route without a user-selected project;
- a Wales or Scotland page inherits England-only permitted-development text;
- a local source belongs to the wrong authority or wrong rule family;
- a generic rule page contains an “assumed setup” for an unrelated project;
- project-specific dimensions appear in a generic rule page without an explicitly labeled example.

Create phrase fingerprints and semantic tests for known failure patterns, including:

- garden room;
- incidental secondary building;
- dropped kerb;
- new vehicular access;
- vehicle crossing;
- extension depth/height terms;
- HMO/use-class terms;
- tree/TPO text;
- conservation/listed-building text.

Use both allowlists and denylists by page family. Do not rely solely on string matching.

## 0.4 Source integrity

Create a normalized source registry:

```json
{
  "source_id": "colchester-article-4-register",
  "authority_id": "colchester",
  "jurisdiction": "england",
  "source_type": "article_4|local_plan|validation_list|pre_app|fees|application_search|conservation_map|committee|national_legislation|official_guidance",
  "title": "...",
  "url": "...",
  "publisher": "...",
  "last_checked_at": "...",
  "status": "active|redirected|unavailable|unverified"
}
```

Requirements:

- Local Article 4 pages must link to the actual authority source where one is verified.
- Historic England or national sources may provide background but cannot substitute for a local designation source.
- Each indexable local page must have at least three authoritative source records and at least five genuinely authority-specific facts unless the page family has an approved exception.
- Source health must be checked automatically.
- Broken or redirected official links must be reported.
- Every fact must be traceable to a source ID in the source registry.

## 0.5 Quarantine weak output

Create a report of all current URLs with:

- family;
- word count;
- content similarity score;
- local-fact count;
- source count;
- source-family match;
- contamination flags;
- organic importance if analytics/GSC data is locally available;
- proposed action: keep, repair, merge, noindex, redirect or 410.

Do not delete URLs solely because traffic is low. Make decisions by topical value, quality and replacement availability.

Generate a redirect map only where the destination is a genuine topical equivalent. Return 410 for obsolete URLs with no replacement.

## 0.6 Remove live placeholders and misleading trust elements

- Remove or complete all “demo-ready UI”, placeholder advertisements, fake partner placements and nonfunctional email forms.
- Replace any reviewer or editorial identity that is not tied to a real documented person/process.
- Use transparent wording such as “Written and source-checked by…” with a real name and verifiable method.
- Synchronize visible updated dates, structured-data `dateModified` and sitemap `lastmod`.
- Avoid mass-updating dates when substantive content did not change.
- Add a per-page source and review panel.

## 0.7 Fix technical hygiene

- Centralize canonical URL generation.
- Reject double slashes, legacy `/planning-guides/` paths and unregistered internal URLs.
- Generate sitemaps only from QA-passed, indexable URLs.
- Build automated internal and outbound link checks.
- Audit repository bloat and remove generated artifacts or oversized duplicated assets from version history only through a separately approved migration.
- Extract repeated inline CSS and shared JavaScript into versioned cacheable assets.
- Preserve essential critical CSS where justified.
- Create a single URL registry used by navigation, sitemaps, canonicals, breadcrumbs and redirects.

# Canary requirement

Before any broad regeneration, build and review these representative families:

- homepage;
- national planning permission hub;
- national permitted development hub;
- one England project page;
- one Wales project page;
- one Scotland project page;
- one rule page;
- one Article 4 page;
- one conservation-area page;
- one authority profile;
- one local project page;
- one local rule page;
- one tool;
- one workflow;
- My Planning Project;
- downloads hub;
- FAQ hub;
- one news/update page;
- one data page;
- one retired/redirected URL.

Use at least three different authorities, including Colchester because known leakage exists there.

Do not continue until all acceptance tests pass.

# Phase 1: site foundation and discoverability

After Phase 0 is approved:

1. Build a shared design system and reusable layouts.
2. Add fast internal search with filters for project, country, authority, rule, tool and process stage.
3. Create a universal “Start your project” entry point.
4. Reduce repeated CTA/trust blocks and improve long-page navigation.
5. Add comparison tables, diagrams and decision trees where they materially improve understanding.
6. Implement page-type-specific structured data.
7. Add complete analytics event documentation and funnel dashboards.
8. Establish performance budgets and CI checks.

# Phase 2: My Planning Project 2.0

Evolve the current browser-only workspace into an optional account-backed product without removing anonymous use.

## Required functions

- multiple projects;
- property/location profile;
- project type and jurisdiction;
- saved pages and tool results;
- tasks, due dates and completion status;
- notes;
- document/evidence checklist;
- constraint checklist;
- application/certificate reference;
- activity timeline;
- export to PDF/print/JSON;
- calendar export;
- cross-device sync through passwordless magic link;
- explicit notification preferences;
- account deletion and data export;
- local-first fallback when not signed in.

## Suggested entities

- User
- Property
- Project
- Authority
- ProjectConstraint
- SavedGuide
- ToolRun
- Task
- DocumentRequirement
- ApplicationWatch
- PolicyWatch
- NotificationPreference
- ReferralConsent
- AuditEvent

Choose the backend only after inspecting the current deployment. A lightweight managed database/auth service or serverless architecture is acceptable. Do not force a full frontend rewrite.

# Phase 3: recurring-use systems

Build in this order:

## 3.1 Application watch

Allow a user to save a planning application reference or official application URL and receive:

- status changes;
- new documents;
- consultation deadlines;
- committee dates;
- decision publication;
- appeal updates where available.

Start with a controlled set of authorities and a reliable data/access method. Do not launch a nationwide brittle scraper.

## 3.2 Council and policy watch

Users can follow an authority and receive a weekly digest of:

- local plan consultations;
- Article 4 updates;
- validation-list changes;
- fee/pre-application changes;
- committee schedules;
- major homeowner-relevant policy updates;
- newly published guidance.

Every item must link to the official source and show the observed date.

## 3.3 “What changed since your last visit”

For signed-in users and local workspaces:

- changed saved guidance;
- updated sources;
- completed or overdue tasks;
- application-watch activity;
- local policy changes;
- recommended next step.

## 3.4 Nearby decisions and examples

Where legally and technically sustainable:

- search nearby applications by project type;
- show approved/refused examples;
- filter by authority and date;
- link to the official record;
- avoid implying one decision guarantees another;
- never republish personal data unnecessarily.

# Phase 4: content and data authority

Implement the editorial/data plan in `04_SEO_CONTENT_AND_DATA_STRATEGY.md`.

Priority clusters:

1. planning route and application process;
2. permitted development and lawful development certificates;
3. extensions, lofts, outbuildings, garden rooms and annexes;
4. fences, boundaries, access and dropped kerbs;
5. conservation areas, listed buildings and Article 4;
6. objections, material considerations, refusals and appeals;
7. drawings, validation, fees, timescales and conditions;
8. use classes, HMOs and change of use;
9. country-specific differences;
10. high-quality council profiles and local project pages.

Do not publish a page merely because a keyword combination exists.

# Phase 5: defensible data products

Develop only after data quality is proven:

- council application-time dashboards;
- approval/refusal trend pages;
- top validated refusal-reason taxonomy;
- fee and pre-application comparison;
- validation requirement comparison;
- annual State of Homeowner Planning report;
- embeddable calculators and authority widgets;
- public data methodology and downloadable aggregates;
- press-ready findings and source notes.

All metrics must disclose coverage, collection date, exclusions and calculation method.

# User experience principles

- Answer first; explanation second.
- Show likely route, confidence and assumptions.
- Separate national baseline from local variation.
- Show official sources adjacent to claims.
- Make uncertainty visible.
- Give one primary next action, not six equal CTAs.
- Keep forms short and progressive.
- Do not gate core guidance.
- Mobile-first, WCAG 2.2 AA.
- Avoid alarmist “risk” labels without explaining the reason.
- Avoid claiming a definitive legal answer from a lightweight self-check.

# SEO principles

- One canonical intent per page.
- No mass local pages without local evidence.
- Prefer fewer authoritative pages over near-duplicates.
- Preserve useful existing URLs.
- Use hub-and-spoke internal linking based on user journey.
- Use HTML links, crawlable content and server-rendered/static output for indexable pages.
- Keep account dashboards and thin filtered states noindex.
- Create news/update pages only for substantive changes.
- Use accurate dates and an update history.
- Build for citations and usefulness, not keyword density.

# Performance and accessibility budgets

At the 75th percentile on real-user data:

- LCP under 2.5 seconds;
- INP under 200 ms;
- CLS under 0.1.

Build targets:

- initial HTML preferably under 175 KB for normal content pages;
- shared critical JavaScript under 100 KB gzip unless justified;
- no render-blocking third-party scripts beyond essential analytics/consent;
- responsive images with dimensions;
- keyboard-complete navigation and tools;
- visible focus states;
- reduced-motion support;
- semantic headings and landmarks;
- labels, error summaries and live regions for forms.

# Analytics

Preserve current useful events and add a documented event schema covering:

- route start/completion;
- tool start/completion;
- source click;
- page save;
- task creation/completion;
- account creation;
- alert creation;
- digest open/click;
- application-watch change;
- return visit;
- referral consent and handoff;
- zero-result internal searches;
- search-to-tool and search-to-guide conversion.

Do not send sensitive free-text project notes to analytics.

# Required testing

Implement all tests in `08_ACCEPTANCE_TESTS.md`, including:

- typed content validation;
- contamination tests;
- jurisdiction tests;
- source-family matching;
- URL/canonical/sitemap consistency;
- broken links;
- duplicate content;
- structured data;
- representative visual snapshots;
- accessibility;
- core tool logic;
- workspace migration;
- Playwright journeys;
- performance budgets.

# Deliverables for each phase

For every phase provide:

1. architecture/change summary;
2. changed files;
3. changed URL list;
4. redirect/noindex list;
5. tests added;
6. test results;
7. screenshots of representative mobile and desktop pages;
8. analytics changes;
9. known limitations;
10. rollback instructions.

# First execution request

Start now with **Phase 0 only**.

Your first response/output should:

- map the repository;
- identify the generator and source-of-truth files;
- quantify current page families and affected URLs;
- propose the exact canary URL set;
- list the specific files you will change;
- create the feature branch;
- implement the schema, source registry skeleton and contamination test framework;
- repair the canary pages;
- run all Phase 0 tests;
- stop for review before regenerating the whole site.

