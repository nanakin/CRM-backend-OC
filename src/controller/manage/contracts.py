from .common import Request, Roles, requests_map


class ContractsControllerMixin:
    # -------------------- CRM Commands below --------------------------

    @requests_map.register(Request.LIST_CONTRACTS, required_role=Roles.ALL)
    def list_contracts(self, not_signed_filter, not_paid_filter):
        displayable_contracts = self.model.get_contracts(not_signed_filter, not_paid_filter)
        self.view.display_contracts(displayable_contracts)

    @requests_map.register(Request.DETAIL_CONTRACT, required_role=Roles.ALL)
    def get_contract(self, contract_uuid):
        displayable_contract = self.model.detail_contract(contract_uuid)
        self.view.display_contract(displayable_contract)

    @requests_map.register(Request.NEW_CONTRACT, required_role=Roles.ADMINISTRATOR)
    def new_contract(self, customer_id, total_amount):
        displayable_contract = self.model.add_contract(customer_id, total_amount)
        self.view.display_contract(displayable_contract, focus=displayable_contract.keys())

    @requests_map.register(Request.ADD_CONTRACT_PAYMENT, required_role=Roles.ADMINISTRATOR | Roles.COMMERCIAL)
    def add_contract_payment(self, contract_uuid, payment):
        displayable_contract = self.model.add_contract_payment(contract_uuid, payment)
        self.view.display_contract(displayable_contract, focus=("Total due",))

    @requests_map.register(Request.UPDATE_CONTRACT, required_role=Roles.ADMINISTRATOR | Roles.COMMERCIAL)
    def update_contract(self, contract_uuid, customer_id, total_amount):
        displayable_contract = self.model.update_contract(contract_uuid, customer_id, total_amount)
        self.view.display_contract(
            displayable_contract, focus=("Total amount" if total_amount else None, "Customer" if customer_id else None)
        )

    @requests_map.register(Request.SIGN_CONTRACT, required_role=Roles.ADMINISTRATOR | Roles.COMMERCIAL)
    def sign_contract(self, contract_uuid):
        displayable_contract = self.model.sign_contract(contract_uuid, self.authenticated_user.username)
        self.view.display_contract(displayable_contract, focus=("Signed",))
