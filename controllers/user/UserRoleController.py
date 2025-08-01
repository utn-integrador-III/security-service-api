from flask_restful import Resource
from flask import request, make_response
from models.user.user import UserModel
from models.role.role import RoleModel
from utils.server_response import ServerResponse, StatusCode
from utils.message_codes import USER_NOT_FOUND
import logging
from pymongo import MongoClient
import os
from dotenv import load_dotenv

# Cargar variables de entorno para conexión directa a MongoDB
load_dotenv()
MONGO_URL = os.getenv("MONGO_URL")
client = MongoClient(MONGO_URL)
db = client['security']
security_collection = db['user']

class UserRoleController(Resource):
    route = '/roleByUser/<string:email>/<string:app>'
    
    def options(self):
        response = make_response()
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add("Access-Control-Allow-Headers", "Content-Type,Authorization")
        response.headers.add("Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS")
        return response
    
    def get(self, email, app):
        """
        Get all roles for a user filtered by app
        """
        try:
            # Primero intentar buscar en la colección de usuarios normales
            user = UserModel.find_by_email(email)
            
            # Si no se encuentra, buscar en la colección de security users
            if not user:
                security_user = security_collection.find_one({"email": email})
                if security_user:
                    # Convertir el usuario de security a formato compatible
                    user = {
                        'id': str(security_user['_id']),
                        'name': security_user['name'],
                        'email': security_user['email'],
                        'password': security_user['password'],
                        'status': security_user.get('status', 'Active'),
                        'apps': security_user.get('apps', []),
                        'token': security_user.get('token', ''),
                        'is_session_active': security_user.get('is_session_active', False)
                    }
            
            if not user:
                return ServerResponse(
                    message="User not found",
                    message_code=USER_NOT_FOUND,
                    status=StatusCode.NOT_FOUND
                ).to_response()
            
            # Obtener roles del usuario para la app específica
            user_roles = []
            
            if user.get('apps') and len(user['apps']) > 0:
                # Usuario de security (tiene apps)
                for app_data in user['apps']:
                    if app_data.get('app') == app:
                        role_name = app_data.get('role', '')
                        if role_name:
                            # Obtener información detallada del rol desde la base de datos
                            role_object = RoleModel.get_by_name(role_name)
                            if role_object:
                                role_info = {
                                    "name": role_object.name,
                                    "permissions": role_object.permissions,
                                    "screens": role_object.screens,
                                    "is_active": role_object.is_active,
                                    "description": role_object.description,
                                    "app": role_object.app
                                }
                            else:
                                # Si no existe el rol en la BD, usar información básica
                                role_info = {
                                    "name": role_name,
                                    "permissions": ["read", "write"],
                                    "screens": ["default"],
                                    "is_active": True,
                                    "description": "Default role",
                                    "app": app
                                }
                            user_roles.append(role_info)
            else:
                # Usuario normal - obtener rol desde la base de datos
                user_role = user.get('role', '')
                if user_role:
                    role_object = RoleModel.get_by_name(user_role)
                    if role_object:
                        role_info = {
                            "name": role_object.name,
                            "permissions": role_object.permissions,
                            "screens": role_object.screens,
                            "is_active": role_object.is_active,
                            "description": role_object.description,
                            "app": role_object.app
                        }
                    else:
                        # Si no existe el rol en la BD, usar información básica
                        role_info = {
                            "name": user_role,
                            "permissions": ["read", "write"],
                            "screens": ["default"],
                            "is_active": True,
                            "description": "Default role",
                            "app": app
                        }
                    user_roles.append(role_info)
            
            response_data = {
                "email": user['email'],
                "name": user['name'],
                "app": app,
                "roles": user_roles
            }
            
            return ServerResponse(
                data=response_data,
                message="User roles retrieved successfully",
                message_code="USER_ROLES_RETRIEVED",
                status=StatusCode.OK
            ).to_response()
        
        except Exception as e:
            logging.error(f"An unexpected error occurred: {str(e)}", exc_info=True)
            return ServerResponse(
                message="An unexpected error occurred.",
                message_code="UNEXPECTED_ERROR",
                status=StatusCode.INTERNAL_SERVER_ERROR
            ).to_response() 