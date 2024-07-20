from flask_restful import Resource
from flask import request
from email_validator import validate_email, EmailNotValidError  # Asegúrate de importar la librería correcta
from models.user.user import UserModel
from models.role.role import RoleModel
from utils.server_response import ServerResponse, StatusCode
from utils.message_codes import (
    INVALID_EMAIL_DOMAIN, INVALID_NAME, INVALID_PASSWORD, USER_ALREADY_REGISTERED, USER_SUCCESSFULLY_CREATED, INVALID_ROLE
)
import logging
import random
from datetime import datetime, timedelta

class UserEnrollmentController(Resource):
    route = '/user/enrollment'
    
    def post(self): 
        try:
            data = request.json
            name = data.get('name')
            password = data.get('password')
            email = data.get('email')
            provided_roles = data.get('roles', [])
            
            # Validar email
            try:
                valid = validate_email(email)  # Validar el email
                email = valid.email  # Actualizar con el email validado
            except EmailNotValidError as e:
                return ServerResponse(
                    message=str(e),
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
                
                # Obtener roles activos y predeterminados
                default_roles = [role for role in active_roles if role.get('default_role', False)]
                
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
                
                # Validar que todos los roles proporcionados existan en la base de datos
                invalid_roles = [role for role in provided_roles if role.lower().strip() not in valid_role_names]
                if invalid_roles:
                    return ServerResponse(
                        message=f"The following roles are not valid: {', '.join(invalid_roles)}",
                        message_code=INVALID_ROLE,
                        status=StatusCode.UNPROCESSABLE_ENTITY
                    )
                
                # Si no se proporcionaron roles, usar los roles predeterminados
                if not provided_roles:
                    provided_roles = [role.get('name') for role in default_roles]
                
                # Generar código de verificación y código de expiración
                verification_code = 123456  # Código de verificación fijo
                expiration_code = datetime.utcnow() + timedelta(minutes=5)
                
                # Crear nuevo usuario
                user_data = {
                    'name': name,
                    'password': password,
                    'email': email,
                    'status': 'Pending',
                    'verification_code': verification_code,
                    'expiration_code': expiration_code,
                    'roles': provided_roles,
                    'token': "",
                    'is_session_active': False
                }
                
                new_user = UserModel.create_user(user_data)
                
                return ServerResponse(
                    message="User successfully created",
                    message_code=USER_SUCCESSFULLY_CREATED,
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
