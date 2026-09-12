/*
 * UK Planning Guide Planning Lead Worker - Cloudflare dashboard version.
 *
 * This file is intentionally self-contained for Cloudflare dashboard copy/paste
 * deployment. Keep the source-module version in src/ as the maintainable source
 * of truth for local development and tests.
 *
 * Required binding:
 * - LEADS_DB: Cloudflare D1 database using schema.sql
 *
 * Supported environment variables/secrets:
 * - ALLOWED_ORIGINS
 * - HASH_SALT
 * - NOTIFY_WEBHOOK_URL
 * - NOTIFY_WEBHOOK_SECRET
 * - OWNER_EMAIL
 * - RATE_LIMIT_PER_HOUR
 * - DEBUG_VALIDATION
 *
 * Do not paste real secrets into this file. Configure secrets and variables in
 * the Cloudflare dashboard or with Wrangler.
 */
const MAX_BODY_BYTES = 64 * 1024;
const MIN_FORM_ELAPSED_MS = 2500;
const MAX_TEXT = {
  name: 120,
  email: 254,
  phone: 80,
  postcode_or_town: 120,
  council: 160,
  project_type: 160,
  property_type: 160,
  timeframe: 120,
  desired_help: 180,
  route_result: 220,
  confidence: 40,
  user_notes: 3000,
  page_url: 600,
  referrer: 600,
  source: 80
};

const LEAD_STATUSES = [
  "New",
  "Checked",
  "Needs reply",
  "Match needed",
  "Sent to professional",
  "Unmatched",
  "Rejected/spam",
  "Archived"
];

const SCRIPT_PATTERN = /<\s*script\b|javascript:|onerror\s*=|onload\s*=|<\s*iframe\b|<\/\s*(script|iframe)\s*>/i;
const SPAM_TEXT_PATTERN = /\b(?:casino|viagra|loan offer|crypto investment|telegram\s*:|whatsapp\s*:)\b/i;
const EMAIL_PATTERN = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/;
const FIELD_ALIASES = {
  submitted_at: ["submitted_at", "submittedAt"],
  page_url: ["page_url", "pageUrl"],
  referrer: ["referrer"],
  project_type: ["project_type", "projectType"],
  property_type: ["property_type", "propertyType"],
  postcode_or_town: ["postcode_or_town", "postcodeOrTown"],
  council: ["council"],
  restrictions: ["restrictions"],
  timeframe: ["timeframe"],
  desired_help: ["desired_help", "desiredHelp"],
  route_result: ["route_result", "routeResult"],
  confidence: ["confidence"],
  user_notes: ["user_notes", "userNotes", "notes"],
  name: ["name", "fullName"],
  email: ["email"],
  phone: ["phone"],
  consent_contact: ["consent_contact", "consentContact"],
  consent_share: ["consent_share", "consentShare"],
  source: ["source"],
  website: ["website", "company", "url", "_gotcha"],
  form_elapsed_ms: ["form_elapsed_ms", "formElapsedMs"]
};

function asText(value) {
  if (value === null || value === undefined) {
    return "";
  }
  return String(value).replace(/\r\n/g, "\n").replace(/\r/g, "\n").trim();
}

function limitText(value, maxLength) {
  const clean = asText(value);
  if (!maxLength || clean.length <= maxLength) {
    return clean;
  }
  return clean.slice(0, maxLength);
}

function safeKeys(value) {
  if (!value || typeof value !== "object" || Array.isArray(value)) {
    return [];
  }
  return Object.keys(value)
    .filter((key) => !["name", "email", "phone", "user_notes", "userNotes", "notes"].includes(key))
    .slice(0, 40);
}

function unwrapSubmission(input) {
  const topLevelKeys = safeKeys(input);
  if (
    input &&
    typeof input === "object" &&
    !Array.isArray(input) &&
    input.payload &&
    typeof input.payload === "object" &&
    !Array.isArray(input.payload)
  ) {
    return {
      payload: input.payload,
      originalPayload: input,
      topLevelKeys,
      payloadKeys: safeKeys(input.payload),
      wrapped: true
    };
  }
  return {
    payload: input,
    originalPayload: input,
    topLevelKeys,
    payloadKeys: safeKeys(input),
    wrapped: false
  };
}

