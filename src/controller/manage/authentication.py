from .common import requests_map, Request, Roles
from collections import namedtuple
import jwt
import os

TOKEN_NAME = 'CRM_TOKEN'
User = namedtuple("User", "username role")


class AuthenticationControllerMixin:

    def refresh_access_token(self):
        # update the access token
        pass

    @staticmethod
    def get_token():
        return os.getenv(TOKEN_NAME, None)

    def token_authentication(self):
        token = self.get_token()
        #jwt.decode(encoded_jwt, "secret", algorithms=["HS256"])
        # >>_{'some': 'payload'}
        self.authenticated_user = token  # temporary

    def authenticate(self):
        if not self.token_authentication():
            username, password = self.view.ask_credentials()
            self.login_with_password(username, password)
        return self.authenticated_user

    def login_with_password(self, username, password):
        is_valid = self.model.valid_password(username, password)
        if is_valid:
            role_name = self.model.get_role(username)
            self.authenticated_user = User(username, Roles[role_name])
            os.environ[TOKEN_NAME] = username  # temporary
        return is_valid

    @requests_map.register(Request.LOGIN)
    def login(self, username, password):
        is_valid = self.login_with_password(username, password)
        if is_valid:
            message = "Successful authentication"
            self.view.info(message)
        else:
            message = "Invalid credentials"
            self.view.warning(message)

    @requests_map.register(Request.LOGOUT)
    def logout(self):
        # remove all stored tokens
        print("logout")
        if TOKEN_NAME in os.environ:
            os.environ.pop(TOKEN_NAME)
