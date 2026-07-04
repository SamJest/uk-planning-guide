# Site Audit and Competitor Gap Analysis

Audit date: 3 July 2026

## Current position

UK Planning Guide has evolved into a credible decision-support site rather than a conventional blog. The homepage reports 28 project guides, 307 local authority paths and 28 tools. It also has workflows, downloads and a saved-project workspace.

The proposition is strong: help users identify the likely planning route before paying for the wrong drawings, application or consultant.

## What is already working

### 1. Strong answer-first positioning

The homepage and key tools prioritize:

- likely planning route;
- local authority context;
- restrictions;
- drawings/readiness;
- costs;
- next actions.

This is materially better than article-only competitors.

### 2. Useful project workflow

The Planning Route Check already collects:

- project type;
- property type;
- location;
- restrictions;
- timeframe;
- preferred next step.

It then connects users to saved-project, lawful-development, drawing-readiness and cost functions. This is the correct product kernel.

### 3. Broad topical architecture

The current sitemap is segmented across:

- country and council pages;
- project guides;
- rules;
- process;
- tools;
- workflows;
- FAQs;
- downloads;
- local search/data pages.

The architecture can support scale once quality gates are reliable.

### 4. Browser-based retention MVP

“My Planning Project” stores:

- saved pages;
- completed checks;
- tasks;
- result summaries;
- project type/location/constraints.

It supports saving, printing and copying a project pack without requiring an account. This is an effective low-friction starting point.

### 5. Credible visual system

The warm neutral palette, green accent, cards and decision components feel more professional than many legacy planning sites.

## Critical weaknesses

### P0 — Cross-family content contamination

Sampled live pages show content from one project template appearing in unrelated generic pages.

Observed patterns include:

- a generic local planning-permission page assuming a garden room;
- a generic permitted-development page assuming a garden room;
- an Article 4 page using garden-room wording and an unrelated verification trigger;
- a generic council page making dropped kerbs/new vehicular access the dominant route.

This is a build-system defect. It creates:

- incorrect or misleading answers;
- duplicated content;
- weak local relevance;
- lower trust;
- poor search-quality signals;
- potentially thousands of contaminated combinations if scaled.

### P0 — Weak local evidence

Some “local” pages provide mostly national rules plus generic mentions of conservation/listed buildings. The site needs actual authority-level records such as:

- local validation list;
- Article 4 register/map;
- conservation-area maps;
- local plan and design guidance;
- pre-application service and fees;
- planning application search;
- committee calendar;
- authority-specific submission requirements.

A local page without verified local evidence should not be indexable.

### P0 — Source mismatch

An Article 4 page must not use a broad Historic England conservation-area page as if it were the local Article 4 source. Background sources and designation sources must be classified separately.

### P0 — Trust inconsistencies

Risks observed in the current output include:

- an “Editorial Review Desk” identity that needs a real, documented process behind it;
- visible update dates that do not always align with structured data;
- methodology-page placeholder advertising/partner/email UI;
- confidence/risk labels that can appear more definitive than the evidence supports.

### P1 — Too much duplicated page chrome

Large amounts of CSS and shared JavaScript are embedded in generated HTML. This increases:

- page size;
- repository size;
- change risk;
- regeneration cost;
- cache inefficiency.

Shared assets and reusable partials should be the default.

### P1 — Tools are broad but not yet a moat

The tool library is substantial, but several tools cover adjacent questions. Without:

- reliable local data;
- saved history;
- alerts;
- application tracking;
- comparable outputs;
- shareable reports;

they remain useful one-session calculators rather than a defensible product.

### P1 — Retention is device-bound

The local-storage workspace cannot currently:

- sync across devices;
- send reminders;
- track official application changes;
- notify users of policy updates;
- support multiple projects cleanly;
- create a meaningful “what changed” loop.

### P1 — Long-page repetition

Some project/local pages contain repeated trust panels, links and CTAs. This can obscure the core answer and reduce task completion. Each page should have:

