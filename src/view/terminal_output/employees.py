from .display import display_table
from typing import Any


def display_employees(data: dict[str, Any]):
    display_table(title="Employees", data=data)
