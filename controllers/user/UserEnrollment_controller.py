import logging
import random
from datetime import datetime, timedelta
from flask import request, Response
from flask_restful import Resource
from validate_email import validate_email
from models.user.user import UserModel
from models.role.role import RoleModel
from utils.email_manager import send_email
from utils.server_response import ServerResponse, StatusCode
from utils.message_codes import (
    CREATED, INVALID_EMAIL_DOMAIN, INVALID_NAME, INVALID_PASSWORD, USER_ALREADY_REGISTERED, NO_ACTIVE_ROLES_FOUND, DEFAULT_ROLE_NOT_FOUND, USER_CREATION_ERROR, UNEXPECTED_ERROR
)

class UserEnrollmentController(Resource):
    route = '/user/enrollment'

    def post(self):
        try:
            data = request.json
            name = data.get('name')
            password = data.get('password')
            email = data.get('email')

            # Validar email
            if not email or not validate_email(email):
                return ServerResponse(
                    message="The provided email is not valid",
                    message_code=INVALID_EMAIL_DOMAIN,
                    status=StatusCode.UNPROCESSABLE_ENTITY
                ).to_response()

            if not any(domain in email for domain in ['utn.ac.cr', 'est.utn.ac.cr', 'adm.utn.ac.cr']):
                return ServerResponse(
                    message="The entered domain does not meet the established standards",
                    message_code=INVALID_EMAIL_DOMAIN,
                    status=StatusCode.UNPROCESSABLE_ENTITY
                ).to_response()

            # Validar nombre
            if not name or len(name.strip()) < 2:
                return ServerResponse(
                    message="The name does not meet the established standards",
                    message_code=INVALID_NAME,
                    status=StatusCode.UNPROCESSABLE_ENTITY
                ).to_response()

            # Validar contraseña
            if not password or len(password) < 8:
                return ServerResponse(
                    message="The password does not meet the established standards",
                    message_code=INVALID_PASSWORD,
                    status=StatusCode.UNPROCESSABLE_ENTITY
                ).to_response()

            try:
                # Verificar si el usuario ya existe
                existing_user = UserModel.find_by_email(email)
                if existing_user:
                    return ServerResponse(
                        message="The user is already registered",
                        message_code=USER_ALREADY_REGISTERED,
                        status=StatusCode.CONFLICT
                    ).to_response()

                # Obtener roles activos y el rol predeterminado
                active_roles, default_role = RoleModel.find_active_and_default_roles()

                # Validar que haya al menos un rol activo
                if not active_roles:
                    return ServerResponse(
                        message="No active roles found",
                        message_code=NO_ACTIVE_ROLES_FOUND,
                        status=StatusCode.UNPROCESSABLE_ENTITY
                    ).to_response()

                # Validar que se haya encontrado un rol predeterminado
                if not default_role:
                    return ServerResponse(
                        message="Default role not found",
                        message_code=DEFAULT_ROLE_NOT_FOUND,
                        status=StatusCode.INTERNAL_SERVER_ERROR
                    ).to_response()

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
                    'role': default_role['name'],
                    'token': "",
                    'is_session_active': False
                }

                new_user = UserModel.create_user(user_data)
                send_email(email, verification_code)

                return ServerResponse(
                    data=None,
                    message="User created successfully",
                    message_code=CREATED,
                    status=StatusCode.CREATED,
                ).to_response()
            except Exception as e:
                logging.error(f"Error creating user: {str(e)}", exc_info=True)
                return ServerResponse(
                    message="Error creating user",
                    message_code=USER_CREATION_ERROR,
                    status=StatusCode.INTERNAL_SERVER_ERROR
                ).to_response()

        except Exception as e:
            logging.error(f"An unexpected error occurred: {str(e)}", exc_info=True)
            return ServerResponse(
                message="An unexpected error occurred.",
                message_code=UNEXPECTED_ERROR,
                status=StatusCode.INTERNAL_SERVER_ERROR
            ).to_response()