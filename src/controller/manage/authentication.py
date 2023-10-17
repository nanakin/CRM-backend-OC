from .common import requests_map, Request


class AuthenticationControllerMixin:

    def refresh_access_token(self):
        # update the access token
        pass

    def is_authenticated(self):
        # return True if a valid token exists else otherwise
        pass

    @requests_map.register(Request.LOGIN)
    def login(self, param=None):
        print("login")
        # verify if already login
        # ask credentials
        # store refresh and access token as environment variable
        data = self.model.get_employees()
        print(data, "employee controller")
        self.view.display_employees(data)

    @requests_map.register(Request.LOGOUT)
    def logout(self):
        # remove all stored tokens
        print("logout")
