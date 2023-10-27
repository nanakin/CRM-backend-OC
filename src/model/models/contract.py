from datetime import datetime
from uuid import uuid4

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.sql import func
from sqlalchemy.types import Uuid

from .common import Base, OperationFailed


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
