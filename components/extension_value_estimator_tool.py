from components.interactive_tool_renderer import build_tool_fallback, render_inline_tool
from components.planning_tool_styles import STRUCTURED_TOOL_STYLES
from components.structured_tool_ui import STRUCTURED_TOOL_UI_HELPERS
from data.extension_value_estimator import EXTENSION_VALUE_ESTIMATOR_CONFIG


def render_extension_value_estimator_tool():
    return render_inline_tool(
        """
<div class="tool-card decision-engine-card">
<style>
__STRUCTURED_TOOL_STYLES__
#extension-value-estimator .decision-question input[data-numeric="true"]{
width:100%;
padding:14px 16px;
border:1px solid rgba(31,41,55,.12);
border-radius:18px;
background:rgba(255,255,255,.94);
font:inherit;
color:var(--ink);
box-shadow:var(--shadow-soft);
}
#extension-value-estimator .decision-question-note{
margin-top:8px;
font-size:13px;
color:var(--ink-faint);
}
#extension-value-estimator .decision-question-error{
margin-top:8px;
font-size:13px;
font-weight:600;
color:#8b2e2e;
}
#extension-value-estimator .value-estimator-metrics{
display:grid;
grid-template-columns:repeat(auto-fit,minmax(180px,1fr));
gap:12px;
margin:18px 0;
}
#extension-value-estimator .value-estimator-metric{
padding:16px;
border-radius:18px;
background:linear-gradient(180deg,rgba(255,255,255,.98),rgba(247,241,232,.9));
border:1px solid rgba(31,41,55,.08);
box-shadow:var(--shadow-soft);
display:grid;
gap:6px;
}
#extension-value-estimator .value-estimator-metric strong{
font-size:13px;
letter-spacing:.08em;
text-transform:uppercase;
color:var(--accent-text);
}
#extension-value-estimator .value-estimator-metric span{
font-size:1.25rem;
font-weight:700;
color:var(--ink);
}
@media (max-width:767px){
#extension-value-estimator .value-estimator-metrics{grid-template-columns:1fr;}
}
</style>
<div id="extension-value-estimator" class="decision-engine" data-tool-root="extension-value-estimator" data-tool-kind="structured"></div>
<noscript>__NOSCRIPT_FALLBACK__</noscript>
<script>
(function () {
  const CONFIG = __CONFIG__;
  const engine = document.getElementById("extension-value-estimator");
  if (!engine) {
    return;
  }

  const STEP_NAMES = ["Project", "Property", "Route", "Review"];
  const projectMap = Object.fromEntries(CONFIG.project_types.map((item) => [item.value, item]));
  const propertyMap = Object.fromEntries(CONFIG.property_types.map((item) => [item.value, item]));
  const bedroomMap = Object.fromEntries(CONFIG.bedroom_gains.map((item) => [item.value, item]));
  const finishMap = Object.fromEntries(CONFIG.finish_levels.map((item) => [item.value, item]));
  const routeMap = Object.fromEntries(CONFIG.planning_route_confidence.map((item) => [item.value, item]));

  function createState() {
    return {
      step: 1,
      projectType: "",
      currentValue: "450000",
      addedArea: "25",
      propertyType: "",
      bedroomGain: "",
      finishLevel: "",
      planningRouteConfidence: "",
      buildCost: "",
      errors: {},
      loading: false,
      result: null
    };
  }

  let state = createState();

  function escapeHtml(value) {
    return String(value || "")
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;")
      .replace(/'/g, "&#39;");
  }

  function logToolEvent(type, detail) {
    if (window.console && typeof window.console.log === "function") {
      window.console.log("[extension-value-estimator]", type, detail || "");
    }
  }

  function currency(value) {
    return new Intl.NumberFormat("en-GB", { style: "currency", currency: "GBP", maximumFractionDigits: 0 }).format(value || 0);
  }

  function percent(value) {
    return (Math.round((value || 0) * 1000) / 10).toFixed(1) + "%";
  }

  function numberValue(raw) {
    const value = Number(String(raw || "").replace(/[^0-9.]/g, ""));
    return Number.isFinite(value) ? value : 0;
  }

  function digitsOnly(raw) {
    return String(raw || "").replace(/[^0-9]/g, "");
  }

  function clamp(value, minValue, maxValue) {
    if (!Number.isFinite(value)) {
      return minValue;
    }
    return Math.min(Math.max(value, minValue), maxValue);
  }

  function limit(name) {
    return CONFIG.numeric_limits[name];
  }

  function formattedInteger(value) {
    return new Intl.NumberFormat("en-GB", { maximumFractionDigits: 0 }).format(value || 0);
  }

  function project() { return projectMap[state.projectType] || null; }
  function route() { return routeMap[state.planningRouteConfidence] || null; }

  function sizeBand(area) {
    return (CONFIG.size_bands || []).find((item) => area <= item.max_sqm) || CONFIG.size_bands[CONFIG.size_bands.length - 1];
  }

  function requiredForStep(stepNumber) {
    if (stepNumber === 1) {
      return Boolean(state.projectType && numberValue(state.addedArea) > 0);
    }
    if (stepNumber === 2) {
      return Boolean(numberValue(state.currentValue) > 0 && state.propertyType && state.bedroomGain);
    }
    if (stepNumber === 3) {
      return Boolean(state.finishLevel && state.planningRouteConfidence);
    }
    if (stepNumber === 4) {
      return requiredForStep(1) && requiredForStep(2) && requiredForStep(3);
    }
    return false;
  }

  function validateStep(stepNumber) {
    const nextErrors = {};
    if (stepNumber === 1 || stepNumber === 4) {
      const area = numberValue(state.addedArea);
      if (!state.projectType) {
        nextErrors.projectType = "Choose the project type first.";
      }
      if (area < limit("added_area_min") || area > limit("added_area_max")) {
        nextErrors.addedArea = "Use a rough added area between " + formattedInteger(limit("added_area_min")) + " and " + formattedInteger(limit("added_area_max")) + " sqm.";
      }
    }
    if (stepNumber === 2 || stepNumber === 4) {
      const currentValue = numberValue(state.currentValue);
      if (currentValue < limit("current_value_min") || currentValue > limit("current_value_max")) {
        nextErrors.currentValue = "Enter a current value between " + currency(limit("current_value_min")) + " and " + currency(limit("current_value_max")) + ".";
      }
      if (!state.propertyType) {
        nextErrors.propertyType = "Choose the property type.";
      }
      if (!state.bedroomGain) {
        nextErrors.bedroomGain = "Choose the bedroom impact.";
      }
    }
    if (stepNumber === 3 || stepNumber === 4) {
      const buildCost = numberValue(state.buildCost);
      if (!state.finishLevel) {
        nextErrors.finishLevel = "Choose the finish level.";
      }
      if (!state.planningRouteConfidence) {
        nextErrors.planningRouteConfidence = "Choose the planning confidence level.";
      }
      if (state.buildCost && (buildCost < limit("build_cost_min") || buildCost > limit("build_cost_max"))) {
        nextErrors.buildCost = "If you enter build cost, keep it between " + currency(limit("build_cost_min")) + " and " + currency(limit("build_cost_max")) + ".";
      }
    }
    state.errors = nextErrors;
    return Object.keys(nextErrors).length === 0;
  }

__STRUCTURED_TOOL_UI_HELPERS__

  function summaryItems() {
    return [
      { label: "Project type", value: project() ? project().label : "Not chosen yet" },
      { label: "Current value", value: numberValue(state.currentValue) > 0 ? currency(numberValue(state.currentValue)) : "Not entered yet" },
      { label: "Added area", value: numberValue(state.addedArea) > 0 ? numberValue(state.addedArea) + " sqm" : "Not entered yet" },
      { label: "Property type", value: propertyMap[state.propertyType] ? propertyMap[state.propertyType].label : "Not chosen yet" },
      { label: "Bedroom impact", value: bedroomMap[state.bedroomGain] ? bedroomMap[state.bedroomGain].label : "Not chosen yet" },
      { label: "Finish level", value: finishMap[state.finishLevel] ? finishMap[state.finishLevel].label : "Not chosen yet" },
      { label: "Planning route confidence", value: route() ? route().label : "Not chosen yet" },
      { label: "Estimated build cost", value: numberValue(state.buildCost) > 0 ? currency(numberValue(state.buildCost)) : "Not entered" }
    ];
  }

  function renderChoiceGrid(questionId, options, selectedValue) {
    return "<div class='decision-choice-grid'>" + (options || []).map((option) => {
      const selected = option.value === selectedValue ? " selected" : "";
      return "<button type='button' class='decision-choice" + selected + "' data-action='set-answer' data-question-id='" + escapeHtml(questionId) + "' data-value='" + escapeHtml(option.value) + "'><strong>" + escapeHtml(option.label) + "</strong></button>";
    }).join("") + "</div>";
  }

  function renderFieldError(fieldId) {
    return state.errors[fieldId]
      ? "<div class='decision-question-error'>" + escapeHtml(state.errors[fieldId]) + "</div>"
      : "";
  }

  function renderStepOne() {
    return "<div class='decision-step-copy'><h3>Tell the tool what kind of project you are pricing</h3><p>Choose the project family first, then add the rough amount of new space being created.</p></div><div class='decision-question'><h4>Project type</h4>" + renderChoiceGrid("projectType", CONFIG.project_types, state.projectType) + renderFieldError("projectType") + "</div><div class='decision-question'><h4>Added floor area</h4><input type='text' inputmode='numeric' pattern='[0-9]*' enterkeyhint='next' autocomplete='off' data-numeric='true' data-field-id='addedArea' value='" + escapeHtml(state.addedArea) + "' placeholder='e.g. 25'><div class='decision-question-note'>Enter the rough additional internal floor area in square metres.</div>" + renderFieldError("addedArea") + "</div><div class='decision-nav'><button type='button' class='button-secondary' data-action='prev' disabled>Back</button><button type='button' class='cta' data-action='next' " + (requiredForStep(1) ? "" : "disabled") + ">Continue</button></div>";
  }

  function renderStepTwo() {
    return "<div class='decision-step-copy'><h3>Add the property context</h3><p>The current value, property type and bedroom impact do most of the work in the uplift estimate.</p></div><div class='decision-question'><h4>Current estimated property value</h4><input type='text' inputmode='numeric' pattern='[0-9]*' enterkeyhint='next' autocomplete='off' data-numeric='true' data-field-id='currentValue' value='" + escapeHtml(state.currentValue) + "' placeholder='e.g. 425000'><div class='decision-question-note'>Use a rough current value in pounds. This is only used to convert the uplift percentage into a money range.</div>" + renderFieldError("currentValue") + "</div><div class='decision-question'><h4>Property type</h4>" + renderChoiceGrid("propertyType", CONFIG.property_types, state.propertyType) + renderFieldError("propertyType") + "</div><div class='decision-question'><h4>Bedroom impact</h4>" + renderChoiceGrid("bedroomGain", CONFIG.bedroom_gains, state.bedroomGain) + renderFieldError("bedroomGain") + "</div><div class='decision-nav'><button type='button' class='button-secondary' data-action='prev'>Back</button><button type='button' class='cta' data-action='next' " + (requiredForStep(2) ? "" : "disabled") + ">Continue</button></div>";
  }

  function renderStepThree() {
    return "<div class='decision-step-copy'><h3>Finish the estimate settings</h3><p>These final choices shape quality and confidence rather than pretending to be a live market valuation.</p></div><div class='decision-question'><h4>Finish or specification level</h4>" + renderChoiceGrid("finishLevel", CONFIG.finish_levels, state.finishLevel) + renderFieldError("finishLevel") + "</div><div class='decision-question'><h4>Planning route confidence</h4>" + renderChoiceGrid("planningRouteConfidence", CONFIG.planning_route_confidence, state.planningRouteConfidence) + renderFieldError("planningRouteConfidence") + "</div><div class='decision-question'><h4>Estimated build cost (optional)</h4><input type='text' inputmode='numeric' pattern='[0-9]*' enterkeyhint='done' autocomplete='off' data-numeric='true' data-field-id='buildCost' value='" + escapeHtml(state.buildCost) + "' placeholder='e.g. 90000'><div class='decision-question-note'>Optional. If entered, the tool will compare estimated value added against the expected spend.</div>" + renderFieldError("buildCost") + "</div><div class='decision-nav'><button type='button' class='button-secondary' data-action='prev'>Back</button><button type='button' class='cta' data-action='next' " + (requiredForStep(3) ? "" : "disabled") + ">Continue</button></div>";
  }

  function renderReview() {
    const cards = summaryItems().map((item) => "<div class='decision-review-card'><strong>" + escapeHtml(item.label) + "</strong><span>" + escapeHtml(item.value) + "</span></div>").join("");
    return "<div class='decision-step-copy'><h3>Review the inputs and estimate the uplift</h3><p>This is a planning-aware value guide, not a formal valuation. Use it to frame the next question, not to price a deal precisely.</p></div><div class='decision-review-grid'>" + cards + "</div><div class='decision-nav'><button type='button' class='button-secondary' data-action='prev'>Back</button><button type='button' class='cta' data-action='run-check' " + (requiredForStep(4) ? "" : "disabled") + ">Estimate value</button></div>";
  }

  function roiBand(ratio) {
    return (CONFIG.roi_bands || []).find((item) => ratio <= item.max_ratio) || CONFIG.roi_bands[CONFIG.roi_bands.length - 1];
  }

  function assess() {
    const currentProject = project();
    const currentRoute = route();
    const size = sizeBand(numberValue(state.addedArea));
    const propertyType = propertyMap[state.propertyType] || { low_adjust: 0, high_adjust: 0 };
    const bedroomGain = bedroomMap[state.bedroomGain] || { low_adjust: 0, high_adjust: 0 };
    const finishLevel = finishMap[state.finishLevel] || { low_adjust: 0, high_adjust: 0 };

    let lowPct = currentProject.base_low + size.low_adjust + propertyType.low_adjust + bedroomGain.low_adjust + finishLevel.low_adjust + currentRoute.low_adjust;
    let highPct = currentProject.base_high + size.high_adjust + propertyType.high_adjust + bedroomGain.high_adjust + finishLevel.high_adjust + currentRoute.high_adjust;

    lowPct = Math.max(0.01, lowPct);
    highPct = Math.max(lowPct + 0.01, highPct);

    const currentValue = numberValue(state.currentValue);
    const upliftLow = Math.round(currentValue * lowPct);
    const upliftHigh = Math.round(currentValue * highPct);
    const newValueLow = currentValue + upliftLow;
    const newValueHigh = currentValue + upliftHigh;
    const midpointUplift = Math.round((upliftLow + upliftHigh) / 2);
    const buildCost = numberValue(state.buildCost);
    const ratio = buildCost > 0 ? midpointUplift / buildCost : 0;
    const roi = buildCost > 0 ? roiBand(ratio) : null;
    const upliftPerSqm = Math.round(midpointUplift / Math.max(1, numberValue(state.addedArea)));
    const narrativePoints = [];

    if (state.bedroomGain !== "none") {
      narrativePoints.push(CONFIG.result_commentary.bedroom_gain);
    }
    if (buildCost > 0 && upliftHigh < buildCost) {
      narrativePoints.push(CONFIG.result_commentary.high_cost);
    } else if (buildCost > 0 && ratio > 1.1) {
      narrativePoints.push(CONFIG.result_commentary.strong_value);
    }
    if (numberValue(state.addedArea) >= 50 || state.finishLevel === "premium") {
      narrativePoints.push(CONFIG.result_commentary.over_improvement);
    }

    const planningLink = currentRoute.value === "clearer"
      ? { title: "Permitted Development", href: "/permitted-development/", description: "Useful when the simpler planning route still looks credible for this project." }
      : { title: "Planning Permission", href: "/planning-permission/", description: "Use this when the route is no longer obviously simple or still needs a fuller check." };
    const faqLink = buildCost > 0
      ? { title: "Extension Cost Vs Value Added", href: "/planning-faq/extension-cost-vs-value-added/", description: "Use this when the real decision is whether the likely uplift justifies the spend." }
      : { title: "Does An Extension Add Value To A House?", href: "/planning-faq/does-an-extension-add-value-to-a-house/", description: "Read the main guide if you want the value question explained in plainer language." };
    const extraLink = currentRoute.value === "uncertain"
      ? { title: "Planning Decision Tool", href: "/tools/planning-decision-tool/", description: "Use the route checker next if planning uncertainty is still the main reason confidence is lower." }
      : { title: "Local Authorities", href: "/councils/", description: "Open the council layer if local controls could still change how realistic the project feels." };

    return {
      confidenceLabel: currentRoute.confidence_label,
      confidenceTone: currentRoute.confidence_tone,
      confidenceSummary: currentRoute.summary,
      lowPct: lowPct,
      highPct: highPct,
      upliftLow: upliftLow,
      upliftHigh: upliftHigh,
      newValueLow: newValueLow,
      newValueHigh: newValueHigh,
      sizeLabel: size.label,
      midpointUplift: midpointUplift,
      upliftPerSqm: upliftPerSqm,
      roi: roi,
      narrativePoints: narrativePoints,
      projectLink: { title: currentProject.guide_title, href: currentProject.guide_href, description: "Open the matching project guide to see the planning limits and design tripwires behind this estimate." },
      planningLink: planningLink,
      faqLink: faqLink,
      extraLink: extraLink
    };
  }

  function renderResult() {
    const result = state.result;
    const nextLinks = [result.projectLink, result.planningLink, result.faqLink, result.extraLink];
    const metrics = [
      { label: "Estimated uplift", value: currency(result.upliftLow) + " to " + currency(result.upliftHigh) },
      { label: "Estimated uplift %", value: percent(result.lowPct) + " to " + percent(result.highPct) },
      { label: "Estimated new value", value: currency(result.newValueLow) + " to " + currency(result.newValueHigh) },
      { label: CONFIG.metric_labels.sqm_value_label, value: currency(result.upliftPerSqm) },
      { label: "Confidence", value: result.confidenceLabel }
    ].map((item) => "<div class='value-estimator-metric'><strong>" + escapeHtml(item.label) + "</strong><span>" + escapeHtml(item.value) + "</span></div>").join("");

    const roiHtml = result.roi
      ? "<div class='decision-result-card'><h3>Cost versus value added</h3><p><strong>" + escapeHtml(result.roi.label) + ".</strong> " + escapeHtml(result.roi.summary) + "</p><p>Estimated spend entered: " + escapeHtml(currency(numberValue(state.buildCost))) + ".</p></div>"
      : "<div class='decision-result-card'><h3>Cost versus value added</h3><p><strong>" + escapeHtml(CONFIG.metric_labels.roi_none_label) + ".</strong> No build cost was entered, so this result focuses on likely value uplift only. Add a rough spend estimate if you want a simple ROI-style sense-check.</p></div>";
    const narrativeHtml = result.narrativePoints.length
      ? "<div class='decision-result-card'><h3>What stands out most</h3><ul><li>" + result.narrativePoints.map((item) => escapeHtml(item)).join("</li><li>") + "</li></ul></div>"
      : "";

    return "<div class='decision-result'><div class='decision-result-banner " + escapeHtml(result.confidenceTone) + "'><div class='decision-status'>" + escapeHtml(result.confidenceLabel) + "</div><h3>Extension value estimate</h3><p>" + escapeHtml(result.confidenceSummary) + " This tool does not model local market heat or replace a valuation survey.</p></div><div class='value-estimator-metrics'>" + metrics + "</div><div class='decision-result-grid'><div class='decision-result-card'><h3>How the range was shaped</h3><ul><li>" + escapeHtml(project().label) + " base uplift band.</li><li>" + escapeHtml(result.sizeLabel) + " size profile based on " + numberValue(state.addedArea) + " sqm.</li><li>" + escapeHtml((propertyMap[state.propertyType] || {}).label || "Property type") + " and " + escapeHtml((finishMap[state.finishLevel] || {}).label || "finish level") + " modifiers.</li><li>" + escapeHtml((bedroomMap[state.bedroomGain] || {}).label || "Bedroom impact") + " and planning confidence adjustments.</li></ul></div>" + roiHtml + narrativeHtml + "<div class='decision-result-card'><h3>Important caveats</h3><ul><li>This is an early planning-aware guide, not a formal valuation.</li><li>Local market conditions are not modeled in this version.</li><li>Planning uncertainty lowers confidence even if the upside still looks attractive.</li></ul></div></div><div><h3>Best next pages</h3><div class='decision-result-links'>" + nextLinks.map((item) => "<a class='decision-result-link' href='" + escapeHtml(item.href) + "'><strong>" + escapeHtml(item.title) + "</strong><span>" + escapeHtml(item.description) + "</span></a>").join("") + "</div></div>" + renderPostResultExtras({ toolSlug: CONFIG.slug, guideHref: result.projectLink.href, guideTitle: result.projectLink.title, resultLabel: result.confidenceLabel, nextTool: { href: result.extraLink.href, title: result.extraLink.title, description: result.extraLink.description } }) + "<div class='decision-nav'><button type='button' class='button-secondary' data-action='edit-result'>Edit answers</button><button type='button' class='button-secondary' data-action='reset'>Start again</button></div></div>";
  }

  function renderSidebarSections() {
    return {
      title: "Estimator inputs",
      summaryHtml: summaryItems().map((item) => "<div class='decision-summary-item'><strong>" + escapeHtml(item.label) + "</strong><span>" + escapeHtml(item.value) + "</span></div>").join(""),
      noteHtml: "<strong>What this tool is:</strong> a deterministic uplift-range guide that combines project type, size, finish and planning confidence. It does not use live market feeds or postcode-level data."
    };
  }

  function renderHeaderActions() {
    return (state.result ? "<button type='button' class='button-secondary' data-action='edit-result'>Edit answers</button>" : "") + "<button type='button' class='button-secondary' data-action='reset'>Start again</button>";
  }

  function renderStepContent() {
    if (state.loading) {
      return "<div class='decision-loading'><div class='decision-loading-dots'><span></span><span></span><span></span></div><h3>Estimating value uplift...</h3><p>This short pause is only UI polish while the range is assembled.</p></div>";
    }
    if (state.result) {
      return renderResult();
    }
    if (state.step === 1) { return renderStepOne(); }
    if (state.step === 2) { return renderStepTwo(); }
    if (state.step === 3) { return renderStepThree(); }
    return renderReview();
  }

  function render() {
    const sections = renderSidebarSections();
    const progress = state.result ? 100 : (state.step / STEP_NAMES.length) * 100;
    renderResponsiveToolShellInto(engine, {
      kicker: CONFIG.title,
      heading: "Run the extension value estimate",
      intro: "Use this planning-aware calculator to estimate the likely value uplift from an extension-style project before you rely on rough rules of thumb alone.",
      actionsHtml: renderHeaderActions(),
      progress: progress,
      stepNames: STEP_NAMES,
      currentStep: state.step,
      hasResult: Boolean(state.result),
      contentHtml: renderStepContent(),
      sidebarHtml: "<aside class='decision-sidebar'><h3>" + escapeHtml(sections.title) + "</h3><div class='decision-summary-list'>" + sections.summaryHtml + "</div><div class='decision-method-note'>" + sections.noteHtml + "</div></aside>",
      summaryTitle: sections.title,
      summaryHtml: sections.summaryHtml,
      noteHtml: sections.noteHtml,
      summaryHint: "View inputs"
    });
  }

  engine.addEventListener("click", function (event) {
    const target = event.target.closest("[data-action]");
    if (!target) {
      return;
    }
    const action = target.getAttribute("data-action");
    const questionId = target.getAttribute("data-question-id") || "";
    const value = target.getAttribute("data-value") || "";

    if (action === "set-answer") {
      logToolEvent("click", { action: action, questionId: questionId, value: value });
      if (questionId === "projectType") { state.projectType = value; }
      if (questionId === "propertyType") { state.propertyType = value; }
      if (questionId === "bedroomGain") { state.bedroomGain = value; }
      if (questionId === "finishLevel") { state.finishLevel = value; }
      if (questionId === "planningRouteConfidence") { state.planningRouteConfidence = value; }
      delete state.errors[questionId];
      state.result = null;
      render();
      return;
    }
    if (action === "next" && state.step < STEP_NAMES.length) {
      if (validateStep(state.step) && requiredForStep(state.step)) {
        state.step += 1;
      }
      render();
      return;
    }
    if (action === "prev" && state.step > 1) {
      state.step -= 1;
      render();
      return;
    }
    if (action === "run-check") {
      if (!validateStep(STEP_NAMES.length) || !requiredForStep(STEP_NAMES.length)) {
        render();
        return;
      }
      logToolEvent("submit", { action: action, snapshot: summaryItems() });
      state.loading = true;
      state.result = null;
      render();
      window.setTimeout(function () {
        state.loading = false;
        state.result = assess();
        render();
      }, 350);
      return;
    }
    if (action === "edit-result") {
      state.result = null;
      state.loading = false;
      state.step = STEP_NAMES.length;
      render();
      return;
    }
    if (action === "reset") {
      state = createState();
      render();
    }
  });

  engine.addEventListener("input", function (event) {
    const target = event.target;
    if (!target || !target.getAttribute) {
      return;
    }
    const fieldId = target.getAttribute("data-field-id");
    if (!fieldId) {
      return;
    }
    if (fieldId === "currentValue") { state.currentValue = digitsOnly(target.value); }
    if (fieldId === "addedArea") { state.addedArea = digitsOnly(target.value); }
    if (fieldId === "buildCost") { state.buildCost = digitsOnly(target.value); }
    delete state.errors[fieldId];
    state.result = null;
    render();
  });

  render();
})();
</script>
</div>
""",
        config=EXTENSION_VALUE_ESTIMATOR_CONFIG,
        styles=STRUCTURED_TOOL_STYLES,
        replacements={
            "__STRUCTURED_TOOL_UI_HELPERS__": STRUCTURED_TOOL_UI_HELPERS,
            "__NOSCRIPT_FALLBACK__": build_tool_fallback(
                "Interactive estimator loading",
                "If the interactive estimator does not appear, open the value guidance pages or the planning tools while JavaScript is unavailable.",
                [
                    {"title": "Does An Extension Add Value To A House?", "href": "/planning-faq/does-an-extension-add-value-to-a-house/", "description": "Read the main value explainer."},
                    {"title": "Planning Decision Tool", "href": "/tools/planning-decision-tool/", "description": "Check the route if planning certainty is still the main blocker."},
                ],
            ),
        },
    )
