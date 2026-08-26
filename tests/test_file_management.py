from taskagentrelay.capabilities.file_management import delete_file, list_files, read_file, write_file


def test_file_lifecycle(tmp_path):
    created = write_file({"path": "nested/hello.txt", "content": "hello", "mode": "create"}, workspace=tmp_path)
    assert created["path"] == "nested/hello.txt"

    read = read_file({"path": "nested/hello.txt"}, workspace=tmp_path)
    assert read["content"] == "hello"

    listing = list_files({"path": "nested"}, workspace=tmp_path)
    assert listing["files"] == ["nested/hello.txt"]

    deleted = delete_file({"path": "nested/hello.txt"}, workspace=tmp_path)
    assert deleted["deleted"] is True


def test_write_create_rejects_existing_file(tmp_path):
    write_file({"path": "hello.txt", "content": "one", "mode": "create"}, workspace=tmp_path)
    try:
        write_file({"path": "hello.txt", "content": "two", "mode": "create"}, workspace=tmp_path)
    except ValueError as exc:
        assert "already exists" in str(exc)
    else:
        raise AssertionError("expected create mode to reject an existing file")


def test_workspace_escape_is_rejected(tmp_path):
    try:
        read_file({"path": "../secret.txt"}, workspace=tmp_path)
    except ValueError as exc:
        assert "escapes" in str(exc)
    else:
        raise AssertionError("expected path traversal to be rejected")
