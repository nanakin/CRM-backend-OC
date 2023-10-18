from .common import requests_map, Request
import jwt

def require_authentication(role=None):
    pass
    # if self.is_authenticated:
    #     try:
    #         self.refresh_access_token
    #     except:
    #         pass


class AuthenticationControllerMixin:

    def refresh_access_token(self):
        # update the access token
        pass

    def is_authenticated(self):
        # return True if a valid token exists else otherwise
        #jwt.decode(encoded_jwt, "secret", algorithms=["HS256"])
        # >>_{'some': 'payload'}
        pass

    @requests_map.register(Request.LOGIN)
    def login(self, username, password):
        is_valid = self.model.valid_password(username, password)
        if is_valid:
            message = "Successful authentication"
            self.view.info(message)
        else:
            message = "Invalid credentials"
            self.view.warning(message)

        #encoded_jwt = jwt.encode({"username": "username"}, "secret", algorithm="HS256")
        # verify if already login
        # store refresh and access token as environment variable

    @requests_map.register(Request.LOGOUT)
    def logout(self):
        # remove all stored tokens
        print("logout")
