from click import BaseCommand
from click.testing import CliRunner, Result


def invoke_cli(cli: BaseCommand, *args, **kwargs) -> Result:
    """Invoke a click command (in standalone mode) with the given arguments and return the result."""
    runner = CliRunner()
    return runner.invoke(cli, *args, **kwargs, standalone_mode=False)
