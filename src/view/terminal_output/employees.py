from typing import Any

from rich.prompt import Prompt

from .display import display_table


def display_employees(data: list[Any]):
    columns_attrs = [
        {"header": "ID", "justify": "right", "style": "cyan"},
        {"header": "Nom complet", "justify": "center", "style": "magenta"},
        {"header": "Identifiant", "justify": "left", "style": "yellow"},
    ]
    display_table("Employees", columns_attrs, data)


def ask_credentials():
    username = Prompt.ask("Username")
    password = Prompt.ask("Password", password=True)
    return username, password
