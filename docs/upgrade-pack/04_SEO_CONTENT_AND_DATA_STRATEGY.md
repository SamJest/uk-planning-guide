# SEO, Content and Data Strategy

## Traffic objective

The operating target is 400,000–500,000+ monthly visits. The model in this pack targets approximately 475,000 visits through several independent engines.

This target should not be pursued through URL volume alone.

## Traffic engine 1: definitive national guidance

Target contribution at maturity: **150,000 monthly visits**

Build or substantially improve 80–120 cornerstone pages.

### Priority topics

- planning permission process;
- permitted development;
- lawful development certificates;
- prior approval;
- planning application types;
- validation;
- drawings and documents;
- planning fees;
- decision times;
- consultation;
- material considerations;
- objections;
- refusals;
- appeals;
- conditions;
- enforcement;
- commencement and expiry;
- “original house” definition;
- conservation areas;
- listed buildings;
- Article 4;
- use classes;
- HMOs;
- change of use;
- curtilage;
- highways/access;
- trees/TPOs;
- flood/ecology constraints;
- country differences.

### Page standard

Each cornerstone page should contain:

- direct answer;
- scope and jurisdiction;
- decision tree;
- assumptions;
- concrete thresholds/rules where valid;
- exception table;
- examples;
- common mistakes;
- local variation section;
- official sources;
- updated/review history;
- relevant tool;
- next action.

## Traffic engine 2: project and scenario clusters

Target contribution at maturity: **100,000 monthly visits**

Focus first on existing demand:

- single-storey extensions;
- two-storey extensions;
- rear/side extensions;
- loft conversions;
- dormers;
- roof alterations;
- porches;
- garages;
- outbuildings;
- garden rooms;
- annexes;
- sheds;
- fences/walls/gates;
- driveways;
- dropped kerbs/access;
- solar/heat pumps;
- windows/doors;
- balconies/decking;
- change of use;
- HMOs.

### Scenario pages

Create scenario pages only where the answer genuinely changes, for example:

- terraced vs semi-detached;
- corner plot;
- conservation area;
- listed building;
- Article 4;
- flat/maisonette;
- previous extension;
- boundary proximity;
- highway-facing elevation;
- green belt/AONB/National Park;
- England vs Wales vs Scotland.

Do not create every combinatorial permutation.

### Diagrams and assets

Produce original, reusable visual assets:

- dimension diagrams;
- elevation/roof examples;
- route flowcharts;
- document checklists;
- timeline graphics;
- boundary/curtilage illustrations.

Make them accessible and embeddable. Original diagrams are linkable assets and reduce ambiguity.

## Traffic engine 3: local authority and local project pages

Target contribution at maturity: **100,000 monthly visits**

### Authority profile

One canonical authority profile should include:

- application search;
- application submission route;
- local validation list;
- pre-application service and fees;
- Article 4 register/map;
- conservation-area map/list;
- local plan;
- design guidance;
- committee calendar;
- typical contact route;
- known portal notices;
- last source check;
- local update feed.

### Local project page quality threshold

An indexable local project page must have:

- a unique authority/project answer;
- at least five authority-specific facts;
- at least three authoritative local sources;
- a real local exception or process difference;
- no duplicated “assumed setup” from another project;
- a current source-check date;
- a useful local next action.

When this threshold is not met:

- keep the national project page canonical;
- show authority links dynamically;
- keep the thin local state noindex;
- do not publish an indexable URL.

### Local page rollout

Start with:

1. authorities already producing impressions/clicks;
2. major population centers;
3. authorities with clear online source material;
4. project clusters with strongest existing performance;
5. known high-friction topics such as Article 4, conservation, HMO, access and local validation.

Do not roll out all authority × project combinations at once.

## Traffic engine 4: updates and data journalism

Target contribution at maturity: **50,000 monthly visits**

### Update cadence

- substantive national update: as needed;
- weekly planning change digest;
- monthly authority/data story;
- quarterly council comparison;
- annual State of UK Homeowner Planning report.

### Original data opportunities

- planning application decision-time distribution;
- validation requirements by authority;
- pre-application fees and service levels;
- application fee changes;
- Article 4 coverage/register availability;
- digital application portal availability;
- project-type decision trends;
- common refusal themes;
- appeal outcome summaries;
- homeowner planning-cost index.

### Methodology

Every data publication must disclose:

