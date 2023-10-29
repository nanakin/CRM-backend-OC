import click

from view.requests import Request


@click.group(name="contract")
def cli_contract():
    """Commands to manage contracts"""
    pass


@cli_contract.command(help="Add a new contract")
@click.option("--customer-id", prompt=True, prompt_required=True, type=int, help="Define the related customer")
@click.option("--total-amount", prompt=True, prompt_required=True, type=int, help="Define the total amount")
def add(customer_id, total_amount):
    return Request.NEW_CONTRACT, customer_id, total_amount


@cli_contract.command(help="Sign contract")
@click.option("--uuid",  prompt=True, prompt_required=True, type=click.UUID, help="Specify the contract")
def sign(uuid):
    return Request.SIGN_CONTRACT, uuid


@click.option("--uuid",  prompt=True, prompt_required=True, type=click.UUID, help="Specify the contract")
@click.option("--payment",  prompt=True, prompt_required=True, default=0, type=int, help="Specify the amount paid")
@cli_contract.command(help="Add a new payment")
def add_payment(uuid, payment):
    return Request.ADD_CONTRACT_PAYMENT, uuid, payment


@cli_contract.command(help="Update contract amount")
@click.argument("uuid", type=click.UUID)
@click.option("--total-amount", default=None, prompt=False, prompt_required=False, type=int, help="Define the new total amount")
@click.option("--customer-id", default=None, prompt=False, prompt_required=False, type=int, help="Define the new customer")
def update(uuid, customer_id, total_amount):
    # to-do: if no option, prompt
    return Request.UPDATE_CONTRACT, uuid, customer_id, total_amount


@click.option("--uuid", prompt=True, prompt_required=True, type=click.UUID, help="Specify the contract")
@cli_contract.command(help="Show contract detail")
def detail(uuid):
    return Request.DETAIL_CONTRACT, uuid


@click.option('--not-signed-filter', is_flag=True, default=False, help="Display not signed contracts only")
@click.option('--not-paid-filter', is_flag=True, default=False, help="Display not paid contracts only")
@cli_contract.command(help="List existing contracts")
def list(not_signed_filter, not_paid_filter):
    return Request.LIST_CONTRACTS, not_signed_filter, not_paid_filter
