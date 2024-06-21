from pymongo import MongoClient
from decouple import config

class UserModel:
    @staticmethod
    def create_user(user_data):
       
        client = MongoClient(config('MONGO_URL'))
        db = client.get_database('student_service_dev')
        users_collection = db.user
      
        users_collection.insert_one(user_data)
    
    @staticmethod
    def find_by_email(email):
    
        client = MongoClient(config('MONGO_URL'))
        db = client.get_database('student_service_dev')
        users_collection = db.user
        
        
        return users_collection.find_one({'email': email})
