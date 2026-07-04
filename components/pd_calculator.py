def render_pd_calculator():
    return """
<div class="tool-card pd-calculator-card" data-tool-root="permitted-development-calculator" data-tool-kind="form">
<style>
.pd-calculator-card{padding:0;background:linear-gradient(180deg,rgba(255,255,255,.98),rgba(247,241,232,.94)),linear-gradient(135deg,rgba(31,111,95,.06),transparent 58%);border-color:rgba(31,111,95,.16);}
.pd-calculator-shell{display:grid;gap:20px;padding:30px;}
.pd-calculator-header{display:grid;gap:14px;padding:0 0 6px;}
.pd-calculator-header h2{margin-bottom:0;}
.pd-calculator-kicker{display:inline-flex;align-items:center;width:max-content;padding:8px 12px;border-radius:999px;background:rgba(31,111,95,.10);color:var(--accent-text);font-size:12px;font-weight:800;letter-spacing:.08em;text-transform:uppercase;}
.pd-calculator-trust{display:grid;gap:6px;padding:14px 15px;background:rgba(223,241,234,.54);border:1px solid rgba(31,111,95,.12);border-radius:16px;}
.pd-calculator-trust strong{font-size:12px;font-weight:800;letter-spacing:.08em;text-transform:uppercase;color:var(--accent-text);}
.pd-calculator-trust span{font-size:14px;line-height:1.58;color:var(--ink-soft);}
.pd-calculator-body{display:grid;gap:18px;grid-template-columns:minmax(0,1.15fr) minmax(0,.85fr);align-items:start;}
.pd-calculator-panel,.pd-calculator-result-panel{min-width:0;padding:22px;background:rgba(255,255,255,.84);border:1px solid rgba(31,41,55,.08);border-radius:22px;box-shadow:var(--shadow-soft);}
.pd-calculator-panel{display:grid;gap:18px;}
.pd-calculator-step-intro{display:grid;gap:8px;padding:16px 18px;background:linear-gradient(135deg,rgba(247,241,232,.74),rgba(255,255,255,.94));border:1px solid rgba(31,41,55,.06);border-radius:18px;}
.pd-calculator-step-intro strong{font-size:13px;letter-spacing:.08em;text-transform:uppercase;color:var(--accent-text);}
.pd-calculator-step-intro p{margin:0;color:var(--ink-soft);}
.pd-calculator-fields{display:grid;gap:14px;grid-template-columns:repeat(auto-fit,minmax(min(100%,180px),1fr));}
.pd-calculator-field{min-width:0;}
.pd-calculator-field label{display:block;margin-bottom:8px;font-size:13px;font-weight:800;letter-spacing:.04em;text-transform:uppercase;color:var(--ink-faint);}
.pd-calculator-field input,.pd-calculator-field select{min-width:0;}
.pd-calculator-actions{display:flex;justify-content:flex-start;gap:12px;margin-top:2px;padding-top:4px;}
.pd-calculator-actions button{margin:0;min-height:50px;padding:14px 20px;font-weight:800;box-shadow:0 14px 26px rgba(31,111,95,.14);}
.pd-calculator-result-panel{display:grid;gap:14px;background:linear-gradient(180deg,rgba(255,255,255,.96),rgba(247,241,232,.86));}
.pd-calculator-result-eyebrow{font-size:12px;font-weight:800;letter-spacing:.08em;text-transform:uppercase;color:var(--accent-text);}
.pd-calculator-result-panel h3{margin-bottom:2px;overflow-wrap:anywhere;}
.pd-calculator-result-panel p{max-width:none;}
.pd-calculator-result-panel .tool-result{margin-top:0;padding:0;background:none;border:0;border-radius:0;box-shadow:none;}
.pd-calculator-result-panel .tool-result[data-result-ready="true"]{opacity:1;transform:none;}
.pd-calculator-empty{padding:18px 20px;background:rgba(247,241,232,.72);border:1px solid rgba(31,41,55,.08);border-radius:18px;}
.pd-calculator-summary{font-size:14px;line-height:1.6;color:var(--ink-faint);}
.pd-calculator-result-copy{display:grid;gap:14px;padding:2px 0 0;}
.pd-calculator-result-copy h3{font-size:1.3rem;line-height:1.15;}
.pd-calculator-result-copy p{line-height:1.65;}
.pd-calculator-result-copy ul{margin:0;padding-left:18px;}
.pd-follow-up{display:grid;gap:14px;margin-top:6px;}
.pd-follow-up-card{display:grid;gap:14px;padding:18px;background:linear-gradient(180deg,rgba(255,255,255,.96),rgba(247,241,232,.86));border:1px solid rgba(31,41,55,.08);border-radius:20px;box-shadow:var(--shadow-soft);}
.pd-follow-up-heading{display:grid;gap:6px;}
.pd-follow-up-heading h3,.pd-follow-up-heading p{margin:0;}
.pd-follow-up-heading p{line-height:1.6;color:var(--ink-soft);}
.pd-follow-up-kicker{display:inline-flex;align-items:center;width:max-content;padding:7px 10px;border-radius:999px;background:rgba(31,111,95,.10);color:var(--accent-text);font-size:11px;font-weight:800;letter-spacing:.08em;text-transform:uppercase;}
.pd-follow-up-grid{display:grid;gap:12px;grid-template-columns:repeat(auto-fit,minmax(min(100%,220px),1fr));}
.pd-follow-up-link{display:block;min-width:0;padding:16px;background:rgba(255,255,255,.94);border:1px solid rgba(31,41,55,.08);border-radius:18px;color:inherit;box-shadow:var(--shadow-soft);}
.pd-follow-up-link strong{display:block;margin-bottom:6px;}
.pd-follow-up-link span{display:block;font-size:14px;line-height:1.58;color:var(--ink-soft);}
.pd-email-capture{display:grid;gap:10px;grid-template-columns:minmax(0,1fr) auto;align-items:center;}
.pd-email-input{width:100%;min-width:0;min-height:50px;padding:13px 15px;border:1px solid rgba(31,41,55,.14);border-radius:16px;background:#fff;color:var(--ink);}
.pd-email-button{min-height:50px;padding:14px 20px;}
.pd-email-note{grid-column:1 / -1;margin:0;font-size:13px;line-height:1.55;color:var(--ink-faint);}
.pd-inline-note{padding:14px 15px;background:rgba(223,241,234,.54);border:1px solid rgba(31,111,95,.12);border-radius:16px;font-size:14px;line-height:1.58;color:var(--ink-soft);}
@media (max-width:960px){.pd-calculator-shell{padding:22px;}.pd-calculator-body{grid-template-columns:1fr;}}
@media (max-width:767px){.pd-calculator-shell{padding:18px;gap:14px;}.pd-calculator-header{padding:0;}.pd-calculator-header h2{font-size:clamp(1.5rem,7vw,2rem);line-height:1.08;}.pd-calculator-panel,.pd-calculator-result-panel,.pd-follow-up-card{padding:18px;border-radius:20px;}.pd-calculator-step-intro{padding:15px 16px;}.pd-calculator-fields{grid-template-columns:1fr;gap:12px;}.pd-calculator-actions{display:grid;gap:10px;}.pd-calculator-actions button,.pd-email-button{width:100%;min-height:52px;}.pd-calculator-empty{padding:16px;}.pd-calculator-result-panel .tool-result-links,.pd-follow-up-grid{grid-template-columns:1fr !important;}.pd-email-capture{grid-template-columns:1fr;}}
@media (max-width:420px){.pd-calculator-shell{padding:16px;}.pd-calculator-panel,.pd-calculator-result-panel,.pd-calculator-step-intro,.pd-calculator-trust,.pd-follow-up-card{padding:16px;}.pd-calculator-kicker{font-size:11px;}.pd-calculator-summary,.pd-calculator-result-copy p,.pd-calculator-trust span,.pd-inline-note,.pd-email-note,.pd-follow-up-link span{font-size:14px;}}
</style>
<div class="pd-calculator-shell">
<div class="pd-calculator-header">
<span class="pd-calculator-kicker">Permitted development</span>
<h2>Permitted Development Calculator</h2>
<p class="tool-summary">Use this self-check to see whether a common home project still looks comfortably inside the usual permitted development envelope.</p>
<div class="pd-calculator-trust"><strong>UK planning baseline</strong><span>Based on common UK permitted development rules. Always confirm the exact measurements, restrictions and local council position before relying on the result.</span></div>
</div>

<div class="pd-calculator-body">
<div class="pd-calculator-panel">
<div class="pd-calculator-step-intro">
<strong>Project details</strong>
<p>Enter the core measurements first, then run the check to see whether the project still looks comfortably inside the usual permitted development range.</p>
</div>
<div class="pd-calculator-fields">
<div class="pd-calculator-field">
<label for="propertyType">Property Type</label>
<select id="propertyType">
  <option value="detached">Detached</option>
  <option value="semi">Semi-detached</option>
  <option value="terrace">Terrace</option>
  <option value="flat">Flat</option>
</select>
</div>

<div class="pd-calculator-field">
<label for="extensionType">Extension Type</label>
<select id="extensionType">
  <option value="rear">Rear Extension</option>
  <option value="side">Side Extension</option>
  <option value="loft">Loft Conversion</option>
</select>
</div>

<div class="pd-calculator-field">
<label for="depth">Extension Depth (m)</label>
<input type="number" id="depth" step="0.1">
</div>

<div class="pd-calculator-field">
<label for="height">Height (m)</label>
<input type="number" id="height" step="0.1">
</div>

<div class="pd-calculator-field">
<label for="boundary">Distance to Boundary (m)</label>
<input type="number" id="boundary" step="0.1">
</div>

<div class="pd-calculator-field">
<label for="conservation">Conservation Area?</label>
<select id="conservation">
  <option value="no">No</option>
  <option value="yes">Yes</option>
</select>
</div>

<div class="pd-calculator-field">
<label for="previous">Previous Extensions?</label>
<select id="previous">
  <option value="no">No</option>
  <option value="yes">Yes</option>
</select>
</div>
</div>

<div class="pd-calculator-actions">
<button type="button" id="pd-check-button">Check</button>
</div>
</div>

<div class="pd-calculator-result-panel">
<span class="pd-calculator-result-eyebrow">Your result</span>
<h3>Result</h3>
<p class="pd-calculator-summary">The tool keeps the same calculator logic as before and updates this panel after each check.</p>
<div id="result" class="tool-result" aria-live="polite">
<div class="pd-calculator-empty">
<p>Choose the project details above, then run the check to see the first-pass result.</p>
</div>
</div>
</div>
</div>
<noscript>
<p class="tool-summary">JavaScript is required for the instant result. If scripts are unavailable, use <a href="/tools/planning-decision-tool/">the planning decision engine</a> or open the detailed planning guides directly.</p>
</noscript>
</div>

<script>
function logPDToolEvent(type, detail) {
    if (typeof console !== "undefined" && console && typeof console.log === "function") {
        console.log("[permitted-development-calculator]", type, detail || "");
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

function buildResultLinks(type, status) {
    const links = [
        { href: "/permitted-development/", title: "Read the permitted development guide", description: "Check the baseline rights behind this calculator result." },
        { href: "/planning-permission/", title: "Review the planning permission route", description: "Open the formal route guide if the project is starting to look borderline." },
        { href: "/tools/planning-decision-tool/", title: "Run the full planning decision tool", description: "Use the deeper route check when your dimensions or site context need more nuance." },
    ];

    if (type === "rear" || type === "side") {
        links.unshift({ href: "/house-extensions/", title: "Compare house extension planning rules", description: "Open the extension guide for depth, height and siting rules." });
    } else if (type === "loft") {
        links.unshift({ href: "/loft-conversions/", title: "Check loft conversion planning rules", description: "Use the loft guide for roof changes, dormers and visibility checks." });
    }

    if (status !== "Likely permitted development") {
        links.push({ href: "/councils/", title: "Check local authority planning context", description: "Use the council layer when conservation area or local restrictions could change the answer." });
    }

    return links.slice(0, 4)
        .map((item) => "<a class='tool-result-link' href='" + escapeHtml(item.href) + "'><strong>" + escapeHtml(item.title) + "</strong><span>" + escapeHtml(item.description) + "</span></a>")
        .join("");
}

function showPDLoading() {
    const result = document.getElementById("result");
    result.removeAttribute("data-result-ready");
    result.classList.remove("tool-result-visible");
    result.innerHTML =
        "<div class='tool-loading-state'><div class='tool-loading-bar'></div><h3>Checking the common permitted development triggers...</h3><p>This short pause is only UI polish while the structured result is assembled.</p></div>";
}

function renderPDResult(status, resultText, nextStep, linksHtml) {
    const result = document.getElementById("result");
    result.setAttribute("data-result-ready", "true");
    result.innerHTML =
        "<div class='pd-calculator-result-copy'><h3>" + escapeHtml(status) + "</h3><p>" + resultText + "</p><p><strong>Next step:</strong> " + escapeHtml(nextStep) + "</p><div class='tool-result-links'>" + linksHtml + "</div>" + renderPDPostResultExtras(status) + "</div>";
}

function renderPDPostResultExtras(status) {
    return "<section class='pd-follow-up'><div class='pd-follow-up-card'><div class='pd-follow-up-heading'><span class='pd-follow-up-kicker'>Next steps</span><h3>Keep the project moving</h3><p>Use the next best action below to confirm the answer, localise it, or move into a deeper planning check.</p></div><div class='pd-follow-up-grid'><a class='pd-follow-up-link' href='/permitted-development/'><strong>View full guide</strong><span>Open the longer permitted development guide behind this result.</span></a><a class='pd-follow-up-link' href='/councils/'><strong>Check rules in your area</strong><span>Compare your local authority planning layer before relying on the answer.</span></a><a class='pd-follow-up-link' href='/tools/planning-decision-tool/'><strong>Use another tool</strong><span>Run the full planning checker when the project needs a deeper route review.</span></a></div></div><div class='pd-follow-up-card'><div class='pd-follow-up-heading'><span class='pd-follow-up-kicker'>Related tools</span><h3>Keep checking from another angle</h3><p>These follow-on tools help you pressure-test the same project without starting your research again.</p></div><div class='pd-follow-up-grid'><a class='pd-follow-up-link' href='/tools/planning-decision-tool/'><strong>Planning checker</strong><span>Use the main rule-based checker for a fuller planning route answer.</span></a><a class='pd-follow-up-link' href='/tools/planning-route-planner/'><strong>Route planner</strong><span>Compare the likely planning path when the answer feels mixed.</span></a><a class='pd-follow-up-link' href='/tools/project-requirements-generator/'><strong>Project requirements</strong><span>Build a practical checklist of documents and follow-on checks.</span></a></div></div><div class='pd-follow-up-card'><div class='pd-follow-up-heading'><span class='pd-follow-up-kicker'>Save or share</span><h3>Keep a clean record of this result</h3><p>Save the summary on this device, then bookmark or print the page if you want to review it with someone else later.</p></div><div class='pd-email-capture' data-pd-email-capture='permitted-development-calculator' data-result-label='" + escapeHtml(status) + "'><button type='button' class='pd-email-button cta' onclick='window.__ukpgSavePDResult && window.__ukpgSavePDResult(this)'>Save result on this device</button><button type='button' class='pd-email-button button-secondary' onclick='window.print()'>Print this result</button><p class='pd-email-note'>Stored only on this device. For sharing, copy the page link from your browser or print this result.</p></div></div><div class='pd-inline-note'>This is a guide based on UK planning rules. Always confirm with your local council.</div></section>";
}

window.__ukpgSavePDResult = function (button) {
    try {
        const wrapper = button && button.closest("[data-pd-email-capture]");
        if (!wrapper) {
            return;
        }
        const note = wrapper.querySelector(".pd-email-note");
        window.localStorage.setItem("ukpg-tool-email:permitted-development-calculator", JSON.stringify({
            resultLabel: wrapper.getAttribute("data-result-label") || "Permitted development result",
            savedAt: new Date().toISOString()
        }));
        if (note) {
            note.textContent = "Saved on this device. Bookmark or print the page as well if you want an easy reference outside this browser.";
        }
    } catch (error) {
        const wrapper = button && button.closest("[data-pd-email-capture]");
        const note = wrapper ? wrapper.querySelector(".pd-email-note") : null;
        if (note) {
            note.textContent = "This browser blocked local storage, so use a bookmark, copied link or printed page instead.";
        }
    }
};

function runPDCheck() {
    const property = document.getElementById("propertyType").value;
    const type = document.getElementById("extensionType").value;
    const depth = parseFloat(document.getElementById("depth").value || 0);
    const height = parseFloat(document.getElementById("height").value || 0);
    const boundary = parseFloat(document.getElementById("boundary").value || 0);
    const conservation = document.getElementById("conservation").value;
    const previous = document.getElementById("previous").value;

    logPDToolEvent("submit", {
        property,
        type,
        depth,
        height,
        boundary,
        conservation,
        previous,
    });

    let issues = [];

    if (property === "flat") {
        issues.push("Flats do not benefit from the usual householder permitted development rights.");
    }

    if (conservation === "yes") {
        issues.push("Conservation areas can tighten controls or remove some permitted development rights.");
    }

    if (previous === "yes") {
        issues.push("Previous extensions can reduce or remove the remaining permitted development allowance.");
    }

    if (type === "rear") {
        if (property === "detached" && depth > 4) {
            issues.push("A detached house rear extension over 4m depth usually needs a closer check.");
        }
        if ((property === "semi" || property === "terrace") && depth > 3) {
            issues.push("A semi-detached or terraced rear extension over 3m depth usually needs a closer check.");
        }
    }

    if (type === "side") {
        issues.push("Side extensions often need planning permission or at least a much closer local review.");
    }

    if (height > 4) {
        issues.push("The height looks above the usual 4m threshold.");
    }

    if (boundary < 2 && height > 3) {
        issues.push("If the building is within 2m of a boundary, the usual 3m height check becomes important.");
    }

    let status = "";
    let result = "";
    let nextStep = "";

    if (issues.length === 0) {
        status = "Likely permitted development";
        result = "Your project appears to fit within the common permitted development checks used in this tool.";
        nextStep = "Now confirm the exact measurements, local restrictions and any previous extensions before relying on the result.";
    } else if (issues.length <= 2) {
        status = "Check required";
        result = issues.join("<br>");
        nextStep = "Open the matching project guide and compare the local authority layer before moving forward.";
    } else {
        status = "Likely requires planning permission";
        result = issues.join("<br>");
        nextStep = "Treat the formal planning route as likely unless more detailed local guidance shows a cleaner answer.";
    }

    renderPDResult(status, result, nextStep, buildResultLinks(type, status));

    logPDToolEvent("result", {
        status: status,
        issues: issues,
    });
}

function initPDCalculator() {
    const button = document.getElementById("pd-check-button");
    if (!button || button.dataset.bound === "true") {
        return;
    }

    button.dataset.bound = "true";
    button.addEventListener("click", function () {
        logPDToolEvent("click", { action: "run-check" });
        showPDLoading();
        window.setTimeout(runPDCheck, 520);
    });
}

if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initPDCalculator);
} else {
    initPDCalculator();
}
</script>
"""
