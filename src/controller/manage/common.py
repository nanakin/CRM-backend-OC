from enum import Flag, auto
from typing import TYPE_CHECKING, Callable, Optional
from dataclasses import dataclass

from model import OperationFailed
from view.log import LogStatus
from view.requests import Request  # noqa
from functools import wraps

if TYPE_CHECKING:
    from controller.core import Controller


class Roles(Flag):
    """Employees roles as Enum to be used in the controller permission."""
    NONE = auto()
    COMMERCIAL = auto()
    SUPPORT = auto()
    ADMINISTRATOR = auto()
    ALL = COMMERCIAL | SUPPORT | ADMINISTRATOR


@dataclass
class Auth:
    """Store authentication information."""

    @dataclass
    class User:
        """Store profile of the authenticated employee."""
        username: str
        id: int
        fullname: str
        role: Roles

    user: Optional[User] = None

    @property
    def user_id(self) -> Optional[int]:
        return self.user.id if self.user else None

    @property
    def is_authenticated(self) -> bool:
        return self.user is not None

    def identify_as(self, username: str, employee_id: int, fullname: str, role: Roles) -> None:
        """Keep track of the authenticated user."""
        self.user = self.User(username, employee_id, fullname, role)


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
        def authenticate_as_role(controller: "Controller", required_role: Roles) -> None:
            """
            Try to authenticate the user and raise an exception if the user does not have the required permissions.
            """
            auth = controller.authenticate()
            if not auth.is_authenticated:
                raise OperationFailed("Authentication failed.")
            if required_role != Roles.NONE and auth.user.role not in required_role:  # type: ignore
                raise OperationFailed(f"{auth.user.fullname} does not have necessary permissions.")

        def wrap(func) -> Callable:
            @wraps(func)  # preserve original signature of the decorated function
            def notif_and_authenticate_wrap(controller: "Controller", *args, **kwargs) -> None:
                """Add a wrapper that notifies the user of the operation result."""
                def decorated_func(*controller_args, **controller_kwargs):
                    if required_role is not None:
                        try:
                            authenticate_as_role(controller, required_role)
                        except OperationFailed as e:
                            controller.view.notification(LogStatus.WARNING, str(e))
                            return
                    try:
                        func(*controller_args, **controller_kwargs)
                    except OperationFailed as e:
                        controller.view.notification(LogStatus.WARNING, str(e))
                    else:
                        controller.view.notification(LogStatus.INFO, "Successful operation.")
                return decorated_func(controller, *args, **kwargs)
            self.allowed_functions[request] = notif_and_authenticate_wrap
            return notif_and_authenticate_wrap

        return wrap


# global singleton that facilitate mapping of controller methods without having to instantiate the controller first
requests_map = RequestsMapping()
