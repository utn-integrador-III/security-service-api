from flask_restful import Resource
from flask import request, make_response, jsonify
from models.user.user import UserModel
from utils.server_response import ServerResponse, StatusCode
from utils.message_codes import (
    USER_NOT_FOUND, INVALID_VERIFICATION_CODE, VERIFICATION_EXPIRED, VERIFICATION_SUCCESSFUL
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
security_collection = db['user']

class UserVerificationController(Resource):
    route = '/user/verification'
    
    def options(self):
        response = make_response()
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add("Access-Control-Allow-Headers", "Content-Type,Authorization")
        response.headers.add("Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS")
        return response
    
    def put(self):
        try:
            data = request.json
            email = data.get('user_email')
            code = data.get('verification_code')
            
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
            
            # Verificar el código según el tipo de usuario
            verification_code_valid = False
            expiration_valid = True
            
            if user.get('apps') and len(user['apps']) > 0:
                # Usuario de security (código en apps[0].code)
                app_verification_code = user['apps'][0].get('code', '')
                verification_code_valid = app_verification_code == str(code)
                
                # Verificar expiración del código
                app_code_expiration = user['apps'][0].get('code_expliration', '')
                if app_code_expiration:
                    try:
                        expiration_date = datetime.strptime(app_code_expiration, "%Y/%m/%d %H:%M:%S")
                        expiration_valid = expiration_date > datetime.utcnow()
                    except ValueError:
                        expiration_valid = True
            else:
                # Usuario normal (código directo)
                verification_code_valid = user.get('verification_code') == int(code)
                expiration_valid = user.get('expiration_code', datetime.utcnow()) > datetime.utcnow()
            
            if not verification_code_valid:
                return ServerResponse(
                    message="Invalid verification code",
                    message_code=INVALID_VERIFICATION_CODE,
                    status=StatusCode.UNAUTHORIZED
                ).to_response()

            if not expiration_valid:
                return ServerResponse(
                    message="Verification code expired",
                    message_code=VERIFICATION_EXPIRED,
                    status=StatusCode.UNAUTHORIZED
                ).to_response()
            
            if user['status'].lower() != 'pending':
                return ServerResponse(
                    message="User is not in a pending state",
                    message_code="USER_NOT_PENDING",
                    status=StatusCode.BAD_REQUEST
                ).to_response()

            # Activar el usuario según el tipo
            if user.get('apps'):
                # Usuario de security - actualizar en la colección de security
                apps = user['apps']
                if apps:
                    apps[0]['code'] = ''
                    apps[0]['code_expliration'] = ''
                    apps[0]['status'] = 'Active'
                
                security_collection.update_one(
                    {"email": email},
                    {
                        "$set": {
                            "status": "Active",
                            "apps": apps,
                            "token": "",
                            "is_session_active": False
                        }
                    }
                )
            else:
                # Usuario normal - usar el método existente
                UserModel.user_activation(email)
            
            return ServerResponse(
                data=None,
                message="User successfully verified",
                message_code=VERIFICATION_SUCCESSFUL,
                status=StatusCode.OK
            ).to_response()
        
        except Exception as e:
            logging.error(f"An unexpected error occurred: {str(e)}", exc_info=True)
            return ServerResponse(
                message="An unexpected error occurred.",
                message_code="UNEXPECTED_ERROR",
                status=StatusCode.INTERNAL_SERVER_ERROR
            ).to_response()
