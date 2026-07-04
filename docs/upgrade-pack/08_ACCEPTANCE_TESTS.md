# Acceptance Tests

Codex must produce an automated test report and a human-review checklist.

## A. Page-family integrity

### A1 Generic authority profile

Given an authority profile with no selected project:

- it must not contain a garden-room, dropped-kerb, extension, HMO or other project assumption;
- it must present balanced authority-level services and constraints;
- project cards may be shown only as clearly labeled navigation.

### A2 Generic planning-permission page

- no “assumed setup” for a project;
- no project-specific answer in the quick-answer block;
- examples must be labeled as examples.

### A3 Article 4 page

- Article 4 explanation is the primary intent;
- authority source is an actual local Article 4 source or the page states that no local source has yet been verified;
- no garden-room verification trigger unless the page is explicitly an Article 4 + garden-room scenario.

### A4 Local project page

- authority and project are explicit;
- national baseline is separated from local variation;
- local claims map to local source IDs;
- at least five unique local facts and three official local sources for index status.

### A5 Jurisdiction

- England-only terms/rules cannot appear as advice on Wales/Scotland pages unless clearly compared;
- country selection is explicit;
- sources match jurisdiction.

## B. Source integrity

- every claim block has one or more source IDs;
- every source ID exists;
- source publisher/domain matches the authority or national body;
- source type matches page topic;
- broken sources are surfaced;
- “last checked” is present;
- background sources are not represented as designation records.

## C. URL and index integrity

- canonical is absolute, registered and self-referential for canonical pages;
- no double slashes after hostname;
- no legacy path generated unintentionally;
- every indexable page appears once in a sitemap;
- noindex pages are absent from sitemaps;
- redirects contain no chains/loops;
- 410 pages are excluded;
- breadcrumbs resolve;
- all internal links return expected status.

## D. Date integrity

- visible updated date reflects substantive update;
- structured-data `dateModified` matches;
- sitemap `lastmod` matches;
- source verification date remains separate;
- build date is not substituted for content update date.

## E. Trust and editorial

- no “demo”, “placeholder”, “connect this form”, fake advertisement or unfinished partner block;
- every named reviewer is real and documented;
- no unsupported expert credential;
- guidance/legal disclaimer is clear but not used to excuse poor sourcing;
- uncertainty and assumptions are visible.

## F. Content quality

- unique page intent;
- answer appears early;
- no duplicated paragraph above threshold;
- no keyword-stuffed council/project combinations;
- no empty sections;
- one primary next action;
- related links are task-relevant;
- local page score at least 85/100;
- statistics include method and source.

## G. Tools

- deterministic unit tests for every rule branch;
- jurisdiction-specific rule set;
- engine version displayed/stored;
- output includes assumptions, confidence, reasons, exceptions, sources and next action;
- no result described as legal approval;
- keyboard and screen-reader usable;
- invalid input produces actionable error;
- result can be saved anonymously.

## H. Workspace

- existing local-storage state migrates without data loss;
- storage-blocked fallback works;
- anonymous save works;
- multiple projects remain isolated;
- account sync handles conflict;
- export and deletion work;
- notification consent is explicit;
- sensitive notes are excluded from analytics.

## I. Alerts

- source/application last-checked time visible;
- duplicate changes are deduplicated;
- unsupported authority is clearly stated;
- user can pause/delete/unsubscribe;
- email contains official source;
- false positive/failed check is logged;
- no nationwide launch until pilot accuracy threshold is met.

## J. Accessibility

- automated WCAG 2.2 AA scan has no critical/serious issues;
- full keyboard path;
- skip link;
- logical headings;
- focus visible;
- error summary;
- form labels/instructions;
- live results announced;
- 200% zoom and mobile reflow;
- reduced motion;
- contrast passes.

## K. Performance

At p75 real-user target:

- LCP < 2.5 s;
- INP < 200 ms;
- CLS < 0.1.

Build checks:

- normal content HTML preferably < 175 KB;
- shared critical JS < 100 KB gzip unless approved;
- no unnecessary script on content-only pages;
- images dimensioned and responsive;
- shared assets cacheable;
- no major regression versus approved canary.

## L. Analytics

- route start/completion;
- tool start/completion;
- project save;
- task completion;
- source click;
- alert creation;
- return action;
- referral consent/handoff;
- zero-result search.

Tests verify:

- no duplicate event firing;
- no personal free text;
- consistent event properties;
- consent behavior.

## M. Canary release

All 20 selected canary URLs must pass:

- content contract;
- contamination scan;
- source scan;
- internal/outbound links;
- canonical/sitemap;
- structured data;
- accessibility;
- mobile/desktop visual review;
- performance budget;
- analytics smoke test.

No broad regeneration until signed off.

