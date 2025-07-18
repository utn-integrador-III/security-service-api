from flask_restful import Resource, reqparse
from flask import request
from utils.server_response import ServerResponse, StatusCode
from models.role.role import RoleModel
from models.user.user import UserModel
from .parser import RolParser
import logging
from datetime import datetime

from models.application.getapp import ApplicationModel
from models.role.role import RoleModel

class RolController(Resource):
    route = "/rol"

    """
    Get a rol
    """
    def get(self):
        try:
            arg = RolParser.parse_put_request()
            object_name = arg['name']

            if not object_name:
                response = ServerResponse(message="name not inserted", message_code="ROL_NOT_FOUND", status=StatusCode.NOT_FOUND)
                return response.to_response()
            
            result = RoleModel.get_by_name(object_name)
            
            if isinstance(result, dict) and "error" in result:
                response = ServerResponse(
                    data={},
                    message=result["error"],
                    status=StatusCode.INTERNAL_SERVER_ERROR,
                )
                return response.to_response()

            if not result:  # If there are no rol objects
                response = ServerResponse(
                    data={},
                    message="No rol objects found",
                    message_code="NO_DATA",
                    status=StatusCode.OK,
                )
                return response.to_response()
            else:
                response = ServerResponse(
                    data=result.to_dict(),  # Convert the RolModel instance to a dictionary
                    message="ROL_FOUND",
                    message_code="OK_MSG",
                    status=StatusCode.OK,
                )
                return response.to_response()
        except Exception as ex:
            logging.error(ex)
            response = ServerResponse(status=StatusCode.INTERNAL_SERVER_ERROR)
            return response.to_response()

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
    

    #POST ROLL new endpoint
   
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

            # Verificar que la app exista por client_id
            app = ApplicationModel().find_by_client_id(client_id)
            if not app:
                return ServerResponse(
                    message="Application not found",
                    message_code="APP_NOT_FOUND",
                    status=StatusCode.NOT_FOUND
                ).to_response()

            # Crear objeto del rol completo según estructura del modelo
            role_data = {
                "name": name.strip(),
                "description": description.strip(),
                "permissions": permissions,
                "creation_date": datetime.utcnow(),
                "mod_date": datetime.utcnow(),
                "is_active": True,
                "default_role": False,
                "screens": [],                   # Vacío por defecto
                "app": app["name"]              
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