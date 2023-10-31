from enum import Flag, auto

from model import OperationFailed
from view.log import LogStatus
from view.requests import Request  # noqa


# create enum from DB values ?
class Roles(Flag):
    NONE = auto()
    COMMERCIAL = auto()
    SUPPORT = auto()
    ADMINISTRATOR = auto()
    ALL = COMMERCIAL | SUPPORT | ADMINISTRATOR


class RequestsMapping:
    def __init__(self):
        self.allowed = {}

    def register(self, request, required_role=None):
        def authenticate_as_role(controller):
            user_profile = controller.authenticate()
            if not user_profile:
                raise OperationFailed("Authentication failed.")
            if user_profile.role not in required_role:
                raise OperationFailed(
                    f"{user_profile.username} does not have necessary permissions."
                )  # print user full name

        def wrap(func):
            def notif_and_authenticate_wrap(controller, *args, **kwargs):
                def decorated_func(*args, **kwargs):
                    if required_role is not None:
                        try:
                            authenticate_as_role(controller)
                        except OperationFailed as e:
                            controller.view.notification(LogStatus.WARNING, str(e))
                            return
                    try:
                        func(*args, **kwargs)
                    except OperationFailed as e:
                        controller.view.notification(LogStatus.WARNING, str(e))
                    else:
                        controller.view.notification(LogStatus.INFO, "Successful operation.")

                return decorated_func(controller, *args)

            self.allowed[request] = notif_and_authenticate_wrap

        return wrap


requests_map = RequestsMapping()
