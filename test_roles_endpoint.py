#!/usr/bin/env python3
"""
Script para probar el endpoint de roles
"""
import requests
import json

def test_roles_endpoint():
    """
    Probar el endpoint de roles
    """
    # Primero hacer login para obtener token
    login_url = "http://localhost:5002/auth/admin/login"
    login_data = {
        "email": "contrerasaaron447111111@est.utn.ac.cr",
        "password": "Secret123*"
    }
    
    try:
        print("🔐 Haciendo login para obtener token...")
        login_response = requests.post(login_url, json=login_data, headers={"Content-Type": "application/json"})
        
        if login_response.status_code != 200:
            print(f"❌ Error en login: {login_response.status_code}")
            return
        
        token = login_response.json()['data']['token']
        print("✅ Login exitoso, token obtenido")
        
        # Probar endpoint de roles
        roles_url = "http://localhost:5002/rol"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}"
        }
        
        print("\n🔍 Probando endpoint de roles...")
        print(f"URL: {roles_url}")
        
        roles_response = requests.get(roles_url, headers=headers)
        
        print(f"\n📊 Respuesta:")
        print(f"Status Code: {roles_response.status_code}")
        
        if roles_response.status_code == 200:
            print("✅ ¡ÉXITO! Roles obtenidos correctamente")
            response_data = roles_response.json()
            print(f"Mensaje: {response_data.get('message', 'No message')}")
            print(f"Cantidad de roles: {len(response_data.get('data', []))}")
            
            # Mostrar los roles
            roles = response_data.get('data', [])
            if roles:
                print("\n📋 Roles encontrados:")
                for i, role in enumerate(roles, 1):
                    print(f"  {i}. {role.get('name', 'Sin nombre')} - {role.get('description', 'Sin descripción')}")
            else:
                print("  No hay roles en la base de datos")
        else:
            print("❌ Error al obtener roles")
            print(f"Respuesta: {roles_response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Error de conexión. Asegúrate de que el servidor esté corriendo en http://localhost:5002")
    except Exception as e:
        print(f"❌ Error inesperado: {str(e)}")

def test_health_endpoint():
    """
    Probar el endpoint de health para verificar que el servidor esté corriendo
    """
    try:
        response = requests.get("http://localhost:5002/health")
        if response.status_code == 200:
            print("✅ Servidor está corriendo correctamente")
            return True
        else:
            print(f"❌ Servidor respondió con status {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ No se puede conectar al servidor")
        return False

if __name__ == "__main__":
    print("🚀 Iniciando pruebas del endpoint de roles...\n")
    
    # Primero verificar que el servidor esté corriendo
    if test_health_endpoint():
        print("\n" + "="*50)
        test_roles_endpoint()
    else:
        print("\n💡 Para iniciar el servidor, ejecuta:")
        print("   python run_server.py")
