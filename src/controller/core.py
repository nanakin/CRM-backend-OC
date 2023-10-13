from .manage.employees import EmployeesControllerMixin


class Controller(EmployeesControllerMixin):

    @classmethod
    def _get_allowed_actions(cls, self):
        allowed = {}
        for controller in cls.__mro__:
            if controller.__name__ not in (cls.__name__, "object"):  # to do : verify interface?
                allowed.update(controller.request_to_action(self))
        return allowed

    def _execute(self, request, param):
        self.allowed_actions[request](param)

    def read_and_execute_command(self):
        returned = self.view.read_user_input()
        request, param = returned if type(returned) is tuple else (returned, None)
        self._execute(request, param)

    def __init__(self, view, model):
        self.view = view
        self.model = model
        self.allowed_actions = Controller._get_allowed_actions(self)
