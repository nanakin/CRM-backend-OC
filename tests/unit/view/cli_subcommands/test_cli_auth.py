"""
Usage: crm auth [OPTIONS] COMMAND [ARGS]...

  Commands to manage authentication.

Options:
  --help  Show this message and exit.

Commands:
  login   Login
  logout  Logout
"""
import pytest
from common import invoke_cli

from crm.view.cli.commands.subcommands import cli_authentication as cli_auth
from crm.view.requests import Request


def test_cli_auth_explicit_help():
    """Test the 'crm event --help' command."""
    result = invoke_cli(cli_auth, ["--help"])
    assert "Usage:" in result.output


@pytest.mark.parametrize("subcommand", [("login", "logout")])
def test_cli_auth_subcommands(subcommand):
    """Test existence of crm event subcommands."""

    result = invoke_cli(cli_auth, [subcommand, "--help"])
    assert result.exit_code == 0
    assert "Usage:" in result.output


class TestCliAuthLogin:
    """Test the 'crm auth login' command."""

    def test_cli_auth_login_request(self):
        """Verify that this subcommand is valid and returning the expected request."""
        result = invoke_cli(cli_auth, ["login"], input="random_username\nrandompassword")
        full_request = result.return_value
        assert result.exit_code == 0
        assert full_request.request.value == Request.LOGIN.value
        assert full_request.params["username"] == "random_username"
        assert full_request.params["password"] == "randompassword"

    def test_cli_auth_login_options(self):
        """Test the options of the subcommand."""
        result = invoke_cli(cli_auth, ["login", "--username", "random_username", "--password", "randompassword"])
        full_request = result.return_value
        assert result.exit_code == 0
        assert full_request.params["username"] == "random_username"
        assert full_request.params["password"] == "randompassword"


class TestCliAuthLogout:
    """Test the 'crm auth logout' command."""

    def test_cli_auth_logout_request(self):
        """Verify that this subcommand is valid and returning the expected request."""
        result = invoke_cli(cli_auth, ["logout"])
        full_request = result.return_value
        assert result.exit_code == 0
        assert full_request.request.value == Request.LOGOUT.value
