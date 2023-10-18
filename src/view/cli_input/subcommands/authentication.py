import click
from view.requests import Request


@click.group(name="auth")
def cli_authentication():
    """Commands to manage employees"""
    pass


@cli_authentication.command(help="Login")
def login():
    username = click.prompt("Nom d'utilisateur ")
    password = click.prompt("Mot de passe ", hide_input=True)
    return Request.LOGIN, username, password


@cli_authentication.command(help="Logout")
def logout():
    return Request.LOGOUT
