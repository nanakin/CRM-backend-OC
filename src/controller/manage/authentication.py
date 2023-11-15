from typing import TYPE_CHECKING
# import jwt
from pathlib import Path

from .common import OperationFailed, Request, Roles, requests_map

if TYPE_CHECKING:
    from model import Model
    from view import View
    from .common import Auth


AUTH_FILENAME = Path(".auth")


class AuthenticationControllerMixin:

    view: "View"
    model: "Model"
    auth: "Auth"

    def _get_token(self):

        return self._load_from_persistent()

    def _set_authenticated_user(self, username):
        employee_as_dict = self.model.detail_employee(username)
        self.auth.identify_as(employee_as_dict["Username"],
                              employee_as_dict["ID"],
                              employee_as_dict["Full name"],
                              Roles[employee_as_dict["Role"].upper()])

    def _token_authentication(self):
        username = self._get_token()
        if username:
            self._set_authenticated_user(username)
        return self.auth.is_authenticated

    def _persistent_save(self):
        with open(AUTH_FILENAME, "w", encoding="utf-8") as f:
            f.write(self.auth.user.username)  # temp

    @staticmethod
    def _load_from_persistent():
        try:
            with open(AUTH_FILENAME, encoding="utf-8") as f:
                username = f.read()  # temp
        except FileNotFoundError:
            username = None
        return username

    def _login_with_password(self, username, password):
        is_valid = self.model.valid_password(username, password)
        if is_valid:
            self._set_authenticated_user(username)
            self._persistent_save()
        return is_valid

    # ---------- used by require_authentication decorator --------------

    def authenticate(self):
        if not self._token_authentication():
            username, password = self.view.ask_credentials()
            self._login_with_password(username, password)
        return self.auth

    # -------------------- CRM Commands below --------------------------

    @requests_map.register(Request.LOGIN)
    def login(self, username, password):
        is_valid = self._login_with_password(username, password)
        if not is_valid:
            raise OperationFailed("Invalid credentials.")

    @requests_map.register(Request.LOGOUT)
    def logout(self):
        if Path.is_file(AUTH_FILENAME):
            Path.unlink(AUTH_FILENAME)
