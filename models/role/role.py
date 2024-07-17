from models.role.db_queries import db_find_active_roles

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

    def to_dict(self):
        return {
            'name': self.name,
            'description': self.description,
            'permissions': self.permissions,
            'creation_date': self.creation_date,
            'mod_date': self.mod_date,
            'is_active': self.is_active,
            'default_role': self.default_role,
            'screens': self.screens,
            'app': self.app,
            '_id': self._id
        }
    
    @classmethod
    def find_active_roles(cls):
        try:
            roles = db_find_active_roles()
            return roles
        except Exception as e:
            raise Exception('Error finding active roles')
