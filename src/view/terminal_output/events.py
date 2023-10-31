from typing import Any

from .display import display_panel, display_table


def display_events(data: list[Any]):
    columns_attrs = [  # fill column name with the dictionary keys
        {"header": "ID", "justify": "right", "style": "cyan"},
        {"header": "Name", "justify": "center", "style": "magenta"},
        {"header": "Contract", "justify": "left", "style": "yellow"},
        {"header": "Support", "justify": "left", "style": "yellow"},
        {"header": "Commercial", "justify": "left", "style": "green"},
        {"header": "Start", "justify": "left", "style": "green"},
    ]
    display_table("Events", columns_attrs, data)


def display_event(event, focus=None):
    display_panel(title="Event", subtitle=event["ID"], focus=focus, **event)
