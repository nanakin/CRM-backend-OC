import pytest
from common import invoke_cli

from crm.view.cli.commands.cli import cli


def test_cli_help():
    """Test the crm command (without subcommand)."""
    result = invoke_cli(cli, [])
    assert "Usage:" in result.output

    result = invoke_cli(cli, ["--help"])
    assert "Usage:" in result.output


@pytest.mark.parametrize("subcommand", ["employee", "event", "customer", "contract", "auth"])
def test_cli_subcommands(subcommand):
    """Test existence of crm subcommands (without option)."""

    result = invoke_cli(cli, [subcommand])
    assert result.exit_code == 0
