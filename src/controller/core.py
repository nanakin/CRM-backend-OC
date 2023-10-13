from .manage.employees import EmployeesController


class Controller(EmployeesController):

    def _execute(self, request, param):
        self.list_employees()

    def read_and_execute_command(self):
        returned = self.view.read_user_input()
        request, param = returned if returned is tuple else returned, None
        self._execute(request, param)

    def __init__(self, view, model):
        self.view = view
        self.model = model
