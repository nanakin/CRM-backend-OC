import click

from view.requests import Request


@click.group(name="event")
def cli_event():
    """Commands to manage events"""
    pass


@cli_event.command(help="Add a new event")
@click.option(
    "--contract-uuid", prompt=True, prompt_required=True, type=click.UUID, help="Define the related contract"
)
@click.option("--name", prompt=True, prompt_required=True, type=str, help="Define the event name")
def add(contract_uuid, name):
    return Request.NEW_EVENT, contract_uuid, name


@cli_event.command(help="Set a new support contact")
@click.option("--id", prompt=True, prompt_required=True, type=int, help="Specify the event")
@click.option("--username", prompt=True, prompt_required=True, type=str, help="Specify the support")
def set_support(id, username):
    return Request.SET_EVENT_SUPPORT, id, username


@cli_event.command(help="Update event data")
@click.argument("id", type=int)
@click.option("--name", default=None, prompt=False, prompt_required=False, type=str, help="Define a new name")
@click.option(
    "--start", default=None, prompt=False, prompt_required=False, type=click.DateTime(), help="Define the start time"
)
@click.option(
    "--end", default=None, prompt=False, prompt_required=False, type=click.DateTime(), help="Define the end time"
)
@click.option(
    "--attendees", default=None, prompt=False, prompt_required=False, type=int, help="Define the number of attendees"
)
@click.option("--location", default=None, prompt=False, prompt_required=False, type=str, help="Define the location")
@click.option("--note", default=None, prompt=False, prompt_required=False, type=str, help="Define a note")
def update(id, name, start, end, attendees, location, note):
    # to-do: if no option, prompt
    return Request.UPDATE_EVENT, id, name, start, end, attendees, location, note


@cli_event.command(help="Show event detail")
@click.option("--id", prompt=True, prompt_required=True, type=int, help="Specify the event")
def detail(id):
    return Request.DETAIL_EVENT, id


@cli_event.command(help="List existing events")
@click.option("--not-signed-filter", is_flag=True, default=False, help="Display not signed contracts only")
@click.option("--not-paid-filter", is_flag=True, default=False, help="Display not paid contracts only")
def list(not_signed_filter, not_paid_filter):
    return Request.LIST_EVENTS, not_signed_filter, not_paid_filter
