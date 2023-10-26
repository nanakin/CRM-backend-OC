from enum import Enum

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy_utils import database_exists, drop_database

from .models import Base, Contract, Customer, CustomerModelMixin, Employee, EmployeeModelMixin, Event, Role

DEFAULT_DB = "sqlite://"


def db_list_entries(engine):
    with Session(engine) as session:
        to_list = [Role, Employee, Customer, Contract, Event]
        for table in to_list:
            items = session.query(table).all()
            for item in items:
                print(item)


class Model(EmployeeModelMixin, CustomerModelMixin):

    def get_roles(self):
        with self.Session() as session:
            roles = session.query(Role).all()
        dict_roles = {}
        for role in roles:
            dict_roles[role.name.upper()] = role.id
        return Enum("EnumRoles", dict_roles)

    def __init__(self, url=DEFAULT_DB, echo=False, reset=False) -> None:
        self.engine = create_engine(url, echo=echo)
        self.Session = sessionmaker(self.engine, expire_on_commit=False)
        self.roles = None
        if reset:
            drop_database(self.engine.url)
        if not database_exists(url):
            Base.metadata.create_all(self.engine)
        else:
            self.roles = self.get_roles()

    def populate_with_sample(self):  # possibility to move this method
        from .model_sample.populate import populate

        populate(self.Session)
        self.roles = self.get_roles()
