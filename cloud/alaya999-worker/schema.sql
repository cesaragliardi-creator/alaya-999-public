-- ALAYA-999 cloud service: public verification metadata and *private* AI drafts only.
-- No user messages or private Drive / GitHub memory must be stored here.
CREATE TABLE IF NOT EXISTS heartbeats (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  checked_at TEXT NOT NULL,
  state TEXT NOT NULL CHECK (state IN ('ok','error')),
  source_url TEXT NOT NULL,
  sha256 TEXT,
  source_version TEXT,
  detail TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS ix_heartbeats_recent ON heartbeats (id DESC);

CREATE TABLE IF NOT EXISTS proposed_experiments (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  created_at TEXT NOT NULL,
  model TEXT NOT NULL,
  anchor_sha256 TEXT NOT NULL,
  proposal TEXT NOT NULL,
  review_status TEXT NOT NULL CHECK (review_status IN ('unreviewed','reviewed','rejected'))
);
CREATE INDEX IF NOT EXISTS ix_proposals_recent ON proposed_experiments (id DESC);
