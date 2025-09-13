# Firebase Setup Guide for Period Care Backend

## Step 1: Create Firebase Project
1. Go to Firebase Console: https://console.firebase.google.com/
2. Click "Add project" or "Create a project"
3. Enter project name: `period-care-app` (or your preferred name)
4. Choose whether to enable Google Analytics (optional)
5. Wait for project creation to complete

## Step 2: Enable Firestore Database
1. In your Firebase project, go to "Firestore Database"
2. Click "Create database"
3. Choose "Start in test mode" (for development)
4. Select a location (choose closest to your users)

## Step 3: Generate Service Account Key
1. Go to Project Settings (gear icon) → "Service accounts"
2. Click "Generate new private key"
3. Download the JSON file
4. Rename it to `firebase-service-account.json`
5. Place it in the `period_care-backend` folder

## Step 4: Configure Authentication
1. Go to "Authentication" → "Sign-in method"
2. Enable "Email/Password" provider
3. Optionally enable other providers as needed

## Step 5: Set up Environment Variables
Create a `.env` file in `period_care-backend` with:
```
FIREBASE_PROJECT_ID=your-project-id
FIREBASE_PRIVATE_KEY_ID=your-private-key-id
FIREBASE_PRIVATE_KEY="-----BEGIN PRIVATE KEY-----\nYOUR_PRIVATE_KEY\n-----END PRIVATE KEY-----\n"
FIREBASE_CLIENT_EMAIL=firebase-adminsdk-xxxxx@your-project-id.iam.gserviceaccount.com
FIREBASE_CLIENT_ID=your-client-id
WHATSAPP_ADMIN_NUMBER=7339625044
JWT_SECRET_KEY=your-super-secret-jwt-key
```

## Step 6: Test Firebase Connection
Run the setup script:
```bash
cd period_care-backend
python setup_firebase.py
```

## Step 7: Initialize Database Collections
Run the database initialization:
```bash
python init_db.py
```

## Security Notes
- Never commit `firebase-service-account.json` to version control
- Add it to your `.gitignore` file
- Keep your service account key secure
- Use environment variables for production deployments

## Troubleshooting
- If you get "default credentials not found", ensure the service account file is in the correct location
- Check that all required fields are present in the JSON file
- Verify your project ID matches in all configurations