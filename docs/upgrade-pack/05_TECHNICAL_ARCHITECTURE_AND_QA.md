# Technical Architecture and QA Plan

## Architectural principle

Preserve the advantages of the current static site:

- crawlable HTML;
- low hosting complexity;
- reliable page delivery;
- easy caching.

Add dynamic services only where they create recurring user value:

- account sync;
- alerts;
- application monitoring;
- email;
- saved-project sharing.

## Recommended layers

```text
/content and /data
        ↓
validated typed records
        ↓
static generator and page-family templates
        ↓
HTML + shared CSS/JS assets
        ↓
CDN/static host

Optional authenticated services:
browser/app → serverless API → auth/database/queue/email
                                  ↓
                         source-change workers
```

## Suggested repository structure

Adapt to the actual codebase after audit.

```text
/
├── content/
│   ├── national/
│   ├── projects/
│   ├── rules/
│   ├── authorities/
│   ├── local/
│   ├── updates/
│   └── reports/
├── data/
│   ├── authorities/
│   ├── sources/
│   ├── rules/
│   ├── projects/
│   └── redirects/
├── schemas/
├── templates/
│   ├── layouts/
│   ├── page-families/
│   ├── components/
│   └── emails/
├── assets/
│   ├── css/
│   ├── js/
│   ├── images/
│   └── diagrams/
├── scripts/
│   ├── build/
│   ├── validate/
│   ├── source-check/
│   ├── redirects/
│   └── reports/
├── tests/
│   ├── unit/
│   ├── content/
│   ├── integration/
│   ├── e2e/
│   ├── accessibility/
│   └── visual/
├── docs/
└── dist/
```

Generated output should not be committed unless deployment requires it. If it must be committed, isolate it and prevent duplicated build artifacts from bloating history.

## Data contracts

### Authority

```json
{
  "authority_id": "colchester",
  "name": "Colchester City Council",
  "jurisdiction": "england",
  "official_domain": "...",
  "status": "active",
  "source_ids": [],
  "facts": [],
  "last_verified_at": "YYYY-MM-DD"
}
```

### Fact

```json
{
  "fact_id": "...",
  "authority_id": "...",
  "topic": "article_4|validation|pre_app|fees|portal|conservation|local_plan|committee",
  "claim": "...",
  "source_id": "...",
  "effective_from": null,
  "effective_to": null,
  "verified_at": "...",
  "confidence": "high|medium|low"
}
```

### Rule

```json
{
  "rule_id": "...",
  "jurisdiction": "england",
  "project_ids": [],
  "summary": "...",
  "conditions": [],
  "exceptions": [],
  "source_ids": [],
  "effective_from": "...",
  "verified_at": "..."
}
```

## Template safeguards

Each page-family template receives only its allowed fields.

Examples:

- `authority_profile` must not receive `assumed_project`.
- `local_rule` may receive authority and rule, but project is nullable and must be explicitly contextual.
- `local_project` requires both authority and project.
- `national_guide` must not receive authority facts.
- `tool` must reference a versioned rule engine.

Do not pass a global “context” object containing every record to every template.

## Rule engine

Tool outputs should use versioned rules:

```json
{
  "engine_version": "2026-07-01",
  "jurisdiction": "england",
  "rule_set_ids": ["..."],
  "input_schema_version": 2,
  "output": {
    "likely_route": "...",
    "confidence": "medium",
    "assumptions": [],
    "reasons": [],
    "exceptions": [],
    "official_checks": [],
    "next_actions": []
  }
}
```

Store the engine version with saved tool runs so old results can be identified when rules change.

## Source-change system

For each official source:

- schedule a reasonable check frequency;
- store response metadata/hash;
- detect material changes;
- create a review task;
- do not auto-publish legal interpretation;
- show “source changed; review pending” where appropriate;
- preserve prior versions for audit.

Respect robots, terms, rate limits and data-protection requirements. Prefer APIs, feeds and published datasets over brittle scraping.

## Account and notification services

Requirements:

