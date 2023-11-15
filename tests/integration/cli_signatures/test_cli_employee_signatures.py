from src.view.cli.commands.subcommands import cli_employee
from tests.unit.cli_subcommands.common import invoke_cli
from tests.integration.cli_signatures.common import matching_signature
from src.controller.manage.employees import EmployeesControllerMixin


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


# def test_cli_employee_add_signature():
#     """
#     Verify the signature of the mapped controller function and the return value of the 'crm employee add' command.
#     """
#     result = invoke_cli(cli_employee, ["add"])
#     assert matching_signature(EmployeesControllerMixin.new_employee, result.return_value.params)
#
#
# def test_cli_employee_delete_signature():
#     """
#     Verify the signature of the mapped controller function and the return value of the 'crm employee delete' command.
#     """
#     result = invoke_cli(cli_employee, ["delete"])
#     assert matching_signature(EmployeesControllerMixin.delete_employee, result.return_value.params)
#
#
# def test_cli_employee_set_password_signature():
#     """
#     Verify the signature of the mapped controller function and the return value of the 'crm employee set-password'
#     command.
#     """
#     result = invoke_cli(cli_employee, ["set-password"])
#     assert matching_signature(EmployeesControllerMixin.set_password_employee, result.return_value.params)
#
#
# def test_cli_employee_set_role_signature():
#     """
#     Verify the signature of the mapped controller function and the return value of the 'crm employee set-role'
#     command.
#     """
#     result = invoke_cli(cli_employee, ["set-role"])
#     assert matching_signature(EmployeesControllerMixin.set_role_employee, result.return_value.params)
#
#
# def test_cli_employee_update_signature():
#     """
#     Verify the signature of the mapped controller function and the return value of the 'crm employee update' command.
#     """
#     result = invoke_cli(cli_employee, ["update"])
#     assert matching_signature(EmployeesControllerMixin.update_employee_data, result.return_value.params)
