# models/apps/app.py
from datetime import datetime
from urllib.parse import urlparse
from bson import ObjectId
from models.apps.db_queries import get_by_name, create_app, list_apps, get_by_id, update_by_id

def _is_valid_url(url: str) -> bool:
    u = urlparse(url or "")
    return u.scheme in ('http', 'https') and bool(u.netloc)

class AppModel:
    def __init__(self, name, redirect_url, status="active", admin_id=None, creation_date=None, _id=None):
        self.name = name
        self.redirect_url = redirect_url
        self.status = status
        self.admin_id = admin_id
        self.creation_date = creation_date or datetime.utcnow()
        self._id = _id

    def to_dict(self):
        return {
            "_id": str(self._id) if self._id else None,
            "name": self.name,
            "redirect_url": self.redirect_url,
            "status": self.status,
            "admin_id": str(self.admin_id) if isinstance(self.admin_id, ObjectId) else self.admin_id,
            "creation_date": self.creation_date
        }

    @staticmethod
    def create(name: str, redirect_url: str, status: str = "active", admin_id: str | None = None):
        if get_by_name((name or "").strip()):
            raise ValueError("App name already exists")
        if not name or len(name.strip()) < 2:
            raise ValueError("Invalid 'name'")
        if not _is_valid_url(redirect_url):
            raise ValueError("Invalid 'redirect_url'")
        if status not in ('active', 'inactive'):
            raise ValueError("Invalid 'status'")

        admin_oid = None
        if admin_id:
            try:
                admin_oid = ObjectId(admin_id)   
            except Exception:
                raise ValueError("Invalid 'admin_id'")

        doc = {
            "name": name.strip(),
            "redirect_url": redirect_url.strip(),
            "status": status,
            "admin_id": admin_oid,
            "creation_date": datetime.utcnow()
        }
        res = create_app(doc)
        if not res:
            raise RuntimeError("Failed to create app")
        new_doc = get_by_id(str(res.inserted_id))
        return AppModel._sanitize(new_doc)

    @staticmethod
    def list(status: str | None = None):
        q = {}
        if status:
            q["status"] = status
        return [AppModel._sanitize(d) for d in list_apps(q)]

    @staticmethod
    def get(id: str):
        return AppModel._sanitize(get_by_id(id))

    @staticmethod
    def update(id: str, status: str | None = None, redirect_url: str | None = None):
        update = {}
        if status is not None:
            if status not in ('active', 'inactive'):
                raise ValueError("Invalid 'status'")
            update["status"] = status
        if redirect_url is not None:
            if not _is_valid_url(redirect_url):
                raise ValueError("Invalid 'redirect_url'")
            update["redirect_url"] = redirect_url

        if not update:
            return None
        result = update_by_id(id, update)
        if result is None or result.matched_count == 0:
            return None
        return AppModel._sanitize(get_by_id(id))

    @staticmethod
    def soft_delete(id: str):
        result = update_by_id(id, {"status": "inactive", "deleted_at": datetime.utcnow()})
        if result is None or result.matched_count == 0:
            return None
        return AppModel._sanitize(get_by_id(id))

    @staticmethod
    def _sanitize(doc):
        if not doc or isinstance(doc, Exception):
            return None
        doc["_id"] = str(doc["_id"])
 
        if "admin_id" in doc and isinstance(doc["admin_id"], ObjectId):
            doc["admin_id"] = str(doc["admin_id"])
        return doc
