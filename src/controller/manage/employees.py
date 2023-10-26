from .common import LogStatus, Request, Roles, requests_map


class EmployeesControllerMixin:
    # -------------------- CRM Commands below --------------------------

    @requests_map.register(Request.LIST_EMPLOYEES, required_role=Roles.ALL)
    def list_employees(self):
        data = self.model.get_employees()
        self.view.display_employees(data)

    @requests_map.register(Request.DETAIL_EMPLOYEE, required_role=Roles.ALL)
    def get_employee(self, username):
        employee = self.model.detail_employee(username)
        if employee:
            self.view.display_employee(employee)

    @requests_map.register(Request.NEW_EMPLOYEE, required_role=Roles.ADMINISTRATOR)
    def new_employee(self, username, fullname):
        employee = self.model.add_employee(username, fullname)
        if employee:
            self.view.display_employee(employee)

    @requests_map.register(Request.EDIT_EMPLOYEE, required_role=Roles.ADMINISTRATOR)
    def update_employee_data(self, id, username, fullname):
        self.model.update_employee_data(id, username, fullname)

    @requests_map.register(Request.SET_EMPLOYEE_ROLE, required_role=Roles.ADMINISTRATOR)
    def set_role_employee(self, username, role_name):
        self.model.set_role(username, role_name)

    @requests_map.register(Request.SET_EMPLOYEE_PASSWORD, required_role=Roles.ADMINISTRATOR)
    def set_password_employee(self, username, password):
        self.model.set_password(username, password)

    @requests_map.register(Request.DELETE_EMPLOYEE, required_role=Roles.ADMINISTRATOR)
    def delete_employee(self, username):
        self.model.delete_employee(username)
