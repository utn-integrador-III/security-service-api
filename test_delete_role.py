#!/usr/bin/env python3
"""
Script para probar el endpoint de eliminar roles
"""
import requests
import json

def test_delete_role():
    """
    Probar el endpoint DELETE /rol para eliminar un rol
    """
    try:
        print("🔍 Probando endpoint de eliminar roles...")
        
        # Primero hacer login para obtener token
        login_url = "http://localhost:5002/auth/admin/login"
        login_data = {
            "email": "contrerasaaron447111111@est.utn.ac.cr",
            "password": "Secret123*"
        }
        
        print("🔐 Haciendo login para obtener token...")
        login_response = requests.post(login_url, json=login_data, headers={"Content-Type": "application/json"})
        
        if login_response.status_code != 200:
            print(f"❌ Error en login: {login_response.status_code}")
            print(f"Login response: {login_response.text}")
            return
        
        token = login_response.json()['data']['token']
        print("✅ Login exitoso, token obtenido")
        
        # Primero crear un rol para luego eliminarlo
        create_role_url = "http://localhost:5002/rol"
        role_data = {
            "name": "TestRoleToDelete",
            "description": "Rol de prueba para eliminar",
            "permissions": ["read", "write"]
        }
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}"
        }
        
        print(f"\n🔍 Creando rol para eliminar...")
        create_response = requests.post(create_role_url, json=role_data, headers=headers)
        
        if create_response.status_code != 201:
            print(f"❌ Error creando rol: {create_response.status_code}")
            print(f"Create response: {create_response.text}")
            return
        
        print("✅ Rol creado exitosamente")
        
        # Ahora eliminar el rol
        delete_role_url = "http://localhost:5002/rol"
        delete_data = {
            "role_name": "TestRoleToDelete"
        }
        
        print(f"\n🔍 Eliminando rol...")
        print(f"URL: {delete_role_url}")
        print(f"Data: {json.dumps(delete_data, indent=2)}")
        
        delete_response = requests.delete(delete_role_url, json=delete_data, headers=headers)
        
        print(f"\n📊 Respuesta:")
        print(f"Status Code: {delete_response.status_code}")
        print(f"Status Text: {delete_response.status_text}")
        
        if delete_response.status_code == 200:
            print("✅ ¡ÉXITO! Rol eliminado correctamente")
            response_data = delete_response.json()
            print(f"Mensaje: {response_data.get('message', 'No message')}")
        else:
            print("❌ Error al eliminar rol")
            print(f"Respuesta: {delete_response.text}")
            
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
    print("🚀 Iniciando pruebas del endpoint de eliminar roles...\n")
    
    if test_health_endpoint():
        print("✅ Servidor está corriendo")
        print("\n" + "="*50)
        test_delete_role()
    else:
        print("❌ Servidor no está corriendo")
        print("\n💡 Para iniciar el servidor, ejecuta:")
        print("   python run_server.py")
