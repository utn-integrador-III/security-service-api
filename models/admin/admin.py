import logging
from datetime import datetime
from bson import ObjectId
import bcrypt
from models.admin.db_queries import get_by_email, create_admin, list_admins, get_by_id, update_by_id

class AdminModel:
    def __init__(self, admin_email, password_secret, status="active", creation_date=None, _id=None):
        self.admin_email = admin_email
        self.password_secret = password_secret
        self.status = status
        self.creation_date = creation_date or datetime.utcnow()
        self._id = _id

    def to_dict(self):
        return {
            "_id": str(self._id) if self._id else None,
            "admin_email": self.admin_email,
            "status": self.status,
            "creation_date": self.creation_date
        }

    @staticmethod
    def create(email: str, raw_password: str, status: str = "active"):
        # email único
        if get_by_email(email):
            raise ValueError("admin_email already exists")

        hashed = bcrypt.hashpw(raw_password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
        doc = {
            "admin_email": email.lower().strip(),
            "password_secret": hashed,
            "status": status,
            "creation_date": datetime.utcnow()
        }
        res = create_admin(doc)
        if not res:
            raise RuntimeError("Failed to create admin")
        new_doc = get_by_id(str(res.inserted_id))
        return AdminModel._sanitize(new_doc)

    @staticmethod
    def list(status: str | None = None):
        q = {}
        if status:
            q["status"] = status
        return [AdminModel._sanitize(d) for d in list_admins(q)]

    @staticmethod
    def get(id: str):
        return AdminModel._sanitize(get_by_id(id))

    @staticmethod
    def update(id: str, status: str | None = None, new_password: str | None = None):
        update = {}
        if status:
            update["status"] = status
        if new_password:
            update["password_secret"] = bcrypt.hashpw(new_password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
        if not update:
            return None
        result = update_by_id(id, update)
        if result is None or result.matched_count == 0:
            return None
        return AdminModel._sanitize(get_by_id(id))

    @staticmethod
    def soft_delete(id: str):
        result = update_by_id(id, {"status": "inactive", "deleted_at": datetime.utcnow()})
        if result is None or result.matched_count == 0:
            return None
        return AdminModel._sanitize(get_by_id(id))

    @staticmethod
    def _sanitize(doc):
        if not doc or isinstance(doc, Exception):
            return None
        doc["_id"] = str(doc["_id"])
        doc.pop("password_secret", None)
        return doc
