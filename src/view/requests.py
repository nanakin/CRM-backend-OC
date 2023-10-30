from enum import Enum, auto


class Request(Enum):
    """List of allowed requests by the view."""

    LOGIN = auto()
    LOGOUT = auto()

    NEW_EMPLOYEE = auto()
    DETAIL_EMPLOYEE = auto()
    LIST_EMPLOYEES = auto()
    UPDATE_EMPLOYEE = auto()
    SET_EMPLOYEE_PASSWORD = auto()
    SET_EMPLOYEE_ROLE = auto()
    DELETE_EMPLOYEE = auto()

    NEW_CUSTOMER = auto()
    DETAIL_CUSTOMER = auto()
    LIST_CUSTOMERS = auto()
    UPDATE_CUSTOMER = auto()
    SET_CUSTOMER_COMMERCIAL = auto()

    NEW_CONTRACT = auto()
    DETAIL_CONTRACT = auto()
    LIST_CONTRACTS = auto()
    SIGN_CONTRACT = auto()
    ADD_CONTRACT_PAYMENT = auto()
    UPDATE_CONTRACT = auto()

    NEW_EVENT = auto()
    DETAIL_EVENT = auto()
    LIST_EVENTS = auto()
    SET_EVENT_SUPPORT = auto()
    UPDATE_EVENT = auto()
