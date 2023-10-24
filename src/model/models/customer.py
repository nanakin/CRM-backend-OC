from datetime import datetime
from sqlalchemy import DateTime, ForeignKey, Unicode
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func
from sqlalchemy_utils import EmailType, PhoneNumberType

from .common import Base


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
