from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

from db_objects import Data
from model import Base, Contract, Customer, Employee, Event, Role


def db_connect():
    return create_engine("sqlite://")


def db_create_and_populate(engine):
    Base.metadata.create_all(engine)
    with Session(engine) as session:
        data = Data(session)


def db_list_entries(engine):
    with Session(engine) as session:
        to_list = [Role, Employee, Customer, Contract, Event]
        for table in to_list:
            stmt = select(table)
            for item in session.scalars(stmt):
                print(item)


if __name__ == "__main__":
    engine = db_connect()
    db_create_and_populate(engine)
    db_list_entries(engine)
