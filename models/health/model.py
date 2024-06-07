from pymongo import MongoClient, errors

# ================================================================
# D A T A A C C E S S C O D E
# ================================================================
# Create connection with MongoDb

class HealthModel():

    # @classmethod
    def contextDB():
        try:
            conex = MongoClient(
                host='mongodb+srv://db-mongodb-nyc1-88903-b647ee80.mongo.ondigitalocean.com',
                username='doadmin', password='15fec6A2m890NI4n',
                serverSelectionTimeoutMS=5000  # 5 seconds timeout
            )
            # Attempt to retrieve server information to check connection
            conex.server_info()
            return conex
        except errors.ServerSelectionTimeoutError as err:
            print(f"Error connecting to MongoDB: {err}")
            return None