from datetime import datetime
from typing import Optional
from uuid import UUID
from sqlalchemy import DateTime, ForeignKey, Integer, Unicode, UnicodeText
from sqlalchemy.orm import Mapped, mapped_column, relationship, sessionmaker
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
            "Name": self.name.capitalize(),
            "Contract": str(self.contract),
            "Customer": str(customer),
            "Support": str(support) if support else "None",
            "Commercial": str(commercial) if commercial else "None",
            "Start": str(self.start)}
        if full:
            data.update({
                "End": str(self.end),
                "Attendees": str(self.attendees),
                "Location": str(self.location),
                "Note": str(self.note)})
        return data


class EventModelMixin:
    """Model Mixin to manage events data."""

    Session: sessionmaker

    def get_event(self, event_id: int) -> Event:
        """Retrieve an event from the database.

        Model usage only."""
        with self.Session() as session:
            result = session.query(Event).filter_by(id=event_id).one_or_none()
            session.commit()  # necessary ?
            if result is None:
                raise OperationFailed(f"Cannot find the event with id {event_id}")
            return result

    def get_events(self, not_signed_filter: bool, not_paid_filter: bool) -> list[dict]:
        """Retrieve events from the database and return them as a list of dictionaries."""
        with self.Session() as session:
            if not not_paid_filter and not not_signed_filter:
                result = session.query(Event)
            else:
                result = session.query(Event).filter()
            return [row.as_dict(full=False) for row in result]

    def detail_event(self, event_id: int) -> dict:
        """Retrieve a given event from the database and return it as a dictionary."""
        event = self.get_event(event_id)
        return event.as_dict()

    def add_event(self, contract_uuid: UUID, name: str, employee_id: int) -> dict:
        """Add a new event to the database (and return it as a dictionary)."""
        connected_employee = self.get_employee(id=employee_id)  # to fix : this mixin depends on other mixins
        contract = self.get_contract(contract_uuid)   # to fix : this mixin depends on other mixins
        if not contract.signed:
            raise OperationFailed(f"Impossible to create an event for the unsigned contrat {contract_uuid}.")
        if contract.customer.commercial_contact != connected_employee:
            raise OperationFailed(
                f"The employee {connected_employee} does not have the permission to add events to {contract.customer} "
                f"contracts (linked to {contract.customer.commercial_contact})."
            )
        with self.Session() as session:
            event = Event(contract_id=contract_uuid, name=name)
            session.add(event)
            session.commit()
            return event.as_dict()

    def set_event_support(self, event_id: int, support_username: str) -> dict:
        """Update the support associated to the event in database (and return the event as a dictionary)."""
        support = self.get_employee(username=support_username)
        if support.role.name.upper() != self.roles.SUPPORT.name.upper():  # temp
            raise OperationFailed(
                f"The employee {support} assigned to support the event is not a support ({support.role})."
            )
        event = self.get_event(event_id)
        with self.Session() as session:
            support = session.merge(support)
            event = session.merge(event)
            event.support_contact = support
            session.add(event)
            session.commit()
            return event.as_dict()

    def update_event(self, event_id: int, name: Optional[str], start: Optional[datetime], end: Optional[datetime], attendees: Optional[int], location: Optional[str], note: Optional[str], employee_id: int) -> dict:
        """Update event fields in database (and return the event as a dictionary)."""
        connected_employee = self.get_employee(id=employee_id)
        event = self.get_event(event_id)
        if event.support_contact_id != connected_employee.id:
            raise OperationFailed(
                f'The employee {connected_employee} does not have the permission manage the event "{event}" (linked '
                f"to {event.support_contact})."
            )
        with self.Session() as session:
            if name:
                event.name = name
            if start:
                event.start = start
            if end:
                event.end = end
            if attendees:
                event.attendees = attendees
            if location:
                event.location = location
            if note:
                event.note = note
            session.add(event)
            session.commit()
            return event.as_dict()
