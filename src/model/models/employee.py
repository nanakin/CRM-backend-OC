from sqlalchemy import ForeignKey, String, Unicode
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy_utils import PasswordType
from sqlalchemy.exc import IntegrityError

from .common import Base


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
            return session.query(Employee).all()

    def add_employee(self, username, fullname):
        employee = Employee(username=username, fullname=fullname, password="", role_id=self.roles.NONE.value)
        try:
            with self.Session() as session:
                session.add(employee)
                session.commit()
        except IntegrityError as e:
            return None
        return employee.as_printable_dict()

    def get_employee(self, username):
        with self.Session() as session:
            return session.query(Employee).filter_by(username=username).one_or_none()

    def valid_password(self, username, password):
        employee = self.get_employee(username)
        if not employee:
            return False
        return employee.valid_password(password)

    def get_role(self, username):
        employee = self.get_employee(username)
        if not employee:
            return False
        return self.roles(employee.role_id).name
