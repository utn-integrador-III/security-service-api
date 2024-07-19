from db.mongo_client import Connection
from decouple import config

__dbmanager__ = Connection(config("USER_COLLECTION"))

def find_by_email(email):
    user = __dbmanager__.collection.find_one({"email": email})
    if user:
        user['id'] = str(user.pop('_id'))  # Convert ObjectId to string and assign it to 'id'
    return user

def update_by_condition(condition, update_values):
    __dbmanager__.collection.update_one(condition, {'$set': update_values})
