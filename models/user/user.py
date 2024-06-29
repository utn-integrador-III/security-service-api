import logging
from utils.encryption_utils import EncryptionUtil
from models.user.db_queries import __dbmanager__

class UserModel:
    def __init__(self, name, email, password, status=None, verification_code=None, expiration_time=None, _id=None):
        self.name = name
        self.email = email
        self.password = password
        self.status = status
        self.verification_code = verification_code
        self.expiration_time = expiration_time
        self._id = _id
    
    def to_dict(self):
        return {
            'name': self.name,
            'email': self.email,
            'password': self.password,
            'status': self.status,
            'verification_code': self.verification_code,
            'expiration_time': self.expiration_time,
            '_id': self._id
        }
    
    @classmethod
    def create_user(cls, user_data):
        try:
            # Encriptar la contraseña
            encryption_util = EncryptionUtil()
            user_data['password'] = encryption_util.encrypt(user_data['password'])
            
            # Insertar el usuario en la base de datos
            result = __dbmanager__.create_data(user_data)
            
            if result:
                return cls(**user_data)
            else:
                raise Exception("Failed to create user in database")
        except Exception as e:
            logging.error(f"Error creating user: {str(e)}", exc_info=True)
            raise Exception('Error creating user')

    @staticmethod
    def find_by_email(email):
        try:
            return __dbmanager__.find_by_email(email)
        except Exception as e:
            logging.error(f"Error finding user by email: {str(e)}", exc_info=True)
            raise Exception('Error finding user by email')
