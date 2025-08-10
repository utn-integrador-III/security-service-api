from flask_restful import Resource
from flask import request
from bson.objectid import ObjectId
from datetime import datetime
from utils.server_response import ServerResponse, StatusCode
import logging
from db.mongo_client import Connection


class AppController(Resource):
    route = "/apps"

    """
    CRUD para "apps" respetando únicamente los campos:
    - name
    - redirect_url
    - creation_date
    - status
    - admin_id
    """

    def get(self, app_id=None):
        try:
            conn = Connection('apps')
            if app_id:
                if not ObjectId.is_valid(app_id):
                    return ServerResponse(
                        message="Invalid app_id",
                        message_code="INVALID_ID",
                        status=StatusCode.UNPROCESSABLE_ENTITY,
                    ).to_response()

                app = conn.get_by_id(app_id)
                if not app:
                    return ServerResponse(
                        message="App not found",
                        message_code="APP_NOT_FOUND",
                        status=StatusCode.NOT_FOUND,
                    ).to_response()

                app_obj = self._to_public(app)
                return ServerResponse(
                    data=app_obj,
                    message="APP_FOUND",
                    message_code="OK_MSG",
                    status=StatusCode.OK,
                ).to_response()
            cursor = conn.get_all_data()
            apps = [self._to_public(a) for a in cursor] if cursor else []
            return ServerResponse(
                data=apps,
                message="APPS_FOUND" if apps else "NO_DATA",
                message_code="OK_MSG",
                status=StatusCode.OK,
            ).to_response()
        except Exception as ex:
            logging.error(ex, exc_info=True)
            return ServerResponse(status=StatusCode.INTERNAL_SERVER_ERROR).to_response()

    def post(self):
        try:
            data = request.get_json(silent=True) or {}
            name = (data.get("name") or "").strip()
            redirect_url = (data.get("redirect_url") or "").strip()
            admin_id = (data.get("admin_id") or "").strip()

            if not name or len(name) < 2:
                return ServerResponse(
                    message="Invalid name",
                    message_code="INVALID_NAME",
                    status=StatusCode.UNPROCESSABLE_ENTITY,
                ).to_response()

            if not redirect_url:
                return ServerResponse(
                    message="redirect_url is required",
                    message_code="INVALID_REDIRECT_URL",
                    status=StatusCode.UNPROCESSABLE_ENTITY,
                ).to_response()

            if not admin_id or not ObjectId.is_valid(admin_id):
                return ServerResponse(
                    message="Invalid admin_id",
                    message_code="INVALID_ADMIN_ID",
                    status=StatusCode.UNPROCESSABLE_ENTITY,
                ).to_response()

            new_app = {
                "name": name,
                "redirect_url": redirect_url,
                "creation_date": datetime.utcnow(),
                "status": "active",
                "admin_id": ObjectId(admin_id),
            }

            conn = Connection('apps')
            result = conn.create_data(new_app)
            return ServerResponse(
                data={"app_id": str(result.inserted_id)},
                message="App created successfully",
                message_code="CREATED",
                status=StatusCode.CREATED,
            ).to_response()
        except Exception as ex:
            logging.error(ex, exc_info=True)
            return ServerResponse(status=StatusCode.INTERNAL_SERVER_ERROR).to_response()

    def put(self, app_id):
        try:
            if not ObjectId.is_valid(app_id):
                return ServerResponse(
                    message="Invalid app_id",
                    message_code="INVALID_ID",
                    status=StatusCode.UNPROCESSABLE_ENTITY,
                ).to_response()

            data = request.get_json(silent=True) or {}
            update_data = {}

            if "name" in data and data["name"] is not None:
                name = str(data["name"]).strip()
                if not name or len(name) < 2:
                    return ServerResponse(
                        message="Invalid name",
                        message_code="INVALID_NAME",
                        status=StatusCode.UNPROCESSABLE_ENTITY,
                    ).to_response()
                update_data["name"] = name

            if "redirect_url" in data and data["redirect_url"] is not None:
                redirect_url = str(data["redirect_url"]).strip()
                if not redirect_url:
                    return ServerResponse(
                        message="Invalid redirect_url",
                        message_code="INVALID_REDIRECT_URL",
                        status=StatusCode.UNPROCESSABLE_ENTITY,
                    ).to_response()
                update_data["redirect_url"] = redirect_url

            if "status" in data and data["status"] is not None:
                status_val = str(data["status"]).strip()
                if status_val not in ("active", "inactive"):
                    return ServerResponse(
                        message="Invalid status",
                        message_code="INVALID_STATUS",
                        status=StatusCode.UNPROCESSABLE_ENTITY,
                    ).to_response()
                update_data["status"] = status_val

            if "admin_id" in data and data["admin_id"] is not None:
                admin_id = str(data["admin_id"]).strip()
                if not ObjectId.is_valid(admin_id):
                    return ServerResponse(
                        message="Invalid admin_id",
                        message_code="INVALID_ADMIN_ID",
                        status=StatusCode.UNPROCESSABLE_ENTITY,
                    ).to_response()
                update_data["admin_id"] = ObjectId(admin_id)

            if not update_data:
                return ServerResponse(
                    message="No update data provided",
                    message_code="NO_DATA",
                    status=StatusCode.UNPROCESSABLE_ENTITY,
                ).to_response()

            conn = Connection('apps')
            updated = conn.update_by_id(app_id, update_data)
            if not updated:
                return ServerResponse(
                    message="App not found",
                    message_code="APP_NOT_FOUND",
                    status=StatusCode.NOT_FOUND,
                ).to_response()

            return ServerResponse(
                message="App updated successfully",
                message_code="UPDATED",
                status=StatusCode.OK,
            ).to_response()
        except Exception as ex:
            logging.error(ex, exc_info=True)
            return ServerResponse(status=StatusCode.INTERNAL_SERVER_ERROR).to_response()

    def delete(self, app_id):
        try:
            if not ObjectId.is_valid(app_id):
                return ServerResponse(
                    message="Invalid app_id",
                    message_code="INVALID_ID",
                    status=StatusCode.UNPROCESSABLE_ENTITY,
                ).to_response()

            conn = Connection('apps')
            deleted = conn.delete_data(app_id)
            if not deleted:
                return ServerResponse(
                    message="App not found",
                    message_code="APP_NOT_FOUND",
                    status=StatusCode.NOT_FOUND,
                ).to_response()

            return ServerResponse(
                message="App deleted successfully",
                message_code="DELETED",
                status=StatusCode.OK,
            ).to_response()
        except Exception as ex:
            logging.error(ex, exc_info=True)
            return ServerResponse(status=StatusCode.INTERNAL_SERVER_ERROR).to_response()

    @staticmethod
    def _to_public(doc: dict) -> dict:
        creation = doc.get("creation_date")
        try:
            creation_serialized = creation.isoformat() if hasattr(creation, "isoformat") else creation
        except Exception:
            creation_serialized = str(creation) if creation is not None else None
        return {
            "_id": str(doc.get("_id")),
            "name": doc.get("name"),
            "redirect_url": doc.get("redirect_url"),
            "creation_date": creation_serialized,
            "status": doc.get("status"),
            "admin_id": str(doc.get("admin_id")) if doc.get("admin_id") else None,
        }
