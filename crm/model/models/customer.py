from datetime import datetime
from typing import Self, Optional

from sqlalchemy import DateTime, ForeignKey, Unicode
from sqlalchemy.orm import Mapped, Session, mapped_column, relationship
from sqlalchemy.sql import func
from sqlalchemy_utils import EmailType, PhoneNumberType

from .common import Base, OperationFailed


class Customer(Base):
    """Customer database model."""

    __tablename__ = "customer"

    id: Mapped[int] = mapped_column(primary_key=True)
    fullname: Mapped[str] = mapped_column(Unicode(255))
    email: Mapped[str] = mapped_column(EmailType)
    phone: Mapped[str] = mapped_column(PhoneNumberType)
    company: Mapped[Optional[str]] = mapped_column(Unicode(255))
    commercial_contact_id: Mapped[int] = mapped_column(ForeignKey("employee.id"))
    commercial_contact: Mapped["Employee"] = relationship(lazy="subquery")  # noqa: F821
    creation_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    last_modified: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    def __str__(self):
        return self.fullname

    def __repr__(self) -> str:
        return (
            f"Customer(id={self.id!r}, fullname={self.fullname!r}, company={self.company!r}, "
            f"commercial={self.commercial_contact_id!r}, email={self.email!r}, phone={self.phone!r}"
            f"creation_date={self.creation_date!r}, last_modified={self.last_modified!r})"
        )

    def as_dict(self, full: bool = True) -> dict:
        """Abstraction of customer database model object with a dictionary."""
        data = {
            "ID": str(self.id),
            "Full name": self.fullname,
            "Company": self.company,
            "Commercial": str(self.commercial_contact),
        }
        if full:
            data.update(
                {
                    "Email": str(self.email),
                    "Phone": str(self.phone),
                    "Creation date": str(datetime.date(self.creation_date)),
                    "Last modification": str(datetime.date(self.last_modified)),
                }
            )
        return data

    @classmethod
    def get(cls, session: Session, customer_id: int) -> Self:
        """Retrieve a customer from a given database session, raise an exception otherwise."""
        result = session.get(cls, customer_id)
        if result is None:
            raise OperationFailed(f"Cannot find the customer with id {customer_id}")
        return result
