from unittest import mock

import pytest

from crm.controller import Controller
from crm.controller.manage.common import requests_map
from crm.view import FullRequest, Request


@pytest.mark.parametrize("user_request", Request)
def test_requests_mapped(user_request):
    """Test that all requests are mapped to a function."""
    assert user_request in requests_map.allowed_functions.keys()


@pytest.mark.parametrize("user_request", Request)
def test_controller_execute(user_request):
    """Test that the controller execute the correct method."""
    view = mock.Mock()
    view.read_user_input = mock.MagicMock(return_value=FullRequest(user_request))
    model = mock.Mock()
    mocked_method = mock.MagicMock(return_value=None)
    requests_map.allowed_functions[user_request] = mocked_method
    controller = Controller(view, model, mock.Mock())
    controller.read_and_execute_command()
    mocked_method.assert_called_once()
