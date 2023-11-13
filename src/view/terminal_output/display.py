from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from view.log import LogStatus

from .console import console


def display_table(title: str, data: list[dict], colors: dict[str, str]):
    """Display a nice colored table with the given title and data."""
    title_color = colors.get("title")
    table = Table(title=title, title_style=title_color, expand=True)
    if data:
        for column_n, key in enumerate(data[0].keys()):
            color = colors.get(key, "white")
            print(f"{key=} {color=}")
            table.add_column(key, justify="left", style=color)
        for row in data:
            table.add_row(*row.values())
    console.print(table)


def display_panel(title: str, data: dict, subtitle: str,  colors: dict[str, str], focus: list | None):
    """Display a nice colored panel with the given titles and data."""
    title_color = colors.get("title")
    to_print = Text()
    for key, value in data.items():
        to_print.append(key + ": ", style="yellow" if focus and key in focus else "sky_blue2")
        to_print.append(value + "\n", style="yellow" if focus and key in focus else "light_cyan1")
    console.print(
        Panel(to_print, title=title, subtitle=subtitle, expand=False),
        justify="center    ", style=title_color)  # type: ignore [arg-type]


def _info(message: str):
    """Display an informative message."""
    text = Text("✅ " + message)
    text.stylize("bold green")
    console.print(text)


def _warning(message: str):
    """Display a warning message."""
    text = Text("⚠️  " + message)
    text.stylize("bold red")
    console.print(text)


def notification(status: LogStatus, message: str):
    """Display a nice message."""
    if status == LogStatus.INFO:
        _info(message)
    elif status == LogStatus.WARNING:
        _warning(message)
