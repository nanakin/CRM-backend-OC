import click

from view.requests import Request


@click.group(name="auth")
def cli_authentication():
    """Commands to manage employees"""
    pass


@cli_authentication.command(help="Login")
@click.option("--username", prompt=True, prompt_required=True, type=str, help="Specify the employee")
@click.option("--password", prompt=True, hide_input=True)
def login(username, password):
    return Request.LOGIN, username, password


@cli_authentication.command(help="Logout")
def logout():
    return Request.LOGOUT
