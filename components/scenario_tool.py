from components.interactive_tool_renderer import build_tool_fallback, render_inline_tool
from components.planning_tool_styles import STRUCTURED_TOOL_STYLES
from components.structured_tool_ui import STRUCTURED_TOOL_UI_HELPERS
from data.scenario_tool_checks import build_scenario_tool_config


def render_scenario_tool(scenario_slug: str) -> str:
    config = build_scenario_tool_config(scenario_slug)
    root_id = f"scenario-tool-{scenario_slug}"

    return render_inline_tool(
        """
<div class="tool-card decision-engine-card">
<style>
__STRUCTURED_TOOL_STYLES__
</style>
<div id="__ROOT_ID__" class="decision-engine" data-tool-root="__TOOL_ROOT__" data-tool-kind="scenario"></div>
<noscript>__NOSCRIPT_FALLBACK__</noscript>
<script>
(function () {{
  const CONFIG = __CONFIG__;
  const engine = document.getElementById("__ROOT_ID__");
  if (!engine) {{
    return;
  }}

  const STEP_NAMES = CONFIG.questions.map((question) => question.step_label).concat("Review");
  const IMPACT_SCORE = {{ clear: 0, warn: 1, danger: 2 }};

  function createState() {{
    return {{
      step: 1,
      answers: {{}},
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

  function questionByStep(stepNumber) {{
    return CONFIG.questions[stepNumber - 1] || null;
  }}

  function optionFor(question, value) {{
    return (question.options || []).find((item) => item.value === value) || null;
  }}
  function logToolEvent(type, detail) {{
    if (window.console && typeof window.console.log === "function") {{
      window.console.log("[scenario-tool:" + CONFIG.slug + "]", type, detail || "");
    }}
  }}

  function answerLabel(question, value) {{
    const option = optionFor(question, value);
    return option ? option.label : "Not chosen yet";
  }}

  function requiredForStep(stepNumber) {{
    if (stepNumber <= CONFIG.questions.length) {{
      const question = questionByStep(stepNumber);
      return Boolean(question && state.answers[question.id]);
    }}
    return CONFIG.questions.every((question) => Boolean(state.answers[question.id]));
  }}

__STRUCTURED_TOOL_UI_HELPERS__

  function pushUnique(target, value) {{
    if (value && !target.includes(value)) {{
      target.push(value);
    }}
  }}

  function assess() {{
    let highestImpact = "clear";
    let warnCount = 0;
    const reasons = [];

    CONFIG.questions.forEach((question) => {{
      const option = optionFor(question, state.answers[question.id]);
      if (!option) {{
        return;
      }}

      if (IMPACT_SCORE[option.impact] > IMPACT_SCORE[highestImpact]) {{
        highestImpact = option.impact;
      }}

      if (option.impact === "warn") {{
        warnCount += 1;
      }}

      if (option.impact !== "clear") {{
        pushUnique(reasons, option.reason);
      }}
    }});

    if (highestImpact !== "danger" && warnCount >= 2) {{
      highestImpact = "danger";
      pushUnique(reasons, "Several borderline answers are stacking up, which is usually enough to move this topic into a stricter check.");
    }}

    if (!reasons.length) {{
      pushUnique(reasons, CONFIG.baseline_reason);
    }}

    return {{
      status: highestImpact,
      summary: CONFIG.status_copy[highestImpact].summary,
      reasons: reasons.slice(0, 4),
      changes: (CONFIG.changes || []).slice(0, 4),
      next_checks: (CONFIG.next_checks || []).slice(0, 4),
      links: (CONFIG.links || []).slice(0, 4),
    }};
  }}

  function summaryItems() {{
    return CONFIG.questions.map((question) => {{
      return {{
        label: question.label,
        value: answerLabel(question, state.answers[question.id]),
      }};
    }});
  }}

  function renderChoiceGrid(question) {{
    return "<div class='decision-choice-grid'>" + question.options.map((option) => {{
      const selected = state.answers[question.id] === option.value ? " selected" : "";
      return "<button type='button' class='decision-choice" + selected + "' data-action='set-answer' data-question-id='" + escapeHtml(question.id) + "' data-value='" + escapeHtml(option.value) + "'><strong>" + escapeHtml(option.label) + "</strong><span>" + escapeHtml(option.hint || "") + "</span></button>";
    }}).join("") + "</div>";
  }}

  function renderQuestionStep(question) {{
    return "<div class='decision-step-copy'><h3>" + escapeHtml(question.label) + "</h3><p>" + escapeHtml(question.help || CONFIG.intro) + "</p></div><div class='decision-question'>" + renderChoiceGrid(question) + "</div><div class='decision-nav'><button type='button' class='button-secondary' data-action='prev'" + (state.step === 1 ? " disabled" : "") + ">Back</button><button type='button' class='cta' data-action='next' " + (requiredForStep(state.step) ? "" : "disabled") + ">Continue</button></div>";
  }}

  function renderReview() {{
    const cards = summaryItems().map((item) => {{
      return "<div class='decision-review-card'><strong>" + escapeHtml(item.label) + "</strong><span>" + escapeHtml(item.value) + "</span></div>";
    }}).join("");

    return "<div class='decision-step-copy'><h3>Review the answers and run the self-check</h3><p>" + escapeHtml(CONFIG.intro) + "</p></div><div class='decision-review-grid'>" + cards + "</div><div class='decision-nav'><button type='button' class='button-secondary' data-action='prev'>Back</button><button type='button' class='cta' data-action='run-check' " + (requiredForStep(CONFIG.questions.length + 1) ? "" : "disabled") + ">Check this topic</button></div>";
  }}

  function renderResult() {{
    const result = state.result;
    const status = CONFIG.status_copy[result.status];

    return "<div class='decision-result'><div class='decision-result-banner " + status.tone + "'><div class='decision-status'>" + escapeHtml(status.label) + "</div><h3>" + escapeHtml(CONFIG.title) + "</h3><p>" + escapeHtml(result.summary) + "</p></div><div class='decision-result-grid'><div class='decision-result-card'><h3>Why this topic needs that answer</h3><ul>" + result.reasons.map((item) => "<li>" + escapeHtml(item) + "</li>").join("") + "</ul></div><div class='decision-result-card'><h3>What usually changes it</h3><ul>" + result.changes.map((item) => "<li>" + escapeHtml(item) + "</li>").join("") + "</ul></div><div class='decision-result-card'><h3>What to check next</h3><ul>" + result.next_checks.map((item) => "<li>" + escapeHtml(item) + "</li>").join("") + "</ul></div></div><div><h3>Useful next pages</h3><div class='decision-result-links'>" + result.links.map((item) => "<a class='decision-result-link' href='" + escapeHtml(item.href) + "'><strong>" + escapeHtml(item.title) + "</strong><span>" + escapeHtml(item.description || "Open the next guide.") + "</span></a>").join("") + "</div></div>" + renderPostResultExtras({ toolSlug: CONFIG.slug, guideHref: (result.links[0] && result.links[0].href) || "/planning-permission/", guideTitle: (result.links[0] && result.links[0].title) || "Planning permission guide", resultLabel: status.label }) + "<div class='decision-nav'><button type='button' class='button-secondary' data-action='edit-result'>Edit answers</button><button type='button' class='button-secondary' data-action='reset'>Start again</button></div></div>";
  }}

  function renderSidebarSections() {{
    return {{
      title: "Your answers",
      summaryHtml: summaryItems().map((item) => "<div class='decision-summary-item'><strong>" + escapeHtml(item.label) + "</strong><span>" + escapeHtml(item.value) + "</span></div>").join(""),
      noteHtml: "<strong>How this tool works:</strong> it is a short, topic-specific self-check designed to tell you whether this one issue still looks simple, borderline or likely to need the fuller route.",
    }};
  }}

  function renderSidebar() {{
    const sections = renderSidebarSections();
    return "<aside class='decision-sidebar'><h3>" + escapeHtml(sections.title) + "</h3><div class='decision-summary-list'>" + sections.summaryHtml + "</div><div class='decision-method-note'>" + sections.noteHtml + "</div></aside>";
  }}

  function renderHeaderActions() {{
    return (state.result ? "<button type='button' class='button-secondary' data-action='edit-result'>Edit answers</button>" : "") + "<button type='button' class='button-secondary' data-action='reset'>Start again</button>";
  }}

  function renderStepContent() {{
    if (state.loading) {{
      return "<div class='decision-loading'><div class='decision-loading-dots'><span></span><span></span><span></span></div><h3>Checking the topic against the first common tripwires...</h3><p>This short pause is only UI polish while the rule-based result is assembled.</p></div>";
    }}

    if (state.result) {{
      return renderResult();
    }}

    if (state.step <= CONFIG.questions.length) {{
      return renderQuestionStep(questionByStep(state.step));
    }}

    return renderReview();
  }}

  function render() {{
    const progress = state.result ? 100 : (state.step / STEP_NAMES.length) * 100;
    const sections = renderSidebarSections();
    renderResponsiveToolShellInto(engine, {{
      kicker: CONFIG.title,
      heading: "Run the quick self-check",
      intro: CONFIG.intro,
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

    if (action === "set-answer") {{
      logToolEvent("click", {{ action, questionId, value }});
      state.answers = Object.assign({{}}, state.answers, {{ [questionId]: value }});
      state.result = null;
      render();
      return;
    }}

    if (action === "next" && state.step < STEP_NAMES.length && requiredForStep(state.step)) {{
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

    if (action === "run-check" && requiredForStep(STEP_NAMES.length)) {{
      logToolEvent("submit", {{ action, snapshot: summaryItems() }});
      state.loading = true;
      state.result = null;
      render();
      window.setTimeout(function () {{
        state.loading = false;
        state.result = assess();
        logToolEvent("result", state.result);
        render();
      }}, 450);
      return;
    }}

    if (action === "edit-result") {{
      logToolEvent("click", {{ action }});
      state.result = null;
      state.loading = false;
      state.step = STEP_NAMES.length;
      render();
      return;
    }}

    if (action === "reset") {{
      logToolEvent("click", {{ action }});
      state = createState();
      render();
    }}
  }});

  render();
}})();
</script>
</div>
""",
        config=config,
        styles=STRUCTURED_TOOL_STYLES,
        replacements={
            "__STRUCTURED_TOOL_UI_HELPERS__": STRUCTURED_TOOL_UI_HELPERS,
            "__ROOT_ID__": root_id,
            "__TOOL_ROOT__": scenario_slug,
            "__NOSCRIPT_FALLBACK__": build_tool_fallback(
                "Self-check loading",
                "If the quick self-check does not appear, open the full topic guide or use the decision engine while JavaScript is unavailable.",
                config["links"][:2],
            ),
        },
    )
