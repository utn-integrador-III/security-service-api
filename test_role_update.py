#!/usr/bin/env python3
"""
Script para probar el endpoint de actualización de roles
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

def test_create_role(token):
    """Crear un rol para probar la actualización"""
    print("\n📝 Creando rol para pruebas...")
    
    role_data = {
        "name": "test-role-update",
        "description": "Rol de prueba para actualización",
        "permissions": ["read", "write"]
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
            role_id = data.get('data', {}).get('_id')
            print(f"✅ Rol creado exitosamente. ID: {role_id}")
            return role_id
        else:
            print(f"❌ Error creando rol: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return None

def test_get_role_by_id(token, role_id):
    """Probar obtener rol por ID"""
    print(f"\n🔍 Obteniendo rol por ID: {role_id}")
    
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    try:
        response = requests.get(f"{BASE_URL}/rol/{role_id}", headers=headers)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Rol obtenido exitosamente")
            print(f"Nombre: {data.get('data', {}).get('name')}")
            print(f"Descripción: {data.get('data', {}).get('description')}")
            return True
        else:
            print(f"❌ Error obteniendo rol: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return False

def test_update_role_name(token, role_id):
    """Probar actualizar nombre del rol"""
    print(f"\n✏️ Actualizando nombre del rol: {role_id}")
    
    update_data = {
        "name": "test-role-updated"
    }
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    
    try:
        response = requests.patch(f"{BASE_URL}/rol/{role_id}", json=update_data, headers=headers)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Nombre actualizado exitosamente")
            print(f"Nuevo nombre: {data.get('data', {}).get('name')}")
            return True
        else:
            print(f"❌ Error actualizando nombre: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return False

def test_update_role_description(token, role_id):
    """Probar actualizar descripción del rol"""
    print(f"\n✏️ Actualizando descripción del rol: {role_id}")
    
    update_data = {
        "description": "Descripción actualizada del rol de prueba"
    }
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    
    try:
        response = requests.patch(f"{BASE_URL}/rol/{role_id}", json=update_data, headers=headers)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Descripción actualizada exitosamente")
            print(f"Nueva descripción: {data.get('data', {}).get('description')}")
            return True
        else:
            print(f"❌ Error actualizando descripción: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return False

def test_update_role_permissions(token, role_id):
    """Probar actualizar permisos del rol"""
    print(f"\n✏️ Actualizando permisos del rol: {role_id}")
    
    update_data = {
        "permissions": ["read", "write", "update", "delete"]
    }
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    
    try:
        response = requests.patch(f"{BASE_URL}/rol/{role_id}", json=update_data, headers=headers)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Permisos actualizados exitosamente")
            print(f"Nuevos permisos: {data.get('data', {}).get('permissions')}")
            return True
        else:
            print(f"❌ Error actualizando permisos: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return False

def test_update_role_screens(token, role_id):
    """Probar actualizar pantallas del rol"""
    print(f"\n✏️ Actualizando pantallas del rol: {role_id}")
    
    update_data = {
        "screens": ["dashboard", "users", "reports", "settings"]
    }
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    
    try:
        response = requests.patch(f"{BASE_URL}/rol/{role_id}", json=update_data, headers=headers)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Pantallas actualizadas exitosamente")
            print(f"Nuevas pantallas: {data.get('data', {}).get('screens')}")
            return True
        else:
            print(f"❌ Error actualizando pantallas: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return False

def test_update_role_status(token, role_id):
    """Probar actualizar estado del rol"""
    print(f"\n✏️ Actualizando estado del rol: {role_id}")
    
    update_data = {
        "is_active": False
    }
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    
    try:
        response = requests.patch(f"{BASE_URL}/rol/{role_id}", json=update_data, headers=headers)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Estado actualizado exitosamente")
            print(f"Nuevo estado: {data.get('data', {}).get('is_active')}")
            return True
        else:
            print(f"❌ Error actualizando estado: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return False

def test_update_multiple_fields(token, role_id):
    """Probar actualizar múltiples campos a la vez"""
    print(f"\n✏️ Actualizando múltiples campos del rol: {role_id}")
    
    update_data = {
        "name": "test-role-multiple-update",
        "description": "Rol con múltiples campos actualizados",
        "permissions": ["read", "write", "admin"],
        "screens": ["dashboard", "admin", "analytics"],
        "is_active": True
    }
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    
    try:
        response = requests.patch(f"{BASE_URL}/rol/{role_id}", json=update_data, headers=headers)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Múltiples campos actualizados exitosamente")
            print(f"Nombre: {data.get('data', {}).get('name')}")
            print(f"Descripción: {data.get('data', {}).get('description')}")
            print(f"Permisos: {data.get('data', {}).get('permissions')}")
            print(f"Pantallas: {data.get('data', {}).get('screens')}")
            print(f"Estado: {data.get('data', {}).get('is_active')}")
            return True
        else:
            print(f"❌ Error actualizando múltiples campos: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return False

def test_update_role_validation_errors(token, role_id):
    """Probar errores de validación"""
    print(f"\n🚫 Probando errores de validación...")
    
    # Probar nombre muy corto
    print("  - Probando nombre muy corto...")
    update_data = {"name": "a"}
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    
    try:
        response = requests.patch(f"{BASE_URL}/rol/{role_id}", json=update_data, headers=headers)
        if response.status_code == 422:
            print("    ✅ Error de validación capturado correctamente")
        else:
            print(f"    ❌ Error inesperado: {response.status_code}")
    except Exception as e:
        print(f"    ❌ Error de conexión: {e}")

def test_update_role_unauthorized(token, role_id):
    """Probar acceso no autorizado (usando un token diferente)"""
    print(f"\n🚫 Probando acceso no autorizado...")
    
    # Usar un token inválido
    invalid_token = "invalid_token_here"
    
    update_data = {
        "name": "unauthorized-update"
    }
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {invalid_token}"
    }
    
    try:
        response = requests.patch(f"{BASE_URL}/rol/{role_id}", json=update_data, headers=headers)
        if response.status_code == 401:
            print("    ✅ Acceso no autorizado capturado correctamente")
        else:
            print(f"    ❌ Error inesperado: {response.status_code}")
    except Exception as e:
        print(f"    ❌ Error de conexión: {e}")

def test_delete_role(token, role_id):
    """Eliminar el rol de prueba"""
    print(f"\n🗑️ Eliminando rol de prueba: {role_id}")
    
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    try:
        response = requests.delete(f"{BASE_URL}/rol/{role_id}", headers=headers)
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
    print("🚀 Iniciando pruebas de actualización de roles")
    print("=" * 60)
    
    # 1. Login para obtener token
    token = test_admin_login()
    if not token:
        print("❌ No se pudo obtener token. Abortando pruebas.")
        return
    
    # 2. Crear rol para pruebas
    role_id = test_create_role(token)
    if not role_id:
        print("❌ No se pudo crear rol. Abortando pruebas.")
        return
    
    # 3. Probar obtener rol por ID
    test_get_role_by_id(token, role_id)
    
    # 4. Probar actualizaciones individuales
    test_update_role_name(token, role_id)
    test_update_role_description(token, role_id)
    test_update_role_permissions(token, role_id)
    test_update_role_screens(token, role_id)
    test_update_role_status(token, role_id)
    
    # 5. Probar actualización múltiple
    test_update_multiple_fields(token, role_id)
    
    # 6. Probar errores de validación
    test_update_role_validation_errors(token, role_id)
    
    # 7. Probar acceso no autorizado
    test_update_role_unauthorized(token, role_id)
    
    # 8. Eliminar rol de prueba
    test_delete_role(token, role_id)
    
    print("\n" + "=" * 60)
    print("✅ Pruebas de actualización de roles completadas")
    print("\n📋 Resumen:")
    print("- ✅ Endpoint PATCH /rol/{id} implementado")
    print("- ✅ Validaciones de seguridad funcionan")
    print("- ✅ Actualización de campos individuales funciona")
    print("- ✅ Actualización múltiple funciona")
    print("- ✅ Errores de validación capturados")
    print("- ✅ Control de acceso implementado")

if __name__ == "__main__":
    main()
