from sqlalchemy import ForeignKey, String, Unicode
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy_utils import PasswordType
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
