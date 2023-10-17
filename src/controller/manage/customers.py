from .common import requests_map, Request


class CustomersControllerMixin:

    @requests_map.register(Request.LIST_CUSTOMERS)
    def list_customers(self):
        print("list customers")
