#!/usr/bin/env python3
"""
Firebase Database Service for Period Care Backend
Handles all Firebase Firestore database operations
"""

import os
import json
import uuid
from datetime import datetime
from typing import Optional, List, Dict, Any
import firebase_admin
from firebase_admin import credentials, firestore
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class FirebaseService:
    def __init__(self):
        self.db = None
        self.initialize_firebase()
    
    def initialize_firebase(self):
        """Initialize Firebase Admin SDK"""
        try:
            # Get Firebase configuration from environment
            service_account_path = os.getenv('FIREBASE_SERVICE_ACCOUNT_PATH')
            project_id = os.getenv('FIREBASE_PROJECT_ID')
            
            if not service_account_path or not os.path.exists(service_account_path):
                raise Exception(f"Firebase service account file not found: {service_account_path}")
            
            # Initialize Firebase Admin SDK
            cred = credentials.Certificate(service_account_path)
            firebase_admin.initialize_app(cred, {
                'projectId': project_id
            })
            
            # Get Firestore database
            self.db = firestore.client()
            print(f"✅ Firebase initialized successfully with project: {project_id}")
            
        except Exception as e:
            print(f"❌ Firebase initialization failed: {str(e)}")
            raise e
    
    # User operations
    def create_user(self, user_data: Dict[str, Any]) -> str:
        """Create a new user in Firestore"""
        try:
            user_id = str(uuid.uuid4())
            user_data.update({
                'id': user_id,
                'created_at': datetime.utcnow(),
                'updated_at': datetime.utcnow()
            })
            
            self.db.collection('users').document(user_id).set(user_data)
            return user_id
            
        except Exception as e:
            print(f"Error creating user: {str(e)}")
            raise e
    
    def get_user_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        """Get user by email"""
        try:
            users_ref = self.db.collection('users')
            query = users_ref.where('email', '==', email).limit(1)
            docs = query.stream()
            
            for doc in docs:
                user_data = doc.to_dict()
                user_data['id'] = doc.id
                return user_data
            
            return None
            
        except Exception as e:
            print(f"Error getting user by email: {str(e)}")
            raise e
    
    def get_user_by_id(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Get user by ID"""
        try:
            doc_ref = self.db.collection('users').document(user_id)
            doc = doc_ref.get()
            
            if doc.exists:
                user_data = doc.to_dict()
                user_data['id'] = doc.id
                return user_data
            
            return None
            
        except Exception as e:
            print(f"Error getting user by ID: {str(e)}")
            raise e
    
    # Kit operations
    def get_all_kits(self) -> List[Dict[str, Any]]:
        """Get all kits from Firestore"""
        try:
            kits_ref = self.db.collection('kits')
            docs = kits_ref.stream()
            
            kits = []
            for doc in docs:
                kit_data = doc.to_dict()
                kit_data['id'] = doc.id
                kits.append(kit_data)
            
            return kits
            
        except Exception as e:
            print(f"Error getting kits: {str(e)}")
            return []
    
    def get_kit_by_id(self, kit_id: str) -> Optional[Dict[str, Any]]:
        """Get kit by ID"""
        try:
            doc_ref = self.db.collection('kits').document(kit_id)
            doc = doc_ref.get()
            
            if doc.exists:
                kit_data = doc.to_dict()
                kit_data['id'] = doc.id
                return kit_data
            
            return None
            
        except Exception as e:
            print(f"Error getting kit by ID: {str(e)}")
            return None
    
    # Order operations
    def create_order(self, order_data: Dict[str, Any]) -> str:
        """Create a new order in Firestore"""
        try:
            order_id = str(uuid.uuid4())
            order_data.update({
                'id': order_id,
                'created_at': datetime.utcnow(),
                'updated_at': datetime.utcnow(),
                'status': 'pending'
            })
            
            self.db.collection('orders').document(order_id).set(order_data)
            return order_id
            
        except Exception as e:
            print(f"Error creating order: {str(e)}")
            raise e
    
    def get_all_orders(self) -> List[Dict[str, Any]]:
        """Get all orders from Firestore"""
        try:
            orders_ref = self.db.collection('orders').order_by('created_at', direction=firestore.Query.DESCENDING)
            docs = orders_ref.stream()
            
            orders = []
            for doc in docs:
                order_data = doc.to_dict()
                order_data['id'] = doc.id
                orders.append(order_data)
            
            return orders
            
        except Exception as e:
            print(f"Error getting orders: {str(e)}")
            return []
    
    # Benefits operations
    def get_all_benefits(self) -> List[Dict[str, Any]]:
        """Get all benefits from Firestore"""
        try:
            benefits_ref = self.db.collection('benefits')
            docs = benefits_ref.stream()
            
            benefits = []
            for doc in docs:
                benefit_data = doc.to_dict()
                benefit_data['id'] = doc.id
                benefits.append(benefit_data)
            
            return benefits
            
        except Exception as e:
            print(f"Error getting benefits: {str(e)}")
            return []
    
    # Testimonials operations
    def get_all_testimonials(self) -> List[Dict[str, Any]]:
        """Get all testimonials from Firestore"""
        try:
            testimonials_ref = self.db.collection('testimonials')
            docs = testimonials_ref.stream()
            
            testimonials = []
            for doc in docs:
                testimonial_data = doc.to_dict()
                testimonial_data['id'] = doc.id
                testimonials.append(testimonial_data)
            
            return testimonials
            
        except Exception as e:
            print(f"Error getting testimonials: {str(e)}")
            return []
    
    def initialize_sample_data(self):
        """Initialize sample data in Firestore"""
        try:
            # Check if data already exists
            kits = self.get_all_kits()
            if len(kits) > 0:
                print("Sample data already exists, skipping initialization")
                return
            
            # Sample kits
            sample_kits = [
                {
                    "name": "Basic Care Kit",
                    "description": "Essential period care items",
                    "price": 299.0,
                    "image": "https://via.placeholder.com/400x300/ff69b4/ffffff?text=Basic+Kit",
                    "features": "Pads, Pain Relief, Hygiene Products",
                    "type": "basic"
                },
                {
                    "name": "Premium Care Kit", 
                    "description": "Complete period care solution",
                    "price": 599.0,
                    "image": "https://via.placeholder.com/400x300/ff1493/ffffff?text=Premium+Kit",
                    "features": "Premium Pads, Pain Relief, Hygiene Products, Comfort Items",
                    "type": "premium"
                },
                {
                    "name": "Deluxe Care Kit",
                    "description": "Ultimate period care package", 
                    "price": 899.0,
                    "image": "https://via.placeholder.com/400x300/c71585/ffffff?text=Deluxe+Kit",
                    "features": "Organic Pads, Advanced Pain Relief, Complete Hygiene Set, Comfort Items, Nutritional Supplements",
                    "type": "deluxe"
                }
            ]
            
            # Add kits to Firestore
            for kit in sample_kits:
                kit_id = str(uuid.uuid4())
                kit['id'] = kit_id
                kit['created_at'] = datetime.utcnow()
                self.db.collection('kits').document(kit_id).set(kit)
            
            # Sample benefits
            sample_benefits = [
                {
                    "title": "Pain Relief Fruits",
                    "description": "Natural ingredients that help reduce cramps and discomfort",
                    "icon": "🍎"
                },
                {
                    "title": "Custom Nutrients", 
                    "description": "Supplements tailored to support your wellness during periods",
                    "icon": "💊"
                },
                {
                    "title": "Flexible Delivery",
                    "description": "Schedule deliveries that match your cycle perfectly",
                    "icon": "📅"
                }
            ]
            
            # Add benefits to Firestore
            for benefit in sample_benefits:
                benefit_id = str(uuid.uuid4())
                benefit['id'] = benefit_id
                benefit['created_at'] = datetime.utcnow()
                self.db.collection('benefits').document(benefit_id).set(benefit)
            
            # Sample testimonials
            sample_testimonials = [
                {
                    "name": "Priya S.",
                    "rating": 5,
                    "text": "Period Care has made my monthly cycle so much easier to manage!",
                    "location": "Mumbai"
                },
                {
                    "name": "Anjali R.",
                    "rating": 5, 
                    "text": "Love the personalized approach and timely delivery.",
                    "location": "Delhi"
                },
                {
                    "name": "Kavya M.",
                    "rating": 4,
                    "text": "Great products and excellent customer service.",
                    "location": "Bangalore"
                }
            ]
            
            # Add testimonials to Firestore
            for testimonial in sample_testimonials:
                testimonial_id = str(uuid.uuid4())
                testimonial['id'] = testimonial_id
                testimonial['created_at'] = datetime.utcnow()
                self.db.collection('testimonials').document(testimonial_id).set(testimonial)
            
            print("✅ Sample data initialized successfully in Firebase")
            
        except Exception as e:
            print(f"❌ Error initializing sample data: {str(e)}")
            raise e

# Global Firebase service instance
firebase_service = None

def get_firebase_service():
    """Get Firebase service instance (singleton pattern)"""
    global firebase_service
    if firebase_service is None:
        firebase_service = FirebaseService()
    return firebase_service