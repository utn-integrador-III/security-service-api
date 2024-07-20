import logging
from datetime import datetime
from flask import request
from flask_restful import Resource
from models.auth.auth import UserModel
from utils.server_response import ServerResponse, StatusCode
from utils.message_codes import (
    INVALID_VERIFICATION_CODE, VERIFICATION_SUCCESSFUL, VERIFICATION_EXPIRED
)

class VerifyCodeController(Resource):
    route = '/auth/verify'
    STATIC_VERIFICATION_CODE = 123456  # Código de verificación estático para pruebas

    def post(self):
        try:
            data = request.json
            logging.debug(f"Data received: {data}")

            email = data.get('email')
            code = data.get('code')
            
            # Verificar que el email y el código estén presentes
            if not email or not code:
                logging.warning("Email or verification code not provided")
                return ServerResponse(
                    message="Email and verification code are required",
                    status=StatusCode.BAD_REQUEST
                )
            
            # Buscar el usuario por email
            user = UserModel.find_by_email(email)
            if not user:
                logging.warning(f"User not found for email: {email}")
                return ServerResponse(
                    message="User not found",
                    status=StatusCode.NOT_FOUND
                )
            
            logging.debug(f"User found: {user}")

            # Verificar el código de verificación (usando el código estático)
            if code != str(self.STATIC_VERIFICATION_CODE):
                logging.warning(f"Invalid verification code for user: {email}")
                return ServerResponse(
                    message="Invalid verification code",
                    message_code=INVALID_VERIFICATION_CODE,
                    status=StatusCode.UNPROCESSABLE_ENTITY
                )
            
            # Omitir la verificación de la expiración del código para pruebas
            # if datetime.utcnow() > user['expiration_code']:
            #     logging.warning(f"Verification code expired for user: {email}")
            #     return ServerResponse(
            #         message="Verification code expired",
            #         message_code=VERIFICATION_EXPIRED,
            #         status=StatusCode.UNPROCESSABLE_ENTITY
            #     )
            
            # Si todo es correcto, actualizar el estado del usuario
            user['status'] = 'Active'
            UserModel.save_to_db(user)
            
            return ServerResponse(
                message="Verification successful",
                message_code=VERIFICATION_SUCCESSFUL,
                status=StatusCode.OK
            )
        
        except Exception as e:
            logging.error(f"An unexpected error occurred: {str(e)}", exc_info=True)
            return ServerResponse(
                message="An unexpected error occurred.",
                status=StatusCode.INTERNAL_SERVER_ERROR
            )
