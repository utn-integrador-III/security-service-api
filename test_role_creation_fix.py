#!/usr/bin/env python3
"""
Test script to verify role creation works correctly after the fix
"""

import requests
import json

BASE_URL = "http://localhost:5002"

def test_admin_login():
    """Test admin login to get a valid token"""
    print("🔐 Testing admin login...")
    
    login_data = {
        "email": "contrerasaaron447111111@est.utn.ac.cr",
        "password": "123456"
    }
    
    response = requests.post(f"{BASE_URL}/auth/admin/login", json=login_data)
    
    if response.status_code == 200:
        data = response.json()
        token = data['data']['token']
        print(f"✅ Login successful. Token: {token[:50]}...")
        return token
    else:
        print(f"❌ Login failed. Status: {response.status_code}")
        print(f"Response: {response.text}")
        return None

def test_create_role(token):
    """Test creating a role with the fixed code"""
    print("\n🔧 Testing role creation...")
    
    role_data = {
        "name": "Test Role Fix",
        "description": "Testing role creation after fix",
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

def test_list_roles(token):
    """Test listing roles to see if the created role appears"""
    print("\n📋 Testing list roles...")
    
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    response = requests.get(f"{BASE_URL}/rol", headers=headers)
    
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        roles = data.get('data', [])
        print(f"Found {len(roles)} roles")
        for role in roles:
            print(f"  - {role.get('name')} (ID: {role.get('_id')})")
        return True
    else:
        print(f"Response: {response.text}")
        return False

def main():
    print("🧪 Testing Role Creation Fix")
    print("=" * 50)
    
    # Step 1: Login
    token = test_admin_login()
    if not token:
        print("❌ Cannot proceed without valid token")
        return
    
    # Step 2: Create role
    success = test_create_role(token)
    if not success:
        print("❌ Role creation failed, stopping test")
        return
    
    # Step 3: List roles
    test_list_roles(token)
    
    print("\n✅ Test completed!")

if __name__ == "__main__":
    main()
