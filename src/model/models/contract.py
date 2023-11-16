from datetime import datetime
from uuid import uuid4, UUID
from typing import Optional

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship, sessionmaker
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


class ContractModelMixin:
    """Model Mixin to manage contracts data."""

    Session: sessionmaker
    #roles:

    def get_contract(self, contract_uuid: UUID) -> Contract:
        """Retrieve a contract from database (raises an exception or return None if missing).

        Model usage only."""
        with self.Session() as session:
            result = session.query(Contract).filter_by(id=contract_uuid).one_or_none()
            session.commit()  # necessary ?
            if result is None:
                raise OperationFailed(f"Cannot find the contract with uuid {contract_uuid}")
            return result

    def verify_contract_authorization(self, connected_employee_id: int, contract: Contract) -> None:
        """Raises an exception if the employee doesn't have the authorization to edit the contract."""
        connected_employee = self.get_employee(employee_id=connected_employee_id)
        if connected_employee.role.name.upper() == self.roles.COMMERCIAL.name.upper():  # to change
            if contract.customer.commercial_contact != connected_employee:
                raise OperationFailed(
                    f"The employee {connected_employee.fullname} does not have the permission to edit "
                    f"{contract.customer.fullname} contracts (linked to "
                    f"{contract.customer.commercial_contact.fullname})"
                )

    def get_contracts(self, not_signed_filter: bool, not_paid_filter: bool) -> list[dict]:
        """Retrieve contracts from database and return them as a list of dictionaries."""
        with self.Session() as session:
            if not not_paid_filter and not not_signed_filter:
                result = session.query(Contract)
            else:
                if not_signed_filter and not not_paid_filter:
                    result = session.query(Contract).filter(Contract.signed == False)  # noqa: E712
                elif not not_signed_filter and not_paid_filter:
                    result = session.query(Contract).filter(Contract.total_payed < Contract.total_amount)
                else:
                    result = session.query(Contract).filter(
                        Contract.signed == False, Contract.total_payed < Contract.total_amount  # noqa: E712
                    )
            return [row.as_dict(full=False) for row in result]

    def detail_contract(self, contract_uuid: UUID) -> dict:
        """Retrieve a given contract from database (and return it as dictionary)."""
        contract = self.get_contract(contract_uuid)
        return contract.as_dict()

    def add_contract(self, customer_id: int, total_amount: float) -> dict:  # to-do: deal with floating amounts
        """Add a new contract to database (and return it as dictionary)."""
        with self.Session() as session:
            contract = Contract(customer_id=customer_id, total_amount=total_amount)
            session.add(contract)
            session.commit()
            return contract.as_dict()

    def sign_contract(self, contract_uuid: UUID, employee_id: int) -> dict:
        """Update contract signed status in database (and return the contract as dictionary)."""
        contract = self.get_contract(contract_uuid)
        self.verify_contract_authorization(employee_id, contract)
        with self.Session() as session:
            contract.signed = True
            session.add(contract)
            session.commit()
            return contract.as_dict()

    def update_contract(self, contract_uuid: UUID, customer_id: Optional[int], total_amount: Optional[float], employee_id: int) -> dict:
        """Update contract fields in database (and return the contract as dictionary)."""
        contract = self.get_contract(contract_uuid)
        self.verify_contract_authorization(employee_id, contract)
        with self.Session() as session:
            if total_amount:
                contract.total_amount = total_amount
            if customer_id:
                contract.customer_id = customer_id
            session.add(contract)
            session.commit()
            return contract.as_dict()

    def add_contract_payment(self, contract_uuid: UUID, paid_amount: float, employee_id: int) -> dict:   # to-do: deal with floating amounts
        """Save a new contract payment into database (and return the contract as dictionary)."""
        contract = self.get_contract(contract_uuid)
        self.verify_contract_authorization(employee_id, contract)
        with self.Session() as session:
            contract.total_payed = contract.total_payed + paid_amount
            session.add(contract)
            session.commit()
            return contract.as_dict()
