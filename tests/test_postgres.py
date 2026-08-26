import os

import pytest

from taskagentrelay.core.events import TaskEvent
from taskagentrelay.core.postgres import PostgresTaskStore


@pytest.mark.integration
def test_postgres_event_persists_dict_data():
    dsn = os.environ.get("TASKAGENTRELAY_TEST_DATABASE_URL")
    if not dsn:
        pytest.skip("TASKAGENTRELAY_TEST_DATABASE_URL is not set")

    store = PostgresTaskStore(dsn)
    try:
        from taskagentrelay.core.models import Task

        task = Task(id="postgres-event-test", capability="read_file")
        store.save(task)
        store.record_event(
            TaskEvent(
                task_id=task.id,
                event="test.event",
                data={"nested": {"ok": True}, "count": 1},
            )
        )
        with store._conn.cursor() as cur:
            cur.execute(
                "SELECT data_json FROM taskagentrelay_events WHERE task_id=%s AND event=%s",
                (task.id, "test.event"),
            )
            row = cur.fetchone()
        assert row is not None
        assert row[0]["nested"]["ok"] is True
        assert row[0]["count"] == 1
    finally:
        store.close()
