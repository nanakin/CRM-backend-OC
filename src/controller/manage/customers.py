from .common import Request, requests_map


class CustomersControllerMixin:
    # -------------------- CRM Commands below --------------------------

    @requests_map.register(Request.LIST_CUSTOMERS)
    def list_customers(self):
        print("list customers")
