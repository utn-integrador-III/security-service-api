from models.auth.db_queries import __dbmanager__

def find_user_by_email(email):
    user = __dbmanager__.collection.find_one({"email": email})
    return user
class UserModel:

    @staticmethod
    def find_by_email(email):
        user = find_user_by_email(email)
        return user

    @staticmethod
    def verify_password(input_password, stored_password):
        return input_password == stored_password
