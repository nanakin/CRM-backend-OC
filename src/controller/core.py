from .manage import (
    AuthenticationControllerMixin,
    CustomersControllerMixin,
    EmployeesControllerMixin,
    EventsControllerMixin,
    requests_map,
)

from view import Request, FullRequest


class Controller(
    EmployeesControllerMixin, CustomersControllerMixin, EventsControllerMixin, AuthenticationControllerMixin
):
    def _execute(self,  full_request: FullRequest):
        """Execute the command corresponding to the given user request."""
        to_execute = requests_map.allowed[full_request.request]
        to_execute(self, **full_request.params)

    def read_and_execute_command(self):
        """Read the user input and execute the corresponding command."""
        full_request = self.view.read_user_input()
        if full_request:
            self._execute(full_request)
        # else : user asked for help (using --help, or launching app without argument) > no command to execute

    def __init__(self, view, model):
        """Initialize the controller."""
        self.view = view
        self.model = model
        self.authenticated_user = None
