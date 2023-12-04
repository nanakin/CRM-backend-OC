from crm.view.cli.terminal.input import ask_credentials
from unittest import mock
from crm.view.cli.terminal.display import console


def test_ask_credentials():
    """Test the 'ask_credentials' function."""
    with console.capture() as capture:
        with mock.patch("crm.view.cli.terminal.input.Prompt.ask", side_effect=["username", "password"]):
            assert ask_credentials() == ("username", "password")
    assert "requires user authentication" in capture.get()
