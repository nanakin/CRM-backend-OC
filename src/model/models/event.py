from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, ForeignKey, Integer, Unicode, UnicodeText
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import Uuid

from .common import Base, OperationFailed


class Event(Base):
    __tablename__ = "event"
    entity_name = __tablename__

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

    def as_printable_dict(self, full=True):
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
    def verify_event_authorization(self, connected_employee, contract):
        if connected_employee.role.name.upper() == self.roles.COMMERCIAL.name.upper():  # to change
            if contract.customer.commercial_contact.id != connected_employee.id:
                raise OperationFailed(
                    f"The employee {connected_employee.fullname} does not have the permission to edit "
                    f"{contract.customer.fullname} contracts (linked to "
                    f"{contract.customer.commercial_contact.fullname})"
                )

    def _get_event(self, event_id=None, missing_ok=False):
        result = None
        with self.Session() as session:
            result = session.query(Event).filter_by(id=event_id).one_or_none()
            session.commit()  # necessary ?
        if not missing_ok and result is None:
            raise OperationFailed(f"Cannot find the event with id {event_id}")
        return result

    def get_events(self, not_signed_filter, not_paid_filter):
        with self.Session() as session:
            if not not_paid_filter and not not_signed_filter:
                result = session.query(Event)
            else:
                result = session.query(Event).filter()
            return [row.as_printable_dict(full=False) for row in result]

    def detail_event(self, event_id):
        event = self._get_event(event_id)
        return event.as_printable_dict()

    def add_event(self, contract_uuid, name, employee_id):
        connected_employee = self.get_employee(id=employee_id)
        contract = self._get_contract(contract_uuid)
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
            return event.as_printable_dict()

    def set_event_support(self, event_id, support_username):
        support = self.get_employee(username=support_username)
        if support.role.name.upper() != self.roles.SUPPORT.name.upper():  # temp
            raise OperationFailed(
                f"The employee {support} assigned to support the event is not a support ({support.role})."
            )
        event = self._get_event(event_id)
        with self.Session() as session:
            support = session.merge(support)
            event = session.merge(event)
            event.support_contact = support
            session.add(event)
            session.commit()
            return event.as_printable_dict()

    def update_event(self, event_id, name, start, end, attendees, location, note, employee_id):
        connected_employee = self.get_employee(id=employee_id)
        event = self._get_event(event_id)
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
            return event.as_printable_dict()
