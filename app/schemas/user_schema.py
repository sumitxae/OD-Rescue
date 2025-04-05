from typing import Optional
from pydantic import BaseModel, EmailStr, Field, field_validator
from datetime import datetime


# --- Custom Validator for Phone ---
def validate_phone_basic(v: Optional[str]) -> Optional[str]:
    if v and not v.isdigit():
        raise ValueError("Phone must contain only digits")
    return v


# --- Base User Schema ---
class UserBase(BaseModel):
    user_name: str = Field(..., example="john_doe", description="Alphanumeric username")
    phone: Optional[str] = Field(None, example="9876543210", description="Optional 10-digit phone number")
    email: EmailStr = Field(..., example="john@example.com", description="Valid email address")

    @field_validator('phone')
    def validate_phone(cls, v):
        return validate_phone_basic(v)


# --- Schema for Creating a User ---
class UserCreateSchema(UserBase):
    role_id: int = Field(..., example=2, description="Role ID assigned to the user")
    account_id: Optional[int] = Field(None, example=1001, description="Optional account reference")
    campus_id: Optional[int] = Field(None, example=201, description="Optional campus reference")


# --- Schema for Password Reset ---
class UserResetPasswordSchema(BaseModel):
    password: str = Field(..., min_length=8, example="NewStrongPassword123")
    confirm_password: str = Field(..., min_length=8, example="NewStrongPassword123")

    class Config:
        from_attributes = True


# --- Response Schema for a User ---
class UserResponse(BaseModel):
    user_id: int = Field(..., example=1)
    user_name: str = Field(..., example="john_doe")
    phone: Optional[str] = Field(None, example="9876543210")
    password: Optional[str] = None 
    email: EmailStr = Field(..., example="john@example.com")
    is_active: bool = Field(default=True)
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    created_by: Optional[str] = Field(None, example="admin")
    updated_by: Optional[str] = Field(None, example="admin")
    role_id: Optional[int] = Field(None, example=2)

    model_config = {
        "from_attributes": True,
        "arbitrary_types_allowed": True,
        "populate_by_name": True
    }


# --- Schema for Forgot Password Flow ---
class UsesForgotPassSchema(BaseModel):
    email: EmailStr = Field(..., example="john@example.com", description="Email address to receive OTP")

    class Config:
        from_attributes = True
