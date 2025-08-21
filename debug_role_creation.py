#!/usr/bin/env python3
"""
Debug script to identify the exact issue with role creation
"""

import requests
import json
import sys
import os

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

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

def test_create_role_with_debug(token):
    """Test creating a role with detailed debugging"""
    print("\n🔧 Testing role creation with debug...")
    
    role_data = {
        "name": "Debug Test Role",
        "description": "Testing role creation with debug",
        "permissions": ["read", "write"]
    }
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    
    print(f"📤 Sending request to: {BASE_URL}/rol")
    print(f"📤 Headers: {headers}")
    print(f"📤 Body: {json.dumps(role_data, indent=2)}")
    
    try:
        response = requests.post(f"{BASE_URL}/rol", json=role_data, headers=headers)
        
        print(f"📥 Status: {response.status_code}")
        print(f"📥 Status Text: {response.reason}")
        print(f"📥 Headers: {dict(response.headers)}")
        print(f"📥 Response: {response.text}")
        
        if response.status_code == 201:
            print("✅ Role creation successful!")
            return True
        else:
            print("❌ Role creation failed!")
            return False
            
    except Exception as e:
        print(f"💥 Exception occurred: {str(e)}")
        return False

def test_direct_model_creation():
    """Test creating a role directly using the model"""
    print("\n🔧 Testing direct model creation...")
    
    try:
        from models.role.role import RoleModel
        from models.apps.app import AppModel
        from bson import ObjectId
        from datetime import datetime
        
        # Test data
        admin_id = "68a590ebec92b4ab68f630d5"
        
        # Get app_id
        admin_apps = AppModel.get_by_admin_id(admin_id)
        print(f"📋 Admin apps: {admin_apps}")
        
        if admin_apps and len(admin_apps) > 0:
            app_id = admin_apps[0]._id
            print(f"📋 App ID: {app_id}")
            
            # Create role data
            role_data = {
                "name": "Direct Test Role",
                "description": "Testing direct model creation",
                "permissions": ["read", "write"],
                "creation_date": datetime.utcnow(),
                "mod_date": datetime.utcnow(),
                "is_active": True,
                "default_role": False,
                "screens": [],
                "admin_id": admin_id,
                "app_id": ObjectId(app_id) if isinstance(app_id, str) else app_id
            }
            
            print(f"📋 Role data: {role_data}")
            
            # Try to create
            new_role = RoleModel.create(role_data)
            
            if new_role:
                print("✅ Direct model creation successful!")
                print(f"📋 Created role: {new_role.to_dict()}")
                return True
            else:
                print("❌ Direct model creation failed!")
                return False
        else:
            print("❌ No apps found for admin!")
            return False
            
    except Exception as e:
        print(f"💥 Exception in direct model creation: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def main():
    print("🐛 Debugging Role Creation Issue")
    print("=" * 50)
    
    # Step 1: Login
    token = test_admin_login()
    if not token:
        print("❌ Cannot proceed without valid token")
        return
    
    # Step 2: Test API creation
    print("\n" + "="*50)
    print("TESTING API CREATION")
    print("="*50)
    api_success = test_create_role_with_debug(token)
    
    # Step 3: Test direct model creation
    print("\n" + "="*50)
    print("TESTING DIRECT MODEL CREATION")
    print("="*50)
    model_success = test_direct_model_creation()
    
    # Summary
    print("\n" + "="*50)
    print("SUMMARY")
    print("="*50)
    print(f"API Creation: {'✅ Success' if api_success else '❌ Failed'}")
    print(f"Model Creation: {'✅ Success' if model_success else '❌ Failed'}")

if __name__ == "__main__":
    main()
