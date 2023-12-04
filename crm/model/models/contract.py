from datetime import datetime
from typing import Self
from uuid import UUID, uuid4

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer
from sqlalchemy.orm import Mapped, Session, mapped_column, relationship
from sqlalchemy.sql import func
from sqlalchemy.types import Uuid

from .common import Base, OperationFailed


class Contract(Base):
    """Contract database model."""

    __tablename__ = "contract"

    id: Mapped[Uuid] = mapped_column(Uuid, primary_key=True, default=uuid4)
    customer_id: Mapped[int] = mapped_column(ForeignKey("customer.id"))
    customer: Mapped["Customer"] = relationship(lazy="subquery")  # noqa: F821
    signed: Mapped[bool] = mapped_column(Boolean, default=False)
    total_amount: Mapped[int] = mapped_column(Integer, default=0)
    total_paid: Mapped[int] = mapped_column(Integer, default=0)
    creation_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    def __str__(self):
        return str(self.id).upper()

    def __repr__(self) -> str:
        return (
            f"Contract(id={self.id!r}, customer_id={self.customer_id!r}, signed={self.signed!r}), "
            f"total_amount={self.total_amount!r})"
        )

    def as_dict(self, full: bool = True) -> dict:  # to-do: deal with floating amounts
        """Abstraction of the contract database model object with a dictionary."""
        commercial = self.customer.commercial_contact
        data = {
            "UUID": str(self.id).upper(),
            "Company": str(self.customer.company),
            "Customer": str(self.customer),
            "Commercial": str(commercial),
            "Signed": str(self.signed),
            "Total due": f"{((self.total_amount - self.total_paid) / 100):.2f} €",
        }
        if full:
            data.update(
                {"Total amount": f"{(self.total_amount / 100):.2f}  €",
                 "Creation date": str(datetime.date(self.creation_date))}
            )
        return data

    def update_total_amount(self, total_amount: float) -> None:
        """Update the total paid amount of the contract."""
        self.total_amount = int(total_amount * 100)

    def add_payment(self, payed: float) -> None:
        """Update the total paid amount of the contract."""
        self.total_paid += int(payed * 100)

    @classmethod
    def get(cls, session: Session, contract_uuid: UUID) -> Self:
        """Retrieve a contract from a given database session, raise an exception otherwise."""
        result = session.get(cls, contract_uuid)
        if result is None:
            raise OperationFailed(f"Cannot find the contract with uuid {str(contract_uuid).upper()}")
        return result
