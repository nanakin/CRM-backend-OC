"""
Test the 'crm employee' subcommands.

Usage: crm employee [OPTIONS] COMMAND [ARGS]...

  Commands to manage employees.

Options:
  --help  Show this message and exit.

Commands:
  add           Add a new employee
  delete        Delete an employee
  detail        Show employee details
  list          List existing employees
  set-password  Set a new password
  set-role      Set a new role
  update        Update employee data
"""

import pytest
from common import invoke_cli

from crm.view.cli.commands.subcommands import cli_employee
from crm.view.requests import Request


def test_cli_employee_explicit_help():
    """Test the 'crm employee --help' command."""
    result = invoke_cli(cli_employee, ["--help"])
    assert "Usage:" in result.output


@pytest.mark.parametrize("subcommand", [("add", "list", "detail", "set-role", "set-password", "update", "delete")])
def test_cli_employee_subcommands(subcommand):
    """Test existence of crm employee subcommands."""

    result = invoke_cli(cli_employee, [subcommand, "--help"])
    assert result.exit_code == 0
    assert "Usage:" in result.output


class TestCliEmployeeList:
    """Test the 'crm employee list' command."""

    def test_cli_employee_list_request(self):
        """Verify that this subcommand is valid and returning the expected request."""
        result = invoke_cli(cli_employee, ["list"])
        full_request = result.return_value
        assert result.exit_code == 0
        assert full_request.request.value == Request.LIST_EMPLOYEES.value

    @pytest.mark.parametrize("role", ["ADMINISTRATOR", "SUPPORT", "COMMERCIAL"])
    def test_cli_employee_list_filter_valid_option(self, role):
        """Test the --role-filter option of 'crm employee list' command."""
        result = invoke_cli(cli_employee, ["list", "--role-filter", role])
        full_request = result.return_value
        assert result.exit_code == 0
        assert full_request.params["role_filter"] == role


class TestCliEmployeeDetail:
    """Test the 'crm employee detail' command."""

    def test_cli_employee_detail_request(self):
        """Verify that this subcommand is valid and returning the expected request."""
        result = invoke_cli(cli_employee, ["detail"], input="random")
        full_request = result.return_value
        assert result.exit_code == 0
        assert full_request.request.value == Request.DETAIL_EMPLOYEE.value
        assert full_request.params["username"] == "random"

    def test_cli_employee_detail_username_random_value(self):
        """Test the --username option of 'crm employee detail' command."""
        result = invoke_cli(cli_employee, ["detail", "--username", "random"])
        full_request = result.return_value
        assert result.exit_code == 0
        assert full_request.params["username"] == "random"


class TestCliEmployeeAdd:
    """Test the 'crm employee add' command."""

    def test_cli_employee_add_request(self):
        """Verify that this subcommand is valid and returning the expected values."""
        result = invoke_cli(cli_employee, ["add"], input="random full name\nrandom_username")
        full_request = result.return_value
        assert result.exit_code == 0
        assert full_request.request.value == Request.NEW_EMPLOYEE.value
        assert full_request.params["username"] == "random_username"
        assert full_request.params["fullname"] == "random full name"

    def test_cli_employee_add_with_options(self):
        """Test options of 'crm employee add' command."""
        result = invoke_cli(cli_employee, ["add", "--username", "random_username", "--fullname", "random full name"])
        full_request = result.return_value
        assert result.exit_code == 0
        assert full_request.params["username"] == "random_username"
        assert full_request.params["fullname"] == "random full name"


class TestCliEmployeeSetRole:
    """Test the 'crm employee set-role' command."""

    def test_cli_employee_set_role_request(self):
        """Verify that this subcommand is valid and returning the expected request."""
        result = invoke_cli(cli_employee, ["set-role"], input="random_username\nADMINISTRATOR")
        full_request = result.return_value
        assert result.exit_code == 0
        assert full_request.request.value == Request.SET_EMPLOYEE_ROLE.value
        assert full_request.params["username"] == "random_username"
        assert full_request.params["role_name"] == "ADMINISTRATOR"

    def test_cli_employee_set_role_with_options(self):
        """Test the --username option of 'crm employee set-role' command."""
        result = invoke_cli(cli_employee, ["add", "--username", "random_username", "--fullname", "random full name"])
        full_request = result.return_value
        assert result.exit_code == 0
        assert full_request.params["username"] == "random_username"
        assert full_request.params["fullname"] == "random full name"


class TestCliEmployeeSetPassword:
    """Test the 'crm employee set-password' command."""

    def test_cli_employee_set_password_request(self):
        """Verify that this subcommand is valid and returning the expected request."""
        result = invoke_cli(cli_employee, ["set-password"], input="random_username\nrandom_password\nrandom_password")
        full_request = result.return_value
        assert result.exit_code == 0
        assert full_request.request.value == Request.SET_EMPLOYEE_PASSWORD.value
        assert full_request.params["username"] == "random_username"
        assert full_request.params["password"] == "random_password"

    def test_cli_employee_set_password_with_options(self):
        """Test the options of 'crm employee set-password' command."""
        result = invoke_cli(
            cli_employee, ["set-password", "--username", "random_username", "--password", "random_password"]
        )
        full_request = result.return_value
        assert result.exit_code == 0
        assert full_request.params["username"] == "random_username"
        assert full_request.params["password"] == "random_password"


class TestCliEmployeeUpdate:
    """Test the 'crm employee update' command."""

    def test_cli_employee_update_nothing(self):
        """Verify that this subcommand is failing without field to update."""
        result = invoke_cli(cli_employee, ["update", "1"])
        assert result.exit_code == 1

    @pytest.mark.parametrize(
        "field_name, param_name, value, expected_value",
        [
            ("--fullname", "fullname", "random full name", "random full name"),
            ("--username", "username", "random_username", "random_username"),
        ],
    )
    def test_cli_employee_update_field(self, field_name, param_name, value, expected_value):
        """Verify that this subcommand is valid and returning the expected request."""
        result = invoke_cli(cli_employee, ["update", "1", field_name], input=value)
        full_request = result.return_value
        assert result.exit_code == 0
        assert full_request.request.value == Request.UPDATE_EMPLOYEE.value
        assert full_request.params[param_name] == expected_value
