from rich.table import Table
from rich.text import Text
from .console import console
from typing import Any
from view.log import LogStatus


def display_table(title: str, columns_attrs: list[dict], rows: list[Any]) -> None:
    table = Table(title=title)
    for column_attrs in columns_attrs:
        table.add_column(**column_attrs)
    for row in rows:
        elements = row.as_printable_tuple()
        table.add_row(*elements)
    console.print(table)


def notification(status, message):
    if status == LogStatus.INFO:
        info(message)
    elif status == LogStatus.WARNING:
        warning(message)


def info(message):
    text = Text(message)
    text.stylize("bold green")
    console.print(text)


def warning(message):
    text = Text(message)
    text.stylize("bold red")
    console.print(text)
