from pymongo import MongoClient
from decouple import config

class MongoDB:
    def __init__(self):
        mongo_url = config("MONGO_URL")
        mongo_db = config("MONGO_DB")
        self.client = MongoClient(mongo_url)
        self.db = self.client[mongo_db]

    def get_collection(self, collection_name):
        return self.db[collection_name]

    def close(self):
        self.client.close()
