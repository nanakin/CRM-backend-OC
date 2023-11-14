from click import BadParameter, BadOptionUsage
from common import invoke_cli
from src.view.cli.commands.subcommands import cli_employee
from src.view.requests import Request



def test_cli_employees_help():
    """Test the crm employee command (without subcommand)."""
    result = invoke_cli(cli_employee, [])
    assert "Usage:" in result.output

    result = invoke_cli(cli_employee, ["--help"])
    assert "Usage:" in result.output

# crm employee list -----------------------------------------------------------


def test_cli_employees_list_help():
    """Test the help of crm employee list command."""
    result_help = invoke_cli(cli_employee, ["list", "--help"])
    assert "Usage:" in result_help.output


def test_cli_employees_list():
    """Test the crm employee list command."""
    result = invoke_cli(cli_employee, ["list"])
    full_request = result.return_value
    assert result.exit_code == 0
    assert full_request.request.value == Request.LIST_EMPLOYEES.value


def test_cli_employees_list_filter():
    """Test the --role-filter option of crm employee list command."""
    result = invoke_cli(cli_employee, ["list", "--role-filter", "COMMERCIAL"])
    full_request = result.return_value
    assert result.exit_code == 0
    assert full_request.params["role_filter"] == "COMMERCIAL"

    result = invoke_cli(cli_employee, ["list", "--role-filter"])
    assert isinstance(result.exception, BadOptionUsage)

    result = invoke_cli(cli_employee, ["list", "--role-filter", "random"])
    assert isinstance(result.exception, BadParameter)

# crm employee detail -----------------------------------------------------------


def test_cli_employees_detail_help():
    """Test the help of crm employee list command."""
    result_help = invoke_cli(cli_employee, ["detail", "--help"])
    assert "Usage:" in result_help.output


def test_cli_employees_detail():
    """Test the crm employee detail command."""
    result = invoke_cli(cli_employee, ["detail"], input="random")
    full_request = result.return_value
    assert result.exit_code == 0
    assert full_request.request.value == Request.DETAIL_EMPLOYEE.value

    result = invoke_cli(cli_employee, ["detail", "--username"])
    assert isinstance(result.exception, BadOptionUsage)

    result = invoke_cli(cli_employee, ["detail", "--username", "random"])
    full_request = result.return_value
    assert result.exit_code == 0
    assert full_request.params["username"] == "random"


