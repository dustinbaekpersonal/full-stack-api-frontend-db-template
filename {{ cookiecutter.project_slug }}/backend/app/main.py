"""Instantiate FastAPI app by including routers defined."""
from fastapi import FastAPI

from app.api.items import router as items_router
from app.api.user import router as user_router

app = FastAPI(title="Stock Level API")

app.include_router(items_router)
app.include_router(user_router)


@app.get("/")
async def root():
    """Root api endpoint."""
    return {"message": "Welcome to Full Stack Dev!"}
