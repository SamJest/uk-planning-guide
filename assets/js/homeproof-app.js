(function () {
  "use strict";

  const root = document.querySelector("[data-homeproof-app]");
  const Core = window.HomeProofCore;
  if (!root || !Core) {
    return;
  }

  const templateUrl = root.getAttribute("data-template-url") || "/assets/data/homeproof/project-templates.json";
  let templatesDocument = null;
  let state = readState();
  let activeTab = "overview";
  let creatingNewProject = false;

  function escapeHtml(value) {
    return String(value == null ? "" : value)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;")
      .replace(/'/g, "&#39;");
  }

  function selected(value, expected) {
    return value === expected ? " selected" : "";
  }

  function checked(value) {
    return value ? " checked" : "";
  }

  function track(eventName, params) {
    if (typeof window.upgTrack === "function") {
      window.upgTrack(eventName, params || {});
      return;
    }
    if (typeof window.gtag === "function") {
      window.gtag("event", eventName, params || {});
    }
  }

  function setStatus(message, tone) {
    const node = root.querySelector("[data-app-status]");
    if (!node) {
      return;
    }
    node.textContent = message || "";
    node.setAttribute("data-tone", tone || "info");
  }

  function readState() {
    try {
      const raw = window.localStorage.getItem(Core.STORAGE_KEY);
      return raw ? Core.normaliseState(JSON.parse(raw)) : Core.createEmptyState();
    } catch (error) {
      const fallback = Core.createEmptyState();
      fallback.storageBlocked = true;
      return fallback;
    }
  }

  function writeState(message) {
    state.updatedAt = new Date().toISOString();
    state = Core.normaliseState(state);
    try {
      window.localStorage.setItem(Core.STORAGE_KEY, JSON.stringify(state));
      if (message) {
        setStatus(message, "success");
      }
      return true;
    } catch (error) {
      state.storageBlocked = true;
      setStatus("This browser blocked local storage. Export a backup before leaving this page.", "error");
      return false;
    }
  }

  function activeProject() {
    return state.projects.find(function (project) {
      return project.id === state.activeProjectId;
    }) || null;
  }

  function updateActiveProject(mutator, message) {
    const index = state.projects.findIndex(function (project) {
      return project.id === state.activeProjectId;
    });
    if (index === -1) {
      return;
    }
    const project = Core.clone(state.projects[index]);
    mutator(project);
    project.updatedAt = new Date().toISOString();
    state.projects[index] = Core.normaliseProject(project);
    writeState(message);
  }

  function stageLabel(stage) {
    return {
      "researching": "Researching",
      "seeking-quotes": "Seeking quotes",
      "work-underway": "Work underway",
      "completion": "Completion and records"
    }[stage] || "Researching";
  }

  function percentage(done, total) {
    if (!total) {
      return 0;
    }
    return Math.round((done / total) * 100);
  }

  function loadLegacyWorkspace() {
    try {
      const raw = window.localStorage.getItem(Core.LEGACY_WORKSPACE_KEY);
      return raw ? JSON.parse(raw) : null;
    } catch (error) {
      return null;
    }
  }

  function legacyAvailable(project) {
    return !state.settings.legacyPromptDismissed && !project.linkedPlanningWorkspace && Boolean(Core.legacyWorkspaceSummary(loadLegacyWorkspace()));
  }

  function renderNewProjectForm() {
    const options = (templatesDocument.templates || []).map(function (template) {
      return "<option value='" + escapeHtml(template.id) + "'>" + escapeHtml(template.name) + "</option>";
    }).join("");

    root.innerHTML = "<div class='app-status' data-app-status aria-live='polite'></div>" +
      "<div class='app-header'><div><span class='eyebrow'>HomeProof workspace</span><h1>Create Your First Project Record</h1><p>Start with the project type. You can add scopes, quotes and completion records without creating an account.</p></div></div>" +
      "<div class='app-view'><form data-new-project-form><div class='form-grid'>" +
      "<div class='form-field full'><label for='hp-template'>Project type</label><select id='hp-template' name='templateId' required><option value=''>Choose a project</option>" + options + "</select></div>" +
      "<div class='form-field'><label for='hp-name'>Project name</label><input id='hp-name' name='name' maxlength='120' placeholder='For example: Rear extension 2026'></div>" +
      "<div class='form-field'><label for='hp-stage'>Current stage</label><select id='hp-stage' name='stage'><option value='researching'>Researching</option><option value='seeking-quotes'>Seeking quotes</option><option value='work-underway'>Work underway</option><option value='completion'>Completion and records</option></select></div>" +
      "<div class='form-field'><label for='hp-property'>Property label <span class='visually-hidden'>(optional)</span></label><input id='hp-property' name='propertyLabel' maxlength='160' placeholder='Use a private label, not necessarily the full address'><small>Stored only in this browser.</small></div>" +
      "<div class='form-field'><label for='hp-council'>Council or area <span class='visually-hidden'>(optional)</span></label><input id='hp-council' name='councilLabel' maxlength='120' placeholder='For example: Colchester City Council'></div>" +
      "<div class='form-field full'><label for='hp-notes'>Initial notes <span class='visually-hidden'>(optional)</span></label><textarea id='hp-notes' name='notes' maxlength='3000' placeholder='Record the decision you are currently trying to make.'></textarea></div>" +
      "</div><div class='button-row'><button class='primary' type='submit'>Create HomeProof project</button>" + (state.projects.length ? "<button class='secondary' type='button' data-action='cancel-new-project'>Cancel</button>" : "") + "</div></form>" +
      "<p class='privacy-note'>HomeProof does not confirm planning permission, building-regulation compliance or contractor quality. It organises your evidence and the checks still requiring official or professional confirmation.</p></div>";
  }

  function renderProjectSwitcher(project) {
    const options = state.projects.map(function (item) {
      return "<option value='" + escapeHtml(item.id) + "'" + selected(item.id, project.id) + ">" + escapeHtml(item.name) + "</option>";
    }).join("");
    return "<div class='project-switcher'><label class='visually-hidden' for='hp-project-switcher'>Active project</label><select id='hp-project-switcher' data-action='switch-project'>" + options + "</select><button class='secondary' type='button' data-action='new-project'>New project</button></div>";
  }

  function renderTabs() {
    const tabs = [
      ["overview", "Overview"],
      ["scope", "Scope"],
      ["quotes", "Quotes"],
      ["documents", "Checks and documents"],
      ["evidence", "Evidence notes"],
      ["export", "Export and privacy"]
    ];
    return "<div class='app-tabs' role='tablist' aria-label='HomeProof project sections'>" + tabs.map(function (tab) {
      return "<button type='button' role='tab' data-tab='" + tab[0] + "' aria-selected='" + (activeTab === tab[0] ? "true" : "false") + "'>" + tab[1] + "</button>";
    }).join("") + "</div>";
  }

  function metric(title, done, total, description) {
    const percent = percentage(done, total);
    return "<div class='metric'><strong>" + escapeHtml(done + "/" + total) + "</strong><span>" + escapeHtml(title) + "</span><div class='progress-track' aria-label='" + escapeHtml(title + " " + percent + "%") + "'><span style='width:" + percent + "%'></span></div><span>" + escapeHtml(description) + "</span></div>";
  }

  function renderOverview(project) {
    const progress = Core.projectProgress(project);
    const comparison = Core.quoteComparison(project);
    const quotesWithWarnings = comparison.filter(function (item) { return item.warnings.length; }).length;
    const legacy = project.linkedPlanningWorkspace;
    return "<section class='app-view' data-view='overview'" + (activeTab === "overview" ? "" : " hidden") + ">" +
      "<div class='dashboard-grid'>" +
      metric("Scope decisions", progress.scope.done, progress.scope.total, "Items marked included, excluded or not applicable.") +
      metric("Approval checks", progress.approvals.done, progress.approvals.total, "Checks with a recorded status.") +
      metric("Completion records", progress.completionDocuments.done, progress.completionDocuments.total, "Documents with a recorded status.") +
      "<div class='metric'><strong>" + project.quotes.length + "</strong><span>Quotes recorded</span><span>" + quotesWithWarnings + " quote" + (quotesWithWarnings === 1 ? " has" : "s have") + " comparison warnings.</span></div>" +
      "</div>" +
      "<div class='panel'><span class='eyebrow'>Project details</span><h2>Keep The Core Record Current</h2><form data-project-details-form><div class='form-grid'>" +
      "<div class='form-field'><label for='detail-name'>Project name</label><input id='detail-name' name='name' maxlength='120' value='" + escapeHtml(project.name) + "'></div>" +
      "<div class='form-field'><label for='detail-stage'>Current stage</label><select id='detail-stage' name='stage'><option value='researching'" + selected(project.stage, "researching") + ">Researching</option><option value='seeking-quotes'" + selected(project.stage, "seeking-quotes") + ">Seeking quotes</option><option value='work-underway'" + selected(project.stage, "work-underway") + ">Work underway</option><option value='completion'" + selected(project.stage, "completion") + ">Completion and records</option></select></div>" +
      "<div class='form-field'><label for='detail-property'>Property label</label><input id='detail-property' name='propertyLabel' maxlength='160' value='" + escapeHtml(project.propertyLabel) + "'></div>" +
      "<div class='form-field'><label for='detail-council'>Council or area</label><input id='detail-council' name='councilLabel' maxlength='120' value='" + escapeHtml(project.councilLabel) + "'></div>" +
      "<div class='form-field full'><label for='detail-notes'>Project notes</label><textarea id='detail-notes' name='notes' maxlength='3000'>" + escapeHtml(project.notes) + "</textarea></div>" +
      "</div><div class='button-row'><button class='primary' type='submit'>Save project details</button>" + (project.planningGuide ? "<a class='button secondary' href='" + escapeHtml(project.planningGuide) + "'>Open matching planning guide</a>" : "") + "</div></form></div>" +
      (legacy ? renderLegacySummary(legacy) : (legacyAvailable(project) ? "<div class='notice'><span class='eyebrow'>Existing workspace found</span><h2>Link Your Current My Planning Project Record</h2><p>HomeProof can copy the saved-page, task and result summary from the existing browser workspace. It does not delete or change the original.</p><div class='button-row'><button class='primary' type='button' data-action='import-legacy'>Link existing planning workspace</button><button class='secondary' type='button' data-action='dismiss-legacy'>Not now</button></div></div>" : "")) +
      "</section>";
  }

  function renderLegacySummary(legacy) {
    return "<div class='legacy-card'><span class='eyebrow'>Linked planning workspace</span><h2>Earlier Planning Work Retained</h2><div class='dashboard-grid'><div class='metric'><strong>" + legacy.savedPages.length + "</strong><span>Saved pages</span></div><div class='metric'><strong>" + legacy.tasks.length + "</strong><span>Tasks</span></div><div class='metric'><strong>" + legacy.checks.length + "</strong><span>Completed checks</span></div><div class='metric'><strong>" + legacy.results.length + "</strong><span>Saved results</span></div></div><p>The original browser workspace remains unchanged. This summary is included in HomeProof exports.</p></div>";
  }

  function renderScope(project) {
    const groups = {};
    project.scopeItems.forEach(function (item) {
      groups[item.sectionId] = groups[item.sectionId] || { name: item.sectionName || "Scope", items: [] };
      groups[item.sectionId].items.push(item);
    });
    const html = Object.keys(groups).map(function (sectionId) {
      const group = groups[sectionId];
      return "<div class='scope-section'><h3>" + escapeHtml(group.name) + "</h3>" + group.items.map(function (item) {
        return "<div class='scope-item' data-scope-item='" + escapeHtml(item.id) + "'><div class='scope-copy'><strong>" + escapeHtml(item.label) + "</strong><p>" + escapeHtml(item.help) + "</p></div>" +
          "<div class='form-field'><label for='scope-status-" + escapeHtml(item.id) + "'>Project status</label><select id='scope-status-" + escapeHtml(item.id) + "' data-scope-field='status'><option value='unknown'" + selected(item.status, "unknown") + ">Not decided</option><option value='included'" + selected(item.status, "included") + ">Include in scope</option><option value='excluded'" + selected(item.status, "excluded") + ">Explicitly excluded</option><option value='not-applicable'" + selected(item.status, "not-applicable") + ">Not applicable</option></select></div>" +
          "<div class='form-field'><label for='scope-responsible-" + escapeHtml(item.id) + "'>Responsible party</label><select id='scope-responsible-" + escapeHtml(item.id) + "' data-scope-field='responsible'><option value='unknown'" + selected(item.responsible, "unknown") + ">Not decided</option><option value='contractor'" + selected(item.responsible, "contractor") + ">Main contractor</option><option value='homeowner'" + selected(item.responsible, "homeowner") + ">Homeowner</option><option value='specialist'" + selected(item.responsible, "specialist") + ">Separate specialist</option><option value='designer'" + selected(item.responsible, "designer") + ">Designer or engineer</option></select></div>" +
          "<div class='form-field item-notes'><label for='scope-notes-" + escapeHtml(item.id) + "'>Specification or assumptions</label><textarea id='scope-notes-" + escapeHtml(item.id) + "' data-scope-field='notes' maxlength='2000'>" + escapeHtml(item.notes) + "</textarea></div></div>";
      }).join("") + "</div>";
    }).join("");
    return "<section class='app-view' data-view='scope'" + (activeTab === "scope" ? "" : " hidden") + "><span class='eyebrow'>Comparable scope</span><h2>Define What Every Quote Should Cover</h2><p>Mark included work before comparing prices. Items deliberately excluded should remain visible so the omission is not mistaken for a cheaper complete quote.</p><div class='section-stack'>" + html + "</div></section>";
  }

  function quoteForm(project) {
    const includedItems = project.scopeItems.filter(function (item) { return item.status === "included"; });
    return "<div class='panel no-print'><span class='eyebrow'>Add quote</span><h2>Record One Quote Against The Same Scope</h2><form data-quote-form><div class='form-grid'>" +
      "<div class='form-field'><label for='quote-contractor'>Contractor or quote label</label><input id='quote-contractor' name='contractorName' maxlength='160' required></div>" +
      "<div class='form-field'><label for='quote-amount'>Quoted amount (£)</label><input id='quote-amount' name='quotedAmount' type='number' min='0' step='0.01' inputmode='decimal'></div>" +
      "<div class='form-field'><label for='quote-vat'>VAT treatment</label><select id='quote-vat' name='vatStatus'><option value='unknown'>Unknown</option><option value='included'>VAT included</option><option value='excluded'>VAT excluded</option><option value='not-registered'>Contractor says not VAT registered</option></select></div>" +
      "<div class='form-field'><label for='quote-deposit'>Deposit (£)</label><input id='quote-deposit' name='depositAmount' type='number' min='0' step='0.01' inputmode='decimal'></div>" +
      "<div class='form-field'><label for='quote-duration'>Duration or programme</label><input id='quote-duration' name='durationText' maxlength='120' placeholder='For example: 10–12 weeks'></div>" +
      "<div class='form-field'><label for='quote-start'>Proposed start</label><input id='quote-start' name='proposedStart' maxlength='40' placeholder='Date or stated lead time'></div>" +
      "<div class='form-field full'><label for='quote-warranty'>Warranty position</label><input id='quote-warranty' name='warrantyText' maxlength='300' placeholder='Record duration, provider and exclusions'></div>" +
      "<div class='form-field full'><label for='quote-notes'>Quote notes and exclusions</label><textarea id='quote-notes' name='notes' maxlength='2000'></textarea></div>" +
      "</div><fieldset><legend class='field-label'>Included scope items covered by this quote</legend>" + (includedItems.length ? "<ul class='coverage-list'>" + includedItems.map(function (item) {
        return "<li><input id='quote-scope-" + escapeHtml(item.id) + "' type='checkbox' name='includedScopeIds' value='" + escapeHtml(item.id) + "'><label for='quote-scope-" + escapeHtml(item.id) + "'>" + escapeHtml(item.label) + "</label></li>";
      }).join("") + "</ul>" : "<p class='privacy-note'>No scope items are marked included yet. Define the scope first so quote omissions can be detected.</p>") + "</fieldset><div class='button-row'><button class='primary' type='submit'>Add quote</button></div></form></div>";
  }

  function money(value) {
    return value == null ? "Not entered" : new Intl.NumberFormat("en-GB", { style: "currency", currency: "GBP" }).format(value);
  }

  function renderQuotes(project) {
    const comparisons = Core.quoteComparison(project);
    const quoteCards = project.quotes.length ? project.quotes.map(function (quote) {
      const comparison = comparisons.find(function (item) { return item.quoteId === quote.id; });
      return "<article class='quote-card'><div class='card-kicker'>Quote</div><h3>" + escapeHtml(quote.contractorName || "Unnamed quote") + "</h3><div class='quote-summary'><strong>Entered: " + escapeHtml(money(quote.quotedAmount)) + "</strong><span>Comparable total: " + escapeHtml(money(comparison && comparison.totalIncludingVat)) + "</span><span>Scope coverage: " + escapeHtml(String(comparison ? comparison.coveragePercent : 0)) + "%</span><span>Deposit: " + escapeHtml(money(quote.depositAmount)) + "</span><span>Duration: " + escapeHtml(quote.durationText || "Not recorded") + "</span><span>Warranty: " + escapeHtml(quote.warrantyText || "Not recorded") + "</span></div>" +
        ((comparison && comparison.warnings.length) ? comparison.warnings.map(function (warning) { return "<p class='quote-warning'>" + escapeHtml(warning) + "</p>"; }).join("") : "<p>All standard comparison fields have a recorded value.</p>") +
        (comparison && comparison.missingScopeItems.length ? "<details><summary>Scope items not marked covered</summary><ul>" + comparison.missingScopeItems.map(function (item) { return "<li>" + escapeHtml(item.label) + "</li>"; }).join("") + "</ul></details>" : "") +
        (quote.notes ? "<p><strong>Notes:</strong> " + escapeHtml(quote.notes) + "</p>" : "") +
        "<div class='button-row no-print'><button class='danger' type='button' data-action='delete-quote' data-quote-id='" + escapeHtml(quote.id) + "'>Delete quote</button></div></article>";
    }).join("") : "<div class='empty-state'><h3>No quotes recorded</h3><p>Add quotes only after defining at least the major included scope items.</p></div>";

    const table = project.quotes.length ? "<div class='panel'><span class='eyebrow'>Side-by-side summary</span><h2>Quote Comparison</h2><div class='table-wrap'><table><thead><tr><th>Quote</th><th>Comparable total</th><th>VAT</th><th>Deposit</th><th>Duration</th><th>Scope coverage</th><th>Warnings</th></tr></thead><tbody>" + project.quotes.map(function (quote) {
      const comparison = comparisons.find(function (item) { return item.quoteId === quote.id; });
      return "<tr><td>" + escapeHtml(quote.contractorName || "Unnamed") + "</td><td>" + escapeHtml(money(comparison && comparison.totalIncludingVat)) + "</td><td>" + escapeHtml(quote.vatStatus) + "</td><td>" + escapeHtml(money(quote.depositAmount)) + "</td><td>" + escapeHtml(quote.durationText || "Not recorded") + "</td><td>" + escapeHtml(String(comparison ? comparison.coveragePercent : 0)) + "%</td><td>" + escapeHtml(String(comparison ? comparison.warnings.length : 0)) + "</td></tr>";
    }).join("") + "</tbody></table></div></div>" : "";

    return "<section class='app-view' data-view='quotes'" + (activeTab === "quotes" ? "" : " hidden") + "><span class='eyebrow'>Quote comparison</span><h2>Compare Coverage Before Price</h2><p>HomeProof does not recommend a contractor. It makes missing scope, unclear VAT and absent commercial terms visible.</p>" + quoteForm(project) + table + "<div class='quote-grid'>" + quoteCards + "</div></section>";
  }

  function documentStatusSelect(item, prefix) {
    return "<select id='" + prefix + "-status-" + escapeHtml(item.id) + "' data-document-field='status'><option value='unknown'" + selected(item.status, "unknown") + ">Not recorded</option><option value='needed'" + selected(item.status, "needed") + ">Needed</option><option value='requested'" + selected(item.status, "requested") + ">Requested or in progress</option><option value='received'" + selected(item.status, "received") + ">Received or confirmed</option><option value='not-applicable'" + selected(item.status, "not-applicable") + ">Not applicable</option></select>";
  }

  function renderDocumentList(items, category, title) {
    return "<div class='document-section' data-document-category='" + category + "'><h3>" + title + "</h3>" + items.map(function (item) {
      return "<div class='document-item' data-document-id='" + escapeHtml(item.id) + "'><div class='document-copy'><strong>" + escapeHtml(item.label) + "</strong>" + (item.officialLink ? "<p><a href='" + escapeHtml(item.officialLink) + "'>Open relevant UK Planning Guide page</a></p>" : "") + "</div><div class='form-field'><label for='" + category + "-status-" + escapeHtml(item.id) + "'>Status</label>" + documentStatusSelect(item, category) + "</div><div class='form-field'><label for='" + category + "-reference-" + escapeHtml(item.id) + "'>Reference or location</label><input id='" + category + "-reference-" + escapeHtml(item.id) + "' data-document-field='reference' maxlength='240' value='" + escapeHtml(item.reference) + "' placeholder='Reference, filename or where it is stored'></div><div class='form-field item-notes'><label for='" + category + "-notes-" + escapeHtml(item.id) + "'>Notes</label><textarea id='" + category + "-notes-" + escapeHtml(item.id) + "' data-document-field='notes' maxlength='2000'>" + escapeHtml(item.notes) + "</textarea></div></div>";
    }).join("") + "</div>";
  }

  function renderDocuments(project) {
    return "<section class='app-view' data-view='documents'" + (activeTab === "documents" ? "" : " hidden") + "><span class='eyebrow'>Approval and completion record</span><h2>Keep The Proof That Usually Goes Missing</h2><p>Statuses are prompts, not confirmation that a document is legally required or sufficient. Use the linked guidance and official bodies to verify the route.</p><div class='section-stack'>" + renderDocumentList(project.approvalChecks, "approval", "Planning, approval and design checks") + renderDocumentList(project.completionDocuments, "completion", "Completion certificates and records") + "</div></section>";
  }

  function renderEvidence(project) {
    const notes = project.evidenceNotes.length ? project.evidenceNotes.map(function (note) {
      return "<article class='evidence-card'><div class='card-kicker'>" + escapeHtml(note.date || "Undated record") + "</div><h3>" + escapeHtml(note.title || "Evidence note") + "</h3><p>" + escapeHtml(note.notes || "No notes entered") + "</p><div class='button-row no-print'><button class='danger' type='button' data-action='delete-evidence' data-evidence-id='" + escapeHtml(note.id) + "'>Delete note</button></div></article>";
    }).join("") : "<div class='empty-state'><h3>No evidence notes yet</h3><p>Record decisions, inspections, photographs held elsewhere and agreed changes without storing private files here.</p></div>";
    return "<section class='app-view' data-view='evidence'" + (activeTab === "evidence" ? "" : " hidden") + "><span class='eyebrow'>Project chronology</span><h2>Record Decisions And Evidence Held Elsewhere</h2><p>Keep text references here while photographs, certificates and identity documents remain in your chosen secure storage.</p><div class='panel no-print'><form data-evidence-form><div class='form-grid'><div class='form-field'><label for='evidence-title'>Record title</label><input id='evidence-title' name='title' maxlength='160' required placeholder='For example: Builder confirmed beam variation'></div><div class='form-field'><label for='evidence-date'>Date</label><input id='evidence-date' name='date' type='date'></div><div class='form-field full'><label for='evidence-notes'>Notes and file location</label><textarea id='evidence-notes' name='notes' maxlength='2000' required placeholder='Record what happened and where the original evidence is stored.'></textarea></div></div><div class='button-row'><button class='primary' type='submit'>Add evidence note</button></div></form></div><div class='section-stack'>" + notes + "</div></section>";
  }

  function renderExport(project) {
    return "<section class='app-view' data-view='export'" + (activeTab === "export" ? "" : " hidden") + "><span class='eyebrow'>Backup and handover</span><h2>Keep A Copy Outside This Browser</h2><div class='privacy-note'><strong>Current storage model:</strong> project data is stored in this browser only. Clearing site data, changing device or using private browsing can remove it. Export a JSON backup after meaningful changes.</div><div class='panel'><h3>Export this workspace</h3><p>The JSON backup includes all HomeProof projects on this device. It can be imported later into the same version or a compatible future version.</p><div class='button-row'><button class='primary' type='button' data-action='export-json'>Download JSON backup</button><button class='secondary' type='button' data-action='print-project'>Print active project pack</button></div></div><div class='panel no-print'><h3>Import a HomeProof backup</h3><p>Import replaces the current HomeProof collection after validation. Export the current collection first.</p><label class='file-input' for='homeproof-import'>Choose HomeProof JSON backup<input id='homeproof-import' type='file' accept='application/json,.json' data-action='import-json'></label></div><div class='panel no-print'><h3>Delete the active project</h3><p>This cannot be undone unless you exported a backup.</p><div class='button-row'><button class='danger' type='button' data-action='delete-project' data-project-id='" + escapeHtml(project.id) + "'>Delete active project</button><button class='danger' type='button' data-action='clear-homeproof'>Delete all HomeProof data</button></div></div></section>";
  }

  function renderWorkspace() {
    const project = activeProject();
    if (creatingNewProject || !project) {
      renderNewProjectForm();
      return;
    }
    root.innerHTML = "<div class='app-status' data-app-status aria-live='polite'></div>" +
      "<div class='app-header'><div><span class='eyebrow'>HomeProof by UK Planning Guide</span><h1>" + escapeHtml(project.name) + "</h1><p>" + escapeHtml(project.templateName) + " · " + escapeHtml(stageLabel(project.stage)) + (project.propertyLabel ? " · " + escapeHtml(project.propertyLabel) : "") + "</p></div>" + renderProjectSwitcher(project) + "</div>" +
      renderTabs() +
      renderOverview(project) +
      renderScope(project) +
      renderQuotes(project) +
      renderDocuments(project) +
      renderEvidence(project) +
      renderExport(project);
    track("homeproof_workspace_view", { template_id: project.templateId, stage: project.stage, project_count: state.projects.length });
  }

  function render() {
    if (!templatesDocument) {
      root.innerHTML = "<div class='app-view'><div class='empty-state'><h2>Loading HomeProof</h2><p>Preparing the project templates.</p></div></div>";
      return;
    }
    renderWorkspace();
  }

  function createProjectFromForm(form) {
    const data = new FormData(form);
    const template = Core.findTemplate(templatesDocument, data.get("templateId"));
    if (!template) {
      setStatus("Choose a supported project type.", "error");
      return;
    }
    const project = Core.createProject({
      name: data.get("name"),
      propertyLabel: data.get("propertyLabel"),
      councilLabel: data.get("councilLabel"),
      stage: data.get("stage"),
      notes: data.get("notes")
    }, template);
    state.projects.push(project);
    state.activeProjectId = project.id;
    creatingNewProject = false;
    activeTab = "overview";
    writeState();
    track("homeproof_project_created", { template_id: project.templateId, stage: project.stage, project_count: state.projects.length });
    render();
    setStatus("HomeProof project created.", "success");
  }

  function saveProjectDetails(form) {
    const data = new FormData(form);
    updateActiveProject(function (project) {
      project.name = Core.cleanString(data.get("name"), 120) || project.templateName;
      project.stage = Core.VALID_STAGES.indexOf(data.get("stage")) !== -1 ? data.get("stage") : project.stage;
      project.propertyLabel = Core.cleanString(data.get("propertyLabel"), 160);
      project.councilLabel = Core.cleanString(data.get("councilLabel"), 120);
      project.notes = Core.cleanString(data.get("notes"), 3000);
    }, "Project details saved.");
    render();
    setStatus("Project details saved.", "success");
  }

  function addQuote(form) {
    const data = new FormData(form);
    const includedScopeIds = data.getAll("includedScopeIds");
    const project = activeProject();
    const validScopeIds = project.scopeItems.map(function (item) { return item.id; });
    const quote = {
      id: Core.randomId("quote"),
      contractorName: data.get("contractorName"),
      quotedAmount: Core.cleanNumber(data.get("quotedAmount")),
      vatStatus: data.get("vatStatus"),
      vatRate: 20,
      depositAmount: Core.cleanNumber(data.get("depositAmount")),
      durationText: data.get("durationText"),
      proposedStart: data.get("proposedStart"),
      warrantyText: data.get("warrantyText"),
      notes: data.get("notes"),
      includedScopeIds: includedScopeIds.filter(function (id) { return validScopeIds.indexOf(id) !== -1; }),
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString()
    };
    updateActiveProject(function (draft) {
      draft.quotes.push(quote);
    }, "Quote added.");
    track("homeproof_quote_added", { template_id: project.templateId, vat_status: quote.vatStatus, included_scope_count: quote.includedScopeIds.length, quote_count: project.quotes.length + 1 });
    render();
    setStatus("Quote added.", "success");
  }

  function addEvidence(form) {
    const data = new FormData(form);
    const project = activeProject();
    updateActiveProject(function (draft) {
      draft.evidenceNotes.unshift({
        id: Core.randomId("evidence"),
        title: Core.cleanString(data.get("title"), 160),
        date: Core.cleanString(data.get("date"), 40),
        notes: Core.cleanString(data.get("notes"), 2000),
        createdAt: new Date().toISOString()
      });
    }, "Evidence note added.");
    track("homeproof_evidence_note_added", { template_id: project.templateId, evidence_count: project.evidenceNotes.length + 1 });
    render();
    setStatus("Evidence note added.", "success");
  }

  function downloadBackup() {
    const blob = new Blob([Core.serialiseState(state)], { type: "application/json;charset=utf-8" });
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    link.download = "homeproof-backup-" + new Date().toISOString().slice(0, 10) + ".json";
    document.body.appendChild(link);
    link.click();
    link.remove();
    window.setTimeout(function () { URL.revokeObjectURL(url); }, 1000);
    const project = activeProject();
    track("homeproof_export_json", { project_count: state.projects.length, active_template_id: project ? project.templateId : "" });
    setStatus("HomeProof backup downloaded.", "success");
  }

  function importBackup(file) {
    if (!file) {
      return;
    }
    const reader = new FileReader();
    reader.onload = function () {
      try {
        const imported = Core.parseState(String(reader.result || ""));
        state = imported;
        creatingNewProject = false;
        writeState();
        activeTab = "overview";
        track("homeproof_import_json", { project_count: state.projects.length });
        render();
        setStatus("HomeProof backup imported.", "success");
      } catch (error) {
        setStatus(error.message || "The backup could not be imported.", "error");
      }
    };
    reader.onerror = function () {
      setStatus("The selected backup could not be read.", "error");
    };
    reader.readAsText(file);
  }

  root.addEventListener("submit", function (event) {
    const form = event.target;
    if (form.matches("[data-new-project-form]")) {
      event.preventDefault();
      createProjectFromForm(form);
      return;
    }
    if (form.matches("[data-project-details-form]")) {
      event.preventDefault();
      saveProjectDetails(form);
      return;
    }
    if (form.matches("[data-quote-form]")) {
      event.preventDefault();
      addQuote(form);
      return;
    }
    if (form.matches("[data-evidence-form]")) {
      event.preventDefault();
      addEvidence(form);
    }
  });

  root.addEventListener("change", function (event) {
    const target = event.target;
    if (target.matches("[data-action='switch-project']")) {
      state.activeProjectId = target.value;
      activeTab = "overview";
      writeState();
      render();
      return;
    }
    const scopeItem = target.closest("[data-scope-item]");
    if (scopeItem && target.hasAttribute("data-scope-field")) {
      const itemId = scopeItem.getAttribute("data-scope-item");
      const field = target.getAttribute("data-scope-field");
      const project = activeProject();
      updateActiveProject(function (draft) {
        const item = draft.scopeItems.find(function (candidate) { return candidate.id === itemId; });
        if (item && ["status", "responsible", "notes"].indexOf(field) !== -1) {
          item[field] = target.value;
        }
      });
      if (field === "status") {
        track("homeproof_scope_status_changed", { template_id: project.templateId, item_id: itemId, status: target.value });
      }
      setStatus("Scope saved on this device.", "success");
      return;
    }
    const documentItem = target.closest("[data-document-id]");
    if (documentItem && target.hasAttribute("data-document-field")) {
      const itemId = documentItem.getAttribute("data-document-id");
      const categoryRoot = target.closest("[data-document-category]");
      const category = categoryRoot ? categoryRoot.getAttribute("data-document-category") : "approval";
      const field = target.getAttribute("data-document-field");
      const project = activeProject();
      updateActiveProject(function (draft) {
        const collection = category === "completion" ? draft.completionDocuments : draft.approvalChecks;
        const item = collection.find(function (candidate) { return candidate.id === itemId; });
        if (item && ["status", "reference", "notes"].indexOf(field) !== -1) {
          item[field] = target.value;
        }
      });
      if (field === "status") {
        track("homeproof_document_status_changed", { template_id: project.templateId, document_id: itemId, category: category, status: target.value });
      }
      setStatus("Document record saved on this device.", "success");
      return;
    }
    if (target.matches("[data-action='import-json']")) {
      importBackup(target.files && target.files[0]);
    }
  });

  root.addEventListener("input", function (event) {
    const target = event.target;
    const scopeItem = target.closest("[data-scope-item]");
    if (scopeItem && target.getAttribute("data-scope-field") === "notes") {
      const itemId = scopeItem.getAttribute("data-scope-item");
      updateActiveProject(function (draft) {
        const item = draft.scopeItems.find(function (candidate) { return candidate.id === itemId; });
        if (item) {
          item.notes = target.value;
        }
      });
    }
    const documentItem = target.closest("[data-document-id]");
    if (documentItem && ["reference", "notes"].indexOf(target.getAttribute("data-document-field")) !== -1) {
      const itemId = documentItem.getAttribute("data-document-id");
      const categoryRoot = target.closest("[data-document-category]");
      const category = categoryRoot ? categoryRoot.getAttribute("data-document-category") : "approval";
      const field = target.getAttribute("data-document-field");
      updateActiveProject(function (draft) {
        const collection = category === "completion" ? draft.completionDocuments : draft.approvalChecks;
        const item = collection.find(function (candidate) { return candidate.id === itemId; });
        if (item) {
          item[field] = target.value;
        }
      });
    }
  });

  root.addEventListener("click", function (event) {
    const tab = event.target.closest("[data-tab]");
    if (tab) {
      activeTab = tab.getAttribute("data-tab") || "overview";
      render();
      const newTab = root.querySelector("[data-tab='" + activeTab + "']");
      if (newTab) {
        newTab.focus();
      }
      return;
    }
    const button = event.target.closest("[data-action]");
    if (!button) {
      return;
    }
    const action = button.getAttribute("data-action");
    if (action === "new-project") {
      creatingNewProject = true;
      renderNewProjectForm();
      return;
    }
    if (action === "cancel-new-project") {
      creatingNewProject = false;
      render();
      return;
    }
    if (action === "export-json") {
      downloadBackup();
      return;
    }
    if (action === "print-project") {
      const project = activeProject();
      track("homeproof_print", { template_id: project ? project.templateId : "" });
      window.print();
      return;
    }
    if (action === "delete-quote") {
      const quoteId = button.getAttribute("data-quote-id");
      if (!window.confirm("Delete this quote record?")) {
        return;
      }
      updateActiveProject(function (project) {
        project.quotes = project.quotes.filter(function (quote) { return quote.id !== quoteId; });
      });
      render();
      setStatus("Quote deleted.", "success");
      return;
    }
    if (action === "delete-evidence") {
      const evidenceId = button.getAttribute("data-evidence-id");
      if (!window.confirm("Delete this evidence note?")) {
        return;
      }
      updateActiveProject(function (project) {
        project.evidenceNotes = project.evidenceNotes.filter(function (note) { return note.id !== evidenceId; });
      });
      render();
      setStatus("Evidence note deleted.", "success");
      return;
    }
    if (action === "import-legacy") {
      const legacy = loadLegacyWorkspace();
      const project = activeProject();
      updateActiveProject(function (draft) {
        const linked = Core.attachLegacyWorkspace(draft, legacy);
        draft.linkedPlanningWorkspace = linked.linkedPlanningWorkspace;
      });
      state.settings.legacyPromptDismissed = true;
      writeState();
      track("homeproof_legacy_imported", { template_id: project ? project.templateId : "" });
      render();
      setStatus("Existing planning workspace linked.", "success");
      return;
    }
    if (action === "dismiss-legacy") {
      state.settings.legacyPromptDismissed = true;
      writeState();
      render();
      return;
    }
    if (action === "delete-project") {
      const projectId = button.getAttribute("data-project-id");
      if (!window.confirm("Delete this HomeProof project? Export a backup first if it may be needed later.")) {
        return;
      }
      state.projects = state.projects.filter(function (project) { return project.id !== projectId; });
      state.activeProjectId = state.projects.length ? state.projects[0].id : "";
      creatingNewProject = false;
      activeTab = "overview";
      writeState();
      render();
      setStatus("Project deleted.", "success");
      return;
    }
    if (action === "clear-homeproof") {
      if (!window.confirm("Delete every HomeProof project stored in this browser?")) {
        return;
      }
      try {
        window.localStorage.removeItem(Core.STORAGE_KEY);
      } catch (error) {}
      state = Core.createEmptyState();
      creatingNewProject = false;
      activeTab = "overview";
      render();
      setStatus("All HomeProof data deleted from this browser.", "success");
    }
  });

  function initNavigation() {
    const header = document.querySelector(".site-header");
    const toggle = document.querySelector(".nav-toggle");
    if (!header || !toggle) {
      return;
    }
    toggle.addEventListener("click", function () {
      const open = header.getAttribute("data-menu-open") === "true";
      header.setAttribute("data-menu-open", open ? "false" : "true");
      toggle.setAttribute("aria-expanded", open ? "false" : "true");
    });
  }

  function loadTemplates() {
    return fetch(templateUrl, { credentials: "same-origin" })
      .then(function (response) {
        if (!response.ok) {
          throw new Error("Template request failed.");
        }
        return response.json();
      })
      .then(function (data) {
        if (!data || !Array.isArray(data.templates) || !data.templates.length) {
          throw new Error("No HomeProof templates were returned.");
        }
        templatesDocument = data;
      });
  }

  initNavigation();
  render();
  loadTemplates().then(function () {
    render();
    track("homeproof_app_loaded", { project_count: state.projects.length, storage_blocked: Boolean(state.storageBlocked) });
  }).catch(function () {
    root.innerHTML = "<div class='app-view'><div class='empty-state'><h2>HomeProof could not load</h2><p>The project template file was unavailable. Check that <code>" + escapeHtml(templateUrl) + "</code> was deployed with the page.</p></div></div>";
  });
}());
