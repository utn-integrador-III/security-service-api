from flask import request, jsonify
from pymongo import MongoClient
import bcrypt
import os
from dotenv import load_dotenv
import random
from datetime import datetime, timedelta
from utils.email_manager import send_email
import uuid

# Cargar variables de entorno
load_dotenv()

MONGO_URL = os.getenv("MONGO_URL")
if not MONGO_URL:
    raise Exception("Falta la variable MONGO_URL en el archivo .env")

client = MongoClient(MONGO_URL)
db = client['security']
collection = db['user']

def register_security_user():
    data = request.get_json()

    if not all(k in data for k in ("name", "password", "email", "apps")):
        return jsonify({"error": "Faltan campos requeridos"}), 400

    # Verificar si ya existe un usuario con ese email
    if collection.find_one({"email": data["email"]}):
        return jsonify({"error": "Ya existe un usuario con ese correo"}), 409

    hashed_password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())

    # Generar código de verificación y expiración
    verification_code = random.randint(100000, 999999)
    expiration_code = datetime.utcnow() + timedelta(minutes=5)

    # Procesar apps para agregar campos de verificación y app_id
    apps = data["apps"]
    for app in apps:
        app.setdefault("code", str(verification_code))
        app.setdefault("token", "")
        app.setdefault("status", "Pending")
        app.setdefault("code_expliration", expiration_code.strftime("%Y/%m/%d %H:%M:%S"))
        app.setdefault("app_id", str(uuid.uuid4()))  # Generar ID único para cada app

    user_data = {
        "name": data["name"],
        "password": hashed_password.decode('utf-8'),
        "email": data["email"],
        "apps": apps,
        "status": "Pending",
        "token": "",
        "is_session_active": False,
        "current_app_id": None,
        "current_app": None,
        "last_login": None
    }

    result = collection.insert_one(user_data)
    
    # Enviar el código por email
    try:
        send_email(data["email"], verification_code)
    except Exception as e:
        # Si falla el envío de email, eliminar el usuario creado
        collection.delete_one({"_id": result.inserted_id})
        return jsonify({"error": "Error al enviar el código de verificación por email"}), 500
    
    return jsonify({
        "message": "Usuario registrado correctamente. Se ha enviado un código de verificación a tu email.", 
        "id": str(result.inserted_id)
    }), 201
