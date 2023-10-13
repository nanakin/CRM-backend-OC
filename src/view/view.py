from .cli_input import cli_main
from .terminal_output.employees import display_employees
from .requests import Request


class View:

    Request = Request

    def read_user_input(self):
        return cli_main()

    def display_employees(self, data):
        display_employees(data)

    def __init__(self):
        #self.console = Console
        pass
