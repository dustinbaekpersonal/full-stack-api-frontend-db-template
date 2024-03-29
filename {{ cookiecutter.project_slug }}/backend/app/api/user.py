"""API calls for user are defined."""
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from loguru import logger
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.user import User
from app.schemas.user import UserIn

router = APIRouter(prefix="/user")


db_dependency = Annotated[AsyncSession, Depends(get_db)]


@router.get("/{email}")
async def get_user_by_email(email: str, db: db_dependency):
    """Retrieve user information by email.

    Args:
        email (str): email address of a user to find
        db (AsyncSession): single logical asynchronous database transaction
    """
    return await User.search(email, db)


@router.post("/")
async def create_user(payload: UserIn, db: db_dependency):
    """Create a user in Users table.

    Args:
        payload (UserIn): pydantic schema required to create a user in users table
        db (AsyncSession): single logical asynchronous database transaction
    """
    logger.info(f"Payload has type of {type(payload)} in form of {payload}.")
    logger.info(f"payload model_dump {payload.model_dump()}")
    # model_dump method creates a dictionary out of user input based on UserIn
    user: User = User(**payload.model_dump())

    try:
        await user.create(db)
    # handling unique constraint violation of email address in users table
    except IntegrityError as e:
        raise HTTPException(
            status_code=404,
            detail=f"There can't be more than one user with same email '{payload.email}'.",
        ) from e


@router.delete("/")
async def delete_user_by_email(email: str, db: db_dependency):
    """Delete user detail matching the given email.

    Args:
        email (str): email address of a user to find
        db (AsyncSession): single logical asynchronous database transaction
    """
    user = await User.search(email, db)
    return await user.delete(db)
