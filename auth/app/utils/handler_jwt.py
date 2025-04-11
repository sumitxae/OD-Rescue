from datetime import datetime, timedelta, timezone
import jwt
from ..config.config import Config
from fastapi import HTTPException

class JWTHandler:
    secret_key = Config.JWT_SECRET_KEY
    algorithm = Config.JWT_ALGORITHM
    expire_minutes = Config.JWT_ACCESS_TOKEN_EXPIRE_MINUTES

    @staticmethod
    def encode(payload: dict) -> str:
        expire = datetime.now(timezone.utc) + timedelta(minutes=JWTHandler.expire_minutes)
        payload.update({"exp": expire})
        return jwt.encode(
            payload, JWTHandler.secret_key, algorithm=JWTHandler.algorithm
        )

    @staticmethod
    def decode(token: str) -> dict:
        try:
            return jwt.decode(
                token, JWTHandler.secret_key, algorithms=[JWTHandler.algorithm]
            )
        except jwt.ExpiredSignatureError as exception:
            raise HTTPException(
                status_code=401,
                detail="Token has expired",
            ) from exception
        except jwt.DecodeError as exception:
            raise HTTPException(
                status_code=401,
                detail="Token is invalid",
            ) from exception

    @staticmethod
    def decode_expired(token: str) -> dict:
        try:
            return jwt.decode(
                token,
                JWTHandler.secret_key,
                algorithms=[JWTHandler.algorithm],
                options={"verify_exp": False},
            )
        except jwt.DecodeError as exception:
            raise HTTPException(
                status_code=401,
                detail="Token is invalid",
            ) from exception
        
    
    def blacklist_token(token: str):
        # Implement your token blacklisting logic here
        pass