function field(payload, canonicalKey) {
  const aliases = FIELD_ALIASES[canonicalKey] || [canonicalKey];
  for (const key of aliases) {
    if (Object.prototype.hasOwnProperty.call(payload, key)) {
      return payload[key];
    }
  }
  return undefined;
}

function requiredText(payload, canonicalKey, errors) {
  const value = asText(field(payload, canonicalKey));
  if (!value) {
    errors.push(`Required ${canonicalKey.replace(/_/g, " ")} is missing.`);
  }
  return value;
}

function isTrue(value) {
  return value === true || value === "true" || value === "yes" || value === 1 || value === "1";
}

function wantsProfessionalSharing(payload) {
  const desired = asText(field(payload, "desired_help")).toLowerCase();
  if (!desired) {
    return true;
  }
  return desired.indexOf("just show me") === -1 && desired.indexOf("route only") === -1;
}

function normalizeRestrictions(value) {
  if (Array.isArray(value)) {
    return value.map((item) => limitText(item, 120)).filter(Boolean).slice(0, 16);
  }
  if (!value) {
    return [];
  }
  return [limitText(value, 120)].filter(Boolean);
}

function textValues(payload) {
  return [
    field(payload, "name"),
    field(payload, "email"),
    field(payload, "phone"),
    field(payload, "postcode_or_town"),
    field(payload, "council"),
    field(payload, "project_type"),
    field(payload, "property_type"),
    field(payload, "timeframe"),
    field(payload, "desired_help"),
    field(payload, "route_result"),
    field(payload, "user_notes"),
    field(payload, "page_url"),
    field(payload, "referrer")
  ].map(asText);
}

function hasSuspiciousText(payload) {
  return textValues(payload).some((value) => SCRIPT_PATTERN.test(value) || SPAM_TEXT_PATTERN.test(value));
}

