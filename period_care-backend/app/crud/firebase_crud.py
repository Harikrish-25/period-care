from google.cloud import firestore
from typing import Optional, List, Dict, Any
from datetime import datetime, date
from app.config.firebase import get_firestore_db
from app.config.security import get_password_hash, verify_password
import json


class FirebaseUserCRUD:
    def __init__(self):
        self.db = get_firestore_db()
        self.collection = 'users'
    
    def get_user_by_id(self, user_id: str) -> Optional[Dict]:
        """Get user by ID"""
        try:
            doc_ref = self.db.collection(self.collection).document(user_id)
            doc = doc_ref.get()
            if doc.exists:
                user_data = doc.to_dict()
                user_data['id'] = doc.id
                return user_data
            return None
        except Exception as e:
            print(f"Error getting user by ID: {e}")
            return None
    
    def get_user_by_email(self, email: str) -> Optional[Dict]:
        """Get user by email"""
        try:
            users_ref = self.db.collection(self.collection)
            query = users_ref.where('email', '==', email).limit(1)
            docs = query.stream()
            
            for doc in docs:
                user_data = doc.to_dict()
                user_data['id'] = doc.id
                return user_data
            return None
        except Exception as e:
            print(f"Error getting user by email: {e}")
            return None
    
    def create_user(self, user_data: Dict) -> Optional[Dict]:
        """Create new user"""
        try:
            # Hash password
            user_data['password'] = get_password_hash(user_data['password'])
            user_data['created_at'] = datetime.utcnow()
            user_data['updated_at'] = datetime.utcnow()
            user_data['role'] = user_data.get('role', 'user')
            user_data['is_active'] = True
            user_data['reminder_sent'] = False
            user_data['last_order_date'] = None
            
            # Add to Firestore
            doc_ref = self.db.collection(self.collection).add(user_data)
            user_data['id'] = doc_ref[1].id
            return user_data
        except Exception as e:
            print(f"Error creating user: {e}")
            return None
    
    def update_user(self, user_id: str, update_data: Dict) -> Optional[Dict]:
        """Update user"""
        try:
            update_data['updated_at'] = datetime.utcnow()
            doc_ref = self.db.collection(self.collection).document(user_id)
            doc_ref.update(update_data)
            return self.get_user_by_id(user_id)
        except Exception as e:
            print(f"Error updating user: {e}")
            return None
    
    def authenticate_user(self, email: str, password: str) -> Optional[Dict]:
        """Authenticate user"""
        user = self.get_user_by_email(email)
        if user and verify_password(password, user['password']):
            return user
        return None
    
    def get_users_due_for_reminder(self, target_date: date) -> List[Dict]:
        """Get users due for reminder"""
        try:
            users_ref = self.db.collection(self.collection)
            query = users_ref.where('last_order_date', '==', target_date).where('reminder_sent', '==', False).where('is_active', '==', True)
            docs = query.stream()
            
            users = []
            for doc in docs:
                user_data = doc.to_dict()
                user_data['id'] = doc.id
                users.append(user_data)
            return users
        except Exception as e:
            print(f"Error getting users due for reminder: {e}")
            return []


class FirebaseKitCRUD:
    def __init__(self):
        self.db = get_firestore_db()
        self.collection = 'kits'
    
    def get_kit_by_id(self, kit_id: str) -> Optional[Dict]:
        """Get kit by ID"""
        try:
            doc_ref = self.db.collection(self.collection).document(kit_id)
            doc = doc_ref.get()
            if doc.exists:
                kit_data = doc.to_dict()
                kit_data['id'] = doc.id
                return kit_data
            return None
        except Exception as e:
            print(f"Error getting kit by ID: {e}")
            return None
    
    def get_kits(self, available_only: bool = True) -> List[Dict]:
        """Get all kits"""
        try:
            kits_ref = self.db.collection(self.collection)
            if available_only:
                query = kits_ref.where('is_available', '==', True)
            else:
                query = kits_ref
            
            docs = query.stream()
            kits = []
            for doc in docs:
                kit_data = doc.to_dict()
                kit_data['id'] = doc.id
                kits.append(kit_data)
            return kits
        except Exception as e:
            print(f"Error getting kits: {e}")
            return []
    
    def create_kit(self, kit_data: Dict) -> Optional[Dict]:
        """Create new kit"""
        try:
            kit_data['created_at'] = datetime.utcnow()
            kit_data['updated_at'] = datetime.utcnow()
            kit_data['is_available'] = True
            
            doc_ref = self.db.collection(self.collection).add(kit_data)
            kit_data['id'] = doc_ref[1].id
            return kit_data
        except Exception as e:
            print(f"Error creating kit: {e}")
            return None


