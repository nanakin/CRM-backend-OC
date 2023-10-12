from typing import Any
from .sample import *
from sqlalchemy.orm import Session


@dataclass
class Populate:
    Session: Session
    roles: dict[str, Any]
    employees: dict[str, Any]
    customers: dict[str, Any]
    contracts: dict[str, Any]
    events: dict[str, Any]

    def __init__(self, sessionmaker):
        self.Session = sessionmaker

    @staticmethod
    def with_session_commit(populate_func: Callable) -> Callable:
        def wrapper_func(self, *args, **kwargs):
            objects = populate_func(self, *args, **kwargs)
            with self.Session() as session:
                session.add_all(objects)
                session.commit()

        return wrapper_func

    @with_session_commit
    def populate_roles(self) -> Iterable[Any]:
        self.roles = get_roles()
        return self.roles.values()

    @with_session_commit
    def populate_employees(self) -> Iterable[Any]:
        self.employees = get_employees(self.roles)
        return self.employees.values()

    @with_session_commit
    def populate_customers(self) -> Iterable[Any]:
        self.customers = get_customers(self.employees)
        return self.customers.values()

    @with_session_commit
    def populate_contracts(self) -> Iterable[Any]:
        self.contracts = get_contracts(self.customers)
        return self.contracts.values()

    @with_session_commit
    def populate_events(self) -> Iterable[Event]:
        self.events = get_events(contracts=self.contracts, employees=self.employees)
        return self.events.values()


def populate(sessionmaker):
    sampleObj = Populate(sessionmaker)
    sampleObj.populate_roles()
    sampleObj.populate_employees()
    sampleObj.populate_customers()
    sampleObj.populate_contracts()
    sampleObj.populate_events()
