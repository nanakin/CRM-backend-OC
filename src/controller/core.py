from .manage.employees import EmployeesController


class Controller(EmployeesController):

    def _execute(self, request):
        print(request, ">>")
        self.list_employees()

    def read_and_execute_command(self):
        request = self.view.read_user_input()
        self._execute(request)

    def __init__(self, view, model):
        self.view = view
        self.model = model
