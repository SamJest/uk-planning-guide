import { MAX_BODY_BYTES, safeValidationResponse, validateLeadPayload } from "./validation.js";
import { notifyOwner } from "./notifications.js";

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

export async function handleRequest(request, env = {}, ctx = {}) {
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
