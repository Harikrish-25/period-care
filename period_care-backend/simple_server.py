#!/usr/bin/env python3
"""
Simple FastAPI server for Period Care Backend
This version includes real WhatsApp message sending to admin
Supports both SQLite and Firebase databases
"""

from fastapi import FastAPI, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import sqlite3
import os
import webbrowser
import urllib.parse
from typing import Dict, List
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Check database type from environment
DATABASE_TYPE = os.getenv('DATABASE_TYPE', 'sqlite').lower()

# Import Firebase service if using Firebase
if DATABASE_TYPE == 'firebase':
    try:
        from firebase_service import get_firebase_service
        print(f"🔥 Using Firebase database")
    except ImportError as e:
        print(f"❌ Firebase service not available: {e}")
        print("🔄 Falling back to SQLite")
        DATABASE_TYPE = 'sqlite'
else:
    print(f"🗄️ Using SQLite database")

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database file path
DATABASE = "periodcare.db"

# Admin WhatsApp number from environment variable or default
ADMIN_WHATSAPP = os.getenv('ADMIN_WHATSAPP', '917339625044')

class OrderRequest(BaseModel):
    kit_id: str  # Frontend sends kit_id as string
    selected_fruits: List[str] = []
    selected_nutrients: List[str] = []
    scheduled_date: str = ""
    delivery_address: str

class User(BaseModel):
    name: str
    email: str
    phone: str
    age: int
    password: str

class LoginRequest(BaseModel):
    username: str  # Frontend sends 'username' instead of 'email'
    password: str

class RegisterRequest(BaseModel):
    name: str
    email: str
    mobile: str  # Frontend sends 'mobile' instead of 'phone'
    address: str
    password: str

class Benefit(BaseModel):
    id: str = None
    title: str
    description: str
    icon: str

class Testimonial(BaseModel):
    id: str = None
    name: str
    rating: int
    text: str
    location: str

