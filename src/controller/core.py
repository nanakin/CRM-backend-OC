from .manage.employees import EmployeesControllerMixin
from .manage.customers import CustomersControllerMixin
from .manage.common import requests_map


class Controller(EmployeesControllerMixin, CustomersControllerMixin):

    def _execute(self, request, param):
        requests_map.allowed[request](self, param)

    def read_and_execute_command(self):
        returned = self.view.read_user_input()
        request, param = returned if type(returned) is tuple else (returned, None)
        self._execute(request, param)

    def __init__(self, view, model):
        self.view = view
        self.model = model
