(function () {
  "use strict";

  const PROJECT_LABELS = {
    "single-storey-extension": "Single-storey extension",
    "two-storey-extension": "Two-storey extension",
    "loft-conversion": "Loft conversion",
    "garage-conversion": "Garage conversion",
    "garden-room-outbuilding": "Garden room / outbuilding",
    "shed-greenhouse": "Shed / greenhouse",
    "fence-wall-gate": "Fence, wall or gate",
    "driveway-hardstanding": "Driveway / hardstanding",
    "dropped-kerb-vehicle-access": "Dropped kerb / vehicle access",
    "solar-panels": "Solar panels",
    porch: "Porch",
    "hmo-change-of-use": "HMO / change of use",
    other: "Other"
  };

  const PROPERTY_LABELS = {
    "detached-house": "Detached house",
    "semi-detached-house": "Semi-detached house",
    "terraced-house": "Terraced house",
    bungalow: "Bungalow",
    "flat-maisonette": "Flat / maisonette",
    "listed-building": "Listed building",
    "commercial-mixed-use": "Commercial / mixed-use",
    "not-sure": "Not sure"
  };

  const RESTRICTION_LABELS = {
    "conservation-area": "Conservation area",
    "listed-building": "Listed building",
    "article-4": "Article 4 direction",
    "protected-landscape": "National park / AONB / protected landscape",
    "previous-condition": "Previous planning condition",
    "leasehold-shared-freeholder": "Leasehold/shared/freeholder restriction",
    "not-sure": "Not sure"
  };

  const TIMEFRAME_LABELS = {
    researching: "Just researching",
    "within-3-months": "Within 3 months",
    "3-6-months": "3-6 months",
    "6-12-months": "6-12 months",
    "already-started": "Already started",
    "urgent-problem": "Urgent/problem has come up"
  };

  const HELP_LABELS = {
    "route-only": "Just show me the likely route",
    "professional-planning-design-help": "I may want professional planning/design help",
    "drawings-application-help": "I need drawings/application help",
    "refusal-enforcement-help": "I need help after a refusal/enforcement issue",
    "contractor-specialist": "I need a contractor/specialist"
  };

  const ROUTE_TYPES = {
    pd: "Permitted development may be possible",
    permission: "Planning permission may be needed",
    highways: "Council/highways approval is likely to be needed",
    professional: "Professional review strongly recommended",
    mixed: "More information needed"
  };

  function escapeHtml(value) {
    return String(value || "").replace(/[&<>"']/g, function (char) {
      return {
        "&": "&amp;",
        "<": "&lt;",
        ">": "&gt;",
        '"': "&quot;",
        "'": "&#39;"
      }[char];
    });
  }

  function getLabel(map, value) {
    return map[value] || value || "";
  }

  function getLeadConfig() {
    return window.UKPG_LEAD_CONFIG || window.UKPG_LEAD_CAPTURE_CONFIG || {};
  }

  function emitEvent(name, params) {
    if (typeof window.gtag !== "function") {
      return;
    }
    window.gtag("event", name, params || {});
  }

  function safeStorageSet(key, value) {
    try {
      if (window.localStorage) {
        window.localStorage.setItem(key, JSON.stringify(value));
      }
    } catch (error) {
      return;
    }
  }

  function listHtml(items) {
    return "<ul class=\"checklist\">" + items.map(function (item) {
      return "<li>" + escapeHtml(item) + "</li>";
    }).join("") + "</ul>";
  }

  function getAnswers(form) {
    const data = new FormData(form);
    const restrictions = data.getAll("restrictions");
    return {
      project_type: data.get("project_type") || "",
      property_type: data.get("property_type") || "",
      postcode_or_town: String(data.get("postcode_or_town") || "").trim(),
      council: String(data.get("council") || "").trim(),
      restrictions: restrictions,
      timeframe: data.get("timeframe") || "",
      desired_help: data.get("desired_help") || "",
      user_notes: String(data.get("user_notes") || "").trim()
    };
  }

  function hasRestriction(answers, key) {
    return answers.restrictions.indexOf(key) !== -1;
  }

  function isExtension(projectType) {
    return [
      "single-storey-extension",
      "two-storey-extension",
      "porch"
    ].indexOf(projectType) !== -1;
  }

  function addUnique(items, text) {
    if (items.indexOf(text) === -1) {
      items.push(text);
    }
  }

  function evaluateRoute(answers) {
    const why = [];
    const warnings = [
      "Building regulations may still apply even where planning permission is not required."
    ];
    const nextSteps = [
      "Check the relevant local council planning guidance before work begins.",
      "Gather measurements, photos, boundary details and any planning-history notes."
    ];
    let route = ROUTE_TYPES.mixed;
    let confidence = "Low";
    let cautionScore = 0;

    const listed = answers.property_type === "listed-building" || hasRestriction(answers, "listed-building");
    const flat = answers.property_type === "flat-maisonette";
    const conservation = hasRestriction(answers, "conservation-area");
    const article4 = hasRestriction(answers, "article-4");
    const protectedLandscape = hasRestriction(answers, "protected-landscape");
    const previousCondition = hasRestriction(answers, "previous-condition");
    const notSureRestriction = hasRestriction(answers, "not-sure");
    const helpWantsProfessional = [
      "professional-planning-design-help",
      "drawings-application-help",
      "refusal-enforcement-help",
      "contractor-specialist"
    ].indexOf(answers.desired_help) !== -1;

    if (answers.project_type === "dropped-kerb-vehicle-access") {
      route = ROUTE_TYPES.highways;
      confidence = "High";
      addUnique(why, "Dropped kerbs and vehicle access normally involve the council or highway authority, even where the planning question looks separate.");
      addUnique(warnings, "Dropped kerbs involve council/highways approval and may also need planning permission depending on the road and frontage.");
      addUnique(nextSteps, "Check your council or highway authority dropped-kerb process before arranging driveway work.");
    } else if (answers.project_type === "hmo-change-of-use") {
      route = "Planning and licensing checks are likely";
      confidence = "Medium";
      cautionScore += 2;
      addUnique(why, "HMO and change-of-use projects depend heavily on use class, local policy, licensing and Article 4 coverage.");
      addUnique(warnings, "HMO and change-of-use routes are council-specific and may involve both planning and licensing checks.");
      addUnique(nextSteps, "Check the council's HMO, licensing and Article 4 guidance for the exact property.");
    } else if (["garden-room-outbuilding", "shed-greenhouse"].indexOf(answers.project_type) !== -1) {
      route = ROUTE_TYPES.pd;
      confidence = "Medium";
      addUnique(why, "Garden rooms, sheds and outbuildings can sometimes use permitted development where the use stays incidental and the building stays within limits.");
      addUnique(warnings, "Outbuildings still need checks on height, position, intended use, overall size and how much land is covered.");
      addUnique(nextSteps, "Check height, eaves height, boundary position, total land coverage and whether the use remains incidental to the house.");
    } else if (isExtension(answers.project_type)) {
      route = ROUTE_TYPES.permission;
      confidence = "Medium";
      addUnique(why, "Extension routes depend on size, height, depth, position, previous additions and property type.");
      addUnique(warnings, "A lawful development certificate may be sensible if you plan to rely on permitted development for an extension.");
      addUnique(nextSteps, "Compare the design against permitted development limits, then consider a lawful development certificate if the route appears to fit.");
    } else if (answers.project_type === "loft-conversion") {
      route = ROUTE_TYPES.pd;
      confidence = "Medium";
      addUnique(why, "Some loft conversions can use permitted development, but dormers, roof form, volume, front-facing changes and restrictions can change the route.");
      addUnique(warnings, "Roof alterations may need a stricter check where the roof change is visible from the road or the property is restricted.");
      addUnique(nextSteps, "Check roof volume, dormer position, roof-plane visibility and whether the property has normal householder rights.");
    } else if (answers.project_type === "garage-conversion") {
      route = ROUTE_TYPES.pd;
      confidence = "Medium";
      addUnique(why, "Garage conversions can sometimes be straightforward, but planning conditions, frontage change and parking policy can change the route.");
      addUnique(warnings, "Previous planning conditions can remove normal conversion assumptions for garages.");
      addUnique(nextSteps, "Check the property's planning history for garage-retention or parking conditions.");
    } else if (answers.project_type === "driveway-hardstanding") {
      route = "Planning permission or drainage checks may be needed";
      confidence = "Medium";
      addUnique(why, "Driveways and hardstanding often turn on drainage, permeable surfacing, frontage design and whether a dropped kerb is involved.");
      addUnique(warnings, "A driveway and a dropped kerb are separate checks: the surface may be one issue and highway access another.");
      addUnique(nextSteps, "Check permeable-surface rules and any separate dropped-kerb or highway approval process.");
    } else if (answers.project_type === "fence-wall-gate") {
      route = "Permitted development may be possible, but height and highway position matter";
      confidence = "Medium";
      addUnique(why, "Fence, wall and gate rules usually depend on height, highway position and whether special controls apply.");
      addUnique(warnings, "Boundary works near a highway can have lower height limits and visibility issues.");
      addUnique(nextSteps, "Check the height from the relevant ground level and whether the boundary fronts a highway.");
    } else if (answers.project_type === "solar-panels") {
      route = ROUTE_TYPES.pd;
      confidence = "Medium";
      addUnique(why, "Solar panels may be permitted development, but listed status, conservation areas, roof visibility and siting can change the answer.");
      addUnique(warnings, "Solar panels on listed buildings or in sensitive locations need more careful consent checks.");
      addUnique(nextSteps, "Check roof/wall siting, visibility and any listed-building or conservation-area controls.");
    } else {
      route = ROUTE_TYPES.mixed;
      confidence = "Low";
      addUnique(why, "The selected project type needs more detail before a reliable planning route can be narrowed.");
      addUnique(nextSteps, "Use the nearest project guide or council page to identify the exact route question.");
    }

    if (flat) {
      cautionScore += 2;
      addUnique(why, "Flats and maisonettes usually have fewer householder permitted development rights than houses.");
      addUnique(warnings, "Flats and maisonettes often have fewer permitted development rights, and lease/freeholder restrictions may also matter.");
      addUnique(nextSteps, "Check flat/maisonette rights, lease terms and management/freeholder requirements before relying on permitted development.");
    }

    if (listed) {
      route = ROUTE_TYPES.professional;
      confidence = "High";
      cautionScore += 3;
      addUnique(why, "Listed building status can create a separate consent route even for work that might otherwise look modest.");
      addUnique(warnings, "Listed buildings usually need specialist listed building consent checks before work starts.");
      addUnique(nextSteps, "Speak to the council conservation team or a specialist before making changes to a listed building.");
    }

    if (conservation) {
      cautionScore += 2;
      addUnique(why, "Conservation areas can make visible changes, roof works, demolition and frontage changes more sensitive.");
      addUnique(warnings, "Conservation areas can restrict normal permitted development and make council checks more important.");
      addUnique(nextSteps, "Check whether the property is in a conservation area and whether extra restrictions apply to this project type.");
    }

    if (article4) {
      cautionScore += 2;
      addUnique(why, "Article 4 directions can remove normal permitted development rights for selected project types or areas.");
      addUnique(warnings, "Article 4 directions can remove normal permitted development rights, so do not rely on the national baseline alone.");
      addUnique(nextSteps, "Check the council's Article 4 map or designation record for the exact address.");
    }

    if (protectedLandscape) {
      cautionScore += 1;
      addUnique(why, "Protected landscapes can tighten design and siting expectations even when the project type is familiar.");
      addUnique(warnings, "National parks, AONBs and protected landscapes can make visual impact and siting more important.");
    }

    if (previousCondition) {
      cautionScore += 1;
      addUnique(why, "A previous planning condition can remove or limit a route that would otherwise look available.");
      addUnique(warnings, "Previous planning conditions can restrict later changes even where a generic rule sounds permissive.");
      addUnique(nextSteps, "Check past decision notices for conditions before relying on the route.");
    }

    if (notSureRestriction || answers.property_type === "not-sure") {
      cautionScore += 1;
      addUnique(why, "One or more property or restriction details are uncertain, so the result should be treated cautiously.");
      addUnique(nextSteps, "Confirm property type, local designations and planning history before work begins.");
    }

    if (helpWantsProfessional || answers.timeframe === "urgent-problem" || answers.timeframe === "already-started") {
      cautionScore += 1;
      addUnique(why, "Your timing or preferred help suggests the next step may need more than a broad rule check.");
      addUnique(nextSteps, "Consider a planning consultant, architectural designer or relevant specialist if the project is urgent, already started or needs drawings/application help.");
    }

    if (route === ROUTE_TYPES.pd && cautionScore >= 2) {
      route = ROUTE_TYPES.permission;
      confidence = "Medium";
    }

    if (cautionScore >= 4 && route !== ROUTE_TYPES.highways) {
      route = ROUTE_TYPES.professional;
      confidence = listed ? "High" : "Medium";
    } else if (confidence === "Medium" && cautionScore >= 2) {
      confidence = "Low";
    }

    addUnique(nextSteps, "Consider a lawful development certificate if you intend to rely on permitted development.");

    return {
      route: route,
      confidence: confidence,
      why: why,
      warnings: warnings,
      nextSteps: nextSteps
    };
  }

  function routeResultType(result) {
    const text = String(result.route || "").toLowerCase();
    if (text.indexOf("permitted development") !== -1) {
      return "permitted_development";
    }
    if (text.indexOf("highways") !== -1) {
      return "highways";
    }
    if (text.indexOf("professional") !== -1) {
      return "professional_review";
    }
    if (text.indexOf("planning") !== -1) {
      return "planning_permission";
    }
    return "more_information";
  }

  function renderResult(result, answers) {
    return [
      "<span class=\"eyebrow\">Your likely route</span>",
      "<div class=\"route-result-summary\">",
      "<div><h2>" + escapeHtml(result.route) + "</h2><p>This is a cautious first-pass route check, not a legal decision.</p></div>",
      "<div class=\"route-confidence\"><span>Confidence</span><strong>" + escapeHtml(result.confidence) + "</strong></div>",
      "</div>",
      "<div class=\"route-result-grid\">",
      "<div class=\"answer-card\"><h3>Why this matters</h3>" + listHtml(result.why) + "</div>",
      "<div class=\"answer-card route-warning-card\"><h3>Watch-outs</h3>" + listHtml(result.warnings) + "</div>",
      "<div class=\"answer-card\"><h3>Next steps</h3>" + listHtml(result.nextSteps) + "</div>",
      "</div>",
      "<p class=\"route-check-disclaimer\"><strong>Important:</strong> Planning results depend on the exact property, drawings, planning history and local restrictions. Check council guidance before work begins and use formal advice where the route is borderline.</p>",
      "<div class=\"tool-result-links\">",
      "<a class=\"tool-result-link\" href=\"/councils/\"><strong>Check your council</strong><span>Use local planning guidance and planning records before committing to work.</span></a>",
      "<a class=\"tool-result-link\" href=\"/planning-faq/lawful-development-certificate-vs-planning-permission/\"><strong>Certificate or permission?</strong><span>Understand when formal proof may be safer than relying on an assumption.</span></a>",
      "</div>",
      "<section class=\"tool-next-step\" data-project-folder-actions=\"true\">",
      "<div class=\"tool-next-step-copy\">Project folder</div>",
      "<h3>Keep This Result For Later</h3>",
      "<p>Save a local project folder on this device, copy a practical checklist, or print the result before you speak to your council, designer or contractor.</p>",
      "<div class=\"hero-ctas\">",
      "<button class=\"btn\" type=\"button\" data-route-action=\"save-folder\">Save project folder</button>",
      "<button class=\"btn button-secondary\" type=\"button\" data-route-action=\"copy-checklist\">Copy checklist</button>",
      "<button class=\"btn button-secondary\" type=\"button\" data-route-action=\"print-result\">Print result</button>",
      "</div>",
      "<p class=\"route-check-disclaimer\" data-project-folder-status=\"true\">Stored only in this browser. No account is created.</p>",
      "</section>",
      "<div class=\"route-result-data\" hidden data-route-result=\"" + escapeHtml(result.route) + "\" data-confidence=\"" + escapeHtml(result.confidence) + "\" data-project-type=\"" + escapeHtml(answers.project_type) + "\"></div>"
    ].join("");
  }

  function prefilledValue(form, name, fallback) {
    const field = form.elements[name];
    return field && field.value ? field.value : fallback || "";
  }

  function renderHelpPanel(answers, result) {
    const projectLabel = getLabel(PROJECT_LABELS, answers.project_type);
    const timeframe = getLabel(TIMEFRAME_LABELS, answers.timeframe);
    const council = answers.council || "";
    const summary = buildSummary(null, answers, result);
    return [
      "<span class=\"eyebrow\">Optional help request</span>",
      "<h2>Want help checking this properly?</h2>",
      "<p>UK Planning Guide is building a network of suitable planning, design and home-improvement professionals. If you ask for help, we may be able to contact you or pass your enquiry to a relevant professional, but a match is not guaranteed.</p>",
      "<form id=\"planning-help-form\" class=\"route-lead-form\" novalidate>",
      "<input type=\"text\" name=\"website\" class=\"route-honeypot\" tabindex=\"-1\" autocomplete=\"off\" aria-hidden=\"true\">",
      "<div class=\"form-grid\">",
      "<div class=\"form-field\"><label for=\"lead-name\">Full name *</label><input id=\"lead-name\" name=\"name\" type=\"text\" autocomplete=\"name\" required></div>",
      "<div class=\"form-field\"><label for=\"lead-email\">Email *</label><input id=\"lead-email\" name=\"email\" type=\"email\" autocomplete=\"email\" required></div>",
      "<div class=\"form-field\"><label for=\"lead-phone\">Phone <span class=\"field-help-inline\">optional but encouraged</span></label><input id=\"lead-phone\" name=\"phone\" type=\"tel\" autocomplete=\"tel\"></div>",
      "<div class=\"form-field\"><label for=\"lead-location\">Postcode/town *</label><input id=\"lead-location\" name=\"postcode_or_town\" type=\"text\" autocomplete=\"postal-code\" value=\"" + escapeHtml(answers.postcode_or_town) + "\" required></div>",
      "<div class=\"form-field\"><label for=\"lead-project\">Project type *</label><input id=\"lead-project\" name=\"project_type\" type=\"text\" value=\"" + escapeHtml(projectLabel) + "\" required></div>",
      "<div class=\"form-field\"><label for=\"lead-council\">Council/local authority</label><input id=\"lead-council\" name=\"council\" type=\"text\" value=\"" + escapeHtml(council) + "\"></div>",
      "<div class=\"form-field\"><label for=\"lead-timeframe\">Timeframe *</label><input id=\"lead-timeframe\" name=\"timeframe\" type=\"text\" value=\"" + escapeHtml(timeframe) + "\" required></div>",
      "<div class=\"form-field form-field-wide\"><label for=\"lead-notes\">Notes/project details *</label><textarea id=\"lead-notes\" name=\"notes\" rows=\"6\" required>" + escapeHtml(answers.user_notes || summary) + "</textarea></div>",
      "</div>",
      "<label class=\"route-consent\"><input type=\"checkbox\" name=\"consent_contact\" value=\"yes\" required><span>I agree that UK Planning Guide may contact me about this enquiry.</span></label>",
      "<label class=\"route-consent\"><input type=\"checkbox\" name=\"consent_share\" value=\"yes\" required><span>If suitable help is available, I agree that UK Planning Guide may share my enquiry details with a relevant planning, design or home-improvement professional for this purpose.</span></label>",
      "<div id=\"lead-form-errors\" class=\"route-check-errors\" role=\"alert\" aria-live=\"polite\"></div>",
      "<div class=\"hero-ctas\"><button class=\"btn\" type=\"submit\">Request planning help</button><button class=\"btn button-secondary\" type=\"button\" id=\"copy-route-summary\">Copy enquiry summary</button></div>",
      "</form>",
      "<section id=\"lead-fallback\" class=\"route-fallback\" hidden></section>",
      "<p class=\"route-check-disclaimer\">Contact details are only used for this enquiry. Do not include sensitive personal information that is not needed for the planning question.</p>"
    ].join("");
  }

  function getLeadData(form) {
    const data = new FormData(form);
    return {
      name: String(data.get("name") || "").trim(),
      email: String(data.get("email") || "").trim(),
      phone: String(data.get("phone") || "").trim(),
      postcode_or_town: String(data.get("postcode_or_town") || "").trim(),
      project_type: String(data.get("project_type") || "").trim(),
      council: String(data.get("council") || "").trim(),
      timeframe: String(data.get("timeframe") || "").trim(),
      notes: String(data.get("notes") || "").trim(),
      consent_contact: data.get("consent_contact") === "yes",
      consent_share: data.get("consent_share") === "yes",
      website: String(data.get("website") || "").trim()
    };
  }

  function buildPayload(lead, answers, result, formElapsedMs) {
    return {
      submitted_at: new Date().toISOString(),
      page_url: window.location.href,
      referrer: document.referrer || "",
      user_agent: navigator.userAgent || "",
      project_type: lead.project_type || getLabel(PROJECT_LABELS, answers.project_type),
      property_type: getLabel(PROPERTY_LABELS, answers.property_type),
      postcode_or_town: lead.postcode_or_town,
      council: lead.council || answers.council,
      restrictions: answers.restrictions.map(function (item) {
        return getLabel(RESTRICTION_LABELS, item);
      }),
      timeframe: lead.timeframe || getLabel(TIMEFRAME_LABELS, answers.timeframe),
      desired_help: getLabel(HELP_LABELS, answers.desired_help),
      route_result: result.route,
      confidence: result.confidence,
      user_notes: answers.user_notes,
      name: lead.name,
      email: lead.email,
      phone: lead.phone,
      consent_contact: lead.consent_contact,
      consent_share: lead.consent_share,
      website: lead.website || "",
      form_elapsed_ms: formElapsedMs || "",
      source: "planning_route_check"
    };
  }

  function cleanSummaryText(value, maxLength) {
    const clean = String(value || "").replace(/\r\n/g, "\n").replace(/\r/g, "\n").trim();
    if (!maxLength || clean.length <= maxLength) {
      return clean;
    }
    return clean.slice(0, maxLength).trim() + "\n[trimmed for email readability]";
  }

  function buildSummary(lead, answers, result) {
    const safeLead = lead || {};
    const notes = cleanSummaryText(safeLead.notes || answers.user_notes || "", 1800);
    return [
      "NEW UK PLANNING GUIDE ENQUIRY",
      "",
      "Project:",
      "Project: " + (safeLead.project_type || getLabel(PROJECT_LABELS, answers.project_type)),
      "Property type: " + getLabel(PROPERTY_LABELS, answers.property_type),
      "Location: " + (safeLead.postcode_or_town || answers.postcode_or_town),
      "Council: " + (safeLead.council || answers.council || "Not provided"),
      "Restrictions: " + (answers.restrictions.length ? answers.restrictions.map(function (item) { return getLabel(RESTRICTION_LABELS, item); }).join(", ") : "None selected"),
      "Timeframe: " + (safeLead.timeframe || getLabel(TIMEFRAME_LABELS, answers.timeframe)),
      "Desired help: " + getLabel(HELP_LABELS, answers.desired_help),
      "Likely route: " + result.route,
      "Confidence: " + result.confidence,
      "",
      "Customer:",
      "Name: " + (safeLead.name || ""),
      "Email: " + (safeLead.email || ""),
      "Phone: " + (safeLead.phone || ""),
      "",
      "Notes:",
      notes,
      "",
      "Consent:",
      "Contact consent: " + (safeLead.consent_contact ? "yes" : "no"),
      "Share consent: " + (safeLead.consent_share ? "yes" : "no"),
      "",
      "Source:",
      "Page URL: " + window.location.href,
      "Submitted at: " + new Date().toISOString()
    ].join("\n");
  }

  function buildProjectChecklist(answers, result) {
    const restrictions = answers.restrictions.length
      ? answers.restrictions.map(function (item) { return getLabel(RESTRICTION_LABELS, item); }).join(", ")
      : "None selected";
    return [
      "UK PLANNING GUIDE PROJECT CHECKLIST",
      "",
      "Project: " + getLabel(PROJECT_LABELS, answers.project_type),
      "Property type: " + getLabel(PROPERTY_LABELS, answers.property_type),
      "Location: " + answers.postcode_or_town,
      "Council: " + (answers.council || "Not provided"),
      "Restrictions: " + restrictions,
      "Likely route: " + result.route,
      "Confidence: " + result.confidence,
      "",
      "Next checks:",
      "- Check the relevant local council planning portal.",
      "- Gather photos, measured dimensions, boundary details and any planning history.",
      "- Check conservation area, Article 4, listed building and previous-condition records if relevant.",
      "- Consider a lawful development certificate if relying on permitted development.",
      "- Ask a qualified professional where the project is restricted, urgent, refused or enforcement-related.",
      "",
      "Questions to ask a designer or planning consultant:",
      "- Which rule or restriction is most likely to decide the route?",
      "- Would a lawful development certificate reduce risk?",
      "- What drawings or documents should be prepared first?",
      "- Should the council be contacted before an application is prepared?",
      "",
      "Saved from: " + window.location.href,
      "Saved at: " + new Date().toISOString()
    ].join("\n");
  }

  function saveProjectFolder(answers, result) {
    const payload = {
      saved_at: new Date().toISOString(),
      page_url: window.location.href,
      project_type: getLabel(PROJECT_LABELS, answers.project_type),
      property_type: getLabel(PROPERTY_LABELS, answers.property_type),
      postcode_or_town: answers.postcode_or_town,
      council: answers.council || "",
      restrictions: answers.restrictions.map(function (item) { return getLabel(RESTRICTION_LABELS, item); }),
      timeframe: getLabel(TIMEFRAME_LABELS, answers.timeframe),
      desired_help: getLabel(HELP_LABELS, answers.desired_help),
      route: result.route,
      confidence: result.confidence,
      next_steps: result.nextSteps,
      checklist: buildProjectChecklist(answers, result)
    };
    safeStorageSet("ukpg:planning-route-result", {
      route: payload.route,
      confidence: payload.confidence,
      project_type: payload.project_type,
      saved_at: payload.saved_at
    });
    safeStorageSet("ukpg:project-folder", payload);
    try {
      const workspaceKey = "ukpg:planning-workspace:v1";
      const existing = JSON.parse(window.localStorage.getItem(workspaceKey) || "{}") || {};
      const workspace = Object.assign({
        version: 1,
        saved_pages: [],
        completed_checks: [],
        tasks: [],
        result_summaries: [],
        constraints: []
      }, existing);
      workspace.project_type = payload.project_type;
      workspace.location_label = payload.council || payload.postcode_or_town || "";
      workspace.constraints = payload.restrictions || [];
      workspace.result_summaries = [{
        id: "planning-route-check|" + (window.location.pathname || "/"),
        tool_slug: "planning-route-check",
        result_label: payload.route,
        title: "Planning Route Check",
        path: window.location.pathname || "/tools/planning-route-check/",
        summary: payload.checklist,
        saved_at: payload.saved_at
      }].concat((workspace.result_summaries || []).filter(function (item) {
        return item && item.id !== "planning-route-check|" + (window.location.pathname || "/");
      })).slice(0, 12);
      workspace.tasks = (payload.next_steps || []).slice(0, 4).map(function (step, index) {
        return {
          id: "route-task|" + index + "|" + payload.saved_at,
          title: step,
          path: window.location.pathname || "/tools/planning-route-check/",
          tool_slug: "planning-route-check",
          completed: false,
          created_at: payload.saved_at
        };
      }).concat(workspace.tasks || []).slice(0, 30);
      workspace.updated_at = payload.saved_at;
      window.localStorage.setItem(workspaceKey, JSON.stringify(workspace));
    } catch (error) {}
    return payload;
  }

  function bindResultActions(panel, answers, result) {
    const actions = panel.querySelector("[data-project-folder-actions]");
    if (!actions) {
      return;
    }
    const status = actions.querySelector("[data-project-folder-status]");
    actions.addEventListener("click", function (event) {
      const button = event.target && event.target.closest ? event.target.closest("[data-route-action]") : null;
      if (!button) {
        return;
      }
      const action = button.getAttribute("data-route-action");
      if (action === "save-folder") {
        saveProjectFolder(answers, result);
        if (status) {
          status.textContent = "Project folder saved on this device.";
        }
        emitEvent("route_result_saved", {
          project_type: answers.project_type,
          result_type: routeResultType(result),
          confidence: result.confidence,
          source_page_type: "planning_route_check"
        });
      } else if (action === "copy-checklist") {
        copyText(buildProjectChecklist(answers, result)).then(function () {
          if (status) {
            status.textContent = "Checklist copied.";
          }
          emitEvent("project_checklist_copied", {
            project_type: answers.project_type,
            result_type: routeResultType(result),
            confidence: result.confidence,
            source_page_type: "planning_route_check"
          });
        });
      } else if (action === "print-result") {
        emitEvent("route_result_printed", {
          project_type: answers.project_type,
          result_type: routeResultType(result),
          confidence: result.confidence,
          source_page_type: "planning_route_check"
        });
        window.print();
      }
    });
  }

  function mailtoLink(summary, lead, answers) {
    const config = getLeadConfig();
    if (!config.owner_email) {
      return "";
    }
    const project = cleanSummaryText((lead && lead.project_type) || getLabel(PROJECT_LABELS, answers.project_type) || "Planning enquiry", 80);
    const location = cleanSummaryText((lead && lead.postcode_or_town) || answers.postcode_or_town || "Unknown location", 80);
    const subject = "UK Planning Guide enquiry - " + project + " - " + location;
    return "mailto:" + encodeURIComponent(config.owner_email) +
      "?subject=" + encodeURIComponent(subject) +
      "&body=" + encodeURIComponent(summary);
  }

  function copyText(text) {
    if (navigator.clipboard && navigator.clipboard.writeText) {
      return navigator.clipboard.writeText(text);
    }
    const textarea = document.createElement("textarea");
    textarea.value = text;
    textarea.setAttribute("readonly", "readonly");
    textarea.style.position = "fixed";
    textarea.style.left = "-9999px";
    document.body.appendChild(textarea);
    textarea.select();
    document.execCommand("copy");
    document.body.removeChild(textarea);
    return Promise.resolve();
  }

  function showFallback(container, summary, heading, lead, answers) {
    const emailHref = mailtoLink(summary, lead || {}, answers || {});
    const configuredCopy = emailHref
      ? "Online submission is not currently configured. You can copy the summary or open an email draft to send it."
      : "Online submission is not currently configured and no fallback email has been set. Copy the summary below and contact the site owner directly if needed.";
    container.hidden = false;
    container.innerHTML = [
      "<h3>" + escapeHtml(heading || "Online submission is not enabled yet") + "</h3>",
      "<p>" + escapeHtml(configuredCopy) + "</p>",
      "<textarea class=\"route-summary-box\" readonly aria-label=\"Enquiry summary\">" + escapeHtml(summary) + "</textarea>",
      "<div class=\"hero-ctas\">",
      "<button class=\"btn\" type=\"button\" data-copy-fallback=\"true\">Copy summary</button>",
      emailHref ? "<a class=\"btn button-secondary\" href=\"" + escapeHtml(emailHref) + "\">Open email draft</a>" : "",
      "</div>"
    ].join("");
    const copyButton = container.querySelector("[data-copy-fallback]");
    if (copyButton) {
      copyButton.addEventListener("click", function () {
        copyText(summary).then(function () {
          copyButton.textContent = "Summary copied";
          emitEvent("lead_form_fallback_used", { source_page_type: "planning_route_check" });
        });
      });
    }
  }

  function validateLead(lead, startedAt) {
    const errors = [];
    if (lead.website) {
      errors.push("Submission could not be accepted.");
    }
    if (Date.now() - startedAt < 2500) {
      errors.push("Please wait a moment before submitting the enquiry.");
    }
    if (!lead.name) {
      errors.push("Enter your full name.");
    }
    if (!lead.email || lead.email.indexOf("@") === -1) {
      errors.push("Enter a valid email address.");
    }
    if (!lead.postcode_or_town) {
      errors.push("Enter the postcode or town.");
    }
    if (!lead.notes) {
      errors.push("Add a short project note.");
    }
    if (!lead.consent_contact) {
      errors.push("Confirm that UK Planning Guide may contact you about this enquiry.");
    }
    if (!lead.consent_share) {
      errors.push("Confirm whether your enquiry may be shared with a relevant professional if suitable help is available.");
    }
    return errors;
  }

  function bindHelpForm(panel, answers, result) {
    const form = panel.querySelector("#planning-help-form");
    const errors = panel.querySelector("#lead-form-errors");
    const fallback = panel.querySelector("#lead-fallback");
    const copyButton = panel.querySelector("#copy-route-summary");
    const startedAt = Date.now();

    if (copyButton) {
      copyButton.addEventListener("click", function () {
        const lead = form ? getLeadData(form) : null;
        copyText(buildSummary(lead, answers, result)).then(function () {
          copyButton.textContent = "Summary copied";
          emitEvent("lead_form_fallback_used", { source_page_type: "planning_route_check" });
        });
      });
    }

    if (!form) {
      return;
    }

    emitEvent("lead_form_opened", {
      project_type: answers.project_type,
      result_type: routeResultType(result),
      confidence: result.confidence,
      source_page_type: "planning_route_check"
    });

    form.addEventListener("submit", function (event) {
      event.preventDefault();
      const lead = getLeadData(form);
      const validationErrors = validateLead(lead, startedAt);
      if (validationErrors.length) {
        errors.innerHTML = listHtml(validationErrors);
        emitEvent("lead_form_failed", {
          project_type: answers.project_type,
          result_type: routeResultType(result),
          confidence: result.confidence,
          source_page_type: "planning_route_check"
        });
        return;
      }

      errors.textContent = "";
      const payload = buildPayload(lead, answers, result, Date.now() - startedAt);
      const summary = buildSummary(lead, answers, result);
      const config = getLeadConfig();
      const endpoint = String(config.endpoint || "").trim();

      if (!config.enabled || !endpoint) {
        showFallback(fallback, summary, "Online submission is not yet enabled", lead, answers);
        emitEvent("lead_form_fallback_used", {
          project_type: answers.project_type,
          result_type: routeResultType(result),
          confidence: result.confidence,
          source_page_type: "planning_route_check"
        });
        return;
      }

      const controller = typeof AbortController === "function" ? new AbortController() : null;
      const timeoutMs = Math.max(1000, Number(config.request_timeout_ms || 10000));
      const timeoutId = controller ? window.setTimeout(function () {
        controller.abort();
      }, timeoutMs) : null;

      fetch(endpoint, {
        method: config.method || "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
        credentials: "omit",
        signal: controller ? controller.signal : undefined
      }).then(function (response) {
        if (timeoutId) {
          window.clearTimeout(timeoutId);
        }
        return response.json().catch(function () {
          return {};
        }).then(function (body) {
          if (!response.ok || body.ok === false) {
            throw new Error(body.message || "Lead endpoint returned " + response.status);
          }
          return body;
        });
      }).then(function () {
        emitEvent("lead_form_submitted", {
          project_type: answers.project_type,
          result_type: routeResultType(result),
          confidence: result.confidence,
          source_page_type: "planning_route_check"
        });
        window.location.assign(config.success_redirect || "/planning-help/thank-you/");
      }).catch(function (error) {
        if (timeoutId) {
          window.clearTimeout(timeoutId);
        }
        if (config.debug && window.console && typeof window.console.warn === "function") {
          window.console.warn("Planning help submission failed", error && error.message ? error.message : error);
        }
        showFallback(fallback, summary, error && error.name === "AbortError" ? "Online submission timed out" : "Online submission failed", lead, answers);
        emitEvent("lead_form_failed", {
          project_type: answers.project_type,
          result_type: routeResultType(result),
          confidence: result.confidence,
          source_page_type: "planning_route_check"
        });
      });
    });
  }

  function bindRouteCheck() {
    const form = document.getElementById("planning-route-check-form");
    const resultPanel = document.getElementById("planning-route-result");
    const helpPanel = document.getElementById("planning-route-help");
    const errors = document.getElementById("route-check-errors");
    const root = document.querySelector("[data-tool-root=\"planning-route-check\"]");
    if (!form || !resultPanel || !helpPanel || !root) {
      return;
    }

    let hasStarted = false;

    form.addEventListener("change", function () {
      if (hasStarted) {
        return;
      }
      hasStarted = true;
      emitEvent("route_check_started", { source_page_type: "planning_route_check" });
    });

    form.addEventListener("reset", function () {
      resultPanel.hidden = true;
      resultPanel.innerHTML = "";
      helpPanel.hidden = true;
      helpPanel.innerHTML = "";
      errors.textContent = "";
    });

    form.addEventListener("submit", function (event) {
      event.preventDefault();
      if (typeof form.reportValidity === "function" && !form.reportValidity()) {
        errors.textContent = "Please answer the required questions before showing your likely route.";
        return;
      }

      const answers = getAnswers(form);
      if (!answers.project_type || !answers.property_type || !answers.postcode_or_town || !answers.timeframe || !answers.desired_help) {
        errors.textContent = "Please answer the required questions before showing your likely route.";
        return;
      }

      errors.textContent = "";
      const result = evaluateRoute(answers);
      resultPanel.hidden = false;
      resultPanel.innerHTML = renderResult(result, answers);
      saveProjectFolder(answers, result);
      bindResultActions(resultPanel, answers, result);
      helpPanel.hidden = false;
      helpPanel.innerHTML = renderHelpPanel(answers, result);
      bindHelpForm(helpPanel, answers, result);

      emitEvent("route_check_completed", {
        project_type: answers.project_type,
        result_type: routeResultType(result),
        confidence: result.confidence,
        source_page_type: "planning_route_check"
      });
      emitEvent("route_check_result_shown", {
        project_type: answers.project_type,
        result_type: routeResultType(result),
        confidence: result.confidence,
        source_page_type: "planning_route_check"
      });

      resultPanel.scrollIntoView({ behavior: "smooth", block: "start" });
    });
  }

  function bindRouteCtas() {
    document.querySelectorAll("[data-planning-route-cta-link]").forEach(function (link) {
      link.addEventListener("click", function () {
        const cta = link.closest("[data-planning-route-cta]");
        emitEvent("planning_help_cta_clicked", {
          source_page_type: cta ? cta.getAttribute("data-source-page-type") || "" : "",
          project_type: cta ? cta.getAttribute("data-project-slug") || "" : "",
          result_type: "",
          confidence: ""
        });
      });
    });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", function () {
      bindRouteCheck();
      bindRouteCtas();
    });
  } else {
    bindRouteCheck();
    bindRouteCtas();
  }
})();
