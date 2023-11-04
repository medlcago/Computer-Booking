import uvicorn
from fastapi import FastAPI

from routers import booking_operations_router
from routers import computer_operations_router
from routers import user_operations_router
from routers import payment_operations_router

app = FastAPI(title="Club management API")

app.include_router(user_operations_router, prefix="/api/v1")
app.include_router(computer_operations_router, prefix="/api/v1")
app.include_router(booking_operations_router, prefix="/api/v1")
app.include_router(payment_operations_router, prefix="/api/v1")

if __name__ == '__main__':
    uvicorn.run(app, port=8000)
