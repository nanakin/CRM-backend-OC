from datetime import datetime
from typing import Optional
from uuid import uuid4

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Unicode, UnicodeText
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.sql import func
from sqlalchemy.types import Uuid
from sqlalchemy_utils import EmailType, PasswordType, PhoneNumberType


# declarative base class
class Base(DeclarativeBase):
    pass


class Role(Base):
    __tablename__ = "role"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(Unicode(127))
    # establish a bidirectional relationship in one-to-many (role-employees)
    # employees: Mapped[List["Employee"]] = relationship(back_populates="role")
    # addresses = db.relationship('Address', backref='person', lazy=True)

    def __repr__(self) -> str:
        return f"Role(id={self.id!r}, name={self.name!r})"


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
        return self.password == password

    def as_printable_tuple(self):
        return str(self.id), self.fullname, self.username


class Customer(Base):
    __tablename__ = "customer"

    id: Mapped[int] = mapped_column(primary_key=True)
    fullname: Mapped[str] = mapped_column(Unicode(255))
    email: Mapped[str] = mapped_column(EmailType)  # try type
    phone: Mapped[str] = mapped_column(PhoneNumberType)
    company: Mapped[str] = mapped_column(Unicode(255), nullable=True)
    commercial_contact_id: Mapped[int] = mapped_column(ForeignKey("employee.id"))
    creation_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    last_modified: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    def __repr__(self) -> str:
        return f"Customer(id={self.id!r}, fullname={self.fullname!r}, company={self.company!r})"


class Contract(Base):
    __tablename__ = "contract"

    id: Mapped[Uuid] = mapped_column(Uuid, primary_key=True, default=uuid4)
    customer_id: Mapped[int] = mapped_column(ForeignKey("customer.id"))
    signed: Mapped[bool] = mapped_column(Boolean, default=False)
    total_amount: Mapped[int] = mapped_column(Integer, default=0)
    amount_due: Mapped[int] = mapped_column(Integer, default=0)
    creation_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self) -> str:
        return f"Contract(id={self.id!r}, customer_id={self.customer_id!r}, signed={self.signed!r})"


class Event(Base):
    __tablename__ = "event"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(Unicode(255))
    contract_id: Mapped[Uuid] = mapped_column(ForeignKey("contract.id"))
    support_contact_id: Mapped[Optional[int]] = mapped_column(ForeignKey("employee.id"))  # to view ?
    start: Mapped[Optional[datetime]] = mapped_column(DateTime)
    end: Mapped[Optional[datetime]] = mapped_column(DateTime)
    attendees: Mapped[Optional[int]] = mapped_column(Integer)
    location: Mapped[Optional[str]] = mapped_column(UnicodeText)
    note: Mapped[Optional[str]] = mapped_column(UnicodeText)

    def __repr__(self) -> str:
        return f"Event(id={self.id!r}, name={self.name!r}, contract_id={self.contract_id!r})"
