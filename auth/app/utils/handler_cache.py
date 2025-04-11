import time
from typing import Optional

class InMemoryOTPStore:
    _store = {}

    @classmethod
    def set(cls, key: str, otp: str, ttl: int = 300):
        expiry = time.time() + ttl  # default 5 minutes
        cls._store[key] = {"otp": otp, "expiry": expiry}

    @classmethod
    def get(cls, key: str) -> Optional[str]:
        data = cls._store.get(key)
        if not data:
            return None
        if time.time() > data["expiry"]:
            cls._store.pop(key, None)  # expired, clean it
            return None
        return data["otp"]

    @classmethod
    def delete(cls, key: str):
        cls._store.pop(key, None)
