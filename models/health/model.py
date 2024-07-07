<<<<<<< HEAD
from models.health.db_queries import __dbmanager__


# ================================================================
# D A T A A C C E S S C O D E
# ================================================================
# Create connection with MongoDb

class HealthModel():

    # @classmethod
    def getInfoDB():
        info_db = []
        response = __dbmanager__.get_all_data()
        for info in response:
            try:
                info_db.append(info)
            except Exception as ex:
                raise Exception(ex)
=======
from models.health.db_queries import __dbmanager__


# ================================================================
# D A T A A C C E S S C O D E
# ================================================================
# Create connection with MongoDb

class HealthModel():

    # @classmethod
    def getInfoDB():
        info_db = []
        response = __dbmanager__.get_all_data()
        for info in response:
            try:
                info_db.append(info)
            except Exception as ex:
                raise Exception(ex)
>>>>>>> 3700107 (Document the endpoint to enroll a new user. In swagger.yml add the endpoint inside Auth section & the existing endpoint with the path /register was changed to the correct /auth/enrollment)
        return info_db