from .common import Request, Roles, requests_map


class EventsControllerMixin:
    # -------------------- CRM Commands below --------------------------

    @requests_map.register(Request.LIST_EVENTS, required_role=Roles.ALL)
    def list_events(self, not_signed_filter, not_paid_filter):
        displayable_events = self.model.get_events(not_signed_filter, not_paid_filter)
        self.view.display_events(displayable_events)

    @requests_map.register(Request.DETAIL_EVENT, required_role=Roles.ALL)
    def get_event(self, event_id):
        displayable_event = self.model.detail_event(event_id)
        self.view.display_event(displayable_event)

    @requests_map.register(Request.NEW_EVENT, required_role=Roles.COMMERCIAL)
    def new_event(self, contract_uuid, name):
        displayable_event = self.model.add_event(contract_uuid, name, authenticated_user=self.authenticated_user.username)
        self.view.display_event(displayable_event, focus=displayable_event.keys())

    @requests_map.register(Request.SET_EVENT_SUPPORT, required_role=Roles.ADMINISTRATOR)
    def set_event_support(self, event_id, support_username):
        displayable_event = self.model.set_event_support(event_id, support_username)
        self.view.display_event(displayable_event, focus=("Support",))

    @requests_map.register(Request.UPDATE_EVENT, required_role=Roles.SUPPORT)
    def update_event(self, event_id, name, start, end, attendees, location, note):
        displayable_event = self.model.update_event(event_id, name, start, end, attendees, location, note, authenticated_user=self.authenticated_user.username)
        self.view.display_event(displayable_event,
                                focus=("Name" if name else None,
                                       "Start" if start else None,
                                       "End" if end else None,
                                       "Attendees" if attendees else None,
                                       "Location" if location else None,
                                       "Note" if note else None))
