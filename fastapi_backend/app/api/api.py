from fastapi import APIRouter

from app.api.routes import items, login,  users, utils
from app.core.config import settings

api_router = APIRouter()
api_router.include_router(login.router, prefix="/auth", tags=["auth"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
# api_router.include_router(items.router, prefix="/items", tags=["items"])

# if settings.ENVIRONMENT == "local":
#     api_router.include_router(privates.router, prefix="/privates", tags=["privates"])
