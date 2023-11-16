import random
import string

from typing import Optional
from sqlalchemy import ForeignKey, String, Unicode
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Mapped, mapped_column, relationship, sessionmaker
from sqlalchemy_utils import PasswordType

from .common import Base, OperationFailed


class Employee(Base):
    """Employee database model."""
    __tablename__ = "employee"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(30), unique=True)
    fullname: Mapped[str] = mapped_column(Unicode(255))
    password: Mapped[int] = mapped_column(
        PasswordType(
            schemes=[
                "pbkdf2_sha512",
            ]
        )
    )
    role_id: Mapped[int] = mapped_column(ForeignKey("role.id"))
    role: Mapped["Role"] = relationship(lazy="subquery")  # noqa: F821

    def __str__(self):
        return self.fullname

    def __repr__(self) -> str:
        return f"Employee(id={self.id!r}, fullname={self.fullname!r}, role_id={self.role_id!r})"

    def valid_password(self, password: str) -> bool:
        """Return True if the password is valid, False otherwise."""
        if self.password is None:
            return False
        return self.password == password

    def as_dict(self) -> dict:
        """Abstraction of employee database model object with a dictionary."""
        return {"ID": str(self.id), "Full name": self.fullname, "Username": self.username, "Role": str(self.role)}


class EmployeeModelMixin:
    """Model Mixin to manage employees data."""

    Session: sessionmaker

    def get_employee(self, username: Optional[str] = None, employee_id: Optional[int] = None) -> Employee:
        """
        Retrieve an employee from the database.

        Model usage only."""
        with self.Session() as session:
            if username:
                result = session.query(Employee).filter_by(username=username).one_or_none()
            else:
                result = session.query(Employee).filter_by(id=employee_id).one_or_none()
            session.commit()  # necessary ?
            if result is None:
                raise OperationFailed(f"Cannot find the employee {username if username else employee_id}")
            return result

    def get_employees(self, role_filter_value=None) -> list[dict]:
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
        generated_password = "".join(random.choices(string.ascii_lowercase, k=12))
        employee = Employee(
            username=username, fullname=fullname, password=generated_password, role_id=self.roles.NONE.value
        )
        try:
            with self.Session() as session:
                session.add(employee)
                session.commit()
                return employee.as_dict()
        except IntegrityError as e:
            raise OperationFailed(e)

    def delete_employee(self, username) -> None:
        """Delete an employee from the database."""
        employee = self.get_employee(username)
        with self.Session() as session:
            session.delete(employee)
            session.commit()

    def valid_password(self, username: str, password: str) -> bool:
        """Return True if the password is valid, False otherwise."""
        try:
            employee = self.get_employee(username=username)
        except OperationFailed:
            return False
        return employee.valid_password(password)

    def get_role(self, username: str) -> str:
        """Return the role of the employee as string."""
        employee = self.get_employee(username=username)
        return self.roles(employee.role_id).name

    def set_role(self, username: str, role_name: str) -> dict:
        """Update the role of an employee in database (and return the employee as dictionary)."""
        valid_roles_names = [role.name for role in self.roles]
        if role_name.upper() not in valid_roles_names:
            raise OperationFailed(f"Invalid role, choose between: {' '.join(valid_roles_names)}.")
        role_id = self.roles[role_name.upper()].value  # temp
        employee = self.get_employee(username=username)
        with self.Session() as session:
            employee.role_id = role_id
            session.add(employee)
            session.commit()
            return employee.as_dict()

    def set_password(self, username: str, password: str) -> None:
        """Update the employee password in database (and return the employee as dictionary)."""
        employee = self.get_employee(username=username)
        with self.Session() as session:
            employee.password = password
            session.add(employee)
            session.commit()

    def update_employee_data(self, employee_id: Optional[int], username: Optional[str], fullname: str) -> dict:
        """Update employee fields in database (and return the employee as dictionary)."""
        employee = self.get_employee(employee_id=employee_id)
        with self.Session() as session:
            if username:
                employee.username = username
            else:
                employee.fullname = fullname
            session.add(employee)
            session.commit()
            return employee.as_dict()

    def detail_employee(self, username: str) -> dict:
        """Retrieve an employee from database (and return it as dictionary)."""
        employee = self.get_employee(username)
        return employee.as_dict()
