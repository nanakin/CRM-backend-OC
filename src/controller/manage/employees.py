from .common import LogStatus, Request, Roles, requests_map, require_authentication


class EmployeesControllerMixin:
    # -------------------- CRM Commands below --------------------------

    @requests_map.register(Request.LIST_EMPLOYEES)
    @require_authentication()
    def list_employees(self):
        data = self.model.get_employees()
        self.view.display_employees(data)

    def get_employee(self):
        pass

    @requests_map.register(Request.NEW_EMPLOYEES)
    @require_authentication(Roles.ADMINISTRATOR)
    def new_employee(self, username, fullname):
        employee = self.model.add_employee(username, fullname)
        if employee is not None:
            self.view.display_employee(employee)
            return LogStatus.INFO, "Employee successfully created"

    @requests_map.register(Request.EDIT_EMPLOYEE)
    def update_employee_data(self, id, fullname, username):
        print("employee controller edit", id)

    def set_role_employee(self):
        pass

    def set_password(self):
        pass

    def delete_employee(self):
        pass
