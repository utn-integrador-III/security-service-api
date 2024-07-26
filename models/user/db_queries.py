import logging
from db.mongo_client import Connection
from decouple import config
from bson.objectid import ObjectId

__dbmanager__ = Connection(config('USER_COLLECTION'))

def update_token(self, user_id, token):
    try:
        # Asegúrate de que user_id esté en formato ObjectId si usas MongoDB
        if isinstance(user_id, str):
            user_id = ObjectId(user_id)
        
        result = self.collection.update_one(
            {'_id': user_id},
            {'$set': {'token': token}}
        )
        # Verifica si se realizó alguna modificación
        if result.modified_count == 0:
            logging.warning(f"No document updated with user_id: {user_id}")
        return result.modified_count > 0
    except Exception as e:
        logging.error(f"Error updating token: {str(e)}", exc_info=True)
        return False