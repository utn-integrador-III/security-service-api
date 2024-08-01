import logging
from db.mongo_client import Connection
from decouple import config
from bson.objectid import ObjectId

__dbmanager__ = Connection(config('USER_COLLECTION'))