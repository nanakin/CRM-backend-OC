from sqlalchemy import create_engine, event
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, drop_database

from .managers import ContractModelMixin, CustomerModelMixin, EmployeeModelMixin, EventModelMixin, RoleModelMixin
from .models import Base, Role

DEFAULT_DB = "sqlite://"  # in-memory SQLite database


# Activate Sqlite foreign key support
@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


class Model(EmployeeModelMixin, CustomerModelMixin, ContractModelMixin, EventModelMixin, RoleModelMixin):
    """Model class to manage database operations."""

    def __init__(self, url: str = DEFAULT_DB, echo: bool = False, reset: bool = False):
        """Initialize the database and create tables if necessary."""
        engine = create_engine(url, echo=echo)
        self.engine = engine
        self.Session = sessionmaker(engine, expire_on_commit=False)
        if reset and database_exists(url):
            drop_database(engine.url)
        if not database_exists(url):
            Base.metadata.create_all(engine)
        else:
            self.roles = self.get_roles()

    def end(self):
        """Close the database."""
        if self.engine:
            self.engine.dispose()

    def populate_with_sample(self):  # possibility to move this method
        """Populate the database with sample data."""
        from .model_sample.populate import populate

        with self.Session() as session:
            if session.query(Role).count() > 0:
                return
        print("ℹ️  Populating database with a dataset sample ...")
        populate(self.Session)
        self.roles = self.get_roles()
