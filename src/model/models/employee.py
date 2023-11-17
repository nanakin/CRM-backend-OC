from typing import Optional, Self
from sqlalchemy import ForeignKey, String, Unicode
from sqlalchemy.orm import Mapped, mapped_column, relationship, Session
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

    @classmethod
    def get(cls, session: Session, username: Optional[str] = None, employee_id: Optional[int] = None) -> Self:
        """Retrieve an employee from a given database session, raise an exception otherwise."""
        if username:
            result = session.query(cls).filter_by(username=username).one_or_none()
        else:
            result = session.get(cls, employee_id)
        if result is None:
            raise OperationFailed(f"Cannot find the employee {username if username else employee_id}")
        return result
