from enum import Enum

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy_utils import database_exists, drop_database

from .models import (
    Base,
    Contract,
    ContractModelMixin,
    Customer,
    CustomerModelMixin,
    Employee,
    EmployeeModelMixin,
    Event,
    EventModelMixin,
    Role,
)

DEFAULT_DB = "sqlite://"  # in-memory SQLite database


class Model(EmployeeModelMixin, CustomerModelMixin, ContractModelMixin, EventModelMixin):
    """Model class to manage database operations."""

    def get_roles(self):
        """Retrieve roles from the database and return an Enum to facilitate permissions management."""
        with self.Session() as session:
            roles = session.query(Role).all()
        dict_roles = {}
        for role in roles:
            dict_roles[role.name.upper()] = role.id
        return Enum("EnumRoles", dict_roles)

    def __init__(self, url: str = DEFAULT_DB, echo: bool = False, reset: bool = False) -> None:
        """Initialize the database and create tables if necessary."""
        engine = create_engine(url, echo=echo)
        self.Session = sessionmaker(engine, expire_on_commit=False)
        if reset:
            drop_database(engine.url)
        if not database_exists(url):
            Base.metadata.create_all(engine)
        else:
            self.roles = self.get_roles()

    def populate_with_sample(self):  # possibility to move this method
        """Populate the database with sample data."""
        from .model_sample.populate import populate

        populate(self.Session)
        self.roles = self.get_roles()
