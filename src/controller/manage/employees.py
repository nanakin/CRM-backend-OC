from .common import requests_map, Request


class EmployeesControllerMixin:

    @requests_map.register(Request.LIST_EMPLOYEES)
    def list_employees(self):
        data = self.model.get_employees()
        print(data, "employee controller")
        self.view.display_employees(data)

    def get_employee(self):
        pass

    def new_employee(self):
        pass

    @requests_map.register(Request.EDIT_EMPLOYEE)
    def update_employee_data(self, id, fullname, username):
        print("employee controller edit", id)

    def set_role_employee(self):
        pass

    def set_password(self):
        pass

    def delete_employee(self):
        pass
