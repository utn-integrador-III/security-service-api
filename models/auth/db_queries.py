from db.mongo_client import Connection
from decouple import config

__dbmanager__ = Connection(config("USER_COLLECTION"))
def find_user_by_email(email):
    user = __dbmanager__.collection.find_one({"email": email})
    return user
