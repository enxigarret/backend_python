
import uuid
from typing import Any
from fastapi import APIRouter, HTTPException, Depends
from app.core.config import settings
from sqlmodel import col ,delete, select,func

from app import crud

from  app.api.deps import SessionDep, get_current_active_superuser
from app.models import UserCreate, User, UserPublic , UserRegister
from app.core.db import engine
from sqlmodel import text
from app.utils import generate_new_account_email, send_email

router = APIRouter(tags=["tests"])

@router.get("/db-test")
def db_test():
    with engine.connect() as conn:
        result = conn.execute(text("SELECT 1"))
        return {"db_status": result.scalar()}