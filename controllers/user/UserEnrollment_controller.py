import logging
from datetime import datetime, timedelta
from dateutil.parser import isoparse
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
            verification_code = data.get('verification_code')
            expiration_code = data.get('expiration_code')
            provided_roles = data.get('roles', [])
            
            # Validar email
            if not email or not validate_email(email):
                return ServerResponse(
                    message="The provided email is not valid",
                    message_code=INVALID_EMAIL_DOMAIN,
                    status=StatusCode.UNPROCESSABLE_ENTITY
                )
            if 'utn.ac.cr' not in email:
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
                
                # Obtener roles activos y predeterminados
                default_roles = RoleModel.find_active_default_roles()
                
                # Validar que haya al menos un rol activo y predeterminado
                if not default_roles:
                    return ServerResponse(
                        message="No active default roles found",
                        status=StatusCode.UNPROCESSABLE_ENTITY
                    )
                
                # Filtrar nombres de roles válidos
                valid_role_names = [role['name'] for role in default_roles if 'name' in role]

                # Validar que se haya encontrado al menos un nombre de rol válido
                if not valid_role_names:
                    return ServerResponse(
                        message="No valid role names found",
                        status=StatusCode.UNPROCESSABLE_ENTITY
                    )

                # Validar que todos los roles proporcionados existan en la base de datos
                for role in provided_roles:
                    if role not in valid_role_names:
                        return ServerResponse(
                            message=f"Role '{role}' is not a valid role",
                            message_code=INVALID_ROLE,
                            status=StatusCode.UNPROCESSABLE_ENTITY
                        )

                # Convertir el código de expiración a formato datetime
                try:
                    expiration_time = isoparse(expiration_code)
                except ValueError:
                    return ServerResponse(
                        message="Invalid expiration code format",
                        status=StatusCode.UNPROCESSABLE_ENTITY
                    )
                
                # Crear nuevo usuario
                user_data = {
                    'name': name,
                    'password': password,
                    'email': email,
                    'status': 'Pending',
                    'verification_code': int(verification_code),
                    'expiration_code': expiration_time,
                    'roles': provided_roles if provided_roles else valid_role_names
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