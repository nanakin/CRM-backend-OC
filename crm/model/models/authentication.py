from sqlalchemy.orm import Mapped, Session, mapped_column
from typing import Self
from sqlalchemy import String
from .common import Base, OperationFailed


class Key(Base):
    """Store JWT secret key."""

    __tablename__ = "key"

    secret: Mapped[str] = mapped_column(String(127), primary_key=True)

    @classmethod
    def get(cls, session: Session) -> Self:
        """Retrieve the JWT secret key, raise an exception otherwise."""
        result = session.query(cls).first()
        if result is None:
            raise OperationFailed("Cannot find JWT secret key")
        return result
