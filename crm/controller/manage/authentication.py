import jwt
from datetime import datetime, timedelta
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING, Optional

from .common import OperationFailed, Request, Roles, requests_map

if TYPE_CHECKING:
    from crm.model import Model
    from crm.view import View


AUTH_FILENAME = Path(".auth")


@dataclass
class Auth:
    """Store authentication information."""

    @dataclass
    class User:
        """Store profile of the authenticated employee."""

        username: str
        id: int
        fullname: str
        role: Roles

    secret_key: str
    user: Optional[User] = None

    @property
    def user_id(self) -> Optional[int]:
        return self.user.id if self.user else None

    @property
    def is_authenticated(self) -> bool:
        return self.user is not None

    def identify_as(self, username: str, employee_id: int, fullname: str, role: Roles) -> None:
        """Keep track of the authenticated user."""
        self.user = self.User(username, employee_id, fullname, role)


class AuthenticationControllerMixin:
    view: "View"
    model: "Model"
    auth: "Auth"

    def _get_data_from_token(self):
        def load_from_persistent():
            try:
                with open(AUTH_FILENAME, encoding="utf-8") as f:
                    token = f.read()
            except FileNotFoundError:
                return None
            except (PermissionError, OSError, IOError):
                print("⚠ Failed to load authentication token.")
                return None
            return token

        token = load_from_persistent()
        if not token:
            return None
        secret_key = self.auth.secret_key
        try:
            data = jwt.decode(token, secret_key, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            print("⚠ Authentication token expired, please log again.")
        except jwt.InvalidTokenError as err:
            print("⚠ Invalid token:", err)
        else:
            return data["username"]

    def _set_authenticated_user(self, username):
        def create_token():
            secret_key = self.auth.secret_key
            token = jwt.encode(
                {"username": self.auth.user.username, "exp": datetime.utcnow() + timedelta(minutes=30)},
                secret_key,
                algorithm="HS256",
            )
            return token

        def persistent_save():
            try:
                with open(AUTH_FILENAME, "w", encoding="utf-8") as f:
                    f.write(token)
            except (FileNotFoundError, PermissionError, OSError, IOError):
                print("⚠ Failed to save authentication token.")

        employee_as_dict = self.model.detail_employee(username)
        self.auth.identify_as(
            employee_as_dict["Username"],
            employee_as_dict["ID"],
            employee_as_dict["Full name"],
            Roles[employee_as_dict["Role"].upper()],
        )
        token = create_token()
        persistent_save()

    def _token_authentication(self):
        username = self._get_data_from_token()
        if username:
            self._set_authenticated_user(username)
        return self.auth.is_authenticated

    def _login_with_password(self, username, password):
        is_valid = self.model.valid_password(username, password)
        if is_valid:
            self._set_authenticated_user(username)
        return is_valid

    # ---------- used by require_authentication decorator --------------

    def authenticate(self):
        if not self._token_authentication():
            username, password = self.view.ask_credentials()
            self._login_with_password(username, password)
        return self.auth

    def authenticate_as_role(self, required_role: Roles) -> None:
        """
        Try to authenticate the user and raise an exception if the user does not have the required permissions.
        """
        auth = self.authenticate()
        if not auth.is_authenticated:
            raise OperationFailed("Authentication failed.")
        if required_role != Roles.NONE and auth.user.role not in required_role:  # type: ignore
            raise OperationFailed(f"{auth.user.fullname} does not have necessary permissions.")

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
