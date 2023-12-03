import click

from crm.view.requests import FullRequest, Request


@click.group(name="employee")
def cli_employee():
    """Commands to manage employees."""


@cli_employee.command(help="Add a new employee")
@click.option("--fullname", prompt=True, prompt_required=True, type=str, help="Define the employee full name")
@click.option("--username", prompt=True, prompt_required=True, type=str, help="Define the employee username")
@click.option(
    "--role",
    "role_name",
    prompt=True,
    prompt_required=True,
    type=click.Choice(["SUPPORT", "ADMINISTRATOR", "COMMERCIAL", "NONE"], case_sensitive=False),
    default="NONE",
    help="Specify the role",
)
def add(**kwargs) -> FullRequest:
    """Command to add a new employee."""
    return FullRequest(Request.NEW_EMPLOYEE, **kwargs)


@cli_employee.command(help="Delete an employee")
@click.option("--username", prompt=True, prompt_required=True, type=str, help="Specify the employee")
def delete(**kwargs) -> FullRequest:
    """Command to delete an employee."""
    return FullRequest(Request.DELETE_EMPLOYEE, **kwargs)


@cli_employee.command(help="Set a new password")
@click.option("--username", prompt=True, prompt_required=True, type=str, help="Specify the employee")
@click.option("--password", prompt=True, hide_input=True, confirmation_prompt=True)
def set_password(**kwargs) -> FullRequest:
    """Command to set a new password."""
    return FullRequest(Request.SET_EMPLOYEE_PASSWORD, **kwargs)


@cli_employee.command(help="Set a new role")
@click.option("--username", prompt=True, prompt_required=True, type=str, help="Specify the employee")
@click.option(
    "--role",
    "role_name",
    prompt=True,
    prompt_required=True,
    type=click.Choice(["SUPPORT", "ADMINISTRATOR", "COMMERCIAL", "NONE"], case_sensitive=False),
    default="NONE",
    help="Specify the role",
)
def set_role(**kwargs) -> FullRequest:
    """Command to set a new role."""
    return FullRequest(Request.SET_EMPLOYEE_ROLE, **kwargs)


@cli_employee.command(help="Update employee data")
@click.argument("employee-id", type=int)
@click.option(
    "--fullname", default=None, prompt=True, prompt_required=False, type=str, help="Define the new full name"
)
@click.option("--username", default=None, prompt=True, prompt_required=False, type=str, help="Define the new username")
def update(**kwargs) -> FullRequest:
    """Command to update an employee data (fullname and username fields)."""
    if kwargs["fullname"] is None and kwargs["username"] is None:
        raise click.BadParameter("You must specify at least one field to update.")
    return FullRequest(Request.UPDATE_EMPLOYEE, **kwargs)


@cli_employee.command(help="Show employee details")
@click.option("--username", prompt=True, prompt_required=True, type=str, help="Specify the employee")
def detail(**kwargs) -> FullRequest:
    """Command to show employee details."""
    return FullRequest(Request.DETAIL_EMPLOYEE, **kwargs)


@cli_employee.command(help="List existing employees", name="list")
@click.option(
    "--role-filter", type=click.Choice(["SUPPORT", "ADMINISTRATOR", "COMMERCIAL"], case_sensitive=False), default=None
)
def listing(**kwargs) -> FullRequest:
    """Command to list existing employees."""
    return FullRequest(Request.LIST_EMPLOYEES, **kwargs)
