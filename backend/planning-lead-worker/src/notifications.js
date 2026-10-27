export function buildOwnerNotification(lead, env = {}) {
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

export async function notifyOwner(lead, env = {}, fetcher = fetch) {
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
