from view.requests import Request
from enum import Enum, auto

class Unauthenticated(Exception):
    pass


class NotEnoughPermission(Exception):
    pass


class Roles(Enum):
    COMMERCIAL = auto()
    SUPPORT = auto()
    ADMINISTRATOR = auto()


def require_authentication(required_role=None):

    def authenticate_as_role(self):
        user_profile = self.authenticate()
        if not user_profile:
            raise Unauthenticated("Authentication failed.")
        if required_role and user_profile.role != required_role:
            raise NotEnoughPermission("Authenticated user does not have necessary permissions.")

    def wrap(func):
        def wrapped_f(self, *args, **kwargs):
            try:
                authenticate_as_role(self)
            except (Unauthenticated, NotEnoughPermission) as e:
                ret = self.view.warning(str(e))
            else:
                ret = func(self, *args, **kwargs)
            return ret
        return wrapped_f
    return wrap


class RequestsMapping:

    def __init__(self):
        self.allowed = {}

    def register(self, request):
        def wrap(func):
            self.allowed[request] = func

            def wrapped_f(*args, **kwargs):
                return func(*args, **kwargs)
            return wrapped_f
        return wrap


requests_map = RequestsMapping()
