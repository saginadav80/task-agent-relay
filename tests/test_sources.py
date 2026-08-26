from taskagentrelay.sources.github import GitHubSource
from taskagentrelay.sources.webhook import WebhookSource


def test_webhook_source_normalizes_task():
    task = WebhookSource().receive({
        "id": "hook-1",
        "capability": "read_file",
        "parameters": {"path": "hello.txt"},
    })
    assert task.id == "hook-1"
    assert task.source == "webhook"


def test_github_source_maps_issue_metadata():
    task = GitHubSource().receive({
        "id": 42,
        "number": 7,
        "title": "Read a file",
        "body": "Read hello.txt",
        "html_url": "https://github.com/example/repo/issues/7",
        "capability": "read_file",
        "parameters": {"path": "hello.txt"},
        "labels": [{"name": "task"}],
        "repository": "example/repo",
    })
    assert task.id == "github:42"
    assert task.source == "github"
    assert task.metadata["repository"] == "example/repo"
    assert task.parameters["path"] == "hello.txt"
