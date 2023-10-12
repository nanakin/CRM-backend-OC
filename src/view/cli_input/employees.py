import click
from view.requests import Request

@click.group(name="employee")
def cli_employee():
    """Commands to manage employees"""
    pass


@cli_employee.command(help="Add a new employee")
def add():
    pass


@cli_employee.command(help="Edit an employee")
def edit():
    click.echo("edit")


@cli_employee.command(help="List existing employees")
def list():
    click.echo("employee list")
    return Request.LIST_EMPLOYEES