function validateLeadPayload(input, now = new Date(), options = {}) {
  const errors = [];
  const spamReasons = [];
  let spamScore = 0;
  const unwrapped = unwrapSubmission(input);
  const payload = unwrapped.payload;
  const debugValidation = Boolean(options.debugValidation);
  const diagnostics = debugValidation ? {
    wrapped: unwrapped.wrapped,
    top_level_keys: unwrapped.topLevelKeys,
    payload_keys: unwrapped.payloadKeys
  } : undefined;

  if (!payload || typeof payload !== "object" || Array.isArray(payload)) {
    return {
      ok: false,
      error: "validation_failed",
      message: "Expected a JSON object.",
      errors: ["Expected a JSON object."],
      diagnostics
    };
  }

  const honeypot = asText(field(payload, "website"));
  if (honeypot) {
    spamScore += 5;
    spamReasons.push("honeypot");
  }

  const elapsed = Number(field(payload, "form_elapsed_ms"));
  if (Number.isFinite(elapsed) && elapsed > 0 && elapsed < MIN_FORM_ELAPSED_MS) {
    spamScore += 3;
    spamReasons.push("too_fast");
  }

  if (hasSuspiciousText(payload)) {
    spamScore += 4;
    spamReasons.push("suspicious_text");
  }

  const projectType = requiredText(payload, "project_type", errors);
  const propertyType = requiredText(payload, "property_type", errors);
  const postcodeOrTown = asText(field(payload, "postcode_or_town"));
  const council = asText(field(payload, "council"));
  if (!postcodeOrTown && !council) {
    errors.push("A postcode, town or council is required.");
  }
  const routeResult = requiredText(payload, "route_result", errors);
  const confidence = requiredText(payload, "confidence", errors);
  const name = requiredText(payload, "name", errors);
  const rawEmail = requiredText(payload, "email", errors);
  const email = rawEmail.toLowerCase();

  if (rawEmail && !EMAIL_PATTERN.test(email)) {
    errors.push("A valid email address is required.");
  }

  const userNotes = asText(field(payload, "user_notes"));
  if (name.length > MAX_TEXT.name) {
    errors.push("Name is too long.");
  }
  if (postcodeOrTown.length > MAX_TEXT.postcode_or_town) {
    errors.push("Location is too long.");
  }
  if (userNotes.length > MAX_TEXT.user_notes) {
    errors.push("Project notes are too long.");
  }
  if (rawEmail.length > MAX_TEXT.email) {
    errors.push("Email address is too long.");
  }

  const consentContact = isTrue(field(payload, "consent_contact"));
  const consentShare = isTrue(field(payload, "consent_share"));
  if (!consentContact) {
    errors.push("Required contact consent is missing.");
  }
  if (wantsProfessionalSharing(payload) && !consentShare) {
    errors.push("Required sharing consent is missing.");
  }

  if (errors.length) {
    return {
      ok: false,
      error: "validation_failed",
      message: errors[0],
      errors,
      diagnostics
    };
  }

  const receivedAt = now.toISOString();
  const isSpam = spamScore >= 3;
  const normalized = {
    submitted_at: limitText(field(payload, "submitted_at") || receivedAt, 80),
    received_at: receivedAt,
    source: limitText(field(payload, "source") || "planning_route_check", MAX_TEXT.source),
    page_url: limitText(field(payload, "page_url"), MAX_TEXT.page_url),
    referrer: limitText(field(payload, "referrer"), MAX_TEXT.referrer),
    project_type: limitText(projectType, MAX_TEXT.project_type),
    property_type: limitText(propertyType, MAX_TEXT.property_type),
    postcode_or_town: limitText(postcodeOrTown, MAX_TEXT.postcode_or_town),
    council: limitText(council, MAX_TEXT.council),
    restrictions: normalizeRestrictions(field(payload, "restrictions")),
    timeframe: limitText(field(payload, "timeframe"), MAX_TEXT.timeframe),
    desired_help: limitText(field(payload, "desired_help"), MAX_TEXT.desired_help),
    route_result: limitText(routeResult, MAX_TEXT.route_result),
    confidence: limitText(confidence, MAX_TEXT.confidence),
    user_notes: limitText(userNotes, MAX_TEXT.user_notes),
    name: limitText(name, MAX_TEXT.name),
    email: limitText(email, MAX_TEXT.email),
    phone: limitText(field(payload, "phone"), MAX_TEXT.phone),
    consent_contact: consentContact,
    consent_share: consentShare,
    status: isSpam ? "Rejected/spam" : "New",
    spam_score: spamScore,
    spam_reasons: spamReasons,
    raw_payload_json: JSON.stringify(unwrapped.originalPayload)
  };

  return {
    ok: true,
    normalized,
    isSpam,
    spamScore,
    spamReasons
  };
}

function safeValidationResponse(result, debugValidation = false) {
  const response = {
    ok: false,
    error: result.error || "validation_failed",
    message: result.message || "The enquiry details could not be accepted."
  };
  if (debugValidation && result.diagnostics) {
    response.diagnostics = result.diagnostics;
  }
  return response;
}

function buildOwnerNotification(lead, env = {}) {
  const payload = {
    lead_id: lead.id,
    submitted_at: lead.submitted_at,
    project_type: lead.project_type,
    location: lead.postcode_or_town,
    council: lead.council,
    route_result: lead.route_result,
    confidence: lead.confidence,
    desired_help: lead.desired_help,
    name: lead.name,
    email: lead.email,
    phone: lead.phone,
    notes: lead.user_notes,
    consent: {
      contact: Boolean(lead.consent_contact),
      share: Boolean(lead.consent_share)
    },
    source_page: lead.page_url,
    status: lead.status
  };

  if (env.OWNER_EMAIL) {
    payload.owner_email = String(env.OWNER_EMAIL);
  }

  return payload;
}

async function notifyOwner(lead, env = {}, fetcher = fetch) {
  const webhookUrl = String(env.NOTIFY_WEBHOOK_URL || "").trim();
  if (!webhookUrl) {
    return { attempted: false, ok: true };
  }

  const headers = {
    "Content-Type": "application/json"
  };
  const secret = String(env.NOTIFY_WEBHOOK_SECRET || "").trim();
  if (secret) {
    headers["X-UKPG-Webhook-Secret"] = secret;
  }

  const response = await fetcher(webhookUrl, {
    method: "POST",
    headers,
    body: JSON.stringify(buildOwnerNotification(lead, env))
  });

  if (!response.ok) {
    throw new Error(`Notification webhook returned ${response.status}`);
  }

  return { attempted: true, ok: true, status: response.status };
}


