from models.auth.db_queries import find_user_by_email

class UserModel:

    @staticmethod
    def find_by_email(email):
        user = find_user_by_email(email)
        return user

    @staticmethod
    def verify_password(input_password, stored_password):
        return input_password == stored_password
