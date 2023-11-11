import uvicorn
from fastapi import FastAPI

from routers import booking_router
from routers import computer_router
from routers import payment_router
from routers import user_router

app = FastAPI(title="Computer management API")

app.include_router(user_router, prefix="/api/v1")
app.include_router(computer_router, prefix="/api/v1")
app.include_router(booking_router, prefix="/api/v1")
app.include_router(payment_router, prefix="/api/v1")

if __name__ == '__main__':
    uvicorn.run(app, port=8000)
