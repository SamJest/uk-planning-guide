(function () {
  "use strict";

  // Public frontend configuration for Planning Route Check enquiries.
  // The endpoint URL is visible to site visitors. Do not add private API keys,
  // bearer tokens, webhook secrets or service credentials here.
  // Keep secrets only in the receiving backend or workflow tool.
  window.UKPG_LEAD_CONFIG = {
    enabled: true,
    // Production example after deploying the separate receiver:
    // endpoint: "https://YOUR-WORKER.your-subdomain.workers.dev/leads",
    endpoint: "",
    method: "POST",
    provider: "generic",
    // Used only for the fallback mailto link when endpoint is blank.
    owner_email: "",
    // Keep this as a local path so redirects remain on ukplanningguide.co.uk.
    success_redirect: "/planning-help/thank-you/",
    request_timeout_ms: 10000,
    // Set false in production. Debug logging must never include private keys.
    debug: false
  };

  // Backwards-compatible alias used by the Batch 1 implementation.
  window.UKPG_LEAD_CAPTURE_CONFIG = window.UKPG_LEAD_CONFIG;
})();
