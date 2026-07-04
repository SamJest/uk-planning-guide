const fs = require("fs");
const http = require("http");
const os = require("os");
const path = require("path");
const { spawn, spawnSync } = require("child_process");

const workspaceRoot = path.resolve(__dirname, "..");
const toolsDir = path.join(workspaceRoot, "output", "tools");
const screenshotDir = path.join(workspaceRoot, "artifacts", "tool-mobile-audit");
const reportPath = path.join(screenshotDir, "audit-report.json");
const edgeCandidates = [
  "C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe",
  "C:\\Program Files\\Microsoft\\Edge\\Application\\msedge.exe",
];

const VIEWPORTS = [320, 360, 375, 390, 430, 768];

function assert(condition, message) {
  if (!condition) {
    throw new Error(message);
  }
}

function wait(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

function findEdge() {
  return edgeCandidates.find((candidate) => fs.existsSync(candidate)) || "";
}

function mimeType(filePath) {
  const ext = path.extname(filePath).toLowerCase();
  switch (ext) {
    case ".html":
      return "text/html; charset=utf-8";
    case ".css":
      return "text/css; charset=utf-8";
    case ".js":
      return "application/javascript; charset=utf-8";
    case ".json":
      return "application/json; charset=utf-8";
    case ".svg":
      return "image/svg+xml";
    case ".png":
      return "image/png";
    case ".jpg":
    case ".jpeg":
      return "image/jpeg";
    case ".webp":
      return "image/webp";
    default:
      return "application/octet-stream";
  }
}

function resolveStaticPath(requestPath) {
  const cleanPath = decodeURIComponent(requestPath.split("?")[0]);
  const relative = cleanPath.replace(/^\/+/, "");
  let filePath = path.join(workspaceRoot, relative);

  if (!filePath.startsWith(workspaceRoot)) {
    return "";
  }

  if (fs.existsSync(filePath) && fs.statSync(filePath).isDirectory()) {
    filePath = path.join(filePath, "index.html");
  }

  return filePath;
}

function createServer() {
  return http.createServer((req, res) => {
    const url = new URL(req.url, "http://127.0.0.1");
    const filePath = resolveStaticPath(url.pathname);
    if (!filePath || !fs.existsSync(filePath) || !fs.statSync(filePath).isFile()) {
      res.writeHead(404, { "Content-Type": "text/plain; charset=utf-8" });
      res.end("Not found");
      return;
    }

    res.writeHead(200, { "Content-Type": mimeType(filePath) });
    res.end(fs.readFileSync(filePath));
  });
}

async function waitForDevToolsPort(userDataDir) {
  const marker = path.join(userDataDir, "DevToolsActivePort");
  for (let attempt = 0; attempt < 300; attempt += 1) {
    if (fs.existsSync(marker)) {
      const [port] = fs.readFileSync(marker, "utf8").trim().split(/\r?\n/);
      if (port) {
        return port;
      }
    }
    await wait(100);
  }
  throw new Error("Edge did not expose a DevTools port");
}

async function fetchJson(url) {
  const response = await fetch(url);
  assert(response.ok, `Request failed: ${url} (${response.status})`);
  return response.json();
}

async function waitForTarget(port) {
  const listUrl = `http://127.0.0.1:${port}/json/list`;
  for (let attempt = 0; attempt < 300; attempt += 1) {
    try {
      const targets = await fetchJson(listUrl);
      const pageTarget = (targets || []).find((target) => target.type === "page" && target.webSocketDebuggerUrl);
      if (pageTarget) {
        return pageTarget.webSocketDebuggerUrl;
      }
    } catch (error) {
      // Edge can take a moment to open the port.
    }
    await wait(100);
  }
  throw new Error("Unable to connect to Edge DevTools");
}

async function createCdpClient(wsUrl) {
  const socket = new WebSocket(wsUrl);
  const pending = new Map();
  const eventListeners = new Map();
  let nextId = 1;

  await new Promise((resolve, reject) => {
    socket.addEventListener("open", resolve, { once: true });
    socket.addEventListener("error", reject, { once: true });
  });

  socket.addEventListener("message", (event) => {
    const message = JSON.parse(event.data);

    if (typeof message.id === "number") {
      const entry = pending.get(message.id);
      if (!entry) {
        return;
      }
      pending.delete(message.id);
      if (message.error) {
        entry.reject(new Error(message.error.message || "CDP command failed"));
      } else {
        entry.resolve(message.result || {});
      }
      return;
    }

    if (!message.method) {
      return;
    }

    const listeners = eventListeners.get(message.method) || [];
    for (const listener of listeners.slice()) {
      listener(message.params || {});
    }
  });

  return {
    send(method, params = {}) {
      return new Promise((resolve, reject) => {
        const id = nextId++;
        pending.set(id, { resolve, reject });
        socket.send(JSON.stringify({ id, method, params }));
      });
    },
    on(method, handler) {
      if (!eventListeners.has(method)) {
        eventListeners.set(method, []);
      }
      eventListeners.get(method).push(handler);
      return () => {
        const listeners = eventListeners.get(method) || [];
        eventListeners.set(
          method,
          listeners.filter((item) => item !== handler)
        );
      };
    },
    waitFor(method, predicate = () => true, timeoutMs = 15000) {
      return new Promise((resolve, reject) => {
        const timeout = setTimeout(() => {
          off();
          reject(new Error(`Timed out waiting for ${method}`));
        }, timeoutMs);

        const off = this.on(method, (params) => {
          if (!predicate(params)) {
            return;
          }
          clearTimeout(timeout);
          off();
          resolve(params);
        });
      });
    },
    async close() {
      socket.close();
      await wait(100);
    },
  };
}

function valueFromRemote(result) {
  if (!result) {
    return null;
  }
  if (Object.prototype.hasOwnProperty.call(result, "value")) {
    return result.value;
  }
  return null;
}

function buildInteractionExpression(toolSlug) {
  const slug = JSON.stringify(toolSlug);
  return `
    (async function () {
      const toolSlug = ${slug};

      function assert(condition, message) {
        if (!condition) {
          throw new Error(message);
        }
      }

      function wait(ms) {
        return new Promise((resolve) => window.setTimeout(resolve, ms));
      }

      async function waitFor(check, message, timeoutMs) {
        const started = Date.now();
        while (Date.now() - started < timeoutMs) {
          const value = check();
          if (value) {
            return value;
          }
          await wait(100);
        }
        throw new Error(message);
      }

      const root = await waitFor(
        () => document.querySelector('[data-tool-root="' + toolSlug + '"]'),
        'Missing interactive root container',
        5000
      );
      const kind = root.getAttribute('data-tool-kind');

      if (kind === 'form') {
        document.getElementById('propertyType').value = 'detached';
        document.getElementById('extensionType').value = 'rear';
        document.getElementById('depth').value = '2.5';
        document.getElementById('height').value = '3.0';
        document.getElementById('boundary').value = '3.0';
        document.getElementById('conservation').value = 'no';
        document.getElementById('previous').value = 'no';

        const button = document.getElementById('pd-check-button');
        assert(button, 'Missing PD calculator button');
        button.click();

        const heading = await waitFor(
          () => document.querySelector('#result h3'),
          'PD calculator did not render a result heading',
          5000
        );

        return {
          ok: true,
          kind,
          resultText: heading.textContent.trim(),
        };
      }

      function byAction(action) {
        return Array.from(root.querySelectorAll('[data-action="' + action + '"]'));
      }

      function findUnansweredGroupButton(action) {
        const buttons = byAction(action);
        const grouped = new Map();
        for (const button of buttons) {
          const key = button.getAttribute('data-question-id') || '';
          if (!grouped.has(key)) {
            grouped.set(key, []);
          }
          grouped.get(key).push(button);
        }

        for (const group of grouped.values()) {
          if (!group.some((button) => button.classList.contains('selected'))) {
            return group.find((button) => !button.disabled) || null;
          }
        }

        return null;
      }

      function findSingleChoiceButton(action) {
        const buttons = byAction(action);
        if (!buttons.length || buttons.some((button) => button.classList.contains('selected'))) {
          return null;
        }
        return buttons.find((button) => !button.disabled) || null;
      }

      for (let step = 0; step < 30; step += 1) {
        const banner = root.querySelector('.decision-result-banner');
        if (banner) {
          return {
            ok: true,
            kind,
            resultText: banner.textContent.trim(),
          };
        }

        const runButton = root.querySelector('[data-action="run-check"]:not([disabled]), [data-action="submit"]:not([disabled])');
        if (runButton) {
          runButton.click();
          await wait(1300);
          continue;
        }

        const answerButton =
          findSingleChoiceButton('choose-project') ||
          findSingleChoiceButton('select-property') ||
          findSingleChoiceButton('choose-property') ||
          findSingleChoiceButton('select-space') ||
          findSingleChoiceButton('choose-previous-work') ||
          findUnansweredGroupButton('set-detail') ||
          findUnansweredGroupButton('set-binary') ||
          findUnansweredGroupButton('set-answer');

        if (answerButton) {
          answerButton.click();
          await wait(100);
          continue;
        }

        const nextButton = root.querySelector('[data-action="next"]:not([disabled])');
        if (nextButton) {
          nextButton.click();
          await wait(100);
          continue;
        }

        throw new Error('No usable action found during browser audit');
      }

      throw new Error('Tool did not reach a result state');
    })()
  `;
}

function buildAuditExpression(toolSlug, viewportWidth) {
  const slug = JSON.stringify(toolSlug);
  return `
    (function () {
      const toolSlug = ${slug};
      const viewportWidth = ${viewportWidth};
      const root = document.querySelector('[data-tool-root="' + toolSlug + '"]');
      if (!root) {
        throw new Error('Missing tool root for audit');
      }

      function isVisible(node) {
        if (!node) {
          return false;
        }
        const style = window.getComputedStyle(node);
        const rect = node.getBoundingClientRect();
        return (
          style.display !== 'none' &&
          style.visibility !== 'hidden' &&
          style.opacity !== '0' &&
          rect.width > 0 &&
          rect.height > 0
        );
      }

      function summarize(selector) {
        const nodes = Array.from(root.querySelectorAll(selector));
        return {
          total: nodes.length,
          visible: nodes.filter(isVisible).length,
        };
      }

      const shells = {
        mobile: summarize('.decision-mobile-calculator-shell, .planning-decision-mobile-shell'),
        mobileHeader: summarize('.decision-mobile-calculator-header, .planning-decision-mobile-header'),
        mobileBody: summarize('.decision-mobile-calculator-body, .planning-decision-mobile-panel'),
        mobilePanel: summarize('.decision-mobile-calculator-panel, .planning-decision-mobile-panel'),
        mobileSummary: summarize('.decision-mobile-calculator-summary, .planning-decision-mobile-summary'),
        sidebar: summarize('.decision-sidebar'),
        stepLabels: summarize('.decision-step-labels'),
        desktopShell: summarize('.decision-desktop-shell, .planning-decision-desktop-shell'),
        desktopHeader: summarize('.decision-engine-header'),
        desktopProgress: summarize('.decision-progress'),
        desktopLayout: summarize('.decision-layout'),
        legacyMobile: summarize('.decision-mobile-shell'),
      };
      const results = {
        decisionResults: summarize('.decision-result'),
        pdResults: summarize('.tool-result[data-result-ready="true"]'),
        nextStepCards: summarize('.tool-next-step'),
      };

      const body = document.body;
      const documentWidth = Math.max(
        document.documentElement.scrollWidth,
        body ? body.scrollWidth : 0
      );
      const rootWidth = Math.ceil(root.getBoundingClientRect().width);
      const overflowX = documentWidth - viewportWidth;

      return {
        viewportWidth,
        toolKind: root.getAttribute('data-tool-kind') || '',
        shells,
        results,
        rootWidth,
        documentWidth,
        overflowX,
        hasHorizontalOverflow: overflowX > 1,
        bodyTextLength: (root.innerText || '').trim().length,
      };
    })()
  `;
}

function buildInitialAuditExpression(toolSlug, viewportWidth) {
  const slug = JSON.stringify(toolSlug);
  return `
    (function () {
      const toolSlug = ${slug};
      const viewportWidth = ${viewportWidth};
      const root = document.querySelector('[data-tool-root="' + toolSlug + '"]');
      if (!root) {
        throw new Error('Missing tool root for initial audit');
      }

      function isVisible(node) {
        if (!node) {
          return false;
        }
        const style = window.getComputedStyle(node);
        const rect = node.getBoundingClientRect();
        return (
          style.display !== 'none' &&
          style.visibility !== 'hidden' &&
          style.opacity !== '0' &&
          rect.width > 0 &&
          rect.height > 0
        );
      }

      function summarize(selector) {
        const nodes = Array.from(root.querySelectorAll(selector));
        return {
          total: nodes.length,
          visible: nodes.filter(isVisible).length,
        };
      }

      return {
        viewportWidth,
        toolKind: root.getAttribute('data-tool-kind') || '',
        mobileShellVisible: summarize('.decision-mobile-calculator-shell, .planning-decision-mobile-shell').visible,
        desktopShellVisible: summarize('.decision-desktop-shell, .planning-decision-desktop-shell').visible,
        legacyMobileVisible: summarize('.decision-mobile-shell').visible,
        fallbackVisible: summarize('[data-tool-fallback="true"]').visible,
        bodyTextLength: (root.innerText || '').trim().length,
      };
    })()
  `;
}

async function setViewport(cdp, width) {
  await cdp.send("Emulation.setDeviceMetricsOverride", {
    width,
    height: 2400,
    deviceScaleFactor: 1,
    mobile: width < 768,
  });
}

async function captureScreenshot(cdp, toolSlug, width) {
  const screenshot = await cdp.send("Page.captureScreenshot", {
    format: "png",
    fromSurface: true,
  });
  fs.mkdirSync(screenshotDir, { recursive: true });
  fs.writeFileSync(
    path.join(screenshotDir, `${toolSlug}-${width}.png`),
    Buffer.from(screenshot.data, "base64")
  );
}

async function auditViewport(cdp, toolSlug, port, width) {
  await setViewport(cdp, width);
  const url = `http://127.0.0.1:${port}/output/tools/${toolSlug}/`;
  const loadPromise = cdp.waitFor("Page.loadEventFired");
  await cdp.send("Page.navigate", { url });
  await loadPromise;

  const initialEvaluation = await cdp.send("Runtime.evaluate", {
    expression: buildInitialAuditExpression(toolSlug, width),
    awaitPromise: false,
    returnByValue: true,
  });
  if (initialEvaluation.exceptionDetails) {
    throw new Error(
      `[${toolSlug}@${width}] ${initialEvaluation.exceptionDetails.text || "Initial audit failed"}`
    );
  }
  const initial = valueFromRemote(initialEvaluation.result);
  assert(initial, `[${toolSlug}@${width}] Missing initial audit payload`);

  const interaction = await cdp.send("Runtime.evaluate", {
    expression: buildInteractionExpression(toolSlug),
    awaitPromise: true,
    returnByValue: true,
  });
  if (interaction.exceptionDetails) {
    throw new Error(
      `[${toolSlug}@${width}] ${interaction.exceptionDetails.text || "Interaction failed"}`
    );
  }

  await wait(250);

  const evaluation = await cdp.send("Runtime.evaluate", {
    expression: buildAuditExpression(toolSlug, width),
    awaitPromise: false,
    returnByValue: true,
  });
  if (evaluation.exceptionDetails) {
    throw new Error(
      `[${toolSlug}@${width}] ${evaluation.exceptionDetails.text || "Audit failed"}`
    );
  }

  const value = valueFromRemote(evaluation.result);
  assert(value, `[${toolSlug}@${width}] Missing audit payload`);
  value.initial = initial;

  await captureScreenshot(cdp, toolSlug, width);
  return value;
}

async function launchEdge(edgePath) {
  const userDataDir = fs.mkdtempSync(path.join(os.tmpdir(), "ukpg-edge-smoke-"));
  const browser = spawn(
    edgePath,
    [
      "--headless=new",
      "--disable-gpu",
      "--no-first-run",
      "--no-default-browser-check",
      "--remote-debugging-port=0",
      `--user-data-dir=${userDataDir}`,
      "about:blank",
    ],
    {
      stdio: "ignore",
    }
  );

  browser.unref();

  try {
    const debugPort = await waitForDevToolsPort(userDataDir);
    const wsUrl = await waitForTarget(debugPort);
    return { browser, userDataDir, wsUrl };
  } catch (error) {
    browser.kill("SIGKILL");
    throw error;
  }
}

async function closeBrowser(browser, userDataDir) {
  if (browser && !browser.killed) {
    spawnSync("taskkill", ["/PID", String(browser.pid), "/T", "/F"], {
      stdio: "ignore",
    });
    await wait(500);
  }
  try {
    fs.rmSync(userDataDir, { recursive: true, force: true });
  } catch (error) {
    // Temporary profile may still be locked for a moment.
  }
}

function listToolSlugs() {
  return fs
    .readdirSync(toolsDir, { withFileTypes: true })
    .filter((entry) => entry.isDirectory())
    .map((entry) => entry.name)
    .sort();
}

function validateAudit(toolSlug, entry) {
  const width = entry.viewportWidth;
  if (width <= 430 && entry.toolKind !== "form") {
    assert(entry.initial.mobileShellVisible === 1, `[${toolSlug}@${width}] initial mobile shell was not visible`);
    assert(entry.initial.desktopShellVisible === 0, `[${toolSlug}@${width}] desktop shell was visible on initial render`);
    assert(entry.initial.legacyMobileVisible === 0, `[${toolSlug}@${width}] legacy mobile shell was visible on initial render`);
    assert(entry.initial.fallbackVisible === 0, `[${toolSlug}@${width}] fallback content was visible after initial render`);
  }

  if (entry.toolKind === "form") {
    assert(!entry.hasHorizontalOverflow, `[${toolSlug}@${width}] horizontal overflow detected`);
    return;
  }

  if (width <= 430) {
    assert(entry.shells.mobile.visible === 1, `[${toolSlug}@${width}] mobile shell should be the only visible shell`);
    assert(entry.shells.mobileHeader.visible === 1, `[${toolSlug}@${width}] mobile header is missing`);
    assert(entry.shells.mobileBody.visible === 1, `[${toolSlug}@${width}] mobile body is missing`);
    assert(entry.shells.mobilePanel.visible === 1, `[${toolSlug}@${width}] mobile main panel is missing`);
    assert(entry.shells.mobileSummary.visible === 1, `[${toolSlug}@${width}] mobile summary panel is missing`);
    assert(entry.shells.desktopShell.visible === 0, `[${toolSlug}@${width}] desktop shell is still visible`);
    assert(entry.shells.desktopHeader.visible === 0, `[${toolSlug}@${width}] desktop header is still visible`);
    assert(entry.shells.desktopProgress.visible === 0, `[${toolSlug}@${width}] desktop progress is still visible`);
    assert(entry.shells.desktopLayout.visible === 0, `[${toolSlug}@${width}] desktop layout is still visible`);
    assert(entry.shells.legacyMobile.visible === 0, `[${toolSlug}@${width}] legacy mobile shell is still visible`);
  } else if (width >= 768) {
    assert(entry.shells.desktopShell.visible === 1, `[${toolSlug}@${width}] desktop shell should be visible`);
    assert(entry.shells.desktopHeader.visible === 1, `[${toolSlug}@${width}] desktop header should be visible`);
    assert(entry.shells.desktopProgress.visible === 1, `[${toolSlug}@${width}] desktop progress should be visible`);
    assert(entry.shells.desktopLayout.visible === 1, `[${toolSlug}@${width}] desktop layout should be visible`);
    assert(entry.shells.mobile.visible === 0, `[${toolSlug}@${width}] mobile shell should not be visible`);
    assert(entry.shells.legacyMobile.visible === 0, `[${toolSlug}@${width}] legacy mobile shell should not be visible`);
  }

  assert(entry.shells.stepLabels.visible === 1, `[${toolSlug}@${width}] step labels are missing`);

  assert(!entry.hasHorizontalOverflow, `[${toolSlug}@${width}] horizontal overflow detected`);
}

async function main() {
  const edgePath = findEdge();
  assert(edgePath, "Microsoft Edge was not found in the expected install paths");

  const requestedSlugs = process.argv.slice(2);
  const toolSlugs = requestedSlugs.length ? requestedSlugs : listToolSlugs();

  const server = createServer();
  await new Promise((resolve) => server.listen(0, "127.0.0.1", resolve));
  const { port } = server.address();

  let browserSession = null;
  let cdp = null;

  try {
    browserSession = await launchEdge(edgePath);
    cdp = await createCdpClient(browserSession.wsUrl);

    await cdp.send("Page.enable");
    await cdp.send("Runtime.enable");

    const report = {};

    for (const toolSlug of toolSlugs) {
      report[toolSlug] = [];
      for (const width of VIEWPORTS) {
        const entry = await auditViewport(cdp, toolSlug, port, width);
        validateAudit(toolSlug, entry);
        report[toolSlug].push(entry);
        console.log(`[AUDIT OK] ${toolSlug} @ ${width}px`);
      }
    }

    fs.mkdirSync(screenshotDir, { recursive: true });
    fs.writeFileSync(reportPath, JSON.stringify(report, null, 2));
  } finally {
    if (cdp) {
      await cdp.close();
    }
    if (browserSession) {
      await closeBrowser(browserSession.browser, browserSession.userDataDir);
    }
    await new Promise((resolve) => server.close(resolve));
  }
}

main().catch((error) => {
  console.error(error.stack || String(error));
  process.exit(1);
});
