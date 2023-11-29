import click

from crm.view.requests import FullRequest, Request


@click.group(name="event")
def cli_event():
    """Commands to manage events."""


@cli_event.command(help="Add a new event")
@click.option(
    "--contract-uuid", prompt=True, prompt_required=True, type=click.UUID, help="Define the related contract"
)
@click.option("--name", prompt=True, prompt_required=True, type=str, help="Define the event name")
def add(**kwargs) -> FullRequest:
    """Command to add a new event."""
    return FullRequest(Request.NEW_EVENT, **kwargs)


@cli_event.command(help="Set a new support contact")
@click.option("--event-id", prompt=True, prompt_required=True, type=int, help="Specify the event")
@click.option("--username", prompt=True, prompt_required=True, type=str, help="Specify the support")
def set_support(**kwargs) -> FullRequest:
    """Command to set a new support contact."""
    return FullRequest(Request.SET_EVENT_SUPPORT, **kwargs)


@cli_event.command(help="Update event data")
@click.argument("event-id", type=int)
@click.option("--name", default=None, prompt=True, prompt_required=False, type=str, help="Define a new name")
@click.option(
    "--start", default=None, prompt=True, prompt_required=False, type=click.DateTime(), help="Define the start time"
)
@click.option(
    "--end", default=None, prompt=True, prompt_required=False, type=click.DateTime(), help="Define the end time"
)
@click.option(
    "--attendees", default=None, prompt=True, prompt_required=False, type=int, help="Define the number of attendees"
)
@click.option("--location", default=None, prompt=True, prompt_required=False, type=str, help="Define the location")
@click.option("--note", default=None, prompt=True, prompt_required=False, type=str, help="Define a note")
def update(**kwargs) -> FullRequest:
    """Command to update an event data (name, start, end, attendees, location and note fields)."""
    if all(value is None for key, value in kwargs.items() if key != "event_id"):
        raise click.BadParameter("You must specify at least one field to update.")
    return FullRequest(Request.UPDATE_EVENT, **kwargs)


@cli_event.command(help="Show event details")
@click.option("--event-id", prompt=True, prompt_required=True, type=int, help="Specify the event")
def detail(**kwargs) -> FullRequest:
    """Command to show event details."""
    return FullRequest(Request.DETAIL_EVENT, **kwargs)


@cli_event.command(help="List existing events")
@click.option("--no-support-assigned", is_flag=True, default=False, help="Display events without support only")
def list(**kwargs) -> FullRequest:
    """Command to list existing events."""
    return FullRequest(Request.LIST_EVENTS, **kwargs)
