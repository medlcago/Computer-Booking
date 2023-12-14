from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from config import config


class APIKeyMiddleware(BaseHTTPMiddleware):
    def __init__(
            self,
            app,
            api_key: str,
    ):
        super().__init__(app)
        self.api_key = api_key

    async def dispatch(self, request: Request, call_next):
        api_v1_prefix = config.api.api_v1_prefix
        if request.url.path.startswith(api_v1_prefix):
            if request.headers.get("x-api-key") != self.api_key:
                return JSONResponse(status_code=403, content="Access is denied.")
        response = await call_next(request)
        return response
