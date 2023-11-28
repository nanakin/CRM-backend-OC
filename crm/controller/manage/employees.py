from typing import TYPE_CHECKING

from .common import Request, Roles, requests_map

if TYPE_CHECKING:
    from crm.model import Model
    from crm.view import View


class EmployeesControllerMixin:
    view: "View"
    model: "Model"

    # -------------------- CRM Commands below --------------------------

    @requests_map.register(Request.LIST_EMPLOYEES, required_role=Roles.ALL)
    def list_employees(self, role_filter: str) -> None:
        """Retrieve employees from database and display them."""
        displayable_employees = self.model.get_employees(role_filter)
        self.view.display_employees(displayable_employees)

    @requests_map.register(Request.DETAIL_EMPLOYEE, required_role=Roles.ALL)
    def get_employee(self, username: str) -> None:
        """Retrieve a given employee from database and display it."""
        displayable_employee = self.model.detail_employee(username)
        self.view.display_employee(displayable_employee)

    @requests_map.register(Request.NEW_EMPLOYEE, required_role=Roles.ADMINISTRATOR)
    def new_employee(self, username: str, fullname: str) -> None:
        """Add a new employee to database and display it."""
        displayable_employee = self.model.add_employee(username, fullname)
        self.view.display_employee(displayable_employee, focus=displayable_employee.keys())

    @requests_map.register(Request.UPDATE_EMPLOYEE, required_role=Roles.ADMINISTRATOR)
    def update_employee_data(self, employee_id: int, username: str, fullname: str) -> None:
        """Update employee fields in database and display the employee."""
        displayable_employee = self.model.update_employee_data(employee_id, username, fullname)
        fields_name = {"Username": username, "Full name": fullname}
        self.view.display_employee(
            displayable_employee, focus=[name for name, new_value in fields_name.items() if new_value is not None]
        )

    @requests_map.register(Request.SET_EMPLOYEE_ROLE, required_role=Roles.ADMINISTRATOR)
    def set_role_employee(self, username: str, role_name: str) -> None:
        """Update the role associated to a given employee in database and display the employee."""
        displayable_employee = self.model.set_role(username, role_name)
        self.view.display_employee(displayable_employee, focus=["Role"])

    @requests_map.register(Request.SET_EMPLOYEE_PASSWORD, required_role=Roles.ADMINISTRATOR)
    def set_password_employee(self, username: str, password: str) -> None:
        """Update the employee password in database."""
        self.model.set_password(username, password)

    @requests_map.register(Request.DELETE_EMPLOYEE, required_role=Roles.ADMINISTRATOR)
    def delete_employee(self, username: str) -> None:
        """Delete an employee from database."""
        self.model.delete_employee(username)
