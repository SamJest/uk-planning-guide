import assert from "node:assert/strict";
import { handleRequest } from "../src/worker.js";
import { validateLeadPayload } from "../src/validation.js";

function validPayload(overrides = {}) {
  return {
    submitted_at: "2026-05-11T08:00:00.000Z",
    page_url: "https://ukplanningguide.co.uk/tools/planning-route-check/",
    referrer: "",
    user_agent: "Test browser",
    project_type: "Garden room / outbuilding",
    property_type: "Semi-detached house",
    postcode_or_town: "Exampletown EX1",
    council: "Example Council",
    restrictions: ["Not sure"],
    timeframe: "Within 3 months",
    desired_help: "I may want professional planning/design help",
    route_result: "Permitted development may be possible",
    confidence: "Medium",
    user_notes: "Fake test payload only.",
    name: "Example Homeowner",
    email: "example.homeowner@example.com",
    phone: "07123 000000",
    consent_contact: true,
    consent_share: true,
    source: "planning_route_check",
    website: "",
    form_elapsed_ms: 5000,
    ...overrides
  };
}

function camelPayload(overrides = {}) {
  return {
    submittedAt: "2026-05-11T08:00:00.000Z",
    pageUrl: "https://ukplanningguide.co.uk/tools/planning-route-check/",
    referrer: "",
    userAgent: "Test browser",
    projectType: "Garden room / outbuilding",
    propertyType: "Semi-detached house",
    postcodeOrTown: "Exampletown EX1",
    council: "Example Council",
    restrictions: ["Not sure"],
    timeframe: "Within 3 months",
    desiredHelp: "I may want professional planning/design help",
    routeResult: "Permitted development may be possible",
    confidence: "Medium",
    userNotes: "Fake test payload only.",
    name: "Example Homeowner",
    email: "example.homeowner@example.com",
    phone: "07123 000000",
    consentContact: true,
    consentShare: true,
    source: "planning_route_check",
    website: "",
    formElapsedMs: 5000,
    ...overrides
  };
}

class FakeD1 {
  constructor() {
    this.rows = [];
    this.count = 0;
  }

  prepare(sql) {
    return {
      bind: (...values) => ({
        first: async () => ({ count: this.count }),
        run: async () => {
          if (/INSERT INTO planning_leads/i.test(sql)) {
            this.rows.push(values);
          }
          return { success: true };
        }
      })
    };
  }
}

function env(overrides = {}) {
  return {
    ALLOWED_ORIGINS: "https://ukplanningguide.co.uk",
    HASH_SALT: "test-salt-only",
    LEADS_DB: new FakeD1(),
    ...overrides
  };
}

function request(method, payload, headers = {}) {
  const options = {
    method,
    headers: {
      Origin: "https://ukplanningguide.co.uk",
      "Content-Type": "application/json",
      "User-Agent": "Worker test",
      "CF-Connecting-IP": "203.0.113.10",
      ...headers
    }
  };
  if (payload !== undefined) {
    options.body = typeof payload === "string" ? payload : JSON.stringify(payload);
  }
  return new Request("https://worker.example/leads", options);
}

async function json(response) {
  return response.json();
}

async function testValidPayloadAccepted() {
  const testEnv = env();
  const response = await handleRequest(request("POST", validPayload()), testEnv, {});
  const body = await json(response);
  assert.equal(response.status, 200);
  assert.equal(body.ok, true);
  assert.equal(body.status, "received");
  assert.ok(body.lead_id);
  assert.equal(testEnv.LEADS_DB.rows.length, 1);
  assert.equal(JSON.stringify(body).includes("example.homeowner@example.com"), false);
}

async function testAcceptedPayloadShapes() {
  const cases = [
    ["exact frontend payload", validPayload()],
    ["wrapped snake_case payload", { payload: validPayload() }],
    ["unwrapped snake_case payload", validPayload({ projectType: "Ignored duplicate" })],
    ["wrapped camelCase payload", { payload: camelPayload() }]
  ];

  for (const [label, payload] of cases) {
    const testEnv = env();
    const response = await handleRequest(request("POST", payload), testEnv, {});
    const body = await json(response);
    assert.equal(response.status, 200, label);
    assert.equal(body.ok, true, label);
    assert.equal(testEnv.LEADS_DB.rows.length, 1, label);
    assert.equal(testEnv.LEADS_DB.rows[0][6], "Garden room / outbuilding", label);
  }
}

