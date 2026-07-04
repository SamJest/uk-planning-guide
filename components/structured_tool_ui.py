STRUCTURED_TOOL_UI_HELPERS = """
  const MOBILE_LAYOUT_BREAKPOINT = 767;
  const compactLayoutQuery = window.matchMedia("(max-width: " + MOBILE_LAYOUT_BREAKPOINT + "px)");
  let compactLayout = compactLayoutQuery.matches;

  function isCompactLayout() {
    return compactLayout;
  }

  function syncCompactLayout(event) {
    const next = event && typeof event.matches === "boolean"
      ? event.matches
      : compactLayoutQuery.matches;
    if (next !== compactLayout) {
      compactLayout = next;
      render();
    }
  }

  if (typeof compactLayoutQuery.addEventListener === "function") {
    compactLayoutQuery.addEventListener("change", syncCompactLayout);
  } else if (typeof compactLayoutQuery.addListener === "function") {
    compactLayoutQuery.addListener(syncCompactLayout);
  }

  function renderProgressLabels(stepNames, currentStep, hasResult) {
    return stepNames.map((name, index) => {
      const stepNumber = index + 1;
      const classes = [
        "decision-step-label",
        hasResult ? "done" : "",
        currentStep === stepNumber && !hasResult ? "active" : "",
        stepNumber < currentStep || (stepNumber <= stepNames.length && hasResult) ? "done" : "",
      ].filter(Boolean).join(" ");
      return "<div class='" + classes + "'><span class='decision-step-number'>Step " + stepNumber + "</span><span class='decision-step-name'>" + escapeHtml(name) + "</span></div>";
    }).join("");
  }

  function renderMobileStepChips(stepNames, currentStep, hasResult) {
    return stepNames.map((name, index) => {
      const stepNumber = index + 1;
      const classes = [
        "decision-mobile-chip",
        hasResult ? "done" : "",
        currentStep === stepNumber && !hasResult ? "active" : "",
        stepNumber < currentStep || hasResult ? "done" : "",
      ].filter(Boolean).join(" ");
      return "<span class='" + classes + "' aria-label='" + escapeHtml("Step " + stepNumber + ": " + name) + "'>" + stepNumber + "</span>";
    }).join("");
  }

  function renderTrustNote() {
    return "<div class='decision-trust-note'><strong>UK planning baseline</strong><span>Based on common UK planning and permitted development rules. Always confirm with your local council if the project is close to a limit or affected by local controls.</span></div>";
  }

  const SHARED_FOLLOW_ON_TOOLS = [
    { slug: "planning-decision-tool", title: "Planning checker", href: "/tools/planning-decision-tool/", description: "Run the full rule-based planning check for a clearer route answer." },
    { slug: "permitted-development-calculator", title: "Size calculator", href: "/tools/permitted-development-calculator/", description: "Use the fast dimensions-first calculator for a simpler first pass." },
    { slug: "planning-route-planner", title: "Route planner", href: "/tools/planning-route-planner/", description: "Compare the likely planning paths when the answer still feels mixed." }
  ];
  const RULE_LINK_PREFIXES = [
    "/planning-permission/",
    "/permitted-development/",
    "/height-limits/",
    "/boundary-rules/",
    "/conservation-areas/",
    "/maximum-height/",
    "/distance-from-boundary/",
    "/roof-alterations/",
    "/article-4/",
    "/listed-buildings/",
    "/depth-limits/"
  ];

  function ensureLink(target, item) {
    if (item && item.href && !target.some((link) => link.href === item.href)) {
      target.push(item);
    }
  }

  function classifyPrimaryLink(item) {
    const href = item && item.href ? String(item.href) : "";
    if (!href) {
      return "other";
    }
    if (href.indexOf("/planning-faq/") === 0) {
      return "faq";
    }
    if (href.indexOf("/councils/") === 0 || href === "/councils/") {
      return "authority";
    }
    if (href.indexOf("/tools/") === 0) {
      return "tool";
    }
    if (RULE_LINK_PREFIXES.some((prefix) => href.indexOf(prefix) === 0)) {
      return "rule";
    }
    if (href.indexOf("/") === 0) {
      return "project";
    }
    return "other";
  }

  function firstLinkByCategory(links, category) {
    return (links || []).find((item) => classifyPrimaryLink(item) === category) || null;
  }

  function buildCoreNextLinks(options) {
    const curated = [];
    const links = options.links || [];

    ensureLink(curated, options.projectLink || firstLinkByCategory(links, "project"));
    ensureLink(curated, options.ruleLink || firstLinkByCategory(links, "rule"));
    ensureLink(curated, options.faqLink || firstLinkByCategory(links, "faq"));
    ensureLink(
      curated,
      options.authorityLink || firstLinkByCategory(links, "authority") || {
        title: "Local Authorities",
        href: "/councils/",
        description: "Compare the local authority layer before relying on the answer.",
      }
    );

    return curated.filter(Boolean);
  }

  function defaultNextTool(currentSlug) {
    const fallback = currentSlug === "what-can-i-build-explorer"
      ? { href: "/tools/planning-decision-tool/", title: "Use another tool", description: "Move from project ideas into the full planning checker." }
      : { href: "/tools/what-can-i-build-explorer/", title: "Use another tool", description: "Open the project explorer to compare other directions for the site." };
    return fallback;
  }

  function renderPostResultExtras(options) {
    const currentSlug = options.toolSlug || "";
    const resultLabel = options.resultLabel || "Result saved";
    const nextTool = options.nextTool || defaultNextTool(currentSlug);
    const guideHref = options.guideHref || "/planning-permission/";
    const guideTitle = options.guideTitle || "Planning permission guide";
    const nextSteps = [
      { title: "View full guide", href: guideHref, description: "Open the longer guide behind this result." },
      { title: "Check rules in your area", href: "/councils/", description: "Compare the local authority layer before relying on the answer." },
      nextTool
    ];
    const relatedTools = SHARED_FOLLOW_ON_TOOLS.filter((item) => item.slug !== currentSlug).slice(0, 3);
    return "<section class='decision-follow-up'><div class='decision-follow-up-card'><div class='decision-follow-up-heading'><span class='decision-follow-up-kicker'>Next steps</span><h3>Keep moving while the result is fresh</h3><p>Use the next best action below to confirm the answer, localise it, or move into a deeper tool.</p></div><div class='decision-follow-up-grid'>" + nextSteps.map((item) => "<a class='decision-follow-up-link' href='" + escapeHtml(item.href) + "'><strong>" + escapeHtml(item.title) + "</strong><span>" + escapeHtml(item.description || "Open the next planning step.") + "</span></a>").join("") + "</div></div><div class='decision-follow-up-card'><div class='decision-follow-up-heading'><span class='decision-follow-up-kicker'>Related tools</span><h3>Continue with another planning check</h3><p>These follow-on tools help you pressure-test the same project from a different angle without starting your research from scratch.</p></div><div class='decision-follow-up-grid'>" + relatedTools.map((item) => "<a class='decision-follow-up-link' href='" + escapeHtml(item.href) + "'><strong>" + escapeHtml(item.title) + "</strong><span>" + escapeHtml(item.description) + "</span></a>").join("") + "</div></div><div class='decision-follow-up-card'><div class='decision-follow-up-heading'><span class='decision-follow-up-kicker'>My Planning Project</span><h3>Save, check off or share this result</h3><p>Keep this result in the local project workspace, mark the check complete, add a follow-up task, print it or copy a short summary.</p></div><div class='decision-email-capture' data-tool-email-capture='" + escapeHtml(currentSlug) + "' data-result-label='" + escapeHtml(resultLabel) + "'><button type='button' class='cta decision-email-button' data-workspace-action='save-tool'>Save to My Planning Project</button><button type='button' class='button-secondary decision-email-button' data-workspace-action='mark-tool-checked'>Mark as checked</button><button type='button' class='button-secondary decision-email-button' data-workspace-action='add-tool-task'>Add next task</button><button type='button' class='button-secondary decision-email-button' data-workspace-action='copy-tool-summary'>Copy summary</button><button type='button' class='button-secondary decision-email-button' onclick='window.print()'>Print pack</button><p class='decision-email-note'>Stored only on this device. No account is created and nothing is sent unless you submit a form.</p></div></div><div class='decision-inline-note'>This is a guide based on UK planning rules. Always confirm with your local council.</div></section>";
  }

  window.__ukpgSaveToolEmail = function (button) {
    try {
      const wrapper = button && button.closest("[data-tool-email-capture]");
      if (!wrapper) {
        return;
      }
      const note = wrapper.querySelector(".decision-email-note");
      const payload = {
        resultLabel: wrapper.getAttribute("data-result-label") || "Planning tool result",
        savedAt: new Date().toISOString()
      };
      window.localStorage.setItem("ukpg-tool-email:" + (wrapper.getAttribute("data-tool-email-capture") || "tool"), JSON.stringify(payload));
      if (note) {
        note.textContent = "Saved on this device. Bookmark or print the page as well if you want an easy reference outside this browser.";
      }
    } catch (error) {
      const wrapper = button && button.closest("[data-tool-email-capture]");
      const note = wrapper ? wrapper.querySelector(".decision-email-note") : null;
      if (note) {
        note.textContent = "This browser blocked local storage, so use a bookmark, copied link or printed page instead.";
      }
    }
  };

  function renderProgressIntro(options, currentName) {
    const title = options.hasResult ? "Result ready" : ("Step " + options.currentStep + " of " + options.stepNames.length);
    const detail = options.hasResult
      ? "You have a structured outcome with follow-on checks and next pages."
      : ("Current focus: " + currentName + ". Complete each step to unlock the full result.");
    return "<div class='decision-progress-top'><strong>" + escapeHtml(title) + "</strong><span>" + escapeHtml(detail) + "</span></div>";
  }

  function renderDesktopToolShell(options) {
    const currentName = options.hasResult ? "Result" : (options.stepNames[options.currentStep - 1] || "Review");
    return "<div class='decision-desktop-shell'><div class='decision-engine-header'><div><span class='decision-kicker'>" + escapeHtml(options.kicker) + "</span><h2>" + escapeHtml(options.heading) + "</h2><p class='tool-summary'>" + escapeHtml(options.intro) + "</p>" + renderTrustNote() + "</div><div class='decision-header-actions'>" + options.actionsHtml + "</div></div><div class='decision-progress'>" + renderProgressIntro(options, currentName) + "<div class='decision-progress-bar'><span style='width:" + options.progress + "%'></span></div><div class='decision-step-labels'>" + renderProgressLabels(options.stepNames, options.currentStep, options.hasResult) + "</div></div><div class='decision-layout'><div class='decision-panel'>" + options.contentHtml + "</div>" + options.sidebarHtml + "</div></div>";
  }

  function renderMobileToolShell(options) {
    const currentName = options.hasResult ? "Result" : (options.stepNames[options.currentStep - 1] || "Review");
    const introLabel = options.hasResult ? "Result ready" : ("Step " + options.currentStep + " of " + options.stepNames.length);
    const introCopy = options.hasResult
      ? "Your structured result and follow-on guidance are ready below."
      : ("Current focus: " + currentName + ". Complete each step to unlock the full result.");
    const summaryBlock = "<div class='decision-mobile-calculator-summary'><h3>" + escapeHtml(options.summaryTitle || "Your answers") + "</h3><div class='decision-summary-list'>" + options.summaryHtml + "</div>" + (options.noteHtml ? "<div class='decision-method-note'>" + options.noteHtml + "</div>" : "") + "</div>";
    return "<div class='decision-mobile-calculator-shell'><div class='decision-mobile-calculator-header'><div><span class='decision-kicker'>" + escapeHtml(options.kicker) + "</span><h2>" + escapeHtml(options.heading) + "</h2><p class='tool-summary'>" + escapeHtml(options.intro) + "</p>" + renderTrustNote() + "</div><div class='decision-mobile-calculator-actions'>" + options.actionsHtml + "</div></div><div class='decision-mobile-calculator-body'><div class='decision-mobile-calculator-panel'><div class='decision-mobile-calculator-step-intro'><strong>" + escapeHtml(introLabel) + "</strong><p>" + escapeHtml(introCopy) + "</p><div class='decision-progress-bar'><span style='width:" + options.progress + "%'></span></div><div class='decision-step-labels'>" + renderProgressLabels(options.stepNames, options.currentStep, options.hasResult) + "</div></div>" + options.contentHtml + "</div>" + summaryBlock + "</div></div>";
  }

  function renderResponsiveToolShellInto(target, options) {
    if (!target) {
      return;
    }
    const markup = "<div class='decision-shell decision-shell-desktop' data-tool-shell='desktop'>" + renderDesktopToolShell(options) + "</div><div class='decision-shell decision-shell-mobile' data-tool-shell='mobile'>" + renderMobileToolShell(options) + "</div>";
    target.innerHTML = markup;
    if (typeof target.setAttribute === "function") {
      target.setAttribute("data-tool-layout", isCompactLayout() ? "mobile" : "desktop");
    }
  }
"""
