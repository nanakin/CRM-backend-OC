"""The main file of the command line interface module."""

import sys

import click

from crm.view.requests import FullRequest

from .subcommands import cli_authentication, cli_contract, cli_customer, cli_employee, cli_event


@click.group()
def cli() -> int | FullRequest:
    """CRM application allows employees, customers, contracts and events management."""


cli.add_command(cli_employee)
cli.add_command(cli_customer)
cli.add_command(cli_authentication)
cli.add_command(cli_contract)
cli.add_command(cli_event)


def cli_main() -> FullRequest | None:
    """Deal with CLI.

    Returns understandable requests to the controller."""

    try:
        # deal with command line using click module
        returned = cli(standalone_mode=False)
        if returned == 0:  # user asked help
            return None
        else:
            return returned
    except click.ClickException as exc:
        exc.show()  # print click error explanation
        sys.exit(click.ClickException.exit_code)
    except click.exceptions.Abort:  # quit at ctrl-c command
        sys.exit()
