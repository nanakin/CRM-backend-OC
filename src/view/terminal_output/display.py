from rich.table import Table
from .console import console
from typing import Any


def display_table(title: str, columns_attrs: list[dict], rows: list[Any]) -> None:
    table = Table(title=title)
    for column_attrs in columns_attrs:
        table.add_column(**column_attrs)
    for row in rows:
        elements = row.as_printable_tuple()
        table.add_row(*elements)
    console.print(table)
