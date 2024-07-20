import logging
import random
from datetime import datetime, timedelta
from flask import request
from flask_restful import Resource
from validate_email import validate_email
from models.user.user import UserModel
from models.role.role import RoleModel
from utils.server_response import ServerResponse, StatusCode
from utils.message_codes import (
    INVALID_EMAIL_DOMAIN, INVALID_NAME, INVALID_PASSWORD, USER_ALREADY_REGISTERED, USER_SUCCESSFULLY_CREATED, INVALID_ROLE
)

class UserEnrollmentController(Resource):
    route = '/user/enrollment'
    
    def post(self):
        try:
            data = request.json
            name = data.get('name')
            password = data.get('password')
            email = data.get('email')
            provided_role = data.get('role', '')
            
            # Validar email
            if not email or not validate_email(email):
                return ServerResponse(
                    message="The provided email is not valid",
                    message_code=INVALID_EMAIL_DOMAIN,
                    status=StatusCode.UNPROCESSABLE_ENTITY
                )
            
            if not any(domain in email for domain in ['utn.ac.cr', 'est.utn.ac.cr', 'adm.utn.ac.cr']):
                return ServerResponse(
                    message="The entered domain does not meet the established standards",
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
            
            try:
                # Verificar si el usuario ya existe
                existing_user = UserModel.find_by_email(email)
                if existing_user:
                    return ServerResponse(
                        message="The user is already registered",
                        message_code=USER_ALREADY_REGISTERED,
                        status=StatusCode.CONFLICT
                    )
                
                # Obtener roles activos
                active_roles = RoleModel.find_active_roles()
                
                # Validar que haya al menos un rol activo
                if not active_roles:
                    return ServerResponse(
                        message="No active roles found",
                        status=StatusCode.UNPROCESSABLE_ENTITY
                    )
                
                # Filtrar nombres de roles válidos y convertirlos a minúsculas
                valid_role_names = [role.get('name', '').lower().strip() for role in active_roles]
                
                # Validar que se haya encontrado al menos un nombre de rol válido
                if not valid_role_names:
                    return ServerResponse(
                        message="No valid role names found",
                        status=StatusCode.UNPROCESSABLE_ENTITY
                    )
                
                # Validar que el rol proporcionado exista en la base de datos
                if provided_role.lower().strip() not in valid_role_names:
                    return ServerResponse(
                        message=f"The provided role is not valid: {provided_role}",
                        message_code=INVALID_ROLE,
                        status=StatusCode.UNPROCESSABLE_ENTITY
                    )
                
                # Generar código de verificación y código de expiración
                verification_code = random.randint(100000, 999999)
                expiration_code = datetime.utcnow() + timedelta(minutes=5)
                
                # Crear nuevo usuario
                user_data = {
                    'name': name,
                    'password': password,
                    'email': email,
                    'status': 'Pending',
                    'verification_code': verification_code,
                    'expiration_code': expiration_code,
                    'role': provided_role,
                    'token': "",
                    'is_session_active': False
                }
                
                new_user = UserModel.create_user(user_data)
                
                return ServerResponse(
                    data={
                        'email': new_user.email,
                        'name': new_user.name,
                        'status': new_user.status,
                        'role_id': [
                            {
                                'roles': new_user.role
                            }
                        ],
                        'token': new_user.token
                    },
                    message="Authentication succeed",
                    message_code="AUTH_SUCCEED",
                    status=StatusCode.OK
                )
            except Exception as e:
                logging.error(f"Error creating user: {str(e)}", exc_info=True)
                return ServerResponse(
                    message="Error creating user",
                    status=StatusCode.INTERNAL_SERVER_ERROR
                )
        
        except Exception as e:
            logging.error(f"An unexpected error occurred: {str(e)}", exc_info=True)
            return ServerResponse(
                message="An unexpected error occurred.",
                status=StatusCode.INTERNAL_SERVER_ERROR
            )