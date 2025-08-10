import logging
from db.mongo_client import Connection
from decouple import config
from bson.objectid import ObjectId

# usa ADMIN_COLLECTION o por defecto 'user_admin'
__dbmanager__ = Connection(config('ADMIN_COLLECTION', default='user_admin'))

def get_by_email(email: str):
    try:
        return __dbmanager__.find_one({'admin_email': email})
    except Exception as e:
        logging.error(f"DB error in get_by_email: {str(e)}", exc_info=True)
        return None

def create_admin(doc: dict):
    try:
        return __dbmanager__.create_data(doc)
    except Exception as e:
        logging.error(f"DB error creating admin: {str(e)}", exc_info=True)
        return None

def list_admins(query: dict):
    try:
        return __dbmanager__.get_by_query(query)
    except Exception as e:
        logging.error(f"DB error listing admins: {str(e)}", exc_info=True)
        return []

def get_by_id(id: str):
    try:
        return __dbmanager__.get_by_id(id)
    except Exception as e:
        logging.error(f"DB error get_by_id: {str(e)}", exc_info=True)
        return None

def update_by_id(id: str, new_data: dict):
    try:
        return __dbmanager__.update_by_condition({'_id': ObjectId(id)}, new_data)
    except Exception as e:
        logging.error(f"DB error update_by_id: {str(e)}", exc_info=True)
        return None
