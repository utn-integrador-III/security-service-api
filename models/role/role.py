from models.role.db_queries import db_find_active_roles, db_find_default_role


class RoleModel:
    def __init__(self, name, description, permissions, creation_date, mod_date, is_active, default_role, screens, app, _id=None):
        self.name = name
        self.description = description
        self.permissions = permissions
        self.creation_date = creation_date
        self.mod_date = mod_date
        self.is_active = is_active
        self.default_role = default_role
        self.screens = screens
        self.app = app
        self._id = _id

    @classmethod
    def find_active_roles(cls):
        # Example implementation to find active roles from the database
        try:
            # Assume db_find_active_roles fetches active roles from the database
            roles = db_find_active_roles()
            return roles
        except Exception as e:
            raise Exception('Error finding active roles')

    @classmethod
    def find_default_role(cls):
        # Fetch the default role from the database
        try:
            # Example database call to find the default role
            default_role = db_find_default_role()
            return default_role
        except Exception as e:
            raise Exception('Error finding default role')
