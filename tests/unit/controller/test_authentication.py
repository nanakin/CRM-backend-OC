from contextlib import nullcontext as does_not_raise
from unittest import mock

import pytest

from crm.controller import Controller
from crm.controller.manage.authentication import Auth
from crm.controller.manage.common import OperationFailed, Roles


@pytest.fixture
def initialized_controller():
    view = mock.Mock()
    model = mock.Mock()
    controller = Controller(view, model)
    return controller


def user_with_role(role):
    return {"username": "test_username", "employee_id": 2, "fullname": "Test Full Name", "role": role}


@pytest.mark.parametrize(
    "trying_role, user_profile, expectation, message",
    [
        (Roles.NONE, None, pytest.raises(OperationFailed), "Authentication failed"),
        (Roles.NONE, user_with_role(Roles.COMMERCIAL), does_not_raise(), None),
        (Roles.ALL, user_with_role(Roles.ADMINISTRATOR), does_not_raise(), None),
        (Roles.ALL, user_with_role(Roles.NONE), pytest.raises(OperationFailed), "not have necessary permissions"),
        (Roles.ADMINISTRATOR | Roles.SUPPORT, None, pytest.raises(OperationFailed), "Authentication failed"),
        (
            Roles.ADMINISTRATOR | Roles.SUPPORT,
            user_with_role(Roles.NONE),
            pytest.raises(OperationFailed),
            "not have necessary permissions",
        ),
        (
            Roles.ADMINISTRATOR | Roles.SUPPORT,
            user_with_role(Roles.COMMERCIAL),
            pytest.raises(OperationFailed),
            "not have necessary permissions",
        ),
        (Roles.ADMINISTRATOR | Roles.SUPPORT, user_with_role(Roles.ADMINISTRATOR), does_not_raise(), None),
        (Roles.ADMINISTRATOR | Roles.SUPPORT, user_with_role(Roles.SUPPORT), does_not_raise(), None),
    ],
)
def test_controller_authenticate_as_role(initialized_controller, trying_role, user_profile, expectation, message):
    """Test role-based filter controller method 'authenticate_as_role'."""
    auth = Auth()
    if user_profile:
        auth.identify_as(**user_profile)
    initialized_controller.authenticate = mock.MagicMock(return_value=auth)
    with expectation as e:
        initialized_controller.authenticate_as_role(trying_role)
    assert message is None or message in str(e)
