from view.requests import Request
from view.log import LogStatus
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
                status = LogStatus.WARNING, str(e)
            else:
                status = func(self, *args, **kwargs)
            return status
        return wrapped_f
    return wrap


class RequestsMapping:

    def __init__(self):
        self.allowed = {}

    def register(self, request):

        def wrap(func):
            def notif_wrap():
                def decorated_func(controller, *args, **kwargs):
                    status = func(controller, *args, **kwargs)
                    if status:
                        controller.view.notification(*status)

                return decorated_func

            self.allowed[request] = notif_wrap()
        return wrap


requests_map = RequestsMapping()
