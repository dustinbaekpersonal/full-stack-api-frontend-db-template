"""Declarative ORM models for user."""
from fastapi import HTTPException
from loguru import logger
from sqlalchemy import Integer, String, UniqueConstraint, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class User(Base):
    """User orm model class.

    Attributes:
        id (int): unique ID assigned for each user
        first_name (str): first name of the user
        last_name (str): last name of the user
        email (str): email of the user

    Methods:
        __repr__: to print out User class with attributes
        search: find a list of user details by email
    """

    __tablename__ = "users"
    __table_args__ = (UniqueConstraint("email", name="unique_hash_user"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String, nullable=False)
    full_name: Mapped[str] = mapped_column(String)
    email: Mapped[str] = mapped_column(String, nullable=False)
    password: Mapped[str] = mapped_column(String, nullable=False)

    def __repr__(self) -> str:
        """Return string representation of class."""
        return (
            f"User detail: ID={self.id}, User Name={self.username} \n"
            + f"Email={self.email}"
        )

    @classmethod
    async def search(cls, email: str, db: AsyncSession):
        """Class method to search user by email."""
        statement = select(cls).where(cls.email == email)
        result = await db.execute(statement)
        result = result.scalars().first()

        logger.debug(f"Users that have email:{email} is {result}")

        if not result:
            raise HTTPException(
                status_code=404, detail=f"User with email '{email}' not found."
            )
        return result
