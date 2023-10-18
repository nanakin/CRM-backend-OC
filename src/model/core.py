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
            return session.query(Employee).all()

    def get_employee(self, username):
        with self.Session() as session:
            return session.query(Employee).filter_by(username=username).one_or_none()

    def valid_password(self, username, password):
        employee = self.get_employee(username)
        if not employee:
            return False
        return employee.valid_password(password)

    def __init__(self, url=DEFAULT_DB, echo=False, reset=False) -> None:
        self.engine = create_engine(url, echo=echo)
        self.Session = sessionmaker(self.engine, expire_on_commit=False)
        if reset:
            drop_database(self.engine.url)
        if not database_exists(url):
            Base.metadata.create_all(self.engine)

    def populate_with_sample(self):  # possibility to move this method
        from .model_sample.populate import populate
        populate(self.Session)
