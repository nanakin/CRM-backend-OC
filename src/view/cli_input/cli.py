import sys

import click

from .subcommands import cli_authentication, cli_customer, cli_employee, cli_contract


@click.group()
def cli():
    pass


def cli_main():
    cli.add_command(cli_employee)
    cli.add_command(cli_customer)
    cli.add_command(cli_authentication)
    cli.add_command(cli_contract)
    try:
        returned = cli(standalone_mode=False)
        if type(returned) is tuple:
            request, *param = returned
        else:
            request, param = returned, ()
        return request, param
    except click.ClickException as exc:
        exc.show()
        sys.exit(click.ClickException.exit_code)
