PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS schema_migrations (
  version INTEGER PRIMARY KEY,
  name TEXT NOT NULL,
  applied_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

INSERT OR IGNORE INTO schema_migrations (version, name)
VALUES (1, 'artist_os_library_initial');

CREATE TABLE IF NOT EXISTS projects (
  project_id TEXT PRIMARY KEY,
  title TEXT NOT NULL,
  status TEXT NOT NULL,
  current_stage TEXT NOT NULL,
  summary TEXT,
  project_dir TEXT NOT NULL,
  manifest_path TEXT NOT NULL,
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_projects_status
ON projects(status);

CREATE INDEX IF NOT EXISTS idx_projects_updated_at
ON projects(updated_at);

CREATE TABLE IF NOT EXISTS project_paths (
  project_id TEXT NOT NULL,
  path_key TEXT NOT NULL,
  path_value TEXT NOT NULL,
  PRIMARY KEY (project_id, path_key),
  FOREIGN KEY (project_id) REFERENCES projects(project_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS project_decisions (
  project_id TEXT PRIMARY KEY,
  interpretation_status TEXT NOT NULL,
  symbology_status TEXT NOT NULL,
  style_status TEXT NOT NULL,
  detail_status TEXT NOT NULL,
  selected_symbology TEXT,
  presentation_mode TEXT,
  selected_style TEXT,
  selected_detail_mode TEXT,
  FOREIGN KEY (project_id) REFERENCES projects(project_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS records (
  project_id TEXT NOT NULL,
  record_type TEXT NOT NULL,
  path TEXT NOT NULL,
  status TEXT,
  updated_at TEXT,
  PRIMARY KEY (project_id, record_type, path),
  FOREIGN KEY (project_id) REFERENCES projects(project_id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_records_type
ON records(record_type);

CREATE TABLE IF NOT EXISTS assets (
  asset_id TEXT PRIMARY KEY,
  project_id TEXT NOT NULL,
  asset_type TEXT NOT NULL,
  stage TEXT NOT NULL,
  path TEXT NOT NULL,
  metadata_path TEXT NOT NULL,
  status TEXT NOT NULL,
  created_at TEXT,
  critique_status TEXT,
  origin TEXT,
  provider TEXT,
  model TEXT,
  source_record_id TEXT,
  brief_id TEXT,
  prompt_plan_id TEXT,
  visual_board_type TEXT,
  prompt_variant_id TEXT,
  FOREIGN KEY (project_id) REFERENCES projects(project_id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_assets_project
ON assets(project_id);

CREATE INDEX IF NOT EXISTS idx_assets_type
ON assets(asset_type);

CREATE INDEX IF NOT EXISTS idx_assets_stage
ON assets(stage);

CREATE TABLE IF NOT EXISTS events (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  event_id TEXT,
  project_id TEXT NOT NULL,
  occurred_at TEXT,
  stage TEXT,
  event_type TEXT,
  summary TEXT,
  payload_json TEXT NOT NULL,
  FOREIGN KEY (project_id) REFERENCES projects(project_id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_events_project
ON events(project_id);

CREATE INDEX IF NOT EXISTS idx_events_occurred_at
ON events(occurred_at);
