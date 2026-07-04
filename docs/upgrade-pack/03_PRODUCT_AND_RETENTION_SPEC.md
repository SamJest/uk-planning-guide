# Product and Retention Specification

## Product goal

Give users a reason to return because their planning project, watched application or local planning environment changed — not because the site sends generic content.

## Core navigation model

The primary navigation should map to user intent:

1. **Start a project**
2. **Check a rule**
3. **Find your council**
4. **Track an application**
5. **Planning updates**
6. **My projects**

Secondary navigation can expose guides, tools, downloads and professional help.

## Universal project entry point

Create a persistent “Start your planning project” flow.

### Inputs

- country/jurisdiction;
- postcode or authority;
- property type;
- project type;
- listed-building status;
- conservation area;
- Article 4 awareness;
- relevant known constraints;
- project stage;
- intended timescale.

### Output

- likely route;
- confidence and assumptions;
- critical blockers;
- official sources;
- local checks;
- documents likely needed;
- recommended next action;
- option to save the project.

Never describe the result as a legal determination.

## My Planning Project 2.0

### Anonymous mode

Retain local-first behavior:

- save a project on the current device;
- save pages and tool runs;
- create tasks;
- print/export;
- no email required.

### Account mode

Offer passwordless sign-in after a user has created value.

Functions:

- sync across devices;
- multiple projects;
- update history;
- reminders;
- alert subscriptions;
- saved official sources;
- application references;
- notes and document requirements;
- project progress;
- export/delete account.

### Project dashboard

Each project should show:

- project title and property;
- authority and jurisdiction;
- likely route;
- confidence;
- unresolved constraints;
- completed checks;
- next three tasks;
- important dates;
- saved evidence;
- watched applications;
- local/rule changes;
- recent activity;
- one primary next action.

### Project stages

Use a consistent stage model:

1. Exploring
2. Checking constraints
3. Choosing route
4. Preparing drawings/evidence
5. Ready to submit
6. Submitted
7. Consultation
8. Decision
9. Conditions/appeal/follow-up
10. Complete

## Return-loop features

### 1. Application Watch

**User need:** “Has anything changed on my application?”

MVP:

- save official application URL or reference;
- poll or ingest supported authority data;
- display current status and last checked time;
- detect new documents/status/deadline/decision;
- send optional email digest;
- link to the official record.

Later:

- appeal tracking;
- committee agenda detection;
- document categorization;
- neighbor application watch.

### 2. Council Watch

**User need:** “Has my council changed anything relevant?”

Weekly digest:

- local plan consultation;
- Article 4 notice/change;
- validation-list update;
- pre-application fee/process update;
- planning committee dates;
- homeowner-relevant design guidance;
- application portal outage/change.

Each item needs:

- official link;
- detected/published date;
- plain-English summary;
- affected project types;
- review status.

### 3. Property/area watch

Optional, privacy-conscious alerts for:

- applications within a user-selected radius;
- selected project types;
- decisions nearby;
- major development;
- conservation/listed-building changes where data exists.

Avoid unnecessary personal-data republication.

### 4. Task and deadline reminders

Examples:

- take site measurements;
- request title plan;
- photograph elevations;
- check Article 4 map;
- obtain ecology/tree input;
- submit before fee/change date;
- consultation closes;
- expected decision date;
- condition-discharge follow-up.

Support:

- email;
- calendar export;
- in-product reminders;
- snooze and complete.

### 5. “What changed” feed

On return, show:

- a saved source changed;
- a rule guide was substantively updated;
- watched application changed;
- a task became due;
- a new local consultation appeared;
- a relevant nearby decision was published.

### 6. Similar decision examples

For a saved project:

- nearby/same-authority applications;
- same project type;
- approved/refused;
- recent first;
- official-record link;
- explicit disclaimer that outcomes are site-specific.

### 7. Project evidence pack

Generate a structured pack containing:

- project summary;
- assumptions;
- dimensions;
- property constraints;
- official-source links;
- required drawings;
- photographs/evidence;
- open questions;
- route recommendation;
- saved examples;
- task checklist.

Export to print/PDF and shareable read-only link.

## Planning update product

Create a current-update hub, but do not become a generic news publisher.

Content types:

- national rule change;
- fee update;
- court/appeal decision with broad homeowner relevance;
- Planning Portal process change;
- authority policy/Article 4/validation change;
- consultation;
- quarterly data insight;
- annual report.

Every update must answer:

- what changed;
- when;
- who is affected;
- what to do now;
- primary source;
- which evergreen pages need updating.

## Internal search

Search should resolve tasks, not only titles.

Filters:

- country;
- authority;
- project;
- rule;
- process stage;
- content type;
- last updated.

Search features:

- synonym handling;
- typo tolerance;
- “do I need permission for…” suggestions;
- direct links to tools;
- zero-result logging;
- official-source results clearly labeled;
- noindex search-result pages.

## Community and expert features

Do not launch an open forum initially.

Safer sequence:

1. moderated “question of the week”;
2. published expert answers;
3. anonymized case studies;
4. verified professional contributor profiles;
5. structured comments on data reports;
6. invitation-only expert panel.

This produces trust and unique content without unmanaged legal/moderation risk.

## Ethical monetization surfaces

Referral opportunities should occur only after the user receives a useful result.

Eligible moments:

- route result indicates professional review is sensible;
- user is ready for drawings;
- user needs heritage/tree/ecology input;
- application pack is incomplete;
- appeal/refusal support is needed.

Requirements:

- explicit consent;
- clear commercial disclosure;
- no fabricated urgency;
- multiple relevant service categories where possible;
- no sale of project details without consent;
- conversion tracking separated from core guidance.

## Retention metrics

Track:

- projects created;
- percentage saved;
- account conversion after anonymous use;
- returning project users at 7/30/90 days;
- alert subscriptions;
- alert-to-return rate;
- task completion;
- application-watch retention;
- digest open/click;
- project export;
- source click-through;
- referral handoff after value;
- unsubscribes and notification fatigue.

Primary north-star metric:

> Monthly active projects with at least one meaningful action.

A meaningful action is a saved result, completed check, task completion, source verification, application-watch interaction or project update — not a page view.

