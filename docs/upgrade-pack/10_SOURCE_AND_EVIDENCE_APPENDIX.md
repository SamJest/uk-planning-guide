# Source and Evidence Appendix

Audit date: 3 July 2026

This appendix records the pages inspected when preparing the implementation plan. Codex should conduct its own repository-wide audit and should not treat this list as exhaustive.

## UK Planning Guide

- Homepage: `https://ukplanningguide.co.uk/`
- Tools hub: `https://ukplanningguide.co.uk/tools/`
- Planning Route Check: `https://ukplanningguide.co.uk/tools/planning-route-check/`
- House extensions hub: `https://ukplanningguide.co.uk/house-extensions/`
- Colchester council page: `https://ukplanningguide.co.uk/councils/colchester/`
- Planning permission in Colchester: local rule page inspected during audit
- Permitted development in Colchester: local rule page inspected during audit
- Article 4 in Colchester: local rule page inspected during audit
- House extension in Colchester: local project page inspected during audit
- Methodology: `https://ukplanningguide.co.uk/methodology/`
- My Planning Project: `https://ukplanningguide.co.uk/my-planning-project/`

## Repository evidence

Repository: `SamJest/uk-planning-guide`

Files inspected:

- `index.html`
- `sitemap.xml`
- `my-planning-project/index.html`
- `assets/js/project-tracker.js`

Observed implementation details:

- GA4 and structured data are present.
- CSS is heavily embedded in generated HTML.
- sitemap index is segmented across page families.
- My Planning Project uses local storage and stores saved pages, tasks, completed checks, constraints and tool-result summaries.
- event tracking exists for route, save, download and related actions.
- current workspace is device-bound.

## Competitor/reference sites

### Primary authoritative sources

- GOV.UK planning guidance and services: `https://www.gov.uk/browse/housing-local-services/planning-permission`
- Planning Portal: `https://www.planningportal.co.uk/`

### Independent guidance and service competitors

- Planning Geek: `https://www.planninggeek.co.uk/`
- Resi: `https://resi.co.uk/`
- Homebuilding & Renovating: `https://www.homebuilding.co.uk/`
- Planning Aid / RTPI: `https://www.planningaid.co.uk/`

### Application-data and alert competitors

- PlanPulse: `https://planpulse.co.uk/`
- Planning.org.uk: `https://www.planning.org.uk/`
- Planning Alert: search/alert product inspected during audit
- Plottr: planning application map/alert product inspected during audit
- SiteLens: planning monitoring/briefing product inspected during audit

## Evidence limitations

- This pack does not contain a fresh Google Search Console or GA4 export.
- Traffic ranges are strategic model targets, not forecasts.
- Competitor product features and pricing can change.
- Council source availability and data-access methods vary and require authority-by-authority verification.
- Planning rules and guidance change; the production system must retain source dates and review workflows.

