from typing import TYPE_CHECKING
from uuid import UUID

from .common import Request, Roles, requests_map

if TYPE_CHECKING:
    from crm.model import Model
    from crm.view import View

    from .common import Auth


class ContractsControllerMixin:
    view: "View"
    model: "Model"
    auth: "Auth"

    # -------------------- CRM Commands below --------------------------

    @requests_map.register(Request.LIST_CONTRACTS, required_role=Roles.ALL)
    def list_contracts(self, not_signed_filter: bool, not_paid_filter: bool) -> None:
        """Retrieve contracts from database and display them."""
        displayable_contracts = self.model.get_contracts(not_signed_filter, not_paid_filter)
        self.view.display_contracts(displayable_contracts)

    @requests_map.register(Request.DETAIL_CONTRACT, required_role=Roles.ALL)
    def get_contract(self, contract_uuid: UUID) -> None:
        """Retrieve a given contract from database and display it."""
        displayable_contract = self.model.detail_contract(contract_uuid)
        self.view.display_contract(displayable_contract)

    @requests_map.register(Request.NEW_CONTRACT, required_role=Roles.ADMINISTRATOR)
    def new_contract(self, customer_id: int, total_amount: float) -> None:
        """Add a new contract to database and display it."""
        displayable_contract = self.model.add_contract(customer_id, total_amount)
        self.view.display_contract(displayable_contract, focus=displayable_contract.keys())

    @requests_map.register(Request.ADD_CONTRACT_PAYMENT, required_role=Roles.ADMINISTRATOR | Roles.COMMERCIAL)
    def add_contract_payment(self, contract_uuid: UUID, payment: float) -> None:
        """Save a new contract payment to database and display it."""
        displayable_contract = self.model.add_contract_payment(contract_uuid, payment, self.auth.user_id)
        self.view.display_contract(displayable_contract, focus=["Total due"])

    @requests_map.register(Request.UPDATE_CONTRACT, required_role=Roles.ADMINISTRATOR | Roles.COMMERCIAL)
    def update_contract(self, contract_uuid: UUID, customer_id: int, total_amount: float) -> None:
        """Update contract fields in database and display the contract."""
        displayable_contract = self.model.update_contract(contract_uuid, customer_id, total_amount, self.auth.user_id)
        fields_name = {"Total_amount": total_amount, "Customer": customer_id}
        self.view.display_contract(
            displayable_contract, focus=[name for name, new_value in fields_name.items() if new_value is not None]
        )

    @requests_map.register(Request.SIGN_CONTRACT, required_role=Roles.ADMINISTRATOR | Roles.COMMERCIAL)
    def sign_contract(self, contract_uuid: UUID) -> None:
        """Update contract signed status in database and display it."""
        displayable_contract = self.model.sign_contract(contract_uuid, self.auth.user_id)
        self.view.display_contract(displayable_contract, focus=["Signed"])
