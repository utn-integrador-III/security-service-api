from flask import request, jsonify
from models.health.user import UserModel
import random
import string
from datetime import datetime, timedelta

class UserController:
    @staticmethod
    def register():
        data = request.json
        email = data.get('email')
        
        # Validar dominio de correo electrónico
        if not email.endswith('@est.utn.ac.cr'):
            return jsonify({"error": "Invalid email domain"}), 400
        
        # Verificar si el usuario ya está registrado
        existing_user = UserModel.find_by_email(email)
        if existing_user and existing_user['status'] == "Active":
            return jsonify({"error": "User already registered"}), 400
        elif existing_user and existing_user['status'] == "Pending":
            return jsonify({"message": "User already registered, request a new verification code"}), 200
        
        # Generar código de verificación y establecer tiempo de expiración
        verification_code = ''.join(random.choices(string.digits, k=4))
        expiration_time = datetime.utcnow() + timedelta(minutes=5)
        
        # Creación del usuario en MongoDB
        user_data = {
            'email': email,
            'status': 'Pending',
            'verification_code': verification_code,
            'expiration_time': expiration_time
        }
        UserModel.create_user(user_data)
    
        
        return jsonify({"message": "User registered successfully, please verify your email"}), 200
