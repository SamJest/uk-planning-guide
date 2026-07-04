const fs = require("fs");
const path = require("path");
const vm = require("vm");

const workspaceRoot = path.resolve(__dirname, "..");
const toolsDir = path.join(workspaceRoot, "output", "tools");

function assert(condition, message) {
  if (!condition) {
    throw new Error(message);
  }
}

function extractScripts(html) {
  return [...html.matchAll(/<script(?:[^>]*)>([\s\S]*?)<\/script>/gi)]
    .map((match) => match[1])
    .filter((script) => !script.includes("@context") && !script.includes("gtag("));
}

function extractToolMeta(html) {
  const match = html.match(/data-tool-root="([^"]+)"[^>]*data-tool-kind="([^"]+)"/);
  assert(match, "Missing data-tool-root/data-tool-kind marker");
  return { root: match[1], kind: match[2] };
}

function extractButtons(html) {
  return [...html.matchAll(/<button\b([^>]*)>/gi)].map((match) => {
    const attrs = match[1];
    const attr = (name) => {
      const attrMatch = attrs.match(new RegExp(`${name}='([^']*)'`));
      return attrMatch ? attrMatch[1] : "";
    };
    const classMatch = attrs.match(/class='([^']*)'/);
    const className = classMatch ? classMatch[1] : "";

    return {
      action: attr("data-action"),
      value: attr("data-value"),
      questionId: attr("data-question-id"),
      disabled: /\sdisabled(?:\s|>|=)/i.test(attrs),
      selected: /\bselected\b/.test(className),
    };
  });
}

function createStructuredHarness(rootId) {
  class FakeElement {
    constructor(id) {
      this.id = id;
      this.innerHTML = "";
      this.listeners = {};
      this.value = "";
    }

    addEventListener(type, handler) {
      this.listeners[type] = handler;
    }

    click(attrs) {
      const handler = this.listeners.click;
      assert(handler, `No click handler registered on ${this.id}`);
      handler({
        target: {
          closest(selector) {
            if (selector !== "[data-action]") {
              return null;
            }
            return {
              getAttribute(name) {
                return attrs[name] || null;
              },
            };
          },
        },
      });
    }
  }

  const elements = new Map();
  const timers = [];

  function getElement(id) {
    if (!elements.has(id)) {
      elements.set(id, new FakeElement(id));
    }
    return elements.get(id);
  }

  const sandbox = {
    console,
    document: {
      getElementById: getElement,
    },
    window: {
      addEventListener() {},
      removeEventListener() {},
      matchMedia() {
        return {
          matches: false,
          media: "",
          addEventListener() {},
          removeEventListener() {},
          addListener() {},
          removeListener() {},
        };
      },
      setTimeout(fn) {
        timers.push(fn);
        return timers.length;
      },
    },
  };

  sandbox.setTimeout = sandbox.window.setTimeout;

  return {
    sandbox,
    root: getElement(rootId),
    flushTimers() {
      while (timers.length) {
        const fn = timers.shift();
        fn();
      }
    },
  };
}

function clickAction(root, attrs) {
  root.click({
    "data-action": attrs.action,
    "data-value": attrs.value || "",
    "data-question-id": attrs.questionId || "",
  });
}

function firstButton(buttons, predicate) {
  return buttons.find(predicate) || null;
}

