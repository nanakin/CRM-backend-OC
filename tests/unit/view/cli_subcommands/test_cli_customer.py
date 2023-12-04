"""
Test the 'crm customer' subcommands.

Usage: crm customer [OPTIONS] COMMAND [ARGS]...

  Commands to manage customers.

Options:
  --help  Show this message and exit.

Commands:
  add             Add a new customer
  detail          Show customer details
  list            List existing customers
  set-commercial  Set a new commercial contact
  update          Update customer data
"""
import pytest
from common import invoke_cli

from crm.view.cli.commands.subcommands import cli_customer
from crm.view.requests import Request


def test_cli_customer_explicit_help():
    """Test the 'crm customer --help' command."""
    result = invoke_cli(cli_customer, ["--help"])
    assert "Usage:" in result.output


@pytest.mark.parametrize("subcommand", [("add", "list", "detail", "set-commercial", "update")])
def test_cli_customer_subcommands(subcommand):
    """Test existence of crm customer subcommands."""

    result = invoke_cli(cli_customer, [subcommand, "--help"])
    assert result.exit_code == 0
    assert "Usage:" in result.output


class TestCliCustomerList:
    """Test the 'crm customer list' command."""

    def test_cli_customer_list_request(self):
        """Verify that this subcommand is valid and returning the expected request."""
        result = invoke_cli(cli_customer, ["list"])
        full_request = result.return_value
        assert result.exit_code == 0
        assert full_request.request.value == Request.LIST_CUSTOMERS.value


class TestCliCustomerDetail:
    """Test the 'crm customer detail' command."""

    def test_cli_customer_detail_request(self):
        """Verify that this subcommand is valid and returning the expected request."""
        result = invoke_cli(cli_customer, ["detail"], input="1")
        full_request = result.return_value
        assert result.exit_code == 0
        assert full_request.request.value == Request.DETAIL_CUSTOMER.value
        assert full_request.params["customer_id"] == 1

    def test_cli_customer_detail_option(self):
        """Test option of 'crm customer detail' command."""
        result = invoke_cli(cli_customer, ["detail", "--customer-id", "1"])
        full_request = result.return_value
        assert result.exit_code == 0
        assert full_request.params["customer_id"] == 1


class TestCliCustomerAdd:
    """Test the 'crm customer add' command."""

    def test_cli_customer_add_request(self):
        """Verify that this subcommand is valid and returning the expected values."""
        result = invoke_cli(
            cli_customer, ["add"], input="random full name\nrandom company\nrandom email\nrandom phone"
        )
        full_request = result.return_value
        assert result.exit_code == 0
        assert full_request.request.value == Request.NEW_CUSTOMER.value
        assert full_request.params["fullname"] == "random full name"
        assert full_request.params["company"] == "random company"
        assert full_request.params["email"] == "random email"
        assert full_request.params["phone"] == "random phone"

    def test_cli_customer_add_options(self):
        """Test options of 'crm customer add' command."""
        result = invoke_cli(
            cli_customer,
            [
                "add",
                "--fullname",
                "random full name",
                "--company",
                "random company",
                "--email",
                "random email",
                "--phone",
                "random phone",
            ],
        )
        full_request = result.return_value
        assert result.exit_code == 0
        assert full_request.params["fullname"] == "random full name"
        assert full_request.params["company"] == "random company"
        assert full_request.params["email"] == "random email"
        assert full_request.params["phone"] == "random phone"


class TestCliCustomerSetCommercial:
    """Test the 'crm customer set-commercial' command."""

    def test_cli_customer_set_commercial_request(self):
        """Verify that this subcommand is valid and returning the expected request."""
        result = invoke_cli(cli_customer, ["set-commercial"], input="1\nrandom_username")
        full_request = result.return_value
        assert result.exit_code == 0
        assert full_request.request.value == Request.SET_CUSTOMER_COMMERCIAL.value
        assert full_request.params["customer_id"] == 1
        assert full_request.params["commercial_username"] == "random_username"

    def test_cli_customer_set_commercial_options(self):
        """Test options of 'crm customer set-commercial' command."""
        result = invoke_cli(cli_customer, ["set-commercial", "--customer-id", "1", "--commercial-username", "random_username"])
        full_request = result.return_value
        assert result.exit_code == 0
        assert full_request.params["customer_id"] == 1
        assert full_request.params["commercial_username"] == "random_username"


class TestCliCustomerUpdate:
    """Test the 'crm customer update' command."""

    def test_cli_customer_update_nothing(self):
        """Verify that this subcommand is failing without field to update."""
        result = invoke_cli(cli_customer, ["update", "1"])
        assert result.exit_code == 1

    @pytest.mark.parametrize(
        "field_name, param_name, value, expected_value",
        [
            ("--fullname", "fullname", "random full name", "random full name"),
            ("--company", "company", "random company", "random company"),
            ("--email", "email", "random email", "random email"),
            ("--phone", "phone", "random phone", "random phone"),
        ],
    )
    def test_cli_customer_update_field(self, field_name, param_name, value, expected_value):
        """Verify that this subcommand is valid and returning the expected request."""
        result = invoke_cli(cli_customer, ["update", "1", field_name], input=value)
        full_request = result.return_value
        assert result.exit_code == 0
        assert full_request.request.value == Request.UPDATE_CUSTOMER.value
        assert full_request.params[param_name] == expected_value
