from components.interactive_tool_renderer import build_tool_fallback, render_inline_tool
from components.planning_tool_styles import STRUCTURED_TOOL_STYLES
from components.structured_tool_ui import STRUCTURED_TOOL_UI_HELPERS
from data.planning_decision_engine import DECISION_ENGINE_CONFIG


def render_planning_decision_tool():
    parts = []
    parts.append(
        """
<div class="tool-card decision-engine-card">
<style>
__STRUCTURED_TOOL_STYLES__
.planning-decision-shell-desktop{display:block;}
.planning-decision-shell-mobile{display:none;}
.planning-decision-desktop-shell{padding:30px;}
.planning-decision-mobile-shell{display:grid;gap:14px;padding:18px;}
.planning-decision-mobile-header,.planning-decision-mobile-panel,.planning-decision-mobile-summary{padding:18px;background:rgba(255,255,255,.94);border:1px solid rgba(31,41,55,.08);border-radius:22px;box-shadow:var(--shadow-soft);}
.planning-decision-mobile-header{display:grid;gap:14px;background:linear-gradient(180deg,rgba(255,255,255,.98),rgba(247,241,232,.92));}
.planning-decision-mobile-header h2{margin-bottom:8px;font-size:clamp(1.5rem,7vw,2rem);line-height:1.08;}
.planning-decision-mobile-actions{display:grid;gap:10px;}
.planning-decision-mobile-actions > *{width:100%;min-height:48px;margin:0;}
.planning-decision-mobile-panel{display:grid;gap:18px;background:linear-gradient(180deg,rgba(255,255,255,.98),rgba(255,255,255,.9));}
.planning-decision-mobile-step-intro{display:grid;gap:10px;padding:15px 16px;background:linear-gradient(135deg,rgba(247,241,232,.74),rgba(255,255,255,.96));border:1px solid rgba(31,41,55,.06);border-radius:18px;}
.planning-decision-mobile-step-intro strong{font-size:13px;letter-spacing:.08em;text-transform:uppercase;color:var(--accent-text);}
.planning-decision-mobile-step-intro p{margin:0;color:var(--ink-soft);line-height:1.55;}
.planning-decision-mobile-summary{display:grid;gap:14px;background:linear-gradient(180deg,rgba(255,255,255,.96),rgba(247,241,232,.86));}
.planning-decision-mobile-summary h3{margin:0;}
.planning-decision-mobile-summary .decision-summary-list{margin-bottom:0;}
.planning-decision-mobile-shell,.planning-decision-mobile-shell *{box-sizing:border-box;}
.planning-decision-mobile-shell > *,.planning-decision-mobile-panel > *,.planning-decision-mobile-summary > *,.planning-decision-mobile-shell .decision-result > *{min-width:0;}
.planning-decision-mobile-shell .decision-step-labels{gap:8px;grid-template-columns:1fr;}
.planning-decision-mobile-shell .decision-step-label{display:grid;gap:4px;padding:13px 14px;align-content:start;}
.planning-decision-mobile-shell .decision-step-number,.planning-decision-mobile-shell .decision-step-name{display:block;line-height:1.25;}
.planning-decision-mobile-shell .decision-choice-grid,.planning-decision-mobile-shell .decision-binary-grid,.planning-decision-mobile-shell .decision-review-grid,.planning-decision-mobile-shell .decision-result-grid,.planning-decision-mobile-shell .decision-result-links,.planning-decision-mobile-shell .decision-chip-row,.planning-decision-mobile-shell .decision-follow-up-grid{grid-template-columns:1fr !important;}
.planning-decision-mobile-shell .decision-choice,.planning-decision-mobile-shell .decision-review-card,.planning-decision-mobile-shell .decision-result-card,.planning-decision-mobile-shell .decision-result-link,.planning-decision-mobile-shell .decision-summary-item,.planning-decision-mobile-shell .decision-chip,.planning-decision-mobile-shell .decision-follow-up-link{width:100%;max-width:100%;}
.planning-decision-mobile-shell .decision-nav{display:flex;flex-direction:column;gap:10px;align-items:stretch;}
.planning-decision-mobile-shell .decision-nav > *{width:100%;flex:1 1 auto;}
.planning-decision-mobile-shell .decision-nav span{display:none;}
.planning-decision-mobile-shell .decision-nav .cta,.planning-decision-mobile-shell .decision-nav .button-secondary,.planning-decision-mobile-shell .decision-email-button{width:100%;min-height:52px;padding:14px 18px;}
.planning-decision-mobile-shell .decision-step-copy,.planning-decision-mobile-shell .decision-question,.planning-decision-mobile-shell .decision-result-banner,.planning-decision-mobile-shell .decision-result-card,.planning-decision-mobile-shell .decision-result-link,.planning-decision-mobile-shell .decision-loading,.planning-decision-mobile-shell .decision-follow-up-card{padding:16px;}
.planning-decision-mobile-shell .decision-email-capture{grid-template-columns:1fr;}
.planning-decision-mobile-shell .decision-step-copy,.planning-decision-mobile-shell .decision-question,.planning-decision-mobile-shell .decision-result,.planning-decision-mobile-shell .decision-result-banner,.planning-decision-mobile-shell .decision-result-card,.planning-decision-mobile-shell .decision-result-link,.planning-decision-mobile-shell .decision-summary-item,.planning-decision-mobile-shell .decision-review-card,.planning-decision-mobile-shell .decision-follow-up-card,.planning-decision-mobile-shell .decision-method-note,.planning-decision-mobile-shell .decision-inline-note{overflow:visible;position:static;transform:none;}
.planning-decision-mobile-shell .decision-step-copy p,.planning-decision-mobile-shell .decision-question p,.planning-decision-mobile-shell .decision-result-banner p,.planning-decision-mobile-shell .decision-result-card p,.planning-decision-mobile-shell .decision-result-card li,.planning-decision-mobile-shell .decision-result-link span,.planning-decision-mobile-shell .decision-summary-item span,.planning-decision-mobile-shell .decision-review-card span,.planning-decision-mobile-shell .decision-follow-up-link span,.planning-decision-mobile-shell .decision-method-note,.planning-decision-mobile-shell .decision-question-note,.planning-decision-mobile-shell .decision-inline-note,.planning-decision-mobile-shell .decision-email-note{display:block;max-width:100%;margin:0;line-height:1.58;white-space:normal;overflow-wrap:anywhere;word-break:normal;}
.planning-decision-mobile-shell .decision-summary-list,.planning-decision-mobile-shell .decision-result,.planning-decision-mobile-shell .decision-result-grid,.planning-decision-mobile-shell .decision-result-links,.planning-decision-mobile-shell .decision-review-grid,.planning-decision-mobile-shell .decision-follow-up,.planning-decision-mobile-shell .decision-follow-up-grid{display:grid;gap:12px;}
.planning-decision-mobile-shell .decision-summary-item,.planning-decision-mobile-shell .decision-review-card,.planning-decision-mobile-shell .decision-result-card{display:grid;gap:8px;align-content:start;}
.planning-decision-mobile-shell .decision-summary-item strong,.planning-decision-mobile-shell .decision-review-card strong,.planning-decision-mobile-shell .decision-result-card h3,.planning-decision-mobile-shell .decision-result-link strong,.planning-decision-mobile-shell .decision-follow-up-link strong{margin:0;line-height:1.32;}
.planning-decision-mobile-shell .decision-summary-item span,.planning-decision-mobile-shell .decision-review-card span{padding-top:0;}
.planning-decision-mobile-shell .decision-result-card ul{display:grid;gap:8px;margin:0;padding-left:18px;}
.planning-decision-mobile-shell .decision-chip-row{align-items:stretch;}
.planning-decision-mobile-shell .decision-chip{min-height:50px;padding:12px 14px;border-radius:18px;white-space:normal;line-height:1.4;}
.planning-decision-mobile-shell .decision-choice{display:grid;gap:6px;align-content:start;}
.planning-decision-mobile-shell .decision-choice strong,.planning-decision-mobile-shell .decision-step-name{font-size:14px;}
.planning-decision-mobile-shell .decision-result-banner h3{font-size:clamp(1.28rem,6vw,1.72rem);line-height:1.12;}
.planning-decision-mobile-shell .decision-result-banner p{max-width:none;}
@media (max-width:767px){.planning-decision-shell-desktop{display:none !important;}.planning-decision-shell-mobile{display:block !important;}}
@media (max-width:960px){.planning-decision-desktop-shell{padding:22px;}}
@media (max-width:420px){.planning-decision-mobile-shell{padding:16px;gap:12px;}.planning-decision-mobile-header,.planning-decision-mobile-panel,.planning-decision-mobile-summary{padding:16px;}.planning-decision-mobile-header h2{font-size:clamp(1.38rem,7.6vw,1.82rem);}.planning-decision-mobile-shell .decision-step-copy,.planning-decision-mobile-shell .decision-question,.planning-decision-mobile-shell .decision-result-banner,.planning-decision-mobile-shell .decision-result-card,.planning-decision-mobile-shell .decision-result-link,.planning-decision-mobile-shell .decision-loading,.planning-decision-mobile-shell .decision-follow-up-card,.planning-decision-mobile-shell .decision-summary-item,.planning-decision-mobile-shell .decision-review-card{padding:14px;}.planning-decision-mobile-shell .decision-choice,.planning-decision-mobile-shell .decision-chip{padding:13px;}.planning-decision-mobile-shell .decision-choice span,.planning-decision-mobile-shell .decision-summary-item span,.planning-decision-mobile-shell .decision-review-card span,.planning-decision-mobile-shell .decision-result-link span,.planning-decision-mobile-shell .decision-method-note,.planning-decision-mobile-shell .decision-question-note,.planning-decision-mobile-shell .decision-email-note{font-size:13px;line-height:1.55;}}
</style>
<div id="planning-decision-engine" class="decision-engine" data-tool-root="planning-decision-tool" data-tool-kind="structured"></div>
<noscript>__NOSCRIPT_FALLBACK__</noscript>
<script>
(function () {
  const CONFIG = __CONFIG__;
  const engine = document.getElementById("planning-decision-engine");
  if (!engine) {
    return;
  }

  const STATUS_RANK = { likely_pd: 0, may_need: 1, likely_needs: 2 };
  const STATUS_COPY = {
    likely_pd: { label: "Likely permitted development", tone: "good", summary(project) { return "Based on these answers, this " + project.label.toLowerCase() + " still looks like the kind of project that can often stay within the normal householder route."; } },
    may_need: { label: "May need planning permission", tone: "warn", summary(project) { return "Based on these answers, this " + project.label.toLowerCase() + " is no longer an obvious permitted development case and needs a closer check."; } },
    likely_needs: { label: "Likely needs planning permission", tone: "danger", summary(project) { return "Based on these answers, this " + project.label.toLowerCase() + " is pushing outside the simpler route in many cases."; } },
    depends: { label: "Depends on additional local constraints", tone: "info", summary(project) { return "The baseline answer for this " + project.label.toLowerCase() + " is being changed by local designations or missing local detail, so the local layer matters before you rely on it."; } },
  };
  const STEP_NAMES = ["Project", "Property", "Details", "Review"];
  const projectMap = Object.fromEntries(CONFIG.projects.map((project) => [project.id, project]));

  function createState() {
    return { step: 1, project: "", property: "", previousWork: "", constraints: [], detailAnswers: {}, loading: false, result: null };
  }

  let state = createState();

  function escapeHtml(value) {
    return String(value || "").replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;").replace(/'/g, "&#39;");
  }

  function project() { return projectMap[state.project] || null; }
  function optionLabel(options, value) { const match = (options || []).find((item) => item.value === value); return match ? match.label : ""; }
  function answerLabel(question, value) { if (!question) { return value === "yes" ? "Yes" : value === "no" ? "No" : ""; } return optionLabel(question.options || [], value); }
  function propertyLabel() { return optionLabel(CONFIG.property_types, state.property); }
  function previousWorkLabel() { return optionLabel(CONFIG.previous_work_options, state.previousWork); }
  function constraintLabels() { return state.constraints.map((value) => optionLabel(CONFIG.constraint_options, value)).filter(Boolean); }
  function isHouseholderProject(projectId) { return ["rear-extension", "side-extension", "loft-conversion", "garden-room", "porch", "garage-conversion"].includes(projectId); }
  function logToolEvent(type, detail) { if (window.console && typeof window.console.log === "function") { window.console.log("[planning-decision-tool]", type, detail || ""); } }

  function requiredForStep(stepNumber) {
    const currentProject = project();
    if (stepNumber === 1) { return Boolean(state.project); }
    if (stepNumber === 2) { return Boolean(state.property && state.previousWork); }
    if (stepNumber === 3) {
      if (!currentProject) { return false; }
      const answers = state.detailAnswers;
      if (!answers[currentProject.primary_question.id]) { return false; }
      if (currentProject.secondary_question && !answers[currentProject.secondary_question.id]) { return false; }
      return (currentProject.binary_questions || []).every((question) => Boolean(answers[question.id]));
    }
    if (stepNumber === 4) { return requiredForStep(1) && requiredForStep(2) && requiredForStep(3); }
    return false;
  }

__STRUCTURED_TOOL_UI_HELPERS__

  function pushUnique(target, text) { if (text && !target.includes(text)) { target.push(text); } }
  function pushLink(result, item) { if (item && item.href && !result.links.some((link) => link.href === item.href)) { result.links.push(item); } }
  function raiseMinStatus(result, status) { if (STATUS_RANK[status] > STATUS_RANK[result.minStatus]) { result.minStatus = status; } }
  function hasConstraint(key) { return state.constraints.includes(key); }

  function buildResultBase(currentProject) {
    const base = {
      hardNeed: false,
      localDependency: false,
      caution: 0,
      minStatus: "likely_pd",
      reasons: [],
      changes: [...(currentProject.common_changes || [])],
      checks: [...(currentProject.next_checks || [])],
      links: [],
    };

    pushLink(base, { title: currentProject.guide_title, href: currentProject.guide_href, description: "Open the main guide for the measurement rules and common tripwires behind this result." });
    (currentProject.related_pages || []).forEach((item) => pushLink(base, item));
    (CONFIG.default_links || []).forEach((item) => pushLink(base, item));
    return base;
  }
"""
    )
    parts.append(
        """
  function applyGlobalChecks(currentProject, result) {
    if (state.property === "flat") {
      if (isHouseholderProject(currentProject.id)) {
        result.hardNeed = true;
        pushUnique(result.reasons, "Flats and maisonettes usually do not benefit from the normal householder permitted development rights used for this kind of project.");
      } else {
        result.caution += 1;
        raiseMinStatus(result, "may_need");
        pushUnique(result.reasons, "Flats and maisonettes often have a tighter route than houses, so the simple answer is less reliable.");
      }
    }

    if (state.property === "other") {
      result.localDependency = true;
      pushUnique(result.reasons, "This tool is tuned to common home projects, so unusual building types need a closer project-specific check.");
    }

    if (state.previousWork === "yes" && isHouseholderProject(currentProject.id)) {
      result.caution += 1;
      raiseMinStatus(result, "may_need");
      pushUnique(result.reasons, "Previous extensions or roof changes can use up allowances that this quicker answer depends on.");
    }

    if (hasConstraint("listed")) {
      result.hardNeed = true;
      pushUnique(result.reasons, "Listed building controls usually mean the project needs a more formal consent route.");
      pushLink(result, { title: "Listed Buildings", href: "/listed-buildings/", description: "Use this when heritage controls are likely to override the normal householder route." });
      pushUnique(result.checks, "Check whether listed building consent is needed alongside planning permission.");
    }

    if (hasConstraint("conservation")) {
      result.localDependency = true;
      pushUnique(result.reasons, "Conservation area controls can tighten what is possible or change how the design is judged.");
      pushLink(result, { title: "Conservation Areas", href: "/conservation-areas/", description: "Helpful when heritage controls are likely to change the baseline answer." });
    }

    if (hasConstraint("article4")) {
      result.localDependency = true;
      pushUnique(result.reasons, "An Article 4 direction can remove permitted development rights that would normally be available.");
      pushLink(result, { title: "Article 4 Restrictions", href: "/article-4/", description: "Open this if local directions may remove the normal PD route." });
    }

    if (hasConstraint("unsure")) {
      result.localDependency = true;
      pushUnique(result.reasons, "The answer depends on whether local designations apply, so that local layer needs checking first.");
      pushUnique(result.checks, "Use the council or local authority page to confirm whether conservation area, Article 4 or heritage controls apply.");
    }
  }

  function assessProjectSpecific(currentProject, result) {
    const answers = state.detailAnswers;

    switch (currentProject.id) {
      case "rear-extension":
        if (answers.form_band === "two-storey") {
          result.hardNeed = true;
          pushUnique(result.reasons, "A two-storey rear extension is a much harder fit for the simple householder route.");
        }
        if (answers.size_band === "large") {
          result.hardNeed = true;
          pushUnique(result.reasons, "The depth looks clearly beyond the usual rear extension limits.");
        }
        if (answers.size_band === "borderline") {
          result.caution += 1;
          raiseMinStatus(result, "may_need");
          pushUnique(result.reasons, "The depth looks close to the normal rear extension threshold.");
        }
        if (answers.form_band === "single-tall") {
          result.caution += 1;
          raiseMinStatus(result, "may_need");
          pushUnique(result.reasons, "Height can become the deciding factor even on a single-storey rear extension.");
        }
        if (answers.near_boundary === "yes") {
          result.caution += 1;
          raiseMinStatus(result, "may_need");
          pushUnique(result.reasons, "Being close to a boundary makes the height check more sensitive.");
        }
        break;

      case "side-extension":
        if (answers.forward_of_house === "yes") {
          result.hardNeed = true;
          pushUnique(result.reasons, "Projecting forward of the main front wall often moves a side extension out of the simple route.");
        }
        if (answers.form_band === "two-storey") {
          result.hardNeed = true;
          pushUnique(result.reasons, "A two-storey side extension usually needs a more formal planning route.");
        }
        if (answers.size_band === "wide") {
          result.hardNeed = true;
          pushUnique(result.reasons, "The width looks beyond the usual side extension comfort zone.");
        }
        if (answers.size_band === "borderline") {
          result.caution += 1;
          raiseMinStatus(result, "may_need");
          pushUnique(result.reasons, "The width looks close to the point where side extensions become borderline.");
        }
        if (answers.form_band === "single-tall") {
          result.caution += 1;
          raiseMinStatus(result, "may_need");
          pushUnique(result.reasons, "A taller side extension needs a closer height and design check.");
        }
        if (answers.near_boundary === "yes") {
          result.caution += 1;
          raiseMinStatus(result, "may_need");
          pushUnique(result.reasons, "Boundary proximity makes the neighbour and height rules more important.");
        }
        break;

      case "loft-conversion":
        if (answers.roof_change === "major") {
          result.hardNeed = true;
          pushUnique(result.reasons, "A major roof reshaping project is unlikely to stay inside the simplest loft route.");
        }
        if (answers.front_facing === "yes") {
          result.hardNeed = true;
          pushUnique(result.reasons, "A front-facing dormer or major front roof change often moves the answer toward planning permission.");
        }
        if (answers.roof_change === "moderate") {
          result.caution += 1;
          raiseMinStatus(result, "may_need");
          pushUnique(result.reasons, "A noticeable roof enlargement usually needs a more detailed volume and design check.");
        }
        break;

      case "garden-room":
        if (answers.use_band === "sleeping") {
          result.hardNeed = true;
          pushUnique(result.reasons, "Sleeping or living use makes a garden room much less likely to stay within the simpler outbuilding route.");
        }
        if (answers.forward_of_house === "yes") {
          result.hardNeed = true;
          pushUnique(result.reasons, "An outbuilding in front of the main house wall is usually a harder planning route.");
        }
        if (answers.height_band === "high") {
          result.hardNeed = true;
          pushUnique(result.reasons, "The height looks beyond the usual outbuilding envelope.");
        }
        if (answers.height_band === "medium") {
          result.caution += 1;
          raiseMinStatus(result, "may_need");
          pushUnique(result.reasons, "The height looks close to the limit where exact measurement matters.");
        }
        if (answers.near_boundary === "yes") {
          result.caution += 1;
          raiseMinStatus(result, "may_need");
          pushUnique(result.reasons, "Being near a boundary makes the height threshold much more important.");
        }
        break;

      case "porch":
        if (answers.footprint_band === "large") {
          result.hardNeed = true;
          pushUnique(result.reasons, "The porch looks larger than the usual small-porch allowance.");
        }
        if (answers.height_band === "high") {
          result.hardNeed = true;
          pushUnique(result.reasons, "A taller porch often falls outside the simpler route.");
        }
        if (answers.within_two_metres_highway === "yes") {
          result.hardNeed = true;
          pushUnique(result.reasons, "Being within about 2 metres of a highway or front boundary is a common porch tripwire.");
        }
        if (answers.footprint_band === "medium") {
          result.caution += 1;
          raiseMinStatus(result, "may_need");
          pushUnique(result.reasons, "The footprint is close enough to the normal limit that the exact area matters.");
        }
        break;

      case "garage-conversion":
        if (answers.change_band === "major") {
          result.hardNeed = true;
          pushUnique(result.reasons, "Major external change or extra footprint makes a garage conversion much less likely to stay inside the simple route.");
        }
        if (answers.change_band === "minor") {
          result.caution += 1;
          raiseMinStatus(result, "may_need");
          pushUnique(result.reasons, "Visible external changes usually need a closer planning check than internal-only conversions.");
        }
        if (answers.parking_band === "affected") {
          result.caution += 1;
          raiseMinStatus(result, "may_need");
          pushUnique(result.reasons, "Parking and access can become the planning issue even where the conversion itself looks simple.");
        }
        break;

      case "driveway":
        if (answers.front_garden === "yes" && answers.surface_band === "sealed" && answers.area_band === "large") {
          result.hardNeed = true;
          pushUnique(result.reasons, "A larger impermeable front garden surface draining toward the road often needs planning permission.");
        } else if (answers.front_garden === "yes" && (answers.surface_band !== "permeable" || answers.area_band === "large")) {
          result.caution += 1;
          raiseMinStatus(result, "may_need");
          pushUnique(result.reasons, "Front garden hard surfacing needs a closer drainage check before the answer is safe.");
        } else if (answers.surface_band === "sealed") {
          result.caution += 1;
          raiseMinStatus(result, "may_need");
          pushUnique(result.reasons, "Impermeable surfacing still needs checking even if the front garden point is less obvious.");
        }
        break;

      case "fences-walls":
        if (answers.location_band === "road" && answers.height_band !== "low") {
          result.hardNeed = true;
          pushUnique(result.reasons, "Height next to a road or footpath is usually the deciding fence and wall tripwire.");
        } else if (answers.location_band === "side-rear" && answers.height_band === "high") {
          result.hardNeed = true;
          pushUnique(result.reasons, "A boundary structure over about 2 metres high often needs planning permission.");
        }
        break;

      case "dropped-kerb":
        raiseMinStatus(result, "may_need");
        pushUnique(result.reasons, "Dropped kerbs usually involve a highways process even when planning permission is not the only consent route.");
        if (answers.road_band === "classified") {
          result.hardNeed = true;
          pushUnique(result.reasons, "A busier or classified road makes a formal route much more likely.");
        }
        if (answers.road_band === "uncertain") {
          result.caution += 1;
          pushUnique(result.reasons, "Road status is not clear yet, which makes the planning route harder to call.");
        }
        if (answers.access_band === "awkward") {
          result.caution += 1;
          pushUnique(result.reasons, "A tight, shared or awkward frontage needs a closer highways and planning review.");
        }
        break;
    }
  }

  function finalizeResult(currentProject, result) {
    let status = "likely_pd";
    if (result.hardNeed) {
      status = "likely_needs";
    } else if (result.localDependency) {
      status = "depends";
    } else if (result.caution > 0 || result.minStatus !== "likely_pd") {
      status = "may_need";
    }

    if (status !== "depends" && STATUS_RANK[result.minStatus] > STATUS_RANK[status]) {
      status = result.minStatus;
    }

    if (!result.reasons.length) {
      pushUnique(result.reasons, "The project details look comfortably inside the common triggers this tool checks first.");
    }

    return {
      status,
      reasons: result.reasons.slice(0, 4),
      changes: result.changes.slice(0, 4),
      checks: result.checks.slice(0, 4),
      links: result.links.slice(0, 6),
      summary: STATUS_COPY[status].summary(currentProject),
    };
  }

  function assess() {
    const currentProject = project();
    const result = buildResultBase(currentProject);
    applyGlobalChecks(currentProject, result);
    assessProjectSpecific(currentProject, result);
    return finalizeResult(currentProject, result);
  }
"""
    )
    parts.append(
        """
  function summaryItems() {
    const currentProject = project();
    if (!currentProject) {
      return [];
    }

    const items = [
      { label: "Project", value: currentProject.label },
      { label: "Property", value: propertyLabel() || "Not chosen yet" },
      { label: "Previous additions", value: previousWorkLabel() || "Not chosen yet" },
      { label: "Constraints", value: constraintLabels().length ? constraintLabels().join(", ") : "None selected" },
    ];
    const answers = state.detailAnswers;

    if (currentProject.primary_question) {
      items.push({ label: currentProject.primary_question.label, value: answerLabel(currentProject.primary_question, answers[currentProject.primary_question.id]) || "Not chosen yet" });
    }
    if (currentProject.secondary_question) {
      items.push({ label: currentProject.secondary_question.label, value: answerLabel(currentProject.secondary_question, answers[currentProject.secondary_question.id]) || "Not chosen yet" });
    }
    (currentProject.binary_questions || []).forEach((question) => {
      items.push({ label: question.label, value: answers[question.id] === "yes" ? "Yes" : answers[question.id] === "no" ? "No" : "Not chosen yet" });
    });
    return items;
  }

  function renderChoiceGrid(options, selectedValue, action, extraAttributes) {
    return "<div class='decision-choice-grid'>" + options.map((option) => {
      const optionValue = option.value || option.id || "";
      const selected = optionValue === selectedValue ? " selected" : "";
      return "<button type='button' class='decision-choice" + selected + "' data-action='" + action + "' data-value='" + escapeHtml(optionValue) + "'" + (extraAttributes || "") + "><strong>" + escapeHtml(option.label) + "</strong><span>" + escapeHtml(option.hint || "") + "</span></button>";
    }).join("") + "</div>";
  }

  function renderBinaryQuestion(question, currentValue) {
    return "<div class='decision-question'><h4>" + escapeHtml(question.label) + "</h4>" + renderChoiceGrid([{ value: "yes", label: "Yes", hint: question.help || "Yes." }, { value: "no", label: "No", hint: question.help || "No." }], currentValue, "set-binary", " data-question-id='" + escapeHtml(question.id) + "'") + "</div>";
  }

  function decisionFaqLink(statusKey) {
    if (statusKey === "likely_pd" || statusKey === "depends") {
      return {
        title: "Lawful Development Certificate Vs Planning Permission",
        href: "/planning-faq/lawful-development-certificate-vs-planning-permission/",
        description: "Useful when the route still looks simpler but written proof may be worth securing before work starts.",
      };
    }
    return {
      title: "Planning Permission Vs Permitted Development",
      href: "/planning-faq/planning-permission-vs-permitted-development/",
      description: "Useful when the result sits between the simpler route and a fuller planning application.",
    };
  }

  function decisionRuleLink(statusKey) {
    if (statusKey === "likely_pd") {
      return {
        title: "Permitted Development",
        href: "/permitted-development/",
        description: "Open the baseline rights behind the simpler route this result is testing.",
      };
    }
    return {
      title: "Planning Permission",
      href: "/planning-permission/",
      description: "Open the formal-route hub when the project is pushing beyond the simpler planning answer.",
    };
  }

  function renderStepContent() {
    const currentProject = project();

    if (state.loading) {
      return "<div class='decision-loading'><div class='decision-loading-dots'><span></span><span></span><span></span></div><h3>Checking your project details against the rule-based guidance...</h3><p>This is a short UI pause so the result appears in sequence. The answer itself is coming from structured rules, not free-text AI.</p></div>";
    }

    if (state.result && currentProject) {
      const status = STATUS_COPY[state.result.status];
      const primaryLinks = buildCoreNextLinks({
        links: state.result.links,
        projectLink: { title: currentProject.guide_title, href: currentProject.guide_href, description: "Open the main project guide behind this route result." },
        ruleLink: decisionRuleLink(state.result.status),
        faqLink: decisionFaqLink(state.result.status),
        authorityLink: {
          title: "Local Authorities",
          href: "/councils/",
          description: state.result.status === "depends"
            ? "Use the local authority layer because local controls are changing the baseline answer here."
            : "Use the authority layer if the site is sensitive or the result still feels borderline.",
        },
      });
      return "<div class='decision-result'><div class='decision-result-banner " + status.tone + "'><div class='decision-status'>" + escapeHtml(status.label) + "</div><h3>" + escapeHtml(currentProject.label) + "</h3><p>" + escapeHtml(state.result.summary) + "</p></div><div class='decision-result-grid'><div class='decision-result-card'><h3>Why this result was reached</h3><ul>" + state.result.reasons.map((item) => "<li>" + escapeHtml(item) + "</li>").join("") + "</ul></div><div class='decision-result-card'><h3>What commonly changes the answer</h3><ul>" + state.result.changes.map((item) => "<li>" + escapeHtml(item) + "</li>").join("") + "</ul></div><div class='decision-result-card'><h3>What to check next</h3><ul>" + state.result.checks.map((item) => "<li>" + escapeHtml(item) + "</li>").join("") + "</ul></div></div><div><h3>Best next pages</h3><div class='decision-result-links'>" + primaryLinks.map((item) => "<a class='decision-result-link' href='" + escapeHtml(item.href) + "'><strong>" + escapeHtml(item.title) + "</strong><span>" + escapeHtml(item.description || "Open the next guide.") + "</span></a>").join("") + "</div></div>" + renderPostResultExtras({ toolSlug: "planning-decision-tool", guideHref: currentProject.guide_href, guideTitle: currentProject.guide_title, resultLabel: status.label, nextTool: { href: "/tools/planning-rejection-risk-analyzer/", title: "Use another tool", description: "Move into the rejection risk analyzer to pressure-test the same project." } }) + "<div class='decision-nav'><button type='button' class='button-secondary' data-action='edit-result'>Edit answers</button><button type='button' class='button-secondary' data-action='reset'>Start again</button></div></div>";
    }

    if (state.step === 1) {
      return "<div class='decision-step-copy'><h3>What kind of project are you checking?</h3><p>Choose the closest project type. The next steps will switch to the measurements and tripwires that matter most for that kind of work.</p></div>" + renderChoiceGrid(CONFIG.projects, state.project, "choose-project") + "<div class='decision-nav'><span></span><button type='button' class='cta' data-action='next' " + (requiredForStep(1) ? "" : "disabled") + ">Continue</button></div>";
    }

    if (state.step === 2) {
      return "<div class='decision-step-copy'><h3>Tell the tool about the property</h3><p>These checks matter because the same project can follow a different route on a house, a flat, or a site affected by local controls.</p></div><div class='decision-question'><h4>Property type</h4>" + renderChoiceGrid(CONFIG.property_types, state.property, "choose-property") + "</div><div class='decision-question'><h4>Previous extensions or major roof changes already on the property?</h4>" + renderChoiceGrid(CONFIG.previous_work_options, state.previousWork, "choose-previous-work") + "</div><div class='decision-question'><h4>Special local constraints</h4><div class='decision-chip-row'>" + CONFIG.constraint_options.map((option) => { const selected = state.constraints.includes(option.value) ? " selected" : ""; return "<button type='button' class='decision-chip" + selected + "' data-action='toggle-constraint' data-value='" + escapeHtml(option.value) + "'>" + escapeHtml(option.label) + "</button>"; }).join("") + "</div><div class='decision-question-note'>Select any that already apply. Leave them clear if you know they do not apply.</div></div><div class='decision-nav'><button type='button' class='button-secondary' data-action='prev'>Back</button><button type='button' class='cta' data-action='next' " + (requiredForStep(2) ? "" : "disabled") + ">Continue</button></div>";
    }

    if (state.step === 3 && currentProject) {
      const answers = state.detailAnswers;
      return "<div class='decision-step-copy'><h3>Check the size, form and siting</h3><p>" + escapeHtml(currentProject.description) + " Answer the questions below with the closest structured option rather than a perfect technical measurement.</p></div><div class='decision-question'><h4>" + escapeHtml(currentProject.primary_question.label) + "</h4>" + renderChoiceGrid(currentProject.primary_question.options, answers[currentProject.primary_question.id], "set-detail", " data-question-id='" + escapeHtml(currentProject.primary_question.id) + "'") + "</div>" + (currentProject.secondary_question ? "<div class='decision-question'><h4>" + escapeHtml(currentProject.secondary_question.label) + "</h4>" + renderChoiceGrid(currentProject.secondary_question.options, answers[currentProject.secondary_question.id], "set-detail", " data-question-id='" + escapeHtml(currentProject.secondary_question.id) + "'") + "</div>" : "") + ((currentProject.binary_questions || []).length ? "<div class='decision-binary-grid'>" + currentProject.binary_questions.map((question) => renderBinaryQuestion(question, answers[question.id])).join("") + "</div>" : "") + "<div class='decision-nav'><button type='button' class='button-secondary' data-action='prev'>Back</button><button type='button' class='cta' data-action='next' " + (requiredForStep(3) ? "" : "disabled") + ">Continue</button></div>";
    }

    if (state.step === 4 && currentProject) {
      const cards = summaryItems().map((item) => "<div class='decision-review-card'><strong>" + escapeHtml(item.label) + "</strong><span>" + escapeHtml(item.value) + "</span></div>").join("");
      return "<div class='decision-step-copy'><h3>Review the answers and run the check</h3><p>The result will give a short answer first, explain why the tool landed there, show what usually changes the answer and point you to the best next pages.</p></div><div class='decision-review-grid'>" + cards + "</div><div class='decision-nav'><button type='button' class='button-secondary' data-action='prev'>Back</button><button type='button' class='cta' data-action='run-check' " + (requiredForStep(4) ? "" : "disabled") + ">Check my project</button></div>";
    }

    return "";
  }

  function renderSidebarSections() {
    const items = summaryItems();
    return {
      title: "Your answers",
      summaryHtml: items.length ? items.map((item) => "<div class='decision-summary-item'><strong>" + escapeHtml(item.label) + "</strong><span>" + escapeHtml(item.value) + "</span></div>").join("") : "<div class='decision-summary-item'><strong>Project snapshot</strong><span>Choose a project to start the decision engine.</span></div>",
      noteHtml: "<strong>How this tool works:</strong> it uses structured rules for common UK planning triggers. It is useful for early triage, but it does not replace formal confirmation where the design is close to a limit or affected by special controls.",
    };
  }

  function renderSidebar() {
    const sections = renderSidebarSections();
    return "<div class='decision-sidebar'><h3>" + escapeHtml(sections.title) + "</h3><div class='decision-summary-list'>" + sections.summaryHtml + "</div><div class='decision-method-note'>" + sections.noteHtml + "</div></div>";
  }

  function renderHeaderActions() {
    return (state.result ? "<button type='button' class='button-secondary' data-action='edit-result'>Edit answers</button>" : "") + "<button type='button' class='button-secondary' data-action='reset'>Start again</button>";
  }

  function renderPlanningDecisionDesktopShell(options) {
    const currentName = options.hasResult ? "Result" : (options.stepNames[options.currentStep - 1] || "Review");
    return "<div class='planning-decision-desktop-shell'><div class='decision-engine-header'><div><span class='decision-kicker'>" + escapeHtml(options.kicker) + "</span><h2>" + escapeHtml(options.heading) + "</h2><p class='tool-summary'>" + escapeHtml(options.intro) + "</p>" + renderTrustNote() + "</div><div class='decision-header-actions'>" + options.actionsHtml + "</div></div><div class='decision-progress'>" + renderProgressIntro(options, currentName) + "<div class='decision-progress-bar'><span style='width:" + options.progress + "%'></span></div><div class='decision-step-labels'>" + renderProgressLabels(options.stepNames, options.currentStep, options.hasResult) + "</div></div><div class='decision-layout'><div class='decision-panel'>" + options.contentHtml + "</div>" + options.sidebarHtml + "</div></div>";
  }

  function renderPlanningDecisionMobileShell(options) {
    const currentName = options.hasResult ? "Result" : (options.stepNames[options.currentStep - 1] || "Review");
    const introLabel = options.hasResult ? "Result ready" : ("Step " + options.currentStep + " of " + options.stepNames.length);
    const introCopy = options.hasResult
      ? "Your structured result and follow-on guidance are ready below."
      : ("Current focus: " + currentName + ". Complete each step to unlock the full result.");
    return "<div class='planning-decision-mobile-shell'><div class='planning-decision-mobile-header'><div><span class='decision-kicker'>" + escapeHtml(options.kicker) + "</span><h2>" + escapeHtml(options.heading) + "</h2><p class='tool-summary'>" + escapeHtml(options.intro) + "</p>" + renderTrustNote() + "</div><div class='planning-decision-mobile-actions'>" + options.actionsHtml + "</div></div><div class='planning-decision-mobile-panel'><div class='planning-decision-mobile-step-intro'><strong>" + escapeHtml(introLabel) + "</strong><p>" + escapeHtml(introCopy) + "</p><div class='decision-progress-bar'><span style='width:" + options.progress + "%'></span></div><div class='decision-step-labels'>" + renderProgressLabels(options.stepNames, options.currentStep, options.hasResult) + "</div></div>" + options.contentHtml + "</div><div class='planning-decision-mobile-summary'><h3>" + escapeHtml(options.summaryTitle || "Your answers") + "</h3><div class='decision-summary-list'>" + options.summaryHtml + "</div>" + (options.noteHtml ? "<div class='decision-method-note'>" + options.noteHtml + "</div>" : "") + "</div></div>";
  }

  function render() {
    const progress = state.result ? 100 : (state.step / STEP_NAMES.length) * 100;
    const sections = renderSidebarSections();
    const shellOptions = {
      kicker: "Planning Decision Engine",
      heading: "Check whether your project probably needs planning permission",
      intro: "A guided, rule-based first pass for common home projects. There is no free-text box and no fake AI layer here, just structured answers and instant planning triage.",
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
    };
    engine.innerHTML = "<div class='planning-decision-shell planning-decision-shell-desktop' data-tool-shell='desktop'>" + renderPlanningDecisionDesktopShell(shellOptions) + "</div><div class='planning-decision-shell planning-decision-shell-mobile' data-tool-shell='mobile'>" + renderPlanningDecisionMobileShell(shellOptions) + "</div>";
    if (typeof engine.setAttribute === "function") {
      engine.setAttribute("data-tool-layout", isCompactLayout() ? "mobile" : "desktop");
    }
  }
"""
    )
    parts.append(
        """
  engine.addEventListener("click", function (event) {
    const target = event.target.closest("[data-action]");
    if (!target) {
      return;
    }

    const action = target.getAttribute("data-action");
    const value = target.getAttribute("data-value") || "";
    const questionId = target.getAttribute("data-question-id") || "";

    if (action === "choose-project") {
      logToolEvent("click", { action, value });
      state.project = value;
      state.detailAnswers = {};
      state.result = null;
      render();
      return;
    }

    if (action === "choose-property") {
      logToolEvent("click", { action, value });
      state.property = value;
      state.result = null;
      render();
      return;
    }

    if (action === "choose-previous-work") {
      logToolEvent("click", { action, value });
      state.previousWork = value;
      state.result = null;
      render();
      return;
    }

    if (action === "toggle-constraint") {
      logToolEvent("click", { action, value });
      state.result = null;
      if (state.constraints.includes(value)) {
        state.constraints = state.constraints.filter((item) => item !== value);
      } else {
        state.constraints = state.constraints.concat(value);
      }
      render();
      return;
    }

    if (action === "set-detail" || action === "set-binary") {
      logToolEvent("click", { action, questionId, value });
      state.detailAnswers = Object.assign({}, state.detailAnswers, { [questionId]: value });
      state.result = null;
      render();
      return;
    }

    if (action === "next" && state.step < 4 && requiredForStep(state.step)) {
      logToolEvent("click", { action, step: state.step });
      state.step += 1;
      render();
      return;
    }

    if (action === "prev" && state.step > 1) {
      logToolEvent("click", { action, step: state.step });
      state.step -= 1;
      render();
      return;
    }

    if (action === "edit-result") {
      logToolEvent("click", { action });
      state.result = null;
      state.loading = false;
      state.step = 4;
      render();
      return;
    }

    if (action === "reset") {
      logToolEvent("click", { action });
      state = createState();
      render();
      return;
    }

    if (action === "run-check" && requiredForStep(4)) {
      logToolEvent("submit", { action, snapshot: summaryItems() });
      state.loading = true;
      state.result = null;
      render();
      window.setTimeout(function () {
        state.loading = false;
        state.result = assess();
        logToolEvent("result", state.result);
        render();
      }, 680);
    }
  });

  render();
})();
</script>
</div>
"""
    )
    return render_inline_tool(
        "".join(parts),
        config=DECISION_ENGINE_CONFIG,
        styles=STRUCTURED_TOOL_STYLES,
        replacements={
            "__STRUCTURED_TOOL_UI_HELPERS__": STRUCTURED_TOOL_UI_HELPERS,
            "__NOSCRIPT_FALLBACK__": build_tool_fallback(
                "Interactive check loading",
                "If the guided questions do not appear, use the permitted development calculator or open the main planning guidance while JavaScript is unavailable.",
                [
                    {
                        "title": "Permitted Development Calculator",
                        "href": "/tools/permitted-development-calculator/",
                        "description": "Use the simpler form-based calculator for a first pass.",
                    },
                    {
                        "title": "Planning Permission",
                        "href": "/planning-permission/",
                        "description": "Open the main route guide if the project already feels borderline.",
                    },
                ],
            )
        },
    )
