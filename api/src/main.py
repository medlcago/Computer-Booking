import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from config import config
from routers import booking_router
from routers import computer_router
from routers import payment_router
from routers import ticket_router
from routers import user_router

app = FastAPI(title="Computer booking API")


@app.middleware("http")
async def api_key_middleware(request: Request, call_next):
    api_key = request.headers.get("x-api-key")
    if api_key != config.api.api_key:
        return JSONResponse(status_code=403, content="Access is denied.")

    response = await call_next(request)
    return response


app.include_router(user_router, prefix="/api/v1")
app.include_router(computer_router, prefix="/api/v1")
app.include_router(booking_router, prefix="/api/v1")
app.include_router(payment_router, prefix="/api/v1")
app.include_router(ticket_router, prefix="/api/v1")

if __name__ == '__main__':
    uvicorn.run(app, port=8000)
