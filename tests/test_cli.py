from taskagentrelay.cli import main


def test_doctor(capsys):
    assert main(["doctor"]) == 0
    output = capsys.readouterr().out
    assert "TaskAgentRelay Doctor" in output
    assert "Capabilities: 4" in output


def test_capabilities(capsys):
    assert main(["capabilities"]) == 0
    output = capsys.readouterr().out
    assert "write_file" in output
    assert "delete_file" in output
