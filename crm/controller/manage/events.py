from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID

from .common import Request, Roles, requests_map

if TYPE_CHECKING:
    from crm.model import Model
    from crm.view import View

    from .authentication import Auth


class EventsControllerMixin:
    view: "View"
    model: "Model"
    auth: "Auth"

    # -------------------- CRM Commands below --------------------------

    @requests_map.register(Request.LIST_EVENTS, required_role=Roles.ALL)
    def list_events(self, no_support_assigned: bool) -> None:
        """Retrieve events from database and display them."""
        displayable_events = self.model.get_events(no_support_assigned)
        self.view.display_events(displayable_events)

    @requests_map.register(Request.DETAIL_EVENT, required_role=Roles.ALL)
    def get_event(self, event_id: int) -> None:
        """Retrieve a given event from database and display it."""
        displayable_event = self.model.detail_event(event_id)
        self.view.display_event(displayable_event)

    @requests_map.register(Request.NEW_EVENT, required_role=Roles.COMMERCIAL)
    def new_event(self, contract_uuid: UUID, name: str) -> None:
        """Add a new event to database and display it."""
        displayable_event = self.model.add_event(contract_uuid, name, employee_id=self.auth.user_id)
        self.view.display_event(displayable_event, focus=displayable_event.keys())

    @requests_map.register(Request.SET_EVENT_SUPPORT, required_role=Roles.ADMINISTRATOR)
    def set_event_support(self, event_id: int, username: str) -> None:
        """Update the support associated to event in database and display the event."""
        displayable_event = self.model.set_event_support(event_id, username)
        self.view.display_event(displayable_event, focus=["Support"])

    @requests_map.register(Request.UPDATE_EVENT, required_role=Roles.SUPPORT)
    def update_event(
        self, event_id: int, name: str, start: datetime, end: datetime, attendees: int, location: str, note: str
    ) -> None:
        """Update event fields in database and display the event."""
        displayable_event = self.model.update_event(
            event_id, name, start, end, attendees, location, note, employee_id=self.auth.user_id
        )
        fields_name: dict = {
            "Name": name,
            "Start": start,
            "End": end,
            "Attendees": attendees,
            "Location": location,
            "Note": note,
        }
        self.view.display_event(
            displayable_event, focus=[name for name, new_value in fields_name if new_value is not None]
        )
