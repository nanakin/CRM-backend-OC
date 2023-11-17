from datetime import datetime
from uuid import uuid4, UUID
from typing import Self

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship, Session
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
    total_payed: Mapped[int] = mapped_column(Integer, default=0)
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
            "Customer": str(self.customer),
            "Commercial": str(commercial),
            "Signed": str(self.signed),
            "Total due": str(self.total_amount - self.total_payed) + " €"}
        if full:
            data.update({
                "Total amount": str(self.total_amount) + " €",
                "Creation date": str(self.creation_date)})
        return data

    @classmethod
    def get(cls, session: Session, contract_uuid: UUID) -> Self:
        """Retrieve a contract from a given database session, raise an exception otherwise."""
        result = session.get(cls, contract_uuid)
        if result is None:
            raise OperationFailed(f"Cannot find the contract with uuid {contract_uuid}")
        return result
