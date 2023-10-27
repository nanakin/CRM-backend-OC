from sqlalchemy import Unicode
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .common import Base

from typing import List


class Role(Base):
    __tablename__ = "role"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(Unicode(127))
    # establish a bidirectional one-to-many relationship (role-employees)
    # employees: Mapped[List["Employee"]] = relationship(back_populates="role")

    def __repr__(self) -> str:
        return f"Role(id={self.id!r}, name={self.name!r})"