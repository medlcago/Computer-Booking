from fastapi import HTTPException
from fastapi.requests import Request
from passlib.hash import bcrypt

from config import API_KEY


class AuthGuard:
    def __init__(self, name: str):
        self.name = name

    def __call__(self, request: Request):
        api_key = request.headers.get(self.name)
        if api_key != API_KEY:
            raise HTTPException(status_code=403, detail="Access is denied.")


class AuthService:
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        return bcrypt.verify(plain_password, hashed_password)

    @staticmethod
    def hash_password(password: str) -> str:
        return bcrypt.hash(password)


auth_guard_key = AuthGuard(name="x-api-key")
auth_service = AuthService()