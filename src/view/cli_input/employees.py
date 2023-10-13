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
@click.argument('identifier', type=int)
def edit(identifier):
    click.echo(f"employee edit {identifier}")
    return Request.EDIT_EMPLOYEE, identifier


@cli_employee.command(help="List existing employees")
def list():
    click.echo("employee list")
    return Request.LIST_EMPLOYEES

