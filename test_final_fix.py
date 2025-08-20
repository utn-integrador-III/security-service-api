#!/usr/bin/env python3
"""
Simple test to verify the final fix for role creation
"""

import requests

BASE_URL = "http://localhost:5002"

def test_role_creation():
    print("🧪 Testing Role Creation Fix")
    print("=" * 40)
    
    # Login
    print("1. Logging in...")
    login_data = {
        "email": "contrerasaaron447111111@est.utn.ac.cr",
        "password": "123456"
    }
    
    response = requests.post(f"{BASE_URL}/auth/admin/login", json=login_data)
    if response.status_code != 200:
        print(f"❌ Login failed: {response.status_code}")
        print(f"Response: {response.text}")
        return
    
    token = response.json()['data']['token']
    print("✅ Login successful")
    
    # Create role
    print("\n2. Creating role...")
    role_data = {
        "name": "Final Test Role",
        "description": "Testing the final fix",
        "permissions": ["read", "write"]
    }
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    
    response = requests.post(f"{BASE_URL}/rol", json=role_data, headers=headers)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text}")
    
    if response.status_code == 201:
        print("✅ Role creation successful!")
        return True
    else:
        print("❌ Role creation failed!")
        return False

if __name__ == "__main__":
    success = test_role_creation()
    if success:
        print("\n🎉 All tests passed!")
    else:
        print("\n💥 Tests failed!")