def init_database():
    """Initialize the database with required tables"""
    if DATABASE_TYPE == 'firebase':
        try:
            firebase_service = get_firebase_service()
            firebase_service.initialize_sample_data()
            print("✅ Firebase database initialized successfully")
        except Exception as e:
            print(f"❌ Firebase initialization failed: {e}")
            print("🔄 Consider checking your Firebase configuration")
    else:
        # SQLite initialization (existing code)
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
    
        # Create users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                phone TEXT NOT NULL,
                age INTEGER,
                address TEXT,
                password TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
    
        # Create kits table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS kits (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT,
                price REAL NOT NULL,
                image_url TEXT,
                features TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
    
        # Create orders table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                kit_id INTEGER NOT NULL,
                quantity INTEGER DEFAULT 1,
                total_amount REAL NOT NULL,
                status TEXT DEFAULT 'pending',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id),
                FOREIGN KEY (kit_id) REFERENCES kits (id)
            )
        ''')
    
        # Create benefits table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS benefits (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT NOT NULL,
                icon TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
    
        # Create testimonials table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS testimonials (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                rating INTEGER NOT NULL,
                text TEXT NOT NULL,
                location TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
    
        # Insert sample kits if they don't exist
        cursor.execute('SELECT COUNT(*) FROM kits')
        if cursor.fetchone()[0] == 0:
            sample_kits = [
                ("Basic Care Kit", "Essential period care items", 299.0, "/api/placeholder/300/200", "Pads, Pain Relief, Hygiene Products"),
                ("Premium Care Kit", "Complete period care solution", 599.0, "/api/placeholder/300/200", "Premium Pads, Pain Relief, Hygiene Products, Comfort Items"),
                ("Deluxe Care Kit", "Ultimate period care package", 899.0, "/api/placeholder/300/200", "Organic Pads, Advanced Pain Relief, Complete Hygiene Set, Comfort Items, Nutritional Supplements")
            ]
            cursor.executemany(
                'INSERT INTO kits (name, description, price, image_url, features) VALUES (?, ?, ?, ?, ?)',
                sample_kits
            )
    
        # Insert sample benefits if they don't exist
        cursor.execute('SELECT COUNT(*) FROM benefits')
        if cursor.fetchone()[0] == 0:
            sample_benefits = [
                ("Comfort & Relief", "Experience comfort during your period with our specially designed products", "💧"),
                ("Natural Ingredients", "All our products use natural, skin-friendly ingredients", "🌿"),
                ("24/7 Support", "Get round-the-clock support from our care team", "🤝"),
                ("Eco-Friendly", "Environmentally conscious products that care for you and the planet", "🌍")
            ]
            cursor.executemany(
                'INSERT INTO benefits (title, description, icon) VALUES (?, ?, ?)',
                sample_benefits
            )
    
        # Insert sample testimonials if they don't exist
        cursor.execute('SELECT COUNT(*) FROM testimonials')
        if cursor.fetchone()[0] == 0:
            sample_testimonials = [
                ("Priya Sharma", 5, "Amazing products! Made my periods so much more comfortable.", "Mumbai"),
                ("Anita Singh", 5, "The care kit is a game changer. Highly recommend!", "Delhi"),
                ("Kavya Reddy", 4, "Great quality and fast delivery. Very satisfied!", "Bangalore"),
                ("Neha Gupta", 5, "Finally found products that actually work. Thank you!", "Pune")
            ]
            cursor.executemany(
                'INSERT INTO testimonials (name, rating, text, location) VALUES (?, ?, ?, ?)',
                sample_testimonials
            )
    
        conn.commit()
        conn.close()
        print("✅ SQLite database initialized successfully")

def get_db_connection():
    """Get database connection"""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def send_whatsapp_message(phone_number: str, message: str) -> bool:
    """Send WhatsApp message notification - directly opens WhatsApp to send message"""
    try:
        # Clean the phone number (remove any non-digits)
        clean_phone = ''.join(filter(str.isdigit, phone_number))
        
        # Ensure phone number starts with country code
        if not clean_phone.startswith('91'):
            clean_phone = '91' + clean_phone
        
        # URL encode the message
        encoded_message = urllib.parse.quote(message)
        
        # Create WhatsApp Web URL
        whatsapp_url = f"https://web.whatsapp.com/send?phone={clean_phone}&text={encoded_message}"
        
        # Automatically open WhatsApp Web with the message
        webbrowser.open(whatsapp_url)
        
        return True
        
    except Exception as e:
        return False

# Database abstraction functions
def db_get_user_by_email(email: str):
    """Get user by email from database"""
    if DATABASE_TYPE == 'firebase':
        firebase_service = get_firebase_service()
        return firebase_service.get_user_by_email(email)
    else:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
        user = cursor.fetchone()
        conn.close()
        return user

def db_get_user_by_id(user_id: str):
    """Get user by ID from database"""
    if DATABASE_TYPE == 'firebase':
        firebase_service = get_firebase_service()
        return firebase_service.get_user_by_id(user_id)
    else:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
        user = cursor.fetchone()
        conn.close()
        return user

def db_create_user(user_data: dict):
    """Create user in database"""
    if DATABASE_TYPE == 'firebase':
        firebase_service = get_firebase_service()
        return firebase_service.create_user(user_data)
    else:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO users (name, email, phone, address, password)
            VALUES (?, ?, ?, ?, ?)
        ''', (user_data['name'], user_data['email'], user_data['phone'], 
              user_data['address'], user_data['password']))
        user_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return str(user_id)

def db_get_all_kits():
    """Get all kits from database"""
    if DATABASE_TYPE == 'firebase':
        firebase_service = get_firebase_service()
        return firebase_service.get_all_kits()
    else:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM kits')
        kits = cursor.fetchall()
        conn.close()
        return [dict(kit) for kit in kits]

def db_get_kit_by_id(kit_id: str):
    """Get kit by ID from database"""
    if DATABASE_TYPE == 'firebase':
        firebase_service = get_firebase_service()
        return firebase_service.get_kit_by_id(kit_id)
    else:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM kits WHERE id = ?', (kit_id,))
        kit = cursor.fetchone()
        conn.close()
        return dict(kit) if kit else None

