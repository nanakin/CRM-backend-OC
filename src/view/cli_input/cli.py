import click
from .employees import cli_employee
from .customers import cli_customer
import sys


@click.group()
def cli():
    pass


def cli_main():
    cli.add_command(cli_employee)
    cli.add_command(cli_customer)
    try:
        return cli(standalone_mode=False)
    except click.ClickException as exc:
        exc.show()
        sys.exit(click.ClickException.exit_code)