function smokeStructuredTool(pagePath, html) {
  const scripts = extractScripts(html);
  assert(scripts.length >= 1, "Missing interactive inline script");

  const rootIdMatch = html.match(/<div id="([^"]+)" class="decision-engine"[^>]*data-tool-root=/);
  assert(rootIdMatch, "Missing decision engine root id");
  const rootId = rootIdMatch[1];
  const toolScript =
    scripts.find((script) => script.includes(`document.getElementById("${rootId}")`)) ||
    scripts.find((script) => script.includes("decision-result-banner") && script.includes("data-action")) ||
    scripts[scripts.length - 1];
  const harness = createStructuredHarness(rootId);

  vm.runInNewContext(toolScript, harness.sandbox, { filename: pagePath });

  let selectedStateSeen = /selected/.test(harness.root.innerHTML);
  let lastHtml = harness.root.innerHTML;
  const history = [];

  for (let step = 0; step < 30; step += 1) {
    lastHtml = harness.root.innerHTML;
    if (harness.root.innerHTML.includes("decision-result-banner")) {
      assert(selectedStateSeen, "Tool never rendered a selected state");
      return;
    }

    const buttons = extractButtons(harness.root.innerHTML);
    assert(buttons.length > 0, "Tool rendered no buttons to interact with");

    const runButton = firstButton(
      buttons,
      (button) => !button.disabled && ["run-check", "submit"].includes(button.action)
    );
    if (runButton) {
      history.push(`run:${runButton.action}`);
      clickAction(harness.root, runButton);
      harness.flushTimers();
      continue;
    }

    const chooseGroupAction = (action) => {
      const group = buttons.filter((button) => button.action === action);
      if (!group.length || group.some((button) => button.selected)) {
        return null;
      }
      return group.find((button) => !button.disabled) || null;
    };

    const chooseQuestionAction = (action) => {
      const groups = new Map();
      for (const button of buttons.filter((item) => item.action === action)) {
        const key = button.questionId;
        if (!groups.has(key)) {
          groups.set(key, []);
        }
        groups.get(key).push(button);
      }

      for (const group of groups.values()) {
        if (!group.some((button) => button.selected)) {
          return group.find((button) => !button.disabled) || null;
        }
      }

      return null;
    };

    const answerButton =
      chooseGroupAction("choose-project") ||
      chooseGroupAction("select-property") ||
      chooseGroupAction("choose-property") ||
      chooseGroupAction("select-space") ||
      chooseGroupAction("choose-previous-work") ||
      chooseQuestionAction("set-detail") ||
      chooseQuestionAction("set-binary") ||
      chooseQuestionAction("set-answer");

    if (answerButton) {
      history.push(`answer:${answerButton.action}:${answerButton.questionId || answerButton.value}`);
      clickAction(harness.root, answerButton);
      selectedStateSeen = selectedStateSeen || /selected/.test(harness.root.innerHTML);
      continue;
    }

    const nextButton = firstButton(
      buttons,
      (button) => !button.disabled && button.action === "next"
    );

    if (nextButton) {
      history.push(`next:${nextButton.action}`);
      clickAction(harness.root, nextButton);
      continue;
    }

    throw new Error("No usable button action found during smoke test");
  }

  throw new Error(
    `Structured tool did not reach a result state. History: ${history.join(" -> ")}. Last HTML: ${lastHtml.slice(0, 800)}`
  );
}

function smokePdCalculator(pagePath, html) {
  const scripts = extractScripts(html);
  const toolScript = scripts.find((script) => script.includes("function runPDCheck"));
  assert(toolScript, "Missing PD calculator script");

  const elements = new Map();
  const documentListeners = {};
  const timers = [];
  const seedValues = {
    propertyType: "detached",
    extensionType: "rear",
    depth: "2.5",
    height: "3.0",
    boundary: "3.0",
    conservation: "no",
    previous: "no",
    result: "",
  };

  function getElement(id) {
    if (!elements.has(id)) {
      elements.set(id, {
        value: seedValues[id] || "",
        innerHTML: "",
        dataset: {},
        attributes: {},
        classList: {
          add() {},
          remove() {},
        },
        listeners: {},
        addEventListener(type, handler) {
          this.listeners[type] = handler;
        },
        setAttribute(name, value) {
          this.attributes[name] = value;
        },
        removeAttribute(name) {
          delete this.attributes[name];
        },
        click() {
          const handler = this.listeners.click;
          assert(handler, `No click handler registered on ${id}`);
          handler({ target: this });
        },
      });
    }
    return elements.get(id);
  }

  const sandbox = {
    console,
    document: {
      readyState: "complete",
      getElementById: getElement,
      addEventListener(type, handler) {
        documentListeners[type] = handler;
      },
    },
    window: {
      setTimeout(fn) {
        timers.push(fn);
        return timers.length;
      },
    },
  };

  vm.runInNewContext(toolScript, sandbox, { filename: pagePath });
  assert(typeof sandbox.runPDCheck === "function", "runPDCheck was not defined");

  const button = getElement("pd-check-button");
  button.click();
  while (timers.length) {
    const fn = timers.shift();
    fn();
  }

  const resultHtml = getElement("result").innerHTML;
  assert(resultHtml.includes("<h3>"), "PD calculator did not render a result heading");
  assert(resultHtml.includes("Next step"), "PD calculator did not render next-step guidance");
}

