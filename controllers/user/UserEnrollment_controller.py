import logging
from flask_restful import Resource
from flask import request
from models.user.user import UserModel
from utils.server_response import ServerResponse, StatusCode
from utils.message_codes import (
    USER_ALREADY_REGISTERED,
    INVALID_EMAIL_DOMAIN,
    USER_SUCCESSFULLY_CREATED,
    INVALID_NAME,
    INVALID_PASSWORD
)
from email_validator import validate_email, EmailNotValidError
from datetime import datetime, timedelta
import random
import string

logger = logging.getLogger(__name__)

class UserEnrollmentController(Resource):
    route = '/user/enrollment'
    
    def post(self):
        try:
            data = request.json
            name = data.get('name')
            password = data.get('password')
            email = data.get('email')
            
            # Validar email
            try:
                valid = validate_email(email)
                email = valid.email
                if not email.endswith('@est.utn.ac.cr'):
                    return ServerResponse(
                        message="The entered domain does not meet the established standards",
                        message_code=INVALID_EMAIL_DOMAIN,
                        status=StatusCode.UNPROCESSABLE_ENTITY
                    )
            except EmailNotValidError:
                return ServerResponse(
                    message="The provided email is not valid",
                    message_code=INVALID_EMAIL_DOMAIN,
                    status=StatusCode.UNPROCESSABLE_ENTITY
                )
            
            # Validar nombre
            if not name or len(name.strip()) < 2:
                return ServerResponse(
                    message="The name does not meet the established standards",
                    message_code=INVALID_NAME,
                    status=StatusCode.UNPROCESSABLE_ENTITY
                )
            
            # Validar contraseña
            if not password or len(password) < 8:
                return ServerResponse(
                    message="The password does not meet the established standards",
                    message_code=INVALID_PASSWORD,
                    status=StatusCode.UNPROCESSABLE_ENTITY
                )
            
            # Verificar si el usuario ya existe
            existing_user = UserModel.find_by_email(email)
            if existing_user:
                return ServerResponse(
                    message="The user is already registered",
                    message_code=USER_ALREADY_REGISTERED,
                    status=StatusCode.CONFLICT
                )
            
            try:
                # Crear nuevo usuario
                verification_code = ''.join(random.choices(string.digits, k=4))
                expiration_time = datetime.utcnow() + timedelta(minutes=5)
                
                user_data = {
                    'name': name,
                    'password': password,
                    'email': email,
                    'status': 'Pending',
                    'verification_code': verification_code,
                    'expiration_time': expiration_time.isoformat()
                }
                
                new_user = UserModel.create_user(user_data)
                
                return ServerResponse(
                    message="User successfully created",
                    message_code=USER_SUCCESSFULLY_CREATED,
                    status=StatusCode.OK
                )
            except Exception as e:
                logger.error(f"Error creating user: {str(e)}", exc_info=True)
                return ServerResponse(
                    message="Error creating user",
                    status=StatusCode.INTERNAL_SERVER_ERROR
                )
        
        except Exception as e:
            logger.error(f"An unexpected error occurred: {str(e)}", exc_info=True)
            return ServerResponse(
                message="An unexpected error occurred.",
                status=StatusCode.INTERNAL_SERVER_ERROR
            )
