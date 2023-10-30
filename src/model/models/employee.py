from sqlalchemy import ForeignKey, String, Unicode
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy_utils import PasswordType
from sqlalchemy.exc import IntegrityError
import random
import string

from .common import Base, OperationFailed


class Employee(Base):
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
    role: Mapped["Role"] = relationship(lazy='subquery')

    def __str__(self):
        return self.fullname

    def __repr__(self) -> str:
        return f"Employee(id={self.id!r}, fullname={self.fullname!r}, role_id={self.role_id!r})"

    def valid_password(self, password):
        if self.password is None:
            return False
        return self.password == password

    def as_printable_dict(self):
        return {"ID": str(self.id), "Full name": self.fullname, "Username": self.username,
                "Role": str(self.role)}

    def as_printable_tuple(self):
        printable = self.as_printable_dict()
        return printable["ID"], printable["Full name"], printable["Username"], printable["Role"]


class EmployeeModelMixin:
    def get_employees(self, role_filter_value=None):
        with self.Session() as session:
            if role_filter_value:
                role_id = self.roles[role_filter_value.upper()].value
                result = session.query(Employee).filter_by(role_id=role_id).order_by(Employee.fullname)
            else:
                result = session.query(Employee).order_by(Employee.fullname)
            return [row.as_printable_tuple() for row in result]

    def add_employee(self, username, fullname):
        generated_password = "".join(random.choices(string.ascii_lowercase, k=12))
        employee = Employee(username=username, fullname=fullname, password=generated_password, role_id=self.roles.NONE.value)
        try:
            with self.Session() as session:
                session.add(employee)
                session.commit()
                return employee.as_printable_dict()
        except IntegrityError as e:
            raise OperationFailed(e)

    def delete_employee(self, username):
        employee = self._get_employee(username)
        with self.Session() as session:
            session.delete(employee)
            session.commit()

    def _get_employee(self, username=None, id=None, missing_ok=False):
        result = None
        with self.Session() as session:
            if username:
                result = session.query(Employee).filter_by(username=username).one_or_none()
            else:
                result = session.query(Employee).filter_by(id=id).one_or_none()
            session.commit()  # necessary ?
        if not missing_ok and result is None:
            raise OperationFailed(f"Cannot find the employee {username if username else id}")
        return result

    def valid_password(self, username, password):
        employee = self._get_employee(username=username, missing_ok=True)
        if employee:
            return employee.valid_password(password)
        else:
            return None

    def get_role(self, username):
        employee = self._get_employee(username=username)
        return self.roles(employee.role_id).name

    def set_role(self, username, role_name):
        valid_roles_names = [role.name for role in self.roles]
        if role_name.upper() not in valid_roles_names:
            raise OperationFailed(f"Invalid role, choose between: {' '.join(valid_roles_names)}.")
        role_id = self.roles[role_name.upper()].value
        employee = self._get_employee(username=username)
        with self.Session() as session:
            employee.role_id = role_id
            session.add(employee)
            session.commit()
            return employee.as_printable_dict()

    def set_password(self, username, password):
        employee = self._get_employee(username=username)
        with self.Session() as session:
            employee.password = password
            session.add(employee)
            session.commit()

    def update_employee_data(self, id, username, fullname):
        employee = self._get_employee(id=id)
        with self.Session() as session:
            if username:
                employee.username = username
            else:
                employee.fullname = fullname
            session.add(employee)
            session.commit()
            return employee.as_printable_dict()

    def detail_employee(self, username):
        employee = self._get_employee(username)
        return employee.as_printable_dict()
