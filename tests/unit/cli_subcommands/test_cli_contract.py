"""
Test the 'crm contract' subcommands.

Usage: crm contract [OPTIONS] COMMAND [ARGS]...

  Commands to manage contracts.

Options:
  --help  Show this message and exit.

Commands:
  add          Add a new contract
  add-payment  Add a new payment
  detail       Show contract details
  list         List existing contracts
  sign         Sign contract
  update       Update contract amount
"""
import uuid

import pytest
from common import invoke_cli

from crm.view.cli.commands.subcommands import cli_contract
from crm.view.requests import Request


def test_cli_contract_explicit_help():
    """Test the 'crm contract --help' command."""
    result = invoke_cli(cli_contract, ["--help"])
    assert "Usage:" in result.output


@pytest.mark.parametrize("subcommand", [("add", "list", "detail", "sign", "update", "add-payment")])
def test_cli_contract_subcommands(subcommand):
    """Test existence of crm contract subcommands."""

    result = invoke_cli(cli_contract, [subcommand, "--help"])
    assert result.exit_code == 0
    assert "Usage:" in result.output


class TestCliContractList:
    """Test the 'crm contract list' command."""

    def test_cli_contract_list_request(self):
        """Verify that this subcommand is valid and returning the expected request."""
        result = invoke_cli(cli_contract, ["list"])
        full_request = result.return_value
        assert result.exit_code == 0
        assert full_request.request.value == Request.LIST_CONTRACTS.value

    @pytest.mark.parametrize(
        "filter_option, filter_param",
        [("--not-signed-filter", "not_signed_filter"), ("--not-paid-filter", "not_paid_filter")],
    )
    def test_cli_contract_list_filter_valid_option(self, filter_option, filter_param):
        """Test the filters option of 'crm contract list' command."""
        result = invoke_cli(cli_contract, ["list", filter_option])
        full_request = result.return_value
        assert result.exit_code == 0
        assert full_request.params[filter_param] is True


class TestCliContractDetail:
    """Test the 'crm contract detail' command."""

    def test_cli_contract_detail_request(self):
        """Verify that this subcommand is valid and returning the expected request."""
        result = invoke_cli(cli_contract, ["detail"], input="123e4567-e89b-12d3-a456-426655440000")
        full_request = result.return_value
        assert result.exit_code == 0
        assert full_request.request.value == Request.DETAIL_CONTRACT.value
        assert full_request.params["contract_uuid"] == uuid.UUID("123e4567-e89b-12d3-a456-426655440000")

    def test_cli_contract_detail_options(self):
        """Test the detail option of 'crm contract detail' command."""
        result = invoke_cli(cli_contract, ["detail", "--contract-uuid", "123e4567-e89b-12d3-a456-426655440000"])
        full_request = result.return_value
        assert result.exit_code == 0
        assert full_request.params["contract_uuid"] == uuid.UUID("123e4567-e89b-12d3-a456-426655440000")


class TestCliContractAdd:
    """Test the 'crm contract add' command."""

    def test_cli_contract_add_request(self):
        """Verify that this subcommand is valid and returning the expected values."""
        result = invoke_cli(cli_contract, ["add"], input="1\n20.90")
        full_request = result.return_value
        assert result.exit_code == 0
        assert full_request.request.value == Request.NEW_CONTRACT.value
        assert full_request.params["customer_id"] == 1
        assert full_request.params["total_amount"] == 20.90

    def test_cli_contract_add_options(self):
        """Test options of 'crm contract add' command."""
        result = invoke_cli(cli_contract, ["add", "--customer-id", "1", "--total-amount", "20.90"])
        full_request = result.return_value
        full_request = result.return_value
        assert result.exit_code == 0
        assert full_request.params["customer_id"] == 1
        assert full_request.params["total_amount"] == 20.90


class TestCliContractSign:
    """Test the 'crm contract sign' command."""

    def test_cli_contract_sign_request(self):
        """Verify that this subcommand is valid and returning the expected request."""
        result = invoke_cli(cli_contract, ["sign"], input="123e4567-e89b-12d3-a456-426655440000")
        full_request = result.return_value
        assert result.exit_code == 0
        assert full_request.request.value == Request.SIGN_CONTRACT.value
        assert full_request.params["contract_uuid"] == uuid.UUID("123e4567-e89b-12d3-a456-426655440000")

    def test_cli_contract_sign_options(self):
        """Test option of 'crm contract sign' command."""
        result = invoke_cli(cli_contract, ["sign", "--contract-uuid", "123e4567-e89b-12d3-a456-426655440000"])
        full_request = result.return_value
        assert result.exit_code == 0
        assert full_request.params["contract_uuid"] == uuid.UUID("123e4567-e89b-12d3-a456-426655440000")


class TestCliContractAddPayment:
    """Test the 'crm contract add-payment' command."""

    def test_cli_contract_add_payment_request(self):
        """Verify that this subcommand is valid and returning the expected values."""
        result = invoke_cli(cli_contract, ["add-payment"], input="123e4567-e89b-12d3-a456-426655440000\n20.90")
        full_request = result.return_value
        assert result.exit_code == 0
        assert full_request.request.value == Request.ADD_CONTRACT_PAYMENT.value
        assert full_request.params["contract_uuid"] == uuid.UUID("123e4567-e89b-12d3-a456-426655440000")
        assert full_request.params["payment"] == 20.90

    def test_cli_contract_add_payment_options(self):
        """Test options of 'crm contract add-payment' command."""
        result = invoke_cli(
            cli_contract,
            ["add-payment", "--contract-uuid", "123e4567-e89b-12d3-a456-426655440000", "--payment", "20.90"],
        )
        full_request = result.return_value
        assert result.exit_code == 0
        assert full_request.params["contract_uuid"] == uuid.UUID("123e4567-e89b-12d3-a456-426655440000")
        assert full_request.params["payment"] == 20.90


class TestCliContractUpdate:
    """Test the 'crm contract update' command."""

    def test_cli_contract_update_nothing(self):
        """Verify that this subcommand is failing without field to update."""
        result = invoke_cli(cli_contract, ["update", "1"])
        assert result.exit_code == 1

    @pytest.mark.parametrize(
        "field_name, param_name, value, expected_value",
        [("--customer-id", "customer_id", "1", 1), ("--total-amount", "total_amount", "208.76", 208.76)],
    )
    def test_cli_contract_update_field(self, field_name, param_name, value, expected_value):
        """Verify that this subcommand is valid and returning the expected request."""
        result = invoke_cli(cli_contract, ["update", "123e4567-e89b-12d3-a456-426655440000", field_name], input=value)
        full_request = result.return_value
        assert result.exit_code == 0
        assert full_request.request.value == Request.UPDATE_CONTRACT.value
        assert full_request.params[param_name] == expected_value
