from typing import Any

from .display import display_panel, display_table


def display_contracts(data: list[Any]):
    columns_attrs = [  # fill column name with the dictionary keys
        {"header": "Uuid", "justify": "right", "style": "cyan"},
        {"header": "Customer", "justify": "center", "style": "magenta"},
        {"header": "Signed", "justify": "left", "style": "yellow"},
        {"header": "Amount due", "justify": "left", "style": "green"},
    ]
    display_table("Contracts", columns_attrs, data)


def display_contract(contract, focus=None):
    display_panel(title="Contract", subtitle=contract["UUID"], focus=focus, **contract)
