from bson.objectid import ObjectId
from datetime import datetime
import logging
from models.role.db_queries import __dbmanager__  # tu conexión / collection

class RoleModel:
    def __init__(self, name, description=None, permissions=None,
                 creation_date=None, mod_date=None, is_active=True,
                 screens=None, app_id=None, default_role=False, _id=None):
        # Asegurar valores por defecto
        self.name = name
        self.description = description or ""
        self.permissions = permissions or []
        self.creation_date = creation_date or datetime.utcnow()
        self.mod_date = mod_date or self.creation_date
        self.is_active = True if is_active is None else is_active
        self.screens = screens or []
        # mantener app_id como ObjectId internamente
        self.app_id = ObjectId(app_id) if app_id and not isinstance(app_id, ObjectId) else app_id
        self.default_role = default_role
        # almacenar _id como ObjectId o None
        self._id = ObjectId(_id) if _id and not isinstance(_id, ObjectId) else _id

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
            "app_id": str(self.app_id) if self.app_id else None,
            "default_role": self.default_role
        }

    # ---------- Helpers DB ----------
    @staticmethod
    def _doc_to_instance(doc):
        if not doc:
            return None
        return RoleModel(
            name=doc.get("name"),
            description=doc.get("description", ""),
            permissions=doc.get("permissions", []),
            creation_date=doc.get("creation_date"),
            mod_date=doc.get("mod_date"),
            is_active=doc.get("is_active", True),
            screens=doc.get("screens", []),
            app_id=doc.get("app_id"),
            default_role=doc.get("default_role", False),
            _id=doc.get("_id")
        )

    # ---------- CRUD ----------
    @classmethod
    def create(cls, role_data: dict):
        try:
          
            if "role_name" in role_data and "name" not in role_data:
                role_data["name"] = role_data.pop("role_name")

           
            role_data.setdefault("creation_date", datetime.utcnow())
            role_data.setdefault("mod_date", role_data["creation_date"])
            role_data.setdefault("is_active", True)
            role_data.setdefault("screens", [])
            role_data.setdefault("permissions", [])
            role_data.setdefault("default_role", False)

            # app_id => ObjectId
            if "app_id" in role_data and role_data["app_id"] is not None and not isinstance(role_data["app_id"], ObjectId):
                role_data["app_id"] = ObjectId(role_data["app_id"])

            res = __dbmanager__.collection.insert_one(role_data)
            if not res.inserted_id:
                return None
            new_doc = __dbmanager__.collection.find_one({"_id": res.inserted_id})
            return cls._doc_to_instance(new_doc)
        except Exception as ex:
            logging.exception("RoleModel.create error")
            raise

    @classmethod
    def get_by_name_and_app_id(cls, name, app_id):
        try:
            query = {"name": name}
            if app_id:
                query["app_id"] = ObjectId(app_id) if not isinstance(app_id, ObjectId) else app_id
            doc = __dbmanager__.collection.find_one(query)
            return cls._doc_to_instance(doc)
        except Exception as ex:
            logging.exception("RoleModel.get_by_name_and_app_id error")
            raise

    @classmethod
    def get_by_id_and_app_id(cls, role_id, app_id):
        try:
            query = {"_id": ObjectId(role_id)}
            if app_id:
                query["app_id"] = ObjectId(app_id) if not isinstance(app_id, ObjectId) else app_id
            doc = __dbmanager__.collection.find_one(query)
            return cls._doc_to_instance(doc)
        except Exception as ex:
            logging.exception("RoleModel.get_by_id_and_app_id error")
            raise

    @classmethod
    def update_by_name_and_app_id(cls, role_name, app_id, update_data):
        try:
            result = __dbmanager__.collection.update_one(
                {"name": role_name, "app_id": ObjectId(app_id)},
                {"$set": update_data}
            )
            if result.matched_count == 0:
                return None
            # Traer el documento actualizado
            updated_doc = __dbmanager__.collection.find_one({"name": update_data.get("name", role_name),
                                                            "app_id": ObjectId(app_id)})
            if updated_doc:
                return cls(
                    name=updated_doc["name"],
                    description=updated_doc.get("description", ""),
                    permissions=updated_doc.get("permissions", []),
                    creation_date=updated_doc.get("creation_date"),
                    mod_date=updated_doc.get("mod_date"),
                    is_active=updated_doc.get("is_active", True),
                    screens=updated_doc.get("screens", []),
                    app_id=updated_doc.get("app_id"),
                    _id=updated_doc.get("_id")
                )
            return None
        except Exception as ex:
            logging.exception(ex)
            return None



    @classmethod
    def update_by_id(cls, role_id, app_id, update_data: dict):
        try:
            if "mod_date" not in update_data:
                update_data["mod_date"] = datetime.utcnow()

            filter_q = {"_id": ObjectId(role_id)}
            if app_id:
                filter_q["app_id"] = ObjectId(app_id) if not isinstance(app_id, ObjectId) else app_id
            res = __dbmanager__.collection.update_one(filter_q, {"$set": update_data})
            if res.matched_count == 0:
                return None
            doc = __dbmanager__.collection.find_one(filter_q)
            return cls._doc_to_instance(doc)
        except Exception as ex:
            logging.exception("RoleModel.update_by_id error")
            raise

    @classmethod
    def list_by_app_id(cls, app_id):
        try:
            q = {"app_id": ObjectId(app_id) if not isinstance(app_id, ObjectId) else app_id}
            docs = list(__dbmanager__.collection.find(q))
            return [cls._doc_to_instance(d) for d in docs]
        except Exception as ex:
            logging.exception("RoleModel.list_by_app_id error")
            raise

    @classmethod
    def delete_by_name_and_app_id(cls, role_name, app_id):
        """
        Soft delete: set is_active = False
        """
        try:
            filter_q = {"name": role_name, "app_id": ObjectId(app_id) if not isinstance(app_id, ObjectId) else app_id}
            res = __dbmanager__.collection.update_one(filter_q, {"$set": {"is_active": False, "mod_date": datetime.utcnow()}})
            if res.matched_count == 0:
                return None
            doc = __dbmanager__.collection.find_one(filter_q)
            return cls._doc_to_instance(doc)
        except Exception as ex:
            logging.exception("RoleModel.delete_by_name_and_app_id error")
            raise
