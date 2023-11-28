"""Test the 'crm employee' subcommands."""
from click import BadOptionUsage, BadParameter
from common import invoke_cli

from crm.view.cli.commands.subcommands import cli_employee
from crm.view.requests import Request


def test_cli_employees_explicit_help():
    """Test the 'crm employee --help' command."""
    result = invoke_cli(cli_employee, ["--help"])
    assert "Usage:" in result.output


def test_cli_employees_help():
    """Test the 'crm employee' command (without subcommand)."""
    result = invoke_cli(cli_employee, [])
    assert "Usage:" in result.output


class TestCliEmployeesList:
    """Test the 'crm employee list' command."""

    def test_cli_employees_list_help(self):
        """Test the help of 'crm employee list' command."""
        result_help = invoke_cli(cli_employee, ["list", "--help"])
        assert "Usage:" in result_help.output

    def test_cli_employees_list_request(self):
        """Verify that this subcommand is valid and returning the expected request."""
        result = invoke_cli(cli_employee, ["list"])
        full_request = result.return_value
        assert result.exit_code == 0
        assert full_request.request.value == Request.LIST_EMPLOYEES.value

    class TestCliEmployeesListFilter:
        """Test the --role-filter option of 'crm employee list' command."""

        def test_cli_employees_list_filter_valid_option(self):
            result = invoke_cli(cli_employee, ["list", "--role-filter", "COMMERCIAL"])
            full_request = result.return_value
            assert result.exit_code == 0
            assert full_request.params["role_filter"] == "COMMERCIAL"

        def test_cli_employees_list_filter_empty_value(self):
            result = invoke_cli(cli_employee, ["list", "--role-filter"])
            assert isinstance(result.exception, BadOptionUsage)

        def test_cli_employees_list_filter_invalid_value(self):
            result = invoke_cli(cli_employee, ["list", "--role-filter", "random"])
            assert isinstance(result.exception, BadParameter)


class TestCliEmployeesDetail:
    """Test the 'crm employee detail' command."""

    def test_cli_employees_detail_help(self):
        """Test the help of the subcommand."""
        result_help = invoke_cli(cli_employee, ["detail", "--help"])
        assert "Usage:" in result_help.output

    def test_cli_employees_detail_request(self):
        """Verify that this subcommand is valid and returning the expected request."""
        result = invoke_cli(cli_employee, ["detail"], input="random")
        full_request = result.return_value
        assert result.exit_code == 0
        assert full_request.request.value == Request.DETAIL_EMPLOYEE.value

    class TestCliEmployeeDetailUsername:
        """Test the --username option of 'crm employee detail' command."""

        def test_cli_employees_detail_username_random_value(self):
            result = invoke_cli(cli_employee, ["detail", "--username", "random"])
            full_request = result.return_value
            assert result.exit_code == 0
            assert full_request.params["username"] == "random"

        def test_cli_employees_detail_username_empty_value(self):
            result = invoke_cli(cli_employee, ["detail", "--username"])
            assert isinstance(result.exception, BadOptionUsage)
