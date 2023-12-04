"""
Usage: crm event [OPTIONS] COMMAND [ARGS]...

  Commands to manage events.

Options:
  --help  Show this message and exit.

Commands:
  add          Add a new event
  detail       Show event details
  list         List existing events
  set-support  Set a new support contact
  update       Update event data
"""
import uuid
from datetime import datetime

import pytest
from common import invoke_cli

from crm.view.cli.commands.subcommands import cli_event
from crm.view.requests import Request


def test_cli_event_explicit_help():
    """Test the 'crm event --help' command."""
    result = invoke_cli(cli_event, ["--help"])
    assert "Usage:" in result.output


@pytest.mark.parametrize("subcommand", [("add", "list", "detail", "set-support", "update")])
def test_cli_event_subcommands(subcommand):
    """Test existence of crm event subcommands."""

    result = invoke_cli(cli_event, [subcommand, "--help"])
    assert result.exit_code == 0
    assert "Usage:" in result.output


class TestCliEventList:
    """Test the 'crm event list' command."""

    def test_cli_event_list_request(self):
        """Verify that this subcommand is valid and returning the expected request."""
        result = invoke_cli(cli_event, ["list"])
        full_request = result.return_value
        assert result.exit_code == 0
        assert full_request.request.value == Request.LIST_EVENTS.value


class TestCliEventDetail:
    """Test the 'crm event detail' command."""

    def test_cli_event_detail_request(self):
        """Verify that this subcommand is valid and returning the expected request."""
        result = invoke_cli(cli_event, ["detail"], input="1")
        full_request = result.return_value
        assert result.exit_code == 0
        assert full_request.request.value == Request.DETAIL_EVENT.value
        assert full_request.params["event_id"] == 1

    def test_cli_event_detail_option(self):
        """Test the detail option of 'crm event detail' command."""
        result = invoke_cli(cli_event, ["detail", "--event-id", "1"])
        full_request = result.return_value
        assert result.exit_code == 0
        assert full_request.params["event_id"] == 1


class TestCliEventAdd:
    """Test the 'crm event add' command."""

    def test_cli_event_add_request(self):
        """Verify that this subcommand is valid and returning the expected values."""
        result = invoke_cli(cli_event, ["add"], input="123e4567-e89b-12d3-a456-426655440000\nrandom name")
        full_request = result.return_value
        assert result.exit_code == 0
        assert full_request.request.value == Request.NEW_EVENT.value
        assert full_request.params["contract_uuid"] == uuid.UUID("123e4567-e89b-12d3-a456-426655440000")
        assert full_request.params["name"] == "random name"

    def test_cli_event_add_options(self):
        """Test the subcommand with options."""
        result = invoke_cli(
            cli_event, ["add", "--contract-uuid", "123e4567-e89b-12d3-a456-426655440000", "--name", "random name"]
        )
        full_request = result.return_value
        assert result.exit_code == 0
        assert full_request.params["contract_uuid"] == uuid.UUID("123e4567-e89b-12d3-a456-426655440000")
        assert full_request.params["name"] == "random name"


class TestCliEventSetSupport:
    """Test the 'crm event set-support' command."""

    def test_cli_event_add_payment_request(self):
        """Verify that this subcommand is valid and returning the expected values."""
        result = invoke_cli(cli_event, ["set-support"], input="1\nrandom_username")
        full_request = result.return_value
        assert result.exit_code == 0
        assert full_request.request.value == Request.SET_EVENT_SUPPORT.value
        assert full_request.params["event_id"] == 1
        assert full_request.params["username"] == "random_username"

    def test_cli_event_add_payment_options(self):
        """Test the subcommand with options."""
        result = invoke_cli(cli_event, ["set-support", "--event-id", "1", "--username", "random_username"])
        full_request = result.return_value
        assert result.exit_code == 0
        assert full_request.params["event_id"] == 1
        assert full_request.params["username"] == "random_username"


class TestCliEventUpdate:
    """Test the 'crm event update' command."""

    def test_cli_event_update_nothing(self):
        """Verify that this subcommand is failing without field to update."""
        result = invoke_cli(cli_event, ["update", "1"])
        assert result.exit_code == 1

    @pytest.mark.parametrize(
        "field_name, param_name, value, expected_value",
        [
            ("--name", "name", "random name", "random name"),
            ("--start", "start", "2020-01-01 00:00:00", datetime.fromisoformat("2020-01-01 00:00:00")),
            ("--end", "end", "2020-01-01 00:00:00", datetime.fromisoformat("2020-01-01 00:00:00")),
            ("--attendees", "attendees", "10", 10),
            ("--location", "location", "random location", "random location"),
            ("--note", "note", "random note", "random note"),
        ],
    )
    def test_cli_event_update_field(self, field_name, param_name, value, expected_value):
        """Verify that this subcommand is valid and returning the expected request."""
        result = invoke_cli(cli_event, ["update", "1", field_name], input=value)
        full_request = result.return_value
        assert result.exit_code == 0
        assert full_request.request.value == Request.UPDATE_EVENT.value
        assert full_request.params[param_name] == expected_value
