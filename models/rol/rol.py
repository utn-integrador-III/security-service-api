import logging
from utils.encryption_utils import EncryptionUtil
from models.rol.db_queries import __dbmanager__
from datetime import datetime
import pytz

class RolModel:
    def __init__(self, name, description, permissions,creation_date,mod_date,is_active,default_role,screens,app, status=None, verification_code=None, expiration_time=None, _id=None):
        self.name = name
        self.description = description
        self.permissions = permissions if permissions else []
        self.creation_date = (
            creation_date 
            if creation_date 
            else datetime.now(pytz.timezone("America/Costa_Rica")).replace(tzinfo=None)
        )
        self.mod_date = mod_date       
        self.is_active = is_active
        self.default_role = default_role
        self.screens = screens if screens else []
        self.app = app
    
    def to_dict(self):
        return {
            'name': self.name,
            'description': self.description,
            'permissions': self.permissions,
            'creation_date': self.creation_date,
            'mod_date': self.mod_date,
            'is_active': self.is_active,
            'default_role': self.default_role,
            'screens':self.screens,
            'app': self.app
        }

    @classmethod
    def get_by_name(cls, name):
        try:
            result = __dbmanager__.find_one({"name": name})
            if result:
                return cls(
                    _id=result.get("_id"),
                    name=result.get("name"),
                    description=result.get("description"),
                    permissions=result.get("permissions"),
                    creation_date=result.get("creation_date"),
                    mod_date=result.get("mod_date"),
                    is_active=result.get("is_active"),
                    default_role=result.get("default_role"),
                    screens=result.get("screens"),
                    app=result.get("app")
                )
            return None
        except Exception as ex:
            logging.exception(ex)
            raise Exception("Failed to get rol by name: " + str(ex))