def db_create_order(order_data: dict):
    """Create order in database"""
    if DATABASE_TYPE == 'firebase':
        firebase_service = get_firebase_service()
        return firebase_service.create_order(order_data)
    else:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO orders (user_id, kit_id, quantity, total_amount)
            VALUES (?, ?, ?, ?)
        ''', (order_data['user_id'], order_data['kit_id'], 
              order_data['quantity'], order_data['total_amount']))
        order_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return str(order_id)

def db_get_all_orders():
    """Get all orders from database"""
    if DATABASE_TYPE == 'firebase':
        firebase_service = get_firebase_service()
        return firebase_service.get_all_orders()
    else:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT 
                o.id, o.quantity, o.total_amount, o.status, o.created_at,
                u.name as user_name, u.email as user_email, u.phone as user_phone,
                k.name as kit_name, k.description as kit_description, k.price as kit_price
            FROM orders o
            JOIN users u ON o.user_id = u.id
            JOIN kits k ON o.kit_id = k.id
            ORDER BY o.created_at DESC
        ''')
        orders = cursor.fetchall()
        conn.close()
        return [dict(order) for order in orders]

def db_get_all_benefits():
    """Get all benefits from database"""
    if DATABASE_TYPE == 'firebase':
        firebase_service = get_firebase_service()
        return firebase_service.get_all_benefits()
    else:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM benefits')
        benefits = cursor.fetchall()
        conn.close()
        return [dict(benefit) for benefit in benefits]

def db_get_all_testimonials():
    """Get all testimonials from database"""
    if DATABASE_TYPE == 'firebase':
        firebase_service = get_firebase_service()
        return firebase_service.get_all_testimonials()
    else:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM testimonials')
        testimonials = cursor.fetchall()
        conn.close()
        return [dict(testimonial) for testimonial in testimonials]

@app.get("/")
def read_root():
    return {"message": "Period Care API Server is running!"}

@app.get("/api/kits")
def get_kits():
    """Get all available kits"""
    kits = db_get_all_kits()
    
    # Transform the database response to match frontend expectations
    transformed_kits = []
    for kit in kits:
        # Determine kit type based on price
        if kit['price'] < 400:
            kit_type = 'basic'
        elif kit['price'] < 700:
            kit_type = 'medium'
        else:
            kit_type = 'premium'
        
        # Convert features string to array of strings
        included_items = kit['features'].split(', ') if kit.get('features') else []
        
        transformed_kit = {
            'id': str(kit['id']),
            'name': kit['name'],
            'type': kit_type,
            'basePrice': kit['price'],
            'image': kit.get('image_url') or kit.get('image', ''),
            'includedItems': included_items,
            'description': kit['description']
        }
        transformed_kits.append(transformed_kit)
    
    return transformed_kits

