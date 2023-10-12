from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, drop_database, create_database
from . import Contract, Customer, Employee, Event, Role, Base

DEFAULT_DB = "sqlite://"


def db_list_entries(engine):
    with Session(engine) as session:
        to_list = [Role, Employee, Customer, Contract, Event]
        for table in to_list:
            items = session.query(table).all()
            for item in items:
                print(item)


class Model:

    def get_employees(self):
        with self.Session() as session:
            items = session.query(Employee).all()
            return items

    def __init__(self, url=DEFAULT_DB, echo=False, reset=False) -> None:
        self.engine = create_engine(url, echo=echo)
        self.Session = sessionmaker(self.engine, expire_on_commit=False)
        if reset:
            print("reset !")
            drop_database(self.engine.url)
        if not database_exists(url):
            print("create !")
            Base.metadata.create_all(self.engine)
        # db_list_entries(self.engine)

    def populate_with_sample(self):
        from .model_sample.populate import populate
        populate(self.Session)

    def list_data(self) -> None:
        print(Role)
        print(Employee)
        # print(self.customers)
        # print(self.contracts)
        # print(self.events)