function smokePlanningRouteCheck(pagePath, html) {
  const routeScriptPath = path.join(workspaceRoot, "output", "assets", "js", "planning-route-check.js");
  const routeScript = fs.existsSync(routeScriptPath)
    ? fs.readFileSync(routeScriptPath, "utf8")
    : fs.readFileSync(path.join(workspaceRoot, "assets", "js", "planning-route-check.js"), "utf8");
  const leadConfigPath = path.join(workspaceRoot, "output", "assets", "js", "lead-config.js");
  const leadConfigScript = fs.existsSync(leadConfigPath)
    ? fs.readFileSync(leadConfigPath, "utf8")
    : fs.readFileSync(path.join(workspaceRoot, "assets", "js", "lead-config.js"), "utf8");
  const combined = html + "\n" + routeScript;

  assert(html.includes('id="planning-route-check-form"'), "Missing route check form");
  assert(html.includes('id="planning-route-result"'), "Missing route result panel");
  assert(html.includes('id="planning-route-help"'), "Missing optional help panel");
  assert(combined.includes('name=\\"consent_contact\\"'), "Missing contact consent checkbox");
  assert(combined.includes('name=\\"consent_share\\"'), "Missing sharing consent checkbox");
  assert(combined.includes('name=\\"website\\"'), "Missing honeypot field");
  assert(html.includes('/assets/js/lead-config.js'), "Missing lead config asset");
  assert(html.includes('/assets/js/planning-route-check.js'), "Missing route check script asset");
  assert(!/name=\\?"consent_(contact|share)\\?"[^>]*checked/i.test(combined), "Consent checkboxes must be unticked by default");

  assert(leadConfigScript.includes("window.UKPG_LEAD_CONFIG"), "Missing current lead config object");
  assert(leadConfigScript.includes("window.UKPG_LEAD_CAPTURE_CONFIG"), "Missing backwards-compatible lead config alias");
  assert(leadConfigScript.includes("endpoint: \"\""), "Lead endpoint should default to blank");
  assert(leadConfigScript.includes("YOUR-WORKER.your-subdomain.workers.dev/leads"), "Missing production receiver endpoint example");
  assert(leadConfigScript.includes("request_timeout_ms: 10000"), "Missing request timeout config");
  assert(leadConfigScript.includes("Do not add private API keys"), "Lead config must warn against frontend secrets");

  assert(routeScript.includes("getLeadConfig()"), "Route check should use compatible lead config lookup");
  assert(routeScript.includes("!config.enabled || !endpoint"), "Missing blank-endpoint fallback path");
  assert(routeScript.includes("owner_email"), "Missing owner email fallback handling");
  assert(routeScript.includes("UK Planning Guide enquiry - "), "Missing admin-friendly mailto subject");
  assert(routeScript.includes("encodeURIComponent(summary)"), "Mailto body should be URL-encoded");
  assert(routeScript.includes("form_elapsed_ms"), "Missing server-side timing signal in lead payload");
  assert(routeScript.includes("website: lead.website"), "Missing server-side honeypot signal in lead payload");
  assert(routeScript.includes("fetch(endpoint"), "Missing configured endpoint POST path");
  assert(routeScript.includes("AbortController"), "Missing timeout/abort handling");
  assert(routeScript.includes("Online submission timed out"), "Missing timeout fallback message");
  assert(routeScript.includes("Submission could not be accepted."), "Missing honeypot validation message");
  assert(routeScript.includes("Confirm that UK Planning Guide may contact you"), "Missing contact consent validation");
  assert(routeScript.includes("Confirm whether your enquiry may be shared"), "Missing sharing consent validation");

  const analyticsBodies = [...routeScript.matchAll(/emitEvent\("[^"]+",\s*\{([\s\S]*?)\}\);/g)].map((match) => match[1]);
  assert(analyticsBodies.length >= 6, "Expected route-check analytics events were not found");
  const piiPattern = /\b(name|email|phone|postcode|notes|user_notes|postcode_or_town)\b/i;
  assert(!analyticsBodies.some((body) => piiPattern.test(body)), "PII-like field is present in analytics event parameters");
}

function run() {
  const toolDirectories = fs
    .readdirSync(toolsDir, { withFileTypes: true })
    .filter((entry) => entry.isDirectory())
    .map((entry) => entry.name)
    .sort();

  for (const toolSlug of toolDirectories) {
    const pagePath = path.join(toolsDir, toolSlug, "index.html");
    const html = fs.readFileSync(pagePath, "utf8");
    const meta = extractToolMeta(html);

    try {
      if (meta.kind === "route-check") {
        smokePlanningRouteCheck(pagePath, html);
      } else if (meta.kind === "form") {
        smokePdCalculator(pagePath, html);
      } else {
        smokeStructuredTool(pagePath, html);
      }
    } catch (error) {
      error.message = `[${toolSlug}] ${error.message}`;
      throw error;
    }

    console.log(`[OK] ${toolSlug}`);
  }
}

run();
