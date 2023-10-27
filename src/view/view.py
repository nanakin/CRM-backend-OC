from .cli_input import cli_main
from .terminal_output.display import notification
from .terminal_output.employees import ask_credentials, display_employees, display_employee
from .terminal_output.customers import display_customers, display_customer


class View:
    def notification(self, status, message):
        notification(status, message)

    def ask_credentials(self):
        return ask_credentials()

    def read_user_input(self):
        return cli_main()

    def display_employees(self, data):
        display_employees(data)

    def display_employee(self, employee, focus=None):
        display_employee(employee, focus)

    def display_customers(self, data):
        display_customers(data)

    def display_customer(self, employee, focus=None):
        display_customer(employee, focus)

    def __init__(self):
        pass
