from flask_restful import Resource
from flask import request
from email_validator import validate_email, EmailNotValidError
from datetime import datetime, timedelta
import random
import string
from models.user.user import UserModel
from utils.server_response import ServerResponse, StatusCode
from utils.message_codes import (
    USER_ALREADY_REGISTERED_GENERATING_NEW_CODE,
    USER_ALREADY_REGISTERED,
    INVALID_EMAIL_DOMAIN,
    USER_SUCCESSFULLY_CREATED,
    INVALID_NAME,
    INVALID_PASSWORD
)

class UserController(Resource):
    route = '/register'

    def post(self):
        data = request.json
        name = data.get('name')
        password = data.get('password')
        email = data.get('email')
        
        try:
            valid = validate_email(email)
            email = valid.email
            if not (email.endswith('@est.utn.ac.cr') or email.endswith('@utn.ac.cr')):
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
        
        if not name or len(name.strip()) == 0:
            return ServerResponse(
                message="The name does not meet the established standards", 
                message_code=INVALID_NAME, 
                status=StatusCode.UNPROCESSABLE_ENTITY
            )

        if not password or len(password) < 8:
            return ServerResponse(
                message="The password does not meet the established standards", 
                message_code=INVALID_PASSWORD, 
                status=StatusCode.UNPROCESSABLE_ENTITY
            )

        user = UserModel.find_by_email(email)
        if user and user['status'] == "Active":
            return ServerResponse(
                message="The user is already registered", 
                message_code=USER_ALREADY_REGISTERED, 
                status=StatusCode.CONFLICT
            )
        elif user and user['status'] == "Pending":
            return ServerResponse(
                message="The user is already registered, generating a new code", 
                message_code=USER_ALREADY_REGISTERED_GENERATING_NEW_CODE, 
                status=StatusCode.OK
            )
        
        verification_code = ''.join(random.choices(string.digits, k=4))
        expiration_time = datetime.utcnow() + timedelta(minutes=5)
        
        user_data = {
            'name': name,
            'password': password,
            'email': email,
            'status': 'Pending',
            'verification_code': verification_code,
            'expiration_time': expiration_time
        }
        
        UserModel.create_user(user_data)
    
        return ServerResponse(
            message="User successfully created", 
            message_code=USER_SUCCESSFULLY_CREATED, 
            status=StatusCode.OK
        )
