from fastapi import HTTPException
from fastapi.requests import Request
from config import API_KEY


class AuthGuard:
    def __init__(self, name: str):
        self.name = name

    def __call__(self, request: Request):
        api_key = request.headers.get(self.name)
        if api_key != API_KEY:
            raise HTTPException(status_code=403, detail="Access is denied.")


auth_guard_key = AuthGuard(name="x-api-key")
