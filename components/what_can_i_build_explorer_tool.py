from components.interactive_tool_renderer import build_tool_fallback, render_inline_tool
from components.planning_tool_styles import STRUCTURED_TOOL_STYLES
from components.structured_tool_ui import STRUCTURED_TOOL_UI_HELPERS
from data.what_can_i_build_explorer import WHAT_CAN_I_BUILD_EXPLORER_CONFIG


def render_what_can_i_build_explorer_tool():
    return render_inline_tool(
        """
<div class="tool-card decision-engine-card">
<style>
__STRUCTURED_TOOL_STYLES__
.explorer-filter-bar{{display:grid;gap:10px;grid-template-columns:repeat(auto-fit,minmax(min(100%,180px),1fr));margin:4px 0 18px;}}
.explorer-grid{{display:grid;gap:14px;grid-template-columns:repeat(auto-fit,minmax(min(100%,240px),1fr));}}
.explorer-card{{min-width:0;padding:18px;background:rgba(255,255,255,.9);border:1px solid rgba(31,41,55,.08);border-radius:20px;box-shadow:var(--shadow-soft);display:flex;flex-direction:column;gap:14px;}}
.explorer-card.good{{background:linear-gradient(180deg,rgba(244,252,249,.98),rgba(255,255,255,.95));border-color:rgba(31,111,95,.16);}}
.explorer-card.warn{{background:linear-gradient(180deg,rgba(255,250,240,.99),rgba(255,255,255,.95));border-color:rgba(183,121,31,.18);}}
.explorer-card.danger{{background:linear-gradient(180deg,rgba(255,242,239,.99),rgba(255,255,255,.95));border-color:rgba(186,66,55,.18);}}
.explorer-card-header{{display:flex;justify-content:space-between;gap:10px;align-items:flex-start;flex-wrap:wrap;}}
.explorer-status{{display:inline-flex;align-items:center;padding:7px 11px;border-radius:999px;font-size:11px;font-weight:800;letter-spacing:.08em;text-transform:uppercase;background:rgba(255,255,255,.86);}}
.explorer-status.good{{color:var(--accent-text);background:rgba(223,241,234,.96);}}
.explorer-status.warn{{color:#8a5a14;background:rgba(255,246,228,.96);}}
.explorer-status.danger{{color:#9a362d;background:rgba(255,236,233,.98);}}
.explorer-fit-note{{font-size:12px;font-weight:700;color:var(--ink-faint);text-transform:uppercase;letter-spacing:.06em;}}
.explorer-card h3{{margin:0;font-size:1.1rem;}}
.explorer-card p{{margin:0;}}
.explorer-meta{{padding:12px 14px;background:rgba(247,241,232,.78);border:1px solid rgba(31,41,55,.06);border-radius:16px;}}
.explorer-meta strong,.explorer-why strong{{display:block;margin-bottom:6px;font-size:12px;letter-spacing:.08em;text-transform:uppercase;color:var(--ink-faint);}}
.explorer-why ul{{margin:0;padding-left:18px;}}
.explorer-card-actions{{display:flex;flex-wrap:wrap;gap:10px;margin-top:auto;}}
.explorer-link{{display:inline-flex;align-items:center;justify-content:center;padding:10px 14px;border-radius:999px;border:1px solid rgba(31,41,55,.12);font-weight:700;color:var(--ink);background:#fff;}}
.explorer-link.primary{{background:var(--accent);border-color:var(--accent);color:#fff;}}
.explorer-link:hover{{border-color:rgba(31,111,95,.28);}}
.explorer-summary-strip{{display:grid;gap:12px;grid-template-columns:repeat(auto-fit,minmax(min(100%,160px),1fr));margin-top:8px;}}
.explorer-summary-card{{padding:14px 16px;background:rgba(255,255,255,.76);border:1px solid rgba(31,41,55,.08);border-radius:18px;}}
.explorer-summary-card strong{{display:block;margin-bottom:4px;font-size:12px;letter-spacing:.08em;text-transform:uppercase;color:var(--ink-faint);}}
.explorer-inline-links{{display:grid;gap:12px;grid-template-columns:repeat(auto-fit,minmax(min(100%,220px),1fr));}}
.explorer-inline-link{{display:block;padding:16px;background:rgba(255,255,255,.9);border:1px solid rgba(31,41,55,.08);border-radius:18px;color:inherit;box-shadow:var(--shadow-soft);}}
.explorer-inline-link:hover{{border-color:rgba(31,111,95,.22);box-shadow:0 18px 30px rgba(31,41,55,.08);transform:translateY(-1px);}}
.explorer-empty{{padding:18px;border-radius:18px;background:rgba(247,241,232,.8);border:1px solid rgba(31,41,55,.08);}}
@media (pointer:coarse), (max-width:1024px){{
  .explorer-grid,.explorer-summary-strip,.explorer-inline-links{{grid-template-columns:1fr;}}
}}
@media (pointer:coarse), (max-width:768px){{
  .explorer-grid,.explorer-summary-strip,.explorer-inline-links{{grid-template-columns:1fr;}}
  .explorer-filter-bar{{grid-template-columns:1fr;}}
  .explorer-card-header{{flex-direction:column;}}
  .explorer-card-actions{{flex-direction:column;}}
  .explorer-link,.explorer-inline-link{{width:100%;}}
}}
</style>
<div id="what-can-i-build-explorer" class="decision-engine" data-tool-root="what-can-i-build-explorer" data-tool-kind="structured"></div>
<noscript>__NOSCRIPT_FALLBACK__</noscript>
<script>
(function () {{
  const CONFIG = __CONFIG__;
  const engine = document.getElementById("what-can-i-build-explorer");
  if (!engine) {{
    return;
  }}

  const STEP_NAMES = ["Property", "Space", "Local layer", "Review"];
  const projectMap = Object.fromEntries(CONFIG.project_options.map((project) => [project.id, project]));

  function createState() {{
    return {{
      step: 1,
      property: "",
      space: "",
      features: [],
      constraints: [],
      loading: false,
      result: null,
      filter: "all",
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

  function optionLabel(options, value) {{
    const match = (options || []).find((item) => item.value === value);
    return match ? match.label : "";
  }}

  function propertyLabel() {{
    return optionLabel(CONFIG.property_types, state.property);
  }}

  function spaceLabel() {{
    return optionLabel(CONFIG.space_options, state.space);
  }}

  function featureLabels() {{
    return state.features.map((value) => optionLabel(CONFIG.feature_options, value)).filter(Boolean);
  }}

  function constraintLabels() {{
    return state.constraints.map((value) => optionLabel(CONFIG.constraint_options, value)).filter(Boolean);
  }}
  function logToolEvent(type, detail) {{
    if (window.console && typeof window.console.log === "function") {{
      window.console.log("[what-can-i-build-explorer]", type, detail || "");
    }}
  }}

  function requiredForStep(stepNumber) {{
    if (stepNumber === 1) {{
      return Boolean(state.property);
    }}
    if (stepNumber === 2) {{
      return Boolean(state.space);
    }}
    if (stepNumber === 3) {{
      return requiredForStep(1) && requiredForStep(2);
    }}
    if (stepNumber === 4) {{
      return requiredForStep(1) && requiredForStep(2);
    }}
    return false;
  }}

__STRUCTURED_TOOL_UI_HELPERS__

  function pushUnique(target, value) {{
    if (value && !target.includes(value)) {{
      target.push(value);
    }}
  }}

  function matchesRule(rule) {{
    if (rule.property && !rule.property.includes(state.property)) {{
      return false;
    }}
    if (rule.space && !rule.space.includes(state.space)) {{
      return false;
    }}
    if (rule.features_any && !rule.features_any.some((item) => state.features.includes(item))) {{
      return false;
    }}
    if (rule.features_all && !rule.features_all.every((item) => state.features.includes(item))) {{
      return false;
    }}
    if (rule.features_none && rule.features_none.some((item) => state.features.includes(item))) {{
      return false;
    }}
    if (rule.constraints_any && !rule.constraints_any.some((item) => state.constraints.includes(item))) {{
      return false;
    }}
    return true;
  }}

  function statusForScore(score) {{
    if (score >= 4) {{
      return "commonly_permitted";
    }}
    if (score >= 2) {{
      return "depends";
    }}
    return "likely_needs";
  }}

  function fitNote(score) {{
    if (score >= 5) {{
      return "Strong early fit";
    }}
    if (score >= 3) {{
      return "Worth checking next";
    }}
    return "More conditional";
  }}

  function evaluateOption(option) {{
    let score = option.base_score || 0;
    const reasons = [];

    (option.rules || []).forEach((rule) => {{
      if (!matchesRule(rule)) {{
        return;
      }}
      score += rule.adjust || 0;
      pushUnique(reasons, rule.reason);
    }});

    const status = statusForScore(score);
    const statusCopy = CONFIG.status_copy[status];

    return {{
      id: option.id,
      title: option.title,
      description: option.description,
      typical_limits: option.typical_limits,
      guide_href: option.guide_href,
      guide_title: option.guide_title,
      score,
      status,
      tone: statusCopy.tone,
      status_label: statusCopy.label,
      fit_note: fitNote(score),
      reasons: reasons.slice(0, 3),
    }};
  }}

  function assess() {{
    const options = CONFIG.project_options
      .map(evaluateOption)
      .sort((a, b) => b.score - a.score || a.title.localeCompare(b.title));

    const counts = {{
      commonly_permitted: options.filter((item) => item.status === "commonly_permitted").length,
      depends: options.filter((item) => item.status === "depends").length,
      likely_needs: options.filter((item) => item.status === "likely_needs").length,
    }};

    const best = options.filter((item) => item.status !== "likely_needs").slice(0, 3);
    const summary = best.length
      ? "The clearest starting points here look like " + best.map((item) => item.title.toLowerCase()).join(", ").replace(/, ([^,]*)$/, " and $1") + "."
      : "Most options here depend on a fuller check or a tighter local route, so the next best move is to test one option in the decision tool.";

    return {{
      options,
      counts,
      summary,
      property_label: propertyLabel(),
      space_label: spaceLabel(),
      feature_labels: featureLabels(),
      constraint_labels: constraintLabels(),
    }};
  }}

  function renderChoiceCards(options, selectedValue, action) {{
    return "<div class='decision-choice-grid'>" + options.map((option) => {{
      const selected = selectedValue === option.value ? " selected" : "";
      return "<button type='button' class='decision-choice" + selected + "' data-action='" + action + "' data-value='" + escapeHtml(option.value) + "'><strong>" + escapeHtml(option.label) + "</strong><span>" + escapeHtml(option.hint || "") + "</span></button>";
    }}).join("") + "</div>";
  }}

  function renderChipChoices(options, selectedValues, action) {{
    return "<div class='decision-chip-row'>" + options.map((option) => {{
      const selected = selectedValues.includes(option.value) ? " selected" : "";
      return "<button type='button' class='decision-chip" + selected + "' data-action='" + action + "' data-value='" + escapeHtml(option.value) + "'>" + escapeHtml(option.label) + "</button>";
    }}).join("") + "</div>";
  }}

  function renderLoading() {{
    return "<div class='decision-loading'><div class='decision-loading-dots'><span></span><span></span><span></span></div><h3>Exploring what could fit this property...</h3><p>This short pause is just UI polish while the tool assembles the rule-based project shortlist from your structured answers.</p></div>";
  }}

  function renderReview() {{
    return "<div class='decision-step-copy'><h3>Check the setup before exploring the options</h3><p>This tool is intentionally broad. It is best used to narrow the shortlist, then move into the decision tool for whichever option starts to look serious.</p></div><div class='decision-review-grid'><div class='decision-review-card'><strong>Property</strong><span>" + escapeHtml(propertyLabel()) + "</span></div><div class='decision-review-card'><strong>Plot size</strong><span>" + escapeHtml(spaceLabel()) + "</span></div><div class='decision-review-card'><strong>Useful features</strong><span>" + escapeHtml(featureLabels().join(", ") || "None selected") + "</span></div><div class='decision-review-card'><strong>Local sensitivity</strong><span>" + escapeHtml(constraintLabels().join(", ") || "None selected") + "</span></div></div>";
  }}

  function explorerRuleLink(topOption) {{
    if (topOption && topOption.status === "commonly_permitted") {{
      return {{
        title: "Permitted Development",
        href: "/permitted-development/",
        description: "Open the baseline rights behind the strongest early-fit options this explorer is surfacing.",
      }};
    }}
    return {{
      title: "Planning Permission",
      href: "/planning-permission/",
      description: "Open the main planning hub when the shortlist is already leaning toward a fuller planning route.",
    }};
  }}

  function explorerFaqLink(topOption) {{
    if (topOption && topOption.status === "commonly_permitted") {{
      return {{
        title: "Planning Permission Vs Permitted Development",
        href: "/planning-faq/planning-permission-vs-permitted-development/",
        description: "Useful when the shortlist is strong but the route still sits between the simpler and formal answers.",
      }};
    }}
    return {{
      title: "Do I Need Planning Permission?",
      href: "/planning-faq/do-i-need-planning-permission/",
      description: "Useful when you still need the broader route question answered before you commit to one project option.",
    }};
  }}

  function renderResults() {{
    const result = state.result;
    const filtered = state.filter === "all"
      ? result.options
      : result.options.filter((item) => item.status === state.filter);
    const topOption = result.options[0] || null;

    const cards = filtered.map((item) => {{
      const reasons = item.reasons.length
        ? "<div class='explorer-why'><strong>Why this is showing up</strong><ul>" + item.reasons.map((reason) => "<li>" + escapeHtml(reason) + "</li>").join("") + "</ul></div>"
        : "";
      return "<article class='explorer-card " + item.tone + "'><div class='explorer-card-header'><span class='explorer-status " + item.tone + "'>" + escapeHtml(item.status_label) + "</span><span class='explorer-fit-note'>" + escapeHtml(item.fit_note) + "</span></div><div><h3>" + escapeHtml(item.title) + "</h3><p>" + escapeHtml(item.description) + "</p></div><div class='explorer-meta'><strong>Typical shape</strong><p>" + escapeHtml(item.typical_limits) + "</p></div>" + reasons + "<div class='explorer-card-actions'><a class='explorer-link primary' href='" + escapeHtml(item.guide_href) + "'>" + escapeHtml(item.guide_title) + "</a><a class='explorer-link' href='/tools/planning-decision-tool/'>Check this option</a></div></article>";
    }}).join("");

    const primaryLinks = buildCoreNextLinks({{
      links: CONFIG.default_links || [],
      projectLink: topOption ? {{
        title: topOption.guide_title,
        href: topOption.guide_href,
        description: "Open the project guide for the option currently looking strongest from this property setup.",
      }} : null,
      ruleLink: explorerRuleLink(topOption),
      faqLink: explorerFaqLink(topOption),
      authorityLink: {{
        title: "Local Authorities",
        href: "/councils/",
        description: "Use the authority layer when local controls could change how realistic the shortlisted options really are.",
      }},
    }});
    const links = primaryLinks.map((link) => {{
      return "<a class='explorer-inline-link' href='" + escapeHtml(link.href) + "'><strong>" + escapeHtml(link.title) + "</strong><span>" + escapeHtml(link.description || "") + "</span></a>";
    }}).join("");

    return "<div class='decision-result'><div class='decision-result-banner good'><span class='decision-status'>Possible project options</span><h3>What could be worth exploring next</h3><p>" + escapeHtml(result.summary) + "</p><div class='explorer-summary-strip'><div class='explorer-summary-card'><strong>Property</strong><span>" + escapeHtml(result.property_label) + "</span></div><div class='explorer-summary-card'><strong>Plot size</strong><span>" + escapeHtml(result.space_label) + "</span></div><div class='explorer-summary-card'><strong>Useful features</strong><span>" + escapeHtml(result.feature_labels.join(", ") || "None selected") + "</span></div><div class='explorer-summary-card'><strong>Local sensitivity</strong><span>" + escapeHtml(result.constraint_labels.join(", ") || "None selected") + "</span></div></div></div><div class='explorer-filter-bar'><button type='button' class='decision-chip" + (state.filter === "all" ? " selected" : "") + "' data-action='filter' data-value='all'>All options (" + result.options.length + ")</button><button type='button' class='decision-chip" + (state.filter === "commonly_permitted" ? " selected" : "") + "' data-action='filter' data-value='commonly_permitted'>Commonly permitted (" + result.counts.commonly_permitted + ")</button><button type='button' class='decision-chip" + (state.filter === "depends" ? " selected" : "") + "' data-action='filter' data-value='depends'>Depends (" + result.counts.depends + ")</button><button type='button' class='decision-chip" + (state.filter === "likely_needs" ? " selected" : "") + "' data-action='filter' data-value='likely_needs'>Likely needs permission (" + result.counts.likely_needs + ")</button></div>" + (cards ? "<div class='explorer-grid'>" + cards + "</div>" : "<div class='explorer-empty'><p>No cards match the current filter. Switch the filter to see the full shortlist again.</p></div>") + "<div class='decision-result-card'><h3>What to do next</h3><p>Pick the option that feels closest to your goal, then run it through the decision tool for a more route-specific answer. If you are already leaning toward an application, the risk analyzer is the best follow-on.</p></div><div class='explorer-inline-links'>" + links + "</div>" + renderPostResultExtras({ toolSlug: "what-can-i-build-explorer", guideHref: "/planning-permission/", guideTitle: "Planning permission guide", resultLabel: "Possible project options", nextTool: { href: "/tools/planning-decision-tool/", title: "Use another tool", description: "Check the option you like best in the full planning checker." } }) + "</div>";
  }}

  function renderStepContent() {{
    if (state.loading) {{
      return renderLoading();
    }}
    if (state.result) {{
      return renderResults();
    }}
    if (state.step === 1) {{
      return "<div class='decision-step-copy'><h3>Choose the property you are exploring</h3><p>This tool is deliberately broad. The aim is to show which project types usually look most realistic for this kind of property before you measure anything in detail.</p></div>" + renderChoiceCards(CONFIG.property_types, state.property, "select-property");
    }}
    if (state.step === 2) {{
      return "<div class='decision-step-copy'><h3>Describe the amount of space you have to work with</h3><p>Keep this high level. We only need a broad sense of plot size and whether there are obvious extra spaces already available.</p></div><div class='decision-question'><h4>How much outside space does the property have?</h4>" + renderChoiceCards(CONFIG.space_options, state.space, "select-space") + "</div><div class='decision-question'><h4>Any existing features worth flagging?</h4>" + renderChipChoices(CONFIG.feature_options, state.features, "toggle-feature") + "<p class='decision-question-note'>Optional. Select any that clearly apply.</p></div>";
    }}
    if (state.step === 3) {{
      return "<div class='decision-step-copy'><h3>Add any local sensitivity you already know about</h3><p>This stays optional on purpose. If you know the property is listed, in a conservation area or affected by Article 4, that should change how adventurous the shortlist feels.</p></div><div class='decision-question'><h4>Known local constraints</h4>" + renderChipChoices(CONFIG.constraint_options, state.constraints, "toggle-constraint") + "<p class='decision-question-note'>Leave this blank if you have not checked yet.</p></div>";
    }}
    return renderReview();
  }}

  function renderSidebarSections() {{
    const summaryItems = [
      ["Property", propertyLabel() || "Choose one"],
      ["Plot size", spaceLabel() || "Choose one"],
      ["Useful features", featureLabels().join(", ") || "Optional"],
      ["Local sensitivity", constraintLabels().join(", ") || "Optional"],
    ];

    return {{
      title: "How to use this explorer",
      summaryHtml: summaryItems.map((item) => {{
        return "<div class='decision-summary-item'><strong>" + escapeHtml(item[0]) + "</strong><span>" + escapeHtml(item[1]) + "</span></div>";
      }}).join(""),
      noteHtml: "This tool is about possibilities, not precision. Use it to build a shortlist quickly, then move into the decision tool or project guide for the stricter checks.",
    }};
  }}

  function renderSidebar() {{
    const sections = renderSidebarSections();
    return "<aside class='decision-sidebar'><h3>" + escapeHtml(sections.title) + "</h3><div class='decision-summary-list'>" + sections.summaryHtml + "</div><div class='decision-method-note'>" + sections.noteHtml + "</div></aside>";
  }}

  function renderNav() {{
    if (state.loading || state.result) {{
      return "";
    }}
    const back = state.step > 1 ? "<button type='button' class='button-secondary' data-action='back'>Back</button>" : "<span></span>";
    const isLastStep = state.step === 4;
    const nextLabel = isLastStep ? "Show project options" : "Continue";
    const disabled = requiredForStep(state.step) ? "" : " disabled";
    return "<div class='decision-nav'>" + back + "<button type='button' class='cta' data-action='" + (isLastStep ? "submit" : "next") + "'" + disabled + ">" + nextLabel + "</button></div>";
  }}

  function renderHeaderActions() {{
    return (state.result ? "<button type='button' class='button-secondary' data-action='edit-result'>Edit answers</button>" : "") + "<button type='button' class='button-secondary' data-action='reset'>Start again</button>";
  }}

  function render() {{
    const progress = state.result ? 100 : (state.step / STEP_NAMES.length) * 100;
    const sections = renderSidebarSections();
    renderResponsiveToolShellInto(engine, {{
      kicker: "What Can I Build? Explorer",
      heading: "Explore the project types that usually look most realistic for this property",
      intro: "A broad, visual planning explorer that helps you move from a property setup into a shortlist of projects worth checking next.",
      actionsHtml: renderHeaderActions(),
      progress,
      stepNames: STEP_NAMES,
      currentStep: state.step,
      hasResult: Boolean(state.result),
      contentHtml: renderStepContent() + renderNav(),
      sidebarHtml: renderSidebar(),
      summaryTitle: sections.title,
      summaryHtml: sections.summaryHtml,
      noteHtml: sections.noteHtml,
      summaryHint: "View setup",
    }});
  }}

  engine.addEventListener("click", function (event) {{
    const target = event.target.closest("[data-action]");
    if (!target) {{
      return;
    }}

    const action = target.getAttribute("data-action");
    const value = target.getAttribute("data-value");

    if (action === "select-property") {{
      logToolEvent("click", {{ action, value }});
      state.property = value;
      state.result = null;
      render();
      return;
    }}

    if (action === "select-space") {{
      logToolEvent("click", {{ action, value }});
      state.space = value;
      state.result = null;
      render();
      return;
    }}

    if (action === "toggle-feature") {{
      logToolEvent("click", {{ action, value }});
      state.features = state.features.includes(value)
        ? state.features.filter((item) => item !== value)
        : state.features.concat(value);
      state.result = null;
      render();
      return;
    }}

    if (action === "toggle-constraint") {{
      logToolEvent("click", {{ action, value }});
      state.constraints = state.constraints.includes(value)
        ? state.constraints.filter((item) => item !== value)
        : state.constraints.concat(value);
      state.result = null;
      render();
      return;
    }}

    if (action === "filter") {{
      logToolEvent("click", {{ action, value }});
      state.filter = value || "all";
      render();
      return;
    }}

    if (action === "back") {{
      logToolEvent("click", {{ action, step: state.step }});
      state.step = Math.max(1, state.step - 1);
      render();
      return;
    }}

    if (action === "next") {{
      if (requiredForStep(state.step)) {{
        logToolEvent("click", {{ action, step: state.step }});
        state.step = Math.min(4, state.step + 1);
        render();
      }}
      return;
    }}

    if (action === "submit") {{
      if (!requiredForStep(4)) {{
        return;
      }}
      logToolEvent("submit", {{ action, snapshot: {{
        property: propertyLabel(),
        space: spaceLabel(),
        features: featureLabels(),
        constraints: constraintLabels(),
      }} }});
      state.loading = true;
      render();
      window.setTimeout(function () {{
        state.loading = false;
        state.result = assess();
        state.filter = "all";
        logToolEvent("result", state.result);
        render();
      }}, 650);
      return;
    }}

    if (action === "reset") {{
      logToolEvent("click", {{ action }});
      state = createState();
      render();
      return;
    }}

    if (action === "edit-result") {{
      logToolEvent("click", {{ action }});
      state.result = null;
      state.loading = false;
      state.step = 1;
      render();
    }}
  }});

  render();
}})();
</script>
</div>
""",
        config=WHAT_CAN_I_BUILD_EXPLORER_CONFIG,
        styles=STRUCTURED_TOOL_STYLES,
        replacements={
            "__STRUCTURED_TOOL_UI_HELPERS__": STRUCTURED_TOOL_UI_HELPERS,
            "__NOSCRIPT_FALLBACK__": build_tool_fallback(
                "Explorer loading",
                "If the project explorer does not appear, start with the decision engine or browse the main project guides directly.",
                [
                    {
                        "title": "Planning Decision Engine",
                        "href": "/tools/planning-decision-tool/",
                        "description": "Use the stricter route checker if you already have one project in mind.",
                    },
                    {
                        "title": "House Extensions",
                        "href": "/house-extensions/",
                        "description": "Open the main project guide while the interactive shortlist is unavailable.",
                    },
                ],
            )
        },
    )
