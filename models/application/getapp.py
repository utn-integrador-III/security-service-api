from db.mongo_client import Connection
from datetime import datetime
import uuid
import bcrypt

class ApplicationModel:
    def __init__(self):
        self.collection = Connection('apps')

    def find_by_client_id(self, client_id):
        return self.collection.find_one({'client_id': client_id})