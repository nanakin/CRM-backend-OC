from dataclasses import dataclass
from typing import Callable, Iterable

from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, drop_database, create_database
from . import Contract, Customer, Employee, Event, Role, Base
from .model_sample.sample import *

DEFAULT_DB = "sqlite://"


def db_list_entries(engine):
    with Session(engine) as session:
        to_list = [Role, Employee, Customer, Contract, Event]
        for table in to_list:
            items = session.query(table).all()
            for item in items:
                print(item)


@dataclass
class Model:
    roles: dict[str, Role]
    employees: dict[str, Employee]
    customers: dict[str, Customer]
    contracts: dict[str, Contract]
    events: dict[str, Event]
    #session: Session

    def get_employees(self):
        return self.employees

    @staticmethod
    def with_session_commit(populate_func: Callable) -> Callable:
        def wrapper_func(self, *args, **kwargs):
            objects = populate_func(self, *args, **kwargs)
            with self.Session() as session:
                session.add_all(objects)
                session.commit()
        return wrapper_func

    def __init__(self, url=DEFAULT_DB, echo=False, reset=False) -> None:
        self.engine = create_engine(url, echo=echo)
        self.Session = sessionmaker(self.engine, expire_on_commit=False)
        if reset:
            print("reset !")
            drop_database(self.engine.url)
        if not database_exists(url):
            print("create !")
            # create_database(self.engine.url)
            Base.metadata.create_all(self.engine)

            self.populate_roles()
            with self.Session() as session:
                items = session.query(Role).all()
                for item in items:
                    print(item)
            print(self.roles)
            self.populate_employees()
            self.populate_customers()
            self.populate_contracts()
            self.populate_events()
        else:
            print("DB already exists")
        db_list_entries(self.engine)

    def list_data(self) -> None:
        print(self.roles)
        print(self.employees)
        print(self.customers)
        print(self.contracts)
        print(self.events)

    @with_session_commit
    def populate_roles(self) -> Iterable[Role]:
        self.roles = get_roles()
        return self.roles.values()

    @with_session_commit
    def populate_employees(self) -> Iterable[Employee]:
        self.employees = get_employees(self.roles)
        return self.employees.values()

    @with_session_commit
    def populate_customers(self) -> Iterable[Customer]:
        self.customers = get_customers(self.employees)
        return self.customers.values()

    @with_session_commit
    def populate_contracts(self) -> Iterable[Contract]:
        self.contracts = get_contracts(self.customers)
        return self.contracts.values()

    @with_session_commit
    def populate_events(self) -> Iterable[Event]:
        self.events = get_events(contracts=self.contracts, employees=self.employees)
        return self.events.values()
