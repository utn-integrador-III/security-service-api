from flask_restful import Resource
from flask import request, make_response
from models.user.user import UserModel
from utils.server_response import ServerResponse, StatusCode
from utils.message_codes import (
    USER_NOT_FOUND
)
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

class UserAppController(Resource):
    route = '/user/current-app'
    
    def options(self):
        response = make_response()
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add("Access-Control-Allow-Headers", "Content-Type,Authorization")
        response.headers.add("Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS")
        return response
    
    def get(self):
        """
        Get current app information for the user
        """
        try:
            # Obtener email del header Authorization o query parameter
            email = request.args.get('email')
            if not email:
                return ServerResponse(
                    message="Email is required",
                    message_code="MISSING_EMAIL",
                    status=StatusCode.BAD_REQUEST
                ).to_response()
            
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
                        'is_session_active': security_user.get('is_session_active', False),
                        'current_app_id': security_user.get('current_app_id'),
                        'current_app': security_user.get('current_app'),
                        'last_login': security_user.get('last_login')
                    }
            
            if not user:
                return ServerResponse(
                    message="User not found",
                    message_code=USER_NOT_FOUND,
                    status=StatusCode.NOT_FOUND
                ).to_response()
            
            # Preparar respuesta con información de la app actual
            response_data = {
                "email": user['email'],
                "name": user['name'],
                "current_app_id": user.get('current_app_id'),
                "current_app": user.get('current_app'),
                "last_login": user.get('last_login'),
                "is_session_active": user.get('is_session_active', False)
            }
            
            # Si el usuario tiene apps, incluir información adicional
            if user.get('apps'):
                response_data['apps'] = user['apps']
            
            return ServerResponse(
                data=response_data,
                message="Current app information retrieved successfully",
                message_code="APP_INFO_RETRIEVED",
                status=StatusCode.OK
            ).to_response()
        
        except Exception as e:
            logging.error(f"An unexpected error occurred: {str(e)}", exc_info=True)
            return ServerResponse(
                message="An unexpected error occurred.",
                message_code="UNEXPECTED_ERROR",
                status=StatusCode.INTERNAL_SERVER_ERROR
            ).to_response() 