-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Jobs table: top-level session / run
CREATE TABLE IF NOT EXISTS jobs (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  created_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
  status TEXT DEFAULT 'pending', -- pending|parsing|filtering|dd_running|completed|failed|removed
  filters JSONB,                 -- {sector, stage, geography, ticket_min, ticket_max, context_text}
  user_token TEXT,               -- anonymous shareable token/UUID
  progress JSONB,                -- {step: "...", percent: N, status_message: "..."}
  error_log TEXT
);

-- Files table: uploaded sources
CREATE TABLE IF NOT EXISTS files (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  job_id UUID REFERENCES jobs(id) ON DELETE CASCADE,
  file_type TEXT,                -- pdf|sheet|url
  original_name TEXT,
  storage_path TEXT,             -- Supabase storage path
  parsed JSONB,                  -- parsed content / summary (filled after parsing)
  created_at TIMESTAMP WITH TIME ZONE DEFAULT now()
);

-- Startups table: extracted rows / candidates
CREATE TABLE IF NOT EXISTS startups (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  job_id UUID REFERENCES jobs(id) ON DELETE CASCADE,
  source_file_id UUID REFERENCES files(id),
  name TEXT,
  sector TEXT,
  stage TEXT,
  geography TEXT,
  ticket_size_min NUMERIC,
  ticket_size_max NUMERIC,
  summary TEXT,
  metadata JSONB,                -- team, traction, links, raw claims
  relevance_score FLOAT,         -- from filter agent 0-1
  created_at TIMESTAMP WITH TIME ZONE DEFAULT now()
);

-- Due diligence table: per startup
CREATE TABLE IF NOT EXISTS due_diligence (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  startup_id UUID REFERENCES startups(id) ON DELETE CASCADE,
  tech_validation JSONB,         -- DeepSeek outputs: claim -> verdict + evidence links
  market_analysis JSONB,         -- Gemini outputs: TAM, competitors, growth assumptions
  competitor_map JSONB,
  financial_check JSONB,         -- parsed financial KPIs, anomalies
  risk_heatmap JSONB,            -- {"tech":"green","market":"yellow","finance":"red","compliance":"green"}
  success_rate FLOAT,            -- 0..100
  competition_difficulty FLOAT,  -- 0..100
  revenue_projection JSONB,      -- {"year1":..,"year2":..,"year3":..}
  profit_margin FLOAT,           -- predicted %
  key_points JSONB,              -- array of bullet insights
  overall_summary TEXT,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT now()
);

-- Results table: final aggregated results per job
CREATE TABLE IF NOT EXISTS results (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  job_id UUID REFERENCES jobs(id) ON DELETE CASCADE,
  top_startups JSONB,            -- [{"startup_id":..., "rank":1, "fit_reason":"..."}]
  one_pager_path TEXT,           -- Supabase storage path for compiled PDF
  created_at TIMESTAMP WITH TIME ZONE DEFAULT now()
);

-- Create indexes for better query performance
CREATE INDEX IF NOT EXISTS idx_jobs_status ON jobs(status);
CREATE INDEX IF NOT EXISTS idx_jobs_created_at ON jobs(created_at);
CREATE INDEX IF NOT EXISTS idx_files_job_id ON files(job_id);
CREATE INDEX IF NOT EXISTS idx_startups_job_id ON startups(job_id);
CREATE INDEX IF NOT EXISTS idx_startups_relevance_score ON startups(relevance_score);
CREATE INDEX IF NOT EXISTS idx_due_diligence_startup_id ON due_diligence(startup_id);
CREATE INDEX IF NOT EXISTS idx_results_job_id ON results(job_id);
