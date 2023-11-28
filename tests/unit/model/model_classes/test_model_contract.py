import datetime
from unittest.mock import Mock
from uuid import UUID

import pytest
from sqlalchemy.exc import IntegrityError
from sqlalchemy_utils import force_instant_defaults

from crm.model.models import Contract

force_instant_defaults()


def test_contract_empty_constructor(db_session):
    """Test the contract constructor with no values."""
    contract = Contract()
    with pytest.raises(IntegrityError) as e_info:
        db_session.add(contract)
        db_session.commit()
    assert "NOT NULL constraint failed: contract.customer_id" in str(e_info.value)


def test_contract_constructor_with_default(db_session):
    """Test the contract constructor with default values."""
    contract = Contract(customer_id=3)
    db_session.add(contract)
    db_session.commit()
    assert isinstance(contract.id, UUID)
    assert isinstance(contract.creation_date, datetime.datetime)
    assert contract.customer_id == 3
    assert contract.signed is False
    assert contract.total_amount == 0
    assert contract.total_paid == 0
    assert hasattr(contract, "customer")


def test_get_contract(db_session):
    """Test the contract constructor with default values."""
    contract = Contract(customer_id=3)
    db_session.add_all([contract, Contract(customer_id=4)])
    db_session.commit()
    assert Contract.get(db_session, contract.id) == contract


def test_contract_update_total_amount():
    """Test the contract 'update_total_amount' method."""
    contract = Contract(customer_id=3)
    contract.update_total_amount(898.99)
    assert contract.total_amount == 89899


def test_contract_add_payment():
    """Test the contract 'add_payment' method."""
    contract = Contract(customer_id=3)
    contract.add_payment(324.3)
    assert contract.total_paid == 32430


def test_as_dict(db_session):
    """Test the contract 'as_dict' method."""
    contract = Contract(
        customer_id=3,
        total_amount=89899,
        signed=True,
        total_paid=3243,
        creation_date=datetime.datetime.fromisoformat("2021-12-30-10:02:59"),
    )
    contract.customer = Mock()
    contract.customer.commercial_contact = None
    expected = {
        "UUID": str(contract.id).upper(),
        "Customer": str(contract.customer),
        "Commercial": "None",
        "Signed": "True",
        "Total due": "866.56 €",
        "Total amount": "898.99 €",
        "Creation date": "2021-12-30 10:02:59",
    }
    result = contract.as_dict()
    assert result == expected
