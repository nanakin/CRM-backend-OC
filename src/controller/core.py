from typing import TYPE_CHECKING

from view import FullRequest

from .manage import (
    Auth,
    AuthenticationControllerMixin,
    ContractsControllerMixin,
    CustomersControllerMixin,
    EmployeesControllerMixin,
    EventsControllerMixin,
    requests_map,
)

if TYPE_CHECKING:
    from model import Model
    from view import View


class Controller(
    EmployeesControllerMixin,
    CustomersControllerMixin,
    EventsControllerMixin,
    AuthenticationControllerMixin,
    ContractsControllerMixin,
):
    """Controller class to act as logical interface between the view and the model."""

    def _execute(self, full_request: FullRequest) -> None:
        """Execute the command corresponding to the given user request."""
        to_execute = requests_map.allowed_functions[full_request.request]
        to_execute(self, **full_request.params)

    def read_and_execute_command(self) -> None:
        """Read the user input and execute the corresponding command."""
        full_request = self.view.read_user_input()
        if full_request:
            self._execute(full_request)

    def __init__(self, view: "View", model: "Model") -> None:
        """Initialize the controller."""
        self.view = view
        self.model = model
        self.auth = Auth()
