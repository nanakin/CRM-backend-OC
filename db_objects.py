import datetime
from dataclasses import dataclass
from typing import Callable, Iterable

from sqlalchemy.orm import Session

from model import Contract, Customer, Employee, Event, Role


def _get_roles():
    roles = {
        "commercial": Role(name="commercial"),
        "support": Role(name="support"),
        "administrator": Role(name="administrator"),
    }
    return roles


def _get_employees(roles):
    employees = {
        "caroline": Employee(
            fullname="Caroline Cridou", username="caroline_c", password="caroline", role_id=roles["commercial"].id
        ),
        "christophe": Employee(
            fullname="Christophe Criselleau",
            username="christophe_c",
            password="christophe",
            role_id=roles["commercial"].id,
        ),
        "amelie": Employee(
            fullname="Amelie Alumu", username="amelie_a", password="amelie", role_id=roles["administrator"].id
        ),
        "amandine": Employee(
            fullname="Amandine Aprostit", username="amandine_a", password="amandine", role_id=roles["administrator"].id
        ),
        "sebastien": Employee(
            fullname="Sebastien Serbot", username="sebastien_s", password="sebastien", role_id=roles["support"].id
        ),
        "sarah": Employee(fullname="Sarah Sergin", username="sarah_s", password="sarah", role_id=roles["support"].id),
    }
    return employees


def _get_customers(employees):
    customers = {
        "EDF": Customer(
            fullname="Thomas Duval",
            email="thomas@edf.fr",
            phone="+33683680178",
            company="EDF",
            commercial_contact_id=employees["caroline"].id,
        ),
        "Withings": Customer(
            fullname="Céline Katari",
            email="celine@withings.fr",
            phone="+337849900022",
            company="Withings",
            commercial_contact_id=employees["christophe"].id,
        ),
        "BK": Customer(
            fullname="Johanna Baker",
            email="johanna@bk.com",
            phone="+48893890045",
            company="Burger King",
            commercial_contact_id=employees["caroline"].id,
        ),
        "mariée": Customer(
            fullname="Inès Pradelle",
            email="ines.pradelle@gmail.com",
            phone="+33673890044",
            commercial_contact_id=employees["christophe"].id,
        ),
    }
    return customers


def _get_contracts(customers):
    contracts = {
        "BK_announcement": Contract(customer_id=customers["BK"].id, signed=False, total_amount=45000),
        "EDF_SG": Contract(customer_id=customers["EDF"].id, signed=True),
        "Withings_party": Contract(
            customer_id=customers["Withings"].id,
            signed=True,
        ),
    }
    return contracts


def _get_events(contracts, employees):
    events = {
        "EDF_SG": Event(
            name="EDF Summer Gathering",
            contract_id=contracts["EDF_SG"].id,
            support_contact_id=employees["sebastien"].id,
            start=datetime.datetime(year=2024, month=8, day=20, hour=14),
            end=datetime.datetime(year=2024, month=8, day=20, hour=14),
            attendees=2000,
            location="Jardin des plantes de Paris",
            note="En cas de pluie, déplacer les chaises dans la salle de projection.",
        )
    }
    return events


@dataclass
class Data:
    roles: dict[str, Role]
    employees: dict[str, Employee]
    customers: dict[str, Customer]
    contracts: dict[str, Contract]
    events: dict[str, Event]
    session: Session

    @staticmethod
    def with_session_commit(populate_func: Callable) -> Callable:
        def wrapper_func(self, *args, **kwargs):
            objects = populate_func(self, *args, **kwargs)
            self.session.add_all(objects)
            self.session.commit()

        return wrapper_func

    def __init__(self, session: Session) -> None:
        self.session = session
        self.populate_roles()
        self.populate_employees()
        self.populate_customers()
        self.populate_contracts()
        self.populate_events()

    def list_data(self) -> None:
        print(self.roles)
        print(self.employees)
        print(self.customers)
        print(self.contracts)
        print(self.events)

    @with_session_commit
    def populate_roles(self) -> Iterable[Role]:
        self.roles = _get_roles()
        return self.roles.values()

    @with_session_commit
    def populate_employees(self) -> Iterable[Employee]:
        self.employees = _get_employees(self.roles)
        return self.employees.values()

    @with_session_commit
    def populate_customers(self) -> Iterable[Customer]:
        self.customers = _get_customers(self.employees)
        return self.customers.values()

    @with_session_commit
    def populate_contracts(self) -> Iterable[Contract]:
        self.contracts = _get_contracts(self.customers)
        return self.contracts.values()

    @with_session_commit
    def populate_events(self) -> Iterable[Event]:
        self.events = _get_events(contracts=self.contracts, employees=self.employees)
        return self.events.values()
