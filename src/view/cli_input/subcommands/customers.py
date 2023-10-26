import click

from view.requests import Request


@click.group(name="customer")
def cli_customer():
    """Commands to manage customers"""
    pass


@cli_customer.command(help="Add a new customer")
@click.option("--fullname", prompt=True, prompt_required=True, type=str, help="Define the customer full name")
@click.option("--company", prompt=True, prompt_required=True, type=str, help="Define the customer company")
@click.option("--email", prompt=True, prompt_required=True, type=str, help="Define the customer email")
@click.option("--phone", prompt=True, prompt_required=True, type=str, help="Define the customer phone")
def add(fullname, company, email, phone):
    return Request.NEW_CUSTOMER, fullname, company, email, phone


@cli_customer.command(help="Update customer data")
@click.argument("id", type=int)
@click.option("--fullname", default=None, prompt=False, prompt_required=False, type=str, help="Define the new full name")
@click.option("--company", default=None, prompt=False, prompt_required=True, type=str, help="Define the new company")
@click.option("--email", default=None, prompt=False, prompt_required=True, type=str, help="Define the new email")
@click.option("--phone", default=None, prompt=False, prompt_required=True, type=str, help="Define the new phone")
def update(id, fullname, company, email, phone):
    return Request.EDIT_CUSTOMER, id, fullname, company, email, phone


@click.option("--id",  prompt=True, prompt_required=True, type=str, help="Specify the customer ID")
@click.option("--username",  prompt=True, prompt_required=True, type=str, help="Specify the username of the commercial")
@cli_customer.command(help="Set a new commercial contact")
def setcommercial(id, username):
    return Request.SET_CUSTOMER_COMMERCIAL, id, username


@click.option("--id", prompt=True, prompt_required=True, type=str, help="Specify the customer ID")
@cli_customer.command(help="Show customer details")
def detail(id):
    return Request.DETAIL_CUSTOMER, id


@cli_customer.command(help="List existing customers")
def list():
    return Request.LIST_CUSTOMERS
