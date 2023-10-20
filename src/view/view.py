from .cli_input import cli_main
from .terminal_output.display import info, warning
from .terminal_output.employees import display_employees, ask_credentials
from .requests import Request


class View:

    #Request = Request

    def info(self, message):
        info(message)

    def warning(self, message):
        warning(message)

    def ask_credentials(self):
        return ask_credentials()

    def read_user_input(self):
        return cli_main()

    def display_employees(self, data):
        display_employees(data)

    def __init__(self):
        #self.console = Console
        pass
