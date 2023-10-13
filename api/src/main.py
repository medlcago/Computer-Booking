import uvicorn
from fastapi import FastAPI

from routers import user_operations_router, computer_operations_router

app = FastAPI(title="Test Project")

app.include_router(user_operations_router, prefix="/api/v1")
app.include_router(computer_operations_router, prefix="/api/v1")

if __name__ == '__main__':
    uvicorn.run(app)
