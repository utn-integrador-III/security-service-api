from models.auth.db_queries import __dbmanager__
from utils.encryption_utils import EncryptionUtil

def find_user_by_email(email):
    user = __dbmanager__.collection.find_one({"email": email})
    if user:
        user['id'] = str(user.pop('_id'))  #Convert ObjectId to string and assign it to 'id'
    return user

class LogoutModel:
    @staticmethod
    def find_by_email(email):
        try:
            return find_user_by_email(email)
        except Exception as e:
            raise Exception(f"Error in find_by_email: {str(e)}")
    
    def logout_user(email):
        try:
            __dbmanager__.collection.update_one({'email': email}, {'$set': {'token': "", 'is_session_active': False}})
        except Exception as e:
            raise Exception(f"Error logging out user: {str(e)}")

