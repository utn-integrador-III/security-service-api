# models/apps/db_queries.py
import logging
from db.mongo_client import Connection
from decouple import config
from bson.objectid import ObjectId

__dbmanager__ = Connection(config('APPS_COLLECTION', default='apps'))

def get_by_name(name: str):
    try:
        return __dbmanager__.find_one({'name': name})
    except Exception as e:
        logging.error(f"DB error in get_by_name: {str(e)}", exc_info=True)
        return None

def create_app(doc: dict):
    try:
        return __dbmanager__.create_data(doc)
    except Exception as e:
        logging.error(f"DB error creating app: {str(e)}", exc_info=True)
        return None

def list_apps(query: dict):
    try:
        return __dbmanager__.get_by_query(query)
    except Exception as e:
        logging.error(f"DB error listing apps: {str(e)}", exc_info=True)
        return []

def get_by_id(id: str):
    try:
        return __dbmanager__.get_by_id(id)
    except Exception as e:
        logging.error(f"DB error get_by_id: {str(e)}", exc_info=True)
        return None

def get_by_admin_id(admin_id: str):
    try:
        return __dbmanager__.get_by_query({'admin_id': ObjectId(admin_id)})
    except Exception as e:
        logging.error(f"DB error get_by_admin_id: {str(e)}", exc_info=True)
        return []

def update_by_id(id: str, new_data: dict):
    try:
        return __dbmanager__.update_by_condition({'_id': ObjectId(id)}, new_data)
    except Exception as e:
        logging.error(f"DB error update_by_id: {str(e)}", exc_info=True)
        return None
