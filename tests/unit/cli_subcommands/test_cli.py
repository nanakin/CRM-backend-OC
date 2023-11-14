from common import invoke_cli
from src.view.cli.commands.cli import cli
from click.exceptions import UsageError


def test_cli_help():
    """Test the crm command (without subcommand)."""
    result = invoke_cli(cli, [])
    assert "Usage:" in result.output

    result = invoke_cli(cli, ["--help"])
    assert "Usage:" in result.output


def test_cli_subcommands():
    """Test existence of crm subcommands (without option)."""
    subcommands = ["employee", "event", "customer", "contract", "auth"]

    for subcommand in subcommands:
        result = invoke_cli(cli, [subcommand])
        assert result.exit_code == 0

    result = invoke_cli(cli, ["random-command"])
    assert isinstance(result.exception, UsageError)
