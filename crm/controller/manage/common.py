from enum import Flag, auto
from functools import wraps
from typing import TYPE_CHECKING, Callable

from crm.model import OperationFailed
from crm.view import ViewOperationFailed
from crm.view.log import LogStatus
from crm.view.requests import Request  # noqa

if TYPE_CHECKING:
    from crm.controller.core import Controller


class Roles(Flag):
    """Employees roles as Enum to be used in the controller permission."""

    NONE = auto()
    COMMERCIAL = auto()
    SUPPORT = auto()
    ADMINISTRATOR = auto()
    ALL = COMMERCIAL | SUPPORT | ADMINISTRATOR | NONE


class RequestsMapping:
    """Map view requests to a controller methods."""

    def __init__(self) -> None:
        """Initialize the mapping dictionary."""
        self.allowed_functions: dict[Request, Callable] = {}

    def register(self, request: Request, required_role: Roles | None = None) -> Callable:
        """
        Decorator to match a controller method and its corresponding view request (+ required permissions).

        Decorated methods are then called by the controller _execute method, using a Request key (given by the view).
        """

        def wrap(func) -> Callable:
            @wraps(func)  # preserve original signature of the decorated function
            def notif_and_authenticate_wrap(controller: "Controller", *args, **kwargs) -> None:
                """Add a wrapper that notifies the user of the operation result."""

                def decorated_func(*controller_args, **controller_kwargs):
                    if required_role is not None:
                        try:
                            controller.authenticate_as_role(required_role)
                        except (OperationFailed, ViewOperationFailed) as e:
                            controller.view.notification(LogStatus.WARNING, str(e))
                            raise e
                    try:
                        func(*controller_args, **controller_kwargs)
                    except OperationFailed as e:
                        controller.view.notification(LogStatus.WARNING, str(e))
                        raise e
                    else:
                        controller.view.notification(LogStatus.INFO, "Successful operation.")

                return decorated_func(controller, *args, **kwargs)

            self.allowed_functions[request] = notif_and_authenticate_wrap
            return notif_and_authenticate_wrap

        return wrap


# global singleton that facilitate mapping of controller methods without having to instantiate the controller first
requests_map = RequestsMapping()
