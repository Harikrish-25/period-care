# Period Care Backend

A complete FastAPI backend for a women's period care e-commerce website.

## Features

- **User Management**: Registration, login, profile management
- **Product Management**: Period care kits, fruits, and nutrients
- **Order System**: One-time orders with customizable add-ons
- **Admin Panel**: Complete admin functionality for managing products and orders
- **WhatsApp Integration**: Automatic notifications for new orders
- **Monthly Reminders**: Automated reminder system for reorders
- **Content Management**: Benefits and testimonials management

## Quick Start

### Prerequisites

- Python 3.8+
- PostgreSQL
- Redis

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd period-care-backend
```

2. Create virtual environment:
```bash
python -m venv venv
venv\Scripts\activate  # On Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
copy .env.example .env
# Edit .env with your configuration
```

5. Set up database:
```bash
# Create PostgreSQL database
createdb periodcare

# Run migrations
alembic upgrade head
```

6. Start Redis server:
```bash
redis-server
```

7. Run the application:
```bash
uvicorn app.main:app --reload
```

8. Start background tasks:
```bash
python -m app.tasks.reminder_tasks
```

## API Documentation

Once the server is running, visit:
- API Documentation: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Default Users

- **Admin**: admin@periodcare.com / admin123
- **Test User**: priya@example.com / user123

## Project Structure

```
period-care-backend/
├── app/
│   ├── main.py                 # FastAPI application
│   ├── config/                 # Configuration files
│   ├── models/                 # Database models
│   ├── schemas/                # Pydantic schemas
│   ├── api/v1/                 # API endpoints
│   ├── crud/                   # Database operations
│   ├── services/               # Business logic
│   └── tasks/                  # Background tasks
├── requirements.txt            # Python dependencies
├── .env                        # Environment variables
└── README.md                   # This file
```

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| DATABASE_URL | PostgreSQL connection string | - |
| SECRET_KEY | JWT secret key | - |
| ADMIN_WHATSAPP_NUMBER | Admin WhatsApp number | +919999999999 |
| FRONTEND_URL | Frontend application URL | http://localhost:5173 |
| REMINDER_CHECK_TIME | Daily reminder check time | 09:00 |

## License

This project is licensed under the MIT License.
