import logging
from db.mongo_client import Connection
from decouple import config
from bson.objectid import ObjectId

__dbmanager__ = Connection(config('USER_COLLECTION'))

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
    if result is None or result.matched_count == 0:
        logging.error("Token update failed: No matching user or error during update.")
        return False

    return True