import click
from view.requests import Request


@click.group(name="authentication")
def cli_authentication():
    """Commands to manage employees"""
    pass


@cli_authentication.command(help="Login")
def login():
    return Request.LOGIN


@cli_authentication.command(help="Logout")
def login():
    return Request.LOGOUT
