from flask_restful import Resource, reqparse
from flask import request, make_response
from models.role.role import RoleModel
from utils.server_response import ServerResponse, StatusCode
from utils.message_codes import (
    ROLE_CREATED_SUCCESSFULLY, ROLE_ALREADY_EXISTS, INVALID_ROLE_DATA
)
import logging
from datetime import datetime
from pymongo import MongoClient
import os
from dotenv import load_dotenv

# Cargar variables de entorno para conexión directa a MongoDB
load_dotenv()
MONGO_URL = os.getenv("MONGO_URL")
client = MongoClient(MONGO_URL)
db = client['security']
role_collection = db['role']

class RoleCreationController(Resource):
    route = '/roles/create'
    
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('name', required=True, help="Role name cannot be blank!")
        self.parser.add_argument('permissions', required=True, type=list, help="Permissions cannot be blank!")
        self.parser.add_argument('app', required=True, help="App cannot be blank!")
        self.parser.add_argument('description', type=str, default="")
        self.parser.add_argument('screens', type=list, default=[])
        self.parser.add_argument('is_active', type=bool, default=True)
        self.parser.add_argument('default_role', type=bool, default=False)
    
    def options(self):
        response = make_response()
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add("Access-Control-Allow-Headers", "Content-Type,Authorization")
        response.headers.add("Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS")
        return response
    
    def post(self):
        """
        Create a new role with permissions and screen access
        """
        try:
            args = self.parser.parse_args()
            name = args['name']
            description = args['description']
            permissions = args['permissions']
            screens = args['screens']
            app = args['app']
            is_active = args['is_active']
            default_role = args['default_role']
            
            # Validar que el nombre del rol no esté vacío
            if not name or not name.strip():
                return ServerResponse(
                    message="Role name cannot be empty",
                    message_code="EMPTY_ROLE_NAME",
                    status=StatusCode.BAD_REQUEST
                ).to_response()
            
            # Validar que los permisos no estén vacíos
            if not permissions or len(permissions) == 0:
                return ServerResponse(
                    message="At least one permission is required",
                    message_code="EMPTY_PERMISSIONS",
                    status=StatusCode.BAD_REQUEST
                ).to_response()
            
            # Validar que la app no esté vacía
            if not app or not app.strip():
                return ServerResponse(
                    message="App cannot be empty",
                    message_code="EMPTY_APP",
                    status=StatusCode.BAD_REQUEST
                ).to_response()
            
            # Verificar si el rol ya existe
            existing_role = role_collection.find_one({"name": name, "app": app})
            if existing_role:
                return ServerResponse(
                    message="Role already exists for this app",
                    message_code=ROLE_ALREADY_EXISTS,
                    status=StatusCode.CONFLICT
                ).to_response()
            
            # Crear el objeto de rol
            current_time = datetime.utcnow()
            role_data = {
                "name": name,
                "description": description,
                "permissions": permissions,
                "screens": screens,
                "app": app,
                "is_active": is_active,
                "default_role": default_role,
                "creation_date": current_time,
                "mod_date": current_time
            }
            
            # Insertar en la base de datos
            result = role_collection.insert_one(role_data)
            
            if not result.inserted_id:
                return ServerResponse(
                    message="Failed to create role",
                    message_code="ROLE_CREATION_FAILED",
                    status=StatusCode.INTERNAL_SERVER_ERROR
                ).to_response()
            
            # Crear objeto RoleModel para la respuesta
            created_role = RoleModel(
                _id=str(result.inserted_id),
                name=name,
                description=description,
                permissions=permissions,
                screens=screens,
                app=app,
                is_active=is_active,
                default_role=default_role,
                creation_date=current_time,
                mod_date=current_time
            )
            
            return ServerResponse(
                data=created_role.to_dict(),
                message="Role created successfully",
                message_code=ROLE_CREATED_SUCCESSFULLY,
                status=StatusCode.CREATED
            ).to_response()
        
        except Exception as e:
            logging.error(f"An unexpected error occurred: {str(e)}", exc_info=True)
            return ServerResponse(
                message="An unexpected error occurred.",
                message_code="UNEXPECTED_ERROR",
                status=StatusCode.INTERNAL_SERVER_ERROR
            ).to_response() 