import logging
from flask import request
from flask_restful import Resource
from models.user.user import UserModel
from utils.auth_manager import generate_verification_code
from utils.server_response import ServerResponse, StatusCode
from utils.encryption_utils import EncryptionUtil
from utils.password_validator import validate_password
from utils.message_codes import (
    MISSING_REQUIRED_FIELDS,
    USER_NOT_FOUND,
    USER_NOT_ACTIVE,
    INVALID_OLD_PASSWORD,
    PASSWORDS_DO_NOT_MATCH,
    PASSWORD_UPDATED_SUCCESSFULLY,
    UNEXPECTED_ERROR_OCCURRED,
    PASSWORD_RESET_INITIATED,
    UPDATE_USER_FAILED,
)
from utils.email_manager import send_email_new_password
from datetime import datetime, timedelta
import random
import string

class UserPasswordController(Resource):
    route = '/user/password'

    def put(self):
        try:
            data = request.json
            user_email = data.get('user_email')
            old_password = data.get('old_password')
            new_password = data.get('new_password')
            confirm_password = data.get('confirm_password')

            if not all([user_email, old_password, new_password, confirm_password]):
                return ServerResponse(
                    message="All fields are required: user_email, old_password, new_password, confirm_password",
                    message_code=MISSING_REQUIRED_FIELDS,
                    status=StatusCode.BAD_REQUEST
                ).to_response()

            # Buscar usuario por email
            user = UserModel.find_by_email(user_email)
            if not user:
                return ServerResponse(
                    message="User not found",
                    message_code=USER_NOT_FOUND,
                    status=StatusCode.NOT_FOUND
                ).to_response()

            # Verificar estado del usuario
            if user['status'] != 'Active':
                return ServerResponse(
                    message="User is not active",
                    message_code=USER_NOT_ACTIVE,
                    status=StatusCode.FORBIDDEN
                ).to_response()

            # Verificar contraseña antigua
            encryption_util = EncryptionUtil()
            if not UserModel.verify_password(old_password, user['password']):
                return ServerResponse(
                    message="Old password is incorrect",
                    message_code=INVALID_OLD_PASSWORD,
                    status=StatusCode.UNAUTHORIZED
                ).to_response()

            # Validar nueva contraseña
            validation_message = validate_password(new_password)
            if validation_message:
                return ServerResponse(
                    message=validation_message,
                    status=StatusCode.BAD_REQUEST
                ).to_response()

            if new_password != confirm_password:
                return ServerResponse(
                    message="New password and confirm password do not match",
                    message_code=PASSWORDS_DO_NOT_MATCH,
                    status=StatusCode.BAD_REQUEST
                ).to_response()

            # Encriptar nueva contraseña
            encrypted_password = encryption_util.encrypt(new_password)

            # Actualizar contraseña
            UserModel.update_password(user_email, encrypted_password)

            return ServerResponse(
                message="Password updated successfully",
                message_code=PASSWORD_UPDATED_SUCCESSFULLY,
                status=StatusCode.OK
            ).to_response()

        except Exception as e:
            logging.error(f"An error occurred: {str(e)}", exc_info=True)
            return ServerResponse(
                message="An unexpected error occurred.",
                message_code=UNEXPECTED_ERROR_OCCURRED,
                status=StatusCode.INTERNAL_SERVER_ERROR
            ).to_response()

    def post(self):
        try:
            data = request.json
            user_email = data.get('email')
            if not user_email:
                return ServerResponse(
                    message="User email is required",
                    message_code=MISSING_REQUIRED_FIELDS,
                    status=StatusCode.BAD_REQUEST
                ).to_response()
            user = UserModel.find_by_email(user_email)
            if not user:
                return ServerResponse(
                    message="User not found",
                    message_code=USER_NOT_FOUND,
                    status=StatusCode.NOT_FOUND
                ).to_response()
            verification_code = generate_verification_code()
            expiration_time = datetime.utcnow() + timedelta(minutes=5)
            email_prefix = user_email.split('@')[0]
            temporal_password = f"{email_prefix}{verification_code}"
            encryption_util = EncryptionUtil()
            encrypted_temp_password = encryption_util.encrypt(temporal_password)
            update_result = UserModel.update_reset_password_info(
                user_email,
                verification_code,
                expiration_time,
                encrypted_temp_password
            )
            if update_result:
                send_email_new_password(user_email, temporal_password)
                return ServerResponse(
                    message="Password reset initiated",
                    message_code=PASSWORD_RESET_INITIATED,
                    status=StatusCode.OK
                ).to_response()
            if not update_result:
                return ServerResponse(
                    message="Failed to update user information",
                    message_code=UPDATE_USER_FAILED,
                    status=StatusCode.INTERNAL_SERVER_ERROR
                ).to_response()    
            else:
                return ServerResponse(
                    message="Failed to update user",
                    status=StatusCode.INTERNAL_SERVER_ERROR
                ).to_response()
        except Exception as e:
            logging.error(f"An error occurred: {str(e)}", exc_info=True)
            return ServerResponse(
                message="An unexpected error occurred.",
                message_code=UNEXPECTED_ERROR_OCCURRED,
                status=StatusCode.INTERNAL_SERVER_ERROR
            ).to_response()