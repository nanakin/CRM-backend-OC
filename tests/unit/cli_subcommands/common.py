from click import BaseCommand
from click.testing import CliRunner, Result


def invoke_cli(cli: BaseCommand, *args, **kwargs) -> Result:
    runner = CliRunner()
    return runner.invoke(cli, *args, **kwargs, standalone_mode=False)
