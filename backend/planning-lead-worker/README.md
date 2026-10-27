# Planning Lead Worker

This package is a small Cloudflare Worker-style receiver for Planning Route Check enquiries. It is deployed separately from the static UK Planning Guide site, so the public site can remain static-first while real enquiries are stored server-side.

The worker:

- accepts `POST /leads` JSON submissions from the route-check form
- checks CORS against configured allowed origins
- validates required fields and consent server-side
- rejects invalid JSON, oversized payloads and invalid emails
- marks honeypot, very-fast or suspicious submissions as `Rejected/spam`
- stores leads in a Cloudflare D1 table
- hashes IP and user-agent signals with a secret salt when available
- optionally posts an owner notification to a configured webhook
- returns small JSON responses without stack traces or personal data

It does not build a partner directory, automate resale of leads, promise matching, or send personal details to analytics.

## Files

- `src/worker.js` - Worker request handling, CORS, storage and response handling
- `src/validation.js` - server-side validation, normalization and spam scoring
- `src/notifications.js` - optional webhook notification adapter
- `schema.sql` - D1-compatible storage schema
- `wrangler.example.toml` - deployment config template with placeholders only
- `test/worker.test.js` - dependency-free Node tests

## Deploy

1. Install and authenticate Wrangler outside this package using your normal Cloudflare workflow.
2. Copy `wrangler.example.toml` to `wrangler.toml`.
3. Fill in only safe public values in `wrangler.toml`, such as the worker name and allowed origins.
4. Create a D1 database:

```powershell
wrangler d1 create ukpg-planning-leads
```

5. Add the returned D1 `database_id` to `wrangler.toml`.
6. Apply the schema:

```powershell
wrangler d1 execute ukpg-planning-leads --file schema.sql
```

7. Add secrets with Wrangler. Do not write real secrets into the repository:

```powershell
wrangler secret put HASH_SALT
wrangler secret put NOTIFY_WEBHOOK_URL
wrangler secret put NOTIFY_WEBHOOK_SECRET
wrangler secret put OWNER_EMAIL
```

Only `HASH_SALT` is strongly recommended for request-signal hashing. Notification secrets are optional.

8. Deploy:

```powershell
wrangler deploy
```

## Environment Variables

Set these in Worker variables or secrets:

- `ALLOWED_ORIGINS`: comma-separated list, for example `https://ukplanningguide.co.uk,https://www.ukplanningguide.co.uk`
- `RATE_LIMIT_PER_HOUR`: optional per-IP-hash soft limit, default `12`
- `HASH_SALT`: secret salt used before hashing IP/user-agent signals
- `NOTIFY_WEBHOOK_URL`: optional webhook endpoint for owner notifications
- `NOTIFY_WEBHOOK_SECRET`: optional shared secret sent as `X-UKPG-Webhook-Secret`
- `OWNER_EMAIL`: optional value included in the webhook payload if your workflow needs it

Do not put private API keys, email provider tokens, database credentials or webhook secrets into `assets/js/lead-config.js`.

## Frontend Config

After deployment, update the static frontend config:

```js
window.UKPG_LEAD_CONFIG = {
  enabled: true,
  endpoint: "https://YOUR-WORKER.your-subdomain.workers.dev/leads",
  method: "POST",
  provider: "generic",
  owner_email: "",
  success_redirect: "/planning-help/thank-you/",
  request_timeout_ms: 10000,
  debug: false
};
```

The endpoint is public. That is expected. The worker performs the serious validation and consent checks.

## Test With Curl

Replace placeholders before running:

```powershell
curl.exe -X POST "https://YOUR-WORKER.your-subdomain.workers.dev/leads" `
  -H "Origin: https://ukplanningguide.co.uk" `
  -H "Content-Type: application/json" `
  --data "{\"project_type\":\"Garden room / outbuilding\",\"property_type\":\"Semi-detached house\",\"postcode_or_town\":\"Exampletown EX1\",\"council\":\"Example Council\",\"route_result\":\"Permitted development may be possible\",\"confidence\":\"Medium\",\"name\":\"Example Homeowner\",\"email\":\"example.homeowner@example.com\",\"phone\":\"07123 000000\",\"desired_help\":\"I may want professional planning/design help\",\"consent_contact\":true,\"consent_share\":true,\"source\":\"planning_route_check\",\"form_elapsed_ms\":5000}"
```

Expected success:

```json
{"ok":true,"lead_id":"...","status":"received"}
```

## Test From The Site

1. Deploy the worker.
2. Set `assets/js/lead-config.js` to the worker `/leads` URL.
3. Run the static build.
4. Open `/tools/planning-route-check/`.
5. Complete the route check.
6. Submit the optional help form with both consent boxes ticked.
7. Confirm the thank-you page loads.
8. Check the D1 `planning_leads` table.
9. If notification is configured, check the owner workflow received the clean notification payload.

## Export And Review Leads

The D1 table uses field names compatible with `scripts/export_leads_csv.py` where practical. For local JSON test submissions, keep using:

```powershell
python scripts/export_leads_csv.py
```

For production D1, use Cloudflare's D1 export/query tools, then map the same columns:

- `submitted_at`
- `source`
- `page_url`
- `project_type`
- `property_type`
- `postcode_or_town`
- `council`
- `restrictions_json`
- `timeframe`
- `desired_help`
- `route_result`
- `confidence`
- `name`
- `email`
- `phone`
- `consent_contact`
- `consent_share`
- `user_notes`
- `status`

Owner-side statuses:

- `New`
- `Checked`
- `Needs reply`
- `Match needed`
- `Sent to professional`
- `Unmatched`
- `Rejected/spam`
- `Archived`

## Notification Failure

If `NOTIFY_WEBHOOK_URL` is blank, the worker stores the lead only.

If notification fails but storage succeeds, the user still receives success. Check Worker logs and the D1 table. Do not ask the user to resubmit unless the lead is missing from storage.

## Do Not Build Yet

This package is an intake endpoint, not a marketplace. Do not add a public partner directory, automated lead resale, "guaranteed matching" claims, approved-professional claims, display ads or hidden sharing.
