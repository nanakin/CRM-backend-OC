from .cli_input import cli_main
from .terminal_output.display import notification, display_panel, display_table
from .terminal_output.input import ask_credentials


class View:

    colors = {"Support": "green", "Commercial": "light_goldenrod2", "Customer": "dark_orange",
              "Contract": "yellow", "Event": "pink1", "Employee": "cyan", "ID": "bright_white"}

    @staticmethod
    def notification(status, message):
        notification(status, message)

    @staticmethod
    def ask_credentials():
        return ask_credentials()

    @staticmethod
    def read_user_input():
        return cli_main()

    @staticmethod
    def display_employees(data: list[dict] | dict, focus: list | None = None):
        colors = {"title": View.colors["Employee"], "Full name": View.colors["Employee"], **View.colors}
        if isinstance(data, list):
            display_table(title="Employees 👷 ", data=data, colors=colors)
        else:
            display_panel(title="Employee 👷 ", data=data, subtitle=data["Full name"], focus=focus, colors=colors)


    @staticmethod
    def display_customers(data: list[dict] | dict, focus: list | None = None):
        colors = {"title": View.colors["Customer"], "Full name": View.colors["Customer"], **View.colors}
        if isinstance(data, list):
            display_table(title="Customers 🏭 ", data=data, colors=colors)
        else:
            display_panel(title="Customer 🏭 ", data=data, subtitle=data["Full name"],
                          focus=focus, colors=colors)

    @staticmethod
    def display_contracts(data: list[dict] | dict, focus: list | None = None):
        colors = {"title": View.colors["Contract"], "UUID": View.colors["Contract"], **View.colors}
        if isinstance(data, list):
            display_table(title="Contracts 📃 ", data=data, colors=colors)
        else:
            display_panel(title="Contract 📃 ", data=data, subtitle=data["UUID"], focus=focus, colors=colors)

    @staticmethod
    def display_events(data: list[dict] | dict, focus: list | None = None):
        colors = {"title": View.colors["Event"], "Name": View.colors["Event"], **View.colors}
        if isinstance(data, list):
            display_table(title="Events 🎪 ", data=data, colors=colors)
        else:
            display_panel(title="Event 🎪 ", data=data, subtitle=data["Name"], focus=focus, colors=colors)

    def __init__(self):
        pass
