import logging

from bson import ObjectId
from utils.encryption_utils import EncryptionUtil
from models.user.db_queries import __dbmanager__

class UserModel:
    def __init__(self, name, password, email, status, verification_code, expiration_code, role, token="", is_session_active=False):
        self.name = name
        self.password = password
        self.email = email
        self.status = status
        self.verification_code = verification_code
        self.expiration_code = expiration_code
        self.role = role
        self.token = token
        self.is_session_active = is_session_active
    
    def to_dict(self):
        return {
            'name': self.name,
            'email': self.email,
            'password': self.password,
            'status': self.status,
            'verification_code': self.verification_code,
            'expiration_code': self.expiration_code,
            'role': self.role,
            'token': self.token,
            'is_session_active': self.is_session_active
        }
    
    @classmethod
    def create_user(cls, user_data):
        try:
            # Encrypt password
            encryption_util = EncryptionUtil()
            user_data['password'] = encryption_util.encrypt(user_data['password'])
            
            # Insert the user in the database
            result = __dbmanager__.create_data(user_data)
            
            if result:
                # Create UserModel instance with expected fields
                return cls(
                    name=user_data['name'],
                    password=user_data['password'],
                    email=user_data['email'],
                    status=user_data['status'],
                    verification_code=user_data['verification_code'],
                    expiration_code=user_data['expiration_code'],
                    role=user_data['role'],
                    token=user_data['token'],
                    is_session_active=user_data['is_session_active']
                )
            else:
                raise Exception("Failed to create user in database")
        except Exception as e:
            logging.error(f"Error creating user: {str(e)}", exc_info=True)
            raise Exception('Error creating user')

     
    @staticmethod
    def find_by_email(email):
        try:
            user = __dbmanager__.find_by_email(email)
            if user:
                user['id'] = str(user.pop('_id'))
            return user
        except Exception as e:
            raise Exception(f"Error in find_by_email: {str(e)}")
        
    @staticmethod
    def logout_user(email):
        try:
             __dbmanager__.update_by_condition({'email': email}, {'token': '', 'is_session_active': False})
        except Exception as e:
            raise Exception(f"Error logging out user: {str(e)}")

    @staticmethod
    def verify_password(plain_password, encrypted_password):
        encryption_util = EncryptionUtil()
        return encryption_util.verify_password(plain_password, encrypted_password)


    @classmethod
    def update_password(cls, email, new_password):
        try:
            __dbmanager__.update_password(email, new_password)
        except Exception as e:
            logging.error(f"Error updating password: {str(e)}", exc_info=True)
            raise Exception('Error updating password')
        
    @staticmethod
    def update_reset_password_info(user_email, verification_code, expiration_time, encrypted_temp_password):
        try:
            update_data = {
                'verification_code': verification_code,
                'expiration_code': expiration_time,
                'password': encrypted_temp_password,
                'status': 'blocked'
            }
            result = __dbmanager__.update_by_condition({'email': user_email}, update_data)
            if result:
                logging.info(f"Successfully updated reset password info for user: {user_email}")
                return True
            else:
                logging.warning(f"Failed to update reset password info for user: {user_email}. User not found or no changes made.")
                return False
        except Exception as e:
            logging.error(f"Error updating reset password info: {str(e)}", exc_info=True)
            raise Exception('Error updating reset password info')

    def update_token(user_id, token):
        try:
            object_id = ObjectId(user_id)
        except Exception as e:
            logging.error(f"Error converting user_id to ObjectId: {e}")
            return False

        condition = {'_id': object_id}
        new_data = {
            'token': token,
            'is_session_active': True
        }

        result = __dbmanager__.update_by_condition(condition, new_data)

        if isinstance(result, bool):
            return result  

        if result is None or result.matched_count == 0:
            logging.error("Token update failed: No matching user or error during update.")
            return False

        return True
