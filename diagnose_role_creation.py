#!/usr/bin/env python3
"""
Comprehensive diagnostic script for role creation issue
"""

import requests
import json
import sys
import os

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

BASE_URL = "http://localhost:5002"

def test_step_by_step():
    """Test each step of the role creation process"""
    print("🔍 DIAGNÓSTICO PASO A PASO")
    print("=" * 60)
    
    # Step 1: Test admin login
    print("\n1️⃣ Testing admin login...")
    login_data = {
        "email": "contrerasaaron447111111@est.utn.ac.cr",
        "password": "123456"
    }
    
    response = requests.post(f"{BASE_URL}/auth/admin/login", json=login_data)
    print(f"   Status: {response.status_code}")
    
    if response.status_code != 200:
        print(f"   ❌ Login failed: {response.text}")
        return None
    
    token = response.json()['data']['token']
    print(f"   ✅ Login successful")
    print(f"   Token: {token[:50]}...")
    
    # Step 2: Test getting admin apps
    print("\n2️⃣ Testing admin apps retrieval...")
    try:
        from models.apps.app import AppModel
        
        admin_id = "68a590ebec92b4ab68f630d5"
        admin_apps = AppModel.get_by_admin_id(admin_id)
        
        print(f"   Admin apps found: {len(admin_apps) if admin_apps else 0}")
        
        if admin_apps and len(admin_apps) > 0:
            app_id = admin_apps[0]._id
            print(f"   First app ID: {app_id}")
            print(f"   App ID type: {type(app_id)}")
            return token, app_id
        else:
            print("   ❌ No apps found for admin")
            return token, None
            
    except Exception as e:
        print(f"   ❌ Error getting admin apps: {str(e)}")
        import traceback
        traceback.print_exc()
        return token, None
    
    # Step 3: Test role creation with API
    print("\n3️⃣ Testing role creation via API...")
    role_data = {
        "name": "Diagnostic Test Role",
        "description": "Testing role creation step by step",
        "permissions": ["read", "write"]
    }
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    
    print(f"   Sending request to: {BASE_URL}/rol")
    print(f"   Headers: {headers}")
    print(f"   Body: {json.dumps(role_data, indent=2)}")
    
    try:
        response = requests.post(f"{BASE_URL}/rol", json=role_data, headers=headers)
        
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.text}")
        
        if response.status_code == 201:
            print("   ✅ Role creation successful!")
            return True
        else:
            print("   ❌ Role creation failed!")
            return False
            
    except Exception as e:
        print(f"   ❌ Exception: {str(e)}")
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
        print(f"   Admin apps: {admin_apps}")
        
        if admin_apps and len(admin_apps) > 0:
            app_id = admin_apps[0]._id
            print(f"   App ID: {app_id}")
            print(f"   App ID type: {type(app_id)}")
            
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
                "app_id": app_id
            }
            
            print(f"   Role data: {role_data}")
            
            # Try to create
            new_role = RoleModel.create(role_data)
            
            if new_role:
                print("   ✅ Direct model creation successful!")
                print(f"   Created role: {new_role.to_dict()}")
                return True
            else:
                print("   ❌ Direct model creation failed!")
                return False
        else:
            print("   ❌ No apps found for admin!")
            return False
            
    except Exception as e:
        print(f"   ❌ Exception in direct model creation: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_database_connection():
    """Test database connection and basic operations"""
    print("\n🗄️ Testing database connection...")
    
    try:
        from db.mongo_client import Connection
        from decouple import config
        
        # Test role collection connection
        role_collection = config('ROLE_COLLECTION')
        print(f"   Role collection: {role_collection}")
        
        connection = Connection(role_collection)
        print(f"   ✅ Database connection successful")
        
        # Test basic query
        count = connection.collection.count_documents({})
        print(f"   Total roles in database: {count}")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Database connection failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def main():
    print("🐛 COMPREHENSIVE ROLE CREATION DIAGNOSTIC")
    print("=" * 60)
    
    # Test database connection
    db_ok = test_database_connection()
    if not db_ok:
        print("\n❌ Database connection failed. Cannot proceed.")
        return
    
    # Test step by step
    result = test_step_by_step()
    if result is None:
        print("\n❌ Login failed. Cannot proceed.")
        return
    
    token, app_id = result
    
    # Test direct model creation
    model_ok = test_direct_model_creation()
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 SUMMARY")
    print("=" * 60)
    print(f"Database Connection: {'✅ OK' if db_ok else '❌ FAILED'}")
    print(f"Login: {'✅ OK' if token else '❌ FAILED'}")
    print(f"App ID Found: {'✅ OK' if app_id else '❌ FAILED'}")
    print(f"Direct Model Creation: {'✅ OK' if model_ok else '❌ FAILED'}")

if __name__ == "__main__":
    main()
