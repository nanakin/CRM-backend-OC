from typing import Optional
from uuid import UUID

from sqlalchemy.orm import Session, sessionmaker

from crm.model.models import Contract, Employee, OperationFailed


class ContractModelMixin:
    """Model Mixin to manage contracts data."""

    Session: sessionmaker

    def verify_contract_authorization(
        self, session: Session, connected_employee_id: int, contract: Contract
    ) -> None:  # to-do : type session
        """Raises an exception if the employee doesn't have the authorization to edit the contract."""

        connected_employee = Employee.get(session, employee_id=connected_employee_id)
        if connected_employee.role.name.upper() == self.roles.COMMERCIAL.name.upper():  # to change
            if contract.customer.commercial_contact != connected_employee:
                raise OperationFailed(
                    f"The employee {connected_employee.fullname} does not have the permission to edit "
                    f"{contract.customer.fullname} contracts (linked to "
                    f"{contract.customer.commercial_contact.fullname})"
                )

    def get_contracts(self, not_signed_filter: bool = False, not_paid_filter: bool = False) -> list[dict]:
        """Retrieve contracts from database and return them as a list of dictionaries."""
        with self.Session() as session:
            if not not_paid_filter and not not_signed_filter:
                result = session.query(Contract)
            else:
                if not_signed_filter and not not_paid_filter:
                    result = session.query(Contract).filter(Contract.signed == False)  # noqa: E712
                elif not not_signed_filter and not_paid_filter:
                    result = session.query(Contract).filter(Contract.total_paid < Contract.total_amount)
                else:
                    result = session.query(Contract).filter(
                        Contract.signed == False, Contract.total_paid < Contract.total_amount  # noqa: E712
                    )
            return [row.as_dict(full=False) for row in result]

    def detail_contract(self, contract_uuid: UUID) -> dict:
        """Retrieve a given contract from database (and return it as dictionary)."""
        with self.Session() as session:
            contract = Contract.get(session, contract_uuid)
            return contract.as_dict()

    def add_contract(self, customer_id: int, total_amount: float) -> dict:  # to-do: deal with floating amounts
        """Add a new contract to database (and return it as dictionary)."""
        with self.Session() as session:
            contract = Contract(customer_id=customer_id)
            contract.update_total_amount(total_amount)
            session.add(contract)
            session.commit()
            return contract.as_dict()

    def sign_contract(self, contract_uuid: UUID, employee_id: int) -> dict:
        """Update contract signed status in database (and return the contract as dictionary)."""
        with self.Session() as session:
            contract = Contract.get(session, contract_uuid)
            self.verify_contract_authorization(session, employee_id, contract)
            contract.signed = True
            session.add(contract)
            session.commit()
            return contract.as_dict()

    def update_contract(
        self, contract_uuid: UUID, customer_id: Optional[int], total_amount: Optional[float], employee_id: int
    ) -> dict:
        """Update contract fields in database (and return the contract as dictionary)."""
        with self.Session() as session:
            contract = Contract.get(session, contract_uuid)
            self.verify_contract_authorization(session, employee_id, contract)
            if total_amount is not None:
                contract.update_total_amount(total_amount)
            if customer_id is not None:
                contract.customer_id = customer_id
            session.add(contract)
            session.commit()
            return contract.as_dict()

    def add_contract_payment(
        self, contract_uuid: UUID, paid_amount: float, employee_id: int
    ) -> dict:  # to-do: deal with floating amounts
        """Save a new contract payment into database (and return the contract as dictionary)."""
        with self.Session() as session:
            contract = Contract.get(session, contract_uuid)
            self.verify_contract_authorization(session, employee_id, contract)
            contract.add_payment(paid_amount)
            session.add(contract)
            session.commit()
            return contract.as_dict()
