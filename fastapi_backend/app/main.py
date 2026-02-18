from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from fastapi.routing import APIRoute    
import sentry_sdk

from app.api.api import api_router
from app.core.config import settings

from starlette.middleware.cors import CORSMiddleware

#custome openapi schema to group endpoints by tags in the documentation
def custom_generate_unique_id(route:APIRoute)-> str:
    return f"{route.tags[0]}_{route.name}"

if settings.ENVIRONMENT == "production" and settings.SENTRY_DSN:
    sentry_sdk.init(
        dsn=settings.SENTRY_DSN,
        traces_sample_rate=1.0,
    )

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