from db.mongo_client import Connection
from datetime import datetime
from bson.objectid import ObjectId
import uuid
import bcrypt
import logging

class ApplicationModel:
    def __init__(self):
        self.collection = Connection('apps')

    @classmethod
    def find_by_client_id(cls, admin_id):
        try:
            collection = Connection('apps')  # Crear una nueva conexión para la colección 'apps'
            result = collection.find_one({'admin_id': admin_id})
            print(f"Application found for admin_id {admin_id}: {result}")
           
            print(result)
            return result if result else None
        except Exception as e:
            logging.exception(f"Error finding application by admin_id: {str(e)}")
            return None