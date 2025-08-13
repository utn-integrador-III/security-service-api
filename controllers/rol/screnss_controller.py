from flask_restful import Resource
from flask import request
from utils.server_response import ServerResponse, StatusCode
from models.role.role import RoleModel
from models.apps.app import AppModel
import logging
from datetime import datetime

class ScreensController(Resource):
    # POST: Agregar screens a un rol existente
    @staticmethod
    def post_add_screens(app_id):
        try:
            data = request.get_json()
            role_name = data.get("role_name")
            new_screens = data.get("screens", [])

            if not role_name:
                return ServerResponse(
                    message="Role name is required",
                    message_code="INVALID_ROLE_NAME",
                    status=StatusCode.UNPROCESSABLE_ENTITY
                ).to_response()

            if not isinstance(new_screens, list):
                return ServerResponse(
                    message="Screens must be a list",
                    message_code="INVALID_SCREENS_FORMAT",
                    status=StatusCode.UNPROCESSABLE_ENTITY
                ).to_response()

            # Buscar el rol por nombre y app_id (ya no admin_id)
            role = RoleModel.get_by_name_and_app_id(role_name, app_id)
            if not role:
                return ServerResponse(
                    message="Role not found for this application",
                    message_code="ROLE_OR_APP_NOT_FOUND",
                    status=StatusCode.NOT_FOUND
                ).to_response()

            # Evitar duplicados
            existing_screens = set(role.screens or [])
            screens_to_add = set(new_screens) - existing_screens

            if not screens_to_add:
                return ServerResponse(
                    message="Screens already exist",
                    message_code="DUPLICATE_SCREENS",
                    status=StatusCode.CONFLICT
                ).to_response()

            updated_screens = list(existing_screens.union(screens_to_add))

            updated_role = RoleModel.update_by_name_and_app_id(
                role_name,
                app_id,
                {
                    "screens": updated_screens,
                    "mod_date": datetime.utcnow()
                }
            )

            if not updated_role:
                return ServerResponse(
                    message="Failed to update role screens",
                    message_code="UPDATE_FAILED",
                    status=StatusCode.INTERNAL_SERVER_ERROR
                ).to_response()

            return ServerResponse(
                data=updated_role.to_dict(),
                message="Screens added successfully",
                message_code="SCREENS_ADDED",
                status=StatusCode.OK
            ).to_response()

        except Exception as e:
            logging.error(f"Error adding screens: {str(e)}", exc_info=True)
            return ServerResponse(
                message="Internal server error",
                message_code="INTERNAL_SERVER_ERROR",
                status=StatusCode.INTERNAL_SERVER_ERROR
            ).to_response()

    # DELETE: Quitar screens de un rol existente
    @staticmethod
    def delete_screens(app_id):
        try:
            data = request.get_json()
            role_name = data.get("role_name")
            screens_to_remove = data.get("screens", [])

            if not role_name:
                return ServerResponse(
                    message="Role name is required",
                    message_code="INVALID_ROLE_NAME",
                    status=StatusCode.UNPROCESSABLE_ENTITY
                ).to_response()

            if not isinstance(screens_to_remove, list):
                return ServerResponse(
                    message="Screens must be a list",
                    message_code="INVALID_SCREENS_FORMAT",
                    status=StatusCode.UNPROCESSABLE_ENTITY
                ).to_response()

            # Buscar el rol por nombre y app_id
            role = RoleModel.get_by_name_and_app_id(role_name, app_id)
            if not role:
                return ServerResponse(
                    message="Role not found for this application",
                    message_code="ROLE_OR_APP_NOT_FOUND",
                    status=StatusCode.NOT_FOUND
                ).to_response()

            existing_screens = set(role.screens or [])
            screens_to_remove_set = set(screens_to_remove)

            # Validar si hay algo para eliminar
            if not existing_screens.intersection(screens_to_remove_set):
                return ServerResponse(
                    message="No matching screens to remove",
                    message_code="NO_MATCHING_SCREENS",
                    status=StatusCode.NOT_FOUND
                ).to_response()

            # Quitar las indicadas
            updated_screens = list(existing_screens - screens_to_remove_set)

            updated_role = RoleModel.update_by_name_and_app_id(
                role_name,
                app_id,
                {
                    "screens": updated_screens,
                    "mod_date": datetime.utcnow()
                }
            )

            if not updated_role:
                return ServerResponse(
                    message="Failed to update role screens",
                    message_code="UPDATE_FAILED",
                    status=StatusCode.INTERNAL_SERVER_ERROR
                ).to_response()

            return ServerResponse(
                data=updated_role.to_dict(),
                message="Screens removed successfully",
                message_code="SCREENS_REMOVED",
                status=StatusCode.OK
            ).to_response()

        except Exception as e:
            logging.error(f"Error removing screens: {str(e)}", exc_info=True)
            return ServerResponse(
                message="Internal server error",
                message_code="INTERNAL_SERVER_ERROR",
                status=StatusCode.INTERNAL_SERVER_ERROR
            ).to_response()
    

    @staticmethod
    def get_screens(app_id):
        """
        GET /role/<app_id>/screens
        body: { "role_name": "Cliente" }
        Obtiene las pantallas asociadas a un rol específico por su nombre.
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

            # Verificar que la app exista
            app = AppModel.get(app_id)
            if not app:
                return ServerResponse(
                    message="App not found",
                    message_code="APP_NOT_FOUND",
                    status=StatusCode.NOT_FOUND
                ).to_response()

            # Obtener el rol por nombre y app_id
            role = RoleModel.get_by_name_and_app_id(role_name, app_id)
            if not role:
                return ServerResponse(
                    message="Role not found",
                    message_code="ROLE_NOT_FOUND",
                    status=StatusCode.NOT_FOUND
                ).to_response()

            return ServerResponse(
                data={"role_name": role.name, "screens": role.screens},
                message="Screens fetched successfully",
                message_code="SCREENS_FETCHED",
                status=StatusCode.OK
            ).to_response()

        except Exception as e:
            logging.exception("Error fetching screens for role")
            return ServerResponse(
                message="Internal server error",
                message_code="INTERNAL_SERVER_ERROR",
                status=StatusCode.INTERNAL_SERVER_ERROR
            ).to_response()

