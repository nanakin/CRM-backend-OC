from sqlalchemy import ForeignKey, String, Unicode
from sqlalchemy.orm import Mapped, mapped_column
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
    # establish a bidirectional relationship in one-to-many (role-employees)
    # role: Mapped["Role"] = relationship(back_populates="employees")

    def __repr__(self) -> str:
        return f"Employee(id={self.id!r}, fullname={self.fullname!r}, role_id={self.role_id!r})"

    def valid_password(self, password):
        if self.password is None:
            return False
        return self.password == password

    def as_printable_dict(self):
        return {"id": str(self.id), "Full name": self.fullname, "Username": self.username,
                "Role": str(self.role_id)}

    def as_printable_tuple(self):
        return str(self.id), self.fullname, self.username, str(self.role_id)


class EmployeeModelMixin:
    def get_employees(self):
        with self.Session() as session:
            result = session.query(Employee).all()
        return result

    def add_employee(self, username, fullname):
        generated_password = "".join(random.choices(string.ascii_lowercase, k=12))
        employee = Employee(username=username, fullname=fullname, password=generated_password, role_id=self.roles.NONE.value)
        try:
            with self.Session() as session:
                session.add(employee)
                session.commit()
        except IntegrityError as e:
            raise OperationFailed(e)
        return employee.as_printable_dict()

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

    def detail_employee(self, username):
        employee = self._get_employee(username)
        return employee.as_printable_dict()
