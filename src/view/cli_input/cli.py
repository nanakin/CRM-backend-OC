import click
from .employees import cli_employee
import sys


@click.group()
def cli():
    pass


def cli_main():
    cli.add_command(cli_employee)
    try:
        return cli(standalone_mode=False)
    except click.ClickException as exc:
        exc.show()
        sys.exit(click.ClickException.exit_code)
