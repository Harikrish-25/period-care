from sqlalchemy.orm import Session
from typing import Optional
from datetime import datetime, timedelta
from app.crud import user as user_crud
from app.schemas.user import UserCreate, UserLogin
from app.schemas.auth import AuthResponse
from app.config.security import (
    create_access_token, 
    create_refresh_token, 
    verify_password,
    get_password_hash
)


class AuthService:
    def __init__(self, db: Session):
        self.db = db
    
    def register_user(self, user_data: UserCreate) -> Optional[AuthResponse]:
        """Register a new user"""
        # Check if user already exists
        existing_user = user_crud.get_user_by_email(self.db, user_data.email)
        if existing_user:
            return None
        
        # Create new user
        new_user = user_crud.create_user(self.db, user_data)
        
        # Generate tokens
        access_token = create_access_token(data={"sub": new_user.email})
        refresh_token = create_refresh_token(data={"sub": new_user.email})
        
        return AuthResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer",
            user={
                "id": new_user.id,
                "name": new_user.name,
                "email": new_user.email,
                "role": new_user.role
            }
        )
    
    def login_user(self, login_data: UserLogin) -> Optional[AuthResponse]:
        """Authenticate and login user"""
        user = user_crud.authenticate_user(
            self.db, 
            login_data.email, 
            login_data.password
        )
        
        if not user or not user.is_active:
            return None
        
        # Generate tokens
        access_token = create_access_token(data={"sub": user.email})
        refresh_token = create_refresh_token(data={"sub": user.email})
        
        return AuthResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer",
            user={
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "role": user.role
            }
        )
    
    def get_current_user(self, email: str):
        """Get current user by email"""
        return user_crud.get_user_by_email(self.db, email)
    
    def refresh_token(self, email: str) -> Optional[AuthResponse]:
        """Generate new access token using refresh token"""
        user = user_crud.get_user_by_email(self.db, email)
        if not user or not user.is_active:
            return None
        
        access_token = create_access_token(data={"sub": user.email})
        refresh_token = create_refresh_token(data={"sub": user.email})
        
        return AuthResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer",
            user={
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "role": user.role
            }
        )
