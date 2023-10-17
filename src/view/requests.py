from enum import Enum, auto


class Request(Enum):
    """List of allowed requests by the view."""

    LOGIN = auto()
    LOGOUT = auto()
    LIST_EMPLOYEES = auto()
    EDIT_EMPLOYEE = auto()
    SET_EMPLOYEE_PASSWORD = auto()
    LIST_CUSTOMERS = auto()
