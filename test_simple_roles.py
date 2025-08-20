#!/usr/bin/env python3
"""
Script simple para probar el endpoint de roles
"""
import requests

def test_roles_endpoint():
    """
    Probar el endpoint de roles sin autenticación primero
    """
    try:
        print("🔍 Probando endpoint de roles...")
        
        # Probar sin autenticación primero
        response = requests.get("http://localhost:5002/rol")
        print(f"Status Code (sin auth): {response.status_code}")
        print(f"Response: {response.text[:200]}...")
        
        if response.status_code == 401:
            print("✅ Endpoint funciona, solo requiere autenticación")
            
            # Ahora probar con autenticación
            print("\n🔐 Probando con autenticación...")
            
            # Login
            login_response = requests.post(
                "http://localhost:5002/auth/admin/login",
                json={
                    "email": "contrerasaaron447111111@est.utn.ac.cr",
                    "password": "Secret123*"
                },
                headers={"Content-Type": "application/json"}
            )
            
            if login_response.status_code == 200:
                token = login_response.json()['data']['token']
                print("✅ Login exitoso")
                
                # Probar roles con token
                roles_response = requests.get(
                    "http://localhost:5002/rol",
                    headers={
                        "Authorization": f"Bearer {token}",
                        "Content-Type": "application/json"
                    }
                )
                
                print(f"Status Code (con auth): {roles_response.status_code}")
                print(f"Response: {roles_response.text[:500]}...")
                
            else:
                print(f"❌ Error en login: {login_response.status_code}")
                print(f"Login response: {login_response.text}")
                
        elif response.status_code == 405:
            print("❌ Error 405 - Method Not Allowed")
            print("El endpoint no está configurado correctamente")
            
        else:
            print(f"❌ Status inesperado: {response.status_code}")
            
    except requests.exceptions.ConnectionError:
        print("❌ No se puede conectar al servidor")
        print("Asegúrate de que el servidor esté corriendo en http://localhost:5002")
    except Exception as e:
        print(f"❌ Error inesperado: {str(e)}")

if __name__ == "__main__":
    print("🚀 Probando endpoint de roles...\n")
    test_roles_endpoint()
