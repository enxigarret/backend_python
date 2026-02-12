from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi

from app.api.api import api_router
from app.core.config import settings

app = FastAPI(debug=settings.DEBUG,openapi_url="/api/docs.json",docs_url="/docs",redoc_url="/redoc")

app.include_router(api_router,prefix="/api")
@app.get("/")
async def root():
    return {"message": "Hello World"}