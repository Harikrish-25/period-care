#!/usr/bin/env python3
"""
Firebase Setup Guide for Period Care Backend
"""

import os
import json

def main():
    print("🔥 Firebase Setup for Period Care Backend")
    print("=" * 50)
    
    # Check if service account file exists
    service_account_path = "./firebase-service-account.json"
    
    if os.path.exists(service_account_path):
        print("✅ Firebase service account file found!")
        try:
            with open(service_account_path, 'r') as f:
                data = json.load(f)
                project_id = data.get('project_id')
                print(f"✅ Project ID: {project_id}")
        except Exception as e:
            print(f"❌ Error reading service account file: {e}")
    else:
        print("❌ Firebase service account file not found!")
        print("\n📝 Setup Instructions:")
        print("1. Go to Firebase Console: https://console.firebase.google.com/")
        print("2. Create a new project or select existing project")
        print("3. Go to Project Settings (gear icon)")
        print("4. Navigate to 'Service accounts' tab")
        print("5. Click 'Generate new private key'")
        print("6. Download the JSON file")
        print("7. Rename it to 'firebase-service-account.json'")
        print("8. Place it in the backend root directory")
        print(f"   Expected path: {os.path.abspath(service_account_path)}")
        
        print("\n🔧 Alternative Setup (using environment variable):")
        print("Set FIREBASE_SERVICE_ACCOUNT_JSON environment variable with the JSON content")
        
        return False
    
    # Check environment variables
    print("\n🔧 Environment Variables:")
    env_vars = [
        'DATABASE_TYPE',
        'FIREBASE_PROJECT_ID',
        'ADMIN_WHATSAPP_NUMBER',
        'SECRET_KEY'
    ]
    
    for var in env_vars:
        value = os.getenv(var)
        if value:
            if var == 'SECRET_KEY':
                print(f"✅ {var}: {'*' * len(value)}")
            else:
                print(f"✅ {var}: {value}")
        else:
            print(f"❌ {var}: Not set")
    
    # Test Firebase connection
    print("\n🧪 Testing Firebase Connection...")
    try:
        from app.config.firebase import firebase_config
        
        if firebase_config.test_connection():
            print("✅ Firebase connection successful!")
            
            # Initialize some test data
            print("\n📊 Initializing sample data...")
            db = firebase_config.get_db()
            
            # Test write operation
            test_doc = db.collection('_test').document('setup')
            test_doc.set({
                'message': 'Period Care Backend Setup Successful!',
                'timestamp': '2025-09-13T12:00:00Z',
                'status': 'active'
            })
            print("✅ Test data written successfully!")
            
            return True
        else:
            print("❌ Firebase connection failed!")
            return False
            
    except Exception as e:
        print(f"❌ Firebase test failed: {e}")
        return False

if __name__ == "__main__":
    if main():
        print("\n🎉 Firebase setup completed successfully!")
        print("You can now start the backend server with: uvicorn app.main:app --reload")
    else:
        print("\n❌ Firebase setup incomplete. Please follow the instructions above.")