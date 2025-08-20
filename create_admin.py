#!/usr/bin/env python3
"""
Script para crear un admin en la base de datos
"""
import os
import bcrypt
from datetime import datetime
from pymongo import MongoClient
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Configuración de MongoDB
MONGO_URL = os.getenv("MONGO_URL")
client = MongoClient(MONGO_URL)
db = client['security']
admin_collection = db['user_admin']

def create_admin_if_not_exists(email, password):
    """
    Crear un admin si no existe
    """
    # Verificar si ya existe
    existing_admin = admin_collection.find_one({"admin_email": email})
    
    if existing_admin:
        print(f"✅ Admin {email} ya existe en la base de datos")
        return existing_admin
    
    # Crear nuevo admin
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    admin_data = {
        "admin_email": email,
        "password_secret": hashed_password,
        "status": "active",
        "creation_date": datetime.utcnow()
    }
    
    result = admin_collection.insert_one(admin_data)
    
    if result.inserted_id:
        print(f"✅ Admin {email} creado exitosamente")
        print(f"   ID: {result.inserted_id}")
        return admin_data
    else:
        print(f"❌ Error al crear admin {email}")
        return None

def list_all_admins():
    """
    Listar todos los admins
    """
    admins = admin_collection.find({})
    print("\n📋 Admins existentes:")
    for admin in admins:
        print(f"   - {admin['admin_email']} (ID: {admin['_id']}, Status: {admin.get('status', 'active')})")

if __name__ == "__main__":
    # Crear el admin específico
    admin_email = "contrerasaaron447111111@est.utn.ac.cr"
    admin_password = "Secret123*"
    
    print("🔧 Creando admin...")
    create_admin_if_not_exists(admin_email, admin_password)
    
    # Listar todos los admins
    list_all_admins()
    
    print("\n🎯 Ahora puedes probar el login con:")
    print(f"   Email: {admin_email}")
    print(f"   Password: {admin_password}")
    print(f"   Endpoint: POST http://localhost:5002/auth/admin/login")
