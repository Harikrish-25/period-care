#!/usr/bin/env python3
"""
Test Firebase connection and basic operations
"""
import os
import sys
from pathlib import Path

# Add the app directory to the Python path
sys.path.append(str(Path(__file__).parent / "app"))

try:
    from config.firebase import db
    print("✅ Firebase configuration imported successfully")
except Exception as e:
    print(f"❌ Failed to import Firebase configuration: {e}")
    sys.exit(1)

def test_firebase_connection():
    """Test basic Firebase operations"""
    try:
        # Test connection by creating a test document
        test_collection = db.collection('connection_test')
        test_doc = test_collection.document('test')
        
        # Write test data
        test_data = {
            'message': 'Firebase connection test',
            'timestamp': firestore.SERVER_TIMESTAMP
        }
        test_doc.set(test_data)
        print("✅ Successfully wrote test document to Firestore")
        
        # Read test data
        doc = test_doc.get()
        if doc.exists:
            print("✅ Successfully read test document from Firestore")
            print(f"   Data: {doc.to_dict()}")
        else:
            print("❌ Test document not found")
            return False
        
        # Clean up test document
        test_doc.delete()
        print("✅ Successfully deleted test document")
        
        return True
        
    except Exception as e:
        print(f"❌ Firebase connection test failed: {e}")
        return False

def test_collections():
    """Test if required collections can be accessed"""
    required_collections = ['users', 'kits', 'orders', 'benefits', 'testimonials']
    
    for collection_name in required_collections:
        try:
            collection = db.collection(collection_name)
            # Try to get the first document (if any)
            docs = collection.limit(1).get()
            print(f"✅ Collection '{collection_name}' accessible")
        except Exception as e:
            print(f"❌ Failed to access collection '{collection_name}': {e}")

if __name__ == "__main__":
    print("🔥 Testing Firebase Connection...")
    print("=" * 50)
    
    # Import firestore after Firebase is initialized
    try:
        from google.cloud import firestore
    except ImportError:
        print("❌ google-cloud-firestore not installed. Run: pip install -r requirements.txt")
        sys.exit(1)
    
    if test_firebase_connection():
        print("\n📊 Testing Collections Access...")
        test_collections()
        print("\n🎉 All Firebase tests completed successfully!")
    else:
        print("\n💥 Firebase connection test failed!")
        sys.exit(1)