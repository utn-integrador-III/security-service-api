from pymongo import MongoClient
from decouple import config
import logging
from bson.objectid import ObjectId


class Connection:

    def __init__(self, collection_name):
        self.collection = None
        self.db = None
        self.connect(collection_name)

    def connect(self, collection_name):
        uri = config("MONGO_URL")
        db = config("MONGO_DB")
        self.collection = MongoClient(uri)[db][collection_name]

    def get_all_data(self):
        try:
            result = self.collection.find({})
        except Exception as e:
            return e
        return result
    
    def find_one(self, name):
        try:
            result = self.collection.find_one(name)
            return result
        except Exception as e:
            logging.exception(e)
            return str(e)
        
    def get_by_query(self, query):
        try:
            result = self.collection.find(query)
        except Exception as e:
            return e
        return result

    def get_by_id(self, id):
        try:
            result = self.collection.find_one({"_id": ObjectId(id)})
        except Exception as e:
            return e
        return result

    def create_data(self, data):
        try:
            return self.collection.insert_one(data)
        except Exception as e:
            return e
        
    def update_by_id(self, id, new_data):
        try:
            result = self.collection.update_one({"_id": ObjectId(id)}, {"$set": new_data})
            return result.modified_count > 0
        except Exception as e:
            logging.exception("Error updating data by id: %s", str(e))
            return False

    def update_by_condition(self, condition, new_data):
        try:
            return self.collection.update_one(condition, {"$set": new_data})
        except Exception as e:
            logging.exception(e)
            raise e

    def update_data(self, id, new_data):
        try:
            result = self.collection.update_one({"_id": ObjectId(id)}, {"$set": new_data})
            return result.modified_count > 0
        except Exception as e:
            logging.exception(e)
            return str(e)

    def delete_data(self, id):
        try:
            result = self.collection.delete_one({"_id": ObjectId(id)})
            if result.deleted_count > 0:
                return True
            else:
                return False
        except Exception as e:
            return e
    
    def find_by_email(self, email):
        try:
            return self.collection.find_one({'email': email})
        except Exception as e:
            logging.error(f"Database error in find_by_email: {str(e)}", exc_info=True)
            raise
        