class FirebaseOrderCRUD:
    def __init__(self):
        self.db = get_firestore_db()
        self.collection = 'orders'
    
    def create_order(self, order_data: Dict) -> Optional[Dict]:
        """Create new order"""
        try:
            order_data['created_at'] = datetime.utcnow()
            order_data['updated_at'] = datetime.utcnow()
            order_data['status'] = 'pending'
            order_data['whatsapp_sent'] = False
            
            doc_ref = self.db.collection(self.collection).add(order_data)
            order_data['id'] = doc_ref[1].id
            return order_data
        except Exception as e:
            print(f"Error creating order: {e}")
            return None
    
    def get_user_orders(self, user_id: str) -> List[Dict]:
        """Get orders for a user"""
        try:
            orders_ref = self.db.collection(self.collection)
            query = orders_ref.where('user_id', '==', user_id).order_by('created_at', direction=firestore.Query.DESCENDING)
            docs = query.stream()
            
            orders = []
            for doc in docs:
                order_data = doc.to_dict()
                order_data['id'] = doc.id
                orders.append(order_data)
            return orders
        except Exception as e:
            print(f"Error getting user orders: {e}")
            return []
    
    def get_all_orders(self) -> List[Dict]:
        """Get all orders"""
        try:
            orders_ref = self.db.collection(self.collection)
            query = orders_ref.order_by('created_at', direction=firestore.Query.DESCENDING)
            docs = query.stream()
            
            orders = []
            for doc in docs:
                order_data = doc.to_dict()
                order_data['id'] = doc.id
                orders.append(order_data)
            return orders
        except Exception as e:
            print(f"Error getting all orders: {e}")
            return []


class FirebaseFruitCRUD:
    def __init__(self):
        self.db = get_firestore_db()
        self.collection = 'fruits'
    
    def get_fruits(self, available_only: bool = True) -> List[Dict]:
        """Get all fruits"""
        try:
            fruits_ref = self.db.collection(self.collection)
            if available_only:
                query = fruits_ref.where('is_available', '==', True)
            else:
                query = fruits_ref
            
            docs = query.stream()
            fruits = []
            for doc in docs:
                fruit_data = doc.to_dict()
                fruit_data['id'] = doc.id
                fruits.append(fruit_data)
            return fruits
        except Exception as e:
            print(f"Error getting fruits: {e}")
            return []
    
    def get_fruit_by_id(self, fruit_id: str) -> Optional[Dict]:
        """Get fruit by ID"""
        try:
            doc_ref = self.db.collection(self.collection).document(fruit_id)
            doc = doc_ref.get()
            if doc.exists:
                fruit_data = doc.to_dict()
                fruit_data['id'] = doc.id
                return fruit_data
            return None
        except Exception as e:
            print(f"Error getting fruit by ID: {e}")
            return None


class FirebaseNutrientCRUD:
    def __init__(self):
        self.db = get_firestore_db()
        self.collection = 'nutrients'
    
    def get_nutrients(self, available_only: bool = True) -> List[Dict]:
        """Get all nutrients"""
        try:
            nutrients_ref = self.db.collection(self.collection)
            if available_only:
                query = nutrients_ref.where('is_available', '==', True)
            else:
                query = nutrients_ref
            
            docs = query.stream()
            nutrients = []
            for doc in docs:
                nutrient_data = doc.to_dict()
                nutrient_data['id'] = doc.id
                nutrients.append(nutrient_data)
            return nutrients
        except Exception as e:
            print(f"Error getting nutrients: {e}")
            return []
    
    def get_nutrient_by_id(self, nutrient_id: str) -> Optional[Dict]:
        """Get nutrient by ID"""
        try:
            doc_ref = self.db.collection(self.collection).document(nutrient_id)
            doc = doc_ref.get()
            if doc.exists:
                nutrient_data = doc.to_dict()
                nutrient_data['id'] = doc.id
                return nutrient_data
            return None
        except Exception as e:
            print(f"Error getting nutrient by ID: {e}")
            return None


# Initialize Firebase CRUD instances
firebase_user_crud = FirebaseUserCRUD()
firebase_kit_crud = FirebaseKitCRUD()
firebase_order_crud = FirebaseOrderCRUD()
firebase_fruit_crud = FirebaseFruitCRUD()
firebase_nutrient_crud = FirebaseNutrientCRUD()
