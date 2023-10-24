from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, ForeignKey, Integer, Unicode, UnicodeText
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.types import Uuid

from .common import Base


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
