from flask import request, jsonify
from pymongo import MongoClient
import bcrypt
import os
from dotenv import load_dotenv

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

    user_data = {
        "name": data["name"],
        "password": hashed_password.decode('utf-8'),
        "email": data["email"],
        "apps": data["apps"]
    }

    result = collection.insert_one(user_data)
    return jsonify({"message": "Usuario registrado correctamente", "id": str(result.inserted_id)}), 201
