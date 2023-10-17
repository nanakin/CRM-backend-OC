import click
from view.requests import Request


@click.group(name="customer")
def cli_customer():
    """Commands to manage employees"""
    pass


@cli_customer.command(help="Add a new customer")
def add():
    pass


@cli_customer.command(help="List existing customers")
def list():
    return Request.LIST_CUSTOMERS
