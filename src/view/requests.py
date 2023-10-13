from enum import Enum, auto
from typing import Any


class Request(Enum):
    """List of allowed requests by the view."""

    LIST_EMPLOYEES = auto()
    EDIT_EMPLOYEE = auto()
