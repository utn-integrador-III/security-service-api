from flask_restful import Resource, reqparse
from flask import request
from utils.server_response import ServerResponse, StatusCode
from models.role.role import RoleModel
from models.user.user import UserModel
from models.apps.app import AppModel
from utils.jwt_manager import validate_jwt
from .parser import RolParser
import logging
from datetime import datetime
from bson import ObjectId

#from models.application.getapp import ApplicationModel
from models.role.role import RoleModel

class RolController(Resource):
    route = "/rol"

    """
    Get roles - list all roles or get by name if provided
    """
    def get(self):
        try:
            # Check if name parameter is provided in query string
            name = request.args.get('name')
            
            if name:
                # Get specific role by name
                result = RoleModel.get_by_name(name)
                
                if isinstance(result, dict) and "error" in result:
                    response = ServerResponse(
                        data={},
                        message=result["error"],
                        status=StatusCode.INTERNAL_SERVER_ERROR,
                    )
                    return response.to_response()

                if not result:
                    response = ServerResponse(
                        data={},
                        message="Role not found",
                        message_code="ROL_NOT_FOUND",
                        status=StatusCode.NOT_FOUND,
                    )
                    return response.to_response()
                else:
                    response = ServerResponse(
                        data=result.to_dict(),
                        message="Role found",
                        message_code="OK_MSG",
                        status=StatusCode.OK,
                    )
                    return response.to_response()
            else:
                # List all roles
                result = RoleModel.list()
                
                if isinstance(result, dict) and "error" in result:
                    response = ServerResponse(
                        data={},
                        message=result["error"],
                        status=StatusCode.INTERNAL_SERVER_ERROR,
                    )
                    return response.to_response()

                if not result:
                    response = ServerResponse(
                        data=[],
                        message="No roles found",
                        message_code="NO_DATA",
                        status=StatusCode.OK,
                    )
                    return response.to_response()
                else:
                    # Convert list of RoleModel instances to dictionaries
                    roles_data = [role.to_dict() if hasattr(role, 'to_dict') else role for role in result]
                    response = ServerResponse(
                        data=roles_data,
                        message="Roles retrieved successfully",
                        message_code="OK_MSG",
                        status=StatusCode.OK,
                    )
                    return response.to_response()
        except Exception as ex:
            logging.error(ex)
            response = ServerResponse(status=StatusCode.INTERNAL_SERVER_ERROR)
            return response.to_response()

    """
    Create a new role
    """
    def post(self):
        try:
            data = request.get_json()
            name = data.get('name')
            description = data.get('description', '')
            permissions = data.get('permissions', [])
            admin_id = data.get('admin_id')  # Campo opcional enviado por el frontend
            app_id = data.get('app_id')  # Campo para especificar la aplicación específica

            # Validación del nombre
            if not name or len(name.strip()) < 2:
                return ServerResponse(
                    message="Invalid role name",
                    message_code="INVALID_NAME",
                    status=StatusCode.UNPROCESSABLE_ENTITY
                ).to_response()

            # Validación de permisos
            if not isinstance(permissions, list):
                return ServerResponse(
                    message="Permissions must be a list",
                    message_code="INVALID_PERMISSIONS",
                    status=StatusCode.UNPROCESSABLE_ENTITY
                ).to_response()

            # Validación de app_id
            if not app_id:
                return ServerResponse(
                    message="app_id is required to specify which application the role belongs to",
                    message_code="APP_ID_REQUIRED",
                    status=StatusCode.UNPROCESSABLE_ENTITY
                ).to_response()

            # Verificar que la aplicación existe
            try:
                app = AppModel.get(app_id)
                if not app:
                    return ServerResponse(
                        message="Application not found",
                        message_code="APP_NOT_FOUND",
                        status=StatusCode.NOT_FOUND
                    ).to_response()
            except Exception as e:
                return ServerResponse(
                    message="Invalid app_id format",
                    message_code="INVALID_APP_ID",
                    status=StatusCode.UNPROCESSABLE_ENTITY
                ).to_response()

            # Verificar si ya existe un rol con el mismo nombre en la misma aplicación
            existing_role = RoleModel.get_by_name(name.strip())
            if existing_role and existing_role.app_id == app_id:
                return ServerResponse(
                    message="Role already exists in this application",
                    message_code="DUPLICATE_ROLE",
                    status=StatusCode.CONFLICT
                ).to_response()

            # Crear el objeto de datos del rol
            role_data = {
                "name": name.strip(),
                "description": description.strip(),
                "permissions": permissions,
                "creation_date": datetime.utcnow(),
                "mod_date": datetime.utcnow(),
                "is_active": True,
                "default_role": False,
                "screens": [],                   # Vacío por defecto
                "app_id": ObjectId(app_id) if isinstance(app_id, str) else app_id
            }

            # Agregar campos opcionales si se proporcionan
            if admin_id:
                role_data["admin_id"] = str(admin_id) if isinstance(admin_id, ObjectId) else admin_id

            new_role = RoleModel.create(role_data)

            if not new_role:
                return ServerResponse(
                    message="Failed to create role",
                    message_code="CREATE_FAILED",
                    status=StatusCode.INTERNAL_SERVER_ERROR
                ).to_response()

            return ServerResponse(
                data=new_role.to_dict(),
                message="Role created successfully",
                message_code="CREATED",
                status=StatusCode.CREATED
            ).to_response()

        except Exception as e:
            logging.error(f"Error creating role: {str(e)}", exc_info=True)
            return ServerResponse(
                message="Internal server error",
                message_code="INTERNAL_SERVER_ERROR",
                status=StatusCode.INTERNAL_SERVER_ERROR
            ).to_response()

    """
    Delete a role by name
    """
    def delete(self):
        try:
            data = request.get_json()
            role_name = data.get("role_name")

            if not role_name:
                return ServerResponse(
                    message="Role name is required",
                    message_code="INVALID_ROLE_NAME",
                    status=StatusCode.UNPROCESSABLE_ENTITY
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

            # Buscar el rol por nombre
            existing_role = RoleModel.get_by_name(role_name)
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
            deleted = RoleModel.delete_by_name_and_client_id(role_name, existing_role.app_id)

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

    # Nuevo endpoint: /roleByUser/<email>/<app>
    @staticmethod
    def get_roles_by_user_and_app(email, app):
        print("ENTRANDO AL MÉTODO get_roles_by_user_and_app")
        try:
            user = UserModel.find_by_email(email)
            print("Usuario encontrado:", user)
            if not user:
                print("ALERTA: Usuario no encontrado")
                return ServerResponse(
                    message="User not found",
                    message_code="USER_NOT_FOUND",
                    status=StatusCode.NOT_FOUND
                ).to_response()

            print("Claves del usuario:", list(user.keys()))
            user_apps = user.get('apps', None)
            print("Tipo de user_apps:", type(user_apps))
            print("Contenido de user_apps:", user_apps)
            if user_apps is None:
                print("ALERTA: El campo 'apps' no existe en el usuario")
            elif isinstance(user_apps, list) and len(user_apps) == 0:
                print("ALERTA: El campo 'apps' está vacío")
            roles_info = []
            if isinstance(user_apps, list):
                for idx, app_entry in enumerate(user_apps):
                    print(f"Revisando app_entry #{idx}:", app_entry)
                    if isinstance(app_entry, dict):
                        print("  Claves de app_entry:", list(app_entry.keys()))
                        if app_entry.get('app') == app:
                            role_name = app_entry.get('role')
                            print("  Buscando rol:", role_name)
                            role_obj = RoleModel.get_by_name(role_name)
                            print("  Rol encontrado:", role_obj)
                            if role_obj:
                                roles_info.append(role_obj.to_dict())
                    else:
                        print(f"  ALERTA: app_entry no es un dict, es {type(app_entry)}")
            else:
                print("ALERTA: user_apps no es una lista")

            if not roles_info:
                print("ALERTA: No se encontraron roles para este usuario y app")
                return ServerResponse(
                    data=[],
                    message="No roles found for this user and app",
                    message_code="NO_ROLES_FOUND",
                    status=StatusCode.OK
                ).to_response()

            print("Roles encontrados:", roles_info)
            return ServerResponse(
                data=roles_info,
                message="Roles found",
                message_code="ROLES_FOUND",
                status=StatusCode.OK
            ).to_response()
        except Exception as ex:
            print("ERROR en get_roles_by_user_and_app:", ex)
            logging.error(ex)
            return ServerResponse(
                message="Internal server error",
                message_code="INTERNAL_SERVER_ERROR",
                status=StatusCode.INTERNAL_SERVER_ERROR
            ).to_response()
    

    @staticmethod
    def post_role(client_id):
        try:
            data = request.get_json()
            name = data.get('name')
            description = data.get('description', '')
            permissions = data.get('permissions', [])

            # Validación del nombre
            if not name or len(name.strip()) < 2:
                return ServerResponse(
                    message="Invalid role name",
                    message_code="INVALID_NAME",
                    status=StatusCode.UNPROCESSABLE_ENTITY
                ).to_response()

            # Validación de permisos
            if not isinstance(permissions, list):
                return ServerResponse(
                    message="Permissions must be a list",
                    message_code="INVALID_PERMISSIONS",
                    status=StatusCode.UNPROCESSABLE_ENTITY
                ).to_response()

            #  que la app exista por client_id
            app = ApplicationModel().find_by_client_id(client_id)
            if not app:
                return ServerResponse(
                    message="Application not found",
                    message_code="APP_NOT_FOUND",
                    status=StatusCode.NOT_FOUND
                ).to_response()

            #  si ya existe un rol con mismo name y app_client_id
            existing_role = RoleModel.get_by_name_and_client_id(name.strip(), app["client_id"])
            if existing_role:
                return ServerResponse(
                    message="Role already exists",
                    message_code="DUPLICATE_ROLE",
                    status=StatusCode.CONFLICT
                ).to_response()

            # json object
            role_data = {
                "name": name.strip(),
                "description": description.strip(),
                "permissions": permissions,
                "creation_date": datetime.utcnow(),
                "mod_date": datetime.utcnow(),
                "is_active": True,
                "default_role": False,
                "screens": [],                   # Vacío por defecto
                "app": app["name"],
                "app_client_id": app["client_id"]
            }

            new_role = RoleModel.create(role_data)

            return ServerResponse(
                data=new_role,
                message="Role created successfully",
                message_code="CREATED",
                status=StatusCode.CREATED
            ).to_response()

        except Exception as e:
            logging.error(f"Error creating role: {str(e)}", exc_info=True)
            return ServerResponse(
                message="Internal server error",
                message_code="INTERNAL_SERVER_ERROR",
                status=StatusCode.INTERNAL_SERVER_ERROR
            ).to_response()

        

    #post metod to insert screens that the user can acces
    @staticmethod
    def post_add_screens(client_id):
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

            updated_role = RoleModel.add_screens(role_name, client_id, new_screens)

            if not updated_role:
                return ServerResponse(
                    message="Role not found or application not found",
                    message_code="ROLE_OR_APP_NOT_FOUND",
                    status=StatusCode.NOT_FOUND
                ).to_response()
            
            if updated_role == "DUPLICATE":
                return ServerResponse(
                    message="Screens already exist",
                    message_code="DUPLICATE_SCREENS",
                    status=StatusCode.CONFLICT  # 409
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

        

    #Delete roll
    @staticmethod
    def delete_role(client_id):
        try:
            data = request.get_json()
            role_name = data.get("role_name")

            if not role_name:
                return ServerResponse(
                    message="Role name is required",
                    message_code="INVALID_ROLE_NAME",
                    status=StatusCode.UNPROCESSABLE_ENTITY
                ).to_response()

            deleted = RoleModel.delete_by_name_and_client_id(role_name, client_id)

            if not deleted:
                return ServerResponse(
                    message="Role not found or already deleted",
                    message_code="ROLE_NOT_FOUND",
                    status=StatusCode.NOT_FOUND
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

