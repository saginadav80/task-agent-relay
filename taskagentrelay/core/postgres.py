from __future__ import annotations

import json
from typing import Any

from .events import TaskEvent
from .models import Task
from .storage import TaskStore


class PostgresTaskStore(TaskStore):
    """PostgreSQL persistence boundary used when psycopg is installed."""

    def __init__(self, dsn: str) -> None:
        try:
            import psycopg
        except ImportError as exc:  # pragma: no cover - dependency is optional
            raise RuntimeError("Postgres support requires: pip install taskagentrelay[postgres]") from exc
        self._psycopg = psycopg
        self._conn = psycopg.connect(dsn)
        self._conn.autocommit = True

    def save(self, task: Task) -> None:
        with self._conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO taskagentrelay_tasks
                    (task_id, capability, source, state, parameters_json, result_json, error_json, artifacts_json, metadata_json, created_at, updated_at)
                VALUES (%s, %s, %s, %s, %s::jsonb, %s::jsonb, %s::jsonb, %s::jsonb, %s::jsonb, %s, %s)
                ON CONFLICT (task_id) DO UPDATE SET
                    state = EXCLUDED.state,
                    result_json = EXCLUDED.result_json,
                    error_json = EXCLUDED.error_json,
                    artifacts_json = EXCLUDED.artifacts_json,
                    metadata_json = EXCLUDED.metadata_json,
                    updated_at = EXCLUDED.updated_at
                """,
                (
                    task.id, task.capability, task.source, task.state,
                    json.dumps(task.parameters), json.dumps(task.result), json.dumps(task.error),
                    json.dumps(task.artifacts), json.dumps(task.metadata), task.created_at, task.updated_at,
                ),
            )

    def get(self, task_id: str) -> Task | None:
        with self._conn.cursor() as cur:
            cur.execute(
                "SELECT task_id, capability, source, state, parameters_json, result_json, error_json, artifacts_json, metadata_json, created_at, updated_at FROM taskagentrelay_tasks WHERE task_id=%s",
                (task_id,),
            )
            row = cur.fetchone()
        if not row:
            return None
        return Task.from_mapping({
            "id": row[0], "capability": row[1], "source": row[2], "state": row[3],
            "parameters": row[4], "result": row[5], "error": row[6], "artifacts": row[7],
            "metadata": row[8], "created_at": str(row[9]), "updated_at": str(row[10]),
        })

    def record_event(self, event: TaskEvent) -> None:
        with self._conn.cursor() as cur:
            cur.execute(
                "INSERT INTO taskagentrelay_events(task_id, event, timestamp, data_json) VALUES (%s, %s, %s, %s::jsonb)",
                (event.task_id, event.event, event.timestamp, json.dumps(event.data)),
            )

    def close(self) -> None:
        self._conn.close()