const JSON_HEADERS = {
  "Content-Type": "application/json; charset=utf-8",
  "Cache-Control": "no-store"
};

function jsonResponse(body, status = 200, extraHeaders = {}) {
  return new Response(JSON.stringify(body), {
    status,
    headers: {
      ...JSON_HEADERS,
      ...extraHeaders
    }
  });
}

function parseAllowedOrigins(env = {}) {
  return String(env.ALLOWED_ORIGINS || "")
    .split(",")
    .map((item) => item.trim())
    .filter(Boolean);
}

function corsHeaders(request, env = {}) {
  const origin = request.headers.get("Origin") || "";
  const allowedOrigins = parseAllowedOrigins(env);
  const headers = {
    "Access-Control-Allow-Methods": "POST, OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type",
    "Access-Control-Max-Age": "86400",
    "Vary": "Origin"
  };

  if (!origin) {
    return headers;
  }
  if (allowedOrigins.includes("*") || allowedOrigins.includes(origin)) {
    headers["Access-Control-Allow-Origin"] = origin;
  }
  return headers;
}

function isAllowedOrigin(request, env = {}) {
  const origin = request.headers.get("Origin") || "";
  if (!origin) {
    return true;
  }
  const allowedOrigins = parseAllowedOrigins(env);
  return allowedOrigins.includes("*") || allowedOrigins.includes(origin);
}

function generateLeadId() {
  if (crypto && typeof crypto.randomUUID === "function") {
    return crypto.randomUUID();
  }
  return `lead_${Date.now()}_${Math.random().toString(36).slice(2, 10)}`;
}

async function sha256Hex(value) {
  if (!value) {
    return "";
  }
  const data = new TextEncoder().encode(value);
  const digest = await crypto.subtle.digest("SHA-256", data);
  return [...new Uint8Array(digest)]
    .map((byte) => byte.toString(16).padStart(2, "0"))
    .join("");
}

async function requestHash(value, salt) {
  const clean = String(value || "").trim();
  const secret = String(salt || "").trim();
  if (!clean || !secret) {
    return "";
  }
  return sha256Hex(`${secret}:${clean}`);
}

function getDatabase(env = {}) {
  return env.LEADS_DB || env.DB || null;
}

async function applyRateLimitIfNeeded(env, lead) {
  const db = getDatabase(env);
  if (!db || !lead.ip_hash || lead.status === "Rejected/spam") {
    return lead;
  }

  const limit = Number(env.RATE_LIMIT_PER_HOUR || 12);
  if (!Number.isFinite(limit) || limit <= 0) {
    return lead;
  }

  const since = new Date(Date.now() - 60 * 60 * 1000).toISOString();
  try {
    const row = await db
      .prepare("SELECT COUNT(*) AS count FROM planning_leads WHERE ip_hash = ? AND received_at >= ?")
      .bind(lead.ip_hash, since)
      .first();
    if (row && Number(row.count || 0) >= limit) {
      return {
        ...lead,
        status: "Rejected/spam",
        spam_score: Math.max(Number(lead.spam_score || 0), 4)
      };
    }
  } catch (error) {
    console.warn("Lead rate-limit check skipped", error && error.message ? error.message : error);
  }
  return lead;
}

async function storeLead(env, lead) {
  const db = getDatabase(env);
  if (!db) {
    throw new Error("D1 database binding LEADS_DB is not configured.");
  }

  await db
    .prepare(
      `INSERT INTO planning_leads (
        id, submitted_at, received_at, source, page_url, referrer,
        project_type, property_type, postcode_or_town, council, restrictions_json,
        timeframe, desired_help, route_result, confidence, user_notes,
        name, email, phone, consent_contact, consent_share, status,
        ip_hash, user_agent_hash, spam_score, raw_payload_json, updated_at
      ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)`
    )
    .bind(
      lead.id,
      lead.submitted_at,
      lead.received_at,
      lead.source,
      lead.page_url,
      lead.referrer,
      lead.project_type,
      lead.property_type,
      lead.postcode_or_town,
      lead.council,
      JSON.stringify(lead.restrictions || []),
      lead.timeframe,
      lead.desired_help,
      lead.route_result,
      lead.confidence,
      lead.user_notes,
      lead.name,
      lead.email,
      lead.phone,
      lead.consent_contact ? 1 : 0,
      lead.consent_share ? 1 : 0,
      lead.status,
      lead.ip_hash,
      lead.user_agent_hash,
      Number(lead.spam_score || 0),
      lead.raw_payload_json,
      lead.updated_at
    )
    .run();
}

