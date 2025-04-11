from pydantic import BaseModel, EmailStr, Field


class AuthLoginSchema(BaseModel):
    email: EmailStr = Field(..., example="user@example.com", description="User's registered email address")
    password: str = Field(
        ..., 
        min_length=8, 
        max_length=128, 
        example="StrongPass123!",
        description="User's account password (min 8 characters)"
    )

    class Config:
        schema_extra = {
            "example": {
                "email": "user@example.com",
                "password": "StrongPass123!"
            }
        }


class Token(BaseModel):
    access_token: str = Field(..., example="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...")
    refresh_token: str = Field(..., example="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...")

    class Config:
        schema_extra = {
            "example": {
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
            }
        }


class SendOtpSchema(BaseModel):
    token: str = Field(..., example="encrypted_email_token_string", description="Encrypted token containing the email")

    class Config:
        schema_extra = {
            "example": {
                "token": "encrypted_email_token_string"
            }
        }


class VerifyOtpSchema(SendOtpSchema):
    otp: str = Field(
        ..., 
        min_length=6, 
        max_length=6, 
        example="123456",
        description="6-digit OTP sent to the user's email"
    )

    class Config:
        schema_extra = {
            "example": {
                "token": "encrypted_email_token_string",
                "otp": "123456"
            }
        }
