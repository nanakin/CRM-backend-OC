from crm.controller.manage.customers import CustomersControllerMixin
from crm.view.cli.commands.subcommands import cli_customer
from tests.integration.cli_signatures.common import matching_signature
from tests.unit.view.cli_subcommands.common import invoke_cli


def test_cli_customer_list_signature():
    """Verify the signature of the 'crm customer list' command."""
    result = invoke_cli(cli_customer, ["list"])
    assert matching_signature(CustomersControllerMixin.list_customers, result.return_value.params)


def test_cli_customer_detail_signature():
    """
    Verify the signature of the mapped controller function and the return value of the 'crm customer detail' command.
    """
    result = invoke_cli(cli_customer, ["detail", "--customer-id", "1"])
    assert matching_signature(CustomersControllerMixin.get_customer, result.return_value.params)


def test_cli_customer_add_signature():
    """
    Verify the signature of the mapped controller function and the return value of the 'crm customer add' command.
    """
    result = invoke_cli(
        cli_customer,
        ["add", "--fullname", "random", "--company", "company", "--phone", "0146310000", "--email", "mail@mail.com"],
    )
    assert matching_signature(CustomersControllerMixin.new_customer, result.return_value.params)