async function readJsonRequest(request) {
  const declaredLength = Number(request.headers.get("Content-Length") || 0);
  if (declaredLength > MAX_BODY_BYTES) {
    return { error: "payload_too_large" };
  }

  const raw = await request.text();
  const actualLength = new TextEncoder().encode(raw).length;
  if (actualLength > MAX_BODY_BYTES) {
    return { error: "payload_too_large" };
  }

  try {
    return { payload: JSON.parse(raw) };
  } catch (_error) {
    return { error: "invalid_json" };
  }
}

async function handleRequest(request, env = {}, ctx = {}) {
  const headers = corsHeaders(request, env);
  const url = new URL(request.url);

  if (request.method === "OPTIONS") {
    if (!isAllowedOrigin(request, env)) {
      return jsonResponse({ ok: false, error: "origin_not_allowed" }, 403, headers);
    }
    return new Response(null, { status: 204, headers });
  }

  if (request.method === "GET" && url.pathname === "/health") {
    return jsonResponse({ ok: true, status: "healthy" }, 200, headers);
  }

  if (url.pathname !== "/leads") {
    return jsonResponse({ ok: false, error: "not_found" }, 404, headers);
  }

  if (request.method !== "POST") {
    return jsonResponse({ ok: false, error: "method_not_allowed" }, 405, headers);
  }

  if (!isAllowedOrigin(request, env)) {
    return jsonResponse({ ok: false, error: "origin_not_allowed" }, 403, headers);
  }

  const parsed = await readJsonRequest(request);
  if (parsed.error === "payload_too_large") {
    return jsonResponse({
      ok: false,
      error: "payload_too_large",
      message: "The enquiry is too large to submit."
    }, 413, headers);
  }
  if (parsed.error === "invalid_json") {
    return jsonResponse({
      ok: false,
      error: "invalid_json",
      message: "The enquiry could not be read."
    }, 400, headers);
  }

  const debugValidation = String(env.DEBUG_VALIDATION || "").toLowerCase() === "true";
  const validation = validateLeadPayload(parsed.payload, new Date(), { debugValidation });
  if (!validation.ok) {
    return jsonResponse(safeValidationResponse(validation, debugValidation), 400, headers);
  }

  const ip = request.headers.get("CF-Connecting-IP") || request.headers.get("X-Forwarded-For") || "";
  const userAgent = request.headers.get("User-Agent") || "";
  let lead = {
    ...validation.normalized,
    id: generateLeadId(),
    ip_hash: await requestHash(ip, env.HASH_SALT),
    user_agent_hash: await requestHash(userAgent, env.HASH_SALT),
    updated_at: validation.normalized.received_at
  };

  try {
    lead = await applyRateLimitIfNeeded(env, lead);
    await storeLead(env, lead);
  } catch (error) {
    console.error("Lead storage failed", error && error.message ? error.message : error);
    return jsonResponse({
      ok: false,
      error: "server_error",
      message: "The enquiry could not be saved right now."
    }, 500, headers);
  }

  if (lead.status !== "Rejected/spam") {
    const notifyPromise = notifyOwner(lead, env).catch((error) => {
      console.warn("Lead notification failed", error && error.message ? error.message : error);
    });
    if (ctx && typeof ctx.waitUntil === "function") {
      ctx.waitUntil(notifyPromise);
    } else {
      await notifyPromise;
    }
  }

  if (lead.status === "Rejected/spam") {
    return jsonResponse({ ok: true, status: "received" }, 200, headers);
  }

  return jsonResponse({
    ok: true,
    lead_id: lead.id,
    status: "received"
  }, 200, headers);
}

export default {
  fetch: handleRequest
};
