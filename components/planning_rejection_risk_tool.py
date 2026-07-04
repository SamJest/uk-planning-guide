from components.interactive_tool_renderer import build_tool_fallback, render_inline_tool
from components.planning_tool_styles import STRUCTURED_TOOL_STYLES
from components.structured_tool_ui import STRUCTURED_TOOL_UI_HELPERS
from data.planning_rejection_risk import RISK_ANALYZER_CONFIG


def render_planning_rejection_risk_tool():
    return render_inline_tool(
        """
<div class="tool-card decision-engine-card">
<style>
__STRUCTURED_TOOL_STYLES__
.risk-factor-grid{{display:grid;gap:12px;grid-template-columns:repeat(auto-fit,minmax(min(100%,220px),1fr));}}
.risk-factor-card{{min-width:0;padding:18px;background:rgba(255,255,255,.88);border:1px solid rgba(31,41,55,.08);border-radius:18px;box-shadow:var(--shadow-soft);}}
.risk-factor-card h4{{margin:10px 0 8px;font-size:1rem;}}
.risk-pill{{display:inline-flex;align-items:center;padding:6px 10px;border-radius:999px;font-size:11px;font-weight:800;letter-spacing:.08em;text-transform:uppercase;}}
.risk-pill.low{{background:rgba(223,241,234,.92);color:var(--accent-text);}}
.risk-pill.moderate{{background:rgba(255,246,228,.96);color:#8a5a14;}}
.risk-pill.high{{background:rgba(255,236,233,.98);color:#9a362d;}}
</style>
<div id="planning-rejection-risk-tool" class="decision-engine" data-tool-root="planning-rejection-risk-analyzer" data-tool-kind="structured"></div>
<noscript>__NOSCRIPT_FALLBACK__</noscript>
<script>
(function () {{
  const CONFIG = __CONFIG__;
  const engine = document.getElementById("planning-rejection-risk-tool");
  if (!engine) {{
    return;
  }}

  const STEP_NAMES = ["Project", "Property", "Details", "Review"];
  const SEVERITY_SCORE = {{ low: 1, moderate: 2, high: 3 }};
  const RESULT_COPY = {{
    low: {{
      label: "Low risk",
      tone: "good",
      summary(project) {{
        return "These answers do not point to a strong refusal risk for this " + project.label.toLowerCase() + ", provided the drawings and detailing are competent.";
      }},
    }},
    moderate: {{
      label: "Moderate risk",
      tone: "warn",
      summary(project) {{
        return "This " + project.label.toLowerCase() + " has some planning application weak points that could lead to objections if the design is not handled carefully.";
      }},
    }},
    high: {{
      label: "High risk",
      tone: "danger",
      summary(project) {{
        return "This " + project.label.toLowerCase() + " is showing multiple refusal risks based on the answers provided, so the design would benefit from changes before submission.";
      }},
    }},
  }};

  const projectMap = Object.fromEntries(CONFIG.projects.map((project) => [project.id, project]));

  function createState() {{
    return {{
      step: 1,
      project: "",
      property: "",
      previousWork: "",
      constraints: [],
      detailAnswers: {{}},
      loading: false,
      result: null,
    }};
  }}

  let state = createState();

  function escapeHtml(value) {{
    return String(value || "")
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;")
      .replace(/'/g, "&#39;");
  }}

  function project() {{
    return projectMap[state.project] || null;
  }}

  function optionLabel(options, value) {{
    const match = (options || []).find((item) => item.value === value);
    return match ? match.label : "";
  }}

  function answerLabel(question, value) {{
    if (!question) {{
      return value === "yes" ? "Yes" : value === "no" ? "No" : "";
    }}
    return optionLabel(question.options || [], value);
  }}

  function propertyLabel() {{
    return optionLabel(CONFIG.property_types, state.property);
  }}

  function previousWorkLabel() {{
    return optionLabel(CONFIG.previous_work_options, state.previousWork);
  }}

  function constraintLabels() {{
    return state.constraints.map((value) => optionLabel(CONFIG.constraint_options, value)).filter(Boolean);
  }}
  function logToolEvent(type, detail) {{
    if (window.console && typeof window.console.log === "function") {{
      window.console.log("[planning-rejection-risk-analyzer]", type, detail || "");
    }}
  }}

  function requiredForStep(stepNumber) {{
    const currentProject = project();
    if (stepNumber === 1) {{
      return Boolean(state.project);
    }}
    if (stepNumber === 2) {{
      return Boolean(state.property && state.previousWork);
    }}
    if (stepNumber === 3) {{
      if (!currentProject) {{
        return false;
      }}
      const answers = state.detailAnswers;
      if (!answers[currentProject.primary_question.id]) {{
        return false;
      }}
      if (currentProject.secondary_question && !answers[currentProject.secondary_question.id]) {{
        return false;
      }}
      return (currentProject.binary_questions || []).every((question) => Boolean(answers[question.id]));
    }}
    if (stepNumber === 4) {{
      return requiredForStep(1) && requiredForStep(2) && requiredForStep(3);
    }}
    return false;
  }}

__STRUCTURED_TOOL_UI_HELPERS__

  function pushUnique(target, text) {{
    if (text && !target.includes(text)) {{
      target.push(text);
    }}
  }}

  function pushLink(target, item) {{
    if (item && item.href && !target.some((link) => link.href === item.href)) {{
      target.push(item);
    }}
  }}

  function summaryItems() {{
    const currentProject = project();
    if (!currentProject) {{
      return [];
    }}

    const items = [
      {{ label: "Project", value: currentProject.label }},
      {{ label: "Property", value: propertyLabel() || "Not chosen yet" }},
      {{ label: "Previous additions", value: previousWorkLabel() || "Not chosen yet" }},
      {{ label: "Constraints", value: constraintLabels().length ? constraintLabels().join(", ") : "None selected" }},
    ];
    const answers = state.detailAnswers;

    if (currentProject.primary_question) {{
      items.push({{ label: currentProject.primary_question.label, value: answerLabel(currentProject.primary_question, answers[currentProject.primary_question.id]) || "Not chosen yet" }});
    }}
    if (currentProject.secondary_question) {{
      items.push({{ label: currentProject.secondary_question.label, value: answerLabel(currentProject.secondary_question, answers[currentProject.secondary_question.id]) || "Not chosen yet" }});
    }}
    (currentProject.binary_questions || []).forEach((question) => {{
      items.push({{ label: question.label, value: answers[question.id] === "yes" ? "Yes" : answers[question.id] === "no" ? "No" : "Not chosen yet" }});
    }});
    return items;
  }}

  function renderChoiceGrid(options, selectedValue, action, extraAttributes) {{
    return "<div class='decision-choice-grid'>" + options.map((option) => {{
      const optionValue = option.value || option.id || "";
      const selected = optionValue === selectedValue ? " selected" : "";
      return "<button type='button' class='decision-choice" + selected + "' data-action='" + action + "' data-value='" + escapeHtml(optionValue) + "'" + (extraAttributes || "") + "><strong>" + escapeHtml(option.label) + "</strong><span>" + escapeHtml(option.hint || "") + "</span></button>";
    }}).join("") + "</div>";
  }}

  function renderBinaryQuestion(question, currentValue) {{
    return "<div class='decision-question'><h4>" + escapeHtml(question.label) + "</h4>" + renderChoiceGrid([{ value: "yes", label: "Yes", hint: question.help || "Yes." }, { value: "no", label: "No", hint: question.help || "No." }], currentValue, "set-binary", " data-question-id='" + escapeHtml(question.id) + "'") + "</div>";
  }}

  function riskFaqLink(level) {{
    if (level === "high") {{
      return {{
        title: "What Happens If Planning Permission Is Refused?",
        href: "/planning-faq/what-happens-if-planning-permission-is-refused/",
        description: "Useful when the scheme looks weak enough that redesign may be smarter than pushing ahead unchanged.",
      }};
    }}
    return {{
      title: "Can Neighbours Stop Planning Permission?",
      href: "/planning-faq/can-neighbours-stop-planning-permission/",
      description: "Useful when the risk profile is being driven by privacy, boundary pressure or likely objections.",
    }};
  }}

  function riskRuleLink(result) {{
    const firstRule = firstLinkByCategory(result.links, "rule");
    if (firstRule) {{
      return firstRule;
    }}
    return {{
      title: "Planning Permission",
      href: "/planning-permission/",
      description: "Open the main planning hub when refusal risk is pushing the project toward a fuller application route.",
    }};
  }}

  function valueForCondition(key) {{
    if (key === "property") {{
      return state.property;
    }}
    if (key === "previous_work") {{
      return state.previousWork;
    }}
    return state.detailAnswers[key] || "";
  }}

  function ruleMatches(rule) {{
    const conditions = rule.conditions || {{}};
    for (const key of Object.keys(conditions)) {{
      const actual = valueForCondition(key);
      if (!conditions[key].includes(actual)) {{
        return false;
      }}
    }}

    if (rule.constraints_any && !rule.constraints_any.some((item) => state.constraints.includes(item))) {{
      return false;
    }}

    return true;
  }}

  function ensureFactor(factors, factorId, severity) {{
    const definition = CONFIG.risk_factors[factorId];
    if (!definition) {{
      return null;
    }}

    if (!factors[factorId]) {{
      factors[factorId] = {{
        id: factorId,
        title: definition.title,
        explanation: definition.explanation,
        severity: severity,
        score: SEVERITY_SCORE[severity],
        reasons: [],
        reductionTips: [],
        links: [],
      }};
    }}

    if (SEVERITY_SCORE[severity] > factors[factorId].score) {{
      factors[factorId].severity = severity;
      factors[factorId].score = SEVERITY_SCORE[severity];
    }}

    definition.reduction_tips.forEach((item) => pushUnique(factors[factorId].reductionTips, item));
    definition.links.forEach((item) => pushLink(factors[factorId].links, item));
    return factors[factorId];
  }}

  function assess() {{
    const currentProject = project();
    const factors = {{}};
    const pageLinks = [];
    const why = [];

    pushLink(pageLinks, {{ title: currentProject.guide_title, href: currentProject.guide_href, description: "Open the main project guide for the wider planning context behind these risks." }});
    (currentProject.related_pages || []).forEach((item) => pushLink(pageLinks, item));
    (CONFIG.default_links || []).forEach((item) => pushLink(pageLinks, item));

    [...(CONFIG.global_rules || []), ...(currentProject.risk_rules || [])].forEach((rule) => {{
      if (!ruleMatches(rule)) {{
        return;
      }}

      const factor = ensureFactor(factors, rule.factor, rule.severity);
      if (!factor) {{
        return;
      }}

      pushUnique(factor.reasons, rule.because);
      pushUnique(why, rule.because);
      factor.links.forEach((item) => pushLink(pageLinks, item));
    }});

    let matchedFactors = Object.values(factors).sort((a, b) => b.score - a.score || a.title.localeCompare(b.title));

    if (!matchedFactors.length) {{
      const baseline = ensureFactor(factors, "baseline_detailing", "low");
      pushUnique(baseline.reasons, "Nothing in these answers points to a strong refusal signal on its own, but design quality and fit still matter.");
      matchedFactors = [baseline];
      pushUnique(why, baseline.reasons[0]);
      baseline.links.forEach((item) => pushLink(pageLinks, item));
    }}

    const riskScore = matchedFactors.reduce((total, factor) => total + factor.score, 0);
    const hasHigh = matchedFactors.some((factor) => factor.score >= 3);
    const hasModerate = matchedFactors.some((factor) => factor.score >= 2);

    let level = "low";
    if (hasHigh || riskScore >= 6) {{
      level = "high";
    }} else if (hasModerate || riskScore >= 3) {{
      level = "moderate";
    }}

    const reductionTips = [];
    matchedFactors.forEach((factor) => factor.reductionTips.forEach((item) => pushUnique(reductionTips, item)));

    return {{
      level,
      summary: RESULT_COPY[level].summary(currentProject),
      factors: matchedFactors.slice(0, 4),
      why: why.slice(0, 5),
      reductionTips: reductionTips.slice(0, 6),
      links: pageLinks.slice(0, 6),
    }};
  }}

  function renderResult() {{
    const currentProject = project();
    const result = state.result;
    const status = RESULT_COPY[result.level];
    const primaryLinks = buildCoreNextLinks({{
      links: result.links,
      projectLink: {{ title: currentProject.guide_title, href: currentProject.guide_href, description: "Open the main project guide behind these refusal risks." }},
      ruleLink: riskRuleLink(result),
      faqLink: riskFaqLink(result.level),
      authorityLink: {{
        title: "Local Authorities",
        href: "/councils/",
        description: "Use the authority layer when local policy, heritage or council expectations may be tightening the risk picture.",
      }},
    }});

    return "<div class='decision-result'><div class='decision-result-banner " + status.tone + "'><div class='decision-status'>" + escapeHtml(status.label) + "</div><h3>" + escapeHtml(currentProject.label) + "</h3><p>" + escapeHtml(result.summary) + "</p></div><div><h3>Key risk factors</h3><div class='risk-factor-grid'>" + result.factors.map((factor) => "<div class='risk-factor-card'><span class='risk-pill " + factor.severity + "'>" + escapeHtml(factor.severity + " risk") + "</span><h4>" + escapeHtml(factor.title) + "</h4><p>" + escapeHtml(factor.explanation) + "</p></div>").join("") + "</div></div><div class='decision-result-grid'><div class='decision-result-card'><h3>Why these risks apply</h3><ul>" + result.why.map((item) => "<li>" + escapeHtml(item) + "</li>").join("") + "</ul></div><div class='decision-result-card'><h3>What can reduce these risks</h3><ul>" + result.reductionTips.map((item) => "<li>" + escapeHtml(item) + "</li>").join("") + "</ul></div></div><div><h3>Best next pages</h3><div class='decision-result-links'>" + primaryLinks.map((item) => "<a class='decision-result-link' href='" + escapeHtml(item.href) + "'><strong>" + escapeHtml(item.title) + "</strong><span>" + escapeHtml(item.description || "Open the next guide.") + "</span></a>").join("") + "</div></div>" + renderPostResultExtras({ toolSlug: "planning-rejection-risk-analyzer", guideHref: currentProject.guide_href, guideTitle: currentProject.guide_title, resultLabel: status.label, nextTool: { href: "/tools/planning-route-planner/", title: "Use another tool", description: "Compare the likely planning route if you want a follow-on route check." } }) + "<div class='decision-nav'><button type='button' class='button-secondary' data-action='edit-result'>Edit answers</button><button type='button' class='button-secondary' data-action='reset'>Start again</button></div></div>";
  }}

  function renderStepContent() {{
    const currentProject = project();

    if (state.loading) {{
      return "<div class='decision-loading'><div class='decision-loading-dots'><span></span><span></span><span></span></div><h3>Analysing your project against common refusal risks...</h3><p>This short pause is just UI polish while the tool assembles the rule-based result from your structured answers.</p></div>";
    }}

    if (state.result && currentProject) {{
      return renderResult();
    }}

    if (state.step === 1) {{
      return "<div class='decision-step-copy'><h3>Which kind of project are you analysing?</h3><p>Choose the nearest project type. The next steps reuse the same structured project model as the decision tool, but the output focuses on refusal risk instead of permission route.</p></div>" + renderChoiceGrid(CONFIG.projects, state.project, "choose-project") + "<div class='decision-nav'><span></span><button type='button' class='cta' data-action='next' " + (requiredForStep(1) ? "" : "disabled") + ">Continue</button></div>";
    }}

    if (state.step === 2) {{
      return "<div class='decision-step-copy'><h3>Tell the tool about the property context</h3><p>Property type, previous additions and local constraints can all change how risky the application looks before the design is even fully detailed.</p></div><div class='decision-question'><h4>Property type</h4>" + renderChoiceGrid(CONFIG.property_types, state.property, "choose-property") + "</div><div class='decision-question'><h4>Previous extensions or major roof changes already on the property?</h4>" + renderChoiceGrid(CONFIG.previous_work_options, state.previousWork, "choose-previous-work") + "</div><div class='decision-question'><h4>Special local constraints</h4><div class='decision-chip-row'>" + CONFIG.constraint_options.map((option) => {{ const selected = state.constraints.includes(option.value) ? " selected" : ""; return "<button type='button' class='decision-chip" + selected + "' data-action='toggle-constraint' data-value='" + escapeHtml(option.value) + "'>" + escapeHtml(option.label) + "</button>"; }}).join("") + "</div><div class='decision-question-note'>Select any that already apply. Leave them clear if the site is not affected.</div></div><div class='decision-nav'><button type='button' class='button-secondary' data-action='prev'>Back</button><button type='button' class='cta' data-action='next' " + (requiredForStep(2) ? "" : "disabled") + ">Continue</button></div>";
    }}

    if (state.step === 3 && currentProject) {{
      const answers = state.detailAnswers;
      return "<div class='decision-step-copy'><h3>Check the shape, scale and siting</h3><p>" + escapeHtml(currentProject.description) + "</p></div><div class='decision-question'><h4>" + escapeHtml(currentProject.primary_question.label) + "</h4>" + renderChoiceGrid(currentProject.primary_question.options, answers[currentProject.primary_question.id], "set-detail", " data-question-id='" + escapeHtml(currentProject.primary_question.id) + "'") + "</div>" + (currentProject.secondary_question ? "<div class='decision-question'><h4>" + escapeHtml(currentProject.secondary_question.label) + "</h4>" + renderChoiceGrid(currentProject.secondary_question.options, answers[currentProject.secondary_question.id], "set-detail", " data-question-id='" + escapeHtml(currentProject.secondary_question.id) + "'") + "</div>" : "") + ((currentProject.binary_questions || []).length ? "<div class='decision-binary-grid'>" + currentProject.binary_questions.map((question) => renderBinaryQuestion(question, answers[question.id])).join("") + "</div>" : "") + "<div class='decision-nav'><button type='button' class='button-secondary' data-action='prev'>Back</button><button type='button' class='cta' data-action='next' " + (requiredForStep(3) ? "" : "disabled") + ">Continue</button></div>";
    }}

    if (state.step === 4 && currentProject) {{
      const cards = summaryItems().map((item) => "<div class='decision-review-card'><strong>" + escapeHtml(item.label) + "</strong><span>" + escapeHtml(item.value) + "</span></div>").join("");
      return "<div class='decision-step-copy'><h3>Review the answers and analyse the refusal risks</h3><p>The result will prioritise the issues most likely to cause trouble, explain why they apply, and show what could make the proposal easier to support.</p></div><div class='decision-review-grid'>" + cards + "</div><div class='decision-nav'><button type='button' class='button-secondary' data-action='prev'>Back</button><button type='button' class='cta' data-action='run-check' " + (requiredForStep(4) ? "" : "disabled") + ">Analyse my project</button></div>";
    }}

    return "";
  }}

  function renderSidebarSections() {{
    const items = summaryItems();
    return {{
      title: "Your answers",
      summaryHtml: items.length ? items.map((item) => "<div class='decision-summary-item'><strong>" + escapeHtml(item.label) + "</strong><span>" + escapeHtml(item.value) + "</span></div>").join("") : "<div class='decision-summary-item'><strong>Project snapshot</strong><span>Choose a project to start the risk analysis.</span></div>",
      noteHtml: "<strong>How this tool works:</strong> it maps your structured answers to common refusal themes such as bulk, privacy, design character, parking and heritage impact. It is for early risk analysis, not a substitute for formal planning advice.",
    }};
  }}

  function renderSidebar() {{
    const sections = renderSidebarSections();
    return "<div class='decision-sidebar'><h3>" + escapeHtml(sections.title) + "</h3><div class='decision-summary-list'>" + sections.summaryHtml + "</div><div class='decision-method-note'>" + sections.noteHtml + "</div></div>";
  }}

  function renderHeaderActions() {{
    return (state.result ? "<button type='button' class='button-secondary' data-action='edit-result'>Edit answers</button>" : "") + "<button type='button' class='button-secondary' data-action='reset'>Start again</button>";
  }}

  function render() {{
    const progress = state.result ? 100 : (state.step / STEP_NAMES.length) * 100;
    const sections = renderSidebarSections();
    renderResponsiveToolShellInto(engine, {{
      kicker: "Planning Rejection Risk Analyzer",
      heading: "See the main reasons a planning application could be refused",
      intro: "A structured follow-on from the decision tool for users who want to stress-test scale, neighbour impact, design character and local policy risk before an application goes in.",
      actionsHtml: renderHeaderActions(),
      progress,
      stepNames: STEP_NAMES,
      currentStep: state.step,
      hasResult: Boolean(state.result),
      contentHtml: renderStepContent(),
      sidebarHtml: renderSidebar(),
      summaryTitle: sections.title,
      summaryHtml: sections.summaryHtml,
      noteHtml: sections.noteHtml,
      summaryHint: "View answers",
    }});
  }}

  engine.addEventListener("click", function (event) {{
    const target = event.target.closest("[data-action]");
    if (!target) {{
      return;
    }}

    const action = target.getAttribute("data-action");
    const value = target.getAttribute("data-value") || "";
    const questionId = target.getAttribute("data-question-id") || "";

    if (action === "choose-project") {{
      logToolEvent("click", {{ action, value }});
      state.project = value;
      state.detailAnswers = {{}};
      state.result = null;
      render();
      return;
    }}

    if (action === "choose-property") {{
      logToolEvent("click", {{ action, value }});
      state.property = value;
      state.result = null;
      render();
      return;
    }}

    if (action === "choose-previous-work") {{
      logToolEvent("click", {{ action, value }});
      state.previousWork = value;
      state.result = null;
      render();
      return;
    }}

    if (action === "toggle-constraint") {{
      logToolEvent("click", {{ action, value }});
      state.result = null;
      if (state.constraints.includes(value)) {{
        state.constraints = state.constraints.filter((item) => item !== value);
      }} else {{
        state.constraints = state.constraints.concat(value);
      }}
      render();
      return;
    }}

    if (action === "set-detail" || action === "set-binary") {{
      logToolEvent("click", {{ action, questionId, value }});
      state.detailAnswers = Object.assign({{}}, state.detailAnswers, {{ [questionId]: value }});
      state.result = null;
      render();
      return;
    }}

    if (action === "next" && state.step < 4 && requiredForStep(state.step)) {{
      logToolEvent("click", {{ action, step: state.step }});
      state.step += 1;
      render();
      return;
    }}

    if (action === "prev" && state.step > 1) {{
      logToolEvent("click", {{ action, step: state.step }});
      state.step -= 1;
      render();
      return;
    }}

    if (action === "edit-result") {{
      logToolEvent("click", {{ action }});
      state.result = null;
      state.loading = false;
      state.step = 4;
      render();
      return;
    }}

    if (action === "reset") {{
      logToolEvent("click", {{ action }});
      state = createState();
      render();
      return;
    }}

    if (action === "run-check" && requiredForStep(4)) {{
      logToolEvent("submit", {{ action, snapshot: summaryItems() }});
      state.loading = true;
      state.result = null;
      render();
      window.setTimeout(function () {{
        state.loading = false;
        state.result = assess();
        logToolEvent("result", state.result);
        render();
      }}, 720);
    }}
  }});

  render();
}})();
</script>
</div>
""",
        config=RISK_ANALYZER_CONFIG,
        styles=STRUCTURED_TOOL_STYLES,
        replacements={
            "__STRUCTURED_TOOL_UI_HELPERS__": STRUCTURED_TOOL_UI_HELPERS,
            "__NOSCRIPT_FALLBACK__": build_tool_fallback(
                "Risk analysis loading",
                "If the refusal-risk analyzer does not appear, use the decision engine first or open the planning permission guidance while JavaScript is unavailable.",
                [
                    {
                        "title": "Planning Decision Engine",
                        "href": "/tools/planning-decision-tool/",
                        "description": "Confirm the likely route first if you still need a permission check.",
                    },
                    {
                        "title": "Planning Permission",
                        "href": "/planning-permission/",
                        "description": "Open the main application guide while the risk analyzer is unavailable.",
                    },
                ],
            )
        },
    )
