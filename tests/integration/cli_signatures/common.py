from inspect import signature


def matching_signature(func, param) -> bool:
    """Verify if the signature of the function correspond to the passed parameters."""
    required_param = list(signature(func).parameters.keys())[1:]
    return set(required_param) == set(param.keys())
