#!/usr/bin/env python3
"""
Script para probar el endpoint de crear roles
"""
import requests
import json

def test_create_role():
    """
    Probar el endpoint POST /rol para crear un rol
    """
    try:
        print("🔍 Probando endpoint de crear roles...")
        
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
        
        # Probar crear un rol
        create_role_url = "http://localhost:5002/rol"
        role_data = {
            "name": "TestRole",
            "description": "Rol de prueba para testing",
            "permissions": ["read", "write", "delete"]
        }
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}"
        }
        
        print(f"\n🔍 Probando crear rol...")
        print(f"URL: {create_role_url}")
        print(f"Data: {json.dumps(role_data, indent=2)}")
        
        create_response = requests.post(create_role_url, json=role_data, headers=headers)
        
        print(f"\n📊 Respuesta:")
        print(f"Status Code: {create_response.status_code}")
        print(f"Status Text: {create_response.status_text}")
        
        if create_response.status_code == 201:
            print("✅ ¡ÉXITO! Rol creado correctamente")
            response_data = create_response.json()
            print(f"Mensaje: {response_data.get('message', 'No message')}")
            print(f"Rol creado: {response_data.get('data', {}).get('name', 'No name')}")
        else:
            print("❌ Error al crear rol")
            print(f"Respuesta: {create_response.text}")
            
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
    print("🚀 Iniciando pruebas del endpoint de crear roles...\n")
    
    if test_health_endpoint():
        print("✅ Servidor está corriendo")
        print("\n" + "="*50)
        test_create_role()
    else:
        print("❌ Servidor no está corriendo")
        print("\n💡 Para iniciar el servidor, ejecuta:")
        print("   python run_server.py")
