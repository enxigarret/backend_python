
import uuid
from typing import Any
from fastapi import Depends, HTTPException, status,APIRouter

from app.api.deps import CurrentUser, SessionDep
from app.models import Item, ItemPublic, ItemsPublic, ItemUpdate,Message

from fastapi import APIRouter


router = APIRouter(prefix="/items", tags=["items"])

@router.get("/",response_model=ItemPublic)
def read_items(
    session: SessionDep, 
    current_user: CurrentUser,
    skip: int = 0, limit: int = 100
) -> Any:
    """
    Retrieve items.
    """
    if current_user.is_superuser:
        count_statement= select(func.count()).select_from(Item)
        count = session.execute(count_statement).one()
        statement = (
            select(Item)
            .order_by(Item.created_at.desc())
            .offset(skip)
            .limit(limit)
        )
        items = session.execute(statement).all()
    else:
        count_statement= (
            select(func.count())
            .select_from(Item)
            .where(Item.owner_id == current_user.id)
        )
        count = session.execute(count_statement).one()
        statement = (
            select(Item)
            .where(Item.owner_id == current_user.id)
            .order_by(Item.created_at.desc())
            .offset(skip)
            .limit(limit)
        )
        items = session.execute(statement).all()
    return ItemPublic(data=items,count=count[0])

# @router.post("/login/access-token")
# def login_access_token(
#     session: SessionDep, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
# ) -> Token:
#     """
#     OAuth2 compatible token login, get an access token for future requests
#     """
#     user = crud.authenticate(
#         session=session, email=form_data.username, password=form_data.password
#     )
#     if not user:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Incorrect email or password",
#             headers={"WWW-Authenticate": "Bearer"},
#         )
#     elif not user.is_active:
#         raise HTTPException(status_code=400, detail="Inactive user")
#     access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
#     return Token(
#         access_token = security.create_access_token(
#             user.id,expires_delta = access_token_expires
#         )
#     )