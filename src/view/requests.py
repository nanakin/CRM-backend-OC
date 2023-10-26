from enum import Enum, auto


class Request(Enum):
    """List of allowed requests by the view."""

    LOGIN = auto()
    LOGOUT = auto()

    NEW_EMPLOYEE = auto()
    DETAIL_EMPLOYEE = auto()
    LIST_EMPLOYEES = auto()
    EDIT_EMPLOYEE = auto()
    SET_EMPLOYEE_PASSWORD = auto()
    SET_EMPLOYEE_ROLE = auto()
    DELETE_EMPLOYEE = auto()

    NEW_CUSTOMER = auto()
    DETAIL_CUSTOMER = auto()
    LIST_CUSTOMERS = auto()
    EDIT_CUSTOMER = auto()
    SET_CUSTOMER_COMMERCIAL = auto()
