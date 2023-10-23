from .cli_input import cli_main
from .terminal_output.display import notification
from .terminal_output.employees import display_employees, ask_credentials
from .requests import Request


class View:

    #Request = Request

    def notification(self, status, message):
        notification(status, message)

    def ask_credentials(self):
        return ask_credentials()

    def read_user_input(self):
        return cli_main()

    def display_employees(self, data):
        display_employees(data)

    def __init__(self):
        #self.console = Console
        pass
