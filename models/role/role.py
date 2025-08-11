from models.role.db_queries import db_find_active_and_default_roles
import logging
from models.role.db_queries import __dbmanager__
from bson.objectid import ObjectId
from datetime import datetime

class RoleModel:
    def __init__(self, name, description, permissions, creation_date, mod_date, is_active, screens, admin_id, _id=None):
        self.name = name
        self.description = description
        self.permissions = permissions
        self.creation_date = creation_date
        self.mod_date = mod_date
        self.is_active = is_active
        self.screens = screens
        self.admin_id = admin_id
        self._id = _id

    def to_dict(self):
        return {
            "_id": str(self._id) if self._id else None,
            "name": self.name,
            "description": self.description,
            "permissions": self.permissions,
            "creation_date": self.creation_date,
            "mod_date": self.mod_date,
            "is_active": self.is_active,
            "screens": self.screens,
            "admin_id": self.admin_id
        }

    @classmethod
    def create(cls, role_data):
        try:
            result = __dbmanager__.create_data(role_data)
            if result.inserted_id:
                instance = cls(
                    name=role_data["name"],
                    description=role_data["description"],
                    permissions=role_data["permissions"],
                    creation_date=role_data["creation_date"],
                    mod_date=role_data["mod_date"],
                    is_active=role_data["is_active"],
                    screens=role_data["screens"],
                    admin_id=role_data["admin_id"]
                )
                instance._id = str(result.inserted_id)
                return instance
            return None
        except Exception as ex:
            logging.exception(ex)
            raise Exception("Error creating role: " + str(ex))

    @classmethod
    def get_by_name_and_app_id(cls, name, admin_id):
        try:
            result = __dbmanager__.find_one({
                "name": name,
                "admin_id": admin_id
            })
            if result:
                instance = cls(
                    name=result["name"],
                    description=result["description"],
                    permissions=result["permissions"],
                    creation_date=result["creation_date"],
                    mod_date=result["mod_date"],
                    is_active=result["is_active"],
                    screens=result["screens"],
                    admin_id=result["admin_id"]
                )
                instance._id = str(result["_id"])
                return instance
            return None
        except Exception as ex:
            logging.exception(ex)
            raise Exception("Failed to get role by name and admin_id: " + str(ex))

    @classmethod
    def get_by_id_and_app_id(cls, role_id, admin_id):
        try:
            result = __dbmanager__.find_one({
                "_id": ObjectId(role_id),
                "admin_id": admin_id
            })
            if result:
                instance = cls(
                    name=result["name"],
                    description=result["description"],
                    permissions=result["permissions"],
                    creation_date=result["creation_date"],
                    mod_date=result["mod_date"],
                    is_active=result["is_active"],
                    screens=result["screens"],
                    admin_id=result["admin_id"]
                )
                instance._id = str(result["_id"])
                return instance
            return None
        except Exception as ex:
            logging.exception(ex)
            raise Exception("Failed to get role by ID and admin_id: " + str(ex))

    @classmethod
    def update_by_id(cls, role_id, admin_id, update_data):
        try:
            if "mod_date" not in update_data:
                update_data["mod_date"] = datetime.utcnow()

            result = __dbmanager__.update_by_condition(
                {"_id": ObjectId(role_id), "admin_id": admin_id},
                update_data  
            )

            if result:
                updated = __dbmanager__.find_one({"_id": ObjectId(role_id)})
                if updated:
                    instance = cls(
                        name=updated["name"],
                        description=updated["description"],
                        permissions=updated["permissions"],
                        creation_date=updated["creation_date"],
                        mod_date=updated["mod_date"],
                        is_active=updated["is_active"],
                        screens=updated["screens"],
                        admin_id=updated["admin_id"]
                    )
                    instance._id = str(updated["_id"])
                    return instance
                return None
            return None
        except Exception as ex:
            logging.exception(ex)
            raise Exception("Failed to update role: " + str(ex))

    @classmethod
    def update_by_name_and_client_id(cls, role_name, admin_id, update_data):
        try:
            result = __dbmanager__.update_by_condition(
                {"name": role_name, "admin_id": admin_id},
                update_data
            )
            if result.modified_count > 0:
                updated = __dbmanager__.find_one({"name": role_name, "admin_id": admin_id})
                if updated:
                    instance = cls(
                        name=updated["name"],
                        description=updated["description"],
                        permissions=updated["permissions"],
                        creation_date=updated["creation_date"],
                        mod_date=updated["mod_date"],
                        is_active=updated["is_active"],
                        screens=updated["screens"],
                        admin_id=updated["admin_id"]
                    )
                    instance._id = str(updated["_id"])
                    return instance
            return None
        except Exception as ex:
            logging.exception(ex)
            raise Exception("Failed to update role: " + str(ex))


    @classmethod
    def find_by_admin_id(cls, admin_id):
        try:
            print(f"Searching for roles with admin_id: {admin_id}")
            result = __dbmanager__.find_one({"admin_id": admin_id})
            print(f"Result found: {result}")
            if result:
                instance = cls(
                    name=result["name"],
                    description=result["description"],
                    permissions=result["permissions"],
                    creation_date=result["creation_date"],
                    mod_date=result["mod_date"],
                    is_active=result["is_active"],
                    screens=result["screens"],
                    admin_id=result["admin_id"]
                )
                instance._id = str(result["_id"])
                return instance
            return None
        except Exception as e:
            logging.exception(e)
            return None