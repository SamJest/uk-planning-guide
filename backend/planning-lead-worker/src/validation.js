export const MAX_BODY_BYTES = 64 * 1024;
export const MIN_FORM_ELAPSED_MS = 2500;
export const MAX_TEXT = {
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

export const LEAD_STATUSES = [
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

export function validateLeadPayload(input, now = new Date(), options = {}) {
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

export function safeValidationResponse(result, debugValidation = false) {
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