@app.get("/api/users")
def get_users():
    """Get all users"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT id, name, email, phone, age, created_at FROM users')
    users = cursor.fetchall()
    conn.close()
    
    return [dict(user) for user in users]

@app.post("/api/users")
def create_user(user: User):
    """Create a new user"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
            INSERT INTO users (name, email, phone, age, password)
            VALUES (?, ?, ?, ?, ?)
        ''', (user.name, user.email, user.phone, user.age, user.password))
        
        user_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return {"message": "User created successfully", "user_id": user_id}
    
    except sqlite3.IntegrityError:
        conn.close()
        raise HTTPException(status_code=400, detail="Email already exists")

@app.post("/api/auth/register")
def register(user: RegisterRequest):
    """Register a new user"""
    try:
        # Check if user already exists
        existing_user = db_get_user_by_email(user.email)
        if existing_user:
            raise HTTPException(status_code=400, detail="Email already exists")
        
        # Create user data
        user_data = {
            "name": user.name,
            "email": user.email,
            "phone": user.mobile,
            "address": user.address,
            "password": user.password
        }
        
        user_id = db_create_user(user_data)
        
        return {
            "message": "User registered successfully",
            "user_id": user_id,
            "access_token": f"fake_token_user_{user_id}",
            "refresh_token": f"fake_refresh_token_user_{user_id}",
            "user": {
                "id": user_id,
                "name": user.name,
                "email": user.email,
                "phone": user.mobile,
                "address": user.address
            }
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Registration failed: {str(e)}")

@app.post("/api/auth/login")
def login(credentials: LoginRequest):
    """Login user"""
    user = db_get_user_by_email(credentials.username)
    
    if not user or user.get('password') != credentials.password:
        raise HTTPException(status_code=401, detail="Invalid email or password")
    
    return {
        "message": "Login successful",
        "access_token": f"fake_token_user_{user['id']}",
        "refresh_token": f"fake_refresh_token_user_{user['id']}",
        "user": {
            "id": user['id'],
            "name": user['name'],
            "email": user['email'],
            "phone": user.get('phone', ''),
            "address": user.get('address', '')
        }
    }

@app.post("/api/auth/logout")
def logout():
    """Logout user (simple implementation)"""
    return {"message": "Logged out successfully"}

@app.post("/api/orders")
def create_order(order: OrderRequest, authorization: Optional[str] = Header(None)):
    """Create a new order and send WhatsApp notification to admin"""
    
    # Extract user_id from authorization header
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Authorization header required")
    
    token = authorization.replace("Bearer ", "")
    if not token.startswith("fake_token_user_"):
        raise HTTPException(status_code=401, detail="Invalid token")
    
    try:
        user_id = token.replace("fake_token_user_", "")
    except ValueError:
        raise HTTPException(status_code=401, detail="Invalid token format")
    
    # Get user details
    user = db_get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Get kit details - try to find kit by ID first, then by name
    kit = db_get_kit_by_id(order.kit_id)
    if not kit:
        # Try to find by name if ID lookup failed
        all_kits = db_get_all_kits()
        for k in all_kits:
            if str(k.get('id')) == order.kit_id or order.kit_id.lower() in k.get('name', '').lower():
                kit = k
                break
    
    if not kit:
        raise HTTPException(status_code=404, detail="Kit not found")
    
    # Calculate total amount (assuming quantity = 1 for now)
    quantity = 1
    total_amount = kit['price'] * quantity
    
    # Create order data
    order_data = {
        'user_id': user_id,
        'kit_id': kit['id'],
        'quantity': quantity,
        'total_amount': total_amount,
        'selected_fruits': order.selected_fruits,
        'selected_nutrients': order.selected_nutrients,
        'scheduled_date': order.scheduled_date,
        'delivery_address': order.delivery_address
    }
    
    order_id = db_create_order(order_data)
    
    order_id = db_create_order(order_data)
    
    # Send WhatsApp notification to admin
    message = f"""🔔 NEW ORDER RECEIVED

Order ID: #{order_id}
Customer: {user['name']}
Phone: {user.get('phone', '')}
Email: {user['email']}

Kit: {kit['name']}
Quantity: {quantity}
Total Amount: ₹{total_amount}
Delivery Address: {order.delivery_address}

Selected Fruits: {', '.join(order.selected_fruits) if order.selected_fruits else 'None'}
Selected Nutrients: {', '.join(order.selected_nutrients) if order.selected_nutrients else 'None'}
Scheduled Date: {order.scheduled_date}

Please process this order promptly.
Period Care Admin"""
    
    # Send WhatsApp message to admin
    whatsapp_sent = send_whatsapp_message(ADMIN_WHATSAPP, message)
    
    return {
        "message": "Order placed successfully!",
        "id": str(order_id),  # Return as string to match frontend expectation
        "totalAmount": total_amount,  # Match frontend naming
        "whatsapp_sent": whatsapp_sent
    }

@app.get("/api/orders")
def get_orders():
    """Get all orders with user and kit details"""
    return db_get_all_orders()

@app.get("/api/orders/{order_id}")
def get_order(order_id: int):
    """Get specific order details"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT 
            o.id, o.quantity, o.total_amount, o.status, o.created_at,
            u.name as user_name, u.email as user_email, u.phone as user_phone,
            k.name as kit_name, k.description as kit_description, k.price as kit_price
        FROM orders o
        JOIN users u ON o.user_id = u.id
        JOIN kits k ON o.kit_id = k.id
        WHERE o.id = ?
    ''', (order_id,))
    
    order = cursor.fetchone()
    
    if not order:
        conn.close()
        raise HTTPException(status_code=404, detail="Order not found")
    
    conn.close()
    return dict(order)