- source;
- collection period;
- authority coverage;
- missing data;
- normalization;
- definitions;
- calculation;
- limitations;
- update date;
- downloadable aggregate where permitted.

## Traffic engine 5: recurring/direct/email use

Target contribution at maturity: **50,000 monthly visits**

Acquired through:

- saved projects;
- application alerts;
- council watches;
- task reminders;
- weekly digests;
- “what changed” feed;
- PWA/bookmark;
- shareable project packs.

This traffic is less dependent on search rankings and is essential to reaching category scale.

## Traffic engine 6: links, referrals and AI discovery

Target contribution at maturity: **25,000 monthly visits**

Build link acquisition around original utility:

- annual reports;
- council league tables with sound methodology;
- original diagrams;
- embeddable tools;
- downloadable datasets;
- planning-change explainers;
- journalist source pages;
- expert quotes;
- case studies.

Create clear machine-readable provenance:

- accurate structured data;
- visible sources;
- author/editor identities;
- concise answer summaries;
- stable fragment IDs;
- update histories;
- descriptive tables;
- accessible diagrams.

Do not create content solely for AI crawlers.

## Information architecture

Recommended top-level structure:

```text
/
├── start/
├── projects/
│   ├── extensions/
│   ├── loft-conversions/
│   ├── outbuildings/
│   ├── boundaries-access/
│   └── change-of-use/
├── rules/
├── process/
├── councils/
│   └── {authority}/
├── tools/
├── track/
│   ├── application/
│   ├── council/
│   └── area/
├── updates/
├── data/
├── case-studies/
├── downloads/
├── my-projects/
└── help/
```

Preserve existing useful URLs through aliases/redirects rather than forcing this exact structure immediately.

## Internal linking model

Each page should link by user journey:

- national rule → relevant projects;
- project → relevant rules;
- project → route tool;
- project → local authority profile;
- local project → authority sources;
- tool result → next step;
- saved project → changed guidance;
- update → affected evergreen guides;
- data report → underlying methodology and relevant guides.

Avoid large generic link blocks repeated across every page.

## Editorial workflow

States:

1. draft;
2. source collected;
3. source checked;
4. editor checked;
5. published;
6. update due;
7. archived.

Every published page records:

- author;
- reviewer/editor where real;
- jurisdiction;
- source IDs;
- verified date;
- next review date;
- change history;
- confidence.

## Content quality scoring

Before indexing, score each generated page:

| Dimension | Weight |
|---|---:|
| Intent match | 15 |
| Factual/source coverage | 20 |
| Unique local or scenario value | 20 |
| Answer clarity | 10 |
| Completeness | 10 |
| Internal linking | 5 |
| Trust/transparency | 10 |
| Technical/index integrity | 10 |

Minimum index threshold: **85/100**.

Automatic failure regardless of score:

- wrong jurisdiction;
- source mismatch;
- cross-project contamination;
- no unique answer;
- invented fact/statistic;
- broken canonical;
- placeholder UI;
- misleading reviewer identity.

## Content production targets

These are quality-controlled targets, not quotas:

### First 90 days

- repair top 100 existing landing pages;
- rebuild 20 cornerstone pages;
- establish 20 high-quality authority profiles;
- publish 25 high-intent local/project pages;
- launch updates hub and 5 substantive updates;
- publish one original linkable report.

### Months 4–6

- 50–70 cornerstone pages complete;
- 75–100 authority profiles;
- 150–250 validated local/project pages;
- 20 case studies;
- one monthly data story;
- application/council watch pilot.

### Months 7–12

- 100+ cornerstone pages;
- broad authority profile coverage;
- 500–900 validated local/project pages;
- 50+ case studies;
- regular policy/update publishing;
- two major original datasets/reports.

### Months 13–24

- fill verified authority gaps;
- expand only winning local/project families;
- scale application/policy monitoring;
- establish annual/quarterly data products;
- update and consolidate rather than endlessly add pages.

## Search performance governance

Weekly:

- indexing anomalies;
- crawl errors;
- top query/page changes;
- CTR opportunities;
- zero-click impressions;
- cannibalization;
- new broken links;
- source changes.

Monthly:

- cluster performance;
- page-quality cohorts;
- new vs returning organic users;
- assisted tool/project creation;
- content decay;
- redirects/noindex effects;
- competitor SERP changes.

Quarterly:

- consolidate weak pages;
- update top pages;
- retire obsolete content;
- reassess authority rollout;
- publish data insight;
- review traffic model assumptions.

