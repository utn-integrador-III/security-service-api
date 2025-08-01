def validate_password(password):
    if len(password) < 8:
        return "The password must be at least 8 characters long."
    return None