@app.delete("/api/orders/{order_id}")
def delete_order(order_id: int):
    """Delete an order"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('DELETE FROM orders WHERE id = ?', (order_id,))
    
    if cursor.rowcount == 0:
        conn.close()
        raise HTTPException(status_code=404, detail="Order not found")
    
    conn.commit()
    conn.close()
    
    return {"message": "Order deleted successfully"}

# CMS Endpoints

@app.get("/api/cms/benefits")
def get_benefits():
    """Get all benefits"""
    return db_get_all_benefits()

@app.post("/api/cms/benefits")
def create_benefit(benefit: Benefit):
    """Create a new benefit"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute(
        'INSERT INTO benefits (title, description, icon) VALUES (?, ?, ?)',
        (benefit.title, benefit.description, benefit.icon)
    )
    
    benefit_id = cursor.lastrowid
    conn.commit()
    
    # Get the created benefit
    cursor.execute('SELECT id, title, description, icon FROM benefits WHERE id = ?', (benefit_id,))
    created_benefit = cursor.fetchone()
    conn.close()
    
    return dict(created_benefit)

@app.put("/api/cms/benefits/{benefit_id}")
def update_benefit(benefit_id: int, benefit: Benefit):
    """Update a benefit"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute(
        'UPDATE benefits SET title = ?, description = ?, icon = ? WHERE id = ?',
        (benefit.title, benefit.description, benefit.icon, benefit_id)
    )
    
    if cursor.rowcount == 0:
        conn.close()
        raise HTTPException(status_code=404, detail="Benefit not found")
    
    conn.commit()
    
    # Get the updated benefit
    cursor.execute('SELECT id, title, description, icon FROM benefits WHERE id = ?', (benefit_id,))
    updated_benefit = cursor.fetchone()
    conn.close()
    
    return dict(updated_benefit)

@app.delete("/api/cms/benefits/{benefit_id}")
def delete_benefit(benefit_id: int):
    """Delete a benefit"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('DELETE FROM benefits WHERE id = ?', (benefit_id,))
    
    if cursor.rowcount == 0:
        conn.close()
        raise HTTPException(status_code=404, detail="Benefit not found")
    
    conn.commit()
    conn.close()
    
    return {"message": "Benefit deleted successfully"}

@app.get("/api/cms/testimonials")
def get_testimonials():
    """Get all testimonials"""
    return db_get_all_testimonials()

@app.post("/api/cms/testimonials")
def create_testimonial(testimonial: Testimonial):
    """Create a new testimonial"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute(
        'INSERT INTO testimonials (name, rating, text, location) VALUES (?, ?, ?, ?)',
        (testimonial.name, testimonial.rating, testimonial.text, testimonial.location)
    )
    
    testimonial_id = cursor.lastrowid
    conn.commit()
    
    # Get the created testimonial
    cursor.execute('SELECT id, name, rating, text, location FROM testimonials WHERE id = ?', (testimonial_id,))
    created_testimonial = cursor.fetchone()
    conn.close()
    
    return dict(created_testimonial)

@app.put("/api/cms/testimonials/{testimonial_id}")
def update_testimonial(testimonial_id: int, testimonial: Testimonial):
    """Update a testimonial"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute(
        'UPDATE testimonials SET name = ?, rating = ?, text = ?, location = ? WHERE id = ?',
        (testimonial.name, testimonial.rating, testimonial.text, testimonial.location, testimonial_id)
    )
    
    if cursor.rowcount == 0:
        conn.close()
        raise HTTPException(status_code=404, detail="Testimonial not found")
    
    conn.commit()
    
    # Get the updated testimonial
    cursor.execute('SELECT id, name, rating, text, location FROM testimonials WHERE id = ?', (testimonial_id,))
    updated_testimonial = cursor.fetchone()
    conn.close()
    
    return dict(updated_testimonial)

@app.delete("/api/cms/testimonials/{testimonial_id}")
def delete_testimonial(testimonial_id: int):
    """Delete a testimonial"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('DELETE FROM testimonials WHERE id = ?', (testimonial_id,))
    
    if cursor.rowcount == 0:
        conn.close()
        raise HTTPException(status_code=404, detail="Testimonial not found")
    
    conn.commit()
    conn.close()
    
    return {"message": "Testimonial deleted successfully"}

if __name__ == "__main__":
    # Initialize database
    init_database()
    
    import uvicorn
    print("Starting Period Care API Server...")
    print(f"Admin WhatsApp: {ADMIN_WHATSAPP}")
    print("Server will be available at: http://localhost:8001")
    print("API Documentation at: http://localhost:8001/docs")
    
    uvicorn.run(app, host="127.0.0.1", port=8001)

# Initialize database when module is imported
init_database()