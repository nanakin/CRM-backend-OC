from .cli_input import cli_main
from .terminal_output.display import notification
from .terminal_output.employees import ask_credentials, display_employees, display_employee
from .terminal_output.customers import display_customers, display_customer
from .terminal_output.contracts import display_contracts, display_contract


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

    def __init__(self):
        pass
