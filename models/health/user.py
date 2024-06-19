from pymongo import MongoClient
from decouple import config

class UserModel:
    @staticmethod
    def create_user(user_data):
        # Conexión a la base de datos MongoDB Atlas
        client = MongoClient(config('MONGO_URL'))
        db = client.get_database('student_service_dev')
        users_collection = db.user
        
        # Insertar usuario en la colección
        users_collection.insert_one(user_data)
    
    @staticmethod
    def find_by_email(email):
        # Conectar a la base de datos MongoDB Atlas
        client = MongoClient(config('MONGO_URL'))
        db = client.get_database('student_service_dev')
        users_collection = db.user
        
        # Buscar usuario por correo electrónico
        return users_collection.find_one({'email': email})
