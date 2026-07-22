(function (root, factory) {
  if (typeof module === "object" && module.exports) {
    module.exports = factory();
  } else {
    root.HomeProofCore = factory();
  }
}(typeof self !== "undefined" ? self : this, function () {
  "use strict";

  const SCHEMA_VERSION = 1;
  const STORAGE_KEY = "ukpg:homeproof:v1";
  const LEGACY_WORKSPACE_KEY = "ukpg:planning-workspace:v1";
  const VALID_STAGES = ["researching", "seeking-quotes", "work-underway", "completion"];
  const VALID_SCOPE_STATUSES = ["unknown", "included", "excluded", "not-applicable"];
  const VALID_DOCUMENT_STATUSES = ["unknown", "needed", "requested", "received", "not-applicable"];
  const VALID_VAT_STATUSES = ["included", "excluded", "not-registered", "unknown"];

  function nowIso() {
    return new Date().toISOString();
  }

  function randomId(prefix) {
    const cryptoObject = typeof globalThis !== "undefined" ? globalThis.crypto : null;
    if (cryptoObject && typeof cryptoObject.randomUUID === "function") {
      return String(prefix || "item") + "-" + cryptoObject.randomUUID();
    }
    return String(prefix || "item") + "-" + Date.now().toString(36) + "-" + Math.random().toString(36).slice(2, 10);
  }

  function clone(value) {
    return JSON.parse(JSON.stringify(value));
  }

  function asArray(value) {
    return Array.isArray(value) ? value : [];
  }

  function cleanString(value, maxLength) {
    const text = String(value == null ? "" : value).replace(/\u0000/g, "").trim();
    return typeof maxLength === "number" ? text.slice(0, maxLength) : text;
  }

  function cleanNumber(value) {
    if (value === "" || value == null) {
      return null;
    }
    const number = Number(value);
    return Number.isFinite(number) && number >= 0 ? Math.round(number * 100) / 100 : null;
  }

  function findTemplate(templatesDocument, templateId) {
    const templates = templatesDocument && Array.isArray(templatesDocument.templates)
      ? templatesDocument.templates
      : [];
    return templates.find(function (template) {
      return template && template.id === templateId;
    }) || null;
  }

  function flattenScope(template) {
    const result = [];
    asArray(template && template.scopeSections).forEach(function (section) {
      asArray(section.items).forEach(function (item) {
        result.push({
          id: item.id,
          sectionId: section.id,
          sectionName: section.name,
          label: item.label,
          help: item.help || ""
        });
      });
    });
    return result;
  }

  function buildScopeItems(template) {
    return flattenScope(template).map(function (item) {
      return Object.assign({}, item, {
        status: "unknown",
        responsible: "unknown",
        notes: ""
      });
    });
  }

  function buildDocumentItems(items, category) {
    return asArray(items).map(function (item) {
      return {
        id: item.id,
        category: category,
        label: item.label,
        officialLink: item.officialLink || "",
        status: "unknown",
        reference: "",
        notes: ""
      };
    });
  }

  function createProject(input, template) {
    if (!template || !template.id) {
      throw new Error("A valid HomeProof project template is required.");
    }
    const stage = VALID_STAGES.indexOf(input && input.stage) !== -1 ? input.stage : "researching";
    const createdAt = nowIso();
    return {
      id: randomId("project"),
      schemaVersion: SCHEMA_VERSION,
      templateId: template.id,
      templateName: template.name,
      planningGuide: template.planningGuide || "",
      name: cleanString(input && input.name, 120) || template.name,
      propertyLabel: cleanString(input && input.propertyLabel, 160),
      councilLabel: cleanString(input && input.councilLabel, 120),
      stage: stage,
      notes: cleanString(input && input.notes, 3000),
      scopeItems: buildScopeItems(template),
      approvalChecks: buildDocumentItems(template.approvalChecks, "approval"),
      completionDocuments: buildDocumentItems(template.completionDocuments, "completion"),
      quotes: [],
      evidenceNotes: [],
      linkedPlanningWorkspace: null,
      createdAt: createdAt,
      updatedAt: createdAt
    };
  }

  function createEmptyState() {
    return {
      schemaVersion: SCHEMA_VERSION,
      projects: [],
      activeProjectId: "",
      settings: {
        legacyPromptDismissed: false
      },
      createdAt: nowIso(),
      updatedAt: nowIso()
    };
  }

  function normaliseScopeItem(item) {
    const status = VALID_SCOPE_STATUSES.indexOf(item && item.status) !== -1 ? item.status : "unknown";
    return {
      id: cleanString(item && item.id, 120),
      sectionId: cleanString(item && item.sectionId, 120),
      sectionName: cleanString(item && item.sectionName, 160),
      label: cleanString(item && item.label, 240),
      help: cleanString(item && item.help, 500),
      status: status,
      responsible: cleanString(item && item.responsible, 80) || "unknown",
      notes: cleanString(item && item.notes, 2000)
    };
  }

  function normaliseDocumentItem(item, category) {
    const status = VALID_DOCUMENT_STATUSES.indexOf(item && item.status) !== -1 ? item.status : "unknown";
    return {
      id: cleanString(item && item.id, 120),
      category: category,
      label: cleanString(item && item.label, 240),
      officialLink: cleanString(item && item.officialLink, 500),
      status: status,
      reference: cleanString(item && item.reference, 240),
      notes: cleanString(item && item.notes, 2000)
    };
  }

  function normaliseQuote(quote, validScopeIds) {
    const includedScopeIds = asArray(quote && quote.includedScopeIds)
      .map(function (id) { return cleanString(id, 120); })
      .filter(function (id, index, values) {
        return id && validScopeIds.indexOf(id) !== -1 && values.indexOf(id) === index;
      });
    const vatStatus = VALID_VAT_STATUSES.indexOf(quote && quote.vatStatus) !== -1 ? quote.vatStatus : "unknown";
    return {
      id: cleanString(quote && quote.id, 140) || randomId("quote"),
      contractorName: cleanString(quote && quote.contractorName, 160),
      quotedAmount: cleanNumber(quote && quote.quotedAmount),
      vatStatus: vatStatus,
      vatRate: cleanNumber(quote && quote.vatRate) == null ? 20 : cleanNumber(quote && quote.vatRate),
      depositAmount: cleanNumber(quote && quote.depositAmount),
      durationText: cleanString(quote && quote.durationText, 120),
      proposedStart: cleanString(quote && quote.proposedStart, 40),
      warrantyText: cleanString(quote && quote.warrantyText, 300),
      notes: cleanString(quote && quote.notes, 2000),
      includedScopeIds: includedScopeIds,
      createdAt: cleanString(quote && quote.createdAt, 40) || nowIso(),
      updatedAt: cleanString(quote && quote.updatedAt, 40) || nowIso()
    };
  }

  function normaliseProject(project) {
    const scopeItems = asArray(project && project.scopeItems).map(normaliseScopeItem).filter(function (item) { return item.id; });
    const validScopeIds = scopeItems.map(function (item) { return item.id; });
    const stage = VALID_STAGES.indexOf(project && project.stage) !== -1 ? project.stage : "researching";
    return {
      id: cleanString(project && project.id, 140) || randomId("project"),
      schemaVersion: SCHEMA_VERSION,
      templateId: cleanString(project && project.templateId, 120),
      templateName: cleanString(project && project.templateName, 160),
      planningGuide: cleanString(project && project.planningGuide, 500),
      name: cleanString(project && project.name, 120) || "Home improvement project",
      propertyLabel: cleanString(project && project.propertyLabel, 160),
      councilLabel: cleanString(project && project.councilLabel, 120),
      stage: stage,
      notes: cleanString(project && project.notes, 3000),
      scopeItems: scopeItems,
      approvalChecks: asArray(project && project.approvalChecks).map(function (item) { return normaliseDocumentItem(item, "approval"); }).filter(function (item) { return item.id; }),
      completionDocuments: asArray(project && project.completionDocuments).map(function (item) { return normaliseDocumentItem(item, "completion"); }).filter(function (item) { return item.id; }),
      quotes: asArray(project && project.quotes).map(function (quote) { return normaliseQuote(quote, validScopeIds); }),
      evidenceNotes: asArray(project && project.evidenceNotes).map(function (note) {
        return {
          id: cleanString(note && note.id, 140) || randomId("evidence"),
          title: cleanString(note && note.title, 160),
          date: cleanString(note && note.date, 40),
          notes: cleanString(note && note.notes, 2000),
          createdAt: cleanString(note && note.createdAt, 40) || nowIso()
        };
      }),
      linkedPlanningWorkspace: project && project.linkedPlanningWorkspace && typeof project.linkedPlanningWorkspace === "object"
        ? clone(project.linkedPlanningWorkspace)
        : null,
      createdAt: cleanString(project && project.createdAt, 40) || nowIso(),
      updatedAt: cleanString(project && project.updatedAt, 40) || nowIso()
    };
  }

  function normaliseState(state) {
    const clean = createEmptyState();
    clean.projects = asArray(state && state.projects).map(normaliseProject);
    clean.activeProjectId = cleanString(state && state.activeProjectId, 140);
    if (!clean.projects.some(function (project) { return project.id === clean.activeProjectId; })) {
      clean.activeProjectId = clean.projects.length ? clean.projects[0].id : "";
    }
    clean.settings = {
      legacyPromptDismissed: Boolean(state && state.settings && state.settings.legacyPromptDismissed)
    };
    clean.createdAt = cleanString(state && state.createdAt, 40) || clean.createdAt;
    clean.updatedAt = nowIso();
    return clean;
  }

  function calculateQuoteTotal(quote) {
    const amount = cleanNumber(quote && quote.quotedAmount);
    if (amount == null) {
      return null;
    }
    const vatStatus = quote && quote.vatStatus;
    if (vatStatus === "excluded") {
      const rate = cleanNumber(quote && quote.vatRate);
      return Math.round(amount * (1 + (rate == null ? 20 : rate) / 100) * 100) / 100;
    }
    return amount;
  }

  function quoteComparison(project) {
    const scopeItems = asArray(project && project.scopeItems);
    const required = scopeItems.filter(function (item) {
      return item && item.status === "included";
    });
    return asArray(project && project.quotes).map(function (quote) {
      const includedIds = asArray(quote.includedScopeIds);
      const missing = required.filter(function (item) {
        return includedIds.indexOf(item.id) === -1;
      });
      const warnings = [];
      if (quote.quotedAmount == null) {
        warnings.push("No usable quoted total has been entered.");
      }
      if (quote.vatStatus === "unknown") {
        warnings.push("VAT treatment is not recorded.");
      }
      if (quote.depositAmount == null) {
        warnings.push("Deposit is not recorded.");
      }
      if (!quote.durationText) {
        warnings.push("Programme or duration is not recorded.");
      }
      if (!quote.warrantyText) {
        warnings.push("Warranty position is not recorded.");
      }
      if (missing.length) {
        warnings.push(String(missing.length) + " included scope item" + (missing.length === 1 ? " is" : "s are") + " not marked as covered.");
      }
      return {
        quoteId: quote.id,
        contractorName: quote.contractorName || "Unnamed quote",
        totalIncludingVat: calculateQuoteTotal(quote),
        missingScopeItems: missing.map(function (item) {
          return { id: item.id, label: item.label, sectionName: item.sectionName };
        }),
        coveragePercent: required.length ? Math.round(((required.length - missing.length) / required.length) * 100) : 100,
        warnings: warnings
      };
    });
  }

  function projectProgress(project) {
    const scope = asArray(project && project.scopeItems);
    const approvals = asArray(project && project.approvalChecks);
    const documents = asArray(project && project.completionDocuments);
    const decidedScope = scope.filter(function (item) { return item.status !== "unknown"; }).length;
    const progressedApprovals = approvals.filter(function (item) { return item.status !== "unknown"; }).length;
    const progressedDocuments = documents.filter(function (item) { return item.status !== "unknown"; }).length;
    return {
      scope: { done: decidedScope, total: scope.length },
      approvals: { done: progressedApprovals, total: approvals.length },
      completionDocuments: { done: progressedDocuments, total: documents.length },
      quotes: asArray(project && project.quotes).length,
      evidenceNotes: asArray(project && project.evidenceNotes).length
    };
  }

  function legacyWorkspaceSummary(legacy) {
    if (!legacy || typeof legacy !== "object") {
      return null;
    }
    const savedPages = asArray(legacy.saved_pages).slice(0, 30).map(function (item) {
      return {
        title: cleanString(item && item.title, 160),
        path: cleanString(item && item.path, 500),
        savedAt: cleanString(item && (item.saved_at || item.savedAt), 40)
      };
    });
    const tasks = asArray(legacy.tasks).slice(0, 30).map(function (item) {
      return {
        title: cleanString(item && (item.title || item.text), 200),
        path: cleanString(item && item.path, 500),
        completed: Boolean(item && item.completed)
      };
    });
    const checks = asArray(legacy.completed_checks).slice(0, 30).map(function (item) {
      return {
        title: cleanString(item && (item.result_label || item.title), 200),
        path: cleanString(item && item.path, 500)
      };
    });
    const results = asArray(legacy.result_summaries).slice(0, 30).map(function (item) {
      return {
        title: cleanString(item && (item.result_label || item.title), 200),
        path: cleanString(item && item.path, 500),
        summary: cleanString(item && item.summary, 500)
      };
    });
    if (!savedPages.length && !tasks.length && !checks.length && !results.length && !legacy.project_type && !legacy.location_label) {
      return null;
    }
    return {
      projectType: cleanString(legacy.project_type, 120),
      locationLabel: cleanString(legacy.location_label, 160),
      constraints: asArray(legacy.constraints).map(function (item) { return cleanString(item, 200); }).filter(Boolean).slice(0, 30),
      savedPages: savedPages,
      tasks: tasks,
      checks: checks,
      results: results,
      importedAt: nowIso()
    };
  }

  function attachLegacyWorkspace(project, legacy) {
    const summary = legacyWorkspaceSummary(legacy);
    if (!summary) {
      return project;
    }
    const clean = normaliseProject(project);
    clean.linkedPlanningWorkspace = summary;
    clean.updatedAt = nowIso();
    return clean;
  }

  function serialiseState(state) {
    return JSON.stringify(normaliseState(state), null, 2);
  }

  function parseState(text) {
    if (typeof text !== "string" || text.length > 5 * 1024 * 1024) {
      throw new Error("The HomeProof backup is not a supported size.");
    }
    let parsed;
    try {
      parsed = JSON.parse(text);
    } catch (error) {
      throw new Error("The selected file is not valid HomeProof JSON.");
    }
    if (!parsed || typeof parsed !== "object" || !Array.isArray(parsed.projects)) {
      throw new Error("The selected file does not contain a HomeProof project collection.");
    }
    return normaliseState(parsed);
  }

  return {
    SCHEMA_VERSION: SCHEMA_VERSION,
    STORAGE_KEY: STORAGE_KEY,
    LEGACY_WORKSPACE_KEY: LEGACY_WORKSPACE_KEY,
    VALID_STAGES: VALID_STAGES.slice(),
    VALID_SCOPE_STATUSES: VALID_SCOPE_STATUSES.slice(),
    VALID_DOCUMENT_STATUSES: VALID_DOCUMENT_STATUSES.slice(),
    VALID_VAT_STATUSES: VALID_VAT_STATUSES.slice(),
    createEmptyState: createEmptyState,
    createProject: createProject,
    normaliseState: normaliseState,
    normaliseProject: normaliseProject,
    findTemplate: findTemplate,
    flattenScope: flattenScope,
    calculateQuoteTotal: calculateQuoteTotal,
    quoteComparison: quoteComparison,
    projectProgress: projectProgress,
    legacyWorkspaceSummary: legacyWorkspaceSummary,
    attachLegacyWorkspace: attachLegacyWorkspace,
    serialiseState: serialiseState,
    parseState: parseState,
    randomId: randomId,
    cleanString: cleanString,
    cleanNumber: cleanNumber,
    clone: clone
  };
}));
