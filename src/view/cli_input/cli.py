import click
from .employees import cli_employee


@click.group()
def cli():
    pass


def cli_main():
    cli.add_command(cli_employee)
    return cli(standalone_mode=False)
