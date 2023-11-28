import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from crm.model.models import Base

TEST_DB = "sqlite://"  # in-memory SQLite database


@pytest.fixture(scope="session")
def db_engine(request):
    """yields a SQLAlchemy engine which is suppressed after the test session."""
    db_url = TEST_DB
    engine = create_engine(db_url, echo=False)
    Base.metadata.create_all(engine)
    yield engine


@pytest.fixture(scope="session")
def db_session_maker(db_engine):
    """returns a SQLAlchemy scoped session factory."""
    return sessionmaker(bind=db_engine, expire_on_commit=False)


@pytest.fixture(scope="session")
def db_session_factory(db_session_maker):
    """returns a SQLAlchemy scoped session factory."""
    return scoped_session(db_session_maker)


@pytest.fixture(scope="function")
def db_session(db_session_factory):
    """yields a SQLAlchemy connection which is rollbacked after the test."""
    session = db_session_factory()
    yield session
    session.rollback()
    session.close()
