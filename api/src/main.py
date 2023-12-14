import uvicorn
from fastapi import FastAPI

from api.middlewares import APIKeyMiddleware
from config import config
from routers import booking_router
from routers import computer_router
from routers import payment_router
from routers import ticket_router
from routers import user_router

api_v1_prefix = config.api.api_v1_prefix
api_key = config.api.api_key

app = FastAPI(title="Computer booking API")
app.add_middleware(APIKeyMiddleware, api_key=api_key)

app.include_router(user_router, prefix=api_v1_prefix)
app.include_router(computer_router, prefix=api_v1_prefix)
app.include_router(booking_router, prefix=api_v1_prefix)
app.include_router(payment_router, prefix=api_v1_prefix)
app.include_router(ticket_router, prefix=api_v1_prefix)

if __name__ == '__main__':
    uvicorn.run(app, port=8000)
