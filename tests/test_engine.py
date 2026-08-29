from taskagentrelay.core.approval import ApprovalPolicy
from taskagentrelay.core.bootstrap import build_registry
from taskagentrelay.core.defaults import DirectAgent
from taskagentrelay.core.engine import TaskEngine
from taskagentrelay.core.events import EventRecorder
from taskagentrelay.core.models import Task
from taskagentrelay.core.storage import InMemoryTaskStore
from taskagentrelay.runners.local import LocalRunner


def test_write_file_requires_approval(tmp_path):
    task = Task(id="approval-1", capability="write_file", parameters={"path": "a.txt", "content": "x"})
    store = InMemoryTaskStore()
    result = TaskEngine(
        registry=build_registry(),
        agent=DirectAgent(),
        runner=LocalRunner(tmp_path),
        store=store,
        approval=ApprovalPolicy(auto_approve=False),
        events=EventRecorder(),
    ).execute(task)
    assert result.state == "awaiting_approval"
    assert not (tmp_path / "a.txt").exists()


def test_write_file_executes_after_approval(tmp_path):
    task = Task(id="write-1", capability="write_file", parameters={"path": "a.txt", "content": "hello"})
    store = InMemoryTaskStore()
    result = TaskEngine(
        registry=build_registry(),
        agent=DirectAgent(),
        runner=LocalRunner(tmp_path),
        store=store,
        approval=ApprovalPolicy(auto_approve=True),
        events=EventRecorder(),
    ).execute(task)
    assert result.state == "completed"
    assert (tmp_path / "a.txt").read_text() == "hello"
    saved = store.get("write-1")
    assert saved is not None
    assert saved.state == "completed"
