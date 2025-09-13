from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.config.database import create_tables
from app.config.firebase import firebase_config
from app.api.v1 import auth, users, kits, orders, fruits, nutrients, admin, cms, reminders, whatsapp
from app.config.settings import settings

# Create FastAPI application
app = FastAPI(
    title="Period Care Backend API",
    description="A complete backend for women's period care e-commerce platform",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create database tables on startup
@app.on_event("startup")
async def startup_event():
    if settings.database_type == "firebase":
        # Initialize Firebase
        firebase_config.test_connection()
        print("🔥 Firebase database initialized!")
    else:
        # Initialize SQL database
        create_tables()
        print("�️ SQL database initialized!")
    
    print("�🚀 Period Care API started successfully!")
    print(f"📚 API Documentation: http://localhost:8000/docs")
    print(f"🔧 Environment: {settings.environment}")
    print(f"🗄️ Database Type: {settings.database_type}")

# Health check endpoint
@app.get("/")
def read_root():
    return {
        "message": "Period Care API is running! 🩷",
        "version": "1.0.0",
        "docs": "/docs",
        "status": "healthy"
    }

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "message": "Period Care API is running smoothly! 💕"
    }

# Include API routers
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Authentication"])
app.include_router(users.router, prefix="/api/v1/users", tags=["Users"])
app.include_router(kits.router, prefix="/api/v1/kits", tags=["Kits"])
app.include_router(orders.router, prefix="/api/v1/orders", tags=["Orders"])
app.include_router(fruits.router, prefix="/api/v1/fruits", tags=["Fruits"])
app.include_router(nutrients.router, prefix="/api/v1/nutrients", tags=["Nutrients"])
app.include_router(reminders.router, prefix="/api/v1/reminders", tags=["Reminders"])
app.include_router(cms.router, prefix="/api/v1/cms", tags=["Content Management"])
app.include_router(admin.router, prefix="/api/v1/admin", tags=["Admin"])
app.include_router(whatsapp.router, prefix="/api/v1/whatsapp", tags=["WhatsApp"])

# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    return HTTPException(
        status_code=500,
        detail=f"Internal server error: {str(exc)}"
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
