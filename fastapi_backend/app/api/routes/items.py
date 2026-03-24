
import logging
import uuid
from typing import Any
from fastapi import Depends, HTTPException, status,APIRouter

from app.api.deps import CurrentUser, SessionDep
from app.models import Item, ItemCreate, ItemPublic, ItemsPublic, ItemUpdate,Message
from sqlalchemy import select, func
from datetime import datetime, timezone

from fastapi import APIRouter


router = APIRouter( tags=["items"])

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

@router.get("/",response_model=ItemsPublic)
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
        count = session.exec(count_statement).one()
        statement = (
            select(Item)
            .order_by(Item.created_at.desc())
            .offset(skip)
            .limit(limit)
        )
        items = session.exec(statement).scalars().all()
    else:
        count_statement= (
            select(func.count())
            .select_from(Item)
            .where(Item.owner_id == current_user.id)
        )
        count = session.exec(count_statement).one()
        statement = (
            select(Item)
            .where(Item.owner_id == current_user.id)
            .order_by(Item.created_at.desc())
            .offset(skip)
            .limit(limit)
        )
        items = session.exec(statement).scalars().all()
    logger.info("Current count: %s", count)
    return ItemsPublic(data=items,count=count[0])


@router.get("/{item_id}", response_model=ItemPublic)
def read_item(
    session: SessionDep,
    current_user: CurrentUser,
    item_id: uuid.UUID, 
) -> Any:
    """
    Get a specific item by id.
    """
    item = session.get(Item, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    if not current_user.is_superuser and ( item.owner_id != current_user.id ):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return item

@router.post("/", response_model=ItemPublic)
def create_item(
    *,
    session: SessionDep, 
    current_user: CurrentUser,
    item_in: ItemCreate
) -> Any:
    """
    Create new item.
    """
    item = Item.model_validate(item_in,update={"owner_id": current_user.id})

    session.add(item)
    session.commit()
    session.refresh(item)
    return item


@router.put("/{item_id}", response_model=ItemPublic)
def update_item(
    *,
    session: SessionDep, 
    current_user: CurrentUser,
    item_id: uuid.UUID, 
    item_in: ItemUpdate
) -> Any:
    """
    Update an item.
    """
    item = session.get(Item, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    if not current_user.is_superuser and ( item.owner_id != current_user.id ):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    
 
    update_data = item_in.model_dump(exclude_unset=True) # exclude_unset=True to only include fields that were provided in the request
    item.sqlmodel_update(update_data)
    session.add(item)
    session.commit()
    session.refresh(item)
    return item
    
@router.delete("/{item_id}", response_model=Message)
def delete_item(
    *,
    session: SessionDep, 
    current_user: CurrentUser,
    item_id: uuid.UUID, 
) -> Message:
    """
    Delete an item.
    """
    item = session.get(Item, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    if not current_user.is_superuser and ( item.owner_id != current_user.id ):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    
    session.delete(item)
    session.commit()
    return Message(message="Item deleted successfully")








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

