"""Base models for other models to inherit from."""
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """Base declarative model.

    This class becomes the parent class of other models.
    Model class is basically an abstraction of a table object in database.
    """

    async def create(self, db: AsyncSession):
        """Create a row in the database for given table."""
        db.add(self)
        await db.commit()
        await db.refresh(self)
        return True

    async def delete(self, db: AsyncSession):
        """Delete row from database for given table."""
        # self is instance of table object/class
        await db.delete(self)
        await db.commit()
        return True
