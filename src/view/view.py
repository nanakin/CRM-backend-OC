from .cli_input import cli_main
from .terminal_output.contracts import display_contract, display_contracts
from .terminal_output.customers import display_customer, display_customers
from .terminal_output.display import notification
from .terminal_output.employees import ask_credentials, display_employee, display_employees
from .terminal_output.events import display_event, display_events


class View:
    def notification(self, status, message):
        notification(status, message)

    def ask_credentials(self):
        return ask_credentials()

    def read_user_input(self):
        return cli_main()

    def display_employees(self, employees):
        display_employees(employees)

    def display_employee(self, employee, focus=None):
        display_employee(employee, focus)

    def display_customers(self, customers):
        display_customers(customers)

    def display_customer(self, customer, focus=None):
        display_customer(customer, focus)

    def display_contracts(self, contracts):
        display_contracts(contracts)

    def display_contract(self, contract, focus=None):
        display_contract(contract, focus)

    def display_events(self, events):
        display_events(events)

    def display_event(self, event, focus=None):
        display_event(event, focus)

    def __init__(self):
        pass
