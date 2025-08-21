#!/usr/bin/env python3
"""
Script para probar que el app_id se guarda como ObjectId
"""
import requests
import json
from datetime import datetime
from bson import ObjectId

BASE_URL = "http://localhost:5002"

def login_admin():
    """Login como admin"""
    url = f"{BASE_URL}/auth/admin/login"
    data = {
        "email": "admin@test.com",
        "password": "admin123"
    }
    
    response = requests.post(url, json=data)
    if response.status_code == 200:
        return response.json()["data"]["token"]
    else:
        print(f"❌ Error en login: {response.status_code}")
        print(response.text)
        return None

def create_test_role(token, admin_id):
    """Crear un rol de prueba y verificar app_id como ObjectId"""
    url = f"{BASE_URL}/rol"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    role_data = {
        "name": f"test_role_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
        "description": "Rol de prueba con app_id como ObjectId",
        "permissions": ["read", "write"],
        "admin_id": admin_id
    }
    
    print(f"📤 Enviando datos del rol: {json.dumps(role_data, indent=2)}")
    
    response = requests.post(url, json=role_data, headers=headers)
    print(f"📥 Respuesta: {response.status_code}")
    
    if response.status_code == 201:
        created_role = response.json()["data"]
        print(f"✅ Rol creado exitosamente:")
        print(f"   - ID: {created_role.get('_id')}")
        print(f"   - Nombre: {created_role.get('name')}")
        print(f"   - Admin ID: {created_role.get('admin_id')} (tipo: {type(created_role.get('admin_id'))})")
        print(f"   - App ID: {created_role.get('app_id')} (tipo: {type(created_role.get('app_id'))})")
        
        # Verificar que app_id es un ObjectId válido
        app_id = created_role.get('app_id')
        if app_id:
            try:
                # Intentar convertir a ObjectId para verificar
                obj_id = ObjectId(app_id)
                print(f"✅ App ID es un ObjectId válido: {obj_id}")
            except Exception as e:
                print(f"❌ App ID no es un ObjectId válido: {e}")
        else:
            print("⚠️ App ID es None")
        
        return created_role
    else:
        print(f"❌ Error creando rol: {response.status_code}")
        print(response.text)
        return None

def main():
    print("🧪 Probando que app_id se guarda como ObjectId")
    print("=" * 50)
    
    # Login
    token = login_admin()
    if not token:
        return
    
    # Extraer admin_id del token (simulado)
    admin_id = "68a590ebec92b4ab68f630d5"  # ID de ejemplo
    
    # Crear rol
    created_role = create_test_role(token, admin_id)
    
    if created_role:
        print("\n✅ Prueba completada exitosamente")
        print("📋 Estructura final del rol:")
        print(json.dumps(created_role, indent=2, default=str))
        
        # Verificar tipos de datos
        print("\n🔍 Verificación de tipos:")
        print(f"   - admin_id: {type(created_role.get('admin_id'))} = {created_role.get('admin_id')}")
        print(f"   - app_id: {type(created_role.get('app_id'))} = {created_role.get('app_id')}")
    else:
        print("\n❌ Prueba falló")

if __name__ == "__main__":
    main()
