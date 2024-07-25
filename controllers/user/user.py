# controllers/user.py
from flask_restful import Resource
from flask import request, make_response
from models.user.user import UserModel
from utils.server_response import ServerResponse, StatusCode
from utils.message_codes import (
    USER_NOT_FOUND, INVALID_VERIFICATION_CODE, VERIFICATION_EXPIRED, VERIFICATION_SUCCESSFUL
)
import logging
from datetime import datetime

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
            
            user = UserModel.find_by_email(email)
            
            if not user:
                return ServerResponse(
                    message="User not found",
                    message_code=USER_NOT_FOUND,
                    status=StatusCode.NOT_FOUND
                )
            
            if user.verification_code != code:
                return ServerResponse(
                    message="Invalid verification code",
                    message_code=INVALID_VERIFICATION_CODE,
                    status=StatusCode.UNAUTHORIZED
                )
            
            if user.expiration_code < datetime.utcnow():
                return ServerResponse(
                    message="Verification code expired",
                    message_code=VERIFICATION_EXPIRED,
                    status=StatusCode.UNAUTHORIZED
                )
            
            if user.status != 'Pending':
                return ServerResponse(
                    message="User is not in a pending state",
                    status=StatusCode.BAD_REQUEST
                )
            
            user.status = 'Active'
            user.token = ""
            user.is_session_active = False
            user.expiration_code = None
            user.verification_code = None
            UserModel.save_to_db(user)
            
            return ServerResponse(
                message="User successfully verified",
                message_code=VERIFICATION_SUCCESSFUL,
                status=StatusCode.OK
            )
        
        except Exception as e:
            logging.error(f"An unexpected error occurred: {str(e)}", exc_info=True)
            return ServerResponse(
                message="An unexpected error occurred.",
                status=StatusCode.INTERNAL_SERVER_ERROR
            )
