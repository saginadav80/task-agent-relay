import pytest

from taskagentrelay.core.defaults import DefaultTaskSource, DirectAgent, RejectingRunner
from taskagentrelay.core.models import Capability, Implementation, Task
from taskagentrelay.core.orchestrator import Orchestrator
from taskagentrelay.core.registry import Registry


def make_system():
    registry = Registry()
    capability = Capability(
        id="write_file",
        version="1.0.0",
        description="Write text to a file.",
    )
    implementation = Implementation(
        id="write_file/local/v1",
        capability="write_file",
        version="1.0.0",
        runner="rejecting",
        entrypoint="not-yet-implemented",
    )
    registry.register_capability(capability)
    registry.register_implementation(implementation)
    return registry


def test_task_source_normalizes_payload():
    task = DefaultTaskSource().receive({
        "id": "task-1",
        "capability": "write_file",
        "parameters": {"path": "hello.txt", "content": "hello"},
        "source": "test",
    })
    assert task.id == "task-1"
    assert task.capability == "write_file"
    assert task.parameters["path"] == "hello.txt"


def test_orchestrator_resolves_capability_and_implementation():
    registry = make_system()
    task = Task(id="task-2", capability="write_file")
    result = Orchestrator(
        registry=registry,
        agent=DirectAgent(),
        runner=RejectingRunner(),
    ).run(task)
    assert result.state == "failed"
    assert result.error is not None
    assert result.error["code"] == "RUNNER_NOT_IMPLEMENTED"


def test_unknown_capability_fails_cleanly():
    registry = make_system()
    task = Task(id="task-3", capability="missing")
    with pytest.raises(ValueError, match="Capability not available"):
        Orchestrator(
            registry=registry,
            agent=DirectAgent(),
            runner=RejectingRunner(),
        ).run(task)
