#!/usr/bin/env python3
"""
Script para probar la estructura simplificada de roles (solo app_id)
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

def test_create_role_simplified(token):
    """Probar creación de rol con estructura simplificada"""
    print("\n📝 Probando creación de rol con estructura simplificada...")
    
    role_data = {
        "name": "TestRoleSimplified",
        "description": "Rol de prueba con estructura simplificada",
        "permissions": ["Read", "Write", "Delete", "Update"]
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
            print(f"Respuesta completa: {json.dumps(data, indent=2)}")
            
            # Verificar estructura simplificada
            role_info = data.get('data', {})
            
            print(f"\n📊 Verificación de estructura simplificada:")
            print(f"  - admin_id: {role_info.get('admin_id')}")
            print(f"  - app_id: {role_info.get('app_id')}")
            print(f"  - app: {role_info.get('app', 'NO EXISTE')}")
            print(f"  - app_client_id: {role_info.get('app_client_id', 'NO EXISTE')}")
            
            # Verificar que NO existen los campos eliminados
            if 'app' not in role_info and 'app_client_id' not in role_info:
                print("✅ Estructura correcta - campos app y app_client_id eliminados")
                return data.get('data', {}).get('name')
            else:
                print("❌ Error: Se encontraron campos que deberían estar eliminados")
                return None
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
                
                # Verificar estructura simplificada
                if 'app' not in first_role and 'app_client_id' not in first_role:
                    print("✅ Roles existentes también tienen estructura simplificada")
                else:
                    print("⚠️  Roles existentes aún tienen campos app/app_client_id")
            
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
    print("🚀 Iniciando pruebas de estructura simplificada de roles")
    print("=" * 60)
    
    # 1. Login
    token = test_admin_login()
    if not token:
        print("❌ No se pudo obtener token. Abortando pruebas.")
        return
    
    # 2. Crear rol con estructura simplificada
    role_name = test_create_role_simplified(token)
    
    # 3. Obtener roles
    test_get_roles(token)
    
    # 4. Eliminar rol de prueba
    if role_name:
        test_delete_role(token, role_name)
    
    print("\n" + "=" * 60)
    print("✅ Pruebas completadas")

if __name__ == "__main__":
    main()
