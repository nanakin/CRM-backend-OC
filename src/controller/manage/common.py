from view.requests import Request


class RequestsMapping:

    def __init__(self):
        self.allowed = {}

    def register(self, request):
        def wrap(func):
            self.allowed[request] = func

            def wrapped_f(*args, **kwargs):
                func(*args, **kwargs)
            return wrapped_f
        return wrap


requests_map = RequestsMapping()