async function testDebugValidationShowsKeysWithoutPii() {
  const response = await handleRequest(request("POST", {
    payload: {
      projectType: "",
      propertyType: "Semi-detached house",
      name: "Sensitive Name",
      email: "sensitive@example.com"
    }
  }), env({ DEBUG_VALIDATION: "true" }), {});
  const text = await response.text();
  assert.equal(response.status, 400);
  assert.match(text, /diagnostics/);
  assert.match(text, /projectType/);
  assert.equal(text.includes("Sensitive Name"), false);
  assert.equal(text.includes("sensitive@example.com"), false);
}

function testValidationRejectsBadPayloads() {
  assert.equal(validateLeadPayload(validPayload({ consent_contact: false })).ok, false);
  assert.equal(validateLeadPayload(validPayload({ email: "not-an-email" })).ok, false);
  assert.equal(validateLeadPayload(validPayload({ project_type: "" })).ok, false);
  assert.equal(validateLeadPayload(validPayload({ user_notes: "x".repeat(3001) })).ok, false);
}

async function testMissingConsentRejectedWithoutPii() {
  const response = await handleRequest(request("POST", validPayload({
    consent_contact: false,
    name: "Sensitive Name",
    email: "sensitive@example.com"
  })), env(), {});
  const text = await response.text();
  assert.equal(response.status, 400);
  assert.equal(text.includes("Sensitive Name"), false);
  assert.equal(text.includes("sensitive@example.com"), false);
  assert.match(text, /Required contact consent is missing/);
}

async function testHoneypotIsAcceptedGenericallyAndMarkedSpam() {
  const testEnv = env();
  const response = await handleRequest(request("POST", validPayload({ website: "https://spam.example" })), testEnv, {});
  const body = await json(response);
  assert.equal(response.status, 200);
  assert.deepEqual(body, { ok: true, status: "received" });
  assert.equal(testEnv.LEADS_DB.rows.length, 1);
  assert.equal(testEnv.LEADS_DB.rows[0][21], "Rejected/spam");
}

async function testCorsAndMethods() {
  const optionsResponse = await handleRequest(request("OPTIONS"), env(), {});
  assert.equal(optionsResponse.status, 204);
  assert.equal(optionsResponse.headers.get("Access-Control-Allow-Origin"), "https://ukplanningguide.co.uk");

  const getResponse = await handleRequest(new Request("https://worker.example/leads", { method: "GET" }), env(), {});
  assert.equal(getResponse.status, 405);
}

async function testNotificationFailureDoesNotFailStoredLead() {
  const originalFetch = globalThis.fetch;
  globalThis.fetch = async () => new Response("no", { status: 500 });
  try {
    const testEnv = env({ NOTIFY_WEBHOOK_URL: "https://notify.example/hook" });
    const response = await handleRequest(request("POST", validPayload()), testEnv, {});
    const body = await json(response);
    assert.equal(response.status, 200);
    assert.equal(body.ok, true);
    assert.equal(testEnv.LEADS_DB.rows.length, 1);
  } finally {
    globalThis.fetch = originalFetch;
  }
}

async function testInvalidJsonAndOrigin() {
  const badJson = await handleRequest(request("POST", "{"), env(), {});
  assert.equal(badJson.status, 400);
  assert.equal((await json(badJson)).error, "invalid_json");

  const badOrigin = await handleRequest(request("POST", validPayload(), { Origin: "https://bad.example" }), env(), {});
  assert.equal(badOrigin.status, 403);
}

async function run() {
  testValidationRejectsBadPayloads();
  await testValidPayloadAccepted();
  await testAcceptedPayloadShapes();
  await testDebugValidationShowsKeysWithoutPii();
  await testMissingConsentRejectedWithoutPii();
  await testHoneypotIsAcceptedGenericallyAndMarkedSpam();
  await testCorsAndMethods();
  await testNotificationFailureDoesNotFailStoredLead();
  await testInvalidJsonAndOrigin();
  console.log("Worker tests passed");
}

run();
