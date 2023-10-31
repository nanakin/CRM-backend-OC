from datetime import datetime
from uuid import uuid4

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from sqlalchemy.types import Uuid

from .common import Base, OperationFailed


class Contract(Base):
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

    def as_printable_dict(self):
        return {
            "UUID": str(self.id).upper(),
            "Customer": str(self.customer),
            "Signed": str(self.signed),
            "Total amount": str(self.total_amount) + " €",
            "Total due": str(self.total_amount - self.total_payed) + " €",
            "Creation date": str(self.creation_date),
        }

    def as_printable_tuple(self):
        printable = self.as_printable_dict()
        return printable["UUID"], printable["Customer"], printable["Signed"], printable["Total due"]


class ContractModelMixin:
    def verify_contract_authorization(self, connected_employee, contract):
        if connected_employee.role.name.upper() == self.roles.COMMERCIAL.name.upper():  # to change
            if contract.customer.commercial_contact != connected_employee:
                raise OperationFailed(
                    f"The employee {connected_employee.fullname} does not have the permission to edit "
                    f"{contract.customer.fullname} contracts (linked to "
                    f"{contract.customer.commercial_contact.fullname})"
                )

    def _get_contract(self, contract_uuid=None, missing_ok=False):
        result = None
        with self.Session() as session:
            result = session.query(Contract).filter_by(id=contract_uuid).one_or_none()
            session.commit()  # necessary ?
        if not missing_ok and result is None:
            raise OperationFailed(f"Cannot find the contract with uuid {contract_uuid}")
        return result

    def get_contracts(self, not_signed_filter, not_paid_filter):
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
            return [row.as_printable_tuple() for row in result]

    def detail_contract(self, contract_uuid):
        contract = self._get_contract(contract_uuid)
        return contract.as_printable_dict()

    def add_contract(self, customer_id, total_amount):
        with self.Session() as session:
            contract = Contract(customer_id=customer_id, total_amount=total_amount)
            session.add(contract)
            session.commit()
            return contract.as_printable_dict()

    def sign_contract(self, contract_uuid, authenticated_user):
        employee = self._get_employee(username=authenticated_user)  # store ID in controller self.authenticated_user ?
        contract = self._get_contract(contract_uuid)
        self.verify_contract_authorization(employee, contract)
        with self.Session() as session:
            contract.signed = True
            session.add(contract)
            session.commit()
            return contract.as_printable_dict()

    def update_contract(self, contract_uuid, customer_id, total_amount, authenticated_user):
        employee = self._get_employee(username=authenticated_user)  # store ID in controller self.authenticated_user ?
        contract = self._get_contract(contract_uuid)
        self.verify_contract_authorization(employee, contract)
        with self.Session() as session:
            if total_amount:
                contract.total_amount = total_amount
            if customer_id:
                contract.customer_id = customer_id
            session.add(contract)
            session.commit()
            return contract.as_printable_dict()

    def add_contract_payment(self, contract_uuid, paid_amount, authenticated_user):
        employee = self._get_employee(username=authenticated_user)  # store ID in controller self.authenticated_user ?
        contract = self._get_contract(contract_uuid)
        self.verify_contract_authorization(employee, contract)
        with self.Session() as session:
            contract.total_payed = contract.total_payed + paid_amount
            session.add(contract)
            session.commit()
            return contract.as_printable_dict()
