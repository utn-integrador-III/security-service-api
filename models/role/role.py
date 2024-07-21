from models.role.db_queries import db_find_active_and_default_roles

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
    def find_active_and_default_roles(cls):
        # Fetch active roles and the default role from the database
        try:
            roles, default_role = db_find_active_and_default_roles()
            return roles, default_role
        except Exception as e:
            raise Exception('Error finding active and default roles')
