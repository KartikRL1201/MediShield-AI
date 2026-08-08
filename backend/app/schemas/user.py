from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from uuid import UUID
from datetime import datetime

# --- Validation Schemas ---
class UserBase(BaseModel):
    email: EmailStr
    first_name: Optional[str] = Field(None, min_length=4)
    last_name: Optional[str] = Field(None, min_length=4)

class UserCreate(UserBase):
    password: str = Field(min_length=4, description="Password must be at least 4 characters long")

class UserUpdate(BaseModel):
    first_name: Optional[str] = Field(None, min_length=4)
    last_name: Optional[str] = Field(None, min_length=4)
    password: Optional[str] = Field(None, min_length=4)

class UserResponse(UserBase):
    id: UUID
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

# --- Token Schemas ---
class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class TokenPayload(BaseModel):
    sub: Optional[str] = None
    type: Optional[str] = None

# --- Forgot Password Schemas ---
class ForgotPasswordRequest(BaseModel):
    email: EmailStr
