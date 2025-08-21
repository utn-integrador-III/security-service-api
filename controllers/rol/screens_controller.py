from flask_restful import Resource
from flask import request
from utils.server_response import ServerResponse, StatusCode
from models.role.role import RoleModel
from utils.jwt_manager import validate_jwt
import logging

class ScreensController(Resource):
    route = "/rol/screens"

    """
    POST /rol/screens - Asignar screens a un rol
    """
    def post(self):
        try:
            # Validar autenticación
            auth_header = request.headers.get('Authorization')
            if not auth_header or not auth_header.startswith('Bearer '):
                return ServerResponse(
                    message="Authorization header required",
                    message_code="AUTH_REQUIRED",
                    status=StatusCode.UNAUTHORIZED
                ).to_response()

            token = auth_header.split(' ')[1]
            jwt_data = validate_jwt(token)
            if not jwt_data:
                return ServerResponse(
                    message="Invalid or expired token",
                    message_code="INVALID_TOKEN",
                    status=StatusCode.UNAUTHORIZED
                ).to_response()

            admin_id = jwt_data['identity']

            # Obtener datos del request
            data = request.get_json()
            role_id = data.get("role_id")
            app_id = data.get("app_id")
            screen_path = data.get("screen_path")

            # Validar campos requeridos
            if not role_id:
                return ServerResponse(
                    message="Role ID is required",
                    message_code="INVALID_ROLE_ID",
                    status=StatusCode.UNPROCESSABLE_ENTITY
                ).to_response()

            if not app_id:
                return ServerResponse(
                    message="Application ID is required",
                    message_code="INVALID_APP_ID",
                    status=StatusCode.UNPROCESSABLE_ENTITY
                ).to_response()

            if not screen_path:
                return ServerResponse(
                    message="Screen path is required",
                    message_code="INVALID_SCREEN_PATH",
                    status=StatusCode.UNPROCESSABLE_ENTITY
                ).to_response()

            # Buscar el rol por ID
            role = RoleModel.get_by_id(role_id)
            if not role:
                return ServerResponse(
                    message="Role not found",
                    message_code="ROLE_NOT_FOUND",
                    status=StatusCode.NOT_FOUND
                ).to_response()

            # Validar que el admin que creó el rol sea el que lo está modificando
            if role.admin_id != admin_id:
                return ServerResponse(
                    message="You can only modify roles that you created",
                    message_code="UNAUTHORIZED_MODIFY",
                    status=StatusCode.FORBIDDEN
                ).to_response()

            # Validar que el rol pertenezca a la aplicación especificada
            if str(role.app_id) != str(app_id):
                return ServerResponse(
                    message="Role does not belong to the specified application",
                    message_code="ROLE_APP_MISMATCH",
                    status=StatusCode.BAD_REQUEST
                ).to_response()

            # Agregar la screen al rol usando el ID del rol directamente
            updated_role = RoleModel.add_screens_by_role_id(role_id, [screen_path])

            if not updated_role:
                return ServerResponse(
                    message="Failed to add screen to role",
                    message_code="ADD_SCREEN_FAILED",
                    status=StatusCode.INTERNAL_SERVER_ERROR
                ).to_response()
            
            if updated_role == "DUPLICATE":
                return ServerResponse(
                    message="Screen already exists in this role",
                    message_code="DUPLICATE_SCREEN",
                    status=StatusCode.CONFLICT
                ).to_response()

            return ServerResponse(
                data=updated_role.to_dict(),
                message="Screen assigned successfully",
                message_code="SCREEN_ASSIGNED",
                status=StatusCode.OK
            ).to_response()

        except Exception as e:
            logging.error(f"Error assigning screen: {str(e)}", exc_info=True)
            return ServerResponse(
                message="Internal server error",
                message_code="INTERNAL_SERVER_ERROR",
                status=StatusCode.INTERNAL_SERVER_ERROR
            ).to_response()

    """
    GET /rol/screens - Obtener screens de un rol
    """
    def get(self):
        try:
            # Validar autenticación
            auth_header = request.headers.get('Authorization')
            if not auth_header or not auth_header.startswith('Bearer '):
                return ServerResponse(
                    message="Authorization header required",
                    message_code="AUTH_REQUIRED",
                    status=StatusCode.UNAUTHORIZED
                ).to_response()

            token = auth_header.split(' ')[1]
            jwt_data = validate_jwt(token)
            if not jwt_data:
                return ServerResponse(
                    message="Invalid or expired token",
                    message_code="INVALID_TOKEN",
                    status=StatusCode.UNAUTHORIZED
                ).to_response()

            admin_id = jwt_data['identity']

            # Obtener parámetros de query
            role_id = request.args.get('role_id')
            app_id = request.args.get('app_id')

            if not role_id:
                return ServerResponse(
                    message="Role ID is required",
                    message_code="INVALID_ROLE_ID",
                    status=StatusCode.UNPROCESSABLE_ENTITY
                ).to_response()

            if not app_id:
                return ServerResponse(
                    message="Application ID is required",
                    message_code="INVALID_APP_ID",
                    status=StatusCode.UNPROCESSABLE_ENTITY
                ).to_response()

            # Buscar el rol por ID
            role = RoleModel.get_by_id(role_id)
            if not role:
                return ServerResponse(
                    message="Role not found",
                    message_code="ROLE_NOT_FOUND",
                    status=StatusCode.NOT_FOUND
                ).to_response()

            # Validar que el admin que creó el rol sea el que lo está consultando
            if role.admin_id != admin_id:
                return ServerResponse(
                    message="You can only view roles that you created",
                    message_code="UNAUTHORIZED_VIEW",
                    status=StatusCode.FORBIDDEN
                ).to_response()

            # Validar que el rol pertenezca a la aplicación especificada
            if str(role.app_id) != str(app_id):
                return ServerResponse(
                    message="Role does not belong to the specified application",
                    message_code="ROLE_APP_MISMATCH",
                    status=StatusCode.BAD_REQUEST
                ).to_response()

            return ServerResponse(
                data={
                    "role_id": role_id,
                    "app_id": app_id,
                    "screens": role.screens or []
                },
                message="Screens retrieved successfully",
                message_code="SCREENS_RETRIEVED",
                status=StatusCode.OK
            ).to_response()

        except Exception as e:
            logging.error(f"Error getting screens: {str(e)}", exc_info=True)
            return ServerResponse(
                message="Internal server error",
                message_code="INTERNAL_SERVER_ERROR",
                status=StatusCode.INTERNAL_SERVER_ERROR
            ).to_response()

    """
    DELETE /rol/screens - Eliminar screens de un rol
    """
    def delete(self):
        try:
            # Validar autenticación
            auth_header = request.headers.get('Authorization')
            if not auth_header or not auth_header.startswith('Bearer '):
                return ServerResponse(
                    message="Authorization header required",
                    message_code="AUTH_REQUIRED",
                    status=StatusCode.UNAUTHORIZED
                ).to_response()

            token = auth_header.split(' ')[1]
            jwt_data = validate_jwt(token)
            if not jwt_data:
                return ServerResponse(
                    message="Invalid or expired token",
                    message_code="INVALID_TOKEN",
                    status=StatusCode.UNAUTHORIZED
                ).to_response()

            admin_id = jwt_data['identity']

            # Obtener datos del request
            data = request.get_json()
            role_id = data.get("role_id")
            app_id = data.get("app_id")
            screen_path = data.get("screen_path")

            # Validar campos requeridos
            if not role_id:
                return ServerResponse(
                    message="Role ID is required",
                    message_code="INVALID_ROLE_ID",
                    status=StatusCode.UNPROCESSABLE_ENTITY
                ).to_response()

            if not app_id:
                return ServerResponse(
                    message="Application ID is required",
                    message_code="INVALID_APP_ID",
                    status=StatusCode.UNPROCESSABLE_ENTITY
                ).to_response()

            if not screen_path:
                return ServerResponse(
                    message="Screen path is required",
                    message_code="INVALID_SCREEN_PATH",
                    status=StatusCode.UNPROCESSABLE_ENTITY
                ).to_response()

            # Buscar el rol por ID
            role = RoleModel.get_by_id(role_id)
            if not role:
                return ServerResponse(
                    message="Role not found",
                    message_code="ROLE_NOT_FOUND",
                    status=StatusCode.NOT_FOUND
                ).to_response()

            # Validar que el admin que creó el rol sea el que lo está modificando
            if role.admin_id != admin_id:
                return ServerResponse(
                    message="You can only modify roles that you created",
                    message_code="UNAUTHORIZED_MODIFY",
                    status=StatusCode.FORBIDDEN
                ).to_response()

            # Validar que el rol pertenezca a la aplicación especificada
            if str(role.app_id) != str(app_id):
                return ServerResponse(
                    message="Role does not belong to the specified application",
                    message_code="ROLE_APP_MISMATCH",
                    status=StatusCode.BAD_REQUEST
                ).to_response()

            # Eliminar la screen del rol
            updated_role = RoleModel.remove_screen_by_role_id(role_id, screen_path)

            if not updated_role:
                return ServerResponse(
                    message="Failed to remove screen from role",
                    message_code="REMOVE_SCREEN_FAILED",
                    status=StatusCode.INTERNAL_SERVER_ERROR
                ).to_response()
            
            if updated_role == "NOT_FOUND":
                return ServerResponse(
                    message="Screen not found in this role",
                    message_code="SCREEN_NOT_FOUND",
                    status=StatusCode.NOT_FOUND
                ).to_response()

            return ServerResponse(
                data=updated_role.to_dict(),
                message="Screen removed successfully",
                message_code="SCREEN_REMOVED",
                status=StatusCode.OK
            ).to_response()

        except Exception as e:
            logging.error(f"Error removing screen: {str(e)}", exc_info=True)
            return ServerResponse(
                message="Internal server error",
                message_code="INTERNAL_SERVER_ERROR",
                status=StatusCode.INTERNAL_SERVER_ERROR
            ).to_response()

    """
    PATCH /rol/screens - Actualizar/reemplazar screens de un rol
    """
    def patch(self):
        try:
            # Validar autenticación
            auth_header = request.headers.get('Authorization')
            if not auth_header or not auth_header.startswith('Bearer '):
                return ServerResponse(
                    message="Authorization header required",
                    message_code="AUTH_REQUIRED",
                    status=StatusCode.UNAUTHORIZED
                ).to_response()

            token = auth_header.split(' ')[1]
            jwt_data = validate_jwt(token)
            if not jwt_data:
                return ServerResponse(
                    message="Invalid or expired token",
                    message_code="INVALID_TOKEN",
                    status=StatusCode.UNAUTHORIZED
                ).to_response()

            admin_id = jwt_data['identity']

            # Obtener datos del request
            data = request.get_json()
            role_id = data.get("role_id")
            app_id = data.get("app_id")
            screens = data.get("screens")

            # Validar campos requeridos
            if not role_id:
                return ServerResponse(
                    message="Role ID is required",
                    message_code="INVALID_ROLE_ID",
                    status=StatusCode.UNPROCESSABLE_ENTITY
                ).to_response()

            if not app_id:
                return ServerResponse(
                    message="Application ID is required",
                    message_code="INVALID_APP_ID",
                    status=StatusCode.UNPROCESSABLE_ENTITY
                ).to_response()

            if not isinstance(screens, list):
                return ServerResponse(
                    message="Screens must be a list",
                    message_code="INVALID_SCREENS_FORMAT",
                    status=StatusCode.UNPROCESSABLE_ENTITY
                ).to_response()

            # Buscar el rol por ID
            role = RoleModel.get_by_id(role_id)
            if not role:
                return ServerResponse(
                    message="Role not found",
                    message_code="ROLE_NOT_FOUND",
                    status=StatusCode.NOT_FOUND
                ).to_response()

            # Validar que el admin que creó el rol sea el que lo está modificando
            if role.admin_id != admin_id:
                return ServerResponse(
                    message="You can only modify roles that you created",
                    message_code="UNAUTHORIZED_MODIFY",
                    status=StatusCode.FORBIDDEN
                ).to_response()

            # Validar que el rol pertenezca a la aplicación especificada
            if str(role.app_id) != str(app_id):
                return ServerResponse(
                    message="Role does not belong to the specified application",
                    message_code="ROLE_APP_MISMATCH",
                    status=StatusCode.BAD_REQUEST
                ).to_response()

            # Actualizar las screens del rol
            updated_role = RoleModel.update_screens_by_role_id(role_id, screens)

            if not updated_role:
                return ServerResponse(
                    message="Failed to update screens for role",
                    message_code="UPDATE_SCREENS_FAILED",
                    status=StatusCode.INTERNAL_SERVER_ERROR
                ).to_response()

            return ServerResponse(
                data=updated_role.to_dict(),
                message="Screens updated successfully",
                message_code="SCREENS_UPDATED",
                status=StatusCode.OK
            ).to_response()

        except Exception as e:
            logging.error(f"Error updating screens: {str(e)}", exc_info=True)
            return ServerResponse(
                message="Internal server error",
                message_code="INTERNAL_SERVER_ERROR",
                status=StatusCode.INTERNAL_SERVER_ERROR
            ).to_response()


