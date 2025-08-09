from models.role.db_queries import db_find_active_and_default_roles
import logging
from models.role.db_queries import __dbmanager__
from models.application.getapp import ApplicationModel

class RoleModel:
    def __init__(self, name, description, permissions, creation_date, mod_date, is_active, default_role, screens, app, app_client_id=None, _id=None):
        self.name = name
        self.description = description
        self.permissions = permissions
        self.creation_date = creation_date
        self.mod_date = mod_date
        self.is_active = is_active
        self.default_role = default_role
        self.screens = screens
        self.app = app
        self.app_client_id = app_client_id
        self._id = _id
        
    def to_dict(self):
        return {
            "_id": self._id,
            "name": self.name,
            "description": self.description,
            "permissions": self.permissions,
            "creation_date": self.creation_date,
            "mod_date": self.mod_date,
            "is_active": self.is_active,
            "default_role": self.default_role,
            "screens": self.screens,
            "app": self.app,
            "app_client_id": self.app_client_id
        }

    @classmethod
    def find_active_and_default_roles(cls):
        # Fetch active roles and the default role from the database
        try:
            roles, default_role = db_find_active_and_default_roles()
            return roles, default_role
        except Exception as e:
            raise Exception('Error finding active and default roles')

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
                    app=result.get("app"),
                    app_client_id=result.get("app_client_id")
                )
            return None
        except Exception as ex:
            logging.exception(ex)
            raise Exception("Failed to get rol by name: " + str(ex))
    

    @classmethod
    def create(cls, role_data):
        try:
            result = __dbmanager__.create_data(role_data)
            if result.inserted_id:
                role_data["_id"] = result.inserted_id
                return cls(**role_data)
            return None
        except Exception as ex:
            logging.exception(ex)
            raise Exception("Error creating role: " + str(ex))
        
    #Meotod para agregar screens
    @classmethod
    def add_screens(cls, role_name, client_id, new_screens):
        try:
            if not isinstance(new_screens, list):
                raise ValueError("Screens must be a list of strings")

            # Buscar rol 
            existing_role = __dbmanager__.find_one({"name": role_name, "app_client_id": client_id})
            if not existing_role:
                return None  # No existe el rol
            

            result = __dbmanager__.collection.update_one(
                {"name": role_name, "app_client_id": client_id},
                {#Para poder seguir agregando sin que se borren existentes
                    "$addToSet": {
                        "screens": {"$each": new_screens}
                    }
                    
                }
            )

            if result.modified_count == 0:
             # No se agregó nada, las screens ya estaban
                return "DUPLICATE"

            updated_role = __dbmanager__.find_one({"name": role_name, "app_client_id": client_id})
            return cls(
                _id=updated_role.get("_id"),
                name=updated_role.get("name"),
                description=updated_role.get("description"),
                permissions=updated_role.get("permissions"),
                creation_date=updated_role.get("creation_date"),
                mod_date=updated_role.get("mod_date"),
                is_active=updated_role.get("is_active"),
                default_role=updated_role.get("default_role"),
                screens=updated_role.get("screens"),
                app=updated_role.get("app"),
                app_client_id=updated_role.get("app_client_id")
            )
        except Exception as ex:
            logging.exception(ex)
            raise Exception("Failed to add screens: " + str(ex))

    

    @classmethod
    def delete_by_name_and_client_id(cls, role_name, client_id):
        try:
            result = __dbmanager__.collection.delete_one({
                "name": role_name,
                "app_client_id": client_id
            })
            return result.deleted_count > 0
        except Exception as e:
            logging.exception(e)
            raise Exception(f"Error deleting role: {str(e)}")
    
    #para obtener el rol por nombre y idapp
    @classmethod
    def get_by_name_and_client_id(cls, name, client_id):
        try:
            result = __dbmanager__.find_one({"name": name, "app_client_id": client_id})
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
                    app=result.get("app"),
                    app_client_id=result.get("app_client_id")
                )
            return None
        except Exception as ex:
            logging.exception(ex)
            raise Exception("Failed to get role by name and client_id: " + str(ex))

