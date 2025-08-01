from db.mongo_client import Connection
from datetime import datetime
import uuid
import bcrypt

class ApplicationModel:
    def __init__(self):
        self.collection = Connection('apps')

    def create_application(self, data):
        try:
            client_id = str(uuid.uuid4())
            client_secret_raw = str(uuid.uuid4())
            hashed_secret = bcrypt.hashpw(client_secret_raw.encode('utf-8'), bcrypt.gensalt())

            app_data = {
                'name': data['name'],
                'admin_email': data['admin_email'],
                'redirect_url': data['redirect_url'],
                'client_id': client_id,
                'password': hashed_secret.decode('utf-8'),
                'creation_date': datetime.utcnow(),
                'status': 'active'
            }
            self.collection.create_data(app_data)
            return {'client_id': client_id, 'password_secret': client_secret_raw}
        except Exception as e:
            # Consider logging the error
            return None

    def find_by_name(self, name):
        return self.collection.find_one({'name': name})
