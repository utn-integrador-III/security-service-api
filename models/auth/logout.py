from models.auth.db_queries import __dbmanager__, find_by_email, update_by_condition

class LogoutModel:
    @staticmethod
    def find_by_email(email):
        try:
            return find_by_email(email)
        except Exception as e:
            raise Exception(f"Error in find_by_email: {str(e)}")
    
    def logout_user(email):
        try:
            update_by_condition({'email': email}, {'token': '', 'is_session_active': False})
        except Exception as e:
            raise Exception(f"Error logging out user: {str(e)}")
