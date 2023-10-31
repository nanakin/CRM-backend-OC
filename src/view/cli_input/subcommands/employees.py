import click

from view.requests import Request


@click.group(name="employee")
def cli_employee():
    """Commands to manage employees"""
    pass


@cli_employee.command(help="Add a new employee")
@click.option("--fullname", prompt=True, prompt_required=True, type=str, help="Define the employee full name")
@click.option("--username", prompt=True, prompt_required=True, type=str, help="Define the employee username")
def add(username, fullname):
    return Request.NEW_EMPLOYEE, username, fullname


@cli_employee.command(help="Delete an employee")
@click.option("--username", prompt=True, prompt_required=True, type=str, help="Specify the employee")
def delete(username):
    return Request.DELETE_EMPLOYEE, username


@cli_employee.command(help="Set a new password")
@click.option("--username", prompt=True, prompt_required=True, type=str, help="Specify the employee")
@click.option("--password", prompt=True, hide_input=True, confirmation_prompt=True)
def set_password(username, password):
    return Request.SET_EMPLOYEE_PASSWORD, username, password


@click.option("--username", prompt=True, prompt_required=True, type=str, help="Specify the employee")
@click.option(
    "--role", prompt=True, prompt_required=True, default="NONE", type=str, help="Specify the role"
)  # use choice ?
@cli_employee.command(help="Set a new role")
def set_role(username, role):
    return Request.SET_EMPLOYEE_ROLE, username, role


@cli_employee.command(help="Update employee data")
@click.argument("id", type=int)
@click.option(
    "--fullname", default=None, prompt=False, prompt_required=False, type=str, help="Define the new full name"
)
@click.option("--username", default=None, prompt=False, prompt_required=True, type=str, help="Define the new username")
def update(id, username, fullname):
    return Request.UPDATE_EMPLOYEE, id, username, fullname


@click.option("--username", prompt=True, prompt_required=True, type=str, help="Specify the employee")
@cli_employee.command(help="Show employee detail")
def detail(username):
    return Request.DETAIL_EMPLOYEE, username


@click.option(
    "--role-filter", type=click.Choice(["SUPPORT", "ADMINISTRATOR", "COMMERCIAL"], case_sensitive=False), default=None
)
@cli_employee.command(help="List existing employees")
def list(role_filter):
    return Request.LIST_EMPLOYEES, role_filter