- one answer summary;
- one assumptions panel;
- one source panel;
- one primary next action;
- one compact related-route section.

## Competitive landscape

### Planning Portal

**Strengths**

- official application gateway;
- common-project guidance;
- interactive house;
- find-your-council utility;
- news and market insight;
- professional ecosystem.

**Weaknesses/opportunity**

- users still need help translating rules into a project-specific route;
- the experience is broad and institutional;
- limited personal project management for homeowners.

**How UKPG wins**

A clearer independent decision journey, saved project, local evidence pack and follow-through after the initial answer.

### GOV.UK and national government guidance

**Strengths**

- authoritative primary guidance;
- high trust;
- canonical national information.

**Weaknesses/opportunity**

- fragmented user journeys;
- limited project workflow;
- little local comparison or personal tracking.

**How UKPG wins**

Never compete on authority. Use government sources as the factual backbone and provide the workflow, plain-English interpretation and local next steps.

### Planning Geek

**Strengths**

- deep technical coverage;
- permitted-development/use-class expertise;
- strong niche brand;
- broad glossary and educational material.

**Weaknesses/opportunity**

- older information architecture and presentation;
- weaker end-to-end project workspace;
- limited local recurring utility.

**How UKPG wins**

Equivalent depth on homeowner-intent topics, better UX, current source records and project/account features.

### Resi and similar service-led platforms

**Strengths**

- polished conversion funnel;
- expert calls;
- architecture/planning service;
- postcode/local-authority tools;
- strong commercial journey.

**Weaknesses/opportunity**

- content ultimately supports a service sale;
- narrower independence;
- less useful for users not ready to buy design services.

**How UKPG wins**

Independent route diagnosis first, broad professional options second, transparent referral consent and no forced sales call.

### Homebuilding and major property publishers

**Strengths**

- editorial authority;
- expert contributors;
- news reach;
- newsletter audience;
- strong links and brand recognition.

**Weaknesses/opportunity**

- articles are not a persistent planning workspace;
- local authority utility is limited;
- planning is one category among many.

**How UKPG wins**

Planning-only depth, actionable tools, verified local data, saved projects and alerts.

### Planning Aid / RTPI resources

**Strengths**

- professional trust;
- independent help;
- qualified-volunteer advice;
- strong process knowledge.

**Weaknesses/opportunity**

- limited productization and automated project tracking;
- eligibility/capacity constraints for individual support.

**How UKPG wins**

Accessible self-service preparation while linking to professional/charitable help where needed.

### PlanPulse, Planning.org.uk, Planning Alert, Plottr, SiteLens and similar data products

**Strengths**

- application search;
- maps;
- monitoring;
- instant or daily alerts;
- dashboards;
- normalized cross-council data;
- commercial lead generation.

**Weaknesses/opportunity**

- often optimized for professionals, prospecting or raw application monitoring;
- weak homeowner explanation and planning-route education;
- limited linkage between a watched application and a personal preparation workflow.

**How UKPG wins**

Combine homeowner guidance, route diagnosis, tasks and evidence with selected application/policy monitoring. Do not attempt to clone every professional planning-data platform.

## The defensible position

UKPG should own this position:

> The independent planning workspace that tells a UK homeowner what route probably applies, what local evidence changes the answer, what to prepare next and what changed since the last visit.

No major competitor combines all five:

1. high-quality national guidance;
2. authority-level verified evidence;
3. personal project workspace;
4. application/policy alerts;
5. independent next-action routing.

## What not to build

- tens of thousands of keyword-combination pages;
- a generic AI chatbot that improvises planning answers;
- a national application scraper before a reliable small-authority pilot;
- social/community forums before moderation and expert participation can be sustained;
- dozens more overlapping calculators;
- fake review badges or anonymous “expert” identities;
- a full SPA rewrite that reduces crawlability and delays quality repair;
- news rewrites with no original analysis;
- statistics without methodology and coverage disclosure.

