from models.auth.db_queries import __dbmanager__
from utils.encryption_utils import EncryptionUtil

def find_user_by_email(email):
    user = __dbmanager__.collection.find_one({"email": email})
    return user

class UserModel:
    @staticmethod
    def find_by_email(email):
        user = find_user_by_email(email)
        return user

    @staticmethod
    def verify_password(input_password, stored_password):
        encryption_util = EncryptionUtil()   
        decrypted_stored_password = encryption_util.decrypt(stored_password)
        return input_password == decrypted_stored_password
