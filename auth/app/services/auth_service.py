from sqlalchemy.ext.asyncio import AsyncSession
from ..repositories.user_repository import UserRepository
from ..schemas.auth_schema import AuthLoginSchema, Token, SendOtpSchema, VerifyOtpSchema
from ..schemas.user_schema import UserResetPasswordSchema, UsesForgotPassSchema
from ..utils.handler_password import PasswordHandler
from ..utils.handler_jwt import JWTHandler
from datetime import datetime, timezone, timedelta
from ..utils.handler_otp import OtpHandler
from ..utils.handler_encryption import helper
from fastapi.responses import JSONResponse
from fastapi import Request, HTTPException, status


class AuthService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.user_repository = UserRepository(db)

    async def login(self, payload: AuthLoginSchema):
        user = await self.user_repository.get_user_by_email(payload.email)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        if not PasswordHandler.verify(
            hashed_password=user.password, plain_password=payload.password
        ):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect password")

        return Token(
            access_token=JWTHandler.encode(
                payload={
                    "id": user.user_id,
                    "email": user.email,
                    "roles": user.role_id,
                    "name": user.user_name,
                }
            ),
            refresh_token=JWTHandler.encode(payload={"sub": "refresh-token"}),
        )

    async def refresh_token(self, access_token: str, refresh_token: str) -> Token:
        try:
            token_payload = JWTHandler.decode(access_token)
            refresh_payload = JWTHandler.decode(refresh_token)
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))

        if refresh_payload.get("sub") != "refresh-token":
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")

        return Token(
            access_token=JWTHandler.encode(payload={"user_id": token_payload.get("user_id")}),
            refresh_token=JWTHandler.encode(payload={"sub": "refresh-token"}),
        )

    async def send_otp(self, payload: SendOtpSchema):
        try:
            decrypted_email = helper.decrypt(payload.token)
        except Exception:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid token")

        user = await self.user_repository.get_user_by_email(decrypted_email)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        otp_handler = OtpHandler(otp_length=6)
        await otp_handler.send_otp(email=decrypted_email)

        return {
            "token": JWTHandler.encode(
                payload={
                    "email": decrypted_email,
                    "exp": datetime.now(timezone.utc) + timedelta(minutes=5),
                }
            )
        }

    async def verify_otp(self, payload: VerifyOtpSchema):
        try:
            decode_token = JWTHandler.decode(payload.token)
        except Exception:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid token")

        extract_email = decode_token.get("email")
        if not extract_email:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email not found in token")

        user = await self.user_repository.get_user_by_email(extract_email)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        otp_handler = OtpHandler(otp_length=6)
        if not otp_handler.verify_otp(extract_email, payload.otp):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid OTP")

        response = JSONResponse(content={"message": "OTP verified successfully"})
        response.set_cookie(
            key="token",
            value=payload.token,
            secure=False,
            httponly=True,
            samesite="lax",
            max_age=300
        )
        return response

    async def reset_password(self, payload: UserResetPasswordSchema, req: Request):
        token = req.cookies.get("token")
        if not token:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token not found")

        try:
            decode_token = JWTHandler.decode(token)
        except Exception:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid token")

        email = decode_token.get("email")
        if not email:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email not found in token")

        user = await self.user_repository.get_user_by_email(email)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        if payload.password != payload.confirm_password:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Passwords do not match")

        user.password = PasswordHandler.hash(payload.password)
        return await self.user_repository.update_user(user.user_id, {"password": user.password})

    async def forgot_password(self, payload: UsesForgotPassSchema):
        user = await self.user_repository.get_user_by_email(payload.email)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        otp_handler = OtpHandler(otp_length=6)
        await otp_handler.send_otp(email=payload.email)

        return {
            "token": JWTHandler.encode(
                payload={
                    "email": payload.email,
                    "exp": datetime.now(timezone.utc) + timedelta(minutes=5),
                }
            )
        }
