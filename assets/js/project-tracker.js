(function () {
  if (typeof window === "undefined" || typeof document === "undefined") {
    return;
  }

  const STORAGE_KEY = "ukpg:my-planning-project";
  const WORKSPACE_KEY = "ukpg:planning-workspace:v1";
  const VERSION = 1;

  function track(eventName, params) {
    const payload = Object.assign({}, params || {});
    if (typeof window.gtag === "function") {
      window.gtag("event", eventName, payload);
    }
  }

  window.upgTrack = window.upgTrack || track;

  function readState() {
    try {
      const raw = window.localStorage.getItem(STORAGE_KEY);
      if (!raw) {
        return { version: VERSION, pages: [], updated_at: "" };
      }
      const parsed = JSON.parse(raw);
      if (!parsed || !Array.isArray(parsed.pages)) {
        return { version: VERSION, pages: [], updated_at: "" };
      }
      parsed.version = VERSION;
      return parsed;
    } catch (error) {
      return { version: VERSION, pages: [], updated_at: "", storage_blocked: true };
    }
  }

  function emptyWorkspace() {
    return {
      version: VERSION,
      project_type: "",
      location_label: "",
      constraints: [],
      saved_pages: [],
      completed_checks: [],
      tasks: [],
      result_summaries: [],
      updated_at: ""
    };
  }

  function readWorkspace() {
    try {
      const raw = window.localStorage.getItem(WORKSPACE_KEY);
      if (!raw) {
        const legacy = readState();
        const workspace = emptyWorkspace();
        workspace.saved_pages = (legacy.pages || []).slice(0, 12);
        return workspace;
      }
      const parsed = JSON.parse(raw);
      const workspace = Object.assign(emptyWorkspace(), parsed || {});
      workspace.saved_pages = Array.isArray(workspace.saved_pages) ? workspace.saved_pages : [];
      workspace.completed_checks = Array.isArray(workspace.completed_checks) ? workspace.completed_checks : [];
      workspace.tasks = Array.isArray(workspace.tasks) ? workspace.tasks : [];
      workspace.result_summaries = Array.isArray(workspace.result_summaries) ? workspace.result_summaries : [];
      workspace.constraints = Array.isArray(workspace.constraints) ? workspace.constraints : [];
      workspace.version = VERSION;
      return workspace;
    } catch (error) {
      const blocked = emptyWorkspace();
      blocked.storage_blocked = true;
      return blocked;
    }
  }

  function writeWorkspace(workspace) {
    try {
      const clean = Object.assign(emptyWorkspace(), workspace || {}, {
        version: VERSION,
        updated_at: new Date().toISOString()
      });
      window.localStorage.setItem(WORKSPACE_KEY, JSON.stringify(clean));
      return true;
    } catch (error) {
      return false;
    }
  }

  function updateWorkspace(mutator) {
    const workspace = readWorkspace();
    if (workspace.storage_blocked) {
      return false;
    }
    mutator(workspace);
    return writeWorkspace(workspace);
  }

  function writeState(state) {
    try {
      const clean = Object.assign({}, state, {
        version: VERSION,
        updated_at: new Date().toISOString(),
      });
      window.localStorage.setItem(STORAGE_KEY, JSON.stringify(clean));
      return true;
    } catch (error) {
      return false;
    }
  }

  function savePageToWorkspace(snapshot) {
    return updateWorkspace(function (workspace) {
      const existing = workspace.saved_pages.filter(function (item) {
        return item && item.path !== snapshot.path;
      });
      workspace.saved_pages = [snapshot].concat(existing).slice(0, 16);
    });
  }

  function toolSnapshot(button) {
    const wrapper = button && button.closest ? button.closest("[data-tool-email-capture]") : null;
    const resultRoot = button && button.closest ? button.closest(".decision-result, .tool-result, .decision-follow-up") : null;
    const page = pageSnapshot();
    const toolSlug = wrapper ? wrapper.getAttribute("data-tool-email-capture") || "" : "";
    const label = wrapper ? wrapper.getAttribute("data-result-label") || "Planning tool result" : "Planning tool result";
    return {
      id: [toolSlug || "tool", page.path, label].join("|"),
      tool_slug: toolSlug,
      result_label: label,
      title: page.title,
      path: page.path,
      summary: resultRoot ? (resultRoot.textContent || "").replace(/\s+/g, " ").trim().slice(0, 320) : page.description,
      saved_at: new Date().toISOString()
    };
  }

  function pageSnapshot() {
    const h1 = document.querySelector("h1");
    const title = (h1 && h1.textContent ? h1.textContent : document.title || "Planning guide").trim();
    const meta = document.querySelector("meta[name='description']");
    return {
      title: title.slice(0, 120),
      path: window.location.pathname || "/",
      description: meta ? (meta.getAttribute("content") || "").slice(0, 180) : "",
      saved_at: new Date().toISOString(),
    };
  }

  function saveCurrentPage(button) {
    const state = readState();
    if (state.storage_blocked) {
      setNote(button, "This browser blocked local storage, so print or copy the summary instead.");
      window.upgTrack("project_save_failed", { reason: "storage_blocked", source_page: window.location.pathname });
      return;
    }

    const snapshot = pageSnapshot();
    const existing = state.pages.filter(function (item) {
      return item && item.path !== snapshot.path;
    });
    state.pages = [snapshot].concat(existing).slice(0, 12);
    const ok = writeState(state);
    savePageToWorkspace(snapshot);
    setNote(button, ok ? "Saved on this device." : "This browser blocked local storage, so print or copy the summary instead.");
    if (ok) {
      window.upgTrack("project_save", {
        source_page: snapshot.path,
        page_count: state.pages.length,
      });
      renderPanel();
    }
  }

  function clearProject() {
    try {
      window.localStorage.removeItem(STORAGE_KEY);
    } catch (error) {}
    window.upgTrack("project_clear", { source_page: window.location.pathname });
    try {
      window.localStorage.removeItem(WORKSPACE_KEY);
    } catch (error) {}
    renderPanel();
    renderWorkspacePage();
  }

  function buildSummaryText() {
    const state = readState();
    const workspace = readWorkspace();
    const current = pageSnapshot();
    const pages = (workspace.saved_pages && workspace.saved_pages.length ? workspace.saved_pages : (state.pages && state.pages.length ? state.pages : [current])).slice(0, 8);
    const tasks = (workspace.tasks || []).filter(function (item) { return !item.completed; }).slice(0, 6);
    const checks = (workspace.completed_checks || []).slice(0, 6);
    const lines = [
      "UK Planning Guide project pack",
      "",
      "Current page: " + current.title,
      "URL: " + window.location.href,
      "",
      "Saved pages:",
    ];
    pages.forEach(function (item, index) {
      lines.push((index + 1) + ". " + (item.title || "Planning guide") + " - " + (item.path || "/"));
    });
    if (tasks.length) {
      lines.push("", "Open tasks:");
      tasks.forEach(function (item, index) {
        lines.push((index + 1) + ". " + (item.title || item.text || "Planning task"));
      });
    }
    if (checks.length) {
      lines.push("", "Completed checks:");
      checks.forEach(function (item, index) {
        lines.push((index + 1) + ". " + (item.result_label || item.title || "Planning check"));
      });
    }
    return lines.join("\n");
  }

  function copySummary(button) {
    const text = buildSummaryText();
    if (navigator.clipboard && typeof navigator.clipboard.writeText === "function") {
      navigator.clipboard.writeText(text).then(function () {
        setNote(button, "Summary copied.");
        window.upgTrack("project_copy_summary", { source_page: window.location.pathname });
      }).catch(function () {
        fallbackCopy(text, button);
      });
      return;
    }
    fallbackCopy(text, button);
  }

  function fallbackCopy(text, button) {
    const textarea = document.createElement("textarea");
    textarea.value = text;
    textarea.setAttribute("readonly", "readonly");
    textarea.style.position = "fixed";
    textarea.style.left = "-9999px";
    document.body.appendChild(textarea);
    textarea.select();
    try {
      document.execCommand("copy");
      setNote(button, "Summary copied.");
      window.upgTrack("project_copy_summary", { source_page: window.location.pathname });
    } catch (error) {
      setNote(button, "Copy was blocked. You can still print the pack.");
    }
    textarea.remove();
  }

  function printPack() {
    window.upgTrack("project_print_pack", { source_page: window.location.pathname });
    window.print();
  }

  function setNote(button, message) {
    const scope = button && button.closest ? button.closest("section, .project-tracker-panel, .result-capture") : null;
    const note = scope ? scope.querySelector("[data-project-note], .result-capture-note, .project-tracker-note") : null;
    if (note) {
      note.textContent = message;
    }
  }

  function escapeHtml(value) {
    return String(value || "")
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;")
      .replace(/'/g, "&#39;");
  }

  function renderPanel() {
    let panel = document.getElementById("ukpg-project-tracker-panel");
    const state = readState();
    const workspace = readWorkspace();
    const pages = (workspace.saved_pages && workspace.saved_pages.length ? workspace.saved_pages : state.pages) || [];
    const openTasks = (workspace.tasks || []).filter(function (item) {
      return !item.completed;
    });
    const completedChecks = workspace.completed_checks || [];

    if (!pages.length && !openTasks.length && !completedChecks.length) {
      if (panel) {
        panel.remove();
      }
      return;
    }

    if (!panel) {
      panel = document.createElement("aside");
      panel.id = "ukpg-project-tracker-panel";
      panel.className = "project-tracker-panel";
      document.body.appendChild(panel);
    }

    const pageList = pages.slice(0, 4).map(function (item) {
      return "<a href='" + escapeHtml(item.path) + "'>" + escapeHtml(item.title) + "</a>";
    }).join("");

    panel.innerHTML = "<div><span>My Planning Project</span><strong>" + pages.length + " saved page" + (pages.length === 1 ? "" : "s") + (openTasks.length ? " · " + openTasks.length + " open task" + (openTasks.length === 1 ? "" : "s") : "") + "</strong></div><nav>" + pageList + "</nav><div class='project-tracker-actions'><a href='/my-planning-project/'>Open workspace</a><button type='button' data-project-action='save-page'>Save page</button><button type='button' data-project-action='print-pack'>Print</button><button type='button' data-project-action='copy-summary'>Copy</button><button type='button' data-project-action='clear-project'>Clear</button></div><p class='project-tracker-note'>Stored only in this browser.</p>";
  }

  function setWorkspaceNote(button, message) {
    const wrapper = button && button.closest ? button.closest("[data-tool-email-capture], [data-workspace-page]") : null;
    const note = wrapper ? wrapper.querySelector(".decision-email-note, [data-workspace-note]") : null;
    if (note) {
      note.textContent = message;
    }
  }

  function saveToolResult(button) {
    const snapshot = toolSnapshot(button);
    const ok = updateWorkspace(function (workspace) {
      workspace.result_summaries = [snapshot].concat((workspace.result_summaries || []).filter(function (item) {
        return item && item.id !== snapshot.id;
      })).slice(0, 12);
      workspace.saved_pages = [pageSnapshot()].concat((workspace.saved_pages || []).filter(function (item) {
        return item && item.path !== snapshot.path;
      })).slice(0, 16);
    });
    setWorkspaceNote(button, ok ? "Saved to My Planning Project on this device." : "This browser blocked local storage, so print or copy the result instead.");
    if (ok) {
      window.upgTrack("workspace_result_saved", { tool_slug: snapshot.tool_slug, result_label: snapshot.result_label, source_page: snapshot.path });
      renderPanel();
      renderWorkspacePage();
    }
  }

  function markToolChecked(button) {
    const snapshot = toolSnapshot(button);
    const ok = updateWorkspace(function (workspace) {
      workspace.completed_checks = [snapshot].concat((workspace.completed_checks || []).filter(function (item) {
        return item && item.id !== snapshot.id;
      })).slice(0, 20);
      workspace.tasks = (workspace.tasks || []).map(function (task) {
        if (task.tool_slug && task.tool_slug === snapshot.tool_slug) {
          return Object.assign({}, task, { completed: true, completed_at: new Date().toISOString() });
        }
        return task;
      });
    });
    setWorkspaceNote(button, ok ? "Marked as checked in My Planning Project." : "This browser blocked local storage.");
    if (ok) {
      window.upgTrack("workspace_task_completed", { tool_slug: snapshot.tool_slug, source_page: snapshot.path });
      renderPanel();
      renderWorkspacePage();
    }
  }

  function addToolTask(button) {
    const snapshot = toolSnapshot(button);
    const task = {
      id: "task|" + snapshot.id + "|" + Date.now(),
      title: "Follow up: " + (snapshot.result_label || snapshot.title || "planning result"),
      path: snapshot.path,
      tool_slug: snapshot.tool_slug,
      completed: false,
      created_at: new Date().toISOString()
    };
    const ok = updateWorkspace(function (workspace) {
      workspace.tasks = [task].concat(workspace.tasks || []).slice(0, 30);
    });
    setWorkspaceNote(button, ok ? "Next task added to My Planning Project." : "This browser blocked local storage.");
    if (ok) {
      window.upgTrack("workspace_task_added", { tool_slug: snapshot.tool_slug, source_page: snapshot.path });
      renderPanel();
      renderWorkspacePage();
    }
  }

  function copyToolSummary(button) {
    const snapshot = toolSnapshot(button);
    const text = [
      "UK Planning Guide result",
      "",
      "Page: " + snapshot.title,
      "Result: " + snapshot.result_label,
      "URL: " + window.location.href,
      "",
      snapshot.summary
    ].join("\n");
    copyPlainText(text).then(function () {
      setWorkspaceNote(button, "Result summary copied.");
      window.upgTrack("workspace_summary_copied", { tool_slug: snapshot.tool_slug, source_page: snapshot.path });
    });
  }

  function copyPlainText(text) {
    if (navigator.clipboard && typeof navigator.clipboard.writeText === "function") {
      return navigator.clipboard.writeText(text);
    }
    const textarea = document.createElement("textarea");
    textarea.value = text;
    textarea.setAttribute("readonly", "readonly");
    textarea.style.position = "fixed";
    textarea.style.left = "-9999px";
    document.body.appendChild(textarea);
    textarea.select();
    try {
      document.execCommand("copy");
    } catch (error) {}
    textarea.remove();
    return Promise.resolve();
  }

  function renderWorkspacePage() {
    const root = document.querySelector("[data-workspace-page]");
    if (!root) {
      return;
    }
    const workspace = readWorkspace();
    const savedPages = workspace.saved_pages || [];
    const tasks = workspace.tasks || [];
    const openTasks = tasks.filter(function (task) { return !task.completed; });
    const checks = workspace.completed_checks || [];
    const results = workspace.result_summaries || [];

    function card(title, body, href, extra) {
      const link = href ? " href='" + escapeHtml(href) + "'" : "";
      return "<a class='card' " + link + "><div class='card-kicker'>" + escapeHtml(extra || "Workspace item") + "</div><h3>" + escapeHtml(title) + "</h3><p>" + escapeHtml(body || "Saved in this browser.") + "</p><span class='cta'>Open</span></a>";
    }

    const savedHtml = savedPages.length
      ? savedPages.slice(0, 12).map(function (item) {
          return card(item.title || "Planning guide", item.description || item.path || "", item.path || "/", "Saved page");
        }).join("")
      : "<div class='answer-card'><h3>No saved pages yet</h3><p>Use Save page on guides and tool results to build a project pack on this device.</p></div>";

    const taskHtml = openTasks.length
      ? openTasks.slice(0, 12).map(function (task) {
          return "<div class='answer-card'><h3>" + escapeHtml(task.title || "Planning task") + "</h3><p>" + escapeHtml(task.path || "Saved task") + "</p><button type='button' class='button-secondary' data-workspace-task-complete='" + escapeHtml(task.id) + "'>Mark complete</button></div>";
        }).join("")
      : "<div class='answer-card'><h3>No open tasks</h3><p>Add tasks from a tool result when you want a next action to come back to.</p></div>";

    const resultHtml = results.length
      ? results.slice(0, 8).map(function (item) {
          return card(item.result_label || item.title || "Planning result", item.summary || item.path || "", item.path || "/", "Saved result");
        }).join("")
      : "<div class='answer-card'><h3>No saved results yet</h3><p>Run a workflow tool, then save the result into My Planning Project.</p></div>";

    root.innerHTML = "<section><span class='eyebrow'>Workspace summary</span><h2>Your Saved Planning Workspace</h2><div class='answer-grid'><div class='answer-card'><h3>" + savedPages.length + " saved page" + (savedPages.length === 1 ? "" : "s") + "</h3><p>Guides and local pages kept on this device.</p></div><div class='answer-card'><h3>" + openTasks.length + " open task" + (openTasks.length === 1 ? "" : "s") + "</h3><p>Next actions still to work through.</p></div><div class='answer-card'><h3>" + checks.length + " completed check" + (checks.length === 1 ? "" : "s") + "</h3><p>Tool results marked as checked.</p></div></div><div class='hero-ctas'><button type='button' class='btn' data-project-action='save-page'>Save current page</button><button type='button' class='btn button-secondary' data-project-action='copy-summary'>Copy pack</button><button type='button' class='btn button-secondary' data-project-action='print-pack'>Print pack</button><button type='button' class='btn button-secondary' data-project-action='clear-project'>Clear workspace</button></div><p class='result-capture-note' data-workspace-note='true'>Stored only in this browser. No account is created.</p></section><section><span class='eyebrow'>Open tasks</span><h2>What Still Needs Doing</h2><div class='answer-grid'>" + taskHtml + "</div></section><section><span class='eyebrow'>Saved results</span><h2>Tool Results To Revisit</h2><div class='grid'>" + resultHtml + "</div></section><section><span class='eyebrow'>Saved guides</span><h2>Pages In Your Project Pack</h2><div class='grid'>" + savedHtml + "</div></section>";
  }

  function completeWorkspaceTask(taskId) {
    const ok = updateWorkspace(function (workspace) {
      workspace.tasks = (workspace.tasks || []).map(function (task) {
        if (task && task.id === taskId) {
          return Object.assign({}, task, { completed: true, completed_at: new Date().toISOString() });
        }
        return task;
      });
    });
    if (ok) {
      window.upgTrack("workspace_task_completed", { source_page: window.location.pathname });
      renderPanel();
      renderWorkspacePage();
    }
  }

  document.addEventListener("click", function (event) {
    const actionButton = event.target && event.target.closest ? event.target.closest("[data-project-action]") : null;
    if (actionButton) {
      const action = actionButton.getAttribute("data-project-action");
      if (action === "save-page" || action === "start-project") {
        saveCurrentPage(actionButton);
      } else if (action === "clear-project") {
        clearProject();
      } else if (action === "print-pack") {
        printPack();
      } else if (action === "copy-summary") {
        copySummary(actionButton);
      }
    }

    const workspaceButton = event.target && event.target.closest ? event.target.closest("[data-workspace-action]") : null;
    if (workspaceButton) {
      const action = workspaceButton.getAttribute("data-workspace-action");
      if (action === "save-tool") {
        saveToolResult(workspaceButton);
      } else if (action === "mark-tool-checked") {
        markToolChecked(workspaceButton);
      } else if (action === "add-tool-task") {
        addToolTask(workspaceButton);
      } else if (action === "copy-tool-summary") {
        copyToolSummary(workspaceButton);
      }
    }

    const completeButton = event.target && event.target.closest ? event.target.closest("[data-workspace-task-complete]") : null;
    if (completeButton) {
      completeWorkspaceTask(completeButton.getAttribute("data-workspace-task-complete") || "");
    }

    const nextStep = event.target && event.target.closest ? event.target.closest("[data-next-step-card]") : null;
    if (nextStep) {
      window.upgTrack(nextStep.getAttribute("data-next-step-event") || "next_step_card_click", {
        card_id: nextStep.getAttribute("data-next-step-card") || "",
        source_page: window.location.pathname,
        page_family: nextStep.getAttribute("data-page-family") || "",
        project_slug: nextStep.getAttribute("data-project-slug") || "",
        tool_slug: nextStep.getAttribute("data-tool-slug") || "",
      });
    }

    const triage = event.target && event.target.closest ? event.target.closest("[data-guidance-triage]") : null;
    if (triage) {
      window.upgTrack("guidance_triage_click", {
        route: triage.getAttribute("data-guidance-triage") || "",
        source_page: window.location.pathname,
      });
    }
  });

  document.addEventListener("submit", function (event) {
    const form = event.target && event.target.closest ? event.target.closest("form[data-guidance-form]") : null;
    if (form) {
      window.upgTrack("full_guidance_form_submit_attempt", {
        source_page: window.location.pathname,
        form_key: form.getAttribute("data-guidance-form") || "",
      });
    }
  }, true);

  document.querySelectorAll("[data-next-step-card]").forEach(function (card) {
    window.upgTrack("next_step_card_view", {
      card_id: card.getAttribute("data-next-step-card") || "",
      source_page: window.location.pathname,
      page_family: card.getAttribute("data-page-family") || "",
      project_slug: card.getAttribute("data-project-slug") || "",
      tool_slug: card.getAttribute("data-tool-slug") || "",
    });
  });

  renderPanel();
  renderWorkspacePage();
})();