- passwordless authentication;
- encrypted transport and managed credentials;
- least-privilege service roles;
- explicit consent records;
- unsubscribe in every email;
- rate limiting;
- abuse protection;
- data export/deletion;
- retention policy;
- no sensitive project-note content in analytics;
- audit log for notification and source-change actions.

## Shared assets

Extract repeated styles/scripts from generated pages.

Create:

- base stylesheet;
- component stylesheet;
- page-family bundles only where needed;
- core navigation/workspace script;
- tool-specific modules loaded only on tool pages;
- hashed/versioned asset names or query versions;
- a small critical CSS subset where necessary.

Remove duplicated script blocks from every page.

## URL registry

A central registry should provide:

- canonical URL;
- page family;
- index status;
- redirect status;
- language/jurisdiction;
- sitemap group;
- breadcrumb path;
- build output path.

Every internal link must resolve through the registry or be validated against it.

## Sitemap policy

Include only:

- canonical;
- 200-status;
- indexable;
- QA-passed pages.

Use accurate `lastmod` based on meaningful content changes.

Exclude:

- dashboard/account pages;
- search results;
- parameter states;
- thin local combinations;
- duplicate tool states;
- retired pages;
- placeholder pages.

## Structured data

Use only when content supports it:

- `WebSite` and `Organization` at site level;
- `Article` for substantive guides/updates;
- `HowTo` only for real step-by-step procedures;
- `SoftwareApplication` or `WebApplication` for tools where appropriate;
- `Dataset` for published data products;
- `BreadcrumbList`;
- `Person` only for real contributors;
- `FAQPage` only where current search-engine policy and visible content justify it.

Do not mark every page as `CollectionPage`.

## Test suites

### Unit tests

- rule calculations and branching;
- jurisdiction selection;
- authority/project/rule selectors;
- source lookup;
- date calculations;
- workspace migration;
- notification preference logic.

### Content tests

- required fields;
- source count;
- local-fact count;
- wrong authority;
- wrong jurisdiction;
- banned contamination;
- duplicate paragraphs;
- empty headings;
- placeholder text;
- unverified statistics;
- date consistency.

### Integration tests

- generator output;
- URL registry;
- canonical;
- breadcrumb;
- sitemap;
- redirects;
- shared assets;
- structured data;
- source links.

### End-to-end tests

Mobile and desktop journeys:

- start route check;
- complete tool;
- save project;
- return to project;
- create task;
- export project;
- sign in;
- subscribe to alert;
- unsubscribe;
- follow official source;
- handle storage disabled;
- handle unsupported authority.

### Accessibility

Automated plus manual:

- axe checks;
- keyboard;
- screen reader labels;
- focus management;
- error summaries;
- live regions;
- contrast;
- zoom/reflow;
- reduced motion.

### Visual regression

Snapshots for the canary set at:

- 360 px;
- 768 px;
- 1440 px.

## CI gates

Fail the build on:

- schema error;
- source-family mismatch;
- cross-family contamination;
- broken internal link;
- canonical mismatch;
- indexable page missing from sitemap;
- noindex page present in sitemap;
- structured-data parse failure;
- placeholder UI;
- accessibility critical/serious issue;
- performance budget regression over threshold;
- unapproved snapshot change.

Warn and require review for:

- official source redirect;
- high content similarity;
- low local-fact score;
- stale verification date;
- large page-size increase;
- unusual URL-count change.

## Observability

Implement:

- uptime monitoring;
- client error reporting;
- backend job alerts;
- source-check failures;
- email delivery/bounce monitoring;
- application-ingestion lag;
- build duration and URL-count reports;
- 404 logs;
- redirect hit counts;
- search zero-result logs.

## Deployment strategy

1. feature branch;
2. test environment or preview deployment;
3. canary URL review;
4. automated test report;
5. approved limited release;
6. monitor errors, indexing and engagement;
7. expand in batches;
8. retain rollback artifact and redirect map.

Never deploy a complete regenerated corpus as the first test of a generator change.

