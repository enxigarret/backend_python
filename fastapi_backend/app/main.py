from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
import sentry_sdk

from app.api.api import api_router
from app.core.config import settings

from starlette.middleware.cors import CORSMiddleware

app = FastAPI(
    debug=settings.DEBUG,
    openapi_url="/api/docs.json",
    docs_url="/docs",
    redoc_url="/redoc"
)



# Set all CORS enabled origins
if settings.all_cors_origins:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.all_cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(api_router,prefix="/api")
@app.get("/")
async def root():
    return {"message": "Hello World"}