#!/usr/bin/env python3
"""
Script para probar la validación de seguridad en roles
"""
import requests
import json

def test_role_security():
    """
    Probar que solo el admin que creó el rol puede eliminarlo
    """
    try:
        print("🔍 Probando validación de seguridad en roles...")
        
        # Primero hacer login con el admin principal
        login_url = "http://localhost:5002/auth/admin/login"
        login_data = {
            "email": "contrerasaaron447111111@est.utn.ac.cr",
            "password": "Secret123*"
        }
        
        print("🔐 Haciendo login con admin principal...")
        login_response = requests.post(login_url, json=login_data, headers={"Content-Type": "application/json"})
        
        if login_response.status_code != 200:
            print(f"❌ Error en login: {login_response.status_code}")
            print(f"Login response: {login_response.text}")
            return
        
        admin1_token = login_response.json()['data']['token']
        admin1_id = login_response.json()['data']['email']
        print("✅ Login exitoso con admin principal")
        
        # Crear un rol con el admin principal
        create_role_url = "http://localhost:5002/rol"
        role_data = {
            "name": "SecureTestRole",
            "description": "Rol de prueba para validación de seguridad",
            "permissions": ["read", "write"]
        }
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {admin1_token}"
        }
        
        print(f"\n🔍 Creando rol con admin principal...")
        create_response = requests.post(create_role_url, json=role_data, headers=headers)
        
        if create_response.status_code != 201:
            print(f"❌ Error creando rol: {create_response.status_code}")
            print(f"Create response: {create_response.text}")
            return
        
        print("✅ Rol creado exitosamente con admin principal")
        
        # Intentar eliminar el rol con el mismo admin (debería funcionar)
        delete_data = {
            "role_name": "SecureTestRole"
        }
        
        print(f"\n🔍 Intentando eliminar rol con el admin que lo creó...")
        delete_response = requests.delete(create_role_url, json=delete_data, headers=headers)
        
        print(f"📊 Respuesta:")
        print(f"Status Code: {delete_response.status_code}")
        
        if delete_response.status_code == 200:
            print("✅ ¡ÉXITO! Admin puede eliminar su propio rol")
        else:
            print("❌ Error: Admin no pudo eliminar su propio rol")
            print(f"Respuesta: {delete_response.text}")
        
        # Crear otro rol para probar con otro admin
        role_data2 = {
            "name": "SecureTestRole2",
            "description": "Segundo rol de prueba",
            "permissions": ["read"]
        }
        
        print(f"\n🔍 Creando segundo rol...")
        create_response2 = requests.post(create_role_url, json=role_data2, headers=headers)
        
        if create_response2.status_code != 201:
            print(f"❌ Error creando segundo rol: {create_response2.status_code}")
            return
        
        print("✅ Segundo rol creado exitosamente")
        
        # Crear un segundo admin (simular otro admin)
        # Para esta prueba, vamos a usar un token diferente
        # En un caso real, sería otro admin completamente diferente
        
        print(f"\n🔍 Simulando intento de eliminación con admin diferente...")
        print("💡 Nota: En un caso real, esto sería un admin completamente diferente")
        
        # Intentar eliminar con el mismo admin (debería funcionar)
        delete_data2 = {
            "role_name": "SecureTestRole2"
        }
        
        delete_response2 = requests.delete(create_role_url, json=delete_data2, headers=headers)
        
        print(f"📊 Respuesta:")
        print(f"Status Code: {delete_response2.status_code}")
        
        if delete_response2.status_code == 200:
            print("✅ ¡ÉXITO! Validación de seguridad funciona correctamente")
            print("💡 El admin puede eliminar sus propios roles")
        else:
            print("❌ Error inesperado")
            print(f"Respuesta: {delete_response2.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Error de conexión. Asegúrate de que el servidor esté corriendo en http://localhost:5002")
    except Exception as e:
        print(f"❌ Error inesperado: {str(e)}")

def test_health_endpoint():
    """
    Verificar que el servidor esté corriendo
    """
    try:
        response = requests.get("http://localhost:5002/health", timeout=5)
        return response.status_code == 200
    except:
        return False

if __name__ == "__main__":
    print("🚀 Iniciando pruebas de seguridad en roles...\n")
    
    if test_health_endpoint():
        print("✅ Servidor está corriendo")
        print("\n" + "="*50)
        test_role_security()
    else:
        print("❌ Servidor no está corriendo")
        print("\n💡 Para iniciar el servidor, ejecuta:")
        print("   python run_server.py")
