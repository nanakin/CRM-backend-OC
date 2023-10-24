from typing import Any

from rich.prompt import Prompt
from .console import console
from .display import display_table, display_panel


def display_employees(data: list[Any]):
    columns_attrs = [
        {"header": "ID", "justify": "right", "style": "cyan"},
        {"header": "Nom complet", "justify": "center", "style": "magenta"},
        {"header": "Identifiant", "justify": "left", "style": "yellow"},
        {"header": "Role", "justify": "left", "style": "green"}
    ]
    display_table("Employees", columns_attrs, data)


def display_employee(employee):
    display_panel("Employee", employee["Full name"], employee)


def ask_credentials():
    console.print("This action requires user authentication")
    username = Prompt.ask("Username")
    password = Prompt.ask("Password", password=True)
    return username, password
