from pymongo import MongoClient
from decouple import config
import logging


class Connection:

    def __init__(self, collection_name):
        self.collection = None
        self.db = None
        self.connect(collection_name)

    def connect(self, collection_name):
        uri = config('MONGO_URL')
        db = config('MONGO_DB')
        self.collection = MongoClient(uri)[db][collection_name]

    def get_all_data(self):
        try:
            result = self.collection.find({})
        except Exception as e:
            return e
        return result

    def get_by_query(self, query):
        try:
            result = self.collection.find(query)
        except Exception as e:
            return e
        return result

    def get_by_id(self, id):
        try:
            result = self.collection.find({'id':id})
        except Exception as e:
            return e
        return result
    
    def create_data(self, data):
        try:
            return self.collection.insert_one(data)
        except Exception as e:
            return e

    def update_data(self, id, new_deal_data):
        try:
            self.collection.update_one(
                {"id": id},
                {"$set": new_deal_data}
            )
        except Exception as e:
            return e

    def delete_data(self, id):
        try:
            return self.collection.delete_one({'id': id})
        except Exception as e:
            return e
    
    def find_by_email(self, email):
        try:
            return self.collection.find_one({'email': email})
        except Exception as e:
            logging.error(f"Database error in find_by_email: {str(e)}", exc_info=True)
            raise
        