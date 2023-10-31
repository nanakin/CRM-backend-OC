from typing import Any

from .display import display_panel, display_table


def display_customers(data: list[Any]):
    columns_attrs = [  # fill column name with the dictionary keys
        {"header": "ID", "justify": "right", "style": "cyan"},
        {"header": "Full name", "justify": "center", "style": "magenta"},
        {"header": "Company", "justify": "left", "style": "yellow"},
        {"header": "Commercial", "justify": "left", "style": "green"},
    ]
    display_table("Customers", columns_attrs, data)


def display_customer(customer, focus=None):
    display_panel(title="Customer", subtitle=customer["Full name"], focus=focus, **customer)