class ScreensByRoleController(Resource):
    route = "/rol/screens/role/<string:role_id>"

    """
    GET /rol/screens/role/{role_id} - Obtener screens de un rol específico
    """
    def get(self, role_id):
        try:
            # Validar autenticación
            auth_header = request.headers.get('Authorization')
            if not auth_header or not auth_header.startswith('Bearer '):
                return ServerResponse(
                    message="Authorization header required",
                    message_code="AUTH_REQUIRED",
                    status=StatusCode.UNAUTHORIZED
                ).to_response()

            token = auth_header.split(' ')[1]
            jwt_data = validate_jwt(token)
            if not jwt_data:
                return ServerResponse(
                    message="Invalid or expired token",
                    message_code="INVALID_TOKEN",
                    status=StatusCode.UNAUTHORIZED
                ).to_response()

            admin_id = jwt_data['identity']

            # Buscar el rol por ID
            role = RoleModel.get_by_id(role_id)
            if not role:
                return ServerResponse(
                    message="Role not found",
                    message_code="ROLE_NOT_FOUND",
                    status=StatusCode.NOT_FOUND
                ).to_response()

            # Validar que el admin que creó el rol sea el que lo está consultando
            if role.admin_id != admin_id:
                return ServerResponse(
                    message="You can only view roles that you created",
                    message_code="UNAUTHORIZED_VIEW",
                    status=StatusCode.FORBIDDEN
                ).to_response()

            return ServerResponse(
                data={
                    "role_id": role_id,
                    "screens": role.screens or []
                },
                message="Screens retrieved successfully",
                message_code="SCREENS_RETRIEVED",
                status=StatusCode.OK
            ).to_response()

        except Exception as e:
            logging.error(f"Error getting screens for role {role_id}: {str(e)}", exc_info=True)
            return ServerResponse(
                message="Internal server error",
                message_code="INTERNAL_SERVER_ERROR",
                status=StatusCode.INTERNAL_SERVER_ERROR
            ).to_response()
