import click

from view.requests import FullRequest, Request


@click.group(name="auth")
def cli_authentication():
    """Commands to manage authentication."""


@cli_authentication.command(help="Login")
@click.option("--username", prompt=True, prompt_required=True, type=str, help="Specify the employee username")
@click.option("--password", prompt=True, hide_input=True)
def login(**kwargs) -> FullRequest:
    """Command to log in to the application."""
    return FullRequest(Request.LOGIN, **kwargs)


@cli_authentication.command(help="Logout")
def logout() -> FullRequest:
    """Command to log out from the application."""
    return FullRequest(Request.LOGOUT)
