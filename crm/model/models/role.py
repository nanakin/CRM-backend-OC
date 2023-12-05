from sqlalchemy import Unicode
from sqlalchemy.orm import Mapped, mapped_column

from .common import Base


class Role(Base):
    """Role database model."""

    __tablename__ = "role"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(Unicode(127))

    def __str__(self):
        return self.name

    def __repr__(self) -> str:
        return f"Role(id={self.id!r}, name={self.name!r})"
