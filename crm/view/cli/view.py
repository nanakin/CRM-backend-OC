from typing import Iterable, Optional

from crm.view.interface import IView
from crm.view.log import LogStatus
from crm.view.requests import FullRequest

from .commands import cli_main
from .terminal.display import display_panel, display_table, notification
from .terminal.input import ask_credentials


class View(IView):
    """Methods to display or to interacts with the user."""

    colors = {
        "Support": "green",
        "Commercial": "light_goldenrod2",
        "Customer": "dark_orange",
        "Contract": "cornsilk1",
        "Event": "pink1",
        "Employee": "cyan",
        "ID": "bright_white",
    }

    def notification(self, status: LogStatus, message: str) -> None:
        notification(status, message)

    def ask_credentials(self) -> tuple[str, str]:
        return ask_credentials()

    def read_user_input(self) -> Optional[FullRequest]:
        return cli_main()

    def display_employees(self, data: list[dict]):
        colors = {"title": View.colors["Employee"], "Full name": View.colors["Employee"], **View.colors}
        display_table(title="Employees 👷 ", data=data, colors=colors)

    def display_employee(self, data: dict, focus: Optional[Iterable] = None):
        colors = {"title": View.colors["Employee"]}
        display_panel(title="Employee 👷 ", data=data, subtitle=data["Full name"], focus=focus, colors=colors)

    def display_customers(self, data: list[dict]):
        colors = {"title": View.colors["Customer"], "Full name": View.colors["Customer"], **View.colors}
        display_table(title="Customers 🏭 ", data=data, colors=colors)

    def display_customer(self, data: dict, focus: Optional[Iterable] = None):
        colors = {"title": View.colors["Customer"]}
        display_panel(title="Customer 🏭 ", data=data, subtitle=data["Full name"], focus=focus, colors=colors)

    def display_contracts(self, data: list[dict]):
        colors = {"title": View.colors["Contract"], "UUID": View.colors["Contract"], **View.colors}
        display_table(title="Contracts 📃 ", data=data, colors=colors)

    def display_contract(self, data: dict, focus: Optional[Iterable] = None):
        colors = {"title": View.colors["Contract"]}
        display_panel(title="Contract 📃 ", data=data, subtitle=data["UUID"], focus=focus, colors=colors)

    def display_events(self, data: list[dict]):
        colors = {"title": View.colors["Event"], "Name": View.colors["Event"], **View.colors}
        display_table(title="Events 🎪 ", data=data, colors=colors)

    def display_event(self, data: dict, focus: Optional[Iterable] = None):
        colors = {"title": View.colors["Event"]}
        display_panel(title="Event 🎪 ", data=data, subtitle=data["Name"], focus=focus, colors=colors)

    def __init__(self):
        pass
