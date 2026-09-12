CREATE TABLE IF NOT EXISTS planning_leads (
  id TEXT PRIMARY KEY,
  submitted_at TEXT NOT NULL,
  received_at TEXT NOT NULL,
  source TEXT,
  page_url TEXT,
  referrer TEXT,
  project_type TEXT,
  property_type TEXT,
  postcode_or_town TEXT,
  council TEXT,
  restrictions_json TEXT,
  timeframe TEXT,
  desired_help TEXT,
  route_result TEXT,
  confidence TEXT,
  user_notes TEXT,
  name TEXT,
  email TEXT,
  phone TEXT,
  consent_contact INTEGER,
  consent_share INTEGER,
  status TEXT DEFAULT 'New',
  ip_hash TEXT,
  user_agent_hash TEXT,
  spam_score INTEGER DEFAULT 0,
  raw_payload_json TEXT,
  updated_at TEXT
);

CREATE INDEX IF NOT EXISTS idx_planning_leads_received_at
  ON planning_leads (received_at);

CREATE INDEX IF NOT EXISTS idx_planning_leads_status
  ON planning_leads (status);

CREATE INDEX IF NOT EXISTS idx_planning_leads_ip_hash_received_at
  ON planning_leads (ip_hash, received_at);
