CREATE TABLE IF NOT EXISTS taskagentrelay_tasks (
    task_id TEXT PRIMARY KEY,
    capability TEXT NOT NULL,
    source TEXT,
    state TEXT NOT NULL,
    parameters_json JSONB NOT NULL DEFAULT '{}'::jsonb,
    result_json JSONB,
    error_json JSONB,
    artifacts_json JSONB NOT NULL DEFAULT '[]'::jsonb,
    metadata_json JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ NOT NULL,
    updated_at TIMESTAMPTZ NOT NULL
);

CREATE TABLE IF NOT EXISTS taskagentrelay_events (
    id BIGSERIAL PRIMARY KEY,
    task_id TEXT NOT NULL REFERENCES taskagentrelay_tasks(task_id) ON DELETE CASCADE,
    event TEXT NOT NULL,
    timestamp TIMESTAMPTZ NOT NULL,
    data_json JSONB NOT NULL DEFAULT '{}'::jsonb
);

CREATE INDEX IF NOT EXISTS idx_taskagentrelay_events_task_id
    ON taskagentrelay_events(task_id);

CREATE INDEX IF NOT EXISTS idx_taskagentrelay_tasks_state
    ON taskagentrelay_tasks(state);
