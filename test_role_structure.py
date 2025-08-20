#!/usr/bin/env python3
"""
Script para probar la nueva estructura de roles con app_id
"""

import requests
import json

# Configuración
BASE_URL = "http://localhost:5002"

def test_admin_login():
    """Probar login de admin para obtener token"""
    print("🔐 Probando login de admin...")
    
    login_data = {
        "email": "contrerasaaron447111111@est.utn.ac.cr",
        "password": "123456"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/auth/admin/login", json=login_data)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            token = data.get('data', {}).get('token')
            print(f"✅ Login exitoso. Token obtenido: {token[:50]}...")
            return token
        else:
            print(f"❌ Error en login: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return None

def test_create_role_with_app_id(token):
    """Probar creación de rol con app_id"""
    print("\n📝 Probando creación de rol con app_id...")
    
    role_data = {
        "name": "TestRoleWithAppId",
        "description": "Rol de prueba con app_id",
        "permissions": ["Read", "Write", "Delete"]
    }
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/rol", json=role_data, headers=headers)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 201:
            data = response.json()
            print("✅ Rol creado exitosamente")
            print(f"Respuesta: {json.dumps(data, indent=2)}")
            return data.get('data', {}).get('name')
        else:
            print(f"❌ Error creando rol: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return None

def test_get_roles(token):
    """Probar obtención de roles"""
    print("\n📋 Probando obtención de roles...")
    
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    try:
        response = requests.get(f"{BASE_URL}/rol", headers=headers)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Roles obtenidos exitosamente")
            print(f"Total de roles: {len(data.get('data', []))}")
            
            # Mostrar estructura del primer rol
            roles = data.get('data', [])
            if roles:
                first_role = roles[0]
                print(f"\n📊 Estructura del primer rol:")
                print(json.dumps(first_role, indent=2, default=str))
            
            return True
        else:
            print(f"❌ Error obteniendo roles: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return False

def test_delete_role(token, role_name):
    """Probar eliminación de rol"""
    if not role_name:
        print("❌ No hay rol para eliminar")
        return False
        
    print(f"\n🗑️ Probando eliminación del rol: {role_name}")
    
    delete_data = {
        "role_name": role_name
    }
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    
    try:
        response = requests.delete(f"{BASE_URL}/rol", json=delete_data, headers=headers)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ Rol eliminado exitosamente")
            return True
        else:
            print(f"❌ Error eliminando rol: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return False

def main():
    """Función principal"""
    print("🚀 Iniciando pruebas de estructura de roles con app_id")
    print("=" * 60)
    
    # 1. Login
    token = test_admin_login()
    if not token:
        print("❌ No se pudo obtener token. Abortando pruebas.")
        return
    
    # 2. Crear rol
    role_name = test_create_role_with_app_id(token)
    
    # 3. Obtener roles
    test_get_roles(token)
    
    # 4. Eliminar rol de prueba
    if role_name:
        test_delete_role(token, role_name)
    
    print("\n" + "=" * 60)
    print("✅ Pruebas completadas")

if __name__ == "__main__":
    main()
