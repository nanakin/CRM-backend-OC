from crm.controller.manage.employees import EmployeesControllerMixin
from crm.view.cli.commands.subcommands import cli_employee
from tests.integration.cli_signatures.common import matching_signature
from tests.unit.view.cli_subcommands.common import invoke_cli


def test_cli_employee_list_signature():
    """Verify the signature of the 'crm employee list' command."""
    result = invoke_cli(cli_employee, ["list"])
    assert matching_signature(EmployeesControllerMixin.list_employees, result.return_value.params)


def test_cli_employee_detail_signature():
    """
    Verify the signature of the mapped controller function and the return value of the 'crm employee detail' command.
    """
    result = invoke_cli(cli_employee, ["detail", "--username", "random"])
    assert matching_signature(EmployeesControllerMixin.get_employee, result.return_value.params)


def test_cli_employee_add_signature():
    """
    Verify the signature of the mapped controller function and the return value of the 'crm employee add' command.
    """
    result = invoke_cli(cli_employee, ["add", "--fullname", "random", "--username", "random", "--role", "ADMINISTRATOR"])
    assert matching_signature(EmployeesControllerMixin.new_employee, result.return_value.params)


def test_cli_employee_delete_signature():
    """
    Verify the signature of the mapped controller function and the return value of the 'crm employee delete' command.
    """
    result = invoke_cli(cli_employee, ["delete", "--username", "random"])
    assert matching_signature(EmployeesControllerMixin.delete_employee, result.return_value.params)


def test_cli_employee_set_password_signature():
    """
    Verify the signature of the mapped controller function and the return value of the 'crm employee set-password'
    command.
    """
    result = invoke_cli(cli_employee, ["set-password", "--password", "random_password", "--username", "random_username"])
    assert matching_signature(EmployeesControllerMixin.set_password_employee, result.return_value.params)


def test_cli_employee_set_role_signature():
    """
    Verify the signature of the mapped controller function and the return value of the 'crm employee set-role'
    command.
    """
    result = invoke_cli(cli_employee, ["set-role", "--role", "ADMINISTRATOR", "--username", "random_username"])
    assert matching_signature(EmployeesControllerMixin.set_role_employee, result.return_value.params)


def test_cli_employee_update_signature():
    """
    Verify the signature of the mapped controller function and the return value of the 'crm employee update' command.
    """
    result = invoke_cli(cli_employee, ["update", "1", "--fullname", "random"])
    assert matching_signature(EmployeesControllerMixin.update_employee_data, result.return_value.params)
