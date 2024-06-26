from flask import request
from flask_restful import Resource
from email_validator import validate_email, EmailNotValidError
from datetime import datetime, timedelta
import random
import string
from models.user.user import UserModel
from utils.encryption_utils import EncryptionUtil
from utils.server_response import ServerResponse, StatusCode
from utils.message_codes import (
    USER_ALREDY_REGISTERED_GENERATING_NEW_CODE,
    USER_ALREDY_REGISTERED,
    INVALID_EMAIL_DOMAIN,
    USER_SUCCESSFULLY_CREATED,
    INVALID_NAME,
    INVALID_PASSWORD
)

class UserController(Resource):
    def post(self):
        data = request.json
        name = data.get('name')
        password = data.get('password')
        email = data.get('email')
        
        try:
            valid = validate_email(email)
            email = valid.email
            if not (email.endswith('@est.utn.ac.cr') or email.endswith('@utn.ac.cr')):
                return ServerResponse(message=INVALID_EMAIL_DOMAIN, message_code='The entered domain does not meet the established standards', status=StatusCode.UNPROCESSABLE_ENTITY)
        except EmailNotValidError as e:
            return ServerResponse(message=str(e), status=StatusCode.UNPROCESSABLE_ENTITY)
        
        if not name or len(name.strip()) == 0:
            return ServerResponse(message=INVALID_NAME, message_code='The name does not meet the established standards', status=StatusCode.UNPROCESSABLE_ENTITY)

        if not password or len(password) < 8:
            return ServerResponse(message=INVALID_PASSWORD, message_code='The password does not meet the established standards', status=StatusCode.UNPROCESSABLE_ENTITY)

        user = UserModel.find_by_email(email)
        if user and user['status'] == "Active":
            return ServerResponse(message=USER_ALREDY_REGISTERED, message_code='The user is already registered', status=StatusCode.CONFLICT)
        elif user and user['status'] == "Pending":
            return ServerResponse(message=USER_ALREDY_REGISTERED_GENERATING_NEW_CODE, message_code='The user is already registered, generating a new code', status=StatusCode.OK)
        
        verification_code = ''.join(random.choices(string.digits, k=4))
        expiration_time = datetime.utcnow() + timedelta(minutes=5)

        encryption_util = EncryptionUtil()
        hashed_password = encryption_util.encrypt(password)
        
        user_data = {
            'name': name,
            'password': hashed_password,
            'email': email,
            'status': 'Pending',
            'verification_code': verification_code,
            'expiration_time': expiration_time
        }
        
        UserModel.create_user(user_data)
    
        return ServerResponse(message=USER_SUCCESSFULLY_CREATED, message_code='User successfully created',status=StatusCode.OK)
        
