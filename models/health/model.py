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
        return info_db