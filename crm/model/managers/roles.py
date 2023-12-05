from enum import Enum

from sqlalchemy.orm import sessionmaker

from crm.model.models import OperationFailed
from crm.model.models.role import Role


class RoleModelMixin:
    Session: sessionmaker

    def get_roles(self):
        """Retrieve roles from the database and return an Enum to facilitate permissions management."""
        with self.Session() as session:
            roles = session.query(Role).all()
        dict_roles = {}
        for role in roles:
            dict_roles[role.name.upper()] = role.id
        return Enum("EnumRoles", dict_roles)

    def is_role_equal(self, db_role, enum_role) -> bool:
        """Return True if the role name and id are matching, False otherwise."""
        return db_role.id == self.roles[enum_role.name.upper()].value

    def get_role_id_from_name(self, role_name: str) -> int:
        valid_roles_names = [role.name for role in self.roles]
        if role_name.upper() not in valid_roles_names:
            raise OperationFailed(f"Invalid role, choose between: {' '.join(valid_roles_names)}.")
        return self.roles[role_name.upper()].value
