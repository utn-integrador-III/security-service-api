import logging
from bson import ObjectId
from utils.encryption_utils import EncryptionUtil
from models.user.db_queries import __dbmanager__, update_token, update_password

class UserModel:
    def __init__(self, name, password, email, status, apps, is_session_active=False):
        self.name = name
        self.password = password
        self.email = email
        self.status = status
        self.apps = apps
        self.is_session_active = is_session_active
    
    def to_dict(self):
        return {
            'name': self.name,
            'email': self.email,
            'password': self.password,
            'status': self.status,
            'apps': self.apps,
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
                return cls(
                    name=user_data['name'],
                    password=user_data['password'],
                    email=user_data['email'],
                    status=user_data['status'],
                    apps=user_data['apps'],
                    is_session_active=user_data.get('is_session_active', False)
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
            __dbmanager__.update_by_condition({'email': email}, {'is_session_active': False})
        except Exception as e:
            raise Exception(f"Error logging out user: {str(e)}")

    @staticmethod
    def verify_password(plain_password, encrypted_password):
        encryption_util = EncryptionUtil()
        return encryption_util.verify_password(plain_password, encrypted_password)

    @classmethod
    def update_password(cls, email, new_password):
        try:
            result = __dbmanager__.update_by_condition(
                {"email": email},
                {"password": new_password}
            )
        
            if not result:
                raise Exception("Failed to update password in the database")
        except Exception as e:
            logging.error(f"Error updating password: {str(e)}", exc_info=True)
            raise Exception('Error updating password')
        
    @staticmethod
    def update_reset_password_info(user_email, verification_code, expiration_time, encrypted_temp_password):
        try:
            update_data = {
                'password': encrypted_temp_password,
                'status': 'blocked',
                # In case you use code verification again, you should add it to each `app`.
            }
            result = __dbmanager__.update_by_condition({'email': user_email}, update_data)
            if result is None or result.matched_count == 0:
                logging.warning(f"Failed to update reset password info for user: {user_email}. User not found or no changes made.")
                return False
            else:
                logging.info(f"Successfully updated reset password info for user: {user_email}")
                return True
        except Exception as e:
            logging.error(f"Error updating reset password info: {str(e)}", exc_info=True)
            raise Exception('Error updating reset password info')

    @staticmethod
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

    @staticmethod
    def user_activation(email):
        try:
            modif = {
                'is_session_active': False,
                'status': 'Active'
                # If you need to modify the states of the apps or tokens, you should update the apps array as well.
            }
            return __dbmanager__.update_by_condition({'email': email}, modif)
        except Exception as e:
            logging.error(f"Error saving user to database: {str(e)}", exc_info=True)
            raise Exception('Error saving user to database')
        
    @staticmethod
    def update_user(email, update_data):
        try:
            result = __dbmanager__.update_by_condition({'email': email}, update_data)
            if result is None or result.matched_count == 0:
                logging.warning(f"Failed to update user: {email}. User not found or no changes made.")
                return False
            else:
                logging.info(f"Successfully updated user: {email}")
                return True
        except Exception as e:
            logging.error(f"Error updating user: {str(e)}", exc_info=True)
            raise Exception('Error updating user')
