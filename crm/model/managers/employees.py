import random
import string
from typing import Optional

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import sessionmaker

from crm.model.models import Employee, Role, OperationFailed


class EmployeeModelMixin:
    """Model Mixin to manage employees data."""

    Session: sessionmaker

    def get_employees(self, role_filter_value=None) -> list[dict]:  # to-do type role_filter_value
        """Retrieve employees from the database (and return them as list of dictionaries).

        Applying an optional filter on the role.
        """
        with self.Session() as session:
            if role_filter_value:
                role_id = self.roles[role_filter_value.upper()].value
                result = session.query(Employee).filter_by(role_id=role_id).order_by(Employee.fullname)
            else:
                result = session.query(Employee).order_by(Employee.fullname)
            return [row.as_dict() for row in result]

    def add_employee(self, username: str, fullname: str) -> dict:
        """Add an employee to the database (with a generated password) and return it as dictionary."""
        try:
            with self.Session() as session:
                generated_password = "".join(random.choices(string.ascii_lowercase, k=12))
                employee = Employee(
                    username=username, fullname=fullname, password=generated_password, role_id=self.roles.NONE.value
                )
                session.add(employee)
                session.commit()
                return employee.as_dict()
        except IntegrityError as e:
            raise OperationFailed(e)

    def delete_employee(self, username: str) -> None:
        """Delete an employee from the database."""
        with self.Session() as session:
            employee = Employee.get(session, username=username)
            session.delete(employee)
            session.commit()

    def valid_password(self, username: str, password: str) -> bool:
        """Return True if the password is valid, False otherwise."""
        with self.Session() as session:
            try:
                employee = Employee.get(session, username=username)
            except OperationFailed:
                return False
            return employee.valid_password(password)

    def get_role(self, username: str) -> str:
        """Return the role of the employee as string."""
        with self.Session() as session:
            employee = Employee.get(session, username=username)
            return self.roles(employee.role_id).name

    def set_role(self, username: str, role_name: str) -> dict:
        """Update the role of an employee in database (and return the employee as dictionary)."""
        valid_roles_names = [role.name for role in self.roles]
        if role_name.upper() not in valid_roles_names:
            raise OperationFailed(f"Invalid role, choose between: {' '.join(valid_roles_names)}.")
        role_id = self.roles[role_name.upper()].value  # temp
        with self.Session() as session:
            employee = Employee.get(session, username=username)
            role = session.get(Role, role_id)
            employee.role = role
            session.add(employee)
            session.commit()
            return employee.as_dict()

    def set_password(self, username: str, password: str) -> None:
        """Update the employee password in database (and return the employee as dictionary)."""
        with self.Session() as session:
            employee = Employee.get(session, username=username)
            employee.password = password
            session.add(employee)
            session.commit()

    def update_employee_data(self, employee_id: Optional[int], username: Optional[str], fullname: str) -> dict:
        """Update employee fields in database (and return the employee as dictionary)."""
        with self.Session() as session:
            employee = Employee.get(session, employee_id=employee_id)
            if username is not None:
                employee.username = username
            if fullname is not None:
                employee.fullname = fullname
            session.add(employee)
            session.commit()
            return employee.as_dict()

    def detail_employee(self, username: str) -> dict:
        """Retrieve an employee from database (and return it as dictionary)."""
        with self.Session() as session:
            employee = Employee.get(session, username=username)
            return employee.as_dict()
