from flask import request
from flask_restful import Resource
from utils.server_response import ServerResponse, StatusCode
from models.role.role import RoleModel
from models.apps.app import AppModel
from datetime import datetime
import logging

class RolController(Resource):
    route = '/role/<string:app_id>'

    @staticmethod
    def post(app_id):
        """
        POST /role/<app_id>  -> crea rol
        body: { "name": "...", "description": "...", "permissions":[...] }
        """
        try:
            data = request.get_json(force=True, silent=True) or {}
            name = data.get("name")
            description = data.get("description", "")
            permissions = data.get("permissions", [])

            if not name or len(name.strip()) < 2:
                return ServerResponse(
                    message="Invalid 'name'",
                    message_code="INVALID_NAME",
                    status=StatusCode.UNPROCESSABLE_ENTITY
                ).to_response()

            if not isinstance(permissions, list):
                return ServerResponse(
                    message="'permissions' must be a list",
                    message_code="INVALID_PERMISSIONS_FORMAT",
                    status=StatusCode.UNPROCESSABLE_ENTITY
                ).to_response()

            # verificar app
            app = AppModel.get(app_id)
            if not app:
                return ServerResponse(
                    message="App not found",
                    message_code="APP_NOT_FOUND",
                    status=StatusCode.NOT_FOUND
                ).to_response()

            # duplicado por name + app_id
            existing = RoleModel.get_by_name_and_app_id(name.strip(), app_id)
            if existing:
                return ServerResponse(
                    message="Role already exists for this application",
                    message_code="ROLE_ALREADY_EXISTS",
                    status=StatusCode.CONFLICT
                ).to_response()

            role_data = {
                "name": name.strip(),
                "description": description or "",
                "permissions": permissions,
                "app_id": app_id,
                "creation_date": datetime.utcnow()
               
            }

            created = RoleModel.create(role_data)
            if not created:
                return ServerResponse(
                    message="Failed to create role",
                    message_code="ROLE_CREATION_FAILED",
                    status=StatusCode.INTERNAL_SERVER_ERROR
                ).to_response()

            return ServerResponse(
                data=created.to_dict(),
                message="Role created successfully",
                message_code="ROLE_CREATED",
                status=StatusCode.CREATED
            ).to_response()

        except Exception as e:
            logging.exception("Error in post role")
            return ServerResponse(
                message="Internal server error",
                message_code="INTERNAL_SERVER_ERROR",
                status=StatusCode.INTERNAL_SERVER_ERROR
            ).to_response()

    @staticmethod
    def get(app_id):
        """
        GET /role/<app_id>  -> lista roles de la app
        """
        try:
            app = AppModel.get(app_id)
            if not app:
                return ServerResponse(
                    message="App not found",
                    message_code="APP_NOT_FOUND",
                    status=StatusCode.NOT_FOUND
                ).to_response()

            roles = RoleModel.list_by_app_id(app_id)
            data = [r.to_dict() for r in roles]
            return ServerResponse(
                data=data,
                message="Roles retrieved successfully",
                message_code="ROLES_RETRIEVED",
                status=StatusCode.OK
            ).to_response()

        except Exception as e:
            logging.exception("Error in get roles")
            return ServerResponse(
                message="Internal server error",
                message_code="INTERNAL_SERVER_ERROR",
                status=StatusCode.INTERNAL_SERVER_ERROR
            ).to_response()

    @staticmethod
    def patch(app_id):
        """
        PATCH /role/<app_id> -> actualizar por nombre
        body: { "role_name": "actual", "name": "nuevo", "description": "...", "permissions": [...] }
        """
        try:
            data = request.get_json(force=True, silent=True) or {}
            role_name = data.get("role_name")  # rol actual que se quiere actualizar
            if not role_name or len(role_name.strip()) < 2:
                return ServerResponse(
                    message="role_name required in JSON body",
                    message_code="INVALID_ROLE_NAME",
                    status=StatusCode.UNPROCESSABLE_ENTITY
                ).to_response()

            new_name = data.get("name")
            description = data.get("description")
            permissions = data.get("permissions")

            if new_name and len(new_name.strip()) < 2:
                return ServerResponse(
                    message="Invalid 'name'",
                    message_code="INVALID_NAME",
                    status=StatusCode.UNPROCESSABLE_ENTITY
                ).to_response()

            if permissions is not None and not isinstance(permissions, list):
                return ServerResponse(
                    message="'permissions' must be a list",
                    message_code="INVALID_PERMISSIONS_FORMAT",
                    status=StatusCode.UNPROCESSABLE_ENTITY
                ).to_response()

            # Verificar que la app exista
            app = AppModel.get(app_id)
            if not app:
                return ServerResponse(
                    message="App not found",
                    message_code="APP_NOT_FOUND",
                    status=StatusCode.NOT_FOUND
                ).to_response()

            # Buscar el rol actual por nombre y app_id
            role = RoleModel.get_by_name_and_app_id(role_name.strip(), app_id)
            if not role:
                return ServerResponse(
                    message="Role not found",
                    message_code="ROLE_NOT_FOUND",
                    status=StatusCode.NOT_FOUND
                ).to_response()

            # Evitar duplicar nombre si se cambia
            if new_name and new_name.strip().lower() != role.name.lower():
                other = RoleModel.get_by_name_and_app_id(new_name.strip(), app_id)
                if other:
                    return ServerResponse(
                        message="Role name already exists",
                        message_code="DUPLICATE_ROLE",
                        status=StatusCode.CONFLICT
                    ).to_response()

            update_data = {}
            if new_name:
                update_data["name"] = new_name.strip()
            if description is not None:
                update_data["description"] = description
            if permissions is not None:
                update_data["permissions"] = permissions

            updated = RoleModel.update_by_name_and_app_id(role_name.strip(), app_id, update_data)
            if not updated:
                return ServerResponse(
                    message="Failed to update role",
                    message_code="ROLE_UPDATE_FAILED",
                    status=StatusCode.INTERNAL_SERVER_ERROR
                ).to_response()

            # Manejar correctamente si updated es diccionario o instancia
            role_data = updated
            if hasattr(updated, "to_dict"):
                role_data = updated.to_dict()

            return ServerResponse(
                data=role_data,
                message="Role updated successfully",
                message_code="ROLE_UPDATED",
                status=StatusCode.OK
            ).to_response()

        except Exception as e:
            logging.exception("Error in patch role")
            return ServerResponse(
                message="Internal server error",
                message_code="INTERNAL_SERVER_ERROR",
                status=StatusCode.INTERNAL_SERVER_ERROR
            ).to_response()



    @staticmethod
    def delete(app_id):
        """
        DELETE /role/<app_id>  -> soft delete por nombre desde JSON
        body: { "role_name": "NombreDelRol" }
        """
        try:
            data = request.get_json(force=True, silent=True) or {}
            role_name = data.get("role_name")
            if not role_name:
                return ServerResponse(
                    message="role_name required in JSON body",
                    message_code="INVALID_ROLE_NAME",
                    status=StatusCode.UNPROCESSABLE_ENTITY
                ).to_response()

            app = AppModel.get(app_id)
            if not app:
                return ServerResponse(
                    message="App not found",
                    message_code="APP_NOT_FOUND",
                    status=StatusCode.NOT_FOUND
                ).to_response()

            deleted = RoleModel.delete_by_name_and_app_id(role_name, app_id)
            if not deleted:
                return ServerResponse(
                    message="Role not found",
                    message_code="ROLE_NOT_FOUND",
                    status=StatusCode.NOT_FOUND
                ).to_response()

            return ServerResponse(
                data=deleted.to_dict(),
                message="Role deactivated successfully",
                message_code="ROLE_DEACTIVATED",
                status=StatusCode.OK
            ).to_response()

        except Exception as e:
            logging.exception("Error in delete role")
            return ServerResponse(
                message="Internal server error",
                message_code="INTERNAL_SERVER_ERROR",
                status=StatusCode.INTERNAL_SERVER_ERROR
            ).to_response()
