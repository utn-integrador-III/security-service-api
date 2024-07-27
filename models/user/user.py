import logging
from utils.encryption_utils import EncryptionUtil
from models.user.db_queries import __dbmanager__
from models.user.db_queries import update_token

class UserModel:
    def __init__(self, name, password, email, status, verification_code, expiration_code, roles):
        self.name = name
        self.password = password
        self.email = email
        self.status = status
        self.verification_code = verification_code
        self.expiration_code = expiration_code
        self.roles = roles
    
    def to_dict(self):
        return {
            'name': self.name,
            'email': self.email,
            'password': self.password,
            'status': self.status,
            'verification_code': self.verification_code,
            'expiration_code': self.expiration_code
        }
    
    @classmethod
    def create_user(cls, user_data):
        try:
            encryption_util = EncryptionUtil()
            user_data['password'] = encryption_util.encrypt(user_data['password'])
            result = __dbmanager__.create_data(user_data)
            
            if result:
                return cls(
                    name=user_data['name'],
                    password=user_data['password'],
                    email=user_data['email'],
                    status=user_data['status'],
                    verification_code=user_data['verification_code'],
                    expiration_code=user_data['expiration_code'],
                    roles=user_data['roles']
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
            logging.error(f"Error finding user by email: {str(e)}", exc_info=True)
            raise Exception('Error finding user by email')

    @staticmethod
    def verify_password(plain_password, encrypted_password):
        encryption_util = EncryptionUtil()
        return encryption_util.verify_password(plain_password, encrypted_password)


    @classmethod
    def update_password(cls, email, new_password):
        try:
            return __dbmanager__.update_data(user.to_dict())
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
            success = update_token(user_id, token)
            return success
        except Exception as e:
            logging.error(f"Error updating token: {str(e)}", exc_info=True)
            return False
