from .common import Request, Roles, requests_map


class EmployeesControllerMixin:
    # -------------------- CRM Commands below --------------------------

    @requests_map.register(Request.LIST_EMPLOYEES, required_role=Roles.ALL)
    def list_employees(self, role_filter):
        displayable_employees = self.model.get_employees(role_filter)
        self.view.display_employees(displayable_employees)

    @requests_map.register(Request.DETAIL_EMPLOYEE, required_role=Roles.ALL)
    def get_employee(self, username):
        displayable_employee = self.model.detail_employee(username)
        self.view.display_employee(displayable_employee)

    @requests_map.register(Request.NEW_EMPLOYEE, required_role=Roles.ADMINISTRATOR)
    def new_employee(self, username, fullname):
        displayable_employee = self.model.add_employee(username, fullname)
        self.view.display_employee(displayable_employee, focus=displayable_employee.keys())

    @requests_map.register(Request.UPDATE_EMPLOYEE, required_role=Roles.ADMINISTRATOR)
    def update_employee_data(self, employee_id, username, fullname):
        displayable_employee = self.model.update_employee_data(employee_id, username, fullname)
        self.view.display_employee(
            displayable_employee, focus=("Username" if username else None, "Full name" if fullname else None)
        )

    @requests_map.register(Request.SET_EMPLOYEE_ROLE, required_role=Roles.ADMINISTRATOR)
    def set_role_employee(self, username, role_name):
        displayable_employee = self.model.set_role(username, role_name)
        self.view.display_employee(displayable_employee, focus=("Role",))

    @requests_map.register(Request.SET_EMPLOYEE_PASSWORD, required_role=Roles.ADMINISTRATOR)
    def set_password_employee(self, username, password):
        self.model.set_password(username, password)

    @requests_map.register(Request.DELETE_EMPLOYEE, required_role=Roles.ADMINISTRATOR)
    def delete_employee(self, username):
        self.model.delete_employee(username)
