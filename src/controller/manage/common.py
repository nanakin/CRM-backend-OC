from enum import Enum, auto

from view.requests import Request  # noqa
from view.log import LogStatus


class Unauthenticated(Exception):
    pass


class NotEnoughPermission(Exception):
    pass


class Roles(Enum):
    COMMERCIAL = auto()
    SUPPORT = auto()
    ADMINISTRATOR = auto()


# def require_authentication(required_role=None):
#     def authenticate_as_role(self):
#         user_profile = self.authenticate()
#         if not user_profile:
#             raise Unauthenticated("Authentication failed.")
#         if required_role and user_profile.role != required_role:
#             raise NotEnoughPermission("Authenticated user does not have necessary permissions.")
#
#     def wrap(func):
#         def wrapped_f(self, *args, **kwargs):
#             try:
#                 authenticate_as_role(self)
#             except (Unauthenticated, NotEnoughPermission) as e:
#                 status = LogStatus.WARNING, str(e)
#             else:
#                 status = func(self, *args, **kwargs)
#             return status
#
#         return wrapped_f
#
#     return wrap


class RequestsMapping:
    def __init__(self):
        self.allowed = {}

    def register(self, request, required_role=None):

        def authenticate_as_role(controller):
            user_profile = controller.authenticate()
            if not user_profile:
                raise Unauthenticated("Authentication failed.")
            if required_role and user_profile.role != required_role:
                raise NotEnoughPermission("Authenticated user does not have necessary permissions.")

        def wrap(func):
            def notif_and_authenticate_wrap(controller, *args, **kwargs):

                def decorated_func(*args, **kwargs):
                    if required_role is not None:
                        try:
                            authenticate_as_role(controller)
                        except (Unauthenticated, NotEnoughPermission) as e:
                            controller.view.notification(LogStatus.WARNING, str(e))
                            return
                    status = func(*args, **kwargs)
                    if status:
                        controller.view.notification(*status)

                return decorated_func(controller, *args)

            self.allowed[request] = notif_and_authenticate_wrap

        return wrap


requests_map = RequestsMapping()
