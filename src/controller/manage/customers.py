from typing import TYPE_CHECKING

from .common import Request, Roles, requests_map

if TYPE_CHECKING:
    from model import Model
    from view import View

    from .common import Auth


class CustomersControllerMixin:
    view: "View"
    model: "Model"
    auth: "Auth"

    # -------------------- CRM Commands below --------------------------

    @requests_map.register(Request.LIST_CUSTOMERS, required_role=Roles.ALL)
    def list_customers(self) -> None:
        """Retrieve customers from database and display them."""
        displayable_customers = self.model.get_customers()
        self.view.display_customers(displayable_customers)

    @requests_map.register(Request.DETAIL_CUSTOMER, required_role=Roles.ALL)
    def get_customer(self, customer_id: int) -> None:
        """Retrieve a given customer from database and display it."""
        displayable_customer = self.model.detail_customer(customer_id)
        self.view.display_customer(displayable_customer)

    @requests_map.register(Request.NEW_CUSTOMER, required_role=Roles.COMMERCIAL)
    def new_customer(self, fullname: str, company: str, email: str, phone: str) -> None:
        """Add a new customer to database and display it."""
        displayable_customer = self.model.add_customer(fullname, company, email, phone, employee_id=self.auth.user_id)
        self.view.display_customer(displayable_customer, focus=displayable_customer.keys())

    @requests_map.register(Request.UPDATE_CUSTOMER, required_role=Roles.COMMERCIAL)
    def update_customer_data(self, customer_id: int, fullname: str, company: str, email: str, phone: str) -> None:
        """Update customer fields in database and display the customer."""
        displayable_customer = self.model.update_customer_data(
            customer_id, fullname, company, email, phone, employee_id=self.auth.user_id
        )
        fields_name = {"Full name": fullname, "Company": company, "Email": email, "Phone": phone}
        self.view.display_customer(
            displayable_customer, focus=[name for name, new_value in fields_name.items() if new_value is not None]
        )

    @requests_map.register(Request.SET_CUSTOMER_COMMERCIAL, required_role=Roles.ADMINISTRATOR)
    def set_customer_commercial(self, customer_id: int, commercial_username: str) -> None:
        """Update the commercial associated to customer in database and display the customer."""
        displayable_customer = self.model.set_customer_commercial(customer_id, commercial_username)
        self.view.display_customer(displayable_customer, focus=["Commercial"])
