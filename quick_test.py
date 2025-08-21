#!/usr/bin/env python3
"""
Quick test to verify role creation fix
"""

import requests

BASE_URL = "http://localhost:5002"

def test_role_creation():
    # Login
    login_data = {
        "email": "contrerasaaron447111111@est.utn.ac.cr",
        "password": "123456"
    }
    
    response = requests.post(f"{BASE_URL}/auth/admin/login", json=login_data)
    if response.status_code != 200:
        print(f"❌ Login failed: {response.status_code}")
        return
    
    token = response.json()['data']['token']
    print("✅ Login successful")
    
    # Create role
    role_data = {
        "name": "Quick Test Role",
        "description": "Testing the fix",
        "permissions": ["read", "write"]
    }
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    
    response = requests.post(f"{BASE_URL}/rol", json=role_data, headers=headers)
    print(f"📥 Status: {response.status_code}")
    print(f"📥 Response: {response.text}")
    
    if response.status_code == 201:
        print("✅ Role creation successful!")
    else:
        print("❌ Role creation failed!")

if __name__ == "__main__":
    test_role_creation()
