#!/usr/bin/env python3
"""
Firebase initialization script with sample data for Period Care Backend
"""

from app.config.firebase import get_firestore_db
from app.config.security import get_password_hash
from datetime import datetime
import json


def create_firebase_sample_data():
    """Create sample data in Firebase Firestore"""
    db = get_firestore_db()
    
    if not db:
        print("❌ Firebase connection failed. Cannot create sample data.")
        return False
    
    try:
        print("📝 Creating sample data in Firebase Firestore...")
        
        # Create admin user
        admin_data = {
            "name": "Admin User",
            "email": "admin@periodcare.com",
            "mobile": "+919999999999",
            "address": "Admin Office, Mumbai",
            "password": get_password_hash("admin123"),
            "role": "admin",
            "is_active": True,
            "reminder_sent": False,
            "last_order_date": None,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
        db.collection('users').add(admin_data)
        
        # Create test user
        test_user_data = {
            "name": "Priya Sharma",
            "email": "priya@example.com",
            "mobile": "+919876543210",
            "address": "123 Main Street, Mumbai, Maharashtra 400001",
            "password": get_password_hash("user123"),
            "role": "user",
            "is_active": True,
            "reminder_sent": False,
            "last_order_date": None,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
        db.collection('users').add(test_user_data)
        print("✅ Users created")
        
        # Create sample kits
        kits_data = [
            {
                "name": "Basic Care Kit",
                "type": "basic",
                "base_price": 299.0,
                "image_url": "https://example.com/basic-kit.jpg",
                "included_items": json.dumps([
                    "10 Regular Pads",
                    "Pain Relief Sachet",
                    "Hygiene Wipes"
                ]),
                "description": "Essential period care items for basic comfort and hygiene.",
                "is_available": True,
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            },
            {
                "name": "Comfort Care Kit",
                "type": "medium",
                "base_price": 499.0,
                "image_url": "https://example.com/comfort-kit.jpg",
                "included_items": json.dumps([
                    "15 Ultra-Soft Pads",
                    "Pain Relief Sachets (3)",
                    "Hygiene Wipes",
                    "Comfort Balm"
                ]),
                "description": "Enhanced comfort with premium products for your period care.",
                "is_available": True,
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            },
            {
                "name": "Premium Wellness Kit",
                "type": "premium",
                "base_price": 799.0,
                "image_url": "https://example.com/premium-kit.jpg",
                "included_items": json.dumps([
                    "20 Premium Pads",
                    "Pain Relief Sachets (5)",
                    "Hygiene Wipes",
                    "Comfort Balm",
                    "Heating Pad",
                    "Wellness Tea"
                ]),
                "description": "Complete wellness package with premium products and comfort accessories.",
                "is_available": True,
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            }
        ]
        
        for kit_data in kits_data:
            db.collection('kits').add(kit_data)
        print("✅ Kits created")
        
        # Create sample fruits
        fruits_data = [
            {
                "name": "Apple Slices",
                "price": 50.0,
                "benefits": "Rich in fiber, helps with digestion",
                "emoji_icon": "🍎",
                "is_available": True,
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            },
            {
                "name": "Banana Chips",
                "price": 40.0,
                "benefits": "High potassium, reduces cramps",
                "emoji_icon": "🍌",
                "is_available": True,
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            },
            {
                "name": "Orange Wedges",
                "price": 60.0,
                "benefits": "Vitamin C boost, mood enhancement",
                "emoji_icon": "🍊",
                "is_available": True,
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            },
            {
                "name": "Mixed Berries",
                "price": 80.0,
                "benefits": "Antioxidants, natural pain relief",
                "emoji_icon": "🫐",
                "is_available": True,
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            }
        ]
        
        for fruit_data in fruits_data:
            db.collection('fruits').add(fruit_data)
        print("✅ Fruits created")
        
        # Create sample nutrients
        nutrients_data = [
            {
                "name": "Iron Supplement",
                "price": 120.0,
                "description": "Combats fatigue and weakness",
                "is_available": True,
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            },
            {
                "name": "Magnesium Complex",
                "price": 150.0,
                "description": "Reduces cramps and muscle tension",
                "is_available": True,
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            },
            {
                "name": "Calcium + D3",
                "price": 100.0,
                "description": "Bone health and mood support",
                "is_available": True,
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            }
        ]
        
        for nutrient_data in nutrients_data:
            db.collection('nutrients').add(nutrient_data)
        print("✅ Nutrients created")
        
        # Create sample benefits
        benefits_data = [
            {
                "title": "Pain Relief Fruits",
                "description": "Natural ingredients that help reduce cramps and discomfort",
                "icon_emoji": "🍎",
                "display_order": 1,
                "is_active": True,
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            },
            {
                "title": "Custom Nutrients",
                "description": "Supplements tailored to support your wellness during periods",
                "icon_emoji": "💊",
                "display_order": 2,
                "is_active": True,
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            }
        ]
        
        for benefit_data in benefits_data:
            db.collection('benefits').add(benefit_data)
        print("✅ Benefits created")
        
        # Create sample testimonials
        testimonials_data = [
            {
                "name": "Priya S.",
                "rating": 5,
                "testimonial_text": "The customizable kits are a game-changer! Love the fruit options and the convenience of delivery.",
                "location": "Mumbai",
                "is_featured": True,
                "is_active": True,
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            },
            {
                "name": "Anita K.",
                "rating": 5,
                "testimonial_text": "Finally, a service that understands what women need. The nutrients really help with my symptoms.",
                "location": "Delhi",
                "is_featured": True,
                "is_active": True,
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            }
        ]
        
        for testimonial_data in testimonials_data:
            db.collection('testimonials').add(testimonial_data)
        print("✅ Testimonials created")
        
        print("🎉 Firebase sample data created successfully!")
        print("🔑 Admin Login: admin@periodcare.com / admin123")
        print("👤 Test User: priya@example.com / user123")
        return True
        
    except Exception as e:
        print(f"❌ Error creating Firebase sample data: {e}")
        return False


if __name__ == "__main__":
    success = create_firebase_sample_data()
    if success:
        print("✅ Firebase initialization complete!")
    else:
        print("❌ Firebase initialization failed!")
