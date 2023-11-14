import click

from view.requests import Request, FullRequest


@click.group(name="customer")
def cli_customer():
    """Commands to manage customers."""


@cli_customer.command(help="Add a new customer")
@click.option("--fullname", prompt=True, prompt_required=True, type=str, help="Define the customer full name")
@click.option("--company", prompt=True, prompt_required=True, type=str, help="Define the customer company")
@click.option("--email", prompt=True, prompt_required=True, type=str, help="Define the customer email")
@click.option("--phone", prompt=True, prompt_required=True, type=str, help="Define the customer phone")
def add(**kwargs) -> FullRequest:
    """Command to add a new customer."""
    return FullRequest(Request.NEW_CUSTOMER, **kwargs)


@cli_customer.command(help="Update customer data")
@click.argument("customer-id", type=int)
@click.option(
    "--fullname", default=None, prompt=False, prompt_required=False, type=str, help="Define the new full name"
)
@click.option("--company", default=None, prompt=False, prompt_required=True, type=str, help="Define the new company")
@click.option("--email", default=None, prompt=False, prompt_required=True, type=str, help="Define the new email")
@click.option("--phone", default=None, prompt=False, prompt_required=True, type=str, help="Define the new phone")
def update(**kwargs) -> FullRequest:
    """Command to update a customer data (fullname, company, email and phone fields)."""
    return FullRequest(Request.UPDATE_CUSTOMER, **kwargs)


@cli_customer.command(help="Set a new commercial contact")
@click.option("--customer-id", prompt=True, prompt_required=True, type=str, help="Specify the customer ID")
@click.option("--username", prompt=True, prompt_required=True, type=str, help="Specify the username of the commercial")
def set_commercial(**kwargs) -> FullRequest:
    """Command to set a new commercial contact."""
    return FullRequest(Request.SET_CUSTOMER_COMMERCIAL, **kwargs)


@cli_customer.command(help="Show customer details")
@click.option("--customer-id", prompt=True, prompt_required=True, type=str, help="Specify the customer ID")
def detail(**kwargs) -> FullRequest:
    """Command to show customer details."""
    return FullRequest(Request.DETAIL_CUSTOMER, **kwargs)


@cli_customer.command(help="List existing customers", name="list")
def listing() -> FullRequest:
    """Command to list existing customers."""
    return FullRequest(Request.LIST_CUSTOMERS)
