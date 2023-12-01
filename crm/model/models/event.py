from datetime import datetime
from typing import Optional, Self

from sqlalchemy import DateTime, ForeignKey, Integer, Unicode, UnicodeText
from sqlalchemy.orm import Mapped, Session, mapped_column, relationship
from sqlalchemy.types import Uuid

from .common import Base, OperationFailed


class Event(Base):
    """Event database model."""

    __tablename__ = "event"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(Unicode(255))
    contract_id: Mapped[Uuid] = mapped_column(ForeignKey("contract.id"))
    contract: Mapped["Contract"] = relationship(lazy="subquery")  # noqa: F821
    support_contact_id: Mapped[Optional[int]] = mapped_column(ForeignKey("employee.id"))
    support_contact: Mapped["Employee"] = relationship(lazy="subquery")  # noqa: F821
    start: Mapped[Optional[datetime]] = mapped_column(DateTime)
    end: Mapped[Optional[datetime]] = mapped_column(DateTime)
    attendees: Mapped[Optional[int]] = mapped_column(Integer)
    location: Mapped[Optional[str]] = mapped_column(UnicodeText)
    note: Mapped[Optional[str]] = mapped_column(UnicodeText)

    def __str__(self):
        return self.name.capitalize()

    def __repr__(self) -> str:
        return f"Event(id={self.id!r}, name={self.name!r}, contract_id={self.contract_id!r})"

    def as_dict(self, full: bool = True) -> dict:
        """Abstraction of event database model object with a dictionary."""
        customer = self.contract.customer
        commercial = self.contract.customer.commercial_contact
        support = self.support_contact
        data = {
            "ID": str(self.id),
            "Name": self.name,
            "Contract": str(self.contract),
            "Customer": str(customer),
            "Support": str(support) if support else "None",
            "Commercial": str(commercial) if commercial else "None",
            "Start": str(self.start),
        }
        if full:
            data.update(
                {
                    "End": str(self.end),
                    "Attendees": str(self.attendees),
                    "Location": str(self.location),
                    "Note": str(self.note),
                }
            )
        return data

    @classmethod
    def get(cls, session: Session, event_id: int) -> Self:
        """Retrieve an event from a given database session, raise an exception otherwise."""
        result = session.get(cls, event_id)
        if result is None:
            raise OperationFailed(f"Cannot find the event with id {event_id}")
        return result
