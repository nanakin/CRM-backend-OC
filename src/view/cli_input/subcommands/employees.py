import click

from view.requests import Request


@click.group(name="employee")
def cli_employee():
    """Commands to manage employees"""
    pass


@cli_employee.command(help="Add a new employee")
def add():
    pass


@cli_employee.command(help="Set a new password")
def setpassword():
    password = click.prompt("New password", hide_input=True, confirmation_prompt=True)
    return Request.SET_EMPLOYEE_PASSWORD, password


@cli_employee.command(help="Update employee data")
@click.argument("id", type=int)
@click.option("--fullname", required=False, type=str, help="Update the employee full name")
@click.option("--username", required=False, type=str, help="Update the employee username")
def update(id, fullname, username):
    return Request.EDIT_EMPLOYEE, (id, fullname, username)


@cli_employee.command(help="List existing employees")
def list():
    return Request.LIST_EMPLOYEES
