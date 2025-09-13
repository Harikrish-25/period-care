# Firebase Setup Guide for Period Care Backend

## Step 1: Create Firebase Project

1. **Go to Firebase Console**
   - Visit: https://console.firebase.google.com/
   - Click "Create a project" or "Add project"

2. **Project Setup**
   - Enter project name: `period-care-backend`
   - Choose to enable/disable Google Analytics (optional)
   - Click "Create project"

## Step 2: Enable Firestore Database

1. **In Firebase Console**
   - Go to your project dashboard
   - Click on "Firestore Database" in the left sidebar
   - Click "Create database"

2. **Security Rules**
   - Choose "Start in test mode" for development
   - Select a location closest to your users
   - Click "Done"

## Step 3: Generate Service Account Key

1. **Project Settings**
   - Click the gear icon (⚙️) next to "Project Overview"
   - Select "Project settings"

2. **Service Accounts Tab**
   - Go to "Service accounts" tab
   - Click "Generate new private key"
   - Download the JSON file
   - **IMPORTANT**: Rename it to `firebase-service-account.json`
   - Place it in your project root: `D:\period care_backend\firebase-service-account.json`

## Step 4: Update Environment Variables

Edit your `.env` file:

```env
# Environment Configuration
DATABASE_TYPE=firebase
FIREBASE_SERVICE_ACCOUNT_PATH=./firebase-service-account.json
FIREBASE_PROJECT_ID=your-actual-project-id

# Other settings...
SECRET_KEY=your-secret-key-here-change-this-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
ADMIN_WHATSAPP_NUMBER=+919999999999
FRONTEND_URL=http://localhost:5173
REMINDER_CHECK_TIME=09:00
SMTP_SERVER=smtp.gmail.com
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-app-password
REDIS_URL=redis://localhost:6379
DEBUG=True
ENVIRONMENT=development
```

## Step 5: Install Firebase Dependencies

```bash
pip install firebase-admin google-cloud-firestore
```

## Step 6: Initialize Firebase with Sample Data

```bash
python init_firebase.py
```

## Step 7: Start the Application

```bash
uvicorn app.main:app --reload
```

## Firestore Collections Structure

Your Firebase project will have these collections:

### `users`
```json
{
  "name": "string",
  "email": "string",
  "mobile": "string", 
  "address": "string",
  "password": "hashed_string",
  "role": "user|admin",
  "is_active": true,
  "reminder_sent": false,
  "last_order_date": "timestamp|null",
  "created_at": "timestamp",
  "updated_at": "timestamp"
}
```

### `kits`
```json
{
  "name": "string",
  "type": "basic|medium|premium",
  "base_price": 299.0,
  "image_url": "string",
  "included_items": "json_string",
  "description": "string",
  "is_available": true,
  "created_at": "timestamp",
  "updated_at": "timestamp"
}
```

### `orders`
```json
{
  "user_id": "string",
  "kit_id": "string", 
  "selected_fruits": "json_string",
  "selected_nutrients": "json_string",
  "scheduled_date": "date",
  "delivery_address": "string",
  "total_amount": 849.0,
  "status": "pending|completed|cancelled",
  "whatsapp_sent": false,
  "created_at": "timestamp",
  "updated_at": "timestamp"
}
```

### `fruits`
```json
{
  "name": "string",
  "price": 50.0,
  "benefits": "string",
  "emoji_icon": "🍎",
  "is_available": true,
  "created_at": "timestamp",
  "updated_at": "timestamp"
}
```

### `nutrients`
```json
{
  "name": "string", 
  "price": 120.0,
  "description": "string",
  "is_available": true,
  "created_at": "timestamp",
  "updated_at": "timestamp"
}
```

### `benefits`
```json
{
  "title": "string",
  "description": "string", 
  "icon_emoji": "🍎",
  "display_order": 1,
  "is_active": true,
  "created_at": "timestamp",
  "updated_at": "timestamp"
}
```

### `testimonials`
```json
{
  "name": "string",
  "rating": 5,
  "testimonial_text": "string",
  "location": "string",
  "is_featured": true,
  "is_active": true,
  "created_at": "timestamp", 
  "updated_at": "timestamp"
}
```

### `reminders`
```json
{
  "user_id": "string",
  "reminder_type": "monthly_reorder",
  "last_order_date": "date",
  "reminder_date": "timestamp|null",
  "status": "pending|sent|completed",
  "admin_notified": false,
  "created_at": "timestamp",
  "updated_at": "timestamp"
}
```

## Security Rules for Production

For production, update Firestore security rules:

```javascript
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    // Users can read/write their own data
    match /users/{userId} {
      allow read, write: if request.auth != null && request.auth.uid == userId;
    }
    
    // Admin can read/write everything
    match /{document=**} {
      allow read, write: if request.auth != null && 
        get(/databases/$(database)/documents/users/$(request.auth.uid)).data.role == 'admin';
    }
    
    // Public read access for kits, fruits, nutrients, benefits, testimonials
    match /kits/{kitId} {
      allow read: if true;
    }
    match /fruits/{fruitId} {
      allow read: if true;
    }
    match /nutrients/{nutrientId} {
      allow read: if true;
    }
    match /benefits/{benefitId} {
      allow read: if true;
    }
    match /testimonials/{testimonialId} {
      allow read: if true;
    }
  }
}
```

## Testing the Connection

After setup, test your Firebase connection:

```bash
python -c "from app.config.firebase import firebase_config; firebase_config.test_connection()"
```

## Troubleshooting

### Common Issues:

1. **"Service account file not found"**
   - Ensure `firebase-service-account.json` is in the project root
   - Check the file path in `.env`

2. **"Permission denied"**
   - Check Firestore security rules
   - Ensure service account has proper permissions

3. **"Project not found"**
   - Verify `FIREBASE_PROJECT_ID` in `.env`
   - Ensure project exists in Firebase Console

4. **Import errors**
   - Run: `pip install firebase-admin google-cloud-firestore`

## API Endpoints (Same as Before)

All existing API endpoints work the same way. The only difference is the backend storage is now Firebase Firestore instead of PostgreSQL/SQLite.

- **Swagger UI**: http://localhost:8000/docs
- **Default Login**: admin@periodcare.com / admin123

## Benefits of Firebase

1. **Real-time Updates**: Firestore provides real-time data synchronization
2. **Scalability**: Auto-scales based on usage
3. **Security**: Built-in authentication and security rules
4. **Offline Support**: Works offline and syncs when back online
5. **Global CDN**: Fast access from anywhere in the world
6. **No Server Management**: Fully managed by Google

Your Period Care backend is now ready to use Firebase! 🔥
