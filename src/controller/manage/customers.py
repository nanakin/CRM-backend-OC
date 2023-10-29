from .common import Request, Roles, requests_map


class CustomersControllerMixin:
    # -------------------- CRM Commands below --------------------------

    @requests_map.register(Request.LIST_CUSTOMERS, required_role=Roles.ALL)
    def list_customers(self):
        displayable_customers = self.model.get_customers()
        self.view.display_customers(displayable_customers)

    @requests_map.register(Request.DETAIL_CUSTOMER, required_role=Roles.ALL)
    def get_customer(self, id):
        displayable_customer = self.model.detail_customer(id)
        self.view.display_customer(displayable_customer)

    @requests_map.register(Request.NEW_CUSTOMER, required_role=Roles.COMMERCIAL)
    def new_customer(self, fullname, company, email, phone):
        displayable_customer = self.model.add_customer(fullname, company, email, phone, commercial_username=self.authenticated_user.username)
        self.view.display_customer(displayable_customer, focus=displayable_customer.keys())

    @requests_map.register(Request.UPDATE_CUSTOMER, required_role=Roles.COMMERCIAL)
    def update_customer_data(self, id, fullname, company, email, phone):
        displayable_customer = self.model.update_customer_data(id, fullname, company, email, phone,
                                                               commercial_contact_filter=self.authenticated_user.username)
        self.view.display_customer(displayable_customer,
                                   focus=("Company" if company else None,
                                          "Full name" if fullname else None,
                                          "Email" if email else None,
                                          "Phone" if phone else None))

    @requests_map.register(Request.SET_CUSTOMER_COMMERCIAL, required_role=Roles.ADMINISTRATOR)
    def set_customer_commercial(self, id, commercial_username):
        displayable_customer = self.model.set_customer_commercial(id, commercial_username)
        self.view.display_customer(displayable_customer, focus=("Commercial",))
