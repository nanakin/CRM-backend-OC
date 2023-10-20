from .manage import EmployeesControllerMixin, CustomersControllerMixin, AuthenticationControllerMixin, requests_map


class Controller(EmployeesControllerMixin, CustomersControllerMixin, AuthenticationControllerMixin):

    def _execute(self, request, args):
        to_execute = requests_map.allowed[request]
        method_arguments = self, *args
        to_execute(*method_arguments)

    def read_and_execute_command(self):
        request, parameters = self.view.read_user_input()
        self._execute(request, parameters)

    def __init__(self, view, model):
        self.view = view
        self.model = model
        self.authenticated_user = None
