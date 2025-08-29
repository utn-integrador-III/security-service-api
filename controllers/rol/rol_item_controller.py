from flask_restful import Resource
from flask import request
from utils.server_response import ServerResponse, StatusCode
from models.role.role import RoleModel
from utils.jwt_manager import validate_jwt
import logging

class RolItemController(Resource):
    route = "/rol/<string:role_id>"

    """
    Get a specific role by ID
    """
    def get(self, role_id):
        try:
            # Obtener el admin_id del token JWT
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

            # VALIDACIÓN DE SEGURIDAD: Solo el admin que creó el rol puede verlo
            if role.admin_id != admin_id:
                return ServerResponse(
                    message="You can only view roles that you created",
                    message_code="UNAUTHORIZED_VIEW",
                    status=StatusCode.FORBIDDEN
                ).to_response()

            return ServerResponse(
                data=role.to_dict(),
                message="Role retrieved successfully",
                message_code="ROLE_FOUND",
                status=StatusCode.OK
            ).to_response()

        except Exception as e:
            logging.error(f"Error getting role: {str(e)}", exc_info=True)
            return ServerResponse(
                message="Internal server error",
                message_code="INTERNAL_SERVER_ERROR",
                status=StatusCode.INTERNAL_SERVER_ERROR
            ).to_response()

    """
    Update an existing role
    """
    def patch(self, role_id):
        try:
            data = request.get_json(force=True, silent=True) or {}
            
            # Validar que se proporcione al menos un campo para actualizar
            allowed_fields = ['name', 'description', 'permissions', 'is_active', 'screens']
            provided_fields = [field for field in allowed_fields if field in data]
            
            if not provided_fields:
                return ServerResponse(
                    message="At least one field must be provided for update: name, description, permissions, is_active, or screens",
                    message_code="NO_FIELDS_PROVIDED",
                    status=StatusCode.BAD_REQUEST
                ).to_response()

            # Obtener el admin_id del token JWT
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
            existing_role = RoleModel.get_by_id(role_id)
            if not existing_role:
                return ServerResponse(
                    message="Role not found",
                    message_code="ROLE_NOT_FOUND",
                    status=StatusCode.NOT_FOUND
                ).to_response()

            # VALIDACIÓN DE SEGURIDAD: Solo el admin que creó el rol puede modificarlo
            if existing_role.admin_id != admin_id:
                return ServerResponse(
                    message="You can only modify roles that you created",
                    message_code="UNAUTHORIZED_MODIFY",
                    status=StatusCode.FORBIDDEN
                ).to_response()

            # Preparar datos para actualización
            update_data = {}
            for field in provided_fields:
                if field in data:
                    update_data[field] = data[field]

            # Actualizar el rol
            updated_role = RoleModel.update(role_id, update_data)

            if not updated_role:
                return ServerResponse(
                    message="Failed to update role",
                    message_code="UPDATE_FAILED",
                    status=StatusCode.INTERNAL_SERVER_ERROR
                ).to_response()

            return ServerResponse(
                data=updated_role.to_dict(),
                message="Role updated successfully",
                message_code="ROLE_UPDATED",
                status=StatusCode.OK
            ).to_response()

        except ValueError as ve:
            return ServerResponse(
                message=str(ve),
                message_code="VALIDATION_ERROR",
                status=StatusCode.UNPROCESSABLE_ENTITY
            ).to_response()
        except Exception as e:
            logging.error(f"Error updating role: {str(e)}", exc_info=True)
            return ServerResponse(
                message="Internal server error",
                message_code="INTERNAL_SERVER_ERROR",
                status=StatusCode.INTERNAL_SERVER_ERROR
            ).to_response()

    """
    Delete a specific role by ID
    """
    def delete(self, role_id):
        try:
            # Obtener el admin_id del token JWT
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
            existing_role = RoleModel.get_by_id(role_id)
            if not existing_role:
                return ServerResponse(
                    message="Role not found",
                    message_code="ROLE_NOT_FOUND",
                    status=StatusCode.NOT_FOUND
                ).to_response()

            # VALIDACIÓN DE SEGURIDAD: Solo el admin que creó el rol puede eliminarlo
            if existing_role.admin_id != admin_id:
                return ServerResponse(
                    message="You can only delete roles that you created",
                    message_code="UNAUTHORIZED_DELETE",
                    status=StatusCode.FORBIDDEN
                ).to_response()

            # Eliminar el rol usando el método del modelo
            deleted = RoleModel.delete_by_name_and_client_id(existing_role.name, existing_role.app_id)

            if not deleted:
                return ServerResponse(
                    message="Failed to delete role",
                    message_code="DELETE_FAILED",
                    status=StatusCode.INTERNAL_SERVER_ERROR
                ).to_response()

            return ServerResponse(
                message="Role deleted successfully",
                message_code="ROLE_DELETED",
                status=StatusCode.OK
            ).to_response()

        except Exception as e:
            logging.error(f"Error deleting role: {str(e)}", exc_info=True)
            return ServerResponse(
                message="Internal server error",
                message_code="INTERNAL_SERVER_ERROR",
                status=StatusCode.INTERNAL_SERVER_ERROR
            ).to_response()
