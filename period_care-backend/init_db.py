#!/usr/bin/env python3
"""
Database initialization script with sample data for Period Care Backend
"""

from sqlalchemy.orm import Session
from app.config.database import SessionLocal, create_tables
from app.config.security import get_password_hash
from app.models.user import User
from app.models.kit import Kit
from app.models.fruit import Fruit
from app.models.nutrient import Nutrient
from app.models.benefit import Benefit
from app.models.testimonial import Testimonial
import json


def get_db():
    """Get database session"""
    return SessionLocal()


def create_sample_data():
    """Create sample data for the application"""
    db = get_db()
    
    try:
        # Create admin user
        admin_user = User(
            name="Admin User",
            email="admin@periodcare.com",
            mobile="+919999999999",
            address="Admin Office, Mumbai",
            password=get_password_hash("admin123"),
            role="admin",
            is_active=True
        )
        db.add(admin_user)
        
        # Create test user
        test_user = User(
            name="Priya Sharma",
            email="priya@example.com",
            mobile="+919876543210",
            address="123 Main Street, Mumbai, Maharashtra 400001",
            password=get_password_hash("user123"),
            role="user",
            is_active=True
        )
        db.add(test_user)
        
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
                "description": "Essential period care items for basic comfort and hygiene."
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
                "description": "Enhanced comfort with premium products for your period care."
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
                "description": "Complete wellness package with premium products and comfort accessories."
            }
        ]
        
        for kit_data in kits_data:
            kit = Kit(**kit_data)
            db.add(kit)
        
        # Create sample fruits
        fruits_data = [
            {
                "name": "Apple Slices",
                "price": 50.0,
                "benefits": "Rich in fiber, helps with digestion",
                "emoji_icon": "🍎"
            },
            {
                "name": "Banana Chips",
                "price": 40.0,
                "benefits": "High potassium, reduces cramps",
                "emoji_icon": "🍌"
            },
            {
                "name": "Orange Wedges",
                "price": 60.0,
                "benefits": "Vitamin C boost, mood enhancement",
                "emoji_icon": "🍊"
            },
            {
                "name": "Mixed Berries",
                "price": 80.0,
                "benefits": "Antioxidants, natural pain relief",
                "emoji_icon": "🫐"
            },
            {
                "name": "Pomegranate",
                "price": 70.0,
                "benefits": "Iron rich, energy boosting",
                "emoji_icon": "🍎"
            },
            {
                "name": "Dates",
                "price": 45.0,
                "benefits": "Natural sweetness, magnesium for cramps",
                "emoji_icon": "🍯"
            }
        ]
        
        for fruit_data in fruits_data:
            fruit = Fruit(**fruit_data)
            db.add(fruit)
        
        # Create sample nutrients
        nutrients_data = [
            {
                "name": "Iron Supplement",
                "price": 120.0,
                "description": "Combats fatigue and weakness"
            },
            {
                "name": "Magnesium Complex",
                "price": 150.0,
                "description": "Reduces cramps and muscle tension"
            },
            {
                "name": "Calcium + D3",
                "price": 100.0,
                "description": "Bone health and mood support"
            },
            {
                "name": "Omega-3 Capsules",
                "price": 180.0,
                "description": "Anti-inflammatory, mood regulation"
            },
            {
                "name": "B-Complex",
                "price": 90.0,
                "description": "Energy boost and hormonal balance"
            }
        ]
        
        for nutrient_data in nutrients_data:
            nutrient = Nutrient(**nutrient_data)
            db.add(nutrient)
        
        # Create sample benefits
        benefits_data = [
            {
                "title": "Pain Relief Fruits",
                "description": "Natural ingredients that help reduce cramps and discomfort",
                "icon_emoji": "🍎",
                "display_order": 1
            },
            {
                "title": "Custom Nutrients",
                "description": "Supplements tailored to support your wellness during periods",
                "icon_emoji": "💊",
                "display_order": 2
            },
            {
                "title": "Flexible Delivery",
                "description": "Schedule deliveries that match your cycle perfectly",
                "icon_emoji": "📅",
                "display_order": 3
            },
            {
                "title": "Premium Quality",
                "description": "Only the best products for your comfort and health",
                "icon_emoji": "⭐",
                "display_order": 4
            }
        ]
        
        for benefit_data in benefits_data:
            benefit = Benefit(**benefit_data)
            db.add(benefit)
        
        # Create sample testimonials
        testimonials_data = [
            {
                "name": "Priya S.",
                "rating": 5,
                "testimonial_text": "The customizable kits are a game-changer! Love the fruit options and the convenience of delivery.",
                "location": "Mumbai",
                "is_featured": True
            },
            {
                "name": "Anita K.",
                "rating": 5,
                "testimonial_text": "Finally, a service that understands what women need. The nutrients really help with my symptoms.",
                "location": "Delhi",
                "is_featured": True
            },
            {
                "name": "Shreya M.",
                "rating": 5,
                "testimonial_text": "Perfect timing with the monthly reminders. Never miss my period prep!",
                "location": "Bangalore",
                "is_featured": True
            }
        ]
        
        for testimonial_data in testimonials_data:
            testimonial = Testimonial(**testimonial_data)
            db.add(testimonial)
        
        # Commit all changes
        db.commit()
        
        print("✅ Sample data created successfully!")
        print("🔑 Admin Login: admin@periodcare.com / admin123")
        print("👤 Test User: priya@example.com / user123")
        
    except Exception as e:
        print(f"❌ Error creating sample data: {e}")
        db.rollback()
    finally:
        db.close()


def init_database():
    """Initialize database with tables and sample data"""
    print("🗄️ Creating database tables...")
    create_tables()
    print("✅ Database tables created!")
    
    print("📝 Creating sample data...")
    create_sample_data()
    
    print("🎉 Database initialization complete!")


if __name__ == "__main__":
    init_database()
