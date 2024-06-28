from pymongo import MongoClient
from decouple import config
from utils.encryption_utils import EncryptionUtil

class UserModel:
    @staticmethod
    def create_user(user_data):
        encryption_util = EncryptionUtil()
        encrypted_password = encryption_util.encrypt(user_data['password'])
        user_data['password'] = encrypted_password

        client = MongoClient(config('MONGO_URL'))
        db = client.get_database(config('MONGO_DB'))
        users_collection = db.get_collection(config('USER_COLLECTION'))

        users_collection.insert_one(user_data)
    
    @staticmethod
    def find_by_email(email):
        client = MongoClient(config('MONGO_URL'))
        db = client.get_database(config('MONGO_DB'))
        users_collection = db.get_collection(config('USER_COLLECTION'))

        return users_collection.find_one({'email': email})
