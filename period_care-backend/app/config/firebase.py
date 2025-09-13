import firebase_admin
from firebase_admin import credentials, firestore
from app.config.settings import settings
import os
import json


class FirebaseConfig:
    def __init__(self):
        self.db = None
        self.app = None
        self.initialize_firebase()
    
    def initialize_firebase(self):
        """Initialize Firebase Admin SDK"""
        try:
            # Check if Firebase is already initialized
            if not firebase_admin._apps:
                service_account_path = settings.firebase_service_account_path
                
                # Method 1: Try with service account file
                if os.path.exists(service_account_path):
                    print(f"🔥 Using Firebase service account: {service_account_path}")
                    cred = credentials.Certificate(service_account_path)
                    self.app = firebase_admin.initialize_app(cred)
                    print("✅ Firebase initialized with service account")
                
                # Method 2: Try with environment variables
                elif os.getenv('FIREBASE_SERVICE_ACCOUNT_JSON'):
                    print("🔥 Using Firebase service account from environment variable")
                    service_account_info = json.loads(os.getenv('FIREBASE_SERVICE_ACCOUNT_JSON'))
                    cred = credentials.Certificate(service_account_info)
                    self.app = firebase_admin.initialize_app(cred)
                    print("✅ Firebase initialized with environment credentials")
                
                # Method 3: Try with default credentials (for deployed environments)
                else:
                    print("🔥 Attempting to use default Firebase credentials")
                    try:
                        self.app = firebase_admin.initialize_app()
                        print("✅ Firebase initialized with default credentials")
                    except Exception as default_error:
                        print(f"❌ Default credentials failed: {default_error}")
                        print("📝 Please set up Firebase credentials:")
                        print("   1. Download service account JSON from Firebase Console")
                        print("   2. Place it as 'firebase-service-account.json' in backend root")
                        print("   3. Or set FIREBASE_SERVICE_ACCOUNT_JSON environment variable")
                        self.db = None
                        return
            else:
                self.app = firebase_admin.get_app()
                print("✅ Firebase already initialized")
            
            # Get Firestore client
            self.db = firestore.client(app=self.app)
            print("✅ Firestore client connected")
            
        except Exception as e:
            print(f"❌ Firebase initialization failed: {e}")
            print("📝 Setup instructions:")
            print("   1. Go to Firebase Console: https://console.firebase.google.com/")
            print("   2. Create/select your project")
            print("   3. Go to Project Settings > Service Accounts")
            print("   4. Generate new private key")
            print("   5. Save as 'firebase-service-account.json' in backend root")
            self.db = None
    
    def get_db(self):
        """Get Firestore database instance"""
        if self.db is None:
            self.initialize_firebase()
        return self.db
    
    def test_connection(self):
        """Test Firebase connection"""
        try:
            if self.db:
                # Try to access a collection to test connection
                test_doc = self.db.collection('_test').document('connection').get()
                print("✅ Firebase connection test successful")
                return True
            else:
                print("❌ Firebase connection test failed - no database instance")
                return False
        except Exception as e:
            print(f"❌ Firebase connection test failed: {e}")
            return False


# Global Firebase instance
firebase_config = FirebaseConfig()


def get_firebase_db():
    """Get Firebase database instance"""
    return firebase_config.get_db()


# Global Firebase instance
firebase_config = FirebaseConfig()


def get_firestore_db():
    """Dependency to get Firestore database"""
    return firebase_config.get_db()
