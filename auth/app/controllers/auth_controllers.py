from fastapi import APIRouter, Depends, Request
from ..schemas.auth_schema import AuthLoginSchema,SendOtpSchema, VerifyOtpSchema
from ..schemas.user_schema import UserResetPasswordSchema, UserResponse,UsesForgotPassSchema
from ..services.auth_service import AuthService
from ..config.connect_db import get_db
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()


def get_auth_service(db: AsyncSession = Depends(get_db)):
    return AuthService(db)


@router.post("/login")
async def login(
    payload: AuthLoginSchema, service: AuthService = Depends(get_auth_service)
):
    return await service.login(payload)

@router.post("/send-otp")
async def send_otp(
    payload: SendOtpSchema, service: AuthService = Depends(get_auth_service)
):
    return await service.send_otp(payload)

@router.post("/verify-otp")
async def verify_otp(
    payload: VerifyOtpSchema, service: AuthService = Depends(get_auth_service)
):
    return await service.verify_otp(payload)


@router.post("/reset-password", response_model=UserResponse)
async def reset_password(
    payload: UserResetPasswordSchema,req: Request, service: AuthService = Depends(get_auth_service)
):
    return await service.reset_password(payload,req)

@router.post("/forgot-password")
async def forgot_password(
    payload: UsesForgotPassSchema, service: AuthService = Depends(get_auth_service)
):
    return await service.forgot_password(payload)
