from .common import requests_map, Request, Roles, LogStatus
from collections import namedtuple
import jwt
from pathlib import Path

AUTH_FILENAME = Path(".auth")
User = namedtuple("User", "username role")


class AuthenticationControllerMixin:

    def refresh_access_token(self):
        # update the access token
        pass

    def get_token(self):
        return self.load_from_persistent()

    def authenticate(self):
        if not self.token_authentication():
            username, password = self.view.ask_credentials()
            self.login_with_password(username, password)
        return self.authenticated_user

    def set_authenticated_user(self, username):
        role_name = self.model.get_role(username)
        self.authenticated_user = User(username, Roles[role_name])

    def token_authentication(self):
        username = self.get_token()
        if username:
            self.set_authenticated_user(username)
        return bool(self.authenticated_user)

    def persistent_save(self):
        with open(AUTH_FILENAME, "w", encoding="utf-8") as f:
            f.write(self.authenticated_user.username)  # temp

    @staticmethod
    def load_from_persistent():
        try:
            with open(AUTH_FILENAME, encoding="utf-8") as f:
                username = f.read()  # temp
        except FileNotFoundError:
            username = None
        return username

    def login_with_password(self, username, password):
        is_valid = self.model.valid_password(username, password)
        if is_valid:
            self.set_authenticated_user(username)
            self.persistent_save()
        return is_valid

    @requests_map.register(Request.LOGIN)
    def login(self, username, password):
        is_valid = self.login_with_password(username, password)
        if is_valid:
            return LogStatus.INFO, "Successful authentication"
        else:
            return LogStatus.WARNING, "Invalid credentials"

    @requests_map.register(Request.LOGOUT)
    def logout(self):
        if Path.is_file(AUTH_FILENAME):
            Path.unlink(AUTH_FILENAME)
            return LogStatus.INFO, "Successfully logged out"
        else:
            return LogStatus.WARNING, "No one to logged out